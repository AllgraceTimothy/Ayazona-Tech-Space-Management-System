import flet as ft
from routes import navigate

class MainPage(ft.UserControl):
  def build(self):
      """Build the UI for the main page."""
      return ft.Container(
          bgcolor=ft.colors.TRANSPARENT,
          width=None,
          height=None,
          content=self.create_main_content()
      )

  def create_main_content(self):
      """Create the main content of the page, including text and buttons."""
      return ft.Column(
          alignment=ft.MainAxisAlignment.CENTER,
          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
              self.create_welcome_text(),
              self.create_action_buttons(),
          ]
      )
  
  def create_welcome_text(self):
      """Create the welcome text for the main page."""
      return ft.Text(
          "Welcome to the Ayazona Techplace!\nYour one-stop-shop for all electronic products",
          size=28,
          weight="bold",
          text_align=ft.TextAlign.CENTER,
          color=ft.colors.ORANGE_ACCENT_200,
      )

  def create_action_buttons(self):
      """Create the action buttons for navigating to the home page and exiting."""
      return ft.Row(
          alignment=ft.MainAxisAlignment.CENTER,
          controls=[
              self.create_home_button(),
              self.create_exit_button(),
          ]
      )
  
  def create_home_button(self):
      """Create the 'Go to Home Page' button."""
      return ft.ElevatedButton(
          text="Continue to Home Page",
          on_click=self.go_to_home_page,
          width=250,
          height=50,
          bgcolor=ft.colors.GREEN_600,
          color=ft.colors.WHITE,
          style=ft.ButtonStyle(
              shape=ft.RoundedRectangleBorder(radius=32),
          )
      )

  def create_exit_button(self):
      """Create the 'Exit' button."""
      return ft.ElevatedButton(
          text="Close App",
          on_click=self.exit_app,
          width=120,
          height=35,
          bgcolor=ft.colors.RED_600,
          color=ft.colors.WHITE,
          style=ft.ButtonStyle(
              shape=ft.RoundedRectangleBorder(radius=32),
          )
      )

  def go_to_home_page(self, e):
      """Navigate to the home page."""
      navigate(self.page, "HOME")

  def exit_app(self, e):
      """Exit the application."""
      self.page.window.close()


def main(page: ft.Page):
    """Set up the page settings and add the MainPage control."""
    page.title = "Ayazona Techspace"
    page.theme_mode = "dark"
    page.window.width = 720
    page.window.height = 650
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="background_images/landing_page_bg.jpg",
            fit=ft.ImageFit.COVER,
            opacity=0.2,
        )
    )

    page.add(MainPage())  # Add the MainPage control to the page


if __name__ == "__main__":
    ft.app(target=main)  # Runs the app
