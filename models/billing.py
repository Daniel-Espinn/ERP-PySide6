from database.db import get_db_connection

class Billing:
    def __init__(self, customer_name, total_amount):
        self.customer_name = customer_name
        self.total_amount = total_amount

    @staticmethod
    def create_table():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS billing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                total_amount REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save(self):
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO billing (customer_name, total_amount)
            VALUES (?, ?)
        ''', (self.customer_name, self.total_amount))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.execute('''
            SELECT * FROM billing
        ''')
        billing = cursor.fetchall()
        conn.close()
        return billing

    @staticmethod
    def update(billing_id, customer_name, total_amount):
        conn = get_db_connection()
        conn.execute('''
            UPDATE billing SET customer_name = ?, total_amount = ? WHERE id = ?
        ''', (customer_name, total_amount, billing_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(billing_id):
        conn = get_db_connection()
        conn.execute('''
            DELETE FROM billing WHERE id = ?
        ''', (billing_id,))
        conn.commit()
        conn.close()