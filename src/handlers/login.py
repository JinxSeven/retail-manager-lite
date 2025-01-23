from PyQt5.QtWidgets import QMessageBox

class LoginHandler:
    def __init__(self, ui):
        self.ui = ui
        self.ui.login_button.clicked.connect(self.login)

    def login(self):
        usr_pwd = self.ui.login_input.text()
        if usr_pwd == "sagayam":
            self.ui.login_info.setText("")
            self.ui.login_input.setText("")
            for i in range(1, 5):
                self.ui.tabWidget.setTabEnabled(i, True)
            self.ui.tabWidget.setCurrentIndex(1)
        else:
            self.ui.login_info.setText("Wrong Password!")

    def logout(self):
        self.ui.tabWidget.setCurrentIndex(0)
        for i in range(1, 5):
            self.ui.tabWidget.setTabEnabled(i, False)
