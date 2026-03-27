from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from utils import isClassFull


class IsClassFullPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Masque Classful")
        title.setObjectName("mainTitle")

        hint = QLabel("Vérifie si un masque contient uniquement des 255 et des 0")
        hint.setObjectName("fieldLabel")

        self.mask_input = QLineEdit()
        self.mask_input.setPlaceholderText("Ex: 255.255.255.0")
        self.mask_input.setFixedHeight(40)

        run_button = QPushButton("Analyser")
        run_button.setObjectName("actionButton")
        run_button.setCursor(Qt.PointingHandCursor)
        run_button.clicked.connect(self.run_check)

        self.result = QLabel("Résultat en attente")
        self.result.setObjectName("statusMessage")
        self.result.setAlignment(Qt.AlignLeft)

        layout.addWidget(title)
        layout.addWidget(hint)
        layout.addWidget(self.mask_input)
        layout.addWidget(run_button)
        layout.addWidget(self.result)
        layout.addStretch(1)

    def run_check(self):
        mask = self.mask_input.text().strip()
        result = isClassFull(mask)

        if result == "error":
            self.result.setText("Masque invalide")
            self.result.setStyleSheet("color: #FF5252;")
        elif result:
            self.result.setText("Masque classful valide")
            self.result.setStyleSheet("color: #4CAF50;")
        else:
            self.result.setText("Masque valide mais non classful")
            self.result.setStyleSheet("color: #f59e0b;")
