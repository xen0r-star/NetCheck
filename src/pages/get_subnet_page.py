from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from utils import ClassMask, getSubnet, isIp


class GetSubnetPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Calcul Sous-Réseau")
        title.setObjectName("mainTitle")

        hint = QLabel("Calcule l'adresse réseau à partir de l'IP et du masque")
        hint.setObjectName("fieldLabel")

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ex: 192.168.12.1")
        self.ip_input.setFixedHeight(40)

        self.mask_input = QLineEdit()
        self.mask_input.setPlaceholderText("Ex: 255.255.255.0")
        self.mask_input.setFixedHeight(40)

        run_button = QPushButton("Calculer")
        run_button.setObjectName("actionButton")
        run_button.setCursor(Qt.PointingHandCursor)
        run_button.clicked.connect(self.run_check)

        self.result = QLabel("Résultat en attente")
        self.result.setObjectName("statusMessage")
        self.result.setAlignment(Qt.AlignLeft)

        layout.addWidget(title)
        layout.addWidget(hint)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.mask_input)
        layout.addWidget(run_button)
        layout.addWidget(self.result)
        layout.addStretch(1)

    def run_check(self):
        ip = self.ip_input.text().strip()
        mask = self.mask_input.text().strip()

        if not isIp(mask):
            self.result.setText("Masque invalide")
            self.result.setStyleSheet("color: #FF5252;")
            return

        subnet = getSubnet(ip, mask)
        if subnet == ClassMask.ERROR.value:
            self.result.setText("Adresse IP invalide")
            self.result.setStyleSheet("color: #FF5252;")
            return

        self.result.setText(f"Sous-réseau: {subnet}")
        self.result.setStyleSheet("color: #4CAF50;")
