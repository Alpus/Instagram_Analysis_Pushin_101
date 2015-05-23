from instagram import client
from app import db
import models
import datetime
from app import celery

CLIENT_ID = '448cfab22275478a9e475784fe8ed4f1'
CLIENT_SECRET = '95e26a3bd94f44c78a534bc8c8a6bacc'
LOGGED_URL = '/logged'
HOME_URL = 'http://54.149.115.96'
REDIRECT_URL = HOME_URL + LOGGED_URL

dbsession = db.session


@celery.task()
def process_login(code):
    instagram_client = client.InstagramAPI(client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri=REDIRECT_URL)
    access_token, instagram_user =\
        instagram_client.exchange_code_for_access_token(code)

    that_user = init_user_by_id(instagram_user['id'])

    that_user.registration_date = datetime.datetime.now()
    that_user.last_visit = datetime.datetime.now()
    that_user.access_token = access_token
    dbsession.commit()

    return that_user.inst_id_user

s
@celery.task()
def init_user_by_id(user_id):
    user =\
        dbsession.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user is None:
        api = client.InstagramAPI(access_token=user.access_token,
                              client_secret=CLIENT_SECRET)
        user_data = api.user(user_id)
        user = models.User(user_data=user_data)
        dbsession.add(user)
        dbsession.commit()

    return user


@celery.task()
def init_user_by_data(user_data):
    user =\
        dbsession.query(models.User).filter(models.User.inst_id_user ==
                                             user_data.id).first()
    if user is None:
        user = models.User(user_data=user_data)
        dbsession.add(user)
        dbsession.commit()

    return user


@celery.task()
def update_user(user_id):
    user =\
        dbsession.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    api = client.InstagramAPI(access_token=user.access_token,
                              client_secret=CLIENT_SECRET)
    user_data = api.user(user_id)
    if user is None:
        user = models.User(user_data)
        dbsession.add(user)
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

    dbsession.commit()
    return user


@celery.task()
def init_tag(tag_name):
    tag =\
        dbsession.query(models.Tag).filter(models.Tag.name ==
                                            tag_name).first()
    if tag is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        tag_data = api.tag(tag_name)
        tag = models.Tag(tag_data)
        dbsession.add(tag)
        dbsession.commit()

    return tag


@celery.task()
def init_comment_by_data(comment_data):
    comment =\
        dbsession.query(models.Comment).filter(models.Comment.inst_id_comment ==
                                                comment_data.id).first()
    if comment is None:
        comment = models.Comment(comment_data=comment_data)
        dbsession.add(comment)
        dbsession.commit()

    return comment


@celery.task()
def init_location(location_id):
    location =\
        dbsession.query(models.Location).filter(models.Location.id_location ==
                                                 location_id).first()
    if location is None:
        api = client.InstagramAPI(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)
        location_data = api.location(location_id)
        location = models.Location(location_data)
        dbsession.add(location)
        dbsession.commit()

    return location


@celery.task()
def update_user_media(user_id):
    user =\
        dbsession.query(models.User).filter(models.User.inst_id_user ==
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
                    dbsession.query(models.Media).filter(models.Media.inst_id_media ==
                                                          media_data.id).first()
                if media is None:
                    media = models.Media(media_data)
                    dbsession.add(media)
                    dbsession.commit()
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
                    dbsession.commit()

                    likes = api.media_likes(media_id=media_data.id)
                    new_likes = []
                    for like in likes:
                        new_likes.append(init_user_by_data(like))
                    media.liked_by = new_likes
                    dbsession.commit()

                    new_tags = []
                    if 'tags' in dir(media_data):
                        for tag in media_data.tags:
                            new_tags.append(init_tag(tag.name))
                    media.tags = new_tags
                    dbsession.commit()

                    new_comments = []
                    old_comments = media.comments.all()
                    for comment_data in media_data.comments:
                        new_comments.append(init_comment_by_data(comment_data))
                    media.comments = new_comments
                    dbsession.commit()
                    to_delete = set(old_comments) - set(new_comments)
                    for comment in to_delete:
                        dbsession.delete(comment)
                    dbsession.commit()

                new_medias.append(media)

        to_delete = set(old_medias) - set(new_medias)
        for media in to_delete:
            dbsession.delete(media)
        dbsession.commit()


@celery.task()
def update_user_follows(user_id):
    user =\
        dbsession.query(models.User).filter(models.User.inst_id_user ==
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

        dbsession.commit()

@celery.task()
def update_user_followed_by(user_id):
    user =\
        dbsession.query(models.User).filter(models.User.inst_id_user ==
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

        dbsession.commit()
