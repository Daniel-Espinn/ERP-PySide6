from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox
from models.user import User
import json
from config import TRANSLATIONS_DIR

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 250)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Español"])
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        self.status_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.language_combo)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.status_label)

        self.login_button.clicked.connect(self.login)
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
        self.setWindowTitle(self.translations[lang]["Login"])
        self.username_input.setPlaceholderText(self.translations[lang]["Username"])
        self.password_input.setPlaceholderText(self.translations[lang]["Password"])
        self.login_button.setText(self.translations[lang]["Login"])
        self.register_button.setText(self.translations[lang]["Register"])

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = User.authenticate(username, password)
        if user:
            from ui.main_window import MainWindow
            self.main_window = MainWindow(user)
            self.main_window.show()
            self.accept()
        else:
            self.status_label.setText("Invalid username or password")

    def register(self):
        from ui.register_window import RegisterWindow
        register_window = RegisterWindow()
        if register_window.exec_() == QDialog.Accepted:
            self.status_label.setText("Registration successful")