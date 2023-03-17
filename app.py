"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    img_url = request.form["img_url"]
    img_url = img_url if img_url else None

    user = User(fname=fname, lname=lname, img_url=img_url)
    db.session.add(user)
    db.session.commit() ## flash a message "new user added" and check for it in testing
    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_page(user_id):
    """Takes user ID and shows the user's page"""
    user = User.query.get_or_404(user_id)
    posts_from_user = user.posts

    return render_template(
        "detail.html",
        user = user,
        posts =  posts_from_user
    )

@app.get('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Show edit page for specific user_id"""
    user = User.query.get_or_404(user_id)

    return render_template(
        "edit.html",
        user = user
    )

@app.post('/users/<int:user_id>/edit')
def update_user_profile(user_id):
    """Update specific user instance with form data"""
    user = User.query.get_or_404(user_id)

    user.fname = request.form['fname']
    user.lname = request.form['lname']
    user.img_url = request.form['img_url']

    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.post('/users/<int:user_id>/delete')
def delete_user_profile(user_id):
    """Remove user from database"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

################################################################################
# Post Routes

@app.get('/users/<int:user_id>/posts/new')
def show_form_for_new_post(user_id):
    """Shows the form to add a post for that user"""

    user = User.query.get_or_404(user_id)

    return render_template("new_post.html", user=user)

@app.post('/users/<int:user_id>/posts/new')
def handle_add_post_form(user_id):
    """Adds post and redirects to the user detail page"""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post!"""

    post = Post.query.get(post_id) #or 404
    return render_template("post_detail.html", post=post)

@app.get('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show edit post form!"""

    post = Post.query.filter_by(id=post_id).all() # should use get_or_404 for vars from url
    return render_template("edit_post.html", post=post[0])

@app.post('/posts/<int:post_id>/edit')
def handle_editing_post(post_id):
    """Handles the editing of a post and redirects to the post view"""
    post = Post.query.filter_by(id=post_id).all() #get or 404
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.post('/posts/<int:post_id>/delete')
def delete_a_post(post_id):
    """Deletes a post from the posts list"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')
