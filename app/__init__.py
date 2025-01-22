from flask import Flask
from config import Config
from app.extensions import db, mail, migrate, login_manager
from app.database.models.user import User
from flask.cli import with_appcontext
import click
import babel.dates

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Register blueprints here
    from app.controllers.main import bp as main_bp
    from app.controllers.auth import bp as auth_bp
    from app.controllers.computation import bp as computation_bp
    from app.controllers.university import bp as university_bp
    from app.controllers.dashboard import bp as dashboard_bp
    from app.controllers.ecole import bp as ecole_bp
    from app.controllers.serie import bp as serie_bp
    from app.controllers.matiere import bp as matiere_bp
    from app.controllers.filiere import bp as filiere_bp
    from app.controllers.post import bp as post_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(computation_bp, url_prefix='/computation')
    app.register_blueprint(university_bp, url_prefix='/dashboard/university')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(ecole_bp, url_prefix='/dashboard/ecole')
    app.register_blueprint(serie_bp, url_prefix='/dashboard/serie')
    app.register_blueprint(matiere_bp, url_prefix='/dashboard/matiere')
    app.register_blueprint(filiere_bp, url_prefix='/dashboard/filiere')
    app.register_blueprint(post_bp, url_prefix='/dashboard/post')
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    # CLI for the app
    @app.cli.command("seed_all")
    @with_appcontext
    def seed():
        """Seed the database with sample data."""
        from app.database.seeds import seed_university
        from app.database.seeds import seed_ecole
        from app.database.seeds import seed_filiere
        from app.database.seeds import seed_matiere_series
        from app.database.seeds import seed_matieres_filieres
        from app.database.seeds import seed_filiere_serie
        from app.database.seeds import seed_users
        
        seed_university.seed_universite()
        seed_ecole.seed_ecoles()
        seed_filiere.seed_filieres()
        seed_matiere_series.seed_series_and_matieres()
        seed_matieres_filieres.seed_filiere_and_matieres()
        seed_filiere_serie.seed_filiere_and_serie()
        seed_users.seed_users()
        click.echo("Database seeded successfully!")
    
    @app.template_filter('format_date')
    def format_date(value, format='medium'):
        if format == 'full':
            format="EEEE, d MMMM y"
        elif format == 'medium':
            format="dd MMMM y"
        return babel.dates.format_datetime(value, format, locale='fr')   
    return app

