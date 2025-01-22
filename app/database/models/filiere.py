from sqlalchemy import String, ForeignKey, Text, Integer, DateTime
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from app.database.models.ecole import Ecole
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy

class Filiere(db.Model):
    """ filiere model
    """
    __tablename__ = 'filieres'
    id_filiere = mapped_column(String(128), primary_key=True, nullable=False)
    nom = mapped_column(String(255), nullable=False)
    debouches = mapped_column(Text(), nullable=True)
    bourses = mapped_column(Integer(), nullable=True)
    semi_bourses = mapped_column(Integer(), nullable=True)
    code = mapped_column(String(128), nullable=True)
    id_ecole = mapped_column(String(128), ForeignKey(Ecole.id_ecole), nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow())
    updated_at = mapped_column(DateTime, default=datetime.utcnow(),onupdate=datetime.now)
    deleted_at = mapped_column(DateTime, nullable=True)

    ecole = relationship("Ecole", back_populates="filieres")
    
    moyennes = relationship("Moyenne", back_populates="filiere", cascade="all, delete-orphan")
    users = association_proxy("moyennes", "user")
    
    matierefiliere = relationship("MatiereFiliere", back_populates="filiere", cascade="all, delete-orphan")
    matieres = association_proxy("matierefiliere", "matiere")
    
    filiereserie = relationship("FiliereSerie", back_populates="filiere", cascade="all, delete-orphan")
    series = association_proxy("filiereserie", "serie")


    def __init__(self, nom, debouches, bourses, semi_bourses, ecole_id):
        """Initiate the model object with column values
        """
        self.id_filiere = str(uuid4())
        self.nom = nom
        self.debouches = debouches
        self.bourses = bourses
        self.semi_bourses = semi_bourses
        self.id_ecole = ecole_id
        self.created_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of a filiere
        """
        return "Filiere: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a filiere
        """
        return "Ecole: {}".format(self.nom)