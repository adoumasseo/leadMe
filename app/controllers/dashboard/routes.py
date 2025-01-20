from flask_login import login_required, current_user
from app.controllers.dashboard import bp
from flask import render_template
from app.middleware.auth import admin_required

@bp.route('/home')
@login_required
@admin_required
def index():
    userFullName = current_user.prenom + " " + current_user.nom
    userInitials = current_user.prenom[0] + current_user.nom[0]
    return render_template('dashboard/index.html', userFullName=userFullName, userInitials=userInitials)