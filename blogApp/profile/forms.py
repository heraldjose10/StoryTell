from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField


class ProfileForm(FlaskForm):
    """Form for adding data to user profile section"""
    about_me = TextAreaField('about me', validators=[DataRequired()])
    profile_pic_encoded = StringField('profile pic')
    post = SubmitField('update')