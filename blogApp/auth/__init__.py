from flask import Blueprint

#create a blueprint with all authentication functionalities
bp = Blueprint('auth', __name__)

from blogApp.auth import routes