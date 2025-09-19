import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType
from config import DB_PATH
from database import initialize_db
from handlers.login import LoginHandler
from handlers.orders import OrderHandler
from handlers.products import ProductHandler
from handlers.initializer import Initializer
from handlers.manage_orders import ManageOrdersHandler

if hasattr(sys, '_MEIPASS'):
    ui_path = os.path.join(sys._MEIPASS, 'assets', 'ui', 'rma.ui')
else:
    ui_path = os.path.join('assets', 'ui', 'rma.ui')

ui, _ = loadUiType(ui_path)

class MainApp(QMainWindow, ui):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        initialize_db()

        self.initializer_handler = Initializer(self)
        self.login_handler = LoginHandler(self)
        self.product_handler = ProductHandler(self)
        self.order_handler = OrderHandler(self)
        self.manage_orders_handler = ManageOrdersHandler(self)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
