from flask import Flask
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate, init
from flask_assets import Environment
from flask_moment import Moment
from flask_mail import Mail
from config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.author"
migrate = Migrate()
assets = Environment()
moment = Moment()
mail = Mail()


def create_app(config_class = Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch = True)
    assets.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    from blogApp.core import bp as main_bp
    app.register_blueprint(main_bp)

    from blogApp.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from blogApp.posts import bp as posts_bp
    app.register_blueprint(posts_bp)

    from blogApp.profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    return app
    