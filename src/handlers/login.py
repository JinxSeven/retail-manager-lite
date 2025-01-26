class LoginHandler:
    def __init__(self, ui):
        self.ui = ui
        self.ui.loginBtn.clicked.connect(self.login)

    def login(self):
        usr_pwd = self.ui.loginInp.text()
        if usr_pwd == "Login@123":
            self.ui.loginInfoLbl.clear()
            self.ui.loginInp.clear()
            # for i in range(1, 5):
            #     self.ui.tabWidget.setTabEnabled(i, True)
            self.ui.tabWidget.setTabEnabled(3, True)
            self.ui.tabWidget.setCurrentIndex(3)
        else:
            self.ui.loginInfoLbl.setText("Incorrect Password")

    def logout(self):
        self.ui.tabWidget.setCurrentIndex(0)
        for i in range(1, 5):
            self.ui.tabWidget.setTabEnabled(i, False)
