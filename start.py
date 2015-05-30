#!flask/bin/python2.7
# -*- coding: utf-8 -*-
from app import app
import users_updater


app.run(debug=True, port=5000)
users_updater.update_users_media.delay()