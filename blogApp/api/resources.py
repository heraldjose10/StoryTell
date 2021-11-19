from flask import request
from flask_restful import Resource, marshal_with
from blogApp.api import api
from blogApp import db
from blogApp.models import Blogs, Authors, Tags
from .marshals import blog_fields, blogs_list_fields, author_fields, tag_feilds, authors_list_fields


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

    @marshal_with(blogs_list_fields)
    def get(self):
        """Return blog resources"""
        per_page = request.args.get('limit') or 5
        current_page = request.args.get('offset') or 1
        total = Blogs.query.count()

        blogs = Blogs.query.order_by(
            Blogs._created.desc()).paginate(int(current_page), int(per_page))

        return {
            'blogs': blogs.items,
            'links': {
                'per_page': per_page,
                'total': total,
                'current_page': current_page,
                'base_link': request.base_url
            }
        }


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

    @marshal_with(authors_list_fields)
    def get(self):
        """Return list of author resource"""
        per_page = request.args.get('limit') or 5
        current_page = request.args.get('offset') or 1
        authors = Authors.query.order_by(Authors.id).paginate(
            int(current_page), int(per_page))
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

    @marshal_with(tag_feilds)
    def get(self, id):
        """Return tag resource

        Parameters
        ----------
        id : int id of tag
        """
        tag = Tags.query.filter_by(id=id).first()

        per_page = request.args.get('limit') or 5
        current_page = request.args.get('offset') or 1
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
            'count': int(per_page),
            'tag': tag,
            'blogs': tag.blogs.paginate(int(current_page), int(per_page)).items
        }


# add resources with routes and endpoints
api.add_resource(BlogsList, '/api/blogs/', endpoint='blogs_list')
api.add_resource(Blog, '/api/blogs/<int:id>', endpoint='blog')

api.add_resource(Author, '/api/authors/<int:id>', endpoint='author')
api.add_resource(AuthorsList, '/api/authors/', endpoint='authors_list')

api.add_resource(Tag, '/api/tags/<int:id>', endpoint='tag')