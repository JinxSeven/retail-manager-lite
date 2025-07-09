import sqlite3
import secrets
import datetime
from src.config import DB_PATH
from src.utils.color import Color
from src.utils.services import Services

class OrderHandler:
    def __init__(self, ui):
        self.ui = ui
        
        self.generate_order_id()
        self.ui.orderDateLbl.setText(datetime.date.today().strftime('%d.%m.%Y'))       
        # Loading combobox with product names
        Services.load_combobox(self.ui.prodOrdNameSel, "SELECT product_name FROM products")
        
    def generate_order_id(self):
        self.ui.orderIdLbl.setText(str(secrets.token_hex(4)))

    def add_product_to_bill(self):
        try:
            order_id = self.ui.orderIdLbl.text()
            product_name = self.ui.prodOrdNameSel.currentText()
            cx_phone_number = int(self.ui.prodOrdPhoneInp.text())
            quantity = int(self.ui.prodOrdQuantInp.text())
        except ValueError as ex:
            Services.display_info(self.ui.prodOrdInfoLbl, "Input type mismatch!", 'red')
            print(Color.RED + f"Input Exception: {ex}" + Color.RED)
            return

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute("SELECT 1 FROM orders WHERE order_id = ?", (order_id,))
                newOrder: bool = cursor.fetchone() is None
                # FIXME - Pick it up from here
                cursor = conn.execute("SELECT selling_price FROM products WHERE product_name = ?", (product_name,))
                result = cursor.fetchone()
                total = float(result[0]) * quantity
                conn.close()
        except sqlite3.Error as ex:
            print(Color.RED + f"SQLite Exception: {ex}" + Color.RED)
        except Exception as ex:
            print(Color.RED + f"Regular Exception: {ex}" + Color.RED)
            return
                
                
    
    # def showOrders(self):
    #     self.tabWidget.setCurrentIndex(3)
    #     self.orders_table.clear()
    #     ord_lst = sqlite3.connect(db_path)
    #     cursor = ord_lst.execute("SELECT * FROM order_data")
    #     result = cursor.fetchall()
    #     row, col = 0, 0
    #     for row_num, row_data in enumerate(result):
    #         row += 1
    #         col = 0
    #         for col_num, data in enumerate(row_data):
    #             col += 1
    #     self.orders_table.setColumnCount(col)
    #     for row_num, row_data in enumerate(result):
    #         self.orders_table.insertRow(row_num)
    #         for col_num, data in enumerate(row_data):
    #             self.orders_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
    #     self.orders_table.setHorizontalHeaderLabels(
    #         ['ID', 'Customer Name', 'Phone No', 'Product ID', 'Quantity', 'Date'])
    #     # self.orders_table.resizeColumnsToContents()
    #     # self.orders_table.verticalHeader().setVisible(False)
    #     # for column in range(self.orders_table.columnCount()):
    #     # self.orders_table.setColumnWidth(column, max(114, self.orders_table.columnWidth(column)))
    #     self.orders_table.setColumnWidth(0, 65)
    #     self.orders_table.setColumnWidth(1, 220)
    #     self.orders_table.setColumnWidth(2, 130)
    #     self.orders_table.setColumnWidth(3, 100)
    #     self.orders_table.setColumnWidth(4, 80)
    #     self.orders_table.setColumnWidth(5, 95)
    #     rowsize = self.orders_table.rowCount()
    #     if rowsize > 9:
    #         self.orders_table.setColumnWidth(5, 90)
    #         if rowsize > 19:
    #             self.orders_table.setColumnWidth(0, 63)
