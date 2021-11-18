from math import ceil
from flask import request
from flask_restful import Resource, marshal_with
from blogApp.api import api
from blogApp import db
from blogApp.models import Blogs, Authors, Tags
from .marshals import blog_fields, blogs_list_fields, author_fields


class Blog(Resource):

    @marshal_with(blog_fields)
    def get(self, id):
        blog = Blogs.query.filter_by(id=id).first()
        return blog


class BlogsList(Resource):

    @marshal_with(blogs_list_fields)
    def get(self):

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
                'total': total
            },
            'blogs': blogs.items,
            'total': total,
            'count': int(per_page)
        }


class Author(Resource):

    @marshal_with(author_fields)
    def get(self, id):

        author = Authors.query.filter_by(id=id).first()
        return author


class Tag(Resource):

    def get(self, id):
        tag = Tags.query.filter_by(id=id).first()
        return tag


api.add_resource(BlogsList, '/api/blogs/', endpoint='blogs_list')
api.add_resource(Blog, '/api/blogs/<int:id>', endpoint='blog')
api.add_resource(Author, '/api/authors/<int:id>', endpoint='author')
api.add_resource(Tag, '/api/tags/<int:id>', endpoint='tag')
