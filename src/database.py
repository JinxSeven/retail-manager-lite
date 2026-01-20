import os
import sys
import sqlite3
import shutil
from utils.color import Color

DB_NAME = "rma.db"

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def get_appdata_dir():
    base = os.getenv("APPDATA")
    app_dir = os.path.join(base, "RetailManagerLite")
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

def get_db_path():
    db_dst = os.path.join(get_appdata_dir(), DB_NAME)

    if not os.path.exists(db_dst):
        db_src = resource_path(os.path.join("database", DB_NAME))
        shutil.copyfile(db_src, db_dst)

    return db_dst

def get_connection():
    return sqlite3.connect(get_db_path())

def initialize_db():
    try:
        conn = get_connection()
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL UNIQUE,
                cost_price DECIMAL(10, 2) NOT NULL,
                selling_price DECIMAL(10, 2) NOT NULL,
                stock_quantity INTEGER NOT NULL DEFAULT 0
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                order_date_time DATETIME NOT NULL,
                cx_phone_num TEXT NOT NULL
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            product_name TEXT NOT NULL,
            product_price DECIMAL(10, 2) NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        conn.commit()
        conn.close()
        print(Color.GREEN + "DataBase initialized successfully!" + Color.GREEN)
    except Exception as ex:
        print(Color.RED + f"An error occurred while initializing database: {ex}" + Color.RED)


