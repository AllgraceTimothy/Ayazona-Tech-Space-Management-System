import flet as ft
from Ayazona_db_manager import verify_login

class CustomerLoginPage(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.page.title = "Customer's Login Page"
        self.page.window.width = 720
        self.page.window.height = 650
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        self.login_btn = ft.ElevatedButton(
            text="Login",
            on_click=self.handle_login,
            width=180,
            height=50,
            bgcolor=ft.colors.GREEN_600,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=24),
            ),
        )
        self.back_btn = ft.ElevatedButton(
            text="Back",
            on_click=self.go_home,
            width=150,
            height=40,
            bgcolor=ft.colors.ORANGE_700,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20)
            )
        )
        self.user_name_field = ft.TextField(label="Username", width=300)
        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

        self.header = ft.Text("Provide your Username and Password to proceed", text_align="center", size=28, weight="bold")
        self.status = ft.Text("", text_align="center", size=16, color="red")
        
        self.forgot_password = ft.Text("Forgot Password ?", text_align="center", size=20, weight="bold")
        self.forgot_password_btn = ft.ElevatedButton(
            text="Reset Password",
            on_click=self.to_change_password,
            width=150,
            height=40,
            bgcolor=ft.colors.PURPLE_700,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
            )
        )

    def to_change_password(self, e):
        """Navigate to the change password page."""
        from routes import navigate
        navigate(self.page, "CHANGE_PASSWORD")

    def handle_login(self, e):
        """Handle the login process when the login button is clicked."""
        user_name = self.user_name_field.value
        password = self.password_field.value
        if not user_name or not password:
            self.status.value = "Please fill in both fields"
            self.page.update(self.status)
            return

        # Verify login credentials
        authenticated_info = verify_login("Customer", user_name, password)

        if authenticated_info is None:
            self.page.snack_bar = ft.SnackBar(ft.Text("Invalid username or password"), open=True)
            self.page.update()
            return
        authenticated, customer_id, customer_name = authenticated_info

        if authenticated:
            self.page.session.set("customer_id", customer_id)
            self.page.session.set("customer_name", customer_name)
            self.page.snack_bar = ft.SnackBar(ft.Text("Login was successful. Redirecting to the Customer's dashboard...."), open=True)
            self.page.update()
            from routes import navigate
            navigate(self.page, "CUSTOMER_DASHBOARD")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Invalid username or password"), open=True)
            self.page.update()

    def go_home(self, e):
        """Navigate to the home page."""
        from routes import navigate
        navigate(self.page, "HOME")

    def build(self):
        """Build the login page layout."""
        return ft.Container(
            alignment=ft.Alignment(0.0, 0.0),
            width=None,
            height=None,
            content=ft.Stack(
                alignment=ft.Alignment(0.0, 0.0),
                controls=[
                    ft.Image(
                        src="assets/customer_login2.jpeg",
                        width=self.page.window.width,
                        height=self.page.window.height,
                        fit=ft.ImageFit.COVER,
                        opacity=0.23,
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.header,
                            self.user_name_field,
                            self.password_field,
                            self.status,
                            self.login_btn,  
                            self.back_btn, 
                            self.forgot_password,
                            self.forgot_password_btn,   
                        ]
                    )
                ]
            )
        )
