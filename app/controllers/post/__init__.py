from flask import Blueprint

bp = Blueprint('posts', __name__)

from app.controllers.post import routes