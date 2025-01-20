from flask import Blueprint

bp = Blueprint('filieres', __name__)

from app.controllers.filiere import routes