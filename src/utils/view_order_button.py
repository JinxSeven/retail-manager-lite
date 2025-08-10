from functools import partial

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

from src.utils.view_order_modal import ViewOrderModal


class ViewOrderButton(QPushButton):
    def __init__(self, ord_id, parent=None):
        icon = QIcon('assets/images/eye.svg')
        
        super().__init__(icon, "", parent)
        self.setObjectName(f"{ord_id}")
        self.setStyleSheet("""
            QPushButton {   
                background-color: #0b6bcb;
                font: 63 8pt "Poppins SemiBold";
                color: white;
                outline: 0;
                padding: 10px 20px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                cursor: pointer;
                background-color: #185ea5;
            }
        """)
        
        self.clicked.connect(partial(self.__on_clicked, ord_id))
        
    def __on_clicked(self, ord_id):
            modal = ViewOrderModal(ord_id)
            modal.exec_()
            
        