# -*- coding: utf-8 -*-
from app import app
from app import db, models
from flask import render_template, redirect, request
import logic

CLIENT_ID = logic.CLIENT_ID
CLIENT_SECRET = logic.CLIENT_SECRET
LOGGED_URL = logic.LOGGED_URL
HOME_URL = logic.HOME_URL
REDIRECT_URL = logic.REDIRECT_URL
'''INSTAGRAM_LOGIN_URL =
('https://api.instagram.com/oauth/authorize/?client_id=' + CLIENT_ID +
                    '&redirect_uri=' + REDIRECT_URL +
                    '&response_type=code&scope=basic')'''


@app.route('/')
def index():
    login_url = ('https://api.instagram.com/oauth/authorize/?client_id=' +
                 CLIENT_ID +
                 '&redirect_uri=' + REDIRECT_URL +
                 '&response_type=code&scope=basic')
    return render_template('login.html', login_url=login_url)


@app.route(LOGGED_URL)
def user_logged():
    code = request.values.get('code')
    error = request.values.get('error')
    if error is 'access_denied':
        return redirect('/')
    user_id = logic.process_login(code)
    return redirect('/analysis/' + str(user_id))


@app.route('/analysis/<user_id>')
def analysis(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user is None:
        return redirect('/')
    else:
        logic.update_user(user_id)
        logic.update_user_media(user_id)
        return render_template('analysis.html',
                               # profile_picture=user.profile_picture,
                               # user_id=user_id,
                               # login=user.login,
                               # full_name=user.full_name,
                               # bio=user.bio,
                               # website=user.website,
                               # count_media=user.count_media,
                               # count_follows=user.count_follows,
                               # count_followed_by=user.count_followed_by,
                               user,
                               users_who_liked=enumerate(logic.get_users_who_liked(user_id)),
                               home_url=HOME_URL)
