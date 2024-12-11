import flet as ft
from Ayazona_db_manager import update_stock_levels, get_product_details

class UpdateStockPage(ft.UserControl):
  def __init__(self, page: ft.Page, **kwargs):
    super().__init__(**kwargs)
    self.page = page
    self.page.views.clear()
    self.page.title = "Update Stock"
    self.page.window.width = 920
    self.page.window.height = 680

    # Sets the aspects for page navigation
    self.current_page = 1
    self.rows_per_page = 5
    self.total_items = len(get_product_details())
    self.data = []

    # Creates the data table
    self.table = ft.DataTable(
      data_row_max_height=70,
      columns=[
        ft.DataColumn(ft.Text("Product ID", size=15)),
        ft.DataColumn(ft.Text("Product Name", size=15, width=100)),
        ft.DataColumn(ft.Text("Available Stock", size=15)),
        ft.DataColumn(ft.Text("New Stock", size=15, width=80)),
        ft.DataColumn(ft.Text("New Price", size=15, width=130)),
        ft.DataColumn(ft.Text()),
      ],
      rows=[]
    )
    # page label showing the page number you are currently on
    self.page_label = ft.Text(f"Page {self.current_page} of {(self.total_items + self.rows_per_page - 1) // self.rows_per_page}")
    # previous button
    self.prev_btn = ft.ElevatedButton(
      text="Previous",
      on_click=self.on_prev_click, disabled=(self.current_page == 1)
    )
    # next button
    self.next_btn = ft.ElevatedButton(
      text="Next",
      on_click=self.on_next_click, disabled=(self.current_page * self.rows_per_page >= self.total_items)
    )
    self.page.update(self.page_label, self.prev_btn, self.prev_btn)

    self.back_btn = ft.ElevatedButton(
      text="Back to Dashboard",
      on_click=self.to_dashboard,
      height=40,
      bgcolor=ft.colors.BLUE_800,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=24),
      )
    )
    self.load_product_data()

  def load_product_data(self):
    """Load the product data for each new product page"""
    self.page.clean()
    offset = (self.current_page - 1) * self.rows_per_page
    self.data = get_product_details()[offset:offset + self.rows_per_page]

    if not self.data:
      self.page.snack_bar = ft.SnackBar(ft.Text("No inventory data found"))
      self.page.update()
      return
    
    self.table.rows.clear()
    for row in self.data:
      product_id_, name, current_quantity, current_price = row
      new_stock_field = ft.TextField(width=80, keyboard_type="number")
      new_price_field = ft.TextField(current_price, width=130, keyboard_type="number")

      update_btn = ft.ElevatedButton(
        text="Update",
        on_click=lambda e, pid=product_id_, nsf=new_stock_field, npf=new_price_field:
          self.handle_update(e, pid, nsf.value.strip(), npf.value),
        bgcolor=ft.colors.GREEN_800,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(
          shape=ft.RoundedRectangleBorder(radius=16),
        )
      )

      self.table.rows.append(
        ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(product_id_, text_align="center"),),
            ft.DataCell(ft.Text(name)),
            ft.DataCell(ft.Text(str(current_quantity), text_align="center")),
            ft.DataCell(new_stock_field),
            ft.DataCell(new_price_field),
            ft.DataCell(update_btn),
          ],
        )
      )
    self.update_pagination_btns()
    self.page.update()

  def update_pagination_btns(self):
    # Updates the previous, next buttons and the page label upon navigation to a different product page
    self.prev_btn.disabled = self.current_page == 1
    self.next_btn.disabled = self.current_page * self.rows_per_page >= self.total_items
    self.page_label.value = f"Page {self.current_page} of {(self.total_items + self.rows_per_page - 1) // self.rows_per_page}"

  def on_prev_click(self, e):
    # Navigates to the previous product page
    if self.current_page > 1:
      self.current_page -= 1
      self.load_product_data()

  def on_next_click(self, e):
    # navigates to the next product page
    total_pages = (self.total_items + self.rows_per_page - 1) // self.rows_per_page
    if self.current_page < total_pages:
      self.current_page += 1
      self.load_product_data()

  def handle_update(self, e, product_id, new_stock, new_price):
    """Handles the update of stock levels and prices"""
    if not new_price and not new_stock:
      self.page.snack_bar = ft.SnackBar(ft.Text("Both fields cannot be empty"), open=True)
      self.page.update()
      return
    elif new_stock and not self.is_valid_number(new_stock):
      self.page.snack_bar = ft.SnackBar(ft.Text("Invalid stock input! Must be a whole number. Please try again"))
      self.page.update()
      return
    elif new_price and not self.is_valid_number(new_price, allow_float=True):
      self.page.snack_bar = ft.SnackBar(ft.Text("Invalid price input! Must be a real number. Please try again"))
      self.page.update()
      return
    else:
      new_stock = int(new_stock) if new_stock else None
      new_price = float(new_price) if new_price else None

      success = update_stock_levels(product_id, new_stock, new_price)

      if success:
        self.page.snack_bar = ft.SnackBar(ft.Text("Stock levels updated successfully"), open=True)
        new_stock = ""
        self.page.update()
      else:
        self.page.snack_bar = ft.SnackBar(ft.Text("An error occurred while updating stock levels. Please try again"), open=True)
    self.page.update()

  def is_valid_number(self, value, allow_float=False):
    try:
      if allow_float:
        float(value)
      else:
        int(value)
      return True
    except ValueError:
      return False
    
  def to_dashboard(self, e):
    # Navigates back to manager's dashboard
    from routes import navigate
    navigate(self.page, "MANAGER_DASHBOARD")
    
  def build(self):
    """Builds the entire page with UI elements"""
    return ft.Container(
      width=None,
      height=None,
        content=ft.Stack(
          alignment=ft.Alignment(0.0, 0.0),
          controls=[
            ft.Image(
              src="assets/Update_stock2.jpeg",
              width=self.page.window.width,
              height=self.page.window.height,
              fit=ft.ImageFit.COVER,
              opacity=0.25,
            ),
            ft.Column(
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                ft.Text("Update Stock Levels and Prices", size=28, weight="bold"),
                self.table,
                ft.Row(
                  alignment=ft.MainAxisAlignment.CENTER,
                  controls=[
                    self.prev_btn,
                    self.page_label,
                    self.next_btn,
                  ]
                ),
                ft.Row(
                  alignment=ft.MainAxisAlignment.CENTER,
                  controls=[
                    self.back_btn,
                  ]
                )
              ]
            )
          ]
        )
    )

