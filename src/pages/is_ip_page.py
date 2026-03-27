from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from utils import isIp


class IsIpPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Validation IP")
        title.setObjectName("mainTitle")

        hint = QLabel("Vérifie si une adresse IPv4 est valide")
        hint.setObjectName("fieldLabel")

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ex: 192.168.1.10")
        self.ip_input.setFixedHeight(40)

        run_button = QPushButton("Vérifier")
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
        valid = isIp(ip)
        if valid:
            self.result.setText("Adresse IP valide")
            self.result.setStyleSheet("color: #4CAF50;")
        else:
            self.result.setText("Adresse IP invalide")
            self.result.setStyleSheet("color: #FF5252;")
