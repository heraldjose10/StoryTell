from blogApp import db
from flask.cli import with_appcontext
import click


def register(app):
    """Function to register the commands after app is created

    Parameters
    ----------
    app : app object
    """
    @click.command(name='create_db')
    @with_appcontext
    def create_db():
        """Function to create database"""
        db.create_all()

    app.cli.add_command(create_db)  # add command create_db to flask app
