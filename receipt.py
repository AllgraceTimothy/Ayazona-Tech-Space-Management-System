import flet as ft
from datetime import datetime
from Ayazona_db_manager import generate_receipt

class GenerateReceipt(ft.UserControl):
  """Handles the page for generating and displaying a receipt."""

  def __init__(self, page: ft.Page, **kwargs):
    """Initializes the receipt page, sets up the back button, and session details."""
    super().__init__(**kwargs)
    self.page = page
    self.page.views.clear()
    self.page.title = "Receipt"

    # Back to Dashboard button
    self.back_btn = ft.ElevatedButton(
      text="Back to Dashboard",
      on_click=self.back_to_dashboard,
      width=200,
      height=40,
      bgcolor=ft.colors.BLUE_900,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=16),
      )
    )

    # Placeholder for the receipt column (to be populated later)
    self.receipt_column = None

    # Retrieve session data for customer ID and purchase time
    customer_id = self.page.session.get('customer_id')
    purchase_date = self.page.session.get('Purchase_time')
    self.page.window.width = 800
    self.page.window.height = 630

  def generate_receipt(self):
    """Generates the receipt by fetching transaction data and formatting it."""
    # Fetch transaction data (purchase details)
    self.transaction_data = generate_receipt(self.page)
    if not self.transaction_data:
      print("No transaction data found")
    else:
      print(self.transaction_data)

    row = [] # To store rows for the data table
    totalprice = 0 # To accumulate total prices of the purchases
    purchase_date = None
    fromatted_date = "Unknown" # Default date Format

    # processes each item in the transaction data
    for product_id, product_name, pr_quantity, unit_price, total_price, purchase_date in self.transaction_data:
      row.append(
        ft.DataRow(
          [
            ft.DataCell(ft.Text(product_name)),
            ft.DataCell(ft.Text(str(pr_quantity))),
            ft.DataCell(ft.Text(f"Ksh. {unit_price:.2f}")),
            ft.DataCell(ft.Text(f"Ksh. {total_price:.2f}")),
          ]
        )
      )
      totalprice += total_price

    # Format the purchase date if available
    if purchase_date:
      try:
        formatted_date = datetime.strptime(purchase_date, '%Y-%m-%d %H:%M:%S.%f').strftime("%B %d, %Y %H:%M")
      except Exception as e:
        print(f"Error in formatting date : {e}")
        formatted_date = "Unknown"
    else:
      print(formatted_date)

    # Creates the receipt column UI layout
    self.receipt_column = ft.Column(
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Text(f"Ayazona Techspace Receipt", size=26, weight="bold"),
        ft.Text(f"Purchase Date: {formatted_date}", size=18),
        ft.Text("----------------------------------------------------------------------------------------------------"),
        ft.DataTable(
          columns=[
            ft.DataColumn(ft.Text("Product Name")),
            ft.DataColumn(ft.Text("Quantity")),
            ft.DataColumn(ft.Text("Unit Price")),
            ft.DataColumn(ft.Text("Total Price")),
          ],
          rows=row,
        ),
        ft.Text("------------------------------------------------------------"),
        ft.Text(f"Total Price: Ksh. {totalprice:.2f}", size=22, weight="bold"),
        ft.Text("------------------------------------------------------------"),
      ]
    )

  def back_to_dashboard(self, e):
    """Navigates back to the customer's dashboard."""
    from routes import navigate
    navigate(self.page, "CUSTOMER_DASHBOARD")

  def build(self):
    """Builds the layout for the Receipt page."""
    self.generate_receipt()

    # Returns the layout with background and receipt content
    return ft.Container(
      alignment=ft.Alignment(0.0, 0.0),
      width=None,
      height=None,
      content=ft.Stack(
        alignment=ft.Alignment(0.0, 0.0),
        controls=[
          # Background image for the receipt page
          ft.Image(
            src="assets/receipt.jpeg",
            width=self.page.window.width,
            height=self.page.window.height,
            fit=ft.ImageFit.COVER,
            opacity=0.20,
          ),
          # Main content (receipt display)
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              self.receipt_column,
              self.back_btn,
            ],
            height=490,
            scroll=ft.ScrollMode.ALWAYS,
          )
        ]
      )
    )
