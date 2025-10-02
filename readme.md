# Retail Manager Lite

A comprehensive GUI-based billing system designed for retail outlets to efficiently handle customer orders, product info, and stock levels. The application is built with **Python** for backend logic, **SQLite** for reliable database management, and **Qt** for a responsive, user-friendly interface.

## 2.0 Change Logs
- **Added Order Preview Table**: View products as they are being added and manage order items.
- **Product Inventory Manager**: Add, edit or remove products and manage stocks in the  `Product Mod` tab.
- **UI Enhancement**: Filled empty spaces with beneficial features, updated icons and overall improved user journey.
- **Order Management**: Implemented search, filter and sort feature, provided options to save, view and delete orders.
- **Refactored**: Improved and cleaned code. Buttons and input fields are no longer named `btn_one`, `inp_two` Lol. Functions are named after the action they perform. 

## Interface
<img width="503" height="572" alt="image" src="https://github.com/user-attachments/assets/a51d3590-f08e-4501-9c37-3a297556f752" />
<img width="503" height="572" alt="image" src="https://github.com/user-attachments/assets/18b5b2ad-ad9c-4bc6-a813-553374a55157" />
<img width="503" height="572" alt="image" src="https://github.com/user-attachments/assets/8c200e2f-40ab-4c85-9a9e-76ea91ea40f3" />
<img width="503" height="572" alt="image" src="https://github.com/user-attachments/assets/6ce09b9b-a209-4b67-8ec5-ac7ea24f6d2c" />
<img width="503" height="572" alt="image" src="https://github.com/user-attachments/assets/789f967b-aeb3-4b12-9b10-c370bfd50a72" />



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
