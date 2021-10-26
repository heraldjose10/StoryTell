from flask import render_template
from blogApp import db
from blogApp.models import Blogs, Tags
from blogApp.core import bp


@bp.route('/')
def index():
    """Route for homepage"""
    blogs = Blogs.query.order_by(Blogs._created.desc()).limit(6).all()  # query six blogs in descending order from Blogs database
    return render_template('core/home.html', title='Home', blogs=blogs)


@bp.route('/tag/<string:tagName>')
def search(tagName):
    """Route for filtering blogs by a specific tag

    Parameters
    ----------
    tagName : str
    """
    tag = Tags.query.filter_by(name=tagName).first()  # query Tags database for a specific tag

    if tag:
        blogs = tag.blogs
    else:
        blogs = None
        
    return render_template('core/tagSearchResults.html', searchResult=blogs, tag=tag)
