from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

class DeleteButton(QPushButton):
    def __init__(self, parent=None):
        icon = QIcon("assets/images/trash-can.svg")
        super().__init__(icon, "", parent)
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
        