"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)

@app.get('/')
def redirect_to_users():
    '''redirects to users page'''
    return redirect('/users')

@app.get('/users')
def get_users_list():
    '''Gets users list'''
    users = User.query.all()
    return render_template('users.html', users=users)

@app.get('/users/new')
def show_add_user_form():
    '''Shows the add users form'''
    return render_template('new_user.html')

@app.post('/users/new')
def add_new_user():
    '''Takes data from form, adds new user and redirects to /users'''
    fname = request.form['fname']
    lname = request.form['lname']
    img_url = request.form["image_url"]
    img_url = str(img_url) if img_url else None

    user = User(fname=fname, lname=lname, img_url=img_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')


