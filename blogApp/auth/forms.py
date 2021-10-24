from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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


class PasswordResetForm(FlaskForm):
    email = StringField('email', validators= [DataRequired(), Email()])
    submit = SubmitField('reset')

class NewPasswordForm(FlaskForm):
    create_password = PasswordField('create new password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm new password', validators=[DataRequired(), EqualTo('create_password', message= 'passwords soes not match')])
    submit = SubmitField('reset')