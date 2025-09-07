from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QPushButton, QLabel, QHeaderView, QTableWidget, QGroupBox, QColumnView
from PyQt5.QtGui import QIcon, QPainter

from src.utils.color import Color
from src.utils.services import Services
from src.utils.view_order_modal import ViewOrderModal

ROW_SIZE = 33.333
COLUMN_VIEW_DIFF = 235
MODAL_SIZE_DIFF = 370
LABEL_DIFF = 127

class SaveOrderButton(QPushButton):
    def __init__(self, ord_data, dsp_label: QLabel, parent=None):
        icon = QIcon('assets/images/download.svg')
        
        super().__init__(icon, "", parent)
        self.setObjectName(f"{ord_data[0]}")
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {   
                background-color: #009688;
                font: 63 8pt "Poppins SemiBold";
                color: white;
                outline: 0;
                padding: 10px 20px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                cursor: pointer;
                background-color: #00897b;
            }
        """)
        
        self.clicked.connect(partial(self.__on_clicked, ord_data, dsp_label))
        
    def __on_clicked(self, ord_data, dsp_label):
        Services.display_info(dsp_label, "Saving order, please wait...")
        
        try:
            view_ord_modal = ViewOrderModal(ord_data[0])
            view_ord_modal.set_order_info_labels(ord_data)
            view_ord_modal.load_order_table(ord_data, dsp_label)
        except Exception as ex:
            print(Color.RED + f"Error building order modal: {ex}" + Color.RESET)
            return
        
        ord_items_lbl: QLabel = view_ord_modal.ordItemsLbl
        ord_items_dsp: QLabel = view_ord_modal.viewOrdOrdItems
        ord_total_lbl: QLabel = view_ord_modal.ordTotalLbl
        ord_total_dsp: QLabel = view_ord_modal.viewOrdOrdTotal

        ord_table: QTableWidget = view_ord_modal.viewOrdOrdTbl
        table_grp_box: QGroupBox = view_ord_modal.groupBox_3
        column_view: QColumnView = view_ord_modal.columnView_10
        ord_items = int(ord_items_dsp.text())
        
        ord_table.setColumnWidth(0, 450)
        ord_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ord_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if ord_items > 6:
            table_height = int(ord_items * ROW_SIZE)
            ord_table.setFixedHeight(table_height)
            table_grp_box.setFixedHeight(table_height)
            column_view.setFixedHeight(table_height + COLUMN_VIEW_DIFF)
            view_ord_modal.resize(view_ord_modal.width(), (table_height + MODAL_SIZE_DIFF))

            ord_items_lbl.setGeometry(
                ord_items_lbl.x(),
                (view_ord_modal.height() - LABEL_DIFF),
                ord_items_lbl.width(),
                ord_items_lbl.height()
            )

            ord_items_dsp.setGeometry(
                ord_items_dsp.x(),
                (view_ord_modal.height() - (LABEL_DIFF + 1)),
                ord_items_dsp.width(),
                ord_items_dsp.height()
            )

            ord_total_lbl.setGeometry(
                ord_total_lbl.x(),
                (view_ord_modal.height() - LABEL_DIFF),
                ord_total_lbl.width(),
                ord_total_lbl.height()
            )

            ord_total_dsp.setGeometry(
                ord_total_dsp.x(),
                (view_ord_modal.height() - (LABEL_DIFF + 1)),
                ord_total_dsp.width(),
                ord_total_dsp.height()
            )

        # view_ord_modal.exec_()

        # QPrinter configuration for PDF
        try:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFileName(f"INV-{ord_data[0]}.pdf")
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOrientation(QPrinter.Portrait)
            printer.setPageSize(QPrinter.PageSize.A4)
    
            # Render modal to PDF
            painter = QPainter(printer)
            page_rect = printer.pageRect()
            x_scale = page_rect.width() / view_ord_modal.width()
            y_scale = page_rect.height() / view_ord_modal.height()
            scale = min(x_scale, y_scale)
    
            painter.translate(page_rect.x(), page_rect.y())
            painter.scale(scale, scale)
            view_ord_modal.render(painter)
            painter.end()
        except Exception as ex:
            print(Color.RED + f"Error saving order: {ex}" + Color.RED)
            Services.display_info(dsp_label, f"Error saving order!", "red")
            return
        
        Services.display_info(dsp_label, f"Order saved successfully!", "green")
    