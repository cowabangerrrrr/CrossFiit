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
import uuid

app = Flask(__name__)
app.secret_key = "5uper 5ecre7 key"

os.environ['GOOGLE_CLIENT_ID'] = 'cliend_id'
os.environ['GOOGLE_CLIENT_SECRET'] = 'cliend_secret'
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
    pass

@app.route('/')
def index():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        response = make_response(render_template('index.html'))
        response.set_cookie('user_id', user_id)
        return response
    return render_template('index.html')

# @app.route('/login')
# def login():
#     if "user" in session:
#         abort(404)
#     return oauth.myApp.authorize_redirect(redirect_uri=url_for("authorized", _external=True))

# @app.route('/logout')
# def logout():
#     session.pop("user", None)
#     return redirect(url_for("home"))

@app.route('/authorize')
def authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get('google')
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('callback', _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    print(provider_data['authorize_url'] + '?' + qs)
    return redirect(provider_data['authorize_url'] + '?' + qs)

@app.route('/callback')
def callback():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get('google')
    if provider_data is None:
        abort(404)

    print('a')
    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
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

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())

    # find or create the user in the database
    # user = db.session.scalar(db.select(User).where(User.email == email))
    # if user is None:
    #     user = User(email=email, username=email.split('@')[0])
    #     db.session.add(user)
    #     db.session.commit()
    print(email)
    # log the user in
    # login_user(user)
    return redirect(url_for('index'))

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