from flask import Flask
from config import Config
from app.extensions import db, mail, migrate, login_manager
from app.database.models.user import User
from flask.cli import with_appcontext
import click

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Register blueprints here
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    # CLI for the app
    @app.cli.command("seed")
    @with_appcontext
    def seed():
        """Seed the database with sample data."""
        from app.database.seeds import seed_users
        from app.database.seeds import seed_university
        from app.database.seeds import seed_ecole
        from app.database.seeds import seed_filiere
        
        seed_users.seed_users()
        seed_university.seed_universite()
        seed_ecole.seed_ecoles()
        seed_filiere.seed_filieres()
        click.echo("Database seeded successfully!")
    
    return app

