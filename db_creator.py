#!flask/bin/python
# -- coding: utf-8 --
from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path
db.create_all()