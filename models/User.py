from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from.Serie import Serie
from ..db import db
from uuid import uuid4
from datetime import datetime


class User(UserMixin, db.Model):
    """User model to map the users table
    """
    __tablename__ = 'users'
    id = mapped_column(String(128), primary_key=True, nullable=False)
    matricule = mapped_column(String(128), nullable=False)
    prenom = mapped_column(String(45), nullable=True)
    nom = mapped_column(String(45), nullable=True)
    email = mapped_column(String(100), nullable=True)
    password = mapped_column(String(200), nullable=False)
    role = mapped_column(String(45), nullable=False)
    serie = mapped_column(String(128), ForeignKey(Serie.id_serie), nullable=True)
    created_at = mapped_column(DateTime, default=datetime.now())
    updated_at = mapped_column(DateTime, default=datetime.now())
    deleted_at = mapped_column(DateTime, nullable=True)
    
    posts = relationship("Post", back_populates="user")

    def __init__(self, prenom, nom, matricule, email, serie, password="ROOT", role="user"):
        """Initiate the model object with column values
        """
        self.id = str(uuid4())
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
