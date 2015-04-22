#!/bin/bash
sudo pip install virtualenv
sudo virtualenv flask
sudo apt-get install mysql
sudo apt-get install python-dev
sudo apt-get install libmysqlclient-dev 
sudo flask/bin/pip install mysql-python
sudo flask/bin/pip install flask
sudo flask/bin/pip install flask-sqlalchemy
sudo flask/bin/pip install flask-bootstrap
sudo flask/bin/pip install sqlalchemy-migrate
sudo flask/bin/pip install python-instagram
