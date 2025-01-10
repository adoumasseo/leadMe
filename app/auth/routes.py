from app.auth import bp
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField
from app.database.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user, login_user
from app.extensions import db

class CSRFProtectForm(FlaskForm):
    """For CSRF protection"""
    pass
class LoginForm(FlaskForm):
    """A class for generating the login form"""
    email = StringField('Email', validators=[DataRequired(message="The Email is require"), Email()])
    password = PasswordField('Password', validators=[DataRequired(message="Password is require")])
    submit = SubmitField('Sign in')

class ChangePasswordForm(FlaskForm):
    """A class to generate the change_password form"""
    oldPassword = PasswordField('Old Password', validators=[DataRequired(message="Old Password is require")])
    newPassword = PasswordField('New Password', validators=[DataRequired(message="New Password is require"), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("In the login form")
    if form.validate_on_submit():
        print("The form have been validate")
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            print("you are login")
            if user.first_login:
                return redirect(url_for('auth.change_password'))
            flash("Login successful!", "success")
            return "You're login"
        flash("Invalid email or password.", "danger")
    else:
        print("Form validation failed.")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")

        return render_template('auth/form/login.html', form=form)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.oldPassword.data):
            flash("Old password is incorrect.", "danger")
            return render_template('auth/form/change_password.html', form=form)
        current_user.password = generate_password_hash(form.newPassword.data)
        current_user.first_login = False
        db.session.commit()
        flash("Password changed successfully!", "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/form/change_password.html', form=form)