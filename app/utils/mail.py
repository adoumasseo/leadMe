from flask.templating import render_template
from flask_mail import Message
from flask import current_app
from app.utils.code import store_reset_code
from app.extensions import mail

def send_reset_email(user):
    """Send a password reset email with the reset code."""
    reset_code = store_reset_code(user.email)
    msg = Message(
        "Password Reset Code",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email],
    )
    msg.body = f"Your password reset code is: {reset_code}. It will expire in 5 minutes."
    msg.html = render_template('email/reset_code.html', username=user.prenom, code=reset_code)
    mail.send(msg)