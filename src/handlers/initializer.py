class Initializer:
    def __init__(self, ui):
        self.ui = ui
        self.ui.tabWidget.setCurrentIndex(0)
        self.disable_tabs()
        
    def disable_tabs(self):
        for i in range(1, 5):
            self.ui.tabWidget.setTabEnabled(i, False)
    def enable_tabs(self):
        for i in range(1, 5):
            self.ui.tabWidget.setTabEnabled(i, True)