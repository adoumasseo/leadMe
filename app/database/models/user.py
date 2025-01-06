from sqlalchemy.orm import mapped_column, relationship
from werkzeug.security import generate_password_hash
from app.extensions import db
from uuid import uuid4
from datetime import datetime


class User(db.Model):
    """User model to map the users table
    """
    __tablename__ = 'users'
    id_user = mapped_column(db.String(128), primary_key=True, nullable=False)
    matricule = mapped_column(db.String(128), nullable=True)
    prenom = mapped_column(db.String(45), nullable=True)
    nom = mapped_column(db.String(45), nullable=True)
    email = mapped_column(db.String(100), nullable=False)
    password = mapped_column(db.String(200), nullable=True)
    role = mapped_column(db.String(45), nullable=False, default="user")
    created_at = mapped_column(db.DateTime, default=datetime.now())
    updated_at = mapped_column(db.DateTime, default=datetime.now())
    deleted_at = mapped_column(db.DateTime, nullable=True)
    filieres = relationship("Filiere", back_populates="users")
    posts = relationship("Post", back_populates="user")

    def __init__(self, prenom, nom, matricule, email, serie, password="Admin@admin", role="user"):
        """Initiate the model object with column values
        """
        self.id_user = str(uuid4())
        self.prenom = prenom
        self.nom = nom
        self.matricule = matricule
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        self.serie = serie
        self.created_at = datetime.now()

    def __str__(self):
        """Return a string representation of a user
        """
        return "User: {} {}".format(self.prenom, self.nom)

    def __repr__(self):
        """Return a string representation of a user
        """
        return "User: {} {}".format(self.prenom, self.nom)
