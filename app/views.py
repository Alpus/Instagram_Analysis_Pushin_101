# -*- coding: utf-8 -*-
from app import app
from app import db, models
from flask import render_template, redirect, request
import logic
import requests

CLIENT_ID = requests.CLIENT_ID
CLIENT_SECRET = requests.CLIENT_SECRET
LOGGED_URL = requests.LOGGED_URL
HOME_URL = requests.HOME_URL
REDIRECT_URL = requests.REDIRECT_URL


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
    user_id = requests.process_login(code)
    return redirect('/analysis/' + str(user_id))


@app.route('/analysis/<user_id>')
def analysis(user_id):
    user = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user is None:
        return redirect('/')
    else:
        requests.update_user(user_id)
        requests.update_user_media(user_id)
        #requests.update_user_followed_by(user_id)
        #requests.update_user_follows(user_id)

        users_who_liked, sum_of_likes, liker_count = logic.get_users_who_liked(user_id)
        user_tags, tag_count_all, tag_count_unique = logic.get_user_tags(user_id)
        tags_likes = logic.get_tags_likes(user_id)
        return render_template('analysis.html',
                               user=user,

                               most_liked_media=enumerate(logic.get_most_liked_media(user_id)),

                               users_who_liked=enumerate(users_who_liked),
                               sum_of_likes=sum_of_likes,
                               liker_count=liker_count,

                               user_tags=enumerate(user_tags),
                               tag_count_all=tag_count_all,
                               tag_count_unique=tag_count_unique,

                               tags_likes=enumerate(tags_likes),

                               home_url=HOME_URL)
