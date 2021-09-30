from sqlalchemy.orm import backref
from blogApp import db
from datetime import datetime


blogtags = db.Table('blogtags',
                    db.Column('blogid', db.Integer, db.ForeignKey(
                        'blogs.id', primary_key=True)),
                    db.Column('tagid', db.Integer, db.ForeignKey(
                        'tags.id', primary_key=True))
                    )


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable = False, default = 'double1.jpg')
    password = db.Column(db.String(60), nullable=False)
    blogs = db.relationship('Blogs', backref='author', lazy=True)

    def __repr__(self):
        return "User(name : {}, email : {})".format(self.name, self.email)


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
