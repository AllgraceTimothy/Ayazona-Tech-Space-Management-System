import flet as ft
from Ayazona_db_manager import change_cust_password, change_manager_password, get_customer_details, get_manager_details
SECRET_KEY = "sct_key.765"

class ChangePasswordPage(ft.UserControl):
  def __init__(self, page: ft.Page, **kwargs):
    super().__init__(**kwargs)
    self.page = page
    self.page.title = "Reset Password"
    self.customer_id = self.page.session.get('customer_id')
    self.page.window.width = 720
    self.page.window.height = 680
    
    self.customers = []
    self.managers = []

    self.account_type = ft.Dropdown(
      label="Account Type",
      options=[
        ft.dropdown.Option(str("Customer")),
        ft.dropdown.Option(str("Manager")),
      ],
      color=ft.colors.WHITE,
      width=350,
      )
    self.email = ft.TextField(label="Email Address", color=ft.colors.WHITE, width=350)
    self.new_password = ft.TextField(label="New Password", password=True, can_reveal_password=True, color=ft.colors.WHITE, width=350, disabled=True)
    self.confirm_password = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, color=ft.colors.WHITE, width=350, disabled=True)

    self.secret_key = ft.TextField(
      label="Secret Key (For Managers Only)",
      password=True,
      can_reveal_password=True,
      color=ft.colors.WHITE,
      disabled=True,
      width=350,
        )
    
    self.status = ft.Text(value="", color="", text_align="center")
    self.status2 = ft.Text(value="", color="", text_align="center")

    self.go_btn = ft.ElevatedButton(
      text="Go",
      on_click=self.confirm_account,
      width=70,
      height=40,
      bgcolor=ft.colors.GREEN_700,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
          shape=ft.RoundedRectangleBorder(radius=20),
      )
    )
    self.change_password_btn = ft.ElevatedButton(
      text="Reset Password",
      on_click=self.change_password,
      width=150,
      height=40,
      bgcolor=ft.colors.ORANGE_700,
      color=ft.colors.WHITE,
    )
    self.back_to_login_btn = ft.ElevatedButton(
      text="Back to Login",
      on_click=self.back_to_login,
      width=150,
      height=40,
      bgcolor=ft.colors.BLUE_800,
      color=ft.colors.WHITE,
      style=ft.ButtonStyle(
          shape=ft.RoundedRectangleBorder(radius=20),
      )
    )

  def confirm_account(self, email):
    email = self.email.value
    self.customers = get_customer_details()
    self.managers = get_manager_details()

    if not email:
      self.page.snack_bar = ft.SnackBar(ft.Text("Please enter your email address to proceed"), open=True)
      self.page.update()
      return
  
    if self.account_type.value == "Customer":
      if not self.customers:
        self.page.snack_bar = ft.SnackBar(ft.Text("No customer accounts have been opened yet"), open=True)
        self.page.update()
      for customer in self.customers:
        if customer[2] == email:
          self.new_password.disabled = False
          self.confirm_password.disabled = False
          self.status.value = "Customer account found"
          self.status.color = "green"
          self.page.update(self.status, self.new_password, self.confirm_password)
          break
        else:
          self.status.value = "Customer account for the provided email address was not found\nConfirm your email adress then try again"
          self.status.color = "red"
          self.page.update(self.status)

    elif self.account_type.value == "Manager":
      if not self.managers:
        self.page.snack_bar = ft.SnackBar(ft.Text("No manager accounts have been opened yet"), open=True)
        self.page.update()
      for manager in self.managers:
        if manager[2] == email:
          self.new_password.disabled = False
          self.confirm_password.disabled = False
          self.secret_key.disabled = False
          self.status.value = "Manager account found"
          self.status.color = "green"
          self.page.update(self.status, self.new_password, self.confirm_password, self.secret_key)
          break
        else:
          self.status.value = "Manager account for the provided email address was not found\nConfirm your email adress then try again"
          self.status.color = "red"
          self.page.update(self.status)
    else:
      self.page.snack_bar = ft.SnackBar(ft.Text("Please select an account type"), open=True)
      self.page.update()

  def change_password(self, new_password):
    email = self.email.value
    new_password = self.new_password.value
    confirm_password = self.confirm_password.value
    secret_key = self.secret_key.value

    if self.account_type.value == "Customer":
      if not new_password or not confirm_password:
        self.page.snack_bar = ft.SnackBar(ft.Text("Please enter new password then confirm it"), open=True)
        self.page.update()
        return
      elif new_password!= confirm_password:
        self.page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match"), open=True)
        self.page.update()
        return
      else:
        success = change_cust_password(email, new_password)
        if success:
          self.status2.value ="Password has been reset successfully !"
          self.status2.color = "green"
          self.page.update(self.status2)
        else:
          self.page.snack_bar = ft.SnackBar(ft.Text("An error occured while resetting the password"), open=True)
          self.page.update()

    else:
      if not new_password or not confirm_password or not secret_key:
        self.page.snack_bar = ft.SnackBar(ft.Text("Please fill in  all the fields"), open=True)
        self.page.update()
        return
      elif new_password != confirm_password:
        self.page.snack_bar = ft.SnackBar(ft.Text("Passwords do not match"), open=True)
        self.page.update()
        return
      elif secret_key!= SECRET_KEY:
        self.page.snack_bar = ft.SnackBar(ft.Text("Invalid secret key"), open=True)
        self.page.update()
        return
      else:
        success = change_manager_password(email, new_password)
        if success:
          self.status2.value ="Password has been reset successfully !"
          self.status2.color = "green"
          self.page.update(self.status2)
        else:
          self.page.snack_bar = ft.SnackBar(ft.Text("An error occured while resetting the password"), open=True)
          self.page.update()

  def back_to_login(self, e):
    from routes import navigate
    if self.account_type.value == "Manager":
      navigate(self.page, "MANAGER_LOGIN")
    elif self.account_type.value == "Customer":
      navigate(self.page, "CUSTOMER_LOGIN")
    else:
      navigate(self.page, "HOME")

  def build(self):
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
            opacity=0.20,
          ),
          ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
              ft.Text("Confirm your email address to reset your password", text_align="center", size=23, weight="bold"),
              self.account_type,
              self.email,
              self.go_btn,
              self.status,
              self.new_password,
              self.confirm_password,
              self.secret_key,
              self.change_password_btn,
              self.status2,
              ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                  self.back_to_login_btn,
                ]
              )
            ]
          )
        ]
      ),
    )


