import sqlite3
from PyQt5.QtWidgets import QMessageBox, QComboBox
from src.config import DB_PATH
from .color import Color
from PyQt5 import QtCore

class Services:
    def confirmation_messagebox(self, title: str, message: str) -> bool:
        msg = QMessageBox()
    
        msg.setWindowTitle(title)
        msg.setText(message)
    
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)    
        # Apply the stylesheet
        msg.setStyleSheet("""
            QDialog {
                background-color: #333333;
            }
            QLabel {
                color: #EEEEEE;
                font-family: 'Poppins';
                font-size: 12px;
                padding-right: 20px;
                padding-top: 10px;
            }
            QPushButton {
                width: 50px;
                background-color: #555555;
                border: 1px solid #777777;
                color: #EEEEEE;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
        """)
    
        result = msg.exec_()
        return result == QMessageBox.Yes
    
    def load_combobox(self, combobox: QComboBox, query: str):
        try:
            combobox.clear()
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute(query)
                results = cursor.fetchall()
                for result in results:
                    combobox.addItem(str(result[0]))
        except sqlite3.Error as ex:
                    print(Color.RED + f"An error occurred while loading combobox: {ex}" + Color.RED)
        except Exception as ex:
                print(Color.RED + f"An unexpected error occurred: {ex}" + Color.RED)
                
    def display_info(self, label, info):
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setText(info)