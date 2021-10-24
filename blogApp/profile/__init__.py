from flask import Blueprint

bp = Blueprint('profile', __name__)

from blogApp.profile import routes