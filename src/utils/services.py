import sqlite3
import time

from PyQt5.QtWidgets import QMessageBox, QComboBox
from src.config import DB_PATH
from .color import Color
from PyQt5 import QtCore

class Services:
    LOAD_ALL_QUERY = """
        SELECT * FROM orders 
        ORDER BY order_date_time DESC
        """
    
    @staticmethod
    def confirmation_messagebox(title: str, message: str) -> bool:
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
    
    # Used to load combobox with details (Inputs: QComboBox, SqlQuery) 
    @staticmethod
    def load_combobox(combobox: QComboBox, query: str):
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

    @staticmethod
    def display_info(label, info, color = 'blue'):
        label.setText(info)
        existing_style = label.styleSheet()
        label.setStyleSheet(existing_style + f"color: {color};")
        QtCore.QTimer.singleShot(3000, label.clear)
