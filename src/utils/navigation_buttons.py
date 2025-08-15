class Navigation:
    # Order Entry buttons
    @staticmethod
    def get_oe_buttons(self):
        return [
            self.ui.navOrderEntryOne,
            self.ui.navOrderEntryTwo,
            self.ui.navOrderEntryThree,
            self.ui.navOrderEntryFour
        ]

    # Product Mod buttons
    @staticmethod
    def get_pm_buttons(self):
        return [
            self.ui.navProdModOne,
            self.ui.navProdModTwo,
            self.ui.navProdModThree,
            self.ui.navProdModFour
        ]
    
    # Logout Buttons list
    @staticmethod
    def get_logout_buttons(self):
        return [
            self.ui.navLogout1,
            self.ui.navLogout3,
            self.ui.logout_3,
            self.ui.logout_2
        ]
    
    # manage Orders button list
    @staticmethod
    def get_manage_orders_buttons(self):
        return [
            self.ui.navManOrdOne,
            self.ui.navProdMod3,
            self.ui.add_prod_4,
            self.ui.add_prod_2
        ]
    
    