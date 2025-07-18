from functools import partial

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from src.utils.services import Services


class DeleteButton(QPushButton):
    # Constructor
    # Takes object name and callback func as args
    def __init__(self, prod_name: str, prod_id: str, delete_func, parent = None):
        icon = QIcon("assets/images/trash-can.svg")
        # Button
        # Base class (QPushButton) constructor
        super().__init__(icon, "", parent)
        self.setObjectName(f"{prod_id}")
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
        
        self.clicked.connect(partial(self.on_delete, prod_name, prod_id, delete_func))
    
    # Calling back method from orders.py
    def on_delete(self, prod_name, prod_id, delete_func):
        proceed = Services.confirmation_messagebox("Order Modification", f"Do you want to remove {prod_name} from order?")
        if not proceed:
            return
        
        delete_func()
        