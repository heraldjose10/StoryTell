from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class AuthorLogin(FlaskForm):
    email = StringField('email', validators= [DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    login = SubmitField('Login')