# ui/charts_module.py
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from models.sales import Sales
from models.purchase import Purchase
from PySide6.QtGui import QPainter

class ChartsModule(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.sales_chart = QChart()
        self.sales_chart_view = QChartView(self.sales_chart)
        self.sales_chart_view.setRenderHint(QPainter.Antialiasing)

        self.purchase_chart = QChart()
        self.purchase_chart_view = QChartView(self.purchase_chart)
        self.purchase_chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(self.sales_chart_view)
        layout.addWidget(self.purchase_chart_view)

        self.setLayout(layout)

        self.refresh_charts()

    def refresh_charts(self):
        self.refresh_sales_chart()
        self.refresh_purchase_chart()

    def refresh_sales_chart(self):
        sales = Sales.get_all()
        series = QPieSeries()
        for sale in sales:
            series.append(sale['customer_name'], sale['total_amount'])

        self.sales_chart.removeAllSeries()
        self.sales_chart.addSeries(series)
        self.sales_chart.setTitle("Sales by Customer")

    def refresh_purchase_chart(self):
        purchases = Purchase.get_all()
        series = QPieSeries()
        for purchase in purchases:
            series.append(purchase['supplier_name'], purchase['total_amount'])

        self.purchase_chart.removeAllSeries()
        self.purchase_chart.addSeries(series)
        self.purchase_chart.setTitle("Purchases by Supplier")