import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)
from PySide6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connexion")
        self.resize(350, 250)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Titre
        title = QLabel("Connexion")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        # Champ utilisateur
        self.username = QLineEdit()
        self.username.setPlaceholderText("Email ou utilisateur")

        # Champ mot de passe
        self.password = QLineEdit()
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.Password)

        # Message
        self.message = QLabel("")
        self.message.setAlignment(Qt.AlignCenter)

        # Bouton
        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self.login)


        # Ajouter les widgets au layout
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)
        layout.addWidget(self.message)

        self.setLayout(layout)

    def login(self):
        user = self.username.text()
        pwd = self.password.text()

        if user == "admin" and pwd == "1234":
            self.message.setStyleSheet("color: green;")
            self.message.setText("Connexion réussie !")
        else:
            self.message.setStyleSheet("color: red;")
            self.message.setText("Identifiants incorrects")



app = QApplication(sys.argv)

# Charger le CSS externe
with open("style.css", "r") as f:
    app.setStyleSheet(f.read())

window = LoginWindow()
window.show()

app.exec()