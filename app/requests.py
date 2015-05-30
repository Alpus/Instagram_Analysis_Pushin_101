from instagram.bind import InstagramAPIError
from instagram import client
from app import db
import models
import datetime
from app import celery
import sys

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

    that_user = init_user_by_id(instagram_user['id'])

    if that_user.registration_date == None:
        that_user.registration_date = datetime.datetime.now()
    that_user.last_visit = datetime.datetime.now()
    that_user.access_token = access_token
    db.session.commit()

    return that_user.inst_id_user, that_user.login


def init_user_by_id(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user is None:
        api = client.InstagramAPI(access_token=user.access_token,
                              client_secret=CLIENT_SECRET)
        user_data = api.user(user_id)
        user = models.User(user_data=user_data)
        db.session.add(user)
        db.session.commit()

    return user


def init_user_by_data(user_data):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_data.id).first()
    if user is None:
        user = models.User(user_data=user_data)
        db.session.add(user)
        db.session.commit()
    else:
        user.inst_id_user = user_data.id
        user.login = user_data.username
        user.full_name = user_data.full_name
        user.profile_picture = user_data.profile_picture

        if 'bio' in dir(user_data):
            user.bio = user_data.bio
        else:
            user.bio = None

        if 'website' in dir(user_data):
            user.website = user_data.website
        else:
            user.website = None

        if 'counts' in dir(user_data):
            user.count_media = user_data.counts['media']
            user.count_follows = user_data.counts['follows']
            user.count_followed_by = user_data.counts['followed_by']
            
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

    db.session.commit()
    return user


def init_tag(tag_name):
    try:
        tag =\
        db.session.query(models.Tag).filter(models.Tag.name ==
                                            tag_name).first()
    except:
        tag = None

    if tag is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        try:
            tag_data = api.tag(tag_name)
            tag = models.Tag(tag_data)
            db.session.add(tag)
            db.session.commit()
        except InstagramAPIError as error:
            tag = None

    return tag


def init_comment_by_data(comment_data):
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
        db.session.query(models.Location).filter(models.Location.inst_id_location ==
                                                 location_id).first()
    if location is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        location_data = api.location(location_id)
        location = models.Location(location_data)
        db.session.add(location)
        db.session.commit()

    return location


@celery.task()
def update_user_media(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()

    if user is not None:
        api = client.InstagramAPI(access_token=user.access_token,
                                  client_secret=CLIENT_SECRET)
        medias = api.user_recent_media(as_generator=True, max_pages=None)
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
                else:
                    if media_data.caption:
                        media.caption = media_data.caption.text
                    else:
                        media.caption = None
                    media.count_of_likes = media_data.like_count
                    if ('location' in dir(media_data)) and (media_data.location.id is not '0'):
                        media.location = init_location(media_data.location.id)
                    else:
                        media.location = None
                    db.session.commit()

                    likes = api.media_likes(media_id=media_data.id)
                    new_likes = []
                    for like in likes:
                        new_likes.append(init_user_by_data(like))
                    media.liked_by = new_likes
                    db.session.commit()

                    new_tags = []
                    if 'tags' in dir(media_data):
                        for tag in media_data.tags:
                            tag = init_tag(tag.name)
                            if tag is not None:
                                new_tags.append(tag)
                    media.tags = new_tags
                    db.session.commit()

                    new_comments = []
                    old_comments = media.comments.all()
                    for comment_data in media_data.comments:
                        new_comments.append(init_comment_by_data(comment_data))
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

    user.last_check = datetime.datetime.now()
    user.is_media_on_update = False
    db.session.commit()


def update_user_follows(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                              user_id).first()
    if user is not None:
        api = client.InstagramAPI(access_token=user.access_token,
                                  client_secret=CLIENT_SECRET)
        follows = api.user_follows(as_generator=True, max_pages=None)
        new_follows = []
        for case in follows:
            for follow in case[0]:
                follow_user = init_user_by_data(follow)
                new_follows.append(follow_user)
        user.follows = new_follows

        db.session.commit()


def update_user_followed_by(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                              user_id).first()
    if user is not None:
        api = client.InstagramAPI(access_token=user.access_token,
                                  client_secret=CLIENT_SECRET)
        followed_by_list = api.user_followed_by(as_generator=True, max_pages=None)
        new_followed_by = []
        for case in followed_by_list:
            for followed_by in case[0]:
                followed_by_user = init_user_by_data(followed_by)
                new_followed_by.append(followed_by_user)
        user.followed_by = new_followed_by

        db.session.commit()


def clear_extra_locations():
    locations = db.session.query(models.Location).filter(models.Location.medias
                                                         == None)
    for location in locations:
        db.session.delete(location)

    db.session.commit()


def update_all_user_information(user_id):
    user = db.session.query(models.User).filter(models.User.inst_id_user ==
                                                user_id).first()
    if user.last_check is None:
        user.last_check = datetime.date(year=1814, month=7, day=19)
        db.session.commit()
    if user.is_media_on_update is False and datetime.datetime.now() - user.last_check > datetime.timedelta(hours=24):
        user.is_media_on_update = True;
        db.session.commit()
        update_user_media.delay(user_id)
        update_user(user_id)
        update_user_followed_by(user_id)
        update_user_follows(user_id)

def is_access_token_valid(user_id):
    user =\
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user.access_token is None:
        return False
    else:
        try:
           api = client.InstagramAPI(access_token=user.access_token,
                                  client_secret=CLIENT_SECRET)
           user_data = api.user(user_id)
        except InstagramAPIError:
               user.access_token = None
               db.session.commit()
               return False

    return True