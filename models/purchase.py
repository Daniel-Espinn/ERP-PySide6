from database.db import get_db_connection

class Purchase:
    def __init__(self, supplier_name, total_amount):
        self.supplier_name = supplier_name
        self.total_amount = total_amount

    @staticmethod
    def create_table():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS purchase (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT NOT NULL,
                total_amount REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save(self):
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO purchase (supplier_name, total_amount)
            VALUES (?, ?)
        ''', (self.supplier_name, self.total_amount))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.execute('''
            SELECT * FROM purchase
        ''')
        purchase = cursor.fetchall()
        conn.close()
        return purchase

    @staticmethod
    def update(purchase_id, supplier_name, total_amount):
        conn = get_db_connection()
        conn.execute('''
            UPDATE purchase SET supplier_name = ?, total_amount = ? WHERE id = ?
        ''', (supplier_name, total_amount, purchase_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(purchase_id):
        conn = get_db_connection()
        conn.execute('''
            DELETE FROM purchase WHERE id = ?
        ''', (purchase_id,))
        conn.commit()
        conn.close()