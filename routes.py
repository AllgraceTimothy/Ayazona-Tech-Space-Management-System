import flet as ft

# Importing custom page classes from different modules
from home import HomePage
from signup import SignUpPage
from manager_login import ManagerLoginPage
from customer_login import CustomerLoginPage
from manager_dashboard import ManagerDashboard
from customer_dashboard import CustomerDashboard
from add_product import AddProductPage
from update_stock import UpdateStockPage
from confirm_purchases import CheckPurchasesPage
from receipt import GenerateReceipt
from transaction_history import GenerateHistory
from reset_password import ChangePasswordPage

# Defines a dictionary of routes to match specific URLs to their corresponding page names
ROUTES = {
  "HOME": "/",
  "SIGN_UP": "/sign-up",
  "CUSTOMER_LOGIN": "/customer_login",
  "MANAGER_LOGIN": "/manager_login",
  "MANAGER_DASHBOARD": "/manager_dashboard",
  "CUSTOMER_DASHBOARD": "/customer_dashboard",
  "ADD_PRODUCT": "/add_new_product",
  "UPDATE_STOCK": "/update_stock_levels",
  "CHECK_PURCHASES": "/check_purchases",
  "RECEIPT": "/receipt",
  "TRANSACTION_HISTORY": "/transactions_history",
  "CHANGE_PASSWORD": "/change_password",
}

# Defines a mapping of routes to their corresponding page classes
PAGE_CLASSES = {
  ROUTES["HOME"]: HomePage,
  ROUTES["SIGN_UP"]: SignUpPage,
  ROUTES["CUSTOMER_LOGIN"]: CustomerLoginPage,
  ROUTES["MANAGER_LOGIN"]: ManagerLoginPage,
  ROUTES["MANAGER_DASHBOARD"]: ManagerDashboard,
  ROUTES["CUSTOMER_DASHBOARD"]: CustomerDashboard,
  ROUTES["ADD_PRODUCT"]: AddProductPage,
  ROUTES["UPDATE_STOCK"]: UpdateStockPage,
  ROUTES["CHECK_PURCHASES"]: CheckPurchasesPage,
  ROUTES["RECEIPT"]: GenerateReceipt,
  ROUTES["TRANSACTION_HISTORY"]: GenerateHistory,
  ROUTES["CHANGE_PASSWORD"]: ChangePasswordPage,
}

# Handles navigation between different pages
def navigate(page: ft.Page, route_key: str, **kwargs):
  """
  Navigates to a specific page based on the provided route key.

  Args:
    page (ft.Page): The Flet page instance to update.
    route_key (str): Key indicating which page to navigate to.
    **kwargs: Additional parameters passed to the page class constructor.
  """
  # Clears any existing views on the page
  page.views.clear()

  page.theme_mode = "dark"
  page.window_width = 720
  page.window_height = 550

  # Gets the route URL corresponding to the given route key
  route = ROUTES.get(route_key)

  if route:
    # Retrieve the page class associated with the route
    page_class = PAGE_CLASSES.get(route)
    if page_class:
      # Create an instance of the page class and add it as a view
      control_instance = page_class(page, **kwargs) 
      page.views.append(
        ft.View(
          route=route,
          controls=[control_instance],  # The page instance is added to the controls
        )
      )
    else:
      # Handles missing page class by displaying a 404 error message
      page.views.append(
        ft.View(
          route=route,
          controls=[ft.Text("404: Page Not Found", size=24, weight="bold")],
          )
        )
  else:
    # Handles invalid route keys by displaying a 404 error message
    page.views.append(
      ft.View(
        route=route,
        controls=[ft.Text("404: Page Not Found", size=24, weight="bold")],
        )
    )
  # Applies updates to the page to reflect the changes
  page.update()

