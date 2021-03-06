import bcrypt
from flask import current_app
from blogApp import db, login_manager, bcrypt
from datetime import datetime
from flask_login import UserMixin
import jwt
from time import time


# helper table for many-to-many relation between tags and blogs
blogtags = db.Table('blogtags',
                    db.Column('blogid', db.Integer, db.ForeignKey(
                        'blogs.id'), primary_key=True),
                    db.Column('tagid', db.Integer, db.ForeignKey(
                        'tags.id'), primary_key=True)
                    )


# adding Flask-Login module
@login_manager.user_loader
def load_user(user_id):
    return Authors.query.get(int(user_id))


class Authors(db.Model, UserMixin):
    """database model for authors/users"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    about = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False,
                           default='double1.jpg')
    password = db.Column(db.String(60), nullable=False)
    blogs = db.relationship('Blogs', backref='author', lazy=True)

    def __repr__(self):
        return "User(name : {}, email : {})".format(self.name, self.email)

    def set_password(self, password):
        """Sets passwords to Author object

        Parameters
        ----------
        password : str
        """
        self.password = bcrypt.generate_password_hash(
            password)  # saves password as hash

    def check_password(self, password):
        """Verifies if password of Author object and password match.
        Return True if matched, else returns False

        Parameters
        ----------
        password : str
        """
        return bcrypt.check_password_hash(self.password, password)

    def get_password_reset_token(self, expire_in=3600):
        """Returns encoded JSON Web Token

        Paramaters
        ----------
        expire_in : int time in seconds after which token should expire
        """
        token = jwt.encode({'password_reset': self.id, 'exp': time(
        )+expire_in}, current_app.config['SECRET_KEY'], algorithm='HS256')

        return token

    @staticmethod
    def verify_password_reset_token(token):
        """Decode and verify token

        Parameters
        ----------
        token : str encoded JSON Web Token
        """
        try:
            # decode token and get value of key password_key
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')[
                'password_reset']
            pass
        except:
            return
        return Authors.query.get(id)


class Blogs(db.Model):
    """database model for blogs/posts"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text)
    _created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    thumbnail = db.Column(db.String(20), nullable=False, default='thumb.jpg')
    authorid = db.Column(db.Integer, db.ForeignKey(
        'authors.id'), nullable=False)
    tags = db.relationship('Tags', secondary=blogtags,
                           backref=db.backref('blogs', lazy='dynamic'))

    def __repr__(self):
        return "Blog(title : {}, date_created : {})".format(self.title, self._created)


class Tags(db.Model):
    """database model for tags"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "Tag(tag : {})".format(self.name)
