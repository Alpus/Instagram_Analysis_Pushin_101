# -*- coding: utf-8 -*-
from app import db
import requests
from instagram import client

CLIENT_ID = requests.CLIENT_ID
CLIENT_SECRET = requests.CLIENT_SECRET
LOGGED_URL = requests.LOGGED_URL
HOME_URL = requests.HOME_URL
REDIRECT_URL = requests.REDIRECT_URL


class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id_user = db.Column(db.Integer, primary_key=True,
                        autoincrement=True)
    inst_id_user = db.Column(db.String(50), nullable=False)
    access_token = db.Column(db.String(100))
    login = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100))
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.String(100))
    website = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime)
    last_visit = db.Column(db.DateTime)
    last_check = db.Column(db.DateTime)
    rating = db.Column(db.Integer, nullable=False, default=0)
    count_media = db.Column(db.Integer, nullable=False, default=0)
    count_follows = db.Column(db.Integer, nullable=False, default=0)
    count_followed_by = db.Column(db.Integer, nullable=False, default=0)

    medias = db.relationship(
        'Media', backref='user', lazy='dynamic')
    comments = db.relationship(
        'Comment', backref='user', lazy='dynamic')
    follows = db.relationship('User', secondary='follows',
        primaryjoin='User.id_user==follows.c.id_user_from',
        secondaryjoin='User.id_user==follows.c.id_user_to',
        backref='followed_by', lazy='dynamic')

    def __init__(self, user_data):
        self.inst_id_user = user_data.id
        self.login = user_data.username
        self.full_name = user_data.full_name
        self.profile_picture = user_data.profile_picture

        if 'bio' in dir(user_data):
            self.bio = user_data.bio
        else:
            self.bio = None

        if 'website' in dir(user_data):
            self.website = user_data.website
        else:
            self.website = None

        if 'counts' in dir(user_data):
            self.count_media = user_data.counts['media']
            self.count_follows = user_data.counts['follows']
            self.count_followed_by = user_data.counts['followed_by']

    def __repr__(self):
        return '<User %r>' % self.login


follows = db.Table('follows',
                 db.Column('id_user_from', db.Integer, db.ForeignKey('Users.id_user')),
                 db.Column('id_user_to', db.Integer, db.ForeignKey('Users.id_user'))
                 )


class Media(db.Model):
    __tablename__ = 'Medias'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_media = db.Column(db.Integer, primary_key=True,
                         autoincrement=True)
    inst_id_media = db.Column(db.String(50), nullable=False)
    type_media = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.String(100))
    count_of_likes = db.Column(db.Integer, default=0)
    filter_media = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    image_low = db.Column(db.String(255), nullable=False)
    image_thumbnail = db.Column(db.String(255), nullable=False)
    image_standard = db.Column(db.String(255), nullable=False)

    id_user = db.Column(db.Integer, db.ForeignKey('Users.id_user'))
    id_location = db.Column(db.Integer,
                            db.ForeignKey('Locations.id_location'))

    comments = db.relationship(
        'Comment', backref='media', lazy='dynamic')

    liked_by = db.relationship(
        'User', secondary='likes',
        backref=db.backref('liked_media', lazy='dynamic'))
    users_in_media = db.relationship(
        'User', secondary='marks',
        backref=db.backref('media_with_user', lazy='dynamic'))
    tags = db.relationship(
        'Tag', secondary='media_tags',
        backref=db.backref('medias_with_tag', lazy='dynamic'))

    def __init__(self, media_data):
        self.inst_id_media = media_data.id
        self.type_media = media_data.type
        if media_data.caption:
            self.caption = media_data.caption.text
        self.count_of_like = media_data.like_count
        self.filter_media = media_data.filter
        self.link = media_data.link
        self.created_time = media_data.created_time
        self.image_low = media_data.images['low_resolution'].url
        self.image_thumbnail = media_data.images['thumbnail'].url
        self.image_standard = media_data.images['standard_resolution'].url

        new_user = requests.init_user_by_id(media_data.user.id)
        self.user = new_user

        if ('location' in dir(media_data)) and (media_data.location.id is not '0'):
            new_location = requests.init_location(media_data.location.id)
        else:
            new_location = None
        self.location = new_location

        api = client.InstagramAPI(access_token=self.user.access_token,
                                  client_secret=CLIENT_SECRET)
        likes = api.media_likes(media_id=media_data.id)
        for like in likes:
            user = requests.init_user_by_data(like)
            self.liked_by.append(user)

        if 'tags' in dir(media_data):
            for tag in media_data.tags:
                tag_data = requests.init_tag(tag.name)
                self.tags.append(tag_data)

        for comment_data in media_data.comments:
            comment = requests.init_comment_by_data(comment_data)
            self.comments.append(comment)

    def __repr__(self):
        return '<Media %r>' % self.id_media


likes = db.Table('likes',
                 db.Column('id_media', db.Integer, db.ForeignKey('Medias.id_media')),
                 db.Column('id_user', db.Integer, db.ForeignKey('Users.id_user'))
                 )

marks = db.Table('marks',
                 db.Column('id_media', db.Integer, db.ForeignKey('Medias.id_media')),
                 db.Column('id_user', db.Integer, db.ForeignKey('Users.id_user'))
                 )


class Comment(db.Model):
    __tablename__ = 'Comments'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_comment = db.Column(db.Integer, primary_key=True,
                           autoincrement=True)
    inst_id_comment = db.Column(db.String(50), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.String(255), nullable=False)

    id_media = db.Column(db.Integer,
                         db.ForeignKey('Medias.id_media'))
    id_user = db.Column(db.Integer,
                        db.ForeignKey('Users.id_user'))

    def __init__(self, comment_data):
        self.inst_id_comment = comment_data.id
        self.created_time = comment_data.created_at
        self.text = comment_data.text
        user = db.session.query(User).filter(User.inst_id_user
                                             == comment_data.user.id).first()
        self.user = user

    def __repr__(self):
        return '<Comment %r>' % self.id_comment


class Tag(db.Model):
    __tablename__ = 'Tags'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_tag = db.Column(db.Integer, primary_key=True,
                       autoincrement=True)
    count = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Unicode(255), nullable=False)

    def __init__(self, tag_data):
        self.count = tag_data.media_count
        self.name = tag_data.name

    def __repr__(self):
        return '<Tag %r>' % self.id_tag


media_tags = db.Table('media_tags',
                      db.Column('id_media', db.Integer, db.ForeignKey('Medias.id_media')),
                      db.Column('id_tag', db.Integer, db.ForeignKey('Tags.id_tag'))
                      )


class Location(db.Model):
    __tablename__ = 'Locations'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_location = db.Column(db.Integer, primary_key=True,
                            autoincrement=True)
    inst_id_location = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    medias = db.relationship(
        'Media', backref='location', lazy='dynamic')

    def __init__(self, location_data):
        self.inst_id_location = location_data.id
        self.name = location_data.name
        self.latitude = location_data.point.latitude
        self.longitude = location_data.point.longitude

    def __repr__(self):
        return '<Location %r>' % self.id_location
