import datetime
import sqlite3

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import QSignalBlocker

from src.config import DB_PATH
from src.utils.color import Color
from src.utils.delete_order_button import DeleteOrderButton
from src.utils.save_order_button import SaveOrderButton
from src.utils.services import Services

from src.utils.view_order_button import ViewOrderButton

GET_ALL_ORDERS = """
        SELECT * FROM orders 
        ORDER BY order_date_time DESC
        """

BTN_INDEX = {
    "START": 4,
    "VIEW": 4,
    "SAVE": 5,
    "DELETE": 6,
    "END": 7    
}

class ManageOrdersHandler:
    def __init__(self, ui):
        self.ui = ui
        self.min_q_date = self.ui.ordDateFltrStart.minimumDate()
        
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
        
        self.ui.beginSearchBtn.clicked.connect(self.filter_and_search)
        self.ui.resetSearchBtn.clicked.connect(self.reset_filters)
        
        self.ui.tabWidget.currentChanged.connect(
            lambda index: self.reset_filters() if index == 3 else None
        )

        self.ui.manageOrdTbl.setColumnWidth(0, 127)
        self.ui.manageOrdTbl.setColumnWidth(1, 175)
        self.ui.manageOrdTbl.setColumnWidth(2, 127)
        self.ui.manageOrdTbl.setColumnWidth(3, 115)
        self.ui.manageOrdTbl.setColumnWidth(4, 63)
        self.ui.manageOrdTbl.setColumnWidth(5, 63)
        self.ui.manageOrdTbl.setColumnWidth(6, 63)
        
        self.load_order_table()
    
    def reset_filters(self):
        self.ui.ordDateFltrStart.setDate(self.min_q_date)
        self.ui.ordDateFltrEnd.setDate(self.today_q_date)
        self.ui.searchQryInput.clear()
        self.filter_and_search()
    
    def load_order_table(self, query=GET_ALL_ORDERS, params=None):
        try:
            with sqlite3.connect(DB_PATH, timeout=10) as conn:
                cursor = conn.cursor()
                if params is None: 
                    cursor.execute(query)
                else: 
                    cursor.execute(query, params)
                results = cursor.fetchall()

                if results:
                    for row_index, row_data in enumerate(results):
                        self.ui.manageOrdTbl.insertRow(row_index)
                        for colm_index, colm_data in enumerate(row_data):
                            self.ui.manageOrdTbl.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
                        
                        for colm_index in range(BTN_INDEX["START"], BTN_INDEX["END"]):
                            if colm_index is BTN_INDEX["VIEW"]:
                                self.ui.manageOrdTbl.setCellWidget(row_index, colm_index, ViewOrderButton(str(row_data[0])))
                            if colm_index is BTN_INDEX["SAVE"]:
                                self.ui.manageOrdTbl.setCellWidget(row_index, colm_index, SaveOrderButton(str(row_data[0])))
                            if colm_index is BTN_INDEX["DELETE"]:
                                self.ui.manageOrdTbl.setCellWidget(row_index, colm_index, DeleteOrderButton(str(row_data[0]),
                                                                                                            self.filter_and_search,
                                                                                                            self.ui.manOrdInfoLbl))
                else:
                    Services.display_info(self.ui.manOrdInfoLbl, "No records found!")
                    
        except sqlite3.Error as ex:
            print(Color.RED + f"An SQLite error occurred: {ex}" + Color.RESET)
        except Exception as ex: 
            print(Color.RED + f"An unexpected error occurred: {ex}" + Color.RESET)
            
    #  Method to check invalid date ranges
    def invalid_date_range_check(self, sender):
        start_date = self.ui.ordDateFltrStart.date()
        end_date = self.ui.ordDateFltrEnd.date()

        if start_date > end_date:
            if sender == self.ui.ordDateFltrStart:
                with QSignalBlocker(self.ui.ordDateFltrStart):
                    self.ui.ordDateFltrStart.setDate(end_date)
                Services.display_info(self.ui.manOrdInfoLbl, "Start date cannot be after end date", "red")

            elif sender == self.ui.ordDateFltrEnd:
                with QSignalBlocker(self.ui.ordDateFltrEnd):
                    self.ui.ordDateFltrEnd.setDate(start_date)
                Services.display_info(self.ui.manOrdInfoLbl, "End date cannot be before start date", "red")
            
    def filter_and_search(self):
        search_query = self.ui.searchQryInput.text()
        start_date = self.ui.ordDateFltrStart.date()
        end_date = self.ui.ordDateFltrEnd.date()
    
        query = GET_ALL_ORDERS
        params = None
        
        if search_query or search_query.strip() != '':
            if self.ui.searchByOrd.isChecked():
                query = """
                    SELECT * FROM orders 
                    WHERE DATE(order_date_time) BETWEEN ? AND ?
                    AND orders.order_id LIKE ? COLLATE NOCASE
                    ORDER BY order_date_time DESC
                    """
                params = (start_date.toString(Qt.ISODate), end_date.toString(Qt.ISODate), f"%{search_query}%")
            else:
                query = """
                    SELECT * FROM orders 
                    WHERE DATE(order_date_time) BETWEEN ? AND ?
                    AND orders.cx_phone_num LIKE ? COLLATE NOCASE
                    ORDER BY order_date_time DESC
                    """
                params = (start_date.toString(Qt.ISODate), end_date.toString(Qt.ISODate), f"%{search_query}%")
        
        self.ui.manageOrdTbl.setRowCount(0)
        self.load_order_table(query, params)