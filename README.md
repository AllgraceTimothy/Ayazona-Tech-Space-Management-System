# Ayazona Tech-Place Management System
  - A powerful and user-friendly solution for managing shopping mall inventory and facilitating customer purchases. Built with Flet for an intuitive user interface and SQLite3 for a reliable and efficient backend.

# 🚀 Features
 ## Manager Dashboard:
  - Add, update, and manage inventory in real-time.
  - Edit stock levels and unit prices seamlessly.
  - Monitor inventory changes with ease.
 ## Customer Dashboard:
  - Browse available products in a simple and intuitive interface.
  - Make secure purchases effortlessly.
 ## Secure Login System:
  - Separate login for managers and customers.
  - User credentials are securely stored in the database.
 ## Real-Time Inventory Updates:
  - Automatic stock adjustment after customer purchases.
  - Instantly updated stock availability for both managers and customers.
 ## Purchase History Tracking:
  - Maintain a detailed record of customer purchases, including:
   - Product: Name and ID.
   - Quantity: Number of items purchased.
   - Total Price: Cost of the purchase.
   - Date: Transaction date for reference.

# 📦 Installation Instructions
 ## Prerequisites:
  - Code Editor. Can be VSCode, Pycharm e.t.c
  - Install Python (version 3.7 or higher).
  - Install SQLite3 (comes pre-installed with Python in most environments).
 ## Steps:
  1. Create a folder in your desired location.
  2. Navigate into your folder from your Code Editor.
  3. Create a virtual environment in this folder
   - Give the following command in the terminal -> "python -m venv env" (env-name of your virtual environment. Can be anything)
  4. Navgate into your virtual environment
   - Give the following command in the terminal -> "env\Scripts\activate" (again {env} can be anything)
  5. Clone the Repository in your virtual environment:
   - Give the following command in the terminal -> "git clone https://github.com/AllgraceTimothy/Ayazona-Tech-Space-Management-System"
   - Give the following command in the terminal -> "cd Ayazona-Tech-Space-Management-System"
  6. Install Dependencies:
   - Give the following command in the terminal -> "pip install -r requirements.txt"
  7. Run the Application:
   - In desktop GUI: Give the following command in the terminal -> "flet run landing_page.py"
   - In a we browser: Give the following command in the terminal -> "flet run --web landing_page.py"
  8. Open the Application in your Browser or on the provided desktop GUI

# 📖 Usage
 1. Manager Login:
  - Use your manager credentials to log in.
  - Navigate to the dashboard to manage inventory, update stock, and edit product prices.
  - The Manager's Secret Key Value is set to "sct_key.765"

 2. Customer Login:
  - Log in with your customer credentials.
  - Browse products, make purchases, and receive real-time updates.

 3. Tracking Purchases:
  - The system automatically records all customer transactions for future reference.

# 🛠️ Technologies Used
 - Frontend: Flet (Python-Based GUI framework)
 - Backend: SQLite3 Database
 - Programming Language: Python
 - Libraries Used:
  - datetime (tracking purchase dates)
  - flet (GUI framework)
  - re (validating format of username, email, and password)

# 👥 Contributors
 - Timothy Allgrace (https://github.com/AllgraceTimothy) - Developer

# 📝 License
 - This project is licensed under the MIT License.

