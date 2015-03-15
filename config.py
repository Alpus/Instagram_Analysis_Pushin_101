CSRF_ENABLED = True
SECRET_KEY = 'nobodyknow'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://alpus:Qwe61283888@localhost/db'