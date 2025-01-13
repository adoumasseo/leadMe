from flask_login import login_required
from app.main import bp
from flask import render_template

@bp.route('/')
def index():
    return render_template("landing_page.html")
    
@login_required
@bp.route('/admin/dashboard')
def index_dashbaord():
    return render_template('dashboard/index.html')