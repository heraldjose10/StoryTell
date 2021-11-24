import secrets
from flask import request, current_app
from flask_restful import Resource, marshal_with, reqparse
from werkzeug.datastructures import FileStorage
from blogApp.api import api
from blogApp import db
from blogApp.models import Blogs, Authors, Tags
from .marshals import blog_fields, blogs_list_fields, author_fields, tag_feilds, authors_list_fields
from .utils import tokens_required


class Blog(Resource):
    """methods for induvidual blog resource"""

    @marshal_with(blog_fields)
    def get(self, id):
        """Return blog resource

        Parameters
        ----------
        id : int id of blog
        """
        blog = Blogs.query.filter_by(id=id).first()
        return blog


class BlogsList(Resource):
    """methods for list of blogs"""

    method_decorators = {'post': [tokens_required]}

    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument(
            'limit', type=int, location='args', help='limit should be integer')
        self.reqparse.add_argument(
            'offset', type=int, location='args', help='offset should be integer')
        self.reqparse.add_argument(
            'title', type=str, help='title of blog is required', location='form')
        self.reqparse.add_argument(
            'tags', type=str, help='tags should be string separated by space', location='form')
        self.reqparse.add_argument(
            'content', type=str, help='content is required', location='form')
        self.reqparse.add_argument(
            'thumbnail', type=FileStorage, help='thumbnail size should be less than 5MB',
            location='files')

    @marshal_with(blogs_list_fields)
    def get(self):
        """Return blog resources"""
        args = self.reqparse.parse_args()
        per_page = args.get('limit') or 5
        current_page = args.get('offset') or 1
        total = Blogs.query.count()

        blogs = Blogs.query.order_by(
            Blogs._created.desc()).paginate(current_page, per_page)

        return {
            'blogs': blogs.items,
            'links': {
                'per_page': per_page,
                'total': total,
                'current_page': current_page,
                'base_link': request.base_url
            }
        }

    def post(self, current_user):
        """Create a blog"""
        post_reqparse = self.reqparse.copy()
        post_reqparse.replace_argument(
            'content', type=str, help='content is required', location='form', required=True)
        post_reqparse.replace_argument(
            'title', type=str, help='title of blog is required', location='form', required=True)
        args = post_reqparse.parse_args()

        # split tags to get list of tags
        tags = args['tags'].split(' ')
        title = args['title']
        content = args['title']

        blog = Blogs(title=title, content=content, author=current_user)
        db.session.add(blog)

        for tag in tags:
            # create new tag and add to database if tag doesnt already exist
            t = Tags.query.filter_by(name=tag).first()
            if t == None:
                t = Tags(name=tag)
                db.session.add(t)
            t.blogs.append(blog)

        # create a random name for thumbnail with 8 letters
        random_hex = secrets.token_hex(8)
        updated_file_name = random_hex + '.jpg'
        thumbnail = args['thumbnail']
        thumbnail.save(current_app.root_path +
                       '/static/assets/thumbnails/'+updated_file_name)
        blog.thumbnail = updated_file_name

        db.session.commit()

        return {
            'msg': 'blog posted successfully',
            'id': blog.id
        }, 201


class Author(Resource):
    """methods for induvidual author resouce"""

    @marshal_with(author_fields)
    def get(self, id):
        """Return author resource

        Parameters
        ----------
        id : int id of author
        """
        author = Authors.query.filter_by(id=id).first()
        return author


class AuthorsList(Resource):
    """methods for list of authors"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument(
            'limit', type=int, help='limit should be integer', location='args')
        self.reqparse.add_argument(
            'offset', type=int, help='offset should be integer', location='args')
        # super().__init__()

    @marshal_with(authors_list_fields)
    def get(self):
        """Return list of author resource"""
        args = self.reqparse.parse_args()
        per_page = args.get('limit') or 5
        current_page = args.get('offset') or 1
        authors = Authors.query.order_by(Authors.id).paginate(
            current_page, per_page)
        total = Authors.query.count()
        return {
            'authors': authors.items,
            'links': {
                'per_page': per_page,
                'total': total,
                'current_page': current_page,
                'base_link': request.base_url
            }
        }


class Tag(Resource):
    """methods for list of tags"""

    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument(
            'limit', type=int, help='limit should be integer', location='args')
        self.reqparse.add_argument(
            'offset', type=int, help='offset should be integer', location='args')
        # super().__init__()

    @marshal_with(tag_feilds)
    def get(self, id):
        """Return tag resource

        Parameters
        ----------
        id : int id of tag
        """
        tag = Tags.query.filter_by(id=id).first()

        args = self.reqparse.parse_args()
        per_page = args.get('limit') or 5
        current_page = args.get('offset') or 1
        total = tag.blogs.count()

        return {
            'links': {
                'per_page': per_page,
                'total': total,
                'current_page': current_page,
                'base_link': request.base_url
            },
            'id': id,
            'total': total,
            'count': per_page,
            'tag': tag,
            'blogs': tag.blogs.paginate(current_page, per_page).items
        }


# add resources with routes and endpoints
api.add_resource(BlogsList, '/api/blogs/', endpoint='blogs_list')
api.add_resource(Blog, '/api/blogs/<int:id>', endpoint='blog')

api.add_resource(Author, '/api/authors/<int:id>', endpoint='author')
api.add_resource(AuthorsList, '/api/authors/', endpoint='authors_list')

api.add_resource(Tag, '/api/tags/<int:id>', endpoint='tag')
