import sqlite3


class Database:
    def __init__(self):
        self._create_table()

    def get_db_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self):
        conn = self.get_db_connection()
        conn.execute(
            """CREATE TABLE IF NOT EXISTS soldiers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id TEXT NOT NULL,
                        name TEXT NOT NULL,
                        birthdate TEXT NOT NULL
                        )"""
        )
        conn.commit()
        conn.close()
