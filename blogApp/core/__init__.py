from flask import Blueprint

bp = Blueprint('core', __name__)

from blogApp.core import routes