import flet as ft
from Ayazona_db_manager import get_inventory_count, navigate_product_pages

class CustomerDashboard(ft.UserControl):
  def __init__(self, page: ft.Page, **kwargs):
    """Initializes the customer dashboard with page settings and components."""
    super().__init__(**kwargs)
    self.page = page
    self.page.views.clear()
    self.page.title = "Customer's Dashboard"
    self.page.window.width = 850
    self.page.window.height = 700

    self.customer_id = self.page.session.get('customer_id')

    self.current_page = 1
    self.rows_per_page = 5
    self.total_items = get_inventory_count()
    self.data = []

    self.selected_items = []

    self.table = ft.DataTable(
      data_row_max_height=65,
      columns=[
        ft.DataColumn(ft.Text("Product ID")),
        ft.DataColumn(ft.Text("Product Name")),
        ft.DataColumn(ft.Text("Quantity")),
        ft.DataColumn(ft.Text("Unit Price", width=110)),
        ft.DataColumn(ft.Text("Purchase Quantity")),
      ],
      rows=[]
    )

    self.page_label = ft.Text(f"Page {self.current_page} of {(self.total_items + self.rows_per_page - 1) // self.rows_per_page}")
    self.prev_button = ft.ElevatedButton("Previous", on_click=self.on_prev_click, disabled=(self.current_page == 1))
    self.next_button = ft.ElevatedButton("Next", on_click=self.on_next_click, disabled=(self.current_page * self.rows_per_page >= self.total_items))
    self.logout_btn = ft.ElevatedButton(
      text="Logout",
      on_click=self.logout,
      width=100,
      height=35,
      bgcolor=ft.colors.BLUE_700,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=16),
      )
    )
    self.check_purchases_btn = ft.ElevatedButton(
      text="View Cart",
      on_click=self.to_check_purchases,
      disabled=True,
      width=150,
      height=35,
      style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=16),
      )
    )
    self.transaction_history_btn = ft.ElevatedButton(
      text="View Transaction History",
      on_click=self.to_transaction_history,
      width=230,
      height=35,
      bgcolor=ft.colors.GREEN_800,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=16),
      )
    )

    self.load_inventory_data()

  def load_inventory_data(self):
    """Fetches inventory data for the current page."""
    self.page.clean()
    offset = (self.current_page - 1) * self.rows_per_page
    self.data = navigate_product_pages(offset, self.rows_per_page)

    if not self.data:
      self.page.snack_bar = ft.SnackBar(ft.Text("No inventory data found"), open=True)
      self.update_pagination_btns()
      self.page.update()
      return
    
    self.table.rows.clear()
    # Fills table with product data
    for row in self.data:
      product_id = row[0]      
      product_name = row[1]
      available_stock = int(row[2])
      unit_price = float(row[3])

      self.table.rows.append(
        ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(product_id)),
            ft.DataCell(ft.Text(product_name)),
            ft.DataCell(ft.Text(str(available_stock))),  # Quantity
            ft.DataCell(ft.Text(f"Ksh {unit_price:.2f}")),  # Unit Price
            ft.DataCell(ft.TextField(keyboard_type="number", width=100, on_change=self.on_quantity_change))  # Purchase Quantity
          ]
        )
      )

    selected_items = self.page.session.get("selected_items") or []

    # Syncs selected items with table inputs
    for idx, row in enumerate(self.table.rows):
      product_id = row.cells[0].content.value
      for selected_item in selected_items:
        if selected_item[0] == product_id:
          row.cells[4].content.value = str(selected_item[2])

    # Update "View Cart" button status
    any_field_filled = any(
      isinstance(row.cells[4].content, ft.TextField) and row.cells[4].content.value.strip()
      for row in self.table.rows
    )

    selected_items = self.page.session.get("selected_items") or []
    selected_not_empty = len(selected_items) > 0
    
    self.check_purchases_btn.disabled = not (any_field_filled or selected_not_empty)

    self.update_pagination_btns()
    self.page.add(self.table)
    self.page.update()

  def on_quantity_change(self, e):
    any_field_filled = any(
      isinstance(row.cells[4].content, ft.TextField) and row.cells[4].content.value.strip()
      for row in self.table.rows
    )

    selected_items = self.page.session.get("selected_items") or []
    selected_not_empty = len(selected_items) > 0
    
    self.check_purchases_btn.disabled = not (any_field_filled or selected_not_empty)
    self.page.update(self.check_purchases_btn)

  def update_pagination_btns(self):
    """Update the state of the pagination buttons."""
    self.prev_button.disabled = (self.current_page == 1)
    self.next_button.disabled = (self.current_page * self.rows_per_page >= self.total_items)
    self.page_label.value = f"Page {self.current_page} of {(self.total_items + self.rows_per_page - 1) // self.rows_per_page}"
    self.page.update(self.prev_button, self.next_button, self.page_label)

  def on_prev_click(self, e):
    """Handles 'Previous' button click."""
    if self.current_page > 1:
      self.current_page -= 1
      self.save_selected_items_on_page_change()  # Save selected items when page changes
      self.load_inventory_data()

  def on_next_click(self, e):
    """Handles 'Next' button click."""
    total_pages = (self.total_items + self.rows_per_page - 1) // self.rows_per_page
    if self.current_page < total_pages:
      self.current_page += 1
      self.save_selected_items_on_page_change()  # Save selected items when page changes
      self.load_inventory_data()

  def logout(self, e):
    """Handles Customer logout"""
    from routes import navigate
    self.page.session.clear()
    navigate(self.page, "CUSTOMER_LOGIN")

  def save_selected_items_on_page_change(self):
    """Saves selected items in the session whenever the page changes."""
    selected_items = self.get_selected_items()
    self.page.session.set("selected_items", selected_items)
    print("Selected items saved on page change:", selected_items)

  def get_selected_items(self):
    saved_selected_items = self.page.session.get("selected_items") or []

    # Update the saved selected items based on user inputs in the table
    for row in self.table.rows:
      product_id = row.cells[0].content.value
      product_name = row.cells[1].content.value
      available_quantity = int(row.cells[2].content.value)
      unit_price = float(row.cells[3].content.value.split(" ")[1])
      purchase_quantity_field = row.cells[4].content

      if purchase_quantity_field.value.strip():
        try:
          purchase_quantity = int(purchase_quantity_field.value)
          if purchase_quantity > 0 and purchase_quantity <= available_quantity:
            # Update the selected items list if the item is selected
            found = False
            for idx, item in enumerate(saved_selected_items):
              if item[0] == product_id:
                  saved_selected_items[idx] = (product_id, product_name, purchase_quantity, unit_price)
                  found = True
                  break
            if not found:
              saved_selected_items.append(
                  (product_id, product_name, purchase_quantity, unit_price)
              )
          else:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Invalid Quantity Entered. Ensure it is within the scope of Available Quantity"), open=True
            )
            self.page.update()
            return []
        except ValueError:
          self.page.snack_bar = ft.SnackBar(
              ft.Text("Invalid Input! Enter a Numeric value"), open=True
          )
          self.page.update()
          return []
      else:
        saved_selected_items = [item for item in saved_selected_items if item[0] != product_id]
    self.page.session.set("selected_items", saved_selected_items)

    return saved_selected_items

  def to_check_purchases(self, e):
    """Navigates to 'Check Purchases' page"""
    from routes import navigate
    selected_items = self.get_selected_items()
    customer_id = self.page.session.get("customer_id")
    customer_name = self.page.session.get("customer_name")
    if not customer_id:
      print("Customer ID not found in session")
      return
    if not selected_items:
      self.page.snack_bar = ft.SnackBar(ft.Text("No items selected for purchase"), open=True)
      self.page.update()
      return
    navigate(self.page, "CHECK_PURCHASES", customer_id=customer_id, selected_items=selected_items)
  
  def to_transaction_history(self, e):
    """Navigate to the transaction history page."""
    from routes import navigate
    navigate(self.page, "TRANSACTION_HISTORY",)

  def build(self):
    """Build the page layout."""
    return ft.Container(
      width=None,
      height=None,
      content=ft.Stack(
        alignment=ft.Alignment(0.0, -1.0),
        controls=[
          ft.Image(
            src="background_images/customer_dash_bg.jpg",
            width=self.page.window.width,
            height=self.page.window.height,
            fit=ft.ImageFit.COVER,
            opacity=0.20,
          ),
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              ft.Text("Current Available Stock", size=29, weight="bold"),
              self.table,
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  self.prev_button,
                  self.page_label,
                  self.next_button,
                  ]
              ),
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  self.check_purchases_btn,
                ]
              ),
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  self.transaction_history_btn,
                ]
              ),
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  self.logout_btn,
                ]
              )
            ]
          ),
        ]
      )
    )
