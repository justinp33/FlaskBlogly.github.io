"""Models for Blogly."""

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


    def __repr__(self):
        u = self
        return f"<User id={u.id} First Name={u.first_name} Last Name={u.last_name} Image={u.image_url}>"

        

    

