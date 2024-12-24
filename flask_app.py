import os
from flask import Flask, send_from_directory, session, redirect, url_for, render_template, request
import requests


GITHUB_CLIENT_ID = 'Ov23liSzCwYCit46QJzQ'  # Замените на ваш Client ID
GITHUB_CLIENT_SECRET = '3b8395d11e1671bcfe3faf96a3f8495eddb920a2'  # Замените на ваш Client Secret
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_API_URL = 'https://api.github.com/user'

app = Flask(__name__)
app.secret_key = "sad"
BOT_TOKEN = "7931056264:AAEnLsI0U7UY5cw6j6SvQMBVfIGIZ58AIwE"

site2_path = os.path.join(os.path.dirname(__file__), 'Html')

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return redirect(url_for('serve_html', filename='index.html', user=user['username']))
    else:
        return send_from_directory(site2_path, 'index.html', mimetype='text/html')

@app.route('/yandex_1be8d855839fe265.html')
def root():
    return render_template("/yandex_1be8d855839fe265.html")
@app.route('/login')
def login():
    return redirect(f'{GITHUB_AUTHORIZE_URL}?client_id={GITHUB_CLIENT_ID}&redirect_uri={url_for("callback", _external=True)}')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Ошибка авторизации', 400

    # Обмен кода на токен
    token_response = requests.post(GITHUB_TOKEN_URL, data={
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': url_for('callback', _external=True)
    }, headers={'Accept': 'application/json'})

    if token_response.status_code != 200:
        return 'Ошибка получения токена', 400

    access_token = token_response.json().get('access_token')
    session['github_token'] = access_token

    return redirect(url_for('home'))

@app.route('/<path:filename>')
def serve_html(filename):
    return send_from_directory(site2_path, filename, mimetype='text/html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(site2_path, 'static'), filename)


if __name__ == '__main__':
    app.run(debug=True)