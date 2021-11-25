import os
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
    """methods for individual blog resource"""

    method_decorators = {
        'delete': [tokens_required],
        'patch': [tokens_required]
    }

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title', type=str, help='title should be string', location='form')
        self.reqparse.add_argument(
            'tags', type=str, help='tags should be string separated by space', location='form')
        self.reqparse.add_argument(
            'content', type=str, help='content is required', location='form')
        self.reqparse.add_argument(
            'thumbnail', type=FileStorage, help='thumbnail size should be less than 5MB',
            location='files')

    @marshal_with(blog_fields)
    def get(self, id):
        """Return blog resource

        Parameters
        ----------
        id : int id of blog
        """
        blog = Blogs.query.filter_by(id=id).first()
        return blog

    def delete(self, current_user, id):
        """Delete a individual blog

        Parameters
        ----------
        id : int id of blog
        current_user : Authors object(user who sent the request)
        """
        blog = Blogs.query.filter_by(id=id).first()

        if not blog:
            return {'msg': 'there is no blog with id {}'.format(id)}, 404

        if blog.author == current_user:
            try:
                file_path = os.path.join(
                    current_app.root_path, 'static/assets/thumbnails/', blog.thumbnail)
                os.remove(file_path)
            except FileNotFoundError:
                pass
            db.session.delete(blog)
            db.session.commit()
            return {'msg': 'blog deleted successfully'}, 200

        return {'msg': 'you do not have permission to delete this blog'}, 403

    def patch(self, current_user, id):
        """update a already existing blog

        Parameters
        ----------
        id : int id of blog
        current_user : Authors object(user who sent the request)
        """
        blog = Blogs.query.filter_by(id=id).first()

        args = self.reqparse.parse_args()
        title = args['title']
        tags = args['tags']
        content = args['content']
        thumbnail = args['thumbnail']

        if not blog:
            return {'msg': 'there is no blog with id {}'.format(id)}, 404

        if blog.author == current_user:

            if title:
                blog.title = title

            if tags:

                to_remove = blog.tags  # remove all the already existing tags of blog
                while to_remove:
                    blog.tags.remove(to_remove[0])
                    to_remove = blog.tags
                db.session.commit()

                tags = tags.split(' ')
                for tag in tags:
                    # create new tag and add to database if tag doesnt already exist
                    t = Tags.query.filter_by(name=tag).first()
                    if t == None:
                        t = Tags(name=tag)
                        db.session.add(t)
                    t.blogs.append(blog)

            if content:
                blog.content = content

            if thumbnail:
                # delete existing thumbnail
                try:
                    file_path = os.path.join(
                        current_app.root_path, 'static/assets/thumbnails/', blog.thumbnail)
                    os.remove(file_path)
                except FileNotFoundError:
                    pass

                updated_file_name = secrets.token_hex(8) + '.jpg'
                thumbnail.save(current_app.root_path +
                               '/static/assets/thumbnails/' + updated_file_name)
                blog.thumbnail = updated_file_name

            db.session.commit()

            return {
                'msg': 'blog updated successfully',
                'id': blog.id
            }, 200

        return {'msg': 'you do not have permission to update this blog'}, 403


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
        content = args['content']

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
    """methods for individual author resource"""

    method_decorators = {
        'patch': [tokens_required]
    }

    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'about', type=str, help='about me should be string', location='form')
        self.reqparse.add_argument(
            'image_file', type=FileStorage, help='profile pic should be less than 5MB',
            location='files')

    @marshal_with(author_fields)
    def get(self, id):
        """Return author resource

        Parameters
        ----------
        id : int id of author
        """
        author = Authors.query.filter_by(id=id).first()
        return author

    def patch(self, current_user, id):
        """Update a author details

        Parameters
        ----------
        id : int id of blog
        current_user : Authors object(user who sent the request)
        """
        args = self.reqparse.parse_args()

        author = Authors.query.filter_by(id=id).first()

        if not author:
            return {'message': 'there is no author with id {}'.format(id)}

        if author == current_user:

            about = args['about']
            profile_pic = args['image_file']

            if about:
                author.about = about

            if profile_pic:
                updated_file_name = secrets.token_hex(8)+'.jpg'
                profile_pic.save(current_app.root_path +
                                       '/static/assets/profile_pics/'+updated_file_name)
                author.image_file = updated_file_name

            db.session.commit()

            return {
                'msg': 'author details updated successfully',
                'id': author.id
            }, 200

        return {'message': 'you do not have permission to update this'}, 403


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

    def post(self):
        """Create a author resource"""
        post_reqparse = self.reqparse.copy()
        post_reqparse.add_argument(
            'name', type=str, help='name is required', required=True, location='form')
        post_reqparse.add_argument(
            'email', type=str, help='email is required', required=True, location='form')
        post_reqparse.add_argument(
            'password', type=str, help='password is required', required=True, location='form')
        args = post_reqparse.parse_args()

        name = args['name']
        email = args['email']
        password = args['password']

        # return error message if username or email is taken
        message = {}
        author = Authors.query.filter_by(name=name).first()
        if author:
            message['name'] = 'Username is already taken'

        author = Authors.query.filter_by(email=email).first()
        if author:
            message['email'] = 'A account already exists for this email'

        if message:
            return {'message': message}

        author = Authors(name=name, email=email)
        author.set_password(password)
        db.session.add(author)
        db.session.commit()

        return {
            'message': 'author created successfully',
            'id': author.id
        }, 201


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
