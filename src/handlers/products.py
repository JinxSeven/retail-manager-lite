import sqlite3
import uuid

from src.config import DB_PATH
from PyQt5 import QtCore
from src.utils.color import Color
from src.utils.services import Services

class ProductHandler:
    def __init__(self, ui):
        self.ui = ui
        self.services = Services()
        
        self.services.load_combobox(self.ui.prodModNameSel, "SELECT product_name FROM product_data")
        self.load_product_details()
        self.ui.prodAddBtn.clicked.connect(self.add_new_product)
        self.ui.prodModDeleteBtn.clicked.connect(self.delete_product)
        self.ui.prodModNameSel.currentIndexChanged.connect(self.load_product_details)

    def add_new_product(self):
        try:
            name = self.ui.prodAddNameInp.text()
            cp = float(self.ui.prodAddCostPriceInp.text())
            sp = float(self.ui.prodAddSellingPriceInp.text())
            quantity = int(self.ui.prodAddQuantityInp.text())
            id = str(uuid.uuid4())
        except ValueError:
            self.ui.prodModPosInfoLbl.clear()
            self.services.display_info(self.ui.prodModNegInfoLbl, 'Invalid Input')
            return
        
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                "INSERT INTO product_data (product_id, product_name, cost_price, selling_price, quantity) VALUES (?, ?, ?, ?, ?)",
                (id, name, cp, sp, quantity)
            )
            conn.commit()
            conn.close()
            
            self.ui.prodModNegInfoLbl.clear()
            self.services.display_info(self.ui.prodModPosInfoLbl, 'Product added successfully!')
            self.services.load_combobox(self.ui.prodModNameSel, "SELECT product_name FROM product_data")
            # self.load_product_details()
        except sqlite3.Error as ex:
            self.ui.prodModPosInfoLbl.clear()
            self.services.display_info(self.ui.prodModNegInfoLbl, 'Product might already exist!')
            print(Color.RED + f"An error occurred while adding product: {ex}" + Color.RED)
            return
        finally:
            self.ui.prodAddNameInp.clear()
            self.ui.prodAddCostPriceInp.clear()
            self.ui.prodAddSellingPriceInp.clear()
            self.ui.prodAddQuantityInp.clear()

    def delete_product(self):
        name = self.ui.prodModNameSel.currentText()
        id = self.ui.prodModIdInp.text()
        proceed = self.services.alert_messagebox("Product Mod", f"Do you want to proceed deleting {name}?")
        if not proceed:
            return
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("DELETE FROM product_data WHERE product_id=?", (id,))
                conn.commit()
                
            self.ui.prodModPosInfoLbl.clear()
            self.services.display_info(self.ui.prodModNegInfoLbl, 'Product deleted successfully!')
            self.services.load_combobox(self.ui.prodModNameSel, "SELECT product_name FROM product_data")
        except sqlite3.Error as ex:
            print(Color.RED + f"An error occurred while deleting product: {ex}")
            self.ui.prodModPosInfoLbl.clear()
            self.services.display_info(self.ui.prodModNegInfoLbl, 'Could not delete product')
            
    def load_product_details(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            selected_name = self.ui.prodModNameSel.currentText()
            cursor = conn.execute("SELECT * FROM product_data WHERE product_name=?", (selected_name,))
            result = cursor.fetchone()
            if result:
                self.ui.prodModIdInp.setText(str(result[0]))
                self.ui.prodModCostPriceInp.setText(str(result[2]))
                self.ui.prodModSellingPriceInp.setText(str(result[3]))
                self.ui.prodModQuantityInp.setText(str(result[4]))
            conn.close()
        except Exception as ex:
            print(Color.RED + f"An error occurred while adding product: {ex}" + Color.RED)
