import sqlite3
from config import DB_PATH
from PyQt5.QtWidgets import QTableWidgetItem

class ProductHandler:
    def __init__(self, ui):
        self.ui = ui
        self.ui.addNewPbtn.clicked.connect(self.add_new_product)
        self.ui.select_proid_2.currentIndexChanged.connect(self.load_product_details)

    def add_new_product(self):
        product_id = self.ui.addNewPid.text()
        product_name = self.ui.addNewPname.text()
        cp = float(self.ui.addNewPcp.text())
        sp = float(self.ui.addNewPsp.text())

        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO product_data VALUES (?, ?, ?, ?)", (product_id, product_name, cp, sp))
            conn.commit()
            conn.close()

            self.ui.addNewPid.clear()
            self.ui.addNewPname.clear()
            self.ui.addNewPcp.clear()
            self.ui.addNewPsp.clear()
            self.load_product_ids()
        except Exception as e:
            print(f"Error adding product: {e}")

    def load_product_ids(self):
        try:
            self.ui.select_proid_2.clear()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.execute("SELECT product_id FROM product_data")
            products = cursor.fetchall()
            for product in products:
                self.ui.select_proid_2.addItem(str(product[0]))
            conn.close()
        except Exception as e:
            print(f"Error loading product IDs: {e}")

    def load_product_details(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            product_id = self.ui.select_proid_2.currentText()
            cursor = conn.execute("SELECT * FROM product_data WHERE product_id=?", (product_id,))
            result = cursor.fetchone()
            if result:
                self.ui.prodModName.setText(result[1])
                self.ui.prodModcp.setText(str(result[2]))
                self.ui.prodModsp.setText(str(result[3]))
            conn.close()
        except Exception as e:
            print(f"Error loading product details: {e}")
