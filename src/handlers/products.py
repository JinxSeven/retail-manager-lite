import sqlite3
from src.config import  DB_PATH
from PyQt5 import QtCore
from src.utils.color import Color
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


class ProductHandler:
    def __init__(self, ui):
        self.ui = ui
        self.ui.prodAddBtn.clicked.connect(self.add_new_product)
        # self.ui.select_proid_2.currentIndexChanged.connect(self.load_product_details)

    def add_new_product(self):
        try:
            name = self.ui.prodAddNameInp.text()
            cp = float(self.ui.prodAddCostPriceInp.text())
            sp = float(self.ui.prodAddSellingPriceInp.text())
            quantity = int(self.ui.prodAddQuantityInp.text())
        except ValueError:
            self.ui.prodModPosInfoLbl.clear()
            self.ui.prodModNegInfoLbl.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.prodModNegInfoLbl.setText('Invalid Input')
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                "INSERT INTO product_data (product_name, cost_price, selling_price, quantity) VALUES (?, ?, ?, ?)",
                (name, cp, sp, quantity)
            )
            conn.commit()
            conn.close()
            
            self.ui.prodModNegInfoLbl.clear()
            self.ui.prodModPosInfoLbl.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.prodModPosInfoLbl.setText('Product added successfully')
            # self.load_product_ids()
        except sqlite3.Error as ex:
            self.ui.prodModPosInfoLbl.clear()
            self.ui.prodModNegInfoLbl.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.prodModNegInfoLbl.setText('Product might already exist ✖')
            print(Color.RED + f"An error occurred while adding product: {ex}" + Color.RED)
            return
        finally:
            self.ui.prodAddNameInp.clear()
            self.ui.prodAddCostPriceInp.clear()
            self.ui.prodAddSellingPriceInp.clear()
            self.ui.prodAddQuantityInp.clear()

    # def load_product_ids(self):
    #     try:
    #         self.ui.select_proid_2.clear()
    #         conn = sqlite3.connect(DB_PATH)
    #         cursor = conn.execute("SELECT product_id FROM product_data")
    #         products = cursor.fetchall()
    #         for product in products:
    #             self.ui.select_proid_2.addItem(str(product[0]))
    #         conn.close()
    #     except Exception as ex:
    #         print(f"Error loading product IDs: {ex}")

    # def load_product_details(self):
    #     try:
    #         conn = sqlite3.connect(DB_PATH)
    #         product_id = self.ui.select_proid_2.currentText()
    #         cursor = conn.execute("SELECT * FROM product_data WHERE product_id=?", (product_id,))
    #         result = cursor.fetchone()
    #         if result:
    #             self.ui.prodModName.setText(result[1])
    #             self.ui.prodModcp.setText(str(result[2]))
    #             self.ui.prodModsp.setText(str(result[3]))
    #         conn.close()
    #     except Exception as ex:
    #         print(f"Error loading product details: {ex}")
