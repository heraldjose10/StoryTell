from flask import render_template
from blogApp import db
from blogApp.models import Blogs, Tags
from blogApp.core import bp


@bp.route('/')
def index():
    blogs = Blogs.query.order_by(Blogs._created.desc()).limit(6).all()
    return render_template('home.html', title='Home', blogs=blogs)



@bp.route('/tag/<tagName>')
def search(tagName):
    tag = Tags.query.filter_by(name=tagName).first()
    blogs = tag.blogs
    return render_template('tagSearchResults.html', searchResult=blogs, tag=tag)