import sqlite3
import secrets
import datetime
from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from src.config import DB_PATH
from src.models.order_model import Order
from src.utils.color import Color
from src.utils.delete_button import DeleteButton
from src.utils.services import Services


# TODO - Edit product quantity in bill

class OrderHandler:
    current_order: List[Order] = []

    def __init__(self, ui):
        self.ui = ui

        # Setting ctable column width
        self.ui.prodOrdTbl.setColumnWidth(0, 10)
        self.ui.prodOrdTbl.setColumnWidth(1, 200)
        self.ui.prodOrdTbl.setColumnWidth(2, 65)
        self.ui.prodOrdTbl.setColumnWidth(3, 65)
        self.ui.prodOrdTbl.setColumnWidth(4, 80)
        self.ui.prodOrdTbl.setColumnWidth(5, 15)

        self.generate_order_id()
        self.ui.orderDateLbl.setText(datetime.date.today().strftime('%d.%m.%Y'))
        self.ui.addToBillBtn.clicked.connect(self.add_product_to_bill)

        # Loading combobox with product names
        Services.load_combobox(self.ui.prodOrdNameSel, "SELECT product_name FROM products")

    def generate_order_id(self):
        self.ui.orderIdLbl.setText(str(secrets.token_hex(4)))

    def delete_order_item(self):
        # TODO - Delete order item from bill table
        raise NotImplementedError("This method is not implemented")

    def add_product_to_bill(self):
        try:
            order_id = self.ui.orderIdLbl.text()
            product_name = self.ui.prodOrdNameSel.currentText()
            quantity = int(self.ui.prodOrdQuantInp.text())
        except ValueError as ex:
            Services.display_info(self.ui.prodOrdInfoLbl, "Input type mismatch!", 'red')
            print(Color.RED + f"Input Exception: {ex}" + Color.RED)
            return

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute("SELECT selling_price FROM products WHERE product_name = ?", (product_name,))
                product_price = cursor.fetchone()
                cursor = conn.execute("SELECT product_id FROM products WHERE product_name = ?", (product_name,))
                product_id = cursor.fetchone()

            product_item = Order(
                order_item_id=len(self.current_order),
                order_id=order_id,
                product_id=product_id[0],
                product_name=product_name,
                product_price=product_price[0],
                quantity=quantity,
            )

            # Checks if product with same ID exists
            self.ui.prodOrdTbl.verticalHeader().setVisible(False)
            matching_index = next(
                (i for i, item in enumerate(self.current_order) if item.product_id == product_item.product_id), -1)
            if matching_index == -1:
                self.current_order.append(product_item)
                self.calculate_total()
                # Append new item to table
                row_position = self.ui.prodOrdTbl.rowCount()
                self.ui.prodOrdTbl.insertRow(row_position)
                self.ui.prodOrdTbl.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))
                self.ui.prodOrdTbl.setItem(row_position, 1, QTableWidgetItem(str(product_item.product_name)))
                self.ui.prodOrdTbl.setItem(row_position, 2, QTableWidgetItem(str(product_item.product_price)))
                self.ui.prodOrdTbl.setItem(row_position, 3, QTableWidgetItem(str(product_item.quantity)))
                self.ui.prodOrdTbl.setItem(row_position, 4,
                                           QTableWidgetItem(str(product_item.product_price * product_item.quantity)))
                self.ui.prodOrdTbl.setCellWidget(row_position, 5, DeleteButton(str(product_item.product_name),
                                                                               str(product_item.product_id),
                                                                               row_position, self.delete_prod))
            else:
                self.current_order[matching_index].quantity += quantity
                
                self.calculate_total()
                # Finding row with matching product ID
                match = self.ui.prodOrdTbl.findItems(product_item.product_name, Qt.MatchExactly)
                row_to_update = match[0].row()
                self.ui.prodOrdTbl.setItem(row_to_update, 3,
                                           QTableWidgetItem(str(self.current_order[matching_index].quantity)))
                self.ui.prodOrdTbl.setItem(row_to_update, 4, QTableWidgetItem(
                    str(product_item.product_price * self.current_order[matching_index].quantity)))
            # Clearing quantity field after adding prod to bill
            self.ui.prodOrdQuantInp.clear()
        except sqlite3.Error as ex:
            print(Color.RED + f"SQLite Exception: {ex}" + Color.RED)
            return
        except Exception as ex:
            print(Color.RED + f"Regular Exception: {ex}" + Color.RED)
            return
        finally:
            conn.close()

    def calculate_total(self):
        total = 0.0
        for i in range(len(self.current_order)):
            total += self.current_order[i].product_price * self.current_order[i].quantity

        self.ui.grandTotalDsp.setText(str(total))

    def delete_prod(self, prod_id: str, row_to_delete: int):
        for prod in self.current_order[:]:
            if prod.product_id == prod_id:
                self.current_order.remove(prod)
                break

        self.ui.prodOrdTbl.removeRow(row_to_delete)
        self.calculate_total()

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
