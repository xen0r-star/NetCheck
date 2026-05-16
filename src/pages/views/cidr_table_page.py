import csv

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFileDialog, QFrame, QHeaderView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from ...services.logic import genererTableauCIDR



class CidrTablePage(QWidget):
    def __init__(self):
        super().__init__()

        # --- Structure principale ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # --- Carte de contenu ---
        card = QFrame()
        card.setObjectName("toolCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 22)
        card_layout.setSpacing(14)

        export_button = QPushButton("Exporter le tableau")
        export_button.setObjectName("actionButton")
        export_button.setFixedSize(190, 44)
        export_button.setCursor(Qt.PointingHandCursor)
        export_button.clicked.connect(self.export_table)

        # --- Tableau CIDR ---
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["CIDR", "Binaire", "Décimal"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setObjectName("cidrTable")
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.copy_cell_value)

        card_layout.addWidget(export_button, 0, Qt.AlignLeft)
        card_layout.addWidget(self.table)

        layout.addWidget(card)

        self._load_table_data()


    def _load_table_data(self):
        rows = genererTableauCIDR()
        self.table.setRowCount(len(rows))

        for row_idx, row_values in enumerate(rows):
            for col_idx, cell_value in enumerate(row_values):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(cell_value))


    def copy_cell_value(self, row, column):
        item = self.table.item(row, column)
        if not item:
            return

        QApplication.clipboard().setText(item.text())


    def export_table(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter le tableau",
            "cidr_table.csv",
            "CSV (*.csv)"
        )

        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["CIDR", "Binaire", "Décimal"])

            for row in range(self.table.rowCount()):
                writer.writerow([
                    self.table.item(row, 0).text(),
                    self.table.item(row, 1).text(),
                    self.table.item(row, 2).text(),
                ])
