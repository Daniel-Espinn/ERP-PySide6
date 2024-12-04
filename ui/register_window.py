from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QCheckBox
from models.user import User
import json
from config import TRANSLATIONS_DIR

class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 300, 350)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Español"])
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.role_input = QLineEdit()
        self.inventory_checkbox = QCheckBox("Inventory")
        self.billing_checkbox = QCheckBox("Billing")
        self.purchase_checkbox = QCheckBox("Purchase")
        self.sales_checkbox = QCheckBox("Sales")
        self.user_management_checkbox = QCheckBox("User Management")
        self.register_button = QPushButton("Register")
        self.status_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.language_combo)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Confirm Password"))
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(QLabel("Role"))
        layout.addWidget(self.role_input)
        layout.addWidget(QLabel("Permissions"))
        layout.addWidget(self.inventory_checkbox)
        layout.addWidget(self.billing_checkbox)
        layout.addWidget(self.purchase_checkbox)
        layout.addWidget(self.sales_checkbox)
        layout.addWidget(self.user_management_checkbox)
        layout.addWidget(self.register_button)
        layout.addWidget(self.status_label)

        self.register_button.clicked.connect(self.register)

        self.setLayout(layout)

        self.translations = {}
        self.load_translations()
        self.set_language("en")

    def load_translations(self):
        for lang in ["en", "es"]:
            with open(f"{TRANSLATIONS_DIR}/{lang}.json", "r", encoding="utf-8") as f:
                self.translations[lang] = json.load(f)

    def change_language(self, index):
        lang = "en" if index == 0 else "es"
        self.set_language(lang)

    def set_language(self, lang):
        self.setWindowTitle(self.translations[lang]["Register"])
        self.username_input.setPlaceholderText(self.translations[lang]["Username"])
        self.password_input.setPlaceholderText(self.translations[lang]["Password"])
        self.confirm_password_input.setPlaceholderText(self.translations[lang]["Confirm Password"])
        self.role_input.setPlaceholderText(self.translations[lang]["Role"])
        self.register_button.setText(self.translations[lang]["Register"])
        self.inventory_checkbox.setText(self.translations[lang]["Inventory"])
        self.billing_checkbox.setText(self.translations[lang]["Billing"])
        self.purchase_checkbox.setText(self.translations[lang]["Purchase"])
        self.sales_checkbox.setText(self.translations[lang]["Sales"])
        self.user_management_checkbox.setText(self.translations[lang]["User Management"])

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        role = self.role_input.text()
        permissions = []
        if self.inventory_checkbox.isChecked():
            permissions.append("inventory")
        if self.billing_checkbox.isChecked():
            permissions.append("billing")
        if self.purchase_checkbox.isChecked():
            permissions.append("purchase")
        if self.sales_checkbox.isChecked():
            permissions.append("sales")
        if self.user_management_checkbox.isChecked():
            permissions.append("user_management")

        if password != confirm_password:
            self.status_label.setText("Passwords do not match")
            return

        user = User(username, password, role, ",".join(permissions))
        user.save()
        self.accept()