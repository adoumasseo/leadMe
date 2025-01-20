from flask import Blueprint

bp = Blueprint('ecoles', __name__)

from app.controllers.ecole import routes