import sqlite3
from logging import raiseExceptions

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QLabel
from PyQt5 import uic

from src.config import DB_PATH
from src.utils.color import Color
from src.utils.services import Services


class ViewOrderModal(QDialog):
    def __init__(self, order_id: str, parent=None):
        super().__init__(parent)
        
        uic.loadUi("assets/ui/view_order_modal.ui", self)
        
        self.setModal(True)
        self.setWindowTitle(f"Bill No: {order_id}")
        
        self.viewOrdOrdTbl.setColumnWidth(0, 472)
        
    def set_order_info_labels(self, ord_data):
        self.viewOrdOrdNum.setText(ord_data[0])
        self.viewOrdDateTime.setText(str(ord_data[1]))
        self.viewOrdPhoneNo.setText(ord_data[2])
        self.viewOrdOrdTotal.setText(str(ord_data[3]))
        
    def load_order_table(self, ord_data, dsp_label: QLabel):
        self.viewOrdOrdTbl.setRowCount(0)
        
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        prd.product_name,
                        prd.selling_price,
                        ord.quantity,
                        prd.selling_price * ord.quantity AS item_total,
                        COUNT(ord.order_id) OVER (PARTITION BY ord.order_id) AS order_item_count
                    FROM order_items AS ord
                    JOIN products AS prd ON ord.product_id = prd.product_id
                    WHERE order_id is ?
                """, (ord_data[0],))
                
                results = cursor.fetchall()
                items_count_set: bool = False
                
                if results:
                    for row_index, row_data in enumerate(results):
                        self.viewOrdOrdTbl.insertRow(row_index)
                        for col_index, col_data in enumerate(row_data):
                            if col_index == 4 and items_count_set is False:
                                self.viewOrdOrdItems.setText(str(col_data))
                                items_count_set = True
                                continue
                            
                            self.viewOrdOrdTbl.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
                
        except sqlite3.Error as ex:
            print(Color.RED + f"An SQLite error occurred: {ex}" + Color.RESET)
            Services.display_info(dsp_label, "There was an issue with retrieving your order!", "red")
            raise sqlite3.Error(f"An SQLite error occurred: {ex}") from ex
        except Exception as ex:
            print(Color.RED + f"An unexpected error occurred: {ex}" + Color.RESET)
            Services.display_info(dsp_label, "There was an issue with displaying your order!", "red")
            raise Exception(f"An unexpected error occurred: {ex}") from ex
            