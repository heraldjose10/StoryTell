from flask import Blueprint

bp = Blueprint('auth', __name__)

from blogApp.auth import routes