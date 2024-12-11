import flet as ft
from datetime import datetime
from Ayazona_db_manager import finalize_purchase

class CheckPurchasesPage(ft.UserControl):
  """Handles the page for confirming and reviewing purchases."""

  def __init__(self, page: ft.Page, customer_id=None, selected_items=None, **kwargs):
    """Initializes the page and sets up the components for confirming purchases."""
    super().__init__(**kwargs)
    self.page = page
    self.page.views.clear()
    self.page.title = "Confirm Purchases"
    self.customer_id = customer_id
    self.selected_items = selected_items or []
    self.snack_bar = ft.SnackBar(ft.Text(""), open=False)
    self.page.window.width = 800
    self.page.window.height = 650

    if self.snack_bar not in self.page.overlay:
      self.page.overlay.append(self.snack_bar)

    # Confirm Purchase button
    self.confirm_btn = ft.ElevatedButton(
      text="Confirm Purchase",
      on_click=self.handle_confirm_purchase,
      width=200,
      height=40,
      bgcolor=ft.colors.GREEN_900,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=16),
      )
    )
    
    # View Receipt button (disabled initially)
    self.view_receipt_btn = ft.ElevatedButton("View Receipt", on_click=self.view_receipt, disabled=True)
    
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

  def calculate_total_cost(self):
    """Calculates the total cost of selected items."""
    return sum(pr_quantity * unit_price for product_id, product_name, pr_quantity, unit_price in self.selected_items)
  
  def handle_confirm_purchase(self, e):
    """Handles the purchase confirmation and communicates with the backend."""
    self.page.session.set("Purchase_time", datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    self.view_receipt_btn.disabled = True
    self.confirm_btn.disabled = True
    self.page.update()

    # Prepare raw items for purchase
    raw_items = [(product_id, product_name, pr_quantity, unit_price) for product_id, product_name, pr_quantity, unit_price in self.selected_items]

    success, message = finalize_purchase(self.customer_id, raw_items)
    self.show_snack_bar(message)

    if success:
      self.view_receipt_btn.disabled = False
      self.page.update(self.view_receipt_btn)
    else:
      self.confirm_btn.disabled = False
    self.page.update()

  def back_to_dashboard(self, e):
    """Navigates back to the customer's dashboard."""
    from routes import navigate
    navigate(self.page, "CUSTOMER_DASHBOARD")

  def view_receipt(self, e):
    """Navigates to the receipt page."""
    from routes import navigate
    navigate(self.page, "RECEIPT")

  def show_snack_bar(self, message):
    """Shows a snack bar with a custom message."""
    self.snack_bar.content = ft.Text(message)
    self.snack_bar.open = True
    self.page.update()

  def build(self):
    """Builds and returns the layout of the CheckPurchases page."""
    # Table to display selected items with their details
    table = ft.DataTable(
      columns=[
        ft.DataColumn(ft.Text("Product Name")),
        ft.DataColumn(ft.Text("Unit Price")),
        ft.DataColumn(ft.Text("Quantity")),
        ft.DataColumn(ft.Text("Total")),
      ],
      rows=[
        ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(product_name)),
            ft.DataCell(ft.Text(f"Ksh. {unit_price}")),
            ft.DataCell(ft.Text(str(pr_quantity))),
            ft.DataCell(ft.Text(f"Ksh. {float(pr_quantity) * float(unit_price):.2f}")),
          ]
        )
        for product_id, product_name, pr_quantity, unit_price in self.selected_items
      ]
    )

    # Total cost text
    total_cost_text = ft.Text(
      f"Overall Total Cost: Ksh. {self.calculate_total_cost():.2f}", size=24, weight="bold"
    )

    # Layout container for the page
    purchase_column = ft.Container(
      width=None,
      height=None,
      content=ft.Stack(
        alignment=ft.Alignment(0.0, 0.0),
        controls=[
          # Background image for the page
          ft.Image(
            src="background_images/cart_bg.jpg",
            width=self.page.window.width,
            height=self.page.window_height,
            fit=ft.ImageFit.COVER,
            opacity=0.15,
          ),
          # Main content (purchase review)
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              ft.Text("Review Your Purchases", size=25, weight="bold"),
              table,
              total_cost_text,
              ft.Row(
                [self.confirm_btn, self.view_receipt_btn],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=35,
              ),
              ft.Row(
                [self.back_btn],
                alignment=ft.MainAxisAlignment.CENTER,
              ),
            ],
            height=490,
            scroll=ft.ScrollMode.ALWAYS,
          ),
        ],
      )
    )
    return purchase_column
