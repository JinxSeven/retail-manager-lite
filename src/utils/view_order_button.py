from functools import partial

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

from src.utils.view_order_modal import ViewOrderModal

class ViewOrderButton(QPushButton):
    def __init__(self, ord_data, parent=None):
        icon = QIcon('assets/images/eye.svg')
        
        super().__init__(icon, "", parent)
        self.setObjectName(f"{ord_data[0]}")
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
        
        self.clicked.connect(partial(self.__on_clicked, ord_data))

    def __on_clicked(self, ord_data):
        print(ord_data)
        view_order_modal = ViewOrderModal(ord_data[0])
        
        view_order_modal.set_order_info(ord_data)
        view_order_modal.load_order_table(ord_data[0])
        
        view_order_modal.exec_()