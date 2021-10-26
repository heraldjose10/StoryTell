from flask import Blueprint

# create a blueprint for handling errors
bp = Blueprint('errors', __name__)

from blogApp.errors import handlers