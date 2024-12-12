import flet as ft
from Ayazona_db_manager import transaction_history
from datetime import datetime

class GenerateHistory(ft.UserControl):
  """Displays the transaction history of a customer."""

  def __init__(self, page: ft.Page, **kwargs):
    """Initializes the page, retrieves customer ID from the session, and sets window size."""

    super().__init__(**kwargs)
    self.page = page
    self.page.views.clear()
    self.page.title = "Transaction History"

    # Retrieve the customer ID from the session
    self.customer_id = self.page.session.get('customer_id')

    self.page.window.width = 880
    self.page.window.height = 700

  def generate_history(self):
    """Fetches the transaction history for the customer using the customer ID."""
    self.transaction_history = transaction_history(self.customer_id)
    
  def back_to_dashboard(self, e):
    """Navigates back to the customer dashboard."""
    from routes import navigate
    navigate(self.page, "CUSTOMER_DASHBOARD")

  def build(self):
    """Builds the layout and displays the transaction history."""
    self.generate_history()

    # If no transaction history is found, displays a message
    if not self.transaction_history:
      self.page.snack_bar = ft.SnackBar(ft.Text("No transactions have been made yet."), open=True)
      self.page.update()

    # Process each transaction item and prepare rows for the data table
    self.rows = []
    self.total_price = 0
    for product_id, product_name, quantity, unit_price, total, purchase_date in self.transaction_history:
      self.rows.append(
        ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(product_name)),
            ft.DataCell(ft.Text(str(quantity))),
            ft.DataCell(ft.Text(f"Ksh {unit_price:.2f}")),
            ft.DataCell(ft.Text(f"Ksh {total:.2f}")),
            ft.DataCell(ft.Text(datetime.strptime(purchase_date, '%Y-%m-%d %H:%M:%S.%f').strftime("%B %d, %Y %H:%M"))),
          ]
        )
      )
      self.total_price += total

    # Creates the main layout for the transaction history page
    history_column = ft.Container(
      alignment=ft.Alignment(0.0, 0.0),
      width=None,
      height=None,
      content=ft.Stack(
      alignment=ft.Alignment(0.0, 0.0),
        controls=[
          # Background image for the transaction history page
          ft.Image(
            src="background_images/transaction_hist_bg.jpg",
            width=self.page.window.width,
            height=self.page.window.height,
            fit=ft.ImageFit.COVER,
            opacity=0.3,
          ),
          ft.Column(
            # Title for the transaction history page
            width=None,
            height=self.page.window.height,
            controls=[
              ft.Text('Your Transaction History', size=30, weight="bold", text_align="center"),
            ],
            spacing=0,
          ),
           # Data table for displaying the transaction history details
          ft.Column(
            controls=[
              ft.DataTable(
                data_row_max_height=60,
                columns=[
                  ft.DataColumn(ft.Text("Product Name", size=20)),
                  ft.DataColumn(ft.Text("Quantity", size=20)),
                  ft.DataColumn(ft.Text("Unit Price", size=20, width=100)),
                  ft.DataColumn(ft.Text("Total", size=20, width=100)),
                  ft.DataColumn(ft.Text("Prurchase Date", size=20, width=150)),
                ],
                rows=self.rows
              ),
              # Display total expenditure
              ft.Text(f"Total Expenditure: Ksh {self.total_price:.2f}", size=26, weight="bold"),
               # Back button to navigate to the dashboard
              ft.ElevatedButton(
                text="Back to Dashboard",
                on_click=self.back_to_dashboard,
                width=200,
                height=40,
                bgcolor=ft.colors.AMBER_800,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(
                  shape=ft.RoundedRectangleBorder(radius=20),
                )
              ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=False,
            height=400,
            scroll=ft.ScrollMode.ALWAYS,
          ),
        ]
      )
    )
    return history_column