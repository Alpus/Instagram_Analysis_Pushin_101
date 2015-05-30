# -*- coding: utf-8 -*-
from app import app
from app import db, models
from flask import jsonify, make_response, render_template, redirect, request, session, send_from_directory
import logic
import requests
import forms
import datetime

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
    user_login = session.get('user_login', None)

    users = None
    if user_login == 'alpusr':
        users = db.session.query(models.User).filter(models.User.access_token !=
                                                 'Null').all()

    button = forms.Button()
    if button.validate_on_submit():
        if request.form['button'] == 'Log in':
            return redirect(login_url)
        elif request.form['button'] == 'Analysis':
            if requests.is_access_token_valid(user_id):
                requests.update_all_user_information(user_id)
                return redirect('/analysis/'+ str(user_id))
            else:
                session['user_id'] = None
                session['user_login'] = None
                return redirect('/')
        else:
            user_id = request.form['button']
            if requests.is_access_token_valid(user_id):
                requests.update_all_user_information(user_id)
                return redirect('/analysis/'+str(user_id))
            else:
                return redirect('/')

    return render_template('login.html',

                           button=button,

                           login_url=login_url,

                           user_id=user_id,
                           user_login=user_login,

                           users=users)


@app.route(LOGGED_URL)
def user_logged():
    code = request.values.get('code')
    error = request.values.get('error')
    if error is 'access_denied':
        return redirect('/')
    user_id, user_login = requests.process_login(code)

    session.permanent = True
    session['user_id'] = user_id
    session['user_login'] = user_login

    return redirect('/')


@app.route('/analysis/<user_id>')
def analysis(user_id):
    cookie_user_id = session.get('user_id', None)
    cookie_user_login = session.get('user_login', None)
    if cookie_user_login != 'alpusr' and user_id != cookie_user_id:
        return redirect('/')

    user = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user is None:
        return redirect('/')
    else:
        if user.last_check > datetime.date(year=1814, month=7, day=19):
            return render_template('analysis.html',
                                   user=user,
                                   is_media_on_update=True)
        else:
            most_liked_media = logic.get_most_liked_media(user_id)
            users_who_liked, sum_of_likes, liker_count, median_like_count = logic.get_users_who_liked(user_id)
            user_tags, tag_count_all, tag_count_unique = logic.get_user_tags(user_id)
            tags_likes = logic.get_tags_likes(user_id)
            follows = logic.get_follows(user_id)
            followed_by = logic.get_followed_by(user_id)
            user_filters, filter_count = logic.get_user_filter(user_id)
            filter_likes = logic.get_filters_likes(user_id)
            user_locations, location_count_all, location_count_unique = logic.get_user_location(user_id)
            location_likes = logic.get_locations_likes(user_id)
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

                                   user_filters=enumerate(user_filters),
                                   filter_count=filter_count,

                                   filter_likes=enumerate(filter_likes),

                                   user_locations=enumerate(user_locations),
                                   location_count_all=location_count_all,
                                   location_count_unique=location_count_unique,

                                   location_likes=enumerate(location_likes),

                                   home_url=HOME_URL,
                                   is_media_on_update=False)


@app.route('/analysis/<user_id>/is_on_update', methods=['GET'])
def is_on_update(user_id):
    user = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    return jsonify(is_on_update=user.is_media_on_update)


#@app.route('/static/<path:filename>')
#def serve_static(filename):
#    return send_from_directory(app.static_folder, filename)
