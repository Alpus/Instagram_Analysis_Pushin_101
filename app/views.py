# -*- coding: utf-8 -*-
from app import app
from app import db, models
from flask import jsonify, make_response, render_template, redirect, request, session, send_from_directory, url_for
import logic
import requests
import datetime

CLIENT_ID = requests.CLIENT_ID
CLIENT_SECRET = requests.CLIENT_SECRET
LOGGED_URL = requests.LOGGED_URL
HOME_URL = requests.HOME_URL
REDIRECT_URL = requests.REDIRECT_URL
LOGIN_URL = ('https://api.instagram.com/oauth/authorize/?client_id=' +
             CLIENT_ID +
             '&redirect_uri=' + REDIRECT_URL +
             '&response_type=code&scope=basic')


class Cookie:
    def __init__(self, user_id, user_login):
        self.user_id = user_id
        self.user_login = user_login
        user = \
            db.session.query(models.User).filter(models.User.inst_id_user ==
                                                 user_id).first()
        if user is not None and user.login == user_login:
            self.valid = True
        else:
            self.valid = False


@app.route('/')
@app.route('/index')
def index():
    user_id = session.get('user_id', None)
    user_login = session.get('user_login', None)

    cookie = Cookie(user_id=user_id, user_login=user_login)

    if cookie.valid:
        if not requests.is_access_token_valid(user_id=user_id):
            session['user_id'] = None
            session['user_login'] = None
            return redirect('/')
        top_users = logic.get_top_users()
        requests.update_user(user_id=user_id)
        user_information = logic.get_user_information(user_id=user_id)
        return render_template('index.html',
                               user_information=user_information,
                               top_users = top_users,
                               cookie=cookie,
                               login_url=LOGIN_URL)
    else:
        top_users = logic.get_top_users()
        return render_template('index.html',
                               top_users = top_users,
                               cookie=cookie,
                               login_url=LOGIN_URL)


@app.route(LOGGED_URL)
def user_logged():
    code = request.values.get('code')
    error = request.values.get('error')
    if error == 'access_denied':
        return redirect('/')
    user_id, user_login = requests.process_login(code)
    session.permanent = True
    session['user_id'] = user_id
    session['user_login'] = user_login

    return redirect('/')


@app.route('/is_on_update/<user_id>')
def is_on_update(user_id):
    return jsonify(is_ready_to_show=logic.is_user_ready_to_show(user_id=user_id))


@app.route('/logout')
def logout():
    session['user_id'] = None
    session['user_login'] = None
    return redirect('/')


@app.route('/secretadminsuperpage/<login>')
def secret(login):
    user = \
            db.session.query(models.User).filter(models.User.login ==
                                                 login).first()
    session['user_id'] = user.inst_id_user
    session['user_login'] = login
    return redirect('/')


#@app.route('/static/<path:filename>')
#def serve_static(filename):
#    return send_from_directory(app.static_folder, filename)
