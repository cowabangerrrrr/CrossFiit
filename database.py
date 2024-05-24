import sqlite3


class Database:
    exercises_table_name = 'exercises'
    exercises_serie_table_name = 'exercises_serie'

    def __init__(self, path_to_db: str):
        self.path_to_db = path_to_db
        self.conn = sqlite3.connect(self.path_to_db, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_database(self):
        self.cursor.execute(
            f'''
CREATE TABLE IF NOT EXISTS {Database.exercises_table_name} 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
--         muscle_group INTEGER NOT NULL,
        main_photo TEXT,
        second_photo TEXT
     );
            ''')
        self.cursor.execute(
            f'''
CREATE TABLE IF NOT EXISTS {Database.exercises_serie_table_name} 
(exercise_id INTEGER NOT NULL, serie INTEGER NOT NULL);
            ''')

    def insert(self, query, data):
        self.cursor.execute(query, data)
        self.conn.commit()

    def select(self, query, data):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()

    def execute_some_good_thing(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        for table in tables:
            try:
                self.cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
            finally:
                pass
        self.conn.commit()
