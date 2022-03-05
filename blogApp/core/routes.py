from flask import render_template, request, url_for
from blogApp import Config
from blogApp.models import Blogs, Tags
from blogApp.core import bp


@bp.route('/')
def index():
    """Route for homepage"""
    page = request.args.get('page', 1, type=int)
    blogs = Blogs.query.order_by(Blogs._created.desc()).paginate(
        page, Config.POSTS_PER_PAGE, False)  # query six blogs in descending order from Blogs database

    next_url = url_for(
        'core.index', page=blogs.next_num) if blogs.has_next else None
    prev_url = url_for(
        'core.index', page=blogs.prev_num) if blogs.has_prev else None

    return render_template(
        'core/home.html',
        title='Home',
        blogs=blogs.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/tag/<string:tagName>')
def search(tagName):
    """Route for filtering blogs by a specific tag

    Parameters
    ----------
    tagName : str
    """
    page = request.args.get('page', 1, type=int)
    tag = Tags.query.filter_by(name=tagName).first(
    )  # query Tags database for a specific tag

    if tag:
        blogs = tag.blogs.paginate(page, Config.POSTS_PER_PAGE, False)
    else:
        blogs = None

    next_url = url_for(
        'core.search', tagName=tagName, page=blogs.next_num) if blogs.has_next else None
    prev_url = url_for(
        'core.search', tagName=tagName, page=blogs.prev_num) if blogs.has_prev else None

    return render_template(
        'core/tagSearchResults.html',
        searchResult=blogs.items if blogs else None,
        tag=tag.name if tag else tagName,
        next_url=next_url,
        prev_url=prev_url
    )
