# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import UniqueConstraint
import datetime

class User(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_user = db.Column(db.Integer(), db.ForeignKey('inst_profile.id_profile'),
                        nullable=False, primary_key=True)
    access_token = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime, nullable=False)
    last_visit = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, id_user, access_token, registration_date):
        self.id_user = id_user
        self.access_token = access_token
        self.registration_date = registration_date
        self.last_visit = registration_date

    def __repr__(self):
        return '<User %r>' % self.id_user


class InstProfile(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_profile = db.Column(db.Integer, nullable=False, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(100))
    bio = db.Column(db.String(100))
    website = db.Column(db.String(100))
    #post_count = db.Column(db.Integer, unsigned=True, nullable=False)
    #followers_count = db.Column(db.Integer, unsigned=True, nullable=False)
    #following_count = db.Column(db.Integer, unsigned=True, nullable=False)
    #given_like = db.Column(db.Integer, unsigned=True)
    #get_like = db.Column(db.Integer, unsigned=True)
    #given_comment = db.Column(db.Integer, unsigned=True)
    #get_comment = db.Column(db.Integer, unsigned=True)
    #marked_count = db.Column(db.Integer, unsigned=True)
    last_check = db.Column(db.DateTime, nullable=False,
                              default=datetime.date(1000, 1, 1))

    user = db.relationship('User', uselist=False, backref='inst_profile', lazy='dynamic')
    followers = db.relationship('InstProfile', secondary='follows',
        primaryjoin='InstProfile.id_profile==follows.c.id_follower',
        secondaryjoin='InstProfile.id_profile==follows.c.id_following',
        backref='following', lazy='dynamic')
    words = db.relationship('Word', secondary='profile_words',
        backref='inst_profiles', lazy='dynamic')
    geos = db.relationship('Geo', secondary='profile_geos',
        backref='inst_profiles', lazy='dynamic')
    posts = db.relationship('Post', backref='ints_profile', lazy='dynamic')
    filters = db.relationship('Filter', secondary='profile_filters',
        backref='inst_profiles', lazy='dynamic')
    usermarks = db.relationship('InstProfile', secondary='usermarks',
        primaryjoin='InstProfile.id_profile==usermarks.c.id_profile',
        secondaryjoin='InstProfile.id_profile==usermarks.c.id_mark',
        backref='usermark_makers', lazy='dynamic')

    def __init__(self, id_profile, login, full_name):
        self.id_profile = id_profile
        self.login = login
        self.full_name = full_name

    def __repr__(self):
        return '<InstProfile %r>' % self.login


follows = db.Table('follows',
    db.Column('id_follower', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              nullable=False),
    db.Column('id_following', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              nullable=False),
    UniqueConstraint('id_follower', 'id_following'),

    db.Column('given_like', db.Integer),
    db.Column('given_comment', db.Integer),
    db.Column('last_check', db.DateTime, nullable=False,
                              default=datetime.date(1000, 1, 1)))


class Geo(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_geo = db.Column(db.Integer, nullable=False, primary_key=True)
    geo_name = db.Column(db.String(100), nullable=False, unique=True)
    #using_count = db.Column(db.Integer, unsigned=True)
    #get_like = db.Column(db.Integer, unsigned=True)
    #get_comment = db.Column(db.Integer, unsigned=True)

    def __init__(self, id_geo, geo_name):
        self.id_geo = id_geo
        self.geo_name = geo_name

    def __repr__(self):
        return '<Geo %r>' % self.id_geo


profile_geos = db.Table('profile_geos',
    db.Column('id_profile', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              nullable=False),
    db.Column('id_geo', db.Integer, db.ForeignKey('geo.id_geo'),
               nullable=False),
    UniqueConstraint('id_profile', 'id_geo'),

    db.Column('using_count', db.Integer),
    db.Column('get_like', db.Integer),
    db.Column('get_comment', db.Integer))


class Word(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_word = db.Column(db.Integer, nullable=False, primary_key=True,
                        autoincrement=True)
    word_name = db.Column(db.String(100), nullable=False, unique=True)
    #using_count = db.Column(db.Integer, unsigned=True)
    #get_like = db.Column(db.Integer, unsigned=True)
    #get_comment = db.Column(db.Integer, unsigned=True)

    meanings = db.relationship('Meaning', secondary='word_meanings',
        backref='words', lazy='dynamic')

    def __init__(self, word_name):
        self.word_name = word_name

    def __repr__(self):
        return '<Word %r>' % self.id_word


profile_words = db.Table('profile_words',
    db.Column('id_profile', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              nullable=False),
    db.Column('id_word', db.Integer, db.ForeignKey('word.id_word'),
              nullable=False),

    db.Column('using_count', db.Integer),
    db.Column('get_like', db.Integer),
    db.Column('get_comment', db.Integer),
    db.Column('is_tag', db.Boolean, nullable=False, default=False),
    UniqueConstraint('id_profile', 'id_word', 'is_tag'))


class Meaning(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_meaning = db.Column(db.Integer, nullable=False, primary_key=True,
                           autoincrement=True)
    meaning_name = db.Column(db.String(100), nullable=False, unique=True)
    #using_count = db.Column(db.Integer, unsigned=True)
    #get_like = db.Column(db.Integer, unsigned=True)
    #get_comment = db.Column(db.Integer, unsigned=True)

    def __init__(self, id_meaning, meaning_name):
        self.id_meaning = id_meaning
        self.meaning_name = meaning_name

    def __repr__(self):
        return '<Meaning %r>' % self.id_meaning


word_meanings = db.Table('word_meanings',
    db.Column('id_word', db.Integer, db.ForeignKey('word.id_word'),
              nullable=False),
    db.Column('id_mean', db.Integer, db.ForeignKey('meaning.id_meaning'),
              nullable=False),
    UniqueConstraint('id_word', 'id_mean'),

    db.Column('importance', db.Integer, nullable=False, default=0))


class Post(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_post = db.Column(db.Integer, nullable=False, primary_key=True)
    id_profile = db.Column(db.Integer, db.ForeignKey('inst_profile.id_profile'),
        nullable=False)
    UniqueConstraint('id_post', 'id_profile')

    get_like = db.Column(db.Integer)
    get_comment = db.Column(db.Integer)
    img_url = db.Column(db.String(100), nullable=False, unique=True)
    filter = db.Column(db.String(100), nullable=False)
    last_check = db.Column(db.DateTime, nullable=False,
                              default=datetime.date(1000, 1, 1))

    def __init__(self, id_post, id_profile, img_url, filter):
        self.id_post = id_post
        self.id_profile = id_profile
        self.img_url = img_url
        self.filter = filter


    def __repr__(self):
        return '<Posts %r>' % self.id_post


class Filter(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_filter = db.Column(db.Integer, nullable=False, primary_key=True,
                        autoincrement=True)
    filter_name = db.Column(db.String(100), nullable=False, unique=True)
    #using_count = db.Column(db.Integer, unsigned=True)
    #get_like = db.Column(db.Integer, unsigned=True)
    #get_comment = db.Column(db.Integer, unsigned=True)

    def __init__(self, filter_name):
        self.filter_name = filter_name

    def __repr__(self):
        return '<Filter %r>' % self.id_filter


profile_filters = db.Table('profile_filters',
    db.Column('id_profile', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              nullable=False),
    db.Column('id_filter', db.Integer, db.ForeignKey('filter.id_filter'),
              nullable=False),
    UniqueConstraint('id_profile', 'id_filter'),

    db.Column('using_count', db.Integer),
    db.Column('get_like', db.Integer),
    db.Column('get_comment', db.Integer))


usermarks = db.Table('profile_usermarks',
    db.Column('id_profile', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              nullable=False),
    db.Column('id_mark', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              nullable=False),
    UniqueConstraint('id_profile', 'id_mark'),

    db.Column('using_count', db.Integer),
    db.Column('get_like', db.Integer),
    db.Column('get_comment', db.Integer))
