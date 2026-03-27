from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from utils import isClassFull


class IsClassFullPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("toolCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 22, 24, 22)
        card_layout.setSpacing(14)

        row = QHBoxLayout()
        row.setSpacing(10)

        self.mask_input = QLineEdit()
        self.mask_input.setPlaceholderText("Ex: 255.255.255.0")
        self.mask_input.setObjectName("primaryInput")
        self.mask_input.setFixedHeight(46)
        self.mask_input.returnPressed.connect(self.run_check)

        run_button = QPushButton("Analyser")
        run_button.setObjectName("actionButton")
        run_button.setFixedSize(130, 46)
        run_button.setCursor(Qt.PointingHandCursor)
        run_button.clicked.connect(self.run_check)

        row.addWidget(self.mask_input, 1)
        row.addWidget(run_button)

        self.empty_state = QFrame()
        self.empty_state.setObjectName("emptyState")
        empty_layout = QHBoxLayout(self.empty_state)
        empty_layout.setContentsMargins(18, 14, 18, 14)

        empty_text = QLabel("Saisissez un masque pour afficher le diagnostic")
        empty_text.setObjectName("emptyStateText")
        empty_layout.addWidget(empty_text)

        self.result_card = QFrame()
        self.result_card.setObjectName("resultCard")
        self.result_card.setVisible(False)
        result_layout = QVBoxLayout(self.result_card)
        result_layout.setContentsMargins(16, 12, 16, 12)
        result_layout.setSpacing(8)

        self.status_badge = QLabel("STATUT")
        self.status_badge.setObjectName("badgeNeutral")
        self.status_badge.setAlignment(Qt.AlignCenter)
        self.status_badge.setFixedWidth(140)

        self.result = QLabel("")
        self.result.setObjectName("statusMessage")

        result_layout.addWidget(self.status_badge, 0, Qt.AlignLeft)
        result_layout.addWidget(self.result)

        card_layout.addLayout(row)
        card_layout.addWidget(self.empty_state)
        card_layout.addWidget(self.result_card)
        card_layout.addStretch(1)

        layout.addWidget(card)

    def run_check(self):
        mask = self.mask_input.text().strip()
        result = isClassFull(mask)

        self.empty_state.setVisible(False)
        self.result_card.setVisible(True)

        if result == "error":
            self.result.setText("Masque invalide")
            self.result.setStyleSheet("color: #ef4444;")
            self.status_badge.setText("INVALIDE")
            self.status_badge.setObjectName("badgeInvalid")
        elif result:
            self.result.setText("Masque classful valide")
            self.result.setStyleSheet("color: #22c55e;")
            self.status_badge.setText("CLASSFUL")
            self.status_badge.setObjectName("badgeValid")
        else:
            self.result.setText("Masque valide mais non classful")
            self.result.setStyleSheet("color: #f59e0b;")
            self.status_badge.setText("NON CLASSFUL")
            self.status_badge.setObjectName("badgeWarn")

        self.status_badge.style().unpolish(self.status_badge)
        self.status_badge.style().polish(self.status_badge)
