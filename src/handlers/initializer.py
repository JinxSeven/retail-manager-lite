from src.utils.navigation_buttons import Navigation 

class Initializer:    
    def __init__(self, ui):
        self.ui = ui

        self.oe_btn_list = Navigation.get_oe_buttons(self)
        self.pm_btn_list = Navigation.get_pm_buttons(self)
        
        self.manage_orders_list = Navigation.get_manage_orders_buttons(self)
        
        for oe_btn in self.oe_btn_list:
            oe_btn.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))
            
        for pm_btn in self.pm_btn_list:
            pm_btn.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))

        for mg_orders_btn in self.manage_orders_list:
            mg_orders_btn.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(3))

        
        self.ui.tabWidget.setCurrentIndex(0)
        self.disable_tabs()
        
    def disable_tabs(self):
        for i in range(1, 4):
            self.ui.tabWidget.setTabEnabled(i, False)
    
    def enable_tabs(self):
        for i in range(1, 4):
            self.ui.tabWidget.setTabEnabled(i, True)