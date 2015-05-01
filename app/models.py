# -*- coding: utf-8 -*-
from app import db
import logic
from sqlalchemy import UniqueConstraint
import datetime


class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id_user = db.Column(db.Integer, nullable=False, primary_key=True)
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

    def __init__(self, user_data):
        id_user = int(user_data.id)
        login = user_data.username
        full_name = user_data.full_name
        profile_picture = user_data.profile_picture
        bio = user_data.bio
        website = user_data.website
        count_media = user_data.counts['media']
        count_follows = user_data.counts['follows']
        count_followed_by = user_data.counts['followed_by']

    def __repr__(self):
        return '<User %r>' % self.login


class Media(db.Model):
    __tablename__ = 'Medias'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_media = db.Column(db.Integer, nullable=False, primary_key=True)
    type_media = db.Column(db.String(50), nullable=False)
    caption = db.Column(db.String(100), nullable=False)
    filter_media = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    created_time = db.Column(db.String(50), nullable=False)
    image_low = db.Column(db.String(255), nullable=False)
    image_thumbnail = db.Column(db.String(255), nullable=False)
    image_standart = db.Column(db.String(255), nullable=False)

    id_user = db.Column(db.Integer, db.ForeignKey('Users.id_user'))
    id_location = db.Column(db.Integer,
                            db.ForeignKey('Locations.id_location'))

    liked_by = db.relationship(
        'User', secondary='likes',
        backref=db.backref('liked_media', lazy='dynamic'))
    users_in_media = db.relationship(
        'User', secondary='marks',
        backref=db.backref('media_with_user', lazy='dynamic'))
    comments = db.relationship(
        'Comment', backref='medias', lazy='dynamic')
    tags = db.relationship(
        'Tag', secondary='media_tags',
        backref=db.backref('medias_with_tag', lazy='dynamic'))

    def __init__(self, media_data):
        id_media = int(media_data.id)
        type_media = media_data.type
        caption = media_data.caption['text']
        filter_media = media_data.filter
        link = media_data.link
        created_time = media_data.created_time
        image_low = media_data.images['low_resolution']
        image_thumbnail = media_data.images['thumbnail']
        image_standart = media_data.images['standart_resolution']

        new_user = logic.init_user(int(media_data.user['id']))
        user = new_user
        new_location = logic.init_location(int(media_data.location['id']))
        location = new_location

        for like in media_data.likes['data']:
            user = int(logic.init_user(like['id']))
            self.liked_by.append(user)
        for mark in media_data.users_in_photo:
            user = int(logic.init_user(mark['user']['id']))
            self.users_in_media.append(user)
        for comment in media_data.comments['data']:
            comment_data = logic.init_comment(comment)
            self.comments.append(comment_data)
        for tag in media_data.tags:
            tag_data = logic.init_tag(tag['name'])
            self.tags.append(tag_data)

    def __repr__(self):
        return '<Media %r>' % self.id_post


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
    id_comment = db.Column(db.Integer, nullable=False, primary_key=True)
    created_time = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(255), nullable=False)

    id_media = db.Column(db.Integer,
                         db.ForeignKey('Medias.id_media'))
    id_user = db.Column(db.Integer,
                        db.ForeignKey('Users.id_user'))

    def __init__(self, comment_data):
        id_comment = int(comment_data.id)
        created_time = comment_data.created_time
        text = comment_data.text
        id_user = int(comment_data['from']['id'])

    def __repr__(self):
        return '<Comment %r>' % self.id_post


class Tag(db.Model):
    __tablename__ = 'Tags'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_tag = db.Column(db.Integer, nullable=False, primary_key=True,
                       autoincrement=True)
    count = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, tag_data):
        count = tag_data.media_count
        name = tag_data.name

    def __repr__(self):
        return '<Tag %r>' % self.id_post


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
    id_location = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)

    medias = db.relationship(
        'Media', backref='location', lazy='dynamic')

    def __init__(self, location_data):
        id_location = int(location_data.id)
        name = location_data.name
        latitude = location_data.latitude
        longitude = location_data.longitude

    def __repr__(self):
        return '<Location %r>' % self.id_post
