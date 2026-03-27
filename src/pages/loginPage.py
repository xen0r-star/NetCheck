import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame

from .dashboardPage import DashboardWindow
from services.login import validate_credentials



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

		base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
		image_path = os.path.join(base_dir, "assets", "images", "digital-technology.jpeg")
		pix = QPixmap(image_path)
		if not pix.isNull():
			self.illustration.setPixmap(pix.scaled(500, 500, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

		left_layout.addWidget(self.illustration)
		main_layout.addWidget(self.left_frame, 1)

		# --- SECTION DROITE (Formulaire) ---
		self.right_frame = QFrame()
		self.right_frame.setObjectName("rightFrame")
		right_layout = QVBoxLayout(self.right_frame)
		right_layout.setContentsMargins(50, 40, 50, 40)

		title = QLabel("Connexion Utilisateur")
		title.setObjectName("mainTitle")
		title.setAlignment(Qt.AlignCenter)

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

		login_button = QPushButton("Se connecter")
		login_button.setObjectName("loginButton")
		login_button.setCursor(Qt.PointingHandCursor)
		login_button.clicked.connect(self.login)

		self.message = QLabel("")
		self.message.setObjectName("statusMessage")
		self.message.setAlignment(Qt.AlignCenter)

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
		if validate_credentials(self.username.text(), self.password.text()):
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
		self.show()
