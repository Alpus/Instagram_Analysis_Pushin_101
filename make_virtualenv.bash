#!/bin/bash
sudo pip install virtualenv
sudo virtualenv flask
sudo apt-get install mysql
sudo apt-get install python-dev
sudo apt-get install libmysqlclient-dev 
sudo apt-get install redis-server
sudo apt-get install uwsgi
sudo apt-get install nginx
sudo apt-get install uwsgi-plugin-python

sudo flask/bin/pip install mysql-python
sudo flask/bin/pip install flask
sudo flask/bin/pip install flask-sqlalchemy
sudo flask/bin/pip install sqlalchemy-migrate
sudo flask/bin/pip install python-instagram
sudo flask/bin/pip install flask-celery
sudo flask/bin/pip install flask-redis
sudo flask/bin/pip install flask-WTF

sudo flask/bin/pip install -U mysql-python
sudo flask/bin/pip install -U flask
sudo flask/bin/pip install -U flask-sqlalchemy
sudo flask/bin/pip install -U sqlalchemy-migrate
sudo flask/bin/pip install -U python-instagram
sudo flask/bin/pip install -U flask-celery
sudo flask/bin/pip install -U flask-redis
sudo flask/bin/pip install -U flask-WTF
