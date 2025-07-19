class Initializer:    
    def __init__(self, ui):
        self.ui = ui

        self.oe_btn_lst = [
            self.ui.navOrderEntryOne,
            self.ui.navOrderEntryTwo,
            self.ui.navOrderEntryThree,
            self.ui.navOrderEntryFour
        ]
        for oe_btn in self.oe_btn_lst:
            oe_btn.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))
        
        self.ui.tabWidget.setCurrentIndex(0)
        self.disable_tabs()
        
    def disable_tabs(self):
        for i in range(1, 5):
            self.ui.tabWidget.setTabEnabled(i, False)
    
    def enable_tabs(self):
        for i in range(1, 5):
            self.ui.tabWidget.setTabEnabled(i, True)