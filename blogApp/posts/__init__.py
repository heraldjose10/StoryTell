from flask import Blueprint

#creating a blueprint for all posts functionality
bp = Blueprint('posts', __name__)

from blogApp.posts import routes