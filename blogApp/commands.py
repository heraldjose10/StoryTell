from blogApp import db
from flask.cli import with_appcontext
import click



def register(app):

    # create command function
    @click.command(name='create_db')
    @with_appcontext
    def create_db():
        db.create_all()


    app.cli.add_command(create_db)