from flask import Blueprint

bp = Blueprint('matieres', __name__)

from app.controllers.matiere import routes