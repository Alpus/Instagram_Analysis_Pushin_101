# -*- coding: utf-8 -*-
from instagram import client
from app import db
import models
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

    that_user = init_user(instagram_user['id'])
    init_user_media(instagram_user['id'])

    that_user.registration_date = datetime.datetime.now()
    that_user.last_visit = datetime.datetime.now()
    that_user.access_token = access_token
    db.session.commit()

    return that_user.id_user


def init_user(user_id):
    user =\
        db.session.query(models.User).filter(models.User.id_user ==
                                             user_id).first()
    if user is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        user_data = api.user(user_id)
        user = models.User(user_data=user_data)
        db.session.add(user)
        db.session.commit()

    return user


def update_user(user_id):
    user =\
        db.session.query(models.User).filter(models.User.id_user ==
                                             user_id).first()
    if user is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET)
        user_data = api.user(user_id)

        user = models.User(user_data)
        db.session.add(user)
    else:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET)
        user_data = api.user(user_id)

        user.login = user_data.username
        user.full_name = user_data.full_name
        user.profile_picture = user_data.profile_picture
        user.bio = user_data.bio
        user.website = user_data.website
        user.count_media = user_data.counts['media']
        user.count_follows = user_data.counts['follows']
        user.count_followed_by = user_data.counts['followed_by']
        user.last_check = datetime.datetime.now()

    db.session.commit()
    return user


def init_tag(tag_name):
    tag =\
        db.session.query(models.Tag).filter(models.Tag.name ==
                                            tag_name).first()
    if tag is not None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        tag_data = api.tag(tag_name)
        tag = models.Tag(tag_data)
        db.session.add(tag)
        db.session.commit()

    return tag


def init_comment(comment_data):
    comment =\
        db.session.query(models.Comment).filter(models.Comment.id_comment ==
                                                comment_data['id']).first()
    if comment is None:
        comment = models.Comment(comment_data)
        db.session.add(comment)
        db.session.commit()

    return comment


def init_location(location_id):
    location =\
        db.session.query(models.Location).filter(models.Location.id_location ==
                                                 location_id).first()
    if location is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        location_data = api.location(location_id)

        location = models.Location(location_data)
        db.session.add(location)
        db.session.commit()

    return location


def init_user_media(user_id):
    user =\
        db.session.query(models.User).filter(models.User.id_user ==
                                             user_id).first()

    if user is not None:
        api = client.InstagramAPI(access_token=user.access_token)
        next_ = 'start'
        while next_ is not None:
            if next_ is 'start':
                medias, next_ = api.user_recent_media(user_id=user_id)
            else:
                medias, next_ = api.user_recent_media(user_id=user_id,
                                                      max_id=next_)
            for media_data in medias:
                media =\
                    db.session.query(models.Media).filter(models.Media.id_media ==
                                                          media_data.id).first()
                if media is None:
                    media = models.Media(media_data)
                    db.session.add(media)
        db.session.commit()


def update_user_media(user_id):
    user =\
        db.session.query(models.User).filter(models.User.id_user ==
                                             user_id).first()
    if user is not None:
        api = client.InstagramAPI(access_token=user.access_token)
        next_ = 'start'
        while next_ is not None:
            if next_ is 'start':
                medias, next_ = api.user_recent_media(user_id=user_id)
            else:
                medias, next_ = api.user_recent_media(user_id=user_id,
                                                      max_id=next_)
            for media_data in medias:
                media =\
                    db.session.query(models.Media).filter(models.Media.id_media ==
                                                          media_data.id).first()
                if media is None:
                    media = models.Media(media_data)
                    db.session.add(media)
                else:
                    media.caption = media_data.caption['text']
                    media.id_location = media_data.location['id']
                    for like in media_data.likes['data']:
                        user_data = init_user(like['id'])
                        media.liked_by.append(user_data)
                    for mark in media_data.users_in_photo:
                        user_data = init_user(mark['user']['id'])
                        media.users_in_media.append(user_data)
                    for comment in media_data.comments['data']:
                        comment_data = init_comment(comment)
                        media.comments.append(comment_data)
                    for tag in media_data.tags:
                        tag_data = init_tag(tag['name'])
                        media.tags.append(tag_data)

        db.session.commit()


def get_users_who_liked(user_id):
    #user_temp =\
    #    db.session.query(models.User).filter(models.User.id_user ==
    #                                         user_id).first()
    medias =\
        db.session.query(models.Media).filter(models.Media.id_user ==
                                              user_id).first()
    users_who_liked = {}
    for media in medias:
        for user in media.liked_by:
            if user not in users_who_liked:
                users_who_liked[user] = 1
            else:
                users_who_liked[user] += 1
    return users_who_liked.items().sort(key=lambda x: (x[1], x[0].login))