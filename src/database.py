import sqlite3
from config import DB_PATH
from utils.color import Color

def initialize_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS product_data (
                product_id TEXT PRIMARY KEY,
                product_name TEXT NOT NULL UNIQUE,
                cost_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()
        print(Color.GREEN + "Initialized database successfully!" + Color.GREEN)
    except Exception as ex:
        print(Color.RED + f"An error occurred while initializing database: {ex}" + Color.RED)
    finally:
        conn.close()
