"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class USER(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                     nullable=False)
                     
    last_name = db.Column(db.String(50),
                     nullable=False)

    image_url = db.Column(db.String)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


    def __repr__(self):
        u = self
        return f"<User id={u.id} First Name={u.first_name} Last Name={u.last_name} Image={u.image_url}>"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(50), nullable = False)

    content = db.Column(db.String, nullable = False)

    created_at = db.Column(db.DateTime,nullable=False,
        default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        

    

