from flask import Blueprint

bp = Blueprint('universites', __name__)

from app.controllers.university import routes