from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from blogApp.models import Authors

class AuthorLogin(FlaskForm):
    email = StringField('email', validators= [DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    login = SubmitField('login')

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField('register')

    def validate_name(form, field):
        user = Authors.query.filter_by(name = field.data).first()
        if user:
            raise ValidationError('Username is already taken')

    def validate_email(form, field):
        user = Authors.query.filter_by(email = field.data).first()
        if user:
            raise ValidationError('A account already exists for this email')


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