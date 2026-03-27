import os

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from pages import (
    CidrTablePage,
    GetIpClassMaskPage,
    GetIpClassPage,
    GetSubnetPage,
    IsClassFullPage,
    IsIpPage,
    UserProfilePage,
)


class DashboardWindow(QWidget):
    logout_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("dashboardWindow")
        self.setWindowTitle("NetTool Admin - Dashboard")
        self.setFixedSize(1150, 650)

        # --- Structure principale ---
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        shell = QFrame()
        shell.setObjectName("dashboardShell")
        shell_layout = QHBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)

        # --- Barre laterale ---
        self.nav = QFrame()
        self.nav.setObjectName("navFrame")
        self.nav.setFixedWidth(222)
        nav_layout = QVBoxLayout(self.nav)
        nav_layout.setContentsMargins(16, 20, 16, 16)
        nav_layout.setSpacing(10)

        brand = QLabel("NetTool")
        brand.setObjectName("sidebarBrand")

        subtitle = QLabel("Outils Réseau")
        subtitle.setObjectName("sidebarSubtitle")

        nav_layout.addWidget(brand)
        nav_layout.addWidget(subtitle)
        nav_layout.addSpacing(14)

        # --- Zone des pages ---
        self.stack = QStackedWidget()
        self.stack.setObjectName("pagesStack")

        self.current_page_title = QLabel("Validation IP")
        self.current_page_title.setObjectName("dashboardHeading")

        self.current_page_hint = QLabel("Vérifie si une adresse IPv4 est valide")
        self.current_page_hint.setObjectName("dashboardSubheading")

        icons_dir = os.path.join(os.path.dirname(__file__), "assets", "icons")
        user_page = UserProfilePage()
        user_page.logout_requested.connect(self.request_logout)

        pages = [
            ("Validation IP", "Vérifie si une adresse IPv4 est valide", QIcon(os.path.join(icons_dir, "ip.svg")), IsIpPage()),
            ("Masque Classful", "Vérifie si un masque contient uniquement des 255 et des 0", QIcon(os.path.join(icons_dir, "mask.svg")), IsClassFullPage()),
            ("Classe IP", "Détermine la classe de l'adresse IPv4", QIcon(os.path.join(icons_dir, "class.svg")), GetIpClassPage()),
            ("Masque Par Classe", "Retourne le masque par défaut selon la classe IP", QIcon(os.path.join(icons_dir, "mask.svg")), GetIpClassMaskPage()),
            ("Calcul Sous-Reseau", "Calcule l'adresse réseau à partir de l'IP et du masque", QIcon(os.path.join(icons_dir, "subnet.svg")), GetSubnetPage()),
            ("Table CIDR", "Affiche les correspondances CIDR, binaire et décimal", QIcon(os.path.join(icons_dir, "cidr.svg")), CidrTablePage()),
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.page_descriptions = {}

        for index, (name, description, icon, page) in enumerate(pages):
            self.stack.addWidget(page)
            self.page_descriptions[index] = description

            btn = QPushButton(name)
            btn.setIcon(icon)
            btn.setIconSize(QSize(18, 18))
            btn.setCheckable(True)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _checked, idx=index, title=name: self.switch_page(idx, title))
            self.button_group.addButton(btn)
            nav_layout.addWidget(btn)

        self.profile_page_index = self.stack.addWidget(user_page)
        self.page_descriptions[self.profile_page_index] = "Informations du compte et session actuelle"

        nav_layout.addStretch(1)

        user_card = QFrame()
        user_card.setObjectName("navUserCard")
        user_layout = QVBoxLayout(user_card)
        user_layout.setContentsMargins(12, 10, 12, 10)
        user_layout.setSpacing(2)

        user_name = QLabel("Admin")
        user_name.setObjectName("navUserName")

        user_role = QLabel("Nom Prenom")
        user_role.setObjectName("navUserRole")

        user_layout.addWidget(user_name)
        user_layout.addWidget(user_role)

        # Ouvre la page profil depuis la carte utilisateur.
        user_card.setCursor(Qt.PointingHandCursor)
        user_card.mousePressEvent = self.open_profile_page

        nav_layout.addWidget(user_card)

        self.content = QFrame()
        self.content.setObjectName("contentFrame")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(26, 22, 26, 22)
        content_layout.setSpacing(18)

        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        header_text_col = QVBoxLayout()
        header_text_col.setSpacing(4)
        header_text_col.addWidget(self.current_page_title)
        header_text_col.addWidget(self.current_page_hint)

        header_row.addLayout(header_text_col)
        header_row.addStretch(1)

        content_layout.addLayout(header_row)
        content_layout.addWidget(self.stack, 1)

        shell_layout.addWidget(self.nav)
        shell_layout.addWidget(self.content, 1)

        root.addWidget(shell)

        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)
            self.switch_page(0, self.button_group.buttons()[0].text())

    def switch_page(self, page_index, title):
        self.stack.setCurrentIndex(page_index)
        self.current_page_title.setText(title)
        self.current_page_hint.setText(self.page_descriptions.get(page_index, ""))
        self.current_page_hint.setVisible(page_index != self.profile_page_index)

    def open_profile_page(self, _event):
        self.switch_page(self.profile_page_index, "Profil Utilisateur")
        for button in self.button_group.buttons():
            button.setChecked(False)

    def request_logout(self):
        self.logout_requested.emit()
        self.close()
