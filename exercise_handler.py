from database import Database
from exercise import Exercise
from user import User

MAX_SERIE_NUMBER = 4
database = Database('data/crossfiit.db')
database.create_database()
MAPPING_EXERCISES = {

}

def get_exercise_by_id(id: int) -> Exercise:
    exercise = database.select(
        f'''
SELECT id, name, description, main_photo, second_photo
FROM {database.exercises_table_name}
WHERE id = (?)
        ''', (id,))
    
    return Exercise(*exercise[0])


def get_exercises_for_user(user_id=None) -> list[Exercise]:
    ids = ('-1', str(user_id)) if user_id else ('-1',)
    
    exercises = database.select(
        f'''
SELECT id, name, description, main_photo, second_photo
FROM {database.exercises_table_name}
WHERE user_id IN ( {', '.join(ids)} );
        ''', tuple())
    
    return [Exercise(*exercise) for exercise in exercises]


def get_exercise_serie(serie_num: int) -> list[Exercise]:
    serie = database.select(
        f'''
SELECT id, name, description, main_photo, second_photo
FROM {database.exercises_serie_table_name}
LEFT OUTER JOIN {database.exercises_table_name}
ON id = exercise_id
WHERE serie = (?)
        ''', (serie_num,))
    
    return [Exercise(*exercise) for exercise in serie]

    
def get_saved_serie_for_user(user_id):
    exercises_ids = database.select(f'''
SELECT exercise_id
FROM {database.user_id_exrecise_id_table_name}
WHERE user_id = (?)
        ''', (user_id, ))
    if not exercises_ids:
        return None
    
    return [get_exercise_by_id(exercise_id[0]) for exercise_id in exercises_ids]

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
    # exercise_type = MAPPING_EXERCISES[request.form['type-exercise']] \
    #     if request.form['type-exercise'] in MAPPING_EXERCISES \
    #     else -1

    return Exercise('', exercise_name, exercise_description, main_foto, instruction_foto)

def get_user_by_id(id):
    user = database.select(f'''
SELECT * 
FROM {database.user_info_table_name}
WHERE user_id = (?)
    ''', (id,))
    if not user:
        return None
    
    return User(*user[0])

def get_user_by_email(email):
    user = database.select(f'''
SELECT * 
FROM {database.user_info_table_name}
WHERE email = (?);
    ''', (email,))
    if not user:
        return None
    
    return User(*user[0])

def insert_user_email_in_db(email):
    database.insert(f'''
INSERT INTO {database.user_info_table_name} (email)
VALUES (?);
    ''', (email,))
    
def insert_user_exercise_in_db(exercise: Exercise, user_id: int):
    database.insert(f"""
INSERT INTO exercises (name, description, main_photo, second_photo, user_id)
VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            exercise.name,
                            exercise.description,
                            exercise.main_photo_path,
                            exercise.second_photo_path,
                            user_id
                        )
                    )
