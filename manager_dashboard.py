import flet as ft
from Ayazona_db_manager import get_inventory_count, navigate_product_pages

class ManagerDashboard(ft.UserControl):
  def __init__(self, page: ft.Page, **kwargs):
    super().__init__(**kwargs)
    self.page = page
    self.page.views.clear()
    self.page.title = "Manager's Dashboard"
    self.page.window.width = 800
    self.page.window.height = 650
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Sets aspects for page navigation
    self.current_page = 1
    self.rows_per_page = 5
    self.total_items = get_inventory_count()
    self.data = []

    # Initializes the data table
    self.table = ft.DataTable(
      columns=[
        ft.DataColumn(ft.Text("Product ID", size=20)),
        ft.DataColumn(ft.Text("Product Name", size=20)),
        ft.DataColumn(ft.Text("Quantity", size=20)),
        ft.DataColumn(ft.Text("Unit Price", size=20)),
      ],
      rows=[]   # Adds the data rows to the table
    )

    # Creates the navigation buttons and page status text
    self.page_label = ft.Text(f"Page {self.current_page} of {(self.total_items + self.rows_per_page - 1) // self.rows_per_page}")
    self.prev_button = ft.ElevatedButton("Previous", on_click=self.on_prev_click, disabled=(self.current_page == 1))
    self.next_button = ft.ElevatedButton("Next", on_click=self.on_next_click, disabled=(self.current_page >= (self.total_items + self.rows_per_page - 1) // self.rows_per_page))

    self.load_inventory_data()  

  def load_inventory_data(self):
    self.page.clean()
    """Fetch inventory data for the current page."""
    offset = (self.current_page - 1) * self.rows_per_page
    self.data = navigate_product_pages(offset, self.rows_per_page)

    if not self.data:
      self.page.snack_bar = ft.SnackBar(ft.Text("No inventory data found"), open=True)
      self.update_pagination_btns()
      self.page.update()
      return

    self.table.rows.clear()
    for row in self.data:
      self.table.rows.append(
        ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(str(row[0]))),  # Product ID
            ft.DataCell(ft.Text(row[1])),       # Product Name
            ft.DataCell(ft.Text(str(row[2]))),  # Quantity
            ft.DataCell(ft.Text(f"Ksh {row[3]:.2f}"))  # Unit Price
          ]
        )
      )
    self.update_pagination_btns()
    self.page.update()

  def update_pagination_btns(self):
    """Update the state of the pagination buttons."""
    self.prev_button.disabled = (self.current_page == 1)
    self.next_button.disabled = (self.current_page >= (self.total_items + self.rows_per_page - 1) // self.rows_per_page)
    self.page_label.value = f"Page {self.current_page} of {(self.total_items + self.rows_per_page - 1) // self.rows_per_page}"
    self.page.update(self.prev_button, self.next_button, self.page_label)

  def go_to_page(self, new_page):
    """Function to navigate to a specific page."""
    total_pages = (self.total_items + self.rows_per_page - 1) // self.rows_per_page

    if 1 <= new_page <= total_pages:
      self.current_page = new_page
      self.load_inventory_data()
    else:
      self.page.snack_bar = ft.SnackBar(ft.Text("No more pages"), open=True)
      self.page.update()

    self.update_pagination_btns()

  def on_prev_click(self, e):
    """Handles 'Previous' button click."""
    self.go_to_page(self.current_page - 1)

  def on_next_click(self, e):
    """Handles 'Next' button click."""
    self.go_to_page(self.current_page + 1)

  def to_add_new_product(self):
    # Navigates to the add new product page
    from routes import navigate
    navigate(self.page, "ADD_PRODUCT")

  def to_update_stock(self):
    # Navigates to the update stock page
    from routes import navigate
    navigate(self.page, "UPDATE_STOCK")

  def logout(self):
    # Logs the current user out and navigates to the login page
    from routes import navigate
    navigate(self.page, "MANAGER_LOGIN")

  """Creates the Page buttons"""
  add_new_btn = ft.ElevatedButton(
    text="Add New Product",
    on_click=to_add_new_product,
    bgcolor=ft.colors.GREEN_800,
    height=40,
    color=ft.colors.WHITE,
    style=ft.ButtonStyle(
      shape=ft.RoundedRectangleBorder(radius=20),
    ),
    )
  update_stock_btn = ft.ElevatedButton(
    text="Update Stock Levels",
    on_click=to_update_stock,
    height=40,
    bgcolor=ft.colors.ORANGE_800,
    color=ft.colors.WHITE,
    style=ft.ButtonStyle(
      shape=ft.RoundedRectangleBorder(radius=20),
    ),
    )
  logout_btn = ft.ElevatedButton(
    text="Logout",
    on_click=logout,
    height=40,
    bgcolor=ft.colors.BLUE_800,
    color=ft.colors.WHITE,
    style=ft.ButtonStyle(
      shape=ft.RoundedRectangleBorder(radius=20),
    ),
    )

  def build(self):
    """Build the page layout."""
    return ft.Container(
      width=None,
      height=None,
      content=ft.Stack(
      alignment=ft.Alignment(0.0, 0.0),
        controls=[
          ft.Image(
            src="background_images/manager_dash_bg.jpg",
            width=self.page.window.width,
            height=self.page.window.height,
            fit=ft.ImageFit.COVER,
            opacity=0.20,
          ),
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              ft.Text("Current Available Stock", size=32, weight="bold"),
              self.table,
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  self.prev_button,
                  self.page_label,
                  self.next_button
                  ]
              ),
              ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                controls=[
                  self.add_new_btn,
                  self.update_stock_btn,
                ]
              ),
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  self.logout_btn,
                ]
              )
            ]
          )
        ]
      )
    )
