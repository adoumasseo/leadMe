from flask_login import login_required
from app.controllers.dashboard import bp
from flask import render_template
from app.middleware.auth import admin_required

@bp.route('/home')
@login_required
@admin_required
def index():
    return render_template('dashboard/index.html')