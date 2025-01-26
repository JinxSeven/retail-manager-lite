import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType
from config import DB_PATH
from database import initialize_db
from handlers.login import LoginHandler
from handlers.orders import OrderHandler
from handlers.products import ProductHandler
from handlers.initializer import Initializer

ui, _ = loadUiType('assets/uiux/sms.ui')
popup, _ = loadUiType('assets/uiux/popup.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        initialize_db()

        self.login_handler = LoginHandler(self)
        # self.order_handler = OrderHandler(self)
        self.product_handler = ProductHandler(self)
        self.initializer_handler = Initializer(self)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
