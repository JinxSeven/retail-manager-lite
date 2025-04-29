from src.handlers.initializer import Initializer
from src.utils.services import Services

class LoginHandler:
    def __init__(self, ui):
        self.ui = ui
        self.services = Services()
        self.initializer = Initializer(self.ui)
        
        self.initializer.disableTabs()
        self.ui.loginBtn.clicked.connect(self.login)

    def login(self):
        usr_pwd = self.ui.loginInp.text()
        if usr_pwd == "Login@123":
            self.initializer.enableTabs()
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.tabWidget.setTabEnabled(0, False)
        else:
            self.services.display_info(self.ui.loginInfoLbl, 'Incorrect Password')

    def logout(self):
        self.ui.loginInp.clear()
        self.ui.loginInfoLbl.clear()
        self.ui.tabWidget.setCurrentIndex(0)
        self.initializer.disableTabs()
