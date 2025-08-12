import sqlite3
from functools import partial
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from src.config import DB_PATH
from src.utils.color import Color
from src.utils.services import Services

class DeleteOrderButton(QPushButton):
    # Constructor
    # Takes object name and callback func as args
    def __init__(self, ord_id: str, load_table_func, parent=None):
        icon = QIcon("assets/images/trash-can.svg")
        # Button
        # Base class (QPushButton) constructor
        super().__init__(icon, "", parent)
        self.setObjectName(f"{ord_id}")
        self.setStyleSheet("""
            QPushButton {   
                background-color: #c41c1c;
                font: 63 8pt "Poppins SemiBold";
                color: white;
                outline: 0;
                padding: 10px 20px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                cursor: pointer;
                background-color: #a51818;
            }
        """)
        
        self.clicked.connect(partial(self.__on_clicked, ord_id, load_table_func))

    def __on_clicked(self, ord_id, load_table_func):
        response = Services.confirmation_messagebox("Delete Order", "Are you sure you want to delete this order?")
        if response:
            try:
                with sqlite3.connect(DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM orders WHERE order_id = ?", (ord_id,))
                    conn.commit()
                    load_table_func()
                    
            except sqlite3.Error as ex:
                print(Color.RED + f"An SQLite error occurred: {ex}" + Color.RESET)
                # Services.display_info(self.ui.prodOrdInfoLbl, "Order deletion failed", Color.RED)
            except Exception as ex:
                print(Color.RED + f"An unexpected error occurred: {ex}" + Color.RESET)
                # Services.display_info(self.ui.prodOrdInfoLbl, "Order deletion failed", Color.RED)