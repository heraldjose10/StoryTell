import jwt
from functools import wraps
from flask import current_app, request
from blogApp.models import Authors


def tokens_required(f):
    """Decorator function for validating JSON web token"""
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return {
                'message': 'access token missing!'
            }

        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms='HS256')['id']
            current_user = Authors.query.filter_by(id = id).first()
        except:
            return {
                'message': 'invalid access token!'
            }
            
        return f(current_user, *args, **kwargs)
    
    return decorator
