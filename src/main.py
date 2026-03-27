import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from dashboard import DashboardWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.dashboard_window = None

        self.setWindowTitle("NetTool Admin")
        self.setFixedSize(900, 500)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)



        # --- SECTION GAUCHE ---
        self.left_frame = QFrame()
        self.left_frame.setObjectName("leftFrame")
        left_layout = QVBoxLayout(self.left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.illustration = QLabel()
        self.illustration.setAlignment(Qt.AlignCenter)

        image_path = os.path.join(os.path.dirname(__file__), "digital-technology.jpeg")
        pix = QPixmap(image_path)
        self.illustration.setPixmap(pix.scaled(500, 500, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        
        left_layout.addWidget(self.illustration)
        main_layout.addWidget(self.left_frame, 1)



        # --- SECTION DROITE (Formulaire) ---
        self.right_frame = QFrame()
        self.right_frame.setObjectName("rightFrame")
        right_layout = QVBoxLayout(self.right_frame)
        right_layout.setContentsMargins(50, 40, 50, 40)

        # Titre
        title = QLabel("Connexion Utilisateur")
        title.setObjectName("mainTitle")
        title.setAlignment(Qt.AlignCenter)

        # Champs de saisie
        user_label = QLabel("Nom d'utilisateur")
        user_label.setObjectName("fieldLabel")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Nom")
        self.username.setFixedSize(300, 40)

        pass_label = QLabel("Mot de passe")
        pass_label.setObjectName("fieldLabel")
        self.password = QLineEdit()
        self.password.setPlaceholderText("••••••••")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedSize(300, 40)

        # Bouton Connexion
        login_button = QPushButton("Se connecter")
        login_button.setObjectName("loginButton")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.clicked.connect(self.login)

        # Message d'erreur/succès
        self.message = QLabel("")
        self.message.setObjectName("statusMessage")
        self.message.setAlignment(Qt.AlignCenter)


        # Organisation du layout droit
        right_layout.addWidget(title)
        right_layout.addSpacing(30)
        right_layout.addWidget(user_label)
        right_layout.addWidget(self.username)
        right_layout.addSpacing(15)
        right_layout.addWidget(pass_label)
        right_layout.addWidget(self.password)
        right_layout.addSpacing(30)
        right_layout.addWidget(login_button)
        right_layout.addWidget(self.message)
        right_layout.addSpacing(70)


        main_layout.addWidget(self.right_frame, 1)


    def login(self):
        if self.username.text() == "admin" and self.password.text() == "1234":
            self.message.setText("Connexion réussie !")
            self.message.setStyleSheet("color: #4CAF50;")
            self.dashboard_window = DashboardWindow()
            self.dashboard_window.logout_requested.connect(self.on_logout)
            self.dashboard_window.show()
            self.hide()
        else:
            self.message.setText("Identifiants incorrects")
            self.message.setStyleSheet("color: #FF5252;")

    def on_logout(self):
        self.password.clear()
        self.message.setText("Deconnecte")
        self.message.setStyleSheet("color: #a0aec0;")
        self.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Calculer le chemin absolu vers le fichier style.css
    basedir = os.path.dirname(__file__)
    css_path = os.path.join(basedir, "style.css")

    try:
        with open(css_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Erreur : Le fichier {css_path} est introuvable.")
    
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())