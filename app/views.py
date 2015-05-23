# -*- coding: utf-8 -*-
from app import app
from app import db, models
from flask import make_response, render_template, redirect, request, session
import logic
import requests
import forms

CLIENT_ID = requests.CLIENT_ID
CLIENT_SECRET = requests.CLIENT_SECRET
LOGGED_URL = requests.LOGGED_URL
HOME_URL = requests.HOME_URL
REDIRECT_URL = requests.REDIRECT_URL


@app.route('/', methods=('GET', 'POST'))
def index():
    login_url = ('https://api.instagram.com/oauth/authorize/?client_id=' +
                 CLIENT_ID +
                 '&redirect_uri=' + REDIRECT_URL +
                 '&response_type=code&scope=basic')
    user_id = session.get('user_id', None)

    button = forms.Button()
    if button.validate_on_submit():
        if request.form['button'] == 'login':
            return redirect(login_url)
        elif request.form['button'] == 'analysis':
            requests.update_user(user_id)
            requests.update_user_media(user_id)
            requests.update_user_followed_by(user_id)
            requests.update_user_follows(user_id)
            return redirect('/analysis/'+str(user_id))

    return render_template('login.html',

                           button=button,

                           login_url=login_url,
                           user_id=user_id)


@app.route(LOGGED_URL)
def user_logged():
    code = request.values.get('code')
    error = request.values.get('error')
    if error is 'access_denied':
        return redirect('/')
    user_id = requests.process_login(code)

    session.permanent = True
    session['user_id'] = user_id

    return redirect('/')


@app.route('/analysis/<user_id>')
def analysis(user_id):
    user = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user is None:
        return redirect('/')
    else:
        most_liked_media = logic.get_most_liked_media(user_id)
        users_who_liked, sum_of_likes, liker_count, median_like_count = logic.get_users_who_liked(user_id)
        user_tags, tag_count_all, tag_count_unique = logic.get_user_tags(user_id)
        tags_likes = logic.get_tags_likes(user_id)
        follows = logic.get_follows(user_id)
        followed_by = logic.get_followed_by(user_id)
        return render_template('analysis.html',
                               user=user,

                               most_liked_media=enumerate(most_liked_media),

                               users_who_liked=enumerate(users_who_liked),
                               sum_of_likes=sum_of_likes,
                               liker_count=liker_count,
                               median_like_count=median_like_count,

                               user_tags=enumerate(user_tags),
                               tag_count_all=tag_count_all,
                               tag_count_unique=tag_count_unique,

                               tags_likes=enumerate(tags_likes),

                               follows=follows,
                               followed_by=followed_by,

                               home_url=HOME_URL)
