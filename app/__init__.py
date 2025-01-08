from flask import Flask
from config import Config
from flask_migrate import Migrate
from app.extensions import db
from flask.cli import with_appcontext
import click

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(app, db, directory="app/database/migrations")
    
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
        seed_users.seed_users()
        click.echo("Database seeded successfully!")
    
    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app