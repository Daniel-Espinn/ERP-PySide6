from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView, QDialog, QCheckBox, QLabel
from PySide6.QtCore import Signal
from models.user import User

class UserManagementModule(QWidget):
    refresh_signal = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Permissions", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_table()

        self.inventory_checkbox = QCheckBox("Inventory")
        self.billing_checkbox = QCheckBox("Billing")
        self.purchase_checkbox = QCheckBox("Purchase")
        self.sales_checkbox = QCheckBox("Sales")
        self.user_management_checkbox = QCheckBox("User Management")

        self.save_button = QPushButton("Save Permissions")
        self.save_button.clicked.connect(self.save_permissions)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(QLabel("Permissions"))
        checkbox_layout.addWidget(self.inventory_checkbox)
        checkbox_layout.addWidget(self.billing_checkbox)
        checkbox_layout.addWidget(self.purchase_checkbox)
        checkbox_layout.addWidget(self.sales_checkbox)
        checkbox_layout.addWidget(self.user_management_checkbox)
        checkbox_layout.addWidget(self.save_button)

        layout.addWidget(self.table)
        layout.addLayout(checkbox_layout)

        self.setLayout(layout)

        self.table.cellClicked.connect(self.on_cell_clicked)
        self.refresh_signal.connect(self.refresh_table)

    def refresh_table(self):
        self.table.setRowCount(0)
        users = User.get_all()
        for user in users:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(user['id'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(user['username']))
            self.table.setItem(row_position, 2, QTableWidgetItem(user['role']))
            self.table.setItem(row_position, 3, QTableWidgetItem(user['permissions']))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, u=user: self.edit_user(u))
            self.table.setCellWidget(row_position, 4, edit_button)

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, u=user: self.delete_user(u))
            self.table.setCellWidget(row_position, 5, delete_button)

    def on_cell_clicked(self, row, column):
        user_id = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        role = self.table.item(row, 2).text()
        permissions = self.table.item(row, 3).text().split(',')

        self.inventory_checkbox.setChecked('inventory' in permissions)
        self.billing_checkbox.setChecked('billing' in permissions)
        self.purchase_checkbox.setChecked('purchase' in permissions)
        self.sales_checkbox.setChecked('sales' in permissions)
        self.user_management_checkbox.setChecked('user_management' in permissions)

    def save_permissions(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        user_id = int(self.table.item(selected_row, 0).text())
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

        User.update_permissions(user_id, ",".join(permissions))
        self.refresh_signal.emit()

    def edit_user(self, user):
        # Obtener los nuevos permisos de los CheckBox
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

        # Actualizar los permisos del usuario
        User.update_permissions(user['id'], ",".join(permissions))
        self.refresh_signal.emit()

    def delete_user(self, user):
        # Código para eliminar usuario...
        User.delete(user['id'])
        self.refresh_signal.emit()