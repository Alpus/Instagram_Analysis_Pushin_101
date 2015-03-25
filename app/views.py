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
'''INSTAGRAM_LOGIN_URL = ('https://api.instagram.com/oauth/authorize/?client_id=' + CLIENT_ID +
                    '&redirect_uri=' + REDIRECT_URL +
                    '&response_type=code&scope=basic')'''


@app.route('/')
def index():
    login_url = ('https://api.instagram.com/oauth/authorize/?client_id=' + CLIENT_ID +
                    '&redirect_uri=' + REDIRECT_URL +
                    '&response_type=code&scope=basic')
    return render_template('login.html', login_url=login_url)

    
@app.route(LOGGED_URL)
def user_logged():
    code = request.values.get('code')
    error = request.values.get('error')
    if (error == 'access_denied'):
        redirect('/')
    user_id = logic.process_login(code)
    redirect('/analysis/' + user_id)


@app.route('/analysis/<profile_id>')
def analysis(profile_id):
    logic.get_inst_profile(profile_id)
    inst_profile = session.query(InstProfile).filter(InstProfile.id_profile==
      profile_id).first()
    return render_template('analysis.html', id_profile = profile_id,
                           login = inst_profile.login,
                           full_name = inst_profile.full_name,
                           bio = inst_profile.bio,
                           website = inst_profile.website)