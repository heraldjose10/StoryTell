from math import ceil
from flask import request
from flask_restful import Resource, marshal_with
from blogApp.api import api
from blogApp import db
from blogApp.models import Blogs, Authors, Tags
from .marshals import blog_fields, blogs_list_fields, author_fields, tag_feilds


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
        last_page_number = ceil(int(total)/int(per_page))

        blogs = Blogs.query.order_by(
            Blogs._created.desc()).paginate(int(current_page), int(per_page))

        return {
            'first': f'{request.base_url}?limit={per_page}&offset=1',
            'self': f'{request.base_url}?limit={per_page}&offset={current_page}',
            'last': f'{request.base_url}?limit={per_page}&offset={last_page_number}',
            'prev': {
                'prev_num': int(current_page)-1,
                'base_link': f'{request.base_url}?limit={per_page}&offset='
            },
            'next': {
                'next_num': int(current_page)+1,
                'base_link': f'{request.base_url}?limit={per_page}&offset=',
                'total': last_page_number
            },
            'blogs': blogs.items,
            'total': total,
            'count': int(per_page)
        }


class Author(Resource):
    """methods for list of authors"""
    @marshal_with(author_fields)
    def get(self, id):
        """Return author resource

        Parameters
        ----------
        id : int id of author
        """
        author = Authors.query.filter_by(id=id).first()
        return author


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
        last_page_number = ceil(int(total)/int(per_page))

        return {
            'first': f'{request.base_url}?limit={per_page}&offset=1',
            'self': f'{request.base_url}?limit={per_page}&offset={current_page}',
            'last': f'{request.base_url}?limit={per_page}&offset={last_page_number}',
            'prev': {
                'prev_num': int(current_page)-1,
                'base_link': f'{request.base_url}?limit={per_page}&offset='
            },
            'next': {
                'next_num': int(current_page)+1,
                'base_link': f'{request.base_url}?limit={per_page}&offset=',
                'total': last_page_number
            },
            'id':id,
            'total': total,
            'count': int(per_page),
            'tag': tag,
            'blogs': tag.blogs.paginate(int(current_page), int(per_page)).items
        }


# add resources with routes and endpoints
api.add_resource(BlogsList, '/api/blogs/', endpoint='blogs_list')
api.add_resource(Blog, '/api/blogs/<int:id>', endpoint='blog')
api.add_resource(Author, '/api/authors/<int:id>', endpoint='author')
api.add_resource(Tag, '/api/tags/<int:id>', endpoint='tag')
