from flask import Flask, flash ,render_template
from .models import (User, Universites, Serie, Role, Note, Moyenne, Matiere, Filiere, Ecole, associations)
from flask_login import LoginManager
import requests
import json
import os
import babel.dates
from lead_me.models.Post import Post


def create_app(test_config=None):
    """configure and return our main app"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(SECRET_KEY='dev')
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'lead_me.db')
    # app.config['SQLALCHEMY_ECHO'] = True
    # app.config['SECRET_KEY'] = 'JOLIDON@21Jolidon@24'
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="postgresql://postgres:Jolidon21@127.0.0.1:5432/leadme",
        SQLALCHEMY_ECHO=True,
        UPLOAD_FOLDER=os.path.join(basedir, 'static/uploads'),
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'}
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.template_filter('format_date')
    def format_date(value, format='medium'):
        if format == 'full':
            format="EEEE, d MMMM y"
        elif format == 'medium':
            format="dd MMMM y"
        return babel.dates.format_datetime(value, format, locale='fr')
    
    from .db import db
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(matricule):
        return User.User.query.get(matricule)
    with app.app_context():
        # db.drop_all()
        db.create_all()
    from .auth import auth_bp
    from .enregistrement import notes_bp
    from .roles import roles_bp
    from .serie import series_bp
    from .universite import universites_bp
    from .ecole import ecoles_bp
    from .user import users_bp
    from .posts import posts_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(series_bp)
    app.register_blueprint(universites_bp)
    app.register_blueprint(ecoles_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    @app.route("/", methods=["GET"])
    def resultat():
        latest_posts = Post.query.order_by(Post.created_at.desc()).limit(3).all()
        return render_template("frontend/landing_page.html", posts=latest_posts)
    
    @app.route("/all_post", methods=["GET"])
    def return_post():
        all_post = Post.query.all()
        return render_template("frontend/posts.html", posts=all_post)
    
    return app
