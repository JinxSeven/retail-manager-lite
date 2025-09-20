from src.handlers.initializer import Initializer
from src.utils.services import Services
from src.utils.navigation_buttons import Navigation

class LoginHandler:
    def __init__(self, ui):
        self.ui = ui
        self.services = Services()
        self.initializer = Initializer(self.ui)
        self.logout_btn_list = Navigation.get_logout_buttons(self)
        
        self.initializer.disable_tabs()
        self.ui.loginInp.returnPressed.connect(self.login)
        self.ui.loginBtn.clicked.connect(self.login)

        for lout_btn in self.logout_btn_list:
            lout_btn.clicked.connect(self.logout)

    def login(self):
        usr_pwd = self.ui.loginInp.text()
        if usr_pwd == "Login@123":
            self.initializer.enable_tabs()
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.tabWidget.setTabEnabled(0, False)
            self.ui.loginInp.clear()
        else:
            self.services.display_info(self.ui.loginInfoLbl, 'Incorrect Password', "red")

    def logout(self):
        # self.ui.loginInfoLbl.clear()
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget.setTabEnabled(0, True)
        self.initializer.disable_tabs()

    