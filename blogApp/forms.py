from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets.core import TextArea

class AuthorLogin(FlaskForm):
    email = StringField('email', validators= [DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    login = SubmitField('login')

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')


class BlogForm(FlaskForm):
    title = StringField('title', validators= [DataRequired()])
    editordata = TextAreaField('add contents', validators= [DataRequired()])
    tags = StringField('tags')
    thumbnail_data = StringField('thumbnail')
    post = SubmitField('post')

class ProfileForm(FlaskForm):
    about_me = TextAreaField('about me', validators = [DataRequired()])
    profile_pic_encoded = StringField('profile pic')
    post = SubmitField('update')