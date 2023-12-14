import sqlite3 as db
from contextlib import contextmanager


class Database:
    def __init__(self, db_path='games.db'):
        self.db_path = db_path

    def get_games(self):
        with self.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            return cur.fetchall()

    def create(self):
        with self.connect() as con:
            cursor = con.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titles TEXT,
            release_date TEXT,
            price TEXT,
            review TEXT,
            description TEXT,
            developer TEXT,
            publisher TEXT,
            min_req TEXT
            )''')

    @contextmanager
    def connect(self):
        con = db.connect(self.db_path)
        try:
            yield con
        finally:
            con.close()

    def clear_data(self):
        with self.connect() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM games")
            cur.execute("DELETE FROM sqlite_sequence WHERE name='games'")
            con.commit()

    def has_data(self):
        with self.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM games")
            return cur.fetchone()[0] > 0
