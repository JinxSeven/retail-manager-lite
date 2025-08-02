import sqlite3
import secrets
from datetime import datetime
from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from src.config import DB_PATH
from src.models.order_model import Order
from src.utils.color import Color
from src.utils.delete_button import DeleteButton
from src.utils.services import Services


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
        self.ui.orderDateLbl.setText(datetime.today().strftime('%d.%m.%Y'))
        self.ui.addToBillBtn.clicked.connect(self.add_product_to_bill)
        self.ui.submitOrderBtn.clicked.connect(self.submit_order)

        # Loading combobox with product names
        Services.load_combobox(self.ui.prodOrdNameSel, "SELECT product_name FROM products")
        self.ui.prodOrdNameSel.currentIndexChanged.connect(self.load_prod_quant)
        
    def generate_order_id(self):
        self.ui.orderIdLbl.setText(str(secrets.token_hex(4)))

    def load_prod_quant(self):
        if self.current_order is []:
            return
        else:
            prod_name = self.ui.prodOrdNameSel.currentText()
            prod_quant = next((prod.quantity for i, prod in enumerate(self.current_order) if prod.product_name == prod_name), 0)
            
            if prod_quant != 0:
                self.ui.prodOrdQuantInp.setText(str(prod_quant))
            else:
                self.ui.prodOrdQuantInp.clear()
            
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
                                                                               self.delete_prod, self.ui.prodOrdTbl))
            else:
                self.current_order[matching_index].quantity = quantity
                
                self.calculate_total()
                # Finding row with matching product ID
                match = self.ui.prodOrdTbl.findItems(product_item.product_name, Qt.MatchExactly)
                row_to_update = match[0].row()
                self.ui.prodOrdTbl.setItem(row_to_update, 3,
                                           QTableWidgetItem(str(self.current_order[matching_index].quantity)))
                self.ui.prodOrdTbl.setItem(row_to_update, 4, QTableWidgetItem(
                    str(product_item.product_price * self.current_order[matching_index].quantity)))
            # Clearing quantity field after adding prod to bill
            # self.ui.prodOrdQuantInp.clear()
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
        
    def renumber_serial_numbers(self, current_row: int):
        for i in range(current_row, self.ui.prodOrdTbl.rowCount()):
            self.ui.prodOrdTbl.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            

    def delete_prod(self, prod_id: str, row_to_delete: int):
        for prod in self.current_order[:]:
            if prod.product_id == prod_id:
                self.current_order.remove(prod)
                break

        self.ui.prodOrdTbl.removeRow(row_to_delete)
        self.calculate_total()
        self.load_prod_quant()
        self.renumber_serial_numbers(row_to_delete)

    def submit_order(self):
        try:
            with sqlite3.connect(DB_PATH, timeout=10) as conn:
                cursor = conn.cursor()
                OrderId = self.ui.orderIdLbl.text()
                grandTotal = float(self.ui.grandTotalDsp.text())
                phone = self.ui.prodOrdPhoneInp.text()
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                conn.execute("BEGIN TRANSACTION")

                # Insert order header
                cursor.execute("""
                    INSERT INTO orders(order_id, order_date_time, cx_phone_num, grand_total) 
                    VALUES (?, ?, ?, ?)""",
                    (OrderId, current_datetime, phone, grandTotal)
                )

                # Insert order items
                for record in self.current_order:
                    cursor.execute("""
                        INSERT INTO order_items(order_id, product_id, quantity) 
                        VALUES (?, ?, ?)""",
                        (record.order_id, record.product_id, record.quantity)
                    )

                conn.commit()
                self.clear_orders_tab()
                Services.display_info(self.ui.prodOrdInfoLbl,"Order submitted successfully",'green')

        except sqlite3.Error as ex:
            Services.display_info(self.ui.prodOrdInfoLbl,"Order submission failed",Color.RED)
            print(Color.RED + f"An SQLite error occurred: {ex}" + Color.RESET)
        except Exception as ex:
            Services.display_info(self.ui.prodOrdInfoLbl,"Order submission failed",Color.RED)
            print(Color.RED + f"An unexpected error occurred: {ex}" + Color.RESET)

    def clear_orders_tab(self):
        self.ui.prodOrdPhoneInp.clear() # clears the phone number in orders
        self.ui.lineEdit.clear() # clears the points field 
        self.ui.prodOrdQuantInp.clear() # clears the NOS field
        self.ui.grandTotalDsp.clear() # clears the grandTotal
        self.ui.prodOrdTbl.clearContents() # clears the table
        self.generate_order_id()
                
            
            
            
            