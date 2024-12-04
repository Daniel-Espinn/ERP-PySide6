from database.db import get_db_connection

class User:
    def __init__(self, username, password, role, permissions):
        self.username = username
        self.password = password
        self.role = role
        self.permissions = permissions

    @staticmethod
    def create_table():
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                permissions TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save(self):
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO users (username, password, role, permissions)
            VALUES (?, ?, ?, ?)
        ''', (self.username, self.password, self.role, self.permissions))
        conn.commit()
        conn.close()

    @staticmethod
    def authenticate(username, password):
        conn = get_db_connection()
        cursor = conn.execute('''
            SELECT * FROM users WHERE username = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.execute('''
            SELECT * FROM users
        ''')
        users = cursor.fetchall()
        conn.close()
        return users

    @staticmethod
    def update_permissions(user_id, permissions):
        conn = get_db_connection()
        conn.execute('''
            UPDATE users SET permissions = ? WHERE id = ?
        ''', (permissions, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        conn.execute('''
            DELETE FROM users WHERE id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()