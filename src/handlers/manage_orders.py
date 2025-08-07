import datetime
import sqlite3

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QTableWidgetItem

from src.config import DB_PATH
from src.utils.services import Services
from PyQt5.QtCore import QSignalBlocker

class ManageOrdersHandler:
    def __init__(self, ui):
        self.ui = ui
        
        # Setting default end date to today
        today_date = datetime.date.today()
        self.today_q_date = QDate(today_date.year,today_date.month,today_date.day)
        self.ui.ordDateFltrEnd.setDate(self.today_q_date)

        self.ui.ordDateFltrStart.dateChanged.connect(
            lambda: self.invalid_date_range_check(self.ui.ordDateFltrStart)
        )
        self.ui.ordDateFltrEnd.dateChanged.connect(
            lambda: self.invalid_date_range_check(self.ui.ordDateFltrEnd)
        )
        
        self.ui.beginSearchBtn.clicked.connect(self.begin_search)
        self.ui.resetSearchBtn.clicked.connect(self.load_order_table)
        self.ui.tabWidget.currentChanged.connect(
            lambda index: self.load_order_table() if index == 3 else None
        )

        self.ui.manageOrdTbl.setColumnWidth(0, 145)
        self.ui.manageOrdTbl.setColumnWidth(1, 145)
        self.ui.manageOrdTbl.setColumnWidth(2, 145)
        self.ui.manageOrdTbl.setColumnWidth(3, 115)
        self.ui.manageOrdTbl.setColumnWidth(4, 63)
        self.ui.manageOrdTbl.setColumnWidth(5, 63)
        self.ui.manageOrdTbl.setColumnWidth(6, 63)
        
        self.load_order_table()
        
    def load_order_table(self, query=Services.LOAD_ALL_QUERY, params=None):
        with sqlite3.connect(DB_PATH, timeout=10) as conn:
            cursor = conn.cursor()
            if params is None: cursor.execute(query)
            else: cursor.execute(query, params)
            results = cursor.fetchall()
            
            if results:
                for row_index, row_data in enumerate(results):
                    self.ui.manageOrdTbl.insertRow(row_index)
                    for colm_index, colm_data in enumerate(row_data):
                        self.ui.manageOrdTbl.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
            
    #  Method to check invalid date ranges
    def invalid_date_range_check(self, sender):
        start_date = self.ui.ordDateFltrStart.date()
        end_date = self.ui.ordDateFltrEnd.date()

        if start_date > end_date:
            if sender == self.ui.ordDateFltrStart:
                # User changed the start date to after the end date
                with QSignalBlocker(self.ui.ordDateFltrStart):
                    self.ui.ordDateFltrStart.setDate(end_date)
                Services.display_info(self.ui.manOrdInfoLbl, "Start date cannot be after end date", "red")

            elif sender == self.ui.ordDateFltrEnd:
                # User changed the end date to before the start date
                with QSignalBlocker(self.ui.ordDateFltrEnd):
                    self.ui.ordDateFltrEnd.setDate(start_date)
                Services.display_info(self.ui.manOrdInfoLbl, "End date cannot be before start date", "red")
            
    def begin_search(self):
        search_query = self.ui.searchQryInput.text()
        start_date = self.ui.ordDateFltrStart.date()
        end_date = self.ui.ordDateFltrEnd.date()
        
        if not search_query or search_query.strip() == '':
            if start_date == self.ui.ordDateFltrStart.minimumDate() and end_date == self.today_q_date:
                self.load_order_table()
                return
            else:
                query = """
                SELECT * FROM orders 
                WHERE DATE(order_date_time) BETWEEN ? AND ? 
                ORDER BY order_date_time DESC
                """
                params = (start_date.toString(Qt.ISODate), end_date.toString(Qt.ISODate))
                self.load_order_table(query, params)
                return

        self.ui.searchByOrd.isChecked()
        print(start_date.toString(Qt.ISODate), end_date.toString(Qt.ISODate))