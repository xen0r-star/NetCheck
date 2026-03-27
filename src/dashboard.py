from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QStyle,
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
)


class DashboardWindow(QWidget):
    logout_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NetTool Admin - Dashboard")
        self.setFixedSize(1100, 620)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.nav = QFrame()
        self.nav.setObjectName("navFrame")
        self.nav.setFixedWidth(280)
        nav_layout = QVBoxLayout(self.nav)
        nav_layout.setContentsMargins(18, 20, 18, 20)
        nav_layout.setSpacing(10)

        brand = QLabel("NetTool")
        brand.setObjectName("mainTitle")

        subtitle = QLabel("Outils Réseau")
        subtitle.setObjectName("fieldLabel")

        self.search_input = QLineEdit()
        self.search_input.setObjectName("navSearch")
        self.search_input.setPlaceholderText("Rechercher une page...")
        self.search_input.textChanged.connect(self.filter_pages)

        nav_layout.addWidget(brand)
        nav_layout.addWidget(subtitle)
        nav_layout.addWidget(self.search_input)
        nav_layout.addSpacing(16)

        self.stack = QStackedWidget()
        self.stack.setObjectName("pagesStack")

        app_style = QApplication.style()
        pages = [
            ("Validation IP", "isip", app_style.standardIcon(QStyle.SP_DialogApplyButton), IsIpPage()),
            ("Masque Classful", "isclassfull", app_style.standardIcon(QStyle.SP_DialogYesButton), IsClassFullPage()),
            ("Classe IP", "getipclass", app_style.standardIcon(QStyle.SP_FileDialogInfoView), GetIpClassPage()),
            ("Masque Par Classe", "getipclassmask", app_style.standardIcon(QStyle.SP_DriveNetIcon), GetIpClassMaskPage()),
            ("Calcul Sous-Reseau", "getsubnet", app_style.standardIcon(QStyle.SP_ComputerIcon), GetSubnetPage()),
            ("Table CIDR", "generertableaucidr", app_style.standardIcon(QStyle.SP_FileDialogDetailedView), CidrTablePage()),
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.nav_buttons = []

        for index, (name, key, icon, page) in enumerate(pages):
            self.stack.addWidget(page)

            btn = QPushButton(name)
            btn.setIcon(icon)
            btn.setCheckable(True)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _checked, idx=index: self.stack.setCurrentIndex(idx))
            self.button_group.addButton(btn)
            nav_layout.addWidget(btn)
            self.nav_buttons.append((index, key, btn))

        nav_layout.addSpacing(8)

        logout_button = QPushButton("Deconnexion")
        logout_button.setObjectName("logoutButton")
        logout_button.setIcon(app_style.standardIcon(QStyle.SP_DialogCloseButton))
        logout_button.setCursor(Qt.PointingHandCursor)
        logout_button.clicked.connect(self.request_logout)
        nav_layout.addWidget(logout_button)

        nav_layout.addStretch(1)

        self.content = QFrame()
        self.content.setObjectName("contentFrame")
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.stack)

        root.addWidget(self.nav)
        root.addWidget(self.content, 1)

        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)

    def filter_pages(self, query):
        normalized = query.strip().lower()
        visible_indexes = []

        for page_index, key, button in self.nav_buttons:
            visible = normalized in key or normalized in button.text().lower()
            button.setVisible(visible)
            if visible:
                visible_indexes.append(page_index)

        current_button = self.button_group.checkedButton()
        if current_button and not current_button.isVisible() and visible_indexes:
            for page_index, _key, button in self.nav_buttons:
                if page_index == visible_indexes[0]:
                    button.setChecked(True)
                    self.stack.setCurrentIndex(page_index)
                    break

    def request_logout(self):
        self.logout_requested.emit()
        self.close()
