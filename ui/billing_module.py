from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QHeaderView, QDialog
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.billing import Billing

class BillingModule(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Customer Name", "Total Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_table()

        self.customer_name_input = QLineEdit()
        self.total_amount_input = QLineEdit()
        self.add_button = QPushButton("Add Billing")
        self.add_button.clicked.connect(self.add_billing)

        self.edit_button = QPushButton("Edit Billing")
        self.edit_button.clicked.connect(self.edit_billing)
        self.edit_button.setEnabled(False)

        self.delete_button = QPushButton("Delete Billing")
        self.delete_button.clicked.connect(self.delete_billing)
        self.delete_button.setEnabled(False)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Customer Name")
        self.search_input.textChanged.connect(self.search_billing)

        self.graph_button = QPushButton("Show Graph")
        self.graph_button.clicked.connect(self.show_graph)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.graph_button)

        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addWidget(QLabel("Customer Name"))
        layout.addWidget(self.customer_name_input)
        layout.addWidget(QLabel("Total Amount"))
        layout.addWidget(self.total_amount_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.table.cellClicked.connect(self.on_cell_clicked)

        # Configurar QTimer para actualizar la tabla cada 5 segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(5000)  # 5000 ms = 5 segundos

    def refresh_table(self):
        self.table.setRowCount(0)
        billing = Billing.get_all()
        for item in billing:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(item['id'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(item['customer_name']))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(item['total_amount'])))

    def add_billing(self):
        customer_name = self.customer_name_input.text()
        total_amount_text = self.total_amount_input.text()

        if not customer_name or not total_amount_text:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        try:
            total_amount = float(total_amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Total Amount must be a number.")
            return

        billing = Billing(customer_name, total_amount)
        billing.save()
        self.refresh_table()
        self.clear_inputs()

    def edit_billing(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a billing to edit.")
            return

        billing_id = int(self.table.item(selected_row, 0).text())
        customer_name = self.customer_name_input.text()
        total_amount_text = self.total_amount_input.text()

        if not customer_name or not total_amount_text:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        try:
            total_amount = float(total_amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Total Amount must be a number.")
            return

        Billing.update(billing_id, customer_name, total_amount)
        self.refresh_table()
        self.clear_inputs()
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def delete_billing(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a billing to delete.")
            return

        billing_id = int(self.table.item(selected_row, 0).text())
        Billing.delete(billing_id)
        self.refresh_table()
        self.clear_inputs()
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def search_billing(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            customer_name = self.table.item(row, 1).text().lower()
            if search_text in customer_name:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def on_cell_clicked(self, row, column):
        billing_id = self.table.item(row, 0).text()
        customer_name = self.table.item(row, 1).text()
        total_amount = self.table.item(row, 2).text()

        self.customer_name_input.setText(customer_name)
        self.total_amount_input.setText(total_amount)

        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def clear_inputs(self):
        self.customer_name_input.clear()
        self.total_amount_input.clear()

    def show_graph(self):
        billing = Billing.get_all()
        customer_names = [item['customer_name'] for item in billing]
        total_amounts = [item['total_amount'] for item in billing]

        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.bar(customer_names, total_amounts)
        ax.set_xlabel('Customer Name')
        ax.set_ylabel('Total Amount')
        ax.set_title('Billing Total Amounts')

        dialog = QDialog(self)
        dialog.setWindowTitle("Billing Graph")
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(canvas)
        dialog.setLayout(dialog_layout)
        dialog.exec()