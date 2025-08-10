from PyQt5.QtWidgets import QDialog

class ViewOrderModal(QDialog):
    def __init__(self, order_id="xsxhx", parent=None):
        self.setModal(True)

        self.setWindowTitle(order_id.upper())
        self.resize(800, 600)
        