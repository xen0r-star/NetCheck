from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

from services.database import Database



class UserProfilePage(QWidget):
    logout_requested = Signal()

    def __init__(self, user_info=None):
        super().__init__()

        self.db = Database()
        username = user_info["username"] if user_info else "Utilisateur"
        role = user_info["role"] if user_info else "ROLE INCONNU"
        self.current_username = username
        self.is_admin = str(role).lower() == "admin"

        # --- Structure principale ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        # --- Carte profil ---
        card = QFrame()
        card.setObjectName("toolCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 22)
        card_layout.setSpacing(12)

        # --- Informations utilisateur ---
        profile_card = QFrame()
        profile_card.setObjectName("resultCard")
        profile_layout = QHBoxLayout(profile_card)
        profile_layout.setContentsMargins(16, 14, 16, 14)
        profile_layout.setSpacing(12)


        username_label = QLabel(username)
        username_label.setObjectName("resultIp")

        role_badge = QLabel(str(role).upper())
        role_badge.setObjectName("badgeValid")
        role_badge.setFixedWidth(84)
        role_badge.setFixedHeight(24)
        role_badge.setAlignment(Qt.AlignCenter)

        logout_button = QPushButton("Deconnexion")
        logout_button.setObjectName("logoutActionButton")
        logout_button.setCursor(Qt.PointingHandCursor)
        logout_button.setFixedHeight(32)
        logout_button.clicked.connect(self.logout_requested.emit)

        profile_layout.addWidget(username_label, 0, Qt.AlignLeft)
        profile_layout.addWidget(role_badge, 0, Qt.AlignLeft)
        profile_layout.addStretch(1)
        profile_layout.addWidget(logout_button, 0, Qt.AlignRight)

        card_layout.addWidget(profile_card)

        # --- Gestion admin ---
        if self.is_admin:
            admin_card = QFrame()
            admin_card.setObjectName("resultCard")
            admin_layout = QVBoxLayout(admin_card)
            admin_layout.setContentsMargins(16, 14, 16, 14)
            admin_layout.setSpacing(10)

            admin_title = QLabel("Gestion des utilisateurs")
            admin_title.setObjectName("resultIp")

            self.user_table = QTableWidget()
            self.user_table.setObjectName("cidrTable")
            self.user_table.setColumnCount(3)
            self.user_table.setHorizontalHeaderLabels(["ID", "Nom", "Role"])
            self.user_table.verticalHeader().setVisible(False)
            self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
            self.user_table.setSelectionMode(QTableWidget.SingleSelection)
            self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.user_table.itemSelectionChanged.connect(self.on_user_selected)
            self.user_table.horizontalHeader().setStretchLastSection(True)
            self.user_table.setMinimumHeight(220)

            self.username_input = QLineEdit()
            self.username_input.setObjectName("primaryInput")
            self.username_input.setPlaceholderText("Nom d'utilisateur")
            self.username_input.setMinimumHeight(40)

            self.password_input = QLineEdit()
            self.password_input.setObjectName("primaryInput")
            self.password_input.setPlaceholderText("Nouveau mot de passe (optionnel en modification)")
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setMinimumHeight(40)

            self.role_input = QComboBox()
            self.role_input.setObjectName("primaryInput")
            self.role_input.addItems(["member", "admin"])
            self.role_input.setMinimumHeight(40)

            actions_row = QHBoxLayout()
            actions_row.setSpacing(8)

            refresh_button = QPushButton("Actualiser")
            refresh_button.setObjectName("actionButton")
            refresh_button.setCursor(Qt.PointingHandCursor)
            refresh_button.clicked.connect(self.refresh_users)

            add_button = QPushButton("Ajouter")
            add_button.setObjectName("actionButton")
            add_button.setCursor(Qt.PointingHandCursor)
            add_button.clicked.connect(self.add_user)

            update_button = QPushButton("Modifier")
            update_button.setObjectName("actionButton")
            update_button.setCursor(Qt.PointingHandCursor)
            update_button.clicked.connect(self.update_user)

            delete_button = QPushButton("Supprimer")
            delete_button.setObjectName("logoutActionButton")
            delete_button.setCursor(Qt.PointingHandCursor)
            delete_button.clicked.connect(self.delete_user)

            actions_row.addWidget(refresh_button)
            actions_row.addWidget(add_button)
            actions_row.addWidget(update_button)
            actions_row.addWidget(delete_button)

            self.admin_message = QLabel("")
            self.admin_message.setObjectName("statusMessage")

            admin_layout.addWidget(admin_title)
            admin_layout.addWidget(self.user_table, 1)
            admin_layout.addWidget(self.username_input)
            admin_layout.addWidget(self.password_input)
            admin_layout.addWidget(self.role_input)
            admin_layout.addLayout(actions_row)
            admin_layout.addWidget(self.admin_message)

            card_layout.addWidget(admin_card)

            self.log_box = self.build_log_panel(card_layout)
            self.append_log("Panel admin initialise")
            self.refresh_users()

        else:
            self.log_box = self.build_log_panel(card_layout)
            self.append_log("Session utilisateur ouverte")

        scroll_layout.addWidget(card)
        scroll_layout.addStretch(1)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)


    def build_log_panel(self, parent_layout):
        log_card = QFrame()
        log_card.setObjectName("resultCard")
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(16, 14, 16, 14)
        log_layout.setSpacing(8)

        log_title = QLabel("Logs")
        log_title.setObjectName("resultIp")

        log_box = QPlainTextEdit()
        log_box.setObjectName("primaryInput")
        log_box.setReadOnly(True)
        log_box.setMinimumHeight(110)
        log_box.setPlaceholderText("Les evenements s affichent ici...")

        log_layout.addWidget(log_title)
        log_layout.addWidget(log_box)
        parent_layout.addWidget(log_card)
        return log_box

    def append_log(self, message):
        self.log_box.appendPlainText(message)

    def set_admin_message(self, text, is_error=False):
        color = "#ff8da1" if is_error else "#a7f3d0"
        self.admin_message.setStyleSheet(f"color: {color};")
        self.admin_message.setText(text)
        self.append_log(text)

    def refresh_users(self):
        users = self.db.listUsers()
        self.user_table.setRowCount(len(users))

        for row_index, (user_id, username, role) in enumerate(users):
            self.user_table.setItem(row_index, 0, QTableWidgetItem(str(user_id)))
            self.user_table.setItem(row_index, 1, QTableWidgetItem(username))
            self.user_table.setItem(row_index, 2, QTableWidgetItem(role))

        self.user_table.resizeColumnsToContents()

        if self.db.last_error:
            self.set_admin_message(self.db.last_error, True)
            return

        if users:
            self.set_admin_message(f"{len(users)} utilisateur(s) charge(s).")
        else:
            self.set_admin_message("Aucun utilisateur trouve.", True)

    def on_user_selected(self):
        items = self.user_table.selectedItems()
        if not items:
            return

        selected_username = items[1].text()
        selected_role = items[2].text()
        self.username_input.setText(selected_username)

        role_index = self.role_input.findText(selected_role)
        if role_index >= 0:
            self.role_input.setCurrentIndex(role_index)

        self.append_log(f"Utilisateur selectionne: {selected_username}")

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not username or not password:
            self.set_admin_message("Nom d'utilisateur et mot de passe obligatoires.", True)
            return

        if self.db.addUser(username, password, role):
            self.set_admin_message("Utilisateur ajoute avec succes.")
            self.password_input.clear()
            self.refresh_users()
            return

        self.set_admin_message("Echec de l'ajout (nom deja pris ou erreur SQL).", True)

    def update_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not username:
            self.set_admin_message("Selectionnez ou saisissez un utilisateur.", True)
            return

        role_ok = self.db.updateRole(username, role)
        password_ok = True

        if password:
            password_ok = self.db.setPassword(username, password)

        if role_ok and password_ok:
            self.set_admin_message("Utilisateur modifie avec succes.")
            self.password_input.clear()
            self.refresh_users()
            return

        self.set_admin_message("Echec de la modification.", True)

    def delete_user(self):
        username = self.username_input.text().strip()

        if not username:
            self.set_admin_message("Selectionnez un utilisateur a supprimer.", True)
            return

        if username == self.current_username:
            self.set_admin_message("Suppression de votre compte interdite.", True)
            return

        if self.db.deleteUser(username):
            self.set_admin_message("Utilisateur supprime avec succes.")
            self.username_input.clear()
            self.password_input.clear()
            self.refresh_users()
            return

        self.set_admin_message("Echec de la suppression.", True)
