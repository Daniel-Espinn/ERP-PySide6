from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QHeaderView, QDialog
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.purchase import Purchase

class PurchaseModule(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Supplier Name", "Total Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_table()

        self.supplier_name_input = QLineEdit()
        self.total_amount_input = QLineEdit()
        self.add_button = QPushButton("Add Purchase")
        self.add_button.clicked.connect(self.add_purchase)

        self.edit_button = QPushButton("Edit Purchase")
        self.edit_button.clicked.connect(self.edit_purchase)
        self.edit_button.setEnabled(False)

        self.delete_button = QPushButton("Delete Purchase")
        self.delete_button.clicked.connect(self.delete_purchase)
        self.delete_button.setEnabled(False)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Supplier Name")
        self.search_input.textChanged.connect(self.search_purchase)

        self.graph_button = QPushButton("Show Graph")
        self.graph_button.clicked.connect(self.show_graph)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.graph_button)

        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addWidget(QLabel("Supplier Name"))
        layout.addWidget(self.supplier_name_input)
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
        purchase = Purchase.get_all()
        for item in purchase:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(item['id'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(item['supplier_name']))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(item['total_amount'])))

    def add_purchase(self):
        supplier_name = self.supplier_name_input.text()
        total_amount_text = self.total_amount_input.text()

        if not supplier_name or not total_amount_text:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        try:
            total_amount = float(total_amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Total Amount must be a number.")
            return

        purchase = Purchase(supplier_name, total_amount)
        purchase.save()
        self.refresh_table()
        self.clear_inputs()

    def edit_purchase(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a purchase to edit.")
            return

        purchase_id = int(self.table.item(selected_row, 0).text())
        supplier_name = self.supplier_name_input.text()
        total_amount_text = self.total_amount_input.text()

        if not supplier_name or not total_amount_text:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        try:
            total_amount = float(total_amount_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Total Amount must be a number.")
            return

        Purchase.update(purchase_id, supplier_name, total_amount)
        self.refresh_table()
        self.clear_inputs()
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def delete_purchase(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a purchase to delete.")
            return

        purchase_id = int(self.table.item(selected_row, 0).text())
        Purchase.delete(purchase_id)
        self.refresh_table()
        self.clear_inputs()
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def search_purchase(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            supplier_name = self.table.item(row, 1).text().lower()
            if search_text in supplier_name:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def on_cell_clicked(self, row, column):
        purchase_id = self.table.item(row, 0).text()
        supplier_name = self.table.item(row, 1).text()
        total_amount = self.table.item(row, 2).text()

        self.supplier_name_input.setText(supplier_name)
        self.total_amount_input.setText(total_amount)

        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def clear_inputs(self):
        self.supplier_name_input.clear()
        self.total_amount_input.clear()

    def show_graph(self):
        purchase = Purchase.get_all()
        supplier_names = [item['supplier_name'] for item in purchase]
        total_amounts = [item['total_amount'] for item in purchase]

        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.bar(supplier_names, total_amounts)
        ax.set_xlabel('Supplier Name')
        ax.set_ylabel('Total Amount')
        ax.set_title('Purchase Total Amounts')

        dialog = QDialog(self)
        dialog.setWindowTitle("Purchase Graph")
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(canvas)
        dialog.setLayout(dialog_layout)
        dialog.exec()