from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget


class UserProfilePage(QWidget):
    logout_requested = Signal()

    def __init__(self):
        super().__init__()

        # --- Structure principale ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # --- Carte profil ---
        card = QFrame()
        card.setObjectName("toolCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 22)
        card_layout.setSpacing(12)

        # --- Informations utilisateur ---
        profile_card = QFrame()
        profile_card.setObjectName("resultCard")
        profile_layout = QVBoxLayout(profile_card)
        profile_layout.setContentsMargins(16, 14, 16, 14)
        profile_layout.setSpacing(8)

        first_name = QLabel("Prenom: Alex")
        first_name.setObjectName("resultIp")

        last_name = QLabel("Nom: Martin")
        last_name.setObjectName("resultIp")

        email = QLabel("Email: alex.martin@nettool.local")
        email.setObjectName("statusMessage")
        email.setStyleSheet("color: #dbe1ff;")

        role_badge = QLabel("ADMIN")
        role_badge.setObjectName("badgeValid")
        role_badge.setFixedWidth(84)
        role_badge.setAlignment(Qt.AlignCenter)

        profile_layout.addWidget(first_name)
        profile_layout.addWidget(last_name)
        profile_layout.addWidget(email)
        profile_layout.addWidget(role_badge, 0, Qt.AlignLeft)

        # --- Action session ---
        logout_button = QPushButton("Deconnexion")
        logout_button.setObjectName("logoutActionButton")
        logout_button.setCursor(Qt.PointingHandCursor)
        logout_button.clicked.connect(self.logout_requested.emit)

        card_layout.addWidget(profile_card)
        card_layout.addSpacing(6)
        card_layout.addWidget(logout_button, 0, Qt.AlignLeft)
        card_layout.addStretch(1)

        layout.addWidget(card)
