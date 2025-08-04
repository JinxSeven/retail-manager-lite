import datetime
import sqlite3

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QTableWidgetItem

from src.config import DB_PATH
from src.utils.services import Services
from PyQt5.QtCore import QSignalBlocker

class ManageOrdersHandler:
    def __init__(self, ui):
        self.ui = ui
        
        # Setting default end date to today
        today_date = datetime.date.today()
        today_q_date = QDate(today_date.year,today_date.month,today_date.day)
        self.ui.ordDateFltrEnd.setDate(today_q_date)

        self.ui.ordDateFltrStart.dateChanged.connect(self.invalid_date_range_check)
        self.ui.ordDateFltrEnd.dateChanged.connect(self.invalid_date_range_check)
        
        self.ui.beginSearchBtn.clicked.connect(self.begin_search)

        self.ui.manageOrdTbl.setColumnWidth(0, 145)
        self.ui.manageOrdTbl.setColumnWidth(1, 145)
        self.ui.manageOrdTbl.setColumnWidth(2, 145)
        self.ui.manageOrdTbl.setColumnWidth(3, 115)
        self.ui.manageOrdTbl.setColumnWidth(4, 63)
        self.ui.manageOrdTbl.setColumnWidth(5, 63)
        self.ui.manageOrdTbl.setColumnWidth(6, 63)
        
        self.fill_order_table()
        
    def fill_order_table(self):
        with sqlite3.connect(DB_PATH, timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders")
            results = cursor.fetchall()
            
            if results:
                for row_index, row_data in enumerate(results):
                    self.ui.manageOrdTbl.insertRow(row_index)
                    for colm_index, colm_data in enumerate(row_data):
                        self.ui.manageOrdTbl.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
            
    #  Method to check invalid date ranges
    def invalid_date_range_check(self):
        start_date = self.ui.ordDateFltrStart.date()
        end_date = self.ui.ordDateFltrEnd.date()

        if end_date < start_date:
            with QSignalBlocker(self.ui.ordDateFltrEnd):
                Services.display_info(self.ui.manOrdInfoLbl, "End date cannot be before start date", "red")
                self.ui.ordDateFltrEnd.setDate(start_date)

        elif start_date > end_date:
            with QSignalBlocker(self.ui.ordDateFltrStart):
                Services.display_info(self.ui.manOrdInfoLbl, "Start date cannot be after end date", "red")
                self.ui.ordDateFltrStart.setDate(end_date)
            
    def begin_search(self):
        self.ui.searchByOrd.isChecked()