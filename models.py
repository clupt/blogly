"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://pbs.twimg.com/profile_images/1237550450/mstom_400x400.jpg'

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User.'''

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    fname = db.Column(
        db.String(20),
        nullable=False)

    lname = db.Column(
        db.String(20),
        nullable=False)

    img_url = db.Column(
        db.String(500),
        nullable = False,
        default = DEFAULT_IMAGE_URL)
    
    # relationship defined for direct naviagtion user -> posts and back


class Post(db.Model):
    '''Post.'''

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)  

    title = db.Column(
        db.String(80),
        nullable=False)

    content = db.Column(
        db.Text,
        nullable = False) 

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = db.func.now)

    user_id = db.Column(
        db.Integer,
        db. ForeignKey('users.id'),
        nullable = False)
    
    user = db.relationship('User', backref="posts")
