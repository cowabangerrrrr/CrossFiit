import json
import os
import requests
import secrets
from urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth
from flask import Flask, abort, redirect, render_template, session, url_for, request, make_response, jsonify, current_app, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_debug import Debug
import exercise_handler
from exercise_handler import *
from random import randint

app = Flask(__name__)
app.secret_key = "5uper 5ecre7 key"

os.environ['GOOGLE_CLIENT_ID'] = 'a'
os.environ['GOOGLE_CLIENT_SECRET'] = 'a'
app.config['OAUTH2_PROVIDERS'] = {
    'google': {
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
    }
}

Debug(app)
login = LoginManager(app)
login.login_view = 'index'

@login.user_loader
def load_user(id):
    user = get_user_by_id(id)
    print(user)
    return user


@app.route('/authorize')
def authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get('google')
    if provider_data is None:
        abort(404)

    session['oauth2_state'] = secrets.token_urlsafe(16)
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('callback', _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    return redirect(provider_data['authorize_url'] + '?' + qs)


@app.route('/callback')
def callback():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get('google')
    if provider_data is None:
        abort(404)

    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    if 'code' not in request.args:
        abort(401)

    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('callback', _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())

    user = get_user_by_email(email)
    if not user:
        insert_user_email_in_db(email)
        user = get_user_by_email(email)
    
    login_user(user)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/workout')
def workout():
    serie_num = randint(1, MAX_SERIE_NUMBER)
    serie = get_exercise_serie(serie_num)
    available_exercises = get_exercises_for_user(None if current_user.is_anonymous else current_user.id)
    return render_template('change.html', serie=serie, exercises=available_exercises)


@app.get('/saved_workout')
def saved_workout():
    saved_serie = get_saved_serie_for_user(current_user.id)
    if not saved_serie:
        session['is_saved_workout'] = True
        return redirect(url_for('index'))
    
    session['delete_restart'] = True
    available_exercises = get_exercises_for_user(None if current_user.is_anonymous else current_user.id)
    return render_template('change.html', serie=saved_serie, exercises=available_exercises)


@app.route('/upload_exercise', methods=['POST'])
def upload_exercise():
    exercise = exercise_handler.exercize(request)
    insert_user_exercise_in_db(exercise, current_user.id)

    return jsonify({'success': True})
    

@app.route('/save_serie', methods=['POST'])
def save_serie_for_user():
    if current_user.is_anonymous:
        return jsonify({'success': False})
    
    data = request.get_json()
    exercises_ids = [int(id) for id in data.get('ids')]
    
    
    database.insert(f'DELETE FROM {database.user_id_exrecise_id_table_name} WHERE user_id = ?', 
                    (current_user.id,))
    for exercise_id in exercises_ids:
        database.insert(f'''
INSERT INTO {database.user_id_exrecise_id_table_name} (user_id, exercise_id)
VALUES (?, ?)
                        ''', (current_user.id, exercise_id))
    return jsonify({'success': True})


@app.route('/get_exercise/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise_data = get_exercise_by_id(id)
    return jsonify(exercise_data)


if __name__ == '__main__':
    app.run(debug=True)