import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QToolButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame

from .dashboardPage import DashboardWindow
from ..services.database import Database



class LoginWindow(QWidget):
	def __init__(self):
		super().__init__()

		self.dashboard_window = None

		self.setWindowTitle("NetTool - Connexion")
		self.setFixedSize(900, 500)
		self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint
        )

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
		image_path = os.path.join(base_dir, "assets", "images", "background.jpg")
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

		eye_open_icon = os.path.join(base_dir, "assets", "icons", "eye-open.svg")
		eye_closed_icon = os.path.join(base_dir, "assets", "icons", "eye-closed.svg")
		self.password_visible = False
		self.password_toggle_icons = {
			True: QIcon(eye_open_icon),
			False: QIcon(eye_closed_icon),
		}
		self.password_toggle_action = self.password.addAction(
			self.password_toggle_icons[False],
			QLineEdit.TrailingPosition
		)

		toggle_button = self.password.findChild(QToolButton)
		if toggle_button:
			toggle_button.setCursor(Qt.PointingHandCursor)

		self.password_toggle_action.triggered.connect(self.toggle_password_visibility)

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
		if not self.username.text().strip() or not self.password.text().strip():
			self.message.setText("Champs incomplets")
			self.message.setStyleSheet("color: #FFB74D;")
			return

		db = Database()

		if db.validateCredentials(self.username.text(), self.password.text()):
			user_info = db.getUserInfo()
			self.dashboard_window = DashboardWindow(user_info=user_info)
			self.dashboard_window.logout_requested.connect(self.on_logout)
			self.dashboard_window.show()
			self.hide()
			
		else:
			self.message.setText(db.last_error if db.last_error else "Erreur de connexion")
			self.message.setStyleSheet("color: #FF5252;")


	def on_logout(self):
		self.message.setText("")
		self.password.clear()
		self.password_visible = False
		self.password.setEchoMode(QLineEdit.Password)
		self.password_toggle_action.setIcon(self.password_toggle_icons[False])
		self.show()


	def toggle_password_visibility(self):
		self.password_visible = not self.password_visible
		echo_mode = QLineEdit.Normal if self.password_visible else QLineEdit.Password
		self.password.setEchoMode(echo_mode)
		self.password_toggle_action.setIcon(self.password_toggle_icons[self.password_visible])
