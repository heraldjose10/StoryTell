from flask import Flask
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_assets import Environment
from flask_moment import Moment
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.author"
migrate = Migrate(app, db, render_as_batch=True)

assets = Environment(app)
app.config['ASSETS_DEBUG'] = True
assets.url = app.static_url_path

moment = Moment(app)

app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(environ.get('MAIL_PORT') or 25)
app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS') is not None
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
app.config['ADMINS'] = ['heraldjose11@gmail.com']

mail = Mail(app)

from blogApp.core import bp as main_bp
app.register_blueprint(main_bp)

from blogApp.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from blogApp.posts import bp as posts_bp
app.register_blueprint(posts_bp)

from blogApp.profile import bp as profile_bp
app.register_blueprint(profile_bp)

from blogApp import commands