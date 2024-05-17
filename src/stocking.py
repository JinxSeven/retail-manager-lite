import os
import sys
import sqlite3
from datetime import date
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

ui, _ = loadUiType('assets/ui/stocking.ui')
db_path = os.path.join('database/', 'stocking.db')

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.login_button.clicked.connect(self.login)
        
        self.logout_1.clicked.connect(self.logout)
        self.logout_2.clicked.connect(self.logout)
        self.logout_3.clicked.connect(self.logout)
        
        self.order_entry_1.clicked.connect(self.showOrderEntry)
        self.order_entry_2.clicked.connect(self.showOrderEntry)
        self.order_entry_3.clicked.connect(self.showOrderEntry)
        
        self.edit_orders_1.clicked.connect(self.showEditOrders)
        self.edit_orders_2.clicked.connect(self.showEditOrders)
        self.edit_orders_3.clicked.connect(self.showEditOrders)
        
        self.orders_1.clicked.connect(self.showOrders)
        self.orders_2.clicked.connect(self.showOrders)
        self.orders_3.clicked.connect(self.showOrders)

        self.oe_button_1.clicked.connect(self.orderPlus)
        self.oe_button_2.clicked.connect(self.orderNext)

        self.select_oid.currentIndexChanged.connect(self.detailsLoad)

        self.eo_button_1.clicked.connect(self.updateOrderDetails)
        self.eo_button_2.clicked.connect(self.deleteOrderDetails)
        
        try:
            db_chk = sqlite3.connect(db_path)
            db_chk.execute("CREATE TABLE IF NOT EXISTS order_data(order_id INTEGER, cx_name TEXT, cx_phno TEXT, product_id INTEGRER, quantity INTEGER, order_date TEXT)")
            db_chk.commit()
            print(Color.GREEN + "Created database sucessfully" + Color.RESET)
        except:
            print(db_chk.Error)
        
        self.genOrderId()
        self.oidLoad()

    def login(self):
        usr_pwd = self.login_input.text()
        if usr_pwd == "sagayam":
            self.login_info.setText("")
            self.login_input.setText("")
            self.tabWidget.setCurrentIndex(1)
        else:
            self.login_info.setText("Wrong Password!")
        
    def logout(self):
        self.tabWidget.setCurrentIndex(0)
        
    def showOrderEntry(self):
        self.tabWidget.setCurrentIndex(1)
        
    def showEditOrders(self):
        self.tabWidget.setCurrentIndex(2)
        
    def showOrders(self):
        self.tabWidget.setCurrentIndex(3)

    def genOrderId(self):
        order_gen = 0
        try:
            oid_db = sqlite3.connect(db_path)
            cursor = oid_db.execute("SELECT MAX(order_id) FROM order_data")
            result = cursor.fetchall()
            if result:
                for maxid in result:
                    order_gen = maxid[0] + 1
                self.order_id.setText(str(order_gen))
        except:
            order_gen = 1001
            self.order_id.setText(str(order_gen))

    def orderNext(self):
        self.genOrderId()
        try:
            oe_db = sqlite3.connect(db_path)
            # order_id INTEGER, cx_name TEXT, cx_phno TEXT, product_id INTEGRER, quantity INTEGER, order_date TEXT, order_time TEXT
            oe_db.execute("INSERT INTO order_data VALUES ("+ self.order_id.text() +", '"+ self.oe_input_1.text() +"', '"+ self.oe_input_3.text() +"', "+ self.oe_input_2.text() +", "+ self.oe_input_4.text() +", '"+ str(date.today()) +"')")
            oe_db.commit()
        except:
            print(Color.RED + "Can't insert values into table" + Color.RESET)
        
        self.order_id.setText("")
        self.oe_input_1.setText("")
        self.oe_input_2.setText("")
        self.oe_input_3.setText("")
        self.oe_input_4.setText("")
        self.genOrderId()
        self.oidLoad()

    def orderPlus(self):
        self.genOrderId()
        try:
            oe_db = sqlite3.connect(db_path)
            # order_id INTEGER, cx_name TEXT, cx_phno TEXT, product_id INTEGRER, quantity INTEGER, order_date TEXT, order_time TEXT
            oe_db.execute("INSERT INTO order_data VALUES ("+ self.order_id.text() +", '"+ self.oe_input_1.text() +"', '"+ self.oe_input_3.text() +"', "+ self.oe_input_2.text() +", "+ self.oe_input_4.text() +", '"+ str(date.today()) +"')")
            oe_db.commit()
        except:
            print(Color.RED + "Can't insert values into table" + Color.RESET)
        
        self.oe_input_2.setText("")
        self.oe_input_4.setText("")
        self.genOrderId()
        self.oidLoad()

    def oidLoad(self):
        try:
            self.select_oid.clear()
            oid_db = sqlite3.connect(db_path)
            cursor = oid_db.execute("SELECT order_id FROM order_data")
            result = cursor.fetchall()
            if result:
                for ids in result:
                    self.select_oid.addItem(str(ids[0]))
        except:
            print(Color.RED + "Can't load values into combo box" + Color.RESET)
            
    def detailsLoad(self):
        try:
            load_db = sqlite3.connect(db_path)
            current_oid = str(self.select_oid.currentText())
            cursor = load_db.execute("SELECT * FROM order_data WHERE order_id = "+ current_oid +"")
            result = cursor.fetchall()
            if result:
                for details in result:
                    self.eo_input_1.setText(details[1])
                    self.eo_input_3.setText(details[2])
                    self.eo_input_2.setText(str(details[3]))
                    self.eo_input_4.setText(str(details[4]))
            self.eo_display.setText("")
        except:
            print(Color.RED + "Can't load details into text boxes" + Color.RESET)

    def updateOrderDetails(self):
        try:
            updt_db = sqlite3.connect(db_path)
            current_oid = str(self.select_oid.currentText())
            # order_id INTEGER, cx_name TEXT, cx_phno TEXT, product_id INTEGRER, quantity INTEGER, order_date TEXT, order_time TEXT
            updt_db.execute("UPDATE order_data SET cx_name = '"+ self.eo_input_1.text() +"', cx_phno = '"+ self.eo_input_3.text() +"', product_id = "+ self.eo_input_2.text() +", quantity = "+ self.eo_input_4.text() +" WHERE order_id = "+ current_oid +"")
            updt_db.commit()
            self.eo_display.setText("Order updated Successfully.")
        except:
            print(Color.RED + "Can't update values into table" + Color.RESET)

    def deleteOrderDetails(self):
        try:
            dlt_db = sqlite3.connect(db_path)
            current_oid = str(self.select_oid.currentText())
            dlt_db.execute("DELETE FROM order_data WHERE order_id = "+ current_oid +"")
            dlt_db.commit()
            self.eo_display_2.setText("Order Deleted Successfully.")
            self.oidLoad()
            self.genOrderId()
        except:
            print(Color.RED + "Can't delete values from table" + Color.RESET)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()


            # oid_count = oid_db.execute("SELECT COUNT(order_id) FROM order_data")
            # if oid_count == 0:
            #     self.eo_input_1.setText("")
            #     self.eo_input_3.setText("")
            #     self.eo_input_2.setText("")
            #     self.eo_input_4.setText("")