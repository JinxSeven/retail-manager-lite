from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

from src.utils.view_order_modal import ViewOrderModal

class SaveOrderButton(QPushButton):
    def __init__(self, ord_id, parent=None):
        icon = QIcon('assets/images/download.svg')
        
        super().__init__(icon, "", parent)
        self.setObjectName(f"{ord_id}")
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {   
                background-color: #009688;
                font: 63 8pt "Poppins SemiBold";
                color: white;
                outline: 0;
                padding: 10px 20px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                cursor: pointer;
                background-color: #00897b;
            }
        """)
        
        self.clicked.connect(partial(self.__on_clicked, ord_id))
        
    def __on_clicked(self, ord_id):
        pass
        