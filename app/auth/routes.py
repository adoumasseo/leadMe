from app.auth import bp
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from app.database.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user, login_user, logout_user
from app.extensions import db
import re
from app.utils.mail import send_reset_email
from redis_config import redis_client

class CSRFProtectForm(FlaskForm):
    """For CSRF protection"""
    pass
class LoginForm(FlaskForm):
    """A class for generating the login form"""
    email = StringField('Email', validators=[DataRequired(message="The Email is require"), Email()])
    password = PasswordField('Password', validators=[DataRequired(message="Password is require")])
    submit = SubmitField('Sign in')
    
    # Custom email validation
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('No account found with that email address.')
    
    # Custom password validation
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not check_password_hash(user.password, field.data):
            raise ValidationError('Invalid password.')

class ChangePasswordForm(FlaskForm):
    """A class to generate the change_password form"""
    oldPassword = PasswordField('Old Password', validators=[DataRequired(message="Old Password is require")])
    newPassword = PasswordField('New Password', validators=[DataRequired(message="New Password is require"), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    
    # Custom validation for oldPassword
    def validate_oldPassword(self, field):
        if current_user and not check_password_hash(current_user.password, field.data):
            raise ValidationError('Invalid password')
      
    # Custom validation for newPassword
    def validate_newPassword(self, field):
        password = field.data
        # Define the regular expression pattern for the password
        pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'
        if not re.match(pattern, password):
            raise ValidationError('Password must be at least 8 characters long and contain at least one number, one lowercase letter, and one uppercase letter.')

class ForgetPasswordRequest(FlaskForm):
    """A class to generate the form for forget password request"""
    email = StringField('Email', validators=[DataRequired(message="The Email is require"), Email()])
    submit = SubmitField('Submit')
    
    # Custom email validation
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('No account found with that email address.')

class VerifyCodeRequest(FlaskForm):
    """A Form to verify the reset password code"""
    code = HiddenField('Code', validators=[DataRequired()])
    submit = SubmitField('Verify')
    
    def __init__(self, email, *args, **kwargs):
        """Use to set the email and use it in validate_code"""
        super().__init__(*args, **kwargs)
        self.email = email
    
    def validate_code(self, field):
        """To check if the code is correct"""
        reset_code = redis_client.get(f"reset_code:{self.email}")
        
        if field.data != reset_code:
            raise ValidationError('Invalid or Expire Code')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            EqualTo('confirm_password', message='Passwords must match.')
        ]
    )
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
   

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.first_login:
                return redirect(url_for('auth.change_password'))
            flash("Login successful!", "success")
            return "You're login"
        else:
            flash("Invalid email or password.", "danger")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
            return render_template('auth/form/login.html', form=form)
            
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
    else:
        print("Form validation failed.")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
        return render_template('auth/form/change_password.html', form=form)

@bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash("A reset code has been sent to your email.", "success")
            return redirect(url_for('auth.verify_code', email=form.email.data))
        flash("Email not found.", "danger")
    return render_template('auth/form/reset_password_request.html', form=form)       

@bp.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    email = request.args.get('email') or request.form.get('email')
    form = VerifyCodeRequest(email)
    print(f"in verify code email: {email}")
    if not email:
        print("not mail")
        flash("Email is required to verify the code.", "danger")
        return redirect(url_for('auth.forget_password'))

    if form.validate_on_submit():
        print("on validate mail")
        print(form.code.data)
        reset_code = redis_client.get(f"reset_code:{email}")
        if reset_code is None:
            print("reset code none")
            flash("The reset code has expired or is invalid.", "danger")
            return redirect(url_for('auth.forget_password'))

        if form.code.data == reset_code:
            print("valid code") 
            flash("Code verified successfully. You can now reset your password.", "success")
            return redirect(url_for('auth.reset_password', email=email))
        else:
            print("invalid code") 
            
            flash("Invalid reset code. Please try again.", "danger")

    return render_template('auth/form/verify_code.html', form=form, email=email)


@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    email = request.args.get('email') or request.form.get('email')


    if not email:
        flash("Email is required to reset the password.", "danger")
        return redirect(url_for('auth.forget_password'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('auth.forget_password'))

        # Update the user's password
        user.password = generate_password_hash(form.new_password.data)  # Assuming `new_password` is hashed in the form validation
        db.session.commit()

        # Delete the reset code from Redis
        redis_client.delete(f"reset_code:{email}")

        flash("Your password has been reset successfully. Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/form/reset_password.html', form=form, email=email)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
