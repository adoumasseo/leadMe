from flask import Flask
from config import Config
from app.extensions import db, mail, migrate
from flask.cli import with_appcontext
import click

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
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

