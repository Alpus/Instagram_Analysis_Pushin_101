from pyasn1_modules.rfc1902 import Unsigned32
import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alpus:Qwe61283888@server/db'
db = SQLAlchemy(app)


class User(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_user = db.Column(db.Integer, db.ForeignKey('inst_profile.id_profile'),
                        unsigned=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime, nullable=False,
                                  default=datetime.datetime.now())
    last_visit = db.Column(db.DateTime, nullable=False,
                                  default=datetime.datetime.now())
    rating = db.Column(db.Integer, unsigned=True, nullable=False, default=0)

    def __init__(self, id_user):
        self.id_user = id_user

    def __repr__(self):
        return '<User %r>' % self.id_user


class InstProfile(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_profile = db.Column(db.Integer, unsigned=True, nullable=False, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    post_count = db.Column(db.Integer, unsigned=True, nullable=False)
    followers_count = db.Column(db.Integer, unsigned=True, nullable=False)
    following_count = db.Column(db.Integer, unsigned=True, nullable=False)
    given_like = db.Column(db.Integer, unsigned=True)
    get_like = db.Column(db.Integer, unsigned=True)
    given_comment = db.Column(db.Integer, unsigned=True)
    get_comment = db.Column(db.Integer, unsigned=True)
    marked_count = db.Column(db.Integer, unsigned=True)
    last_check = db.Column(db.DateTime, nullable=False,
                              default=datetime.datetime.now())

    user = db.relationship('User', backref='inst_profile', lazy='dynamic')
    followers = db.relationship('InstProfile', secondary=follows,
        backref='following', lazy='dynamic')
    geos = db.relationship('Geo', secondary=profile_geos,
        backref='int_profiles', lazy='dynamic')

    def __init__(self, id_profile, post_count, followers_count, following_count):
        self.id_profile = id_profile
        self.post_count = post_count
        self.followers_count = followers_count
        self.following_count = following_count

    def __repr__(self):
        return '<InstProfile %r>' % self.login


follows = db.table('follows',
    db.Column('id_follower', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              unsigned=True, nullable=False),
    db.Column('id_following', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              unsigned=True, nullable=False),
    UniqueConstraint('id_follower', 'id_following'),

    given_like = db.Column(db.Integer, unsigned=True),
    given_comment = db.Column(db.Integer, unsigned=True),
    last_check = db.Column(db.DateTime, nullable=False,
                              default=datetime.datetime.now())


class Geo(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_geo = db.Column(db.Integer, unsigned=True, nullable=False, primary_key=True)
    geo_name = db.Column(db.String(100), nullable=False, unique=True)
    using_count = db.Column(db.Integer, unsigned=True)
    get_like = db.Column(db.Integer, unsigned=True)
    get_comment = db.Column(db.Integer, unsigned=True)

    def __init__(self, id_geo, geo_name):
        self.id_geo = id_geo
        self.geo_name = geo_name

    def __repr__(self):
        return '<Geo %r>' % self.id_geo


profile_geos = db.table('profile_geos',
    db.Column('id_profile', db.Integer, db.ForeignKey('inst_profile.id_profile'),
              unsigned=True, nullable=False),
    db.Column('id_geo', db.Integer, db.ForeignKey('geo.id_geo'),
              unsigned=True, nullable=False),
    UniqueConstraint('id_profile', 'id_geo'),

    using_count = db.Column(db.Integer, unsigned=True),
    get_like = db.Column(db.Integer, unsigned=True),
    get_comment = db.Column(db.Integer, unsigned=True))


class Word(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_word = db.Column(db.Integer, unsigned=True, nullable=False, primary_key=True,
                        autoincrement=True)
    word_name = db.Column(db.String(100), nullable=False, unique=True)
    using_count = db.Column(db.Integer, unsigned=True)
    get_like = db.Column(db.Integer, unsigned=True)
    get_comment = db.Column(db.Integer, unsigned=True)

    meanings = db.relationship('Meaning', secondary=word_meanings,
        backref='words', lazy='dynamic')

    def __init__(self, id_word, word_name):
        self.id_word = id_word
        self.word_name = word_name

    def __repr__(self):
        return '<Word %r>' % self.id_word


class Meaning(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id_meaning = db.Column(db.Integer, unsigned=True, nullable=False, primary_key=True,
                           autoincrement=True)
    meaning_name = db.Column(db.String(100), nullable=False, unique=True)
    using_count = db.Column(db.Integer, unsigned=True)
    get_like = db.Column(db.Integer, unsigned=True)
    get_comment = db.Column(db.Integer, unsigned=True)

    def __init__(self, id_meaning, meaning_name):
        self.id_meaning = id_meaning
        self.meaning_name = meaning_name

    def __repr__(self):
        return '<Meaning %r>' % self.id_meaning


word_meanings = db.table('word_meanings',
    db.Column('id_word', db.Integer, db.ForeignKey('word.id_word'),
              unsigned=True, nullable=False),
    db.Column('id_mean', db.Integer, db.ForeignKey('meaning.id_meaning'),
              unsigned=True, nullable=False),
    UniqueConstraint('id_profile', 'id_geo'),

    importance = db.Column(db.Integer, unsigned=True, nullable=False, default=0))