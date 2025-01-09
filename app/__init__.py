from flask import Flask
from config import Config
from flask_migrate import Migrate
from app.extensions import db
from flask.cli import with_appcontext
import click
from flask_login import LoginManager 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(app, db, directory="app/database/migrations")
    login_manager = LoginManager()
    login_manager.init_app(app)

    
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # CLI for the app
    # Add CLI commands
    @app.cli.command("seed")
    @with_appcontext
    def seed():
        """Seed the database with sample data."""
        from app.database.seeds import seed_users
        from app.database.seeds import seed_university
        seed_users.seed_users()
        seed_university.seed_universite()
        click.echo("Database seeded successfully!")
    
    @app.cli.command("seed_universities")
    @with_appcontext
    def seed_university_only():
        """Seed university Only"""
        from app.database.seeds import seed_university
        seed_university.seed_universite()
        click.echo("Database seeded successfully!")
    
    @app.cli.command("seed_ecole")
    @with_appcontext
    def seed_ecole_only():
        """Seed ecole Only"""
        from app.database.seeds import seed_ecole
        seed_ecole.seed_ecoles()
        click.echo("Database seeded successfully!")
        
    @app.cli.command("seed_filiere")
    @with_appcontext
    def seed_filiere_only():
        """Seed ecole Only"""
        from app.database.seeds import seed_filiere
        seed_filiere.seed_filieres()
        click.echo("Database seeded successfully!")

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app