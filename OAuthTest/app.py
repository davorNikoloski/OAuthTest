from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from auth_decorator import login_required
from authlib.jose import jwt


app = Flask(__name__, template_folder="static")
app.secret_key = 'golematajna'
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

#OAuth Conmfig
oauth = OAuth(app)
oauth.init_app(app)
google = oauth.register(  
    name='google',
    client_id=('441739940837-fli3ejpskaifccrrjtr8jsc10ccm7rvm.apps.googleusercontent.com'),
    client_secret=("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"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo',
    client_kwargs={'scope': 'email profile'},
)

@app.route("/")
def index():
    user_info = session.get('profile', {})
    email = user_info.get('email')
    return render_template('index.html',user_info = user_info, email=email)
    

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize(): 
    google = oauth.create_client('google') 
    token = google.authorize_access_token() 
    resp = google.get('userinfo')  
    user_info = resp.json()
    user = oauth.google.userinfo(token = token) 
    
    session['profile'] = user_info
    session.permanent = True 
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True) 