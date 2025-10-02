# Retail Manager Lite

A comprehensive GUI-based billing system designed for retail outlets to efficiently handle customer orders, product info, and stock levels. The application is built with **Python** for backend logic, **SQLite** for reliable database management, and **Qt** for a responsive, user-friendly interface.


## 2.0 Change Logs
- **Added Order Preview Table**: View products as they are being added and manage order items.
- **Product Inventory Manager**: Add, edit or remove products and manage stocks in the  `Product Mod` tab.
- **UI Enhancement**: Filled empty spaces with beneficial features, updated icons and overall improved user journey.
- **Order Management**: Implemented search, filter and sort feature, provided options to save, view and delete orders.
- **Refactored**: Improved and cleaned code. Buttons and input fields are no longer named `btn_one`, `inp_two` Lol. Functions are named after the action they perform. 

## Features
- **Customer Order Generation**: Create and manage customer orders with ease.  
- **Order & Product Management**: Add, update, and delete orders and products.  
- **Stock Management**: Track and update inventory levels to maintain accurate stock records.  
- **User-Friendly Interface**: Clean and intuitive GUI built with Qt.  
- **Persistent Storage**: Orders and stock data are securely stored in an SQLite database.

## Tech Stack
- **Python** – Backend application logic  
- **Qt** – Graphical user interface  
- **SQLite** – Lightweight relational database

## Getting Started

> [!NOTE]
> **Clone The Repo**:
> 
> Copy the command given below and run it in your terminal.
> ```bash
> git clone https://github.com/JinxSeven/retail-manager-lite.git
> ```
>
> **Install Dependencies**:
> 
> The project needs a lot of dependencies, mostly Qt packages. Go to the root of the project and run the command given below.
> ```bash
> pip install -r requirements.txt
> ```
> This should automatically set your local machine ready to run the project.
> 
> **Run/Debug Configuration**:
> 
> Point the run/debug configuration to the `program.py` file as the startup file which can be found inside the `src` folder.
> 
   
> [!IMPORTANT]
> **Install Required Fonts**:
> 
> Install all the fonts given in assets folder for better experience
> ```bash
> cd assets/native_fonts
> ```

## Learning Acknowledgment

This project was developed with the knowledge and skills I gained by partaking in CS50x, a course provided by Harvard University.
