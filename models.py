"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
        db.String(100),
        nullable = False,
        default = 'https://pbs.twimg.com/profile_images/1237550450/mstom_400x400.jpg'
    )