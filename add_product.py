import flet as ft
from Ayazona_db_manager import add_new_products

class AddProductPage(ft.UserControl):
  def __init__(self, page: ft.Page, **kwargs):
    super().__init__(**kwargs)
    self.page = page
    self.page.views.clear()
    self.page.title = "Add New Product"
    self.page.window.width = 650
    self.page.window.height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Creates the UI elements
    self.header = ft.Text("Fill in the fields below to add a new product", size=24, weight="bold")
    self.product_name_field = ft.TextField(label="Product Name", width=200)
    self.quantity_field = ft.TextField(label="Quantity", keyboard_type="number", width=100)
    self.price_field = ft.TextField(label="Unit Price", keyboard_type="number", width=150)

    self.submit_btn = ft.ElevatedButton(
      text="Submit",
      on_click=self.submit_new,
      width=200,
      height=50,
      bgcolor=ft.colors.GREEN_600,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=18),
      ),
    )
    self.back_btn = ft.ElevatedButton(
      text="Back to Dashboard",
      on_click=self.to_dashboard,
      height=40,
      bgcolor=ft.colors.BLUE_900,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=24),
      ),
    )
    self.status = ft.Text("", color="red", size=16, text_align="center")

  def submit_new(self, e):
    """Handles Submission of a new product"""
    product_name = self.product_name_field.value
    quantity = self.quantity_field.value
    price = self.price_field.value

    if not product_name or not quantity or not price:
      self.status.value = "Please fill in all the fields"
      self.page.update(self.status)
    else:
      try:
        quantity = int(quantity)
        price = float(price)

        success = add_new_products(product_name, quantity, price)
        if success:
          self.page.snack_bar = ft.SnackBar(ft.Text("Product added successfully"), open=True)
          self.product_name_field.value = ""
          self.quantity_field.value = ""
          self.price_field.value = ""
          self.page.update(self.product_name_field, self.quantity_field, self.price_field)
        else:
          self.page.snack_bar = ft.SnackBar(ft.Text("An error occured while adding product. Kindly try again"), open=True)
      except ValueError:
        self.page.snack_bar = ft.SnackBar(ft.Text("Quantity and Price field only take valid numbers"), open=True)
      self.page.update()

  def to_dashboard(self, e):
    # Navigates back to Manager's dashboard
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
            src="background_images/add_product_bg.jpg",
            width=self.page.window.width,
            height=self.page.window.height,
            fit=ft.ImageFit.COVER,
            opacity=0.20,
          ),
          ft.Column(
            controls=[
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[self.header],
              ),
              ft.Row(
                controls=[
                  self.product_name_field,
                  self.quantity_field,
                  self.price_field,
                  self.status,
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
              ),
              ft.Row(
                controls=[self.status],
                alignment=ft.MainAxisAlignment.CENTER
              ),
              ft.Row(
                controls=[self.submit_btn],
                alignment=ft.MainAxisAlignment.CENTER,
              ),
              ft.Row(
                controls=[self.back_btn],
                alignment=ft.MainAxisAlignment.CENTER,
              )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40,
          ),
        ],
      ),
    )
