# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import UniqueConstraint
import datetime

class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    id_user = db.Column(db.String(100), nullable=False, primary_key=True)
    access_token = db.Column(db.String(100))
    login = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100))
    profile_picture = db.Column(db.String(500))
    bio = db.Column(db.String(100))
    website = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime)
    last_visit = db.Column(db.DateTime)
    last_check = db.Column(db.DateTime)
    rating = db.Column(db.Integer, nullable=False, default=0)
    count_media = db.Column(db.Integer, nullable=False, default=0)
    count_follows = db.Column(db.Integer, nullable=False, default=0)
    count_followed_by = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, id_user, login, full_name,
        profile_picture, bio, website, count_media, count_follows,
        last_check):
        self.id_user = id_user
        self.login = login
        self.full_name = full_name
        self.profile_picture = profile_picture
        self.bio = bio
        self.website = website
        self.count_media = count_media
        self.count_follows = count_follows
        self.count_followed_by = count_followed_by
        self.last_check = last_check


    def __repr__(self):
        return '<User %r>' % self.login