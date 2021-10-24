from flask import Blueprint

bp = Blueprint('posts', __name__)

from blogApp.posts import routes