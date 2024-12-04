from database.db import get_db_connection

class Inventory:
    def __init__(self, product_name, quantity, price):
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    @staticmethod
    def create_table():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save(self):
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO inventory (product_name, quantity, price)
            VALUES (?, ?, ?)
        ''', (self.product_name, self.quantity, self.price))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.execute('''
            SELECT * FROM inventory
        ''')
        inventory = cursor.fetchall()
        conn.close()
        return inventory

    @staticmethod
    def update(product_id, product_name, quantity, price):
        conn = get_db_connection()
        conn.execute('''
            UPDATE inventory SET product_name = ?, quantity = ?, price = ? WHERE id = ?
        ''', (product_name, quantity, price, product_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(product_id):
        conn = get_db_connection()
        conn.execute('''
            DELETE FROM inventory WHERE id = ?
        ''', (product_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_quantity(product_id, quantity):
        conn = get_db_connection()
        conn.execute('''
            UPDATE inventory SET quantity = quantity - ? WHERE id = ?
        ''', (quantity, product_id))
        conn.commit()
        conn.close()