from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from utils import ClassMask, getIPClassMask


class GetIpClassMaskPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Masque Par Classe")
        title.setObjectName("mainTitle")

        hint = QLabel("Retourne le masque par défaut selon la classe IP")
        hint.setObjectName("fieldLabel")

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ex: 172.16.0.10")
        self.ip_input.setFixedHeight(40)

        run_button = QPushButton("Obtenir le masque")
        run_button.setObjectName("actionButton")
        run_button.setCursor(Qt.PointingHandCursor)
        run_button.clicked.connect(self.run_check)

        self.result = QLabel("Résultat en attente")
        self.result.setObjectName("statusMessage")
        self.result.setAlignment(Qt.AlignLeft)

        layout.addWidget(title)
        layout.addWidget(hint)
        layout.addWidget(self.ip_input)
        layout.addWidget(run_button)
        layout.addWidget(self.result)
        layout.addStretch(1)

    def run_check(self):
        ip = self.ip_input.text().strip()
        mask = getIPClassMask(ip)

        if mask == ClassMask.ERROR.value:
            self.result.setText("Adresse IP invalide")
            self.result.setStyleSheet("color: #FF5252;")
            return

        self.result.setText(f"Masque: {mask}")
        self.result.setStyleSheet("color: #4CAF50;")
