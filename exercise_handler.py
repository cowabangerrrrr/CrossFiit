from database import Database
from exercise import Exercise

MAX_SERIE_NUMBER = 4
database = Database('data/crossfiit.db')
MAPPING_EXERCISES = {

}

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


def exercize(request):
    main_foto = request.files['main-foto'].filename
    instruction_foto = request.files['instruction-foto'].filename

    if main_foto != '':
        with open(f'static/images/{main_foto}', 'wb') as foto:
            foto.write(request.files['main-foto'].read())

    if instruction_foto != '':
        with open(f'static/images/{instruction_foto}', 'wb') as foto:
            foto.write(request.files['instruction-foto'].read())

    exercise_name = request.form['name-exercise']
    exercise_description = request.form['description']
    exercise_type = MAPPING_EXERCISES[request.form['type-exercise']] \
        if request.form['type-exercise'] in MAPPING_EXERCISES \
        else -1

    return Exercise('', exercise_name, exercise_description, exercise_type, main_foto, instruction_foto)
