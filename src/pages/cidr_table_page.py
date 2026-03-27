from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from utils import genererTableauCIDR


class CidrTablePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Table CIDR")
        title.setObjectName("mainTitle")

        hint = QLabel("Affiche les correspondances CIDR, binaire et décimal")
        hint.setObjectName("fieldLabel")

        run_button = QPushButton("Charger la table")
        run_button.setObjectName("actionButton")
        run_button.setCursor(Qt.PointingHandCursor)
        run_button.clicked.connect(self.load_table)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["CIDR", "Binaire", "Décimal"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(title)
        layout.addWidget(hint)
        layout.addWidget(run_button)
        layout.addWidget(self.table)

    def load_table(self):
        rows = genererTableauCIDR()
        self.table.setRowCount(len(rows))

        for row_idx, row_values in enumerate(rows):
            for col_idx, cell_value in enumerate(row_values):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(cell_value))
