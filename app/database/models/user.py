from sqlalchemy import String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import mapped_column, relationship
from werkzeug.security import generate_password_hash
from app.extensions import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from app.database.models.serie import Serie
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User model to map the users table
    """
    __tablename__ = 'users'
    id_user = mapped_column(String(128), primary_key=True, nullable=False)
    matricule = mapped_column(String(128), nullable=True)
    prenom = mapped_column(String(45), nullable=True)
    nom = mapped_column(String(45), nullable=True)
    email = mapped_column(String(255), nullable=False)
    password = mapped_column(String(255), nullable=True)
    role = mapped_column(String(45), nullable=False, default="user")
    first_login = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, default=datetime.utcnow())
    updated_at = mapped_column(DateTime, default=datetime.utcnow(), onupdate=datetime.now)
    deleted_at = mapped_column(DateTime, nullable=True)
    
    # filiere users
    moyennes = relationship("Moyenne", back_populates="user", cascade="all, delete-orphan")
    filieres = association_proxy("moyennes", "filiere")
    
    # posts and series
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    id_serie = mapped_column(String(128), ForeignKey(Serie.id_serie), nullable=True)
    serie = relationship("Serie", back_populates="users")
    
    # user matiere 
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    matieres = association_proxy("note", "matiere")

    def __init__(self, prenom, nom, matricule, email, serie_id, password="user@user1234", role="user"):
        """Initiate the model object with column values
        """
        self.id_user = str(uuid4())
        self.prenom = prenom
        self.nom = nom
        self.matricule = matricule
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
        if serie_id:
            self.id_serie = serie_id
        else:
            self.id_serie = None
        self.created_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of a user
        """
        return "User: {} {}".format(self.prenom, self.nom)

    def __repr__(self):
        """Return a string representation of a user
        """
        return "User: {} {}".format(self.prenom, self.nom)
        
    def get_id(self):
         return str(self.id_user)