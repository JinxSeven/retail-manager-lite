
# 🛒 Supermarket Order Management System

This project is a GUI application developed to generate and manage customer orders in supermarkets. The application leverages Python for backend logic, SQLite for database management, and Qt for the graphical user interface.

## Features

- **📝 Customer Order Generation**: Create and manage customer orders with ease.
  
- **🔄 Order Management**: View, update, and delete existing orders.
  
- **🖥️ User-Friendly Interface**: Intuitive and easy-to-use graphical interface built with qT.
  
- **💾 Persistent Storage**: All orders are stored in an SQLite database, ensuring data persistence.

## Technologies Used

- **🐍 Python**: The primary programming language used for developing the application.
  
- **🗃️ SQLite**: A lightweight, disk-based database to store order data.
  
- **🎨 Qt**: A free and open-source widget toolkit for creating graphical user interfaces.

## Screenshots

*Login screen of the application.*

![SAGAYAM](https://github.com/JinxSeven/Cx_Orders/assets/164835921/071e0c82-310e-488e-9509-e7ecfb372ba3)

*Main screen of the application.*

![SAGAYAM_OE](https://github.com/JinxSeven/Cx_Orders/assets/164835921/c71f110e-f9ef-4cb4-9ac1-a0a22c424bad)

*Order management interface.*

![SAGAYAM_EO](https://github.com/JinxSeven/Cx_Orders/assets/164835921/b099cec1-f0ba-44f1-b787-a7373f91cb2f)

*View orders interface.*

![SAGAYAM_OL](https://github.com/JinxSeven/Cx_Orders/assets/164835921/e2a47392-afea-45ee-86ce-dfab419b8575)

## Installation

1. **📥 Clone the repository**
   ```bash
   git clone https://github.com/JinxSeven/Cx_Orders.git
   //Open the cloned folder
   ```

2. **📦 Install dependencies**
   Ensure you have `python` and `pip` installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   
3. **📝 Install required fonts**
   Install all `.ttf` files according your operating system
   ```bash
   cd assets/fonts_used
   ```
   
5. **🚀 Run the application**
   ```bash
   cd src
   python stocking.py
   ```

## Usage

1. **🆕 Create Orders**:
   - Open the application.
     
   - Navigate to the "Order Entry" section.
     
   - Fill in the required details and click "Submit" to create a new order.

2. **📝 Managing Orders**:
   - Navigate to the "Edit Orders" section.
     
   - Select an order to view, update, or delete.
     
   - Make the necessary changes and save them.

3. **📋 View Orders**:
   - Navigate to the "Orders" section.
     
   - Select a date to view orders place on that day.
     
   - Click show all to view all orders.

## Learning Acknowledgment

This project was developed with the knowledge and skills I gained by partaking in CS50x, a course provided by Harvard University.
