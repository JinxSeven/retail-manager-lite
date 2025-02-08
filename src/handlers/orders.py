import sqlite3
import secrets
import datetime
from src.config import DB_PATH
from src.utils.services import Services
from PyQt5.QtWidgets import QTableWidgetItem

class OrderHandler:
    def __init__(self, ui):
        self.ui = ui
        self.services = Services()
        
        self.generate_order_id()
        
        self.ui.orderDateLbl.setText(datetime.date.today().strftime('%d.%m.%Y'))
        self.services.load_combobox(self.ui.prodOrdNameSel, "SELECT product_name FROM products")
        
    def generate_order_id(self):
        self.ui.orderIdLbl.setText(str(secrets.token_hex(8)))

    # def add_order(self):
    #     try:
    #         order_id = self.ui.orderIdLbl.text()
    #         product_name = self.ui.prodOrdNameSel.currentText()
    #         cx_phone_number = int(self.ui.prodOrdPhoneInp.text())
    #         quantity = int(self.ui.prodOrdQuantInp.text())
    #     except ValueError:
            
    
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
