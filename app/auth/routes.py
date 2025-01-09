from app.auth import bp
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    """A class for generating the login form"""
    