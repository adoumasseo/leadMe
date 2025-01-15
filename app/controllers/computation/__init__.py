from flask import Blueprint

bp = Blueprint('computation', __name__)

from app.controllers.computation import routes