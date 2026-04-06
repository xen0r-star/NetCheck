import sys
import os
from PySide6.QtWidgets import QApplication

from pages.loginPage import LoginWindow



def loadStyleSheet():
    cssFile = [
        "badges.css", "buttons.css", 
        "content.css", "dashboard.css", 
        "global.css", "login.css", 
        "results.css", "sidebar.css", 
        "table.css", "tools.css"
    ]
    full_stylesheet = ""

    for css in cssFile:
        css_path = os.path.join(os.path.dirname(__file__), "style", css)

        try:
            with open(css_path, "r") as f:
                full_stylesheet += f.read() + "\n"
            
        except FileNotFoundError:
            print(f"Erreur : Le fichier {css_path} est introuvable.")
        
    return full_stylesheet
    


app = QApplication(sys.argv)
app.setStyleSheet(loadStyleSheet())


window = LoginWindow()
window.show()
sys.exit(app.exec())
