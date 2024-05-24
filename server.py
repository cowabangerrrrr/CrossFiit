import sqlite3
import os
from flask import Flask, render_template, request, jsonify
# from flask_debug import Debug
from werkzeug.utils import secure_filename

import exercise_handler
from exercise_handler import *
from random import randint


app = Flask(__name__)
# Debug(app)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/workout')
def workout():
    serie = get_exercise_serie(randint(1, MAX_SERIE_NUMBER))
    all_exercises = get_all_exercises()
    return render_template('change.html', serie=serie, exercises=all_exercises)

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

@app.route('/get_exercise/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise_data = get_exercise_by_id(id)
    return jsonify(exercise_data)

if __name__ == '__main__':
    app.run(debug=False)