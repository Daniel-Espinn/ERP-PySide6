import sys
from PySide6.QtWidgets import QApplication, QDialog
from ui.login_window import LoginWindow
from models.user import User
from models.inventory import Inventory
from models.billing import Billing
from models.purchase import Purchase
from models.sales import Sales

if __name__ == "__main__":
    app = QApplication(sys.argv)

    User.create_table()
    Inventory.create_table()
    Billing.create_table()
    Purchase.create_table()
    Sales.create_table()

    with open("ui/styles.css", "r") as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)

    login_window = LoginWindow()
    if login_window.exec() == QDialog.Accepted:
        sys.exit(app.exec())
