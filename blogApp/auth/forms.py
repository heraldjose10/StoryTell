from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from blogApp.models import Authors


class AuthorLogin(FlaskForm):
    """Form for logging in authors/users"""
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    login = SubmitField('login')


class RegisterForm(FlaskForm):
    """Form for registering authors/users"""
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[
                                     DataRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField('register')

    def validate_name(form, field):
        """Function for validating that name is not already taken"""
        user = Authors.query.filter_by(name=field.data).first()
        if user:
            raise ValidationError('Username is already taken')

    def validate_email(form, field):
        """Function for validating that email id is not already taken"""
        user = Authors.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('A account already exists for this email')


class PasswordResetForm(FlaskForm):
    """Form for submitting email id for sending password reset mail"""
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('reset')


class NewPasswordForm(FlaskForm):
    """Form for submitting new passwords for resetting password"""
    create_password = PasswordField(
        'create new password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm new password', validators=[
                                     DataRequired(), EqualTo('create_password', message='passwords soes not match')])
    submit = SubmitField('reset')
