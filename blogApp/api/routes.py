import jwt
from time import time
from flask import make_response, request
from blogApp.api import bp
from blogApp.models import Authors
from flask import current_app


@bp.route('/api/login')
def login_author():
    """route for authorizing user and returning access token"""
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    author = Authors.query.filter_by(email=auth['username']).first()

    # if author exists and passwords match
    if author and author.check_password(auth['password']):
        # create a JSON web token with expiration time of one hour
        token = jwt.encode({
            'id': author.id,
            'exp': time()+3600,
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return {'token': token}
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
