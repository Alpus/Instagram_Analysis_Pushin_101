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
    users = db.relationship('User', backref='user', lazy='dynamic')
    followings = db.relationship('InstProfile', secondary=follows, backref='followings',
                                 lazy='dynamic')
    followers = db.relationship('InstProfile', secondary=follows, backref='followers',
                                 lazy='dynamic')

    def __init__(self, id_profile, post_count, followers_count, following_count):
        self.id_profile = id_profile
        self.post_count = post_count
        self.followers_count = followers_count
        self.following_count = following_count

    def __repr__(self):
        return '<InstProfile %r>' % self.login

follows = db.table('follows',
    db.Column('id_follower', db.Integer, db.ForeignKey('int_profile.id_profile'),
              unsigned=True, nullable=False),
    db.Column('id_following', db.Integer, db.ForeignKey('int_profile.id_profile'),
              unsigned=True, nullable=False),
    UniqueConstraint('id_follower', 'id_following'),

    given_like = db.Column(db.Integer, unsigned=True),
    given_comment = db.Column(db.Integer, unsigned=True),
    last_check = db.Column(db.DateTime, nullable=False,
                              default=datetime.datetime.now())

