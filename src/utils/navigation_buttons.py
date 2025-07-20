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
    
    