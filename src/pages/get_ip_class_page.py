from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from utils import ClassMask, getIPClass


class GetIpClassPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Classe IP")
        title.setObjectName("mainTitle")

        hint = QLabel("Détermine la classe de l'adresse IPv4")
        hint.setObjectName("fieldLabel")

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ex: 10.0.0.1")
        self.ip_input.setFixedHeight(40)

        run_button = QPushButton("Obtenir la classe")
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
        ip_class = getIPClass(ip)

        if ip_class == ClassMask.ERROR:
            self.result.setText("Adresse IP invalide")
            self.result.setStyleSheet("color: #FF5252;")
            return

        class_name = ip_class.name.replace("CLASS_", "Classe ")
        self.result.setText(f"{class_name}")
        self.result.setStyleSheet("color: #4CAF50;")
