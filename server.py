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

    # if 'imageFile' not in request.files:
    #     return jsonify({'error': 'No file part'})
    
    # imageFile = request.files['main-foto']
    # imageName = request.form['imageName']

    exercise = exercise_handler.exercize(request)

    database.insert(f"""
                        INSERT INTO exercises (name, description, muscle_group, main_photo, second_photo)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            exercise.name,
                            exercise.description,
                            exercise.muscle_group,
                            exercise.main_photo,
                            exercise.second_photo
                        )
                    )

    # if imageFile.filename == '':
    #     return jsonify({'error': 'No selected file'})
    #
    # if imageFile and imageName:
    #     filename = secure_filename(imageFile.filename)
    #     imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     imageFile.save(imagePath)
    #
    return jsonify({'success': True})
    # else:
    #     return jsonify({'error': 'Missing image or name'})

@app.route('/get_exercise/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise_data = get_exercise_by_id(id)
    return jsonify(exercise_data)

if __name__ == '__main__':
    app.run(debug=False)