#!flask/bin/python2.7
# -*- coding: utf-8 -*-
from app import app
from app import users_updater


app.run(debug=True, port=5000)