from flask import Blueprint

bp = Blueprint('series', __name__)

from app.controllers.serie import routes