from database import Database
from exercise import Exercise

MAX_SERIE_NUMBER = 1
database = Database('data/crossfiit.db')

def get_exercise_by_id(id: int) -> Exercise:
    exercise = database.select(
        f'''
SELECT * 
FROM {database.exercises_table_name}
WHERE id = (?)
        ''', (id,))
    
    return Exercise(*exercise[0])


def get_all_exercises() -> list[Exercise]:
    exercises = database.select(
        f'''
SELECT * 
FROM {database.exercises_table_name}
        ''', tuple())
    
    return [Exercise(*exercise) for exercise in exercises]


def get_exercise_serie(serie_num: int) -> list[Exercise]:
    serie = database.select(
        f'''
SELECT id, name, description, muscle_group, main_photo, second_photo
FROM {database.exercises_serie_table_name}
LEFT OUTER JOIN {database.exercises_table_name}
ON id = exercise_id
WHERE serie = (?)
        ''', (serie_num,))
    
    return [Exercise(*exercise) for exercise in serie]


def exercize(data):
    pass
