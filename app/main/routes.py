from flask_login import login_required
from app.main import bp
from flask import render_template
from app.middleware.auth import admin_required


@bp.route('/')
def index():
    return render_template("landing_page.html")
    
@bp.route('/admin/dashboard')
@login_required
@admin_required
def index_dashboard():
    return render_template('dashboard/index.html')