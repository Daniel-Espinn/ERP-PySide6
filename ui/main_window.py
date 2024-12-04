# ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QComboBox
from ui.inventory_module import InventoryModule
from ui.billing_module import BillingModule
from ui.purchase_module import PurchaseModule
from ui.sales_module import SalesModule
from ui.user_management_module import UserManagementModule
import json
from config import TRANSLATIONS_DIR

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("ERP System")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.inventory_module = InventoryModule()
        self.billing_module = BillingModule()
        self.purchase_module = PurchaseModule()
        self.sales_module = SalesModule()
        self.user_management_module = UserManagementModule()

        self.add_tabs()

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Español"])
        self.language_combo.currentIndexChanged.connect(self.change_language)

        layout = QVBoxLayout()
        layout.addWidget(self.language_combo)
        layout.addWidget(self.tab_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.translations = {}
        self.load_translations()

    def load_translations(self):
        for lang in ["en", "es"]:
            with open(f"{TRANSLATIONS_DIR}/{lang}.json", "r", encoding="utf-8") as f:
                self.translations[lang] = json.load(f)

    def change_language(self, index):
        lang = "en" if index == 0 else "es"
        self.set_language(lang)

    def set_language(self, lang):
        self.setWindowTitle(self.translations[lang]["ERP System"])
        self.tab_widget.setTabText(0, self.translations[lang]["Inventory"])
        self.tab_widget.setTabText(1, self.translations[lang]["Billing"])
        self.tab_widget.setTabText(2, self.translations[lang]["Purchase"])
        self.tab_widget.setTabText(3, self.translations[lang]["Sales"])
        self.tab_widget.setTabText(4, self.translations[lang]["User Management"])

    def add_tabs(self):
        permissions = self.user['permissions'].split(',')
        if 'inventory' in permissions:
            self.tab_widget.addTab(self.inventory_module, "Inventory")
        if 'billing' in permissions:
            self.tab_widget.addTab(self.billing_module, "Billing")
        if 'purchase' in permissions:
            self.tab_widget.addTab(self.purchase_module, "Purchase")
        if 'sales' in permissions:
            self.tab_widget.addTab(self.sales_module, "Sales")
        if 'user_management' in permissions:
            self.tab_widget.addTab(self.user_management_module, "User Management")