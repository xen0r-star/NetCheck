from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QComboBox, QFormLayout, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QInputDialog

from ...services.database import Database



class UserProfilePage(QWidget):
    logout_requested = Signal()

    def __init__(self, user_info=None):
        super().__init__()

        self.db = Database()
        username = user_info["username"] if user_info else "Utilisateur"
        role = user_info["role"] if user_info else "ROLE INCONNU"
        self.current_username = username
        self.is_admin = str(role).lower() == "admin"
        self.last_login = self.db.getLastLogin(username)
        self.user_metadata = {}

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
        profile_layout = QGridLayout(profile_card)
        profile_layout.setContentsMargins(16, 14, 16, 14)
        profile_layout.setHorizontalSpacing(14)
        profile_layout.setVerticalSpacing(6)


        username_label = QLabel(username)
        username_label.setObjectName("resultIp")

        last_login_label = QLabel(f"Derniere connexion: {self._format_timestamp(self.last_login)}")
        last_login_label.setObjectName("statusMessage")

        user_info_col = QVBoxLayout()
        user_info_col.setSpacing(4)
        user_info_col.addWidget(username_label)
        user_info_col.addWidget(last_login_label)

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

        logout_button.setFixedSize(146, 36)

        profile_layout.addLayout(user_info_col, 0, 0, Qt.AlignVCenter | Qt.AlignLeft)
        profile_layout.addWidget(role_badge, 0, 1, Qt.AlignCenter)
        profile_layout.addWidget(logout_button, 0, 2, Qt.AlignVCenter | Qt.AlignRight)
        profile_layout.setColumnStretch(0, 2)
        profile_layout.setColumnStretch(1, 1)
        profile_layout.setColumnStretch(2, 1)

        card_layout.addWidget(profile_card)

        # --- Gestion admin ---
        if self.is_admin:
            admin_card = QFrame()
            admin_card.setObjectName("resultCard")
            admin_layout = QVBoxLayout(admin_card)
            admin_layout.setContentsMargins(16, 14, 16, 14)
            admin_layout.setSpacing(12)

            header_row = QHBoxLayout()
            header_row.setSpacing(12)

            admin_title = QLabel("Gestion des utilisateurs")
            admin_title.setObjectName("resultIp")

            refresh_button = QPushButton("Actualiser")
            refresh_button.setObjectName("actionButton")
            refresh_button.setCursor(Qt.PointingHandCursor)
            refresh_button.clicked.connect(self.refresh_users)
            refresh_button.setFixedSize(140, 44)

            header_row.addWidget(admin_title)
            header_row.addStretch(1)
            header_row.addWidget(refresh_button)

            self.user_table = QTableWidget()
            self.user_table.setObjectName("cidrTable")
            self.user_table.setColumnCount(8)
            self.user_table.setHorizontalHeaderLabels(
                ["ID", "Nom", "Role", "Temp", "Actif", "Echecs", "Bloque jusqu", "Derniere connexion"]
            )
            self.user_table.verticalHeader().setVisible(False)
            self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
            self.user_table.setSelectionMode(QTableWidget.SingleSelection)
            self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.user_table.itemSelectionChanged.connect(self.on_user_selected)
            self.user_table.horizontalHeader().setStretchLastSection(True)
            self.user_table.setMinimumHeight(240)

            self.selection_label = QLabel("Selection: aucune")
            self.selection_label.setObjectName("statusMessage")

            self.add_username_input = QLineEdit()
            self.add_username_input.setObjectName("primaryInput")
            self.add_username_input.setPlaceholderText("Nom d'utilisateur")
            self.add_username_input.setMinimumHeight(40)

            self.add_password_input = QLineEdit()
            self.add_password_input.setObjectName("primaryInput")
            self.add_password_input.setPlaceholderText("Mot de passe")
            self.add_password_input.setEchoMode(QLineEdit.Password)
            self.add_password_input.setMinimumHeight(40)

            self.add_role_input = QComboBox()
            self.add_role_input.setObjectName("primaryInput")
            self.add_role_input.addItems(["member", "admin"])
            self.add_role_input.setMinimumHeight(40)

            self.edit_username_input = QLineEdit()
            self.edit_username_input.setObjectName("primaryInput")
            self.edit_username_input.setPlaceholderText("Nom d'utilisateur")
            self.edit_username_input.setMinimumHeight(40)
            self.edit_username_input.setReadOnly(True)

            self.lock_until_input = QLineEdit()
            self.lock_until_input.setObjectName("primaryInput")
            self.lock_until_input.setPlaceholderText("YYYY-MM-DD HH:MM ou vide")
            self.lock_until_input.setMinimumHeight(40)

            self.edit_role_input = QComboBox()
            self.edit_role_input.setObjectName("primaryInput")
            self.edit_role_input.addItems(["member", "admin"])
            self.edit_role_input.setMinimumHeight(40)

            add_button = QPushButton("Ajouter")
            add_button.setObjectName("actionButton")
            add_button.setCursor(Qt.PointingHandCursor)
            add_button.clicked.connect(self.add_user)
            add_button.setFixedSize(140, 44)

            self.update_button = QPushButton("Modifier")
            self.update_button.setObjectName("actionButton")
            self.update_button.setCursor(Qt.PointingHandCursor)
            self.update_button.clicked.connect(self.update_user)
            self.update_button.setFixedSize(140, 44)

            self.reset_password_button = QPushButton("Reset MDP")
            self.reset_password_button.setObjectName("actionButton")
            self.reset_password_button.setCursor(Qt.PointingHandCursor)
            self.reset_password_button.clicked.connect(self.reset_password)
            self.reset_password_button.setFixedSize(140, 44)

            self.delete_button = QPushButton("Desactiver")
            self.delete_button.setObjectName("dangerButton")
            self.delete_button.setCursor(Qt.PointingHandCursor)
            self.delete_button.clicked.connect(self.delete_user)
            self.delete_button.setFixedSize(140, 44)

            self.admin_message = QLabel("")
            self.admin_message.setObjectName("statusMessage")

            form_card = QFrame()
            form_card.setObjectName("toolCard")
            form_layout = QVBoxLayout(form_card)
            form_layout.setContentsMargins(16, 14, 16, 14)
            form_layout.setSpacing(12)

            form_title = QLabel("Gestion des utilisateurs")
            form_title.setObjectName("resultIp")

            add_title = QLabel("Ajouter un utilisateur")
            add_title.setObjectName("resultIp")

            add_fields = QFormLayout()
            add_fields.setLabelAlignment(Qt.AlignLeft)
            add_fields.setFormAlignment(Qt.AlignTop)
            add_fields.setHorizontalSpacing(10)
            add_fields.setVerticalSpacing(8)
            add_fields.addRow(QLabel("Nom d'utilisateur"), self.add_username_input)
            add_fields.addRow(QLabel("Mot de passe"), self.add_password_input)
            add_fields.addRow(QLabel("Role"), self.add_role_input)

            add_actions = QHBoxLayout()
            add_actions.setSpacing(8)
            add_actions.addWidget(add_button)
            add_actions.addStretch(1)

            edit_title = QLabel("Modifier un utilisateur")
            edit_title.setObjectName("resultIp")

            edit_fields = QFormLayout()
            edit_fields.setLabelAlignment(Qt.AlignLeft)
            edit_fields.setFormAlignment(Qt.AlignTop)
            edit_fields.setHorizontalSpacing(10)
            edit_fields.setVerticalSpacing(8)
            edit_fields.addRow(QLabel("Selection"), self.selection_label)
            edit_fields.addRow(QLabel("Nom d'utilisateur"), self.edit_username_input)
            edit_fields.addRow(QLabel("Role"), self.edit_role_input)
            edit_fields.addRow(QLabel("Bloque jusqu'a"), self.lock_until_input)

            edit_actions = QHBoxLayout()
            edit_actions.setSpacing(8)
            edit_actions.addWidget(self.update_button)
            edit_actions.addWidget(self.reset_password_button)
            edit_actions.addWidget(self.delete_button)
            edit_actions.addStretch(1)

            form_layout.addWidget(form_title)
            form_layout.addWidget(add_title)
            form_layout.addLayout(add_fields)
            form_layout.addLayout(add_actions)
            form_layout.addSpacing(8)
            form_layout.addWidget(edit_title)
            form_layout.addLayout(edit_fields)
            form_layout.addLayout(edit_actions)

            admin_layout.addLayout(header_row)
            admin_layout.addWidget(self.user_table, 1)
            admin_layout.addWidget(form_card)
            admin_layout.addWidget(self.admin_message)

            card_layout.addWidget(admin_card)

            self._set_action_state(False)
            self.refresh_users()

        scroll_layout.addWidget(card)
        scroll_layout.addStretch(1)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _format_timestamp(self, value):
        if not value:
            return "Jamais"
        return value.strftime("%d/%m/%Y %H:%M")

    def _set_action_state(self, enabled):
        self.update_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)
        self.reset_password_button.setEnabled(enabled)

    def set_admin_message(self, text, is_error=False):
        color = "#ff8da1" if is_error else "#a7f3d0"
        self.admin_message.setStyleSheet(f"color: {color};")
        self.admin_message.setText(text)

    def refresh_users(self):
        users = self.db.listUsers()
        self.user_table.setRowCount(len(users))
        self.user_metadata = {}

        for row_index, (user_id, username, role, is_temporary, is_active, failed_attempts, locked_until, last_login) in enumerate(users):
            self.user_table.setItem(row_index, 0, QTableWidgetItem(str(user_id)))
            self.user_table.setItem(row_index, 1, QTableWidgetItem(username))
            self.user_table.setItem(row_index, 2, QTableWidgetItem(role))
            self.user_table.setItem(row_index, 3, QTableWidgetItem("Oui" if is_temporary else "Non"))
            self.user_table.setItem(row_index, 4, QTableWidgetItem("Oui" if is_active else "Non"))
            self.user_table.setItem(row_index, 5, QTableWidgetItem(str(failed_attempts)))
            self.user_table.setItem(row_index, 6, QTableWidgetItem(self._format_timestamp(locked_until)))
            self.user_table.setItem(row_index, 7, QTableWidgetItem(self._format_timestamp(last_login)))
            self.user_metadata[username] = {
                "locked_until": locked_until,
            }

        self.user_table.resizeColumnsToContents()
        self.user_table.clearSelection()
        self._set_action_state(False)
        self.selection_label.setText("Selection: aucune")
        self.edit_username_input.clear()
        self.lock_until_input.clear()

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
        self.edit_username_input.setText(selected_username)

        role_index = self.edit_role_input.findText(selected_role)
        if role_index >= 0:
            self.edit_role_input.setCurrentIndex(role_index)

        self.selection_label.setText(f"Selection: {selected_username}")
        locked_until = self.user_metadata.get(selected_username, {}).get("locked_until")
        self.lock_until_input.setText(self._format_timestamp(locked_until) if locked_until else "")
        self._set_action_state(True)

    def add_user(self):
        username = self.add_username_input.text().strip()
        password = self.add_password_input.text().strip()
        role = self.add_role_input.currentText()

        if not username or not password:
            self.set_admin_message("Nom d'utilisateur et mot de passe obligatoires.", True)
            return

        if self.db.addUser(username, password, role, is_temporary=True):
            self.set_admin_message("Utilisateur ajoute avec succes.")
            self.add_username_input.clear()
            self.add_password_input.clear()
            self.refresh_users()
            return

        self.set_admin_message("Echec de l'ajout (nom deja pris ou erreur SQL).", True)

    def update_user(self):
        username = self.edit_username_input.text().strip()
        role = self.edit_role_input.currentText()
        lock_until_text = self.lock_until_input.text().strip()

        if not username:
            self.set_admin_message("Selectionnez ou saisissez un utilisateur.", True)
            return

        role_ok = self.db.updateRole(username, role)
        lock_ok = True

        if lock_until_text:
            try:
                lock_until = datetime.strptime(lock_until_text, "%d/%m/%Y %H:%M")
            except ValueError:
                try:
                    lock_until = datetime.strptime(lock_until_text, "%Y-%m-%d %H:%M")
                except ValueError:
                    self.set_admin_message("Format date invalide. Utilisez YYYY-MM-DD HH:MM", True)
                    return
            lock_ok = self.db.updateLockout(username, lock_until)
        else:
            lock_ok = self.db.updateLockout(username, None)

        if role_ok and lock_ok:
            self.set_admin_message("Utilisateur modifie avec succes.")
            self.lock_until_input.clear()
            self.refresh_users()
            return

        self.set_admin_message("Echec de la modification.", True)

    def reset_password(self):
        username = self.edit_username_input.text().strip()

        if not username:
            self.set_admin_message("Selectionnez un utilisateur pour reset MDP.", True)
            return

        temp_password, ok = QInputDialog.getText(
            self,
            "Reset MDP",
            "Nouveau mot de passe temporaire",
            QLineEdit.Password
        )

        if not ok:
            return

        if not temp_password.strip():
            self.set_admin_message("Mot de passe temporaire requis.", True)
            return

        if self.db.setTemporaryPassword(username, temp_password.strip()):
            self.set_admin_message("Mot de passe temporaire applique.")
            self.refresh_users()
            return

        self.set_admin_message("Echec du reset MDP.", True)

    def delete_user(self):
        username = self.edit_username_input.text().strip()

        if not username:
            self.set_admin_message("Selectionnez un utilisateur a supprimer.", True)
            return

        if username == self.current_username:
            self.set_admin_message("Desactivation de votre compte interdite.", True)
            return

        confirm = QMessageBox.question(
            self,
            "Confirmation",
            f"Desactiver le compte '{username}' ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        if self.db.deleteUser(username):
            self.set_admin_message("Utilisateur desactive avec succes.")
            self.edit_username_input.clear()
            self.lock_until_input.clear()
            self.refresh_users()
            return

        self.set_admin_message("Echec de la desactivation.", True)
