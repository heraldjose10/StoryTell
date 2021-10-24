from flask import current_app
from blogApp import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import jwt
from time import time


blogtags = db.Table('blogtags',
                    db.Column('blogid', db.Integer, db.ForeignKey(
                        'blogs.id'), primary_key=True),
                    db.Column('tagid', db.Integer, db.ForeignKey(
                        'tags.id'), primary_key=True)
                    )


@login_manager.user_loader
def load_user(user_id):
    return Authors.query.get(int(user_id))

class Authors(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    about = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable = False, default = 'double1.jpg')
    password = db.Column(db.String(60), nullable=False)
    blogs = db.relationship('Blogs', backref='author', lazy=True)

    def __repr__(self):
        return "User(name : {}, email : {})".format(self.name, self.email)

    def get_password_reset_token(self):
        token = jwt.encode({'password_reset':self.id, 'exp':time()+3600}, current_app.config['SECRET_KEY'], algorithm='HS256', )
        return token

    @staticmethod
    def verify_password_reset_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')['password_reset']
            pass
        except:
            return
        return Authors.query.get(id)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text)
    _created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    thumbnail = db.Column(db.String(20), nullable = False, default = 'thumb.jpg')
    authorid = db.Column(db.Integer, db.ForeignKey(
        'authors.id'), nullable=False)
    tags = db.relationship('Tags', secondary=blogtags, 
                           backref=db.backref('blogs', lazy='dynamic'))

    def __repr__(self):
        return "Blog(title : {}, date_created : {})".format(self.title, self._created)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "Tag(tag : {})".format(self.name)
