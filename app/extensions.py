from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
mail = Mail()
migrate = Migrate(directory="app/database/migrations")
login_manager = LoginManager()
login_manager.login_view = 'auth.login'