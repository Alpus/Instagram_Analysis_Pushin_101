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


def process_login(code):
    instagram_client = client.InstagramAPI(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URL)
    access_token, instagram_user =\
        instagram_client.exchange_code_for_access_token(code)

    that_user = db.session.query(models.User).filter(models.User.id_user==
      instagram_user['id']).first()
    if (that_user == None):
        api = client.InstagramAPI(access_token=access_token)
        user_data = api.user(instagram_user['id'])

        user = models.User(id_user=instagram_user['id'],
            access_token=access_token, 
            login=instagram_user['username'],
            full_name=instagram_user['full_name'],
            profile_picture=user_data.profile_picture,
            bio=user_data.bio,
            website=user_data.website,
            count_media=user_data.counts['media'],
            count_follows=user_data.counts['follows'],
            count_followed_by=user_data.counts['followed_by'],
            registration_date=datetime.datetime.now())

        db.session.add(user)
        db.session.commit()
        that_user = user
    else:
        api = client.InstagramAPI(access_token=access_token)
        user_data = api.user(instagram_user['id'])

        that_user.update({'login': instagram_user['username']}
        that_user.update({'full_name': instagram_user['full_name']})
        that_user.update({'profile_picture': user_data.profile_picture})
        that_user.update({'bio': user_data.bio})
        that_user.update({'website': user_data.website})
        that_user.update({'count_media': user_data.counts['media']})
        that_user.update({'count_follows': user_data.counts['follows']})
        that_user.update({'count_followed_by': user_data.counts['followed_by']})
        that_user.update({'last_visit': datetime.datetime.now()})
        that_user.update({'access_token': access_token})
        db.session.commit()

    return instagram_user['id']
