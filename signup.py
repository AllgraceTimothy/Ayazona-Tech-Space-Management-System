import flet as ft
import re
from Ayazona_db_manager import save_customer, save_manager
SECRET_KEY = "sct_key.765"

class SignUpPage(ft.UserControl):
  # Sets the main layout aspects of the page
  def __init__(self, page: ft.Page, **kwargs):
    super().__init__(**kwargs)
    self.page = page
    self.page.title = 'Sign Up'
    self.page.window.width = 720
    self.page.window.height = 650

    self.account_type = ft.Dropdown(
      label="Account Type",
      options=[
        ft.dropdown.Option(str("Customer")),
        ft.dropdown.Option(str("Manager")),
      ],
      color=ft.colors.WHITE,
      on_change=lambda e: self.enable_secret_key(),
      width=350,
      )
    self.username = ft.TextField(label="Username", color=ft.colors.WHITE, width=350)
    self.email = ft.TextField(label="Email Address", color=ft.colors.WHITE, width=350)
    self.password = ft.TextField(label="Password", password=True, can_reveal_password=True, color=ft.colors.WHITE, width=350)
    self.secret_key = ft.TextField(
      label="Secret Key (For Managers Only)",
      password=True,
      can_reveal_password=True,
      color=ft.colors.WHITE,
      disabled=True,
      width=350,
        )
    self.status = ft.Text(value="", color="red", text_align="center")
    self.page.snack_bar = ft.SnackBar(ft.Text(""), open=False)

  def show_snack_bar(self, message):
    # Handles the snack bar
    self.page.snack_bar.content = ft.Text(value=message)
    self.page.snack_bar.open = True
    self.page.update()

  def enable_secret_key(self):
    # Enables or disables the secret key field based on the selected account type
    self.secret_key.disabled = self.account_type.value != str("Manager")
    self.page.update(self.secret_key)

  def validate_username(self, username):
    # Ensures the username is between 5 and 20 characters and only contains alphanumeric and underscores/dashes
    # and contains at least one letter (both uppercase or lowercase)
    return re.match(r'^(?=.*[A-Za-z])[A-Za-z0-9 _-]{5,20}$', username)
  
  def validate_email(self, email):
    # Regex to validate a proper email format
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
  
  def validate_password(self, password):
    # Validates password to have at least 8 characters, a number, a lowercase and uppercase letter, and a special character
    return re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&#+-])[A-Za-z\d@$!%*?&#+-]{8,}$', password)

  def signup(self, e):
    # Handles account creation
    username = self.username.value
    email = self.email.value
    password = self.password.value
    entered_secret_key = self.secret_key.value

    if self.account_type.value == "Customer":
      if not username or not email or not password:
        self.status.value = "Please fill in all the fields"
        self.page.update(self.status)
      elif not self.validate_username(username):
        self.status.value = "Invalid username. It should be 5-20 characters long and contain only alphanumeric characters, underscores, or dashes"
        self.page.update(self.status)
      elif not self.validate_email(email):
        self.status.value = "Invalid email address format"
        self.page.update(self.status)
      elif not self.validate_password(password):
        self.status.value = "Password should be at least 8 characters long and contain at least one number,\none uppercase letter, and one special character"
        self.page.update(self.status)
      else:
        success = save_customer(username, email, password)
        if success:
          self.show_snack_bar("Customer Account created successfully")
          self.to_customer_login()
        else:
          self.show_snack_bar("Error creating customer account")

    elif self.account_type.value == "Manager":
      if not username or not password or not email:
        self.status.value = "Please fill in all the fields"
        self.page.update(self.status)
      elif not entered_secret_key:
        self.status.value = "Please enter the secret key to proceed"
        self.page.update(self.status)
      elif entered_secret_key!= SECRET_KEY:
        self.status.value = "Incorrect Secret Key Please try again"
        self.page.update(self.status)
      elif not self.validate_username(username):
        self.status.value = "Invalid username. It should be 5-20 characters long and contain only alphanumeric characters, underscores, or dashes"
        self.page.update(self.status)
      elif not self.validate_email(email):
        self.status.value = "Invalid email address format"
        self.page.update(self.status)
      elif not self.validate_password(password):
        self.status.value = "Password should be at least 8 characters long and contain at least one number,\none uppercase letter, and one special character"
        self.page.update(self.status)
      else:
        success = save_manager(username, email, password)
        if success:
          self.show_snack_bar("Manager account created successfully")
          self.to_manager_login()
        else:
          self.show_snack_bar("Error creating manager account")
    else:
      self.status.value = "Please select an account type"
      self.page.update(self.status)

  def to_customer_login(self):
    # Redirects to the Customer Login page after successfully creating a new account
    from routes import navigate
    navigate(self.page, "CUSTOMER_LOGIN")

  def to_manager_login(self):
    # Redirects to the Manager Login page after successfully creating a new account
    from routes import navigate
    navigate(self.page, "MANAGER_LOGIN")

  def go_home(self):
    # Navigate to the home page
    from routes import navigate
    navigate(self.page, "HOME")

  # creates the back button
  back_btn = ft.ElevatedButton(
    text="Back",
    on_click=go_home,
    width=150,
    height=40,
    bgcolor=ft.colors.BLUE_900,
    color=ft.colors.WHITE,
    style=ft.ButtonStyle(
      shape=ft.RoundedRectangleBorder(radius=16),
    )
    )

  def build(self):
    """Buils the UI for the Signup Page"""
    return ft.Container(
    alignment=ft.Alignment(0.0, 0.0),
    width=None,
    height=None,
    content=ft.Stack(
    alignment=ft.Alignment(0.0, 0.0),
      controls=[
        ft.Image(
          src="background_images/reset_password_bg.jpg",
          width=self.page.window.width,
          height=self.page.window_height,
          fit=ft.ImageFit.COVER,
          opacity=0.25,
        ),
        ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            ft.Text(
              "Instantly create your account by filling in these fields",
              size=26,
              weight="bold",
              color=ft.colors.WHITE,
              ),
            self.account_type,
            self.username, 
            self.email, 
            self.password, 
            self.secret_key,

            # creates the generate account button
            ft.ElevatedButton(
              text="Generate Account",
              on_click=self.signup,
              width=200,
              height=45,
              bgcolor=ft.colors.ORANGE_600,
              color=ft.colors.WHITE,
              style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
              )
            ),
            ft.Column(
              alignment=ft.MainAxisAlignment.CENTER,
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                self.status,
                self.back_btn,
              ]
            )
          ]
        ),
      ]
    )
  )




