from flask import Flask
import jinja2
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_assets import Environment
from flask_moment import Moment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfuygiaughdauij3q72846yqiuehrgiq'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "author"
migrate = Migrate(app, db, render_as_batch=True)

assets = Environment(app)
app.config['ASSETS_DEBUG'] = True
assets.url = app.static_url_path

moment = Moment(app)

from blogApp import routes, commands