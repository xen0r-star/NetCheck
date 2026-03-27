import sys
import os
from PySide6.QtWidgets import QApplication

from pages.loginPage import LoginWindow



def loadStyleSheet():
    css_path = os.path.join(os.path.dirname(__file__), "./style/style.css")

    try:
        with open(css_path, "r") as f:
            return f.read()
        
    except FileNotFoundError:
        print(f"Erreur : Le fichier {css_path} est introuvable.")
        return ""
    


app = QApplication(sys.argv)
app.setStyleSheet(loadStyleSheet())


window = LoginWindow()
window.show()
sys.exit(app.exec())
