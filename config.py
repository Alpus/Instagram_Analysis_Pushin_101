#!flask/bin/python
# -*- coding: utf-8 -*-

# Server
CSRF_ENABLED = True
SECRET_KEY = 'Pty1Ruz78LmG4jD8lAI36Fs'

# Database
import os
basedir = os.path.abspath(os.path.dirname(__file__))

STATIC_FOLDER = os.path.join(basedir, 'app', 'static')
SQLALCHEMY_DATABASE_URI = 'mysql://alpus:Qwe61283888@localhost/db'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
CELERY_BROKER_URL='redis://localhost:6379',
CELERY_RESULT_BACKEND='redis://localhost:6379'
