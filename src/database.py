import sqlite3
from config import DB_PATH
from utils.color import Color

def initialize_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS product_data (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                cost_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_data (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cx_name TEXT NOT NULL,
                cx_phno TEXT,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES product_data(product_id)
            )
        """)
        conn.commit()
        print(Color.GREEN + "Database Initialized Successfully!" + Color.RESET)
    except Exception as e:
        print(Color.RED + f"Error initializing database: {e}" + Color.RESET)
    finally:
        conn.close()
