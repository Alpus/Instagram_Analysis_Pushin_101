# -- coding: utf-8 --
from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('base.html')

    
@app.route('/<username>')
def show_user_profile(username):
    return render_template('base.html', username=username)
