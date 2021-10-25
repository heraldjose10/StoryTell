from flask import Blueprint

#create a blueprint with all core functionalities
bp = Blueprint('core', __name__)

from blogApp.core import routes