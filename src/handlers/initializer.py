class Initializer:
    def __init__(self, ui):
        self.ui = ui
        self.ui.tabWidget.setCurrentIndex(0)
        self.disableTabs()
        
    def disableTabs(self):
        for i in range(1, 5):
            self.ui.tabWidget.setTabEnabled(i, False)
    def enableTabs(self):
        for i in range(1, 5):
            self.ui.tabWidget.setTabEnabled(i, True)