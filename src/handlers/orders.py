import sqlite3
from config import DB_PATH
from PyQt5.QtWidgets import QTableWidgetItem

class OrderHandler:
    def __init__(self, ui):
        self.ui = ui
        self.ui.show_all.clicked.connect(self.show_orders)

    def show_orders(self):
        self.ui.orders_table.clear()
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.execute("SELECT * FROM order_data")
            orders = cursor.fetchall()

            self.ui.orders_table.setColumnCount(6)
            self.ui.orders_table.setRowCount(len(orders))

            for row_num, order in enumerate(orders):
                for col_num, data in enumerate(order):
                    self.ui.orders_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

            self.ui.orders_table.setHorizontalHeaderLabels(
                ['ID', 'Customer Name', 'Phone No', 'Product ID', 'Quantity', 'Date']
            )
            conn.close()
        except Exception as e:
            print(f"Error loading orders: {e}")
