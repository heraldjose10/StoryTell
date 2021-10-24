from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf import FlaskForm


class BlogForm(FlaskForm):
    title = StringField('title', validators= [DataRequired()])
    editordata = TextAreaField('add contents', validators= [DataRequired()])
    tags = StringField('tags')
    thumbnail_data = StringField('thumbnail')
    post = SubmitField('post')