from PySide6.QtWidgets import (
    QFrame,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from utils import genererTableauCIDR


class CidrTablePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("toolCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 22)
        card_layout.setSpacing(14)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["CIDR", "Binaire", "Décimal"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setObjectName("cidrTable")
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        card_layout.addWidget(self.table)

        layout.addWidget(card)




        rows = genererTableauCIDR()
        self.table.setRowCount(len(rows))

        for row_idx, row_values in enumerate(rows):
            for col_idx, cell_value in enumerate(row_values):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(cell_value))
