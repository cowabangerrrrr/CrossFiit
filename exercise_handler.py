from database import Database
from exercise import Exercise
from user import User

database = Database('data/crossfiit.db')
database.create_database()
count_exercises_for_users = {}


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

def exercize(request, user_id):
    if user_id not in count_exercises_for_users:
        count_exercises_for_users[user_id] = 0
    
    main_foto = request.files['main-foto'].filename
    instruction_foto = request.files['instruction-foto'].filename

    if main_foto != '':
        main_foto = f'{user_id}0{count_exercises_for_users[user_id]}'
        with open(f'static/images/{main_foto}', 'wb') as foto:
            foto.write(request.files['main-foto'].read())

    if instruction_foto != '':
        instruction_foto = f'{user_id}1{count_exercises_for_users[user_id]}'
        with open(f'static/images/{instruction_foto}', 'wb') as foto:
            foto.write(request.files['instruction-foto'].read())

    count_exercises_for_users[user_id] += 1
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

def set_count_exercises_for_users():
    global count_exercises_for_users
    data = database.select(f'''
SELECT user_id, COUNT(id)
FROM {database.exercises_table_name}
WHERE user_id != -1
GROUP BY user_id''', tuple())
    count_exercises_for_users = {pair[0]: pair[1] for pair in data }

def count_serie_number():
    data = database.select(f'''
SELECT COUNT( DISTINCT serie )
FROM {database.exercises_serie_table_name}''', tuple())
    return data[0][0]
