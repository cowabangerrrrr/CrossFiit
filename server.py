import sqlite3
import os
import uuid

from flask import Flask, render_template, request, make_response, jsonify
from flask_debug import Debug
from werkzeug.utils import secure_filename

import exercise_handler
from exercise_handler import *
from random import randint


app = Flask(__name__)
Debug(app)

@app.get('/')
def index():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        response.set_cookie('user_id', user_id)
    response = make_response(render_template('index.html'))
    
    return response

@app.get('/workout')
def workout():
    serie_num = randint(1, MAX_SERIE_NUMBER)
    serie = get_exercise_serie(serie_num)
    all_exercises = get_all_exercises()
    return render_template('change.html', serie=serie, exercises=all_exercises, serie_num=serie_num)

@app.route('/upload_exercise', methods=['POST'])
def upload_exercise():
    exercise = exercise_handler.exercize(request)

    database.insert(f"""
                        INSERT INTO exercises (name, description, main_photo, second_photo)
                        VALUES (?, ?, ?, ?)
                    """,
                        (
                            exercise.name,
                            exercise.description,
                            exercise.main_photo_path,
                            exercise.second_photo_path
                        )
                    )

    return jsonify({'success': True})
    # else:
    #     return jsonify({'error': 'Missing image or name'})
    
@app.route('/save_serie', methods=['POST'])
def save_serie_for_user():
    data = request.get_json()
    user_id = data.get('user_id')
    serie_num = data.get('serie_num')
    database.insert(f'''
INSERT INTO {database.user_id_serie_num_table_name} (user_id, serie)
VALUES (?, ?)
ON CONFLICT(user_id) DO UPDATE SET serie=excluded.serie
                    ''', (user_id, serie_num))
    return jsonify({'success': True})

@app.route('/get_exercise/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise_data = get_exercise_by_id(id)
    return jsonify(exercise_data)

if __name__ == '__main__':
    app.run(debug=True)