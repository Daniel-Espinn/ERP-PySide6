from PySide6.QtCore import QObject, Signal

class DataChangeNotifier(QObject):
    inventory_changed = Signal()
    billing_changed = Signal()
    sales_changed = Signal()
    purchase_changed = Signal()
    user_changed = Signal()

data_change_notifier = DataChangeNotifier()