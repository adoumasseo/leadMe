
from app.controllers.main import bp
from flask import render_template


@bp.route('/')
def index():
    return render_template("landing_page.html")