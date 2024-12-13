# Ayazona Tech-Space Management System
 A powerful and user-friendly solution for managing shopping mall inventory and facilitating customer purchases. Built with Flet for an intuitive user interface and SQLite3 for a reliable and efficient backend.

 ---

## 🚀 Features
 ### Manager Dashboard:
  - Add, update, and manage inventory in real-time.
  - Edit stock levels and unit prices seamlessly.
  - Monitor inventory changes with ease.
 ### Customer Dashboard:
  - Browse available products in a simple and intuitive interface.
  - Make secure purchases effortlessly.
 ### Secure Login System:
  - Separate login for managers and customers.
  - User's credentials are securely stored in the database.
 ### Real-Time Inventory Updates:
  - Automatic stock adjustment after customer purchases.
  - Instantly updated stock availability for both managers and customers.
 ### Purchase History Tracking:
  - Maintains a detailed record of customer purchases, including:
   - **Product**: Name and ID.
   - **Quantity**: Number of items purchased.
   - **Total Price**: Cost of the purchase.
   - **Date**: Transaction date for reference.

---

## 📦 Installation Instructions
 ### Prerequisites:
  - A code editor (e.g., VSCode, PyCharm).
  - Python (version 3.7 or higher).
  - SQLite3 (comes pre-installed with Python in most environments).
  - Git.
 ### Steps:
  1. **Create a Project Folder**
 Choose a desired location on your computer and create a folder for the project.
  2. **Navigate into the Folder**
 Open the folder in your code editor.
  3. **Install Git**
 Ensure Git is installed.
 ```bash
    git --version
 ```
    - If not installed download it [here](https://git-scm.com/downloads)
  4. **Install virtualenv**
 This enables you to create and work in a virtual environment.
 ```bash
    pip install virtualenv
 ```
  5. **Create a virtual environment**
 ```bash
    python -m venv env
 ```
 Replace env with your desired environment name.
 It might take a while kindly remain patient 😇
  6. **Activate the virtual environment**
   - Windows
 ```bash
    env\Scripts\activate
 ```
   - macOS/Linux:
 ```bash
     source env/bin/activate
 ```
  7. **Clone the Repository**
 ```bash
     git clone https://github.com/AllgraceTimothy/Ayazona-Tech-Space-Management-System
 ```
  8. **Navigate into the Projects Directory**
 ```bash
     cd Ayazona-Tech-Space-Management-System
 ```
  9. **Install Dependencies**
 ```bash
     pip install -r requirements.txt
 ```
    - It might also take a while 😇
  10. **Run the Application**
 Desktop GUI: 
 ```bash
     flet run landing_page.py
 ```
 Web browser: 
 ```bash
     flet run --web landing_page.py
 ```

## 📖 Usage
 1. **Manager Login**
  - Use manager credentials to log in.
  - Navigate to the dashboard to manage inventory, update stock, and edit product prices.
  - Default Manager's Secret Key: sct_key.765

 2. **Customer Login**
  - Log in with customer credentials.
  - Browse products, make purchases, view your receipt, and view transaction history.

 3. **Tracking Purchases**
  - The system automatically records all customer transactions for future reference.

## 🛠️ Technologies Used
 - ***Frontend***: Flet (Python-Based GUI framework)
 - ***Backend:*** SQLite3 Database
 - ***Programming Language:*** Python
 - ***Libraries:***
  - datetime: (Tracking purchase dates)
  - flet: (GUI development)
  - re: (Input validation)

## 👥 Contributors
 - [Timothy Allgrace](https://github.com/AllgraceTimothy) - Developer

## 📝 License
 - This project is licensed under the MIT License.
