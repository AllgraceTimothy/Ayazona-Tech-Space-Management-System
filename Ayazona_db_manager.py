import sqlite3
from datetime import datetime
import traceback
import flet as ft

def save_customer(username, email, password):
  try:
    conn = sqlite3.connect('Ayazona_Database')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (user_name, email, passwd) VALUES (?,?,?)", (username, email, password))
    conn.commit()
    conn.close()
  except sqlite3.IntegrityError:
    return False
  return True

def save_manager(username, email, password):
  try:
    conn = sqlite3.connect('Ayazona_Database')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO managers (user_name, email, passwd) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()
  except sqlite3.IntegrityError:
    return False
  return True

def verify_login(user_type, user_name, password, secret_key=None):
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()
  table = "managers" if user_type == "manager" else "customers"
  cursor.execute(f"SELECT * FROM {table} WHERE user_name = ? AND passwd = ?", (user_name, password))
  user = cursor.fetchone()
  conn.close()

  if user is not None:
    customer_id = user[0]
    customer_name = user[1]
    return True, customer_id, customer_name
  return None

def add_new_products(item_name, quantity, unit_price):
  try:
    conn = sqlite3.connect('Ayazona_Database')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (product_name, quantity, unit_price) VALUES (?, ?, ?)", (item_name, quantity, unit_price))
    conn.commit()
    conn.close()
  except sqlite3.IntegrityError:
    return False
  return True

def update_stock_levels(product_id, new_stock, new_price):
  try:
    conn = sqlite3.connect('Ayazona_Database')
    cursor = conn.cursor()
    
    updates = []
    values = []

    if new_stock is not None:
      updates.append("quantity = quantity + ?")
      values.append(new_stock)

    if new_price is not None:
      updates.append("unit_price = ?")
      values.append(new_price)

    if not updates:
      print("No updates specified.")
      return False
    
    values.append(product_id)

    query = f"UPDATE products SET {','.join(updates)} WHERE product_id = ?"
    cursor.execute(query, tuple(values))

    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
      print(f"No rows updated. check if product_id {product_id} exists.")
      return False
    
    return True
  except sqlite3.Error as e:
    print(f"Database error: {e}")
  except Exception as e:
    print(f"Error in updating stock: {e}")
    return False
  
def navigate_product_pages(offset, items_per_page):
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()
  cursor.execute(
    "SELECT product_id, product_name, quantity, unit_price FROM products LIMIT ? OFFSET ?", (items_per_page, offset)
  )
  rows = cursor.fetchall()
  conn.close()
  return rows

def get_inventory_count():
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()
  cursor.execute("SELECT COUNT(*) FROM products")
  count = cursor.fetchone()[0]
  conn.close()
  return count

def get_product_details():
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()
  cursor.execute('SELECT product_id, product_name, quantity, unit_price FROM products')
  result = cursor.fetchall()
  conn.close()
  return result

def finalize_purchase(customer_id, purchases):
  try:
    conn = sqlite3.connect('Ayazona_Database')
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE customer_id=?", (customer_id,))
    if not cursor.fetchone():
      conn.close()
      return False, "Customer not found"
    
    cursor.execute("BEGIN")
    
    for product_id, product_name, quantity, unit_price in purchases:
      cursor.execute("SELECT quantity FROM products WHERE product_id=?", (product_id,))
      result = cursor.fetchone()
      if not result or result[0] < quantity:
        conn.rollback()
        conn.close()
        return False, f"Insufficient stock for the product '{product_name}'"

      cursor.execute("UPDATE products SET quantity = quantity - ? WHERE product_id=? AND quantity >= ?", (quantity, product_id, quantity))
      
      total_price = unit_price * quantity
      cursor.execute(
        """
        INSERT INTO purchases (customer_id, product_id, quantity, total_price, purchase_date)
        VALUES (?,?,?,?,?)
        """,
        (customer_id, product_id, quantity, total_price, datetime.now()),
      )

      conn.commit()
    conn.close()
    return True, "Purchase successfully completed"
    
  except Exception as e:
    traceback.print_exc()
    conn.rollback()
    return False, f"An error occurred while finalizing purchase: {e}"
  
def generate_receipt(page: ft.Page):
  customer_id = page.session.get('customer_id')
  purchase_time = page.session.get('Purchase_time')

  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()

  cursor.execute("""
    SELECT p.product_id, pr.product_name, p.quantity, pr.unit_price, p.total_price, p.purchase_date
    FROM purchases p
    JOIN products pr ON p.product_id = pr.product_id
    WHERE p.customer_id = ? AND p.purchase_date >= ?
    ORDER BY p.purchase_date DESC
  """, (customer_id, purchase_time))

  purchase_data = cursor.fetchall()
  conn.close()

  if not purchase_data:
    print("No transaction data found")
    
  return purchase_data

def transaction_history(customr_id):
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()

  cursor.execute("""
    SELECT p.product_id, pr.product_name, p.quantity, pr.unit_price, p.total_price, p.purchase_date
    FROM purchases p
    JOIN products pr ON p.product_id = pr.product_id
    WHERE p.customer_id = ?
    ORDER BY p.purchase_date DESC
  """, (customr_id,)), 
  pr_history = cursor.fetchall()
  conn.close()
  if not pr_history:
    print("No transaction history found")
  else:
    return pr_history
  
def change_cust_password(email, new_password) -> None:
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()
  cursor.execute("UPDATE customers SET passwd = ? WHERE email = ?", (new_password, email))
  conn.commit()
  conn.close()
  return True

def change_manager_password(email, new_password, secret_key=None) -> None:
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()
  cursor.execute("UPDATE managers SET passwd = ? WHERE email = ?", (new_password, email))
  conn.commit()
  conn.close()
  return True

def get_customer_details():
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()
  cursor.execute('SELECT customer_id, user_name, email, passwd FROM customers')
  result = cursor.fetchall()
  conn.close()
  return result

def get_manager_details():
  conn = sqlite3.connect('Ayazona_Database')
  cursor = conn.cursor()
  cursor.execute('SELECT manager_id, user_name, email, passwd FROM managers')
  result = cursor.fetchall()
  conn.close()
  return result