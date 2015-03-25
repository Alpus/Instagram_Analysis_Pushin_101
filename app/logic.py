# -*- coding: utf-8 -*-
from instagram import client
from app import db, models
from sqlalchemy import update
import datetime

CLIENT_ID = '448cfab22275478a9e475784fe8ed4f1'
CLIENT_SECRET = '95e26a3bd94f44c78a534bc8c8a6bacc'
LOGGED_URL = '/logged'
HOME_URL = 'http://54.149.115.96'
REDIRECT_URL = HOME_URL + LOGGED_URL

'''def add_profile_word(user_id, word_name, is_tag):
    that_word = db.session.query(Word).filter_by(word_name=word_name).first()
    if (that_word == None):
        word = Word(word_name=word_name)

    inst_profile = db.session.query(InstProfile).filter_by(id_profile=user_id).first()
    linked_word = inst_profile.words.filter_by(word_name=word_name).first()
    if (lenked_word == None):'''



def process_login(code):
    instagram_client = client.InstagramAPI(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URL)
    access_token, instagram_user =\
        instagram_client.exchange_code_for_access_token(code)

    that_inst_profile = db.session.query(models.InstProfile).filter(models.InstProfile.id_profile==
      instagram_user['id']).first()
    if (that_inst_profile == None):
        inst_profile = models.InstProfile(id_profile=instagram_user['id'],
                               login=instagram_user['username'],
                               full_name=instagram_user['full_name'])
        db.session.add(inst_profile)
        db.session.commit()
        that_inst_profile = inst_profile


    that_user = that_inst_profile.user
    if (that_user == None):
        user = models.User(id_user=instagram_user['id'],
                               access_token=access_token,
                               registration_date=datetime.datetime.now())
        db.session.add(user)
        db.session.commit()
    else:
        that_user.last_visit = datetime.datetime.now()
        that_user.access_token = access_token

    return instagram_user['id']


def get_inst_profile(profile_id):
    inst_profile = db.session.query(models.InstProfile).filter(models.InstProfile.id_profile==
      profile_id).first()
    user = inst_profile.user
    api = client.InstagramAPI(access_token=user.access_token)
    user_data = api.user(profile_id)
    inst_profile.bio = user_data.bio
    inst_profile.website = user_data.website


def get_profiles_posts(profile_id):
    inst_profile = db.session.query(models.InstProfile).filter(models.InstProfile.id_profile==
      profile_id).first()
    user = inst_profile.user
    api = client.InstagramAPI(access_token=user.access_token)
    posts_data = api.user(profile_id)
'''    for post in posts_data:
        for tag in post['tags']:
            add_profile_word(user_id, word_name, true)'''

