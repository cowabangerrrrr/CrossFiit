import sqlite3
import os
from flask import Flask, render_template, request, jsonify
from flask_debug import Debug
from werkzeug.utils import secure_filename


app = Flask(__name__)
Debug(app)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/workout')
def workout():
    data = [{"storage": "anschumania.png", "name": "Анжуманя", "id": "1"},
            {"storage": "planka.png", "name": "Планка", "id": "2"}]
    return render_template('change.html', data=data)

@app.route('/upload_exercise', methods=['POST'])
def upload_exrecise():
    if 'imageFile' not in request.files:
        return jsonify({'error': 'No file part'})
    
    imageFile = request.files['imageFile']
    imageName = request.form['imageName']

    if imageFile.filename == '':
        return jsonify({'error': 'No selected file'})

    if imageFile and imageName:
        filename = secure_filename(imageFile.filename)
        imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imageFile.save(imagePath)
        
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Missing image or name'})


if __name__ == '__main__':
    app.run(debug=True)