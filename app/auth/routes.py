from app.auth import bp
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms import StringField, PasswordField, SubmitField

class CSRFProtectForm(FlaskForm):
    """For CSRF protection"""
    pass
class LoginForm(FlaskForm):
    """A class for generating the login form"""
    email = StringField('Email', validators=[DataRequired("The Email is require"), Email()])
    password = PasswordField('Password', validators=[DataRequired("Password is require")])
    submit = SubmitField('Login')

