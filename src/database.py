import sqlite3
from utils.color import Color
from config import get_db_path

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
