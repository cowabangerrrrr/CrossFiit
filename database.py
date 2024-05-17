import sqlite3
import re


class Database:
    exercises_table_name = 'exercises'

    def __init__(self, path_to_db: str):
        self.path_to_db = path_to_db
        self.conn = sqlite3.connect(self.path_to_db)
        self.conn.create_function('regexp', 2, self.__regexp)
        self.cursor = self.conn.cursor()

    def __regexp(self, expr: str, item: str):
        reg = re.compile(expr)
        return reg.search(item) is not None

    def create_database(self):
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {Database.exercises_table_name} (id TEXT, lat REAL, lon REAL)")

    def insert(self, data: list[Exercise]):
        self.cursor.executemany('', data)
        self.conn.commit()

    def select(self, query, data):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()
