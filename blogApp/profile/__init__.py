from flask import Blueprint

# create a blueprint for all funcions of profile
bp = Blueprint('profile', __name__)

from blogApp.profile import routes