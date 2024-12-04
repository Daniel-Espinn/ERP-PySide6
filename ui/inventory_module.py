from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QHeaderView, QDialog
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.inventory import Inventory

class InventoryModule(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Product Name", "Quantity", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_table()

        self.product_name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)

        self.edit_button = QPushButton("Edit Product")
        self.edit_button.clicked.connect(self.edit_product)
        self.edit_button.setEnabled(False)

        self.delete_button = QPushButton("Delete Product")
        self.delete_button.clicked.connect(self.delete_product)
        self.delete_button.setEnabled(False)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Product Name")
        self.search_input.textChanged.connect(self.search_product)

        self.graph_button = QPushButton("Show Graph")
        self.graph_button.clicked.connect(self.show_graph)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.graph_button)

        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addWidget(QLabel("Product Name"))
        layout.addWidget(self.product_name_input)
        layout.addWidget(QLabel("Quantity"))
        layout.addWidget(self.quantity_input)
        layout.addWidget(QLabel("Price"))
        layout.addWidget(self.price_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.table.cellClicked.connect(self.on_cell_clicked)

        # Configurar QTimer para actualizar la tabla cada 5 segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(5000)  # 5000 ms = 5 segundos

    def refresh_table(self):
        self.table.setRowCount(0)
        inventory = Inventory.get_all()
        for item in inventory:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(item['id'])))
            self.table.setItem(row_position, 1, QTableWidgetItem(item['product_name']))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(item['quantity'])))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(item['price'])))

    def add_product(self):
        product_name = self.product_name_input.text()
        quantity_text = self.quantity_input.text()
        price_text = self.price_input.text()

        if not product_name or not quantity_text or not price_text:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        try:
            quantity = int(quantity_text)
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Quantity and Price must be numbers.")
            return

        inventory = Inventory(product_name, quantity, price)
        inventory.save()
        self.refresh_table()
        self.clear_inputs()

    def edit_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a product to edit.")
            return

        product_id = int(self.table.item(selected_row, 0).text())
        product_name = self.product_name_input.text()
        quantity_text = self.quantity_input.text()
        price_text = self.price_input.text()

        if not product_name or not quantity_text or not price_text:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        try:
            quantity = int(quantity_text)
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Quantity and Price must be numbers.")
            return

        Inventory.update(product_id, product_name, quantity, price)
        self.refresh_table()
        self.clear_inputs()
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a product to delete.")
            return

        product_id = int(self.table.item(selected_row, 0).text())
        Inventory.delete(product_id)
        self.refresh_table()
        self.clear_inputs()
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def search_product(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            product_name = self.table.item(row, 1).text().lower()
            if search_text in product_name:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def on_cell_clicked(self, row, column):
        product_id = self.table.item(row, 0).text()
        product_name = self.table.item(row, 1).text()
        quantity = self.table.item(row, 2).text()
        price = self.table.item(row, 3).text()

        self.product_name_input.setText(product_name)
        self.quantity_input.setText(quantity)
        self.price_input.setText(price)

        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def clear_inputs(self):
        self.product_name_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()

    def show_graph(self):
        inventory = Inventory.get_all()
        product_names = [item['product_name'] for item in inventory]
        quantities = [item['quantity'] for item in inventory]

        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.bar(product_names, quantities)
        ax.set_xlabel('Product Name')
        ax.set_ylabel('Quantity')
        ax.set_title('Inventory Quantities')

        dialog = QDialog(self)
        dialog.setWindowTitle("Inventory Graph")
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(canvas)
        dialog.setLayout(dialog_layout)
        dialog.exec()