from database.db import get_db_connection

class Sales:
    def __init__(self, customer_name, total_amount, quantity):
        self.customer_name = customer_name
        self.total_amount = total_amount
        self.quantity = quantity

    @staticmethod
    def create_table():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                total_amount REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save(self):
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO sales (customer_name, total_amount, quantity)
            VALUES (?, ?, ?)
        ''', (self.customer_name, self.total_amount, self.quantity))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.execute('''
            SELECT * FROM sales
        ''')
        sales = cursor.fetchall()
        conn.close()
        return sales

    @staticmethod
    def update(sale_id, customer_name, total_amount, quantity):
        conn = get_db_connection()
        conn.execute('''
            UPDATE sales SET customer_name = ?, total_amount = ?, quantity = ? WHERE id = ?
        ''', (customer_name, total_amount, quantity, sale_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(sale_id):
        conn = get_db_connection()
        conn.execute('''
            DELETE FROM sales WHERE id = ?
        ''', (sale_id,))
        conn.commit()
        conn.close()