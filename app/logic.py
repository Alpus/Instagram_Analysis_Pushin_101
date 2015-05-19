# -*- coding: utf-8 -*-
from instagram import client
from app import db
import models
import datetime
import unicodedata

CLIENT_ID = '448cfab22275478a9e475784fe8ed4f1'
CLIENT_SECRET = '95e26a3bd94f44c78a534bc8c8a6bacc'
LOGGED_URL = '/logged'
HOME_URL = 'http://54.149.115.96'
REDIRECT_URL = HOME_URL + LOGGED_URL


def process_login(code):
    instagram_client = client.InstagramAPI(client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri=REDIRECT_URL)
    unicodedata.normalize('NFKD', code).encode('ascii','ignore')
    access_token, instagram_user =\
        instagram_client.exchange_code_for_access_token(code)

    that_user = init_user_by_id(instagram_user['id'])

    that_user.registration_date = datetime.datetime.now()
    that_user.last_visit = datetime.datetime.now()
    that_user.access_token = access_token
    db.session.commit()

    init_user_media(instagram_user['id'])

    return that_user.inst_id_user


def init_user_by_id(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        user_data = api.user(user_id)
        user = models.User(user_data=user_data)
        db.session.add(user)
        db.session.commit()

    return user


def init_user_by_information(like):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             like.id).first()
    if user is None:
        user = models.User(user_data=like)
        db.session.add(user)
        db.session.commit()

    return user


def update_user(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    api = client.InstagramAPI(access_token=user.access_token,
                              client_secret=CLIENT_SECRET)
    user_data = api.user(user_id)
    if user is None:
        user = models.User(user_data)
        db.session.add(user)
    else:
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
    if tag is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        tag_data = api.tag(tag_name)
        tag = models.Tag(tag_data)
        db.session.add(tag)
        db.session.commit()

    return tag


def init_comment(comment_data):
    comment =\
        db.session.query(models.Comment).filter(models.Comment.inst_id_comment ==
                                                comment_data.id).first()
    if comment is None:
        comment = models.Comment(comment_data=comment_data)
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
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()

    if user is not None:
        api = client.InstagramAPI(access_token=user.access_token,
                                  client_secret=CLIENT_SECRET)
        medias = api.user_recent_media(as_generator=True)
        for case in medias:
            for media_data in case[0]:
                media =\
                    db.session.query(models.Media).filter(models.Media.inst_id_media ==
                                                          media_data.id).first()
                if media is None:
                    media = models.Media(media_data)
                    db.session.add(media)
                    db.session.commit()
                    for comment in media_data.comments:
                        comment_data = init_comment(comment_data=comment)
                        db.session.add(comment_data)
                        db.session.commit()

                        comment_data =\
                            db.session.query(models.Comment).filter(models.Comment.id_comment ==
                                                                    comment_data.id_comment).first()
                        media.comments.append(comment_data)
                        db.session.commit()

        db.session.commit()

def update_user_media(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user is not None:
        api = client.InstagramAPI(access_token=user.access_token,
                                  client_secret=CLIENT_SECRET)
        medias = api.user_recent_media(as_generator=True)
        old_medias = user.medias.all()
        new_medias = []
        for case in medias:
            for media_data in case[0]:
                media =\
                    db.session.query(models.Media).filter(models.Media.inst_id_media ==
                                                          media_data.id).first()
                if media is None:
                    media = models.Media(media_data)
                    db.session.add(media)
                    db.session.commit()
                    for comment in media_data.comments:
                        comment_data = init_comment(comment_data=comment)
                        db.session.add(comment_data)
                        db.session.commit()
                        media.comments.append(comment_data)
                        db.session.commit()
                else:
                    if media_data.caption:
                        media.caption = media_data.caption.text
                    media.count_of_likes = media_data.like_count
                    if ('location' in dir(media_data)) and (media_data.location.id is not '0'):
                        new_location = init_location(media_data.location.id)
                    else:
                        new_location = None
                    media.location = new_location
                    db.session.commit()

                    likes = api.media_likes(media_id=media_data.id)
                    new_likes = []
                    for like in likes:
                        new_likes.append(init_user_by_information(like))
                    media.liked_by = new_likes
                    db.session.commit()

                    new_tags = []
                    if 'tags' in dir(media_data):
                        for tag in media_data.tags:
                            new_tags.append(init_tag(tag.name))
                    media.tags = new_tags
                    db.session.commit()

                    new_comments = []
                    old_comments = media.comments.all()
                    for comment_data in media_data.comments:
                        new_comments.append(init_comment(comment_data))
                    media.comments = new_comments
                    db.session.commit()
                    to_delete = set(old_comments) - set(new_comments)
                    for comment in to_delete:
                        db.session.delete(comment)
                    db.session.commit()

                new_medias.append(media)

        to_delete = set(old_medias) - set(new_medias)
        for media in to_delete:
            db.session.delete(media)
        db.session.commit()

        db.session.commit()


def get_users_who_liked(user_id):
    user_temp =\
       db.session.query(models.User).filter(models.User.inst_id_user ==
                                            user_id).first()
    medias = user_temp.medias.all()
    users_who_liked = {}
    sum_of_likes = 0
    for media in medias:
        for user in media.liked_by:
            if user not in users_who_liked:
                users_who_liked[user] = 1
            else:
                users_who_liked[user] += 1
            sum_of_likes += 1
    users_who_liked = users_who_liked.items()
    users_who_liked.sort(key=lambda x: (-x[1], x[0].login))
    liker_count = len(users_who_liked)
    return users_who_liked, sum_of_likes, liker_count


def get_most_liked_media(user_id):
    user_temp =\
       db.session.query(models.User).filter(models.User.inst_id_user ==
                                            user_id).first()
    most_liked_media = user_temp.medias.all()
    most_liked_media.sort(key=lambda x: -x.count_of_likes)
    return most_liked_media


def get_user_tags(user_id):
    user_temp =\
       db.session.query(models.User).filter(models.User.inst_id_user ==
                                            user_id).first()
    medias = user_temp.medias.all()
    user_tags = {}
    tag_count_all = 0
    for media in medias:
        for tag in media.tags:
            if tag not in user_tags:
                user_tags[tag] = 1
            else:
                user_tags[tag] += 1
            tag_count_all += 1
    user_tags = user_tags.items()
    user_tags.sort(key=lambda x: (-x[1], x[0].name))
    tag_count_unique = len(user_tags)
    return user_tags, tag_count_all, tag_count_unique