import flet as ft

class HomePage(ft.UserControl):
  """Defines the main settings for the Home Page"""
  def __init__(self, page: ft.Page, **kwargs):
    super().__init__(**kwargs)
    self.page = page
    self.page.title = 'Home Page'
    self.page.window.width = 720
    self.page.window.height = 650
    self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Sets the background image for the page
    self.image = ft.Image(
      src="background_images/home_bg.jpg",
      width=self.page.window.width,
      height=self.page.window.height,
      fit=ft.ImageFit.COVER,
      opacity=0.27,
    )
    # Creates the Welcome message and the Siignup and Log-in Buttons
    self.column = ft.Column(
      width=None,
      height=None,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        ft.Text(
          "Welcome to Ayazona Techspace",
          size=28,
          weight="bold",
          text_align=ft.TextAlign.CENTER,
          color=ft.colors.WHITE,
          ),
        ft.ElevatedButton(
          text="Customer Login",
          on_click=self.to_customer_login,
          width=200,
          height=50,
          bgcolor=ft.colors.GREEN_600,
          color=ft.colors.WHITE,
          style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=18),
            ),
          ),
          ft.ElevatedButton(
            text="Manager Login",
            on_click=self.to_manager_login,
            width=200,
            height=50,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
              shape=ft.RoundedRectangleBorder(radius=18),
            ),
          ),
          ft.Text(
            "Don't have an Account yet?",
            size=24,
            text_align=ft.TextAlign.CENTER,
            color=ft.colors.WHITE,
            ),
          ft.ElevatedButton(
            text="Sign Up",
            on_click=self.to_signup,
            width=200,
            height=50,
            bgcolor=ft.colors.ORANGE_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
              shape=ft.RoundedRectangleBorder(radius=18),
            ),
          ),
        ]
      )
    
  def to_manager_login(self, e):
    # Transports to the manager login page
    from routes import navigate
    navigate(self.page,"MANAGER_LOGIN")

  def to_customer_login(self, e):
    # Transports to the customer login page
    from routes import navigate
    navigate(self.page,"CUSTOMER_LOGIN")

  def to_signup(self, e):
    # Transports to the sign up page
    from routes import navigate
    navigate(self.page,"SIGN_UP")
    
  def build(self):
    # Builds the UI components of the Home Page
    return ft.Container(
      alignment=ft.Alignment(0.0, 0.0),
      width=None,
      height=None,
        content=ft.Stack(
          alignment=ft.Alignment(0.0, 0.0),
          controls=[
            self.image,
            self.column,
          ],
        )
    )

