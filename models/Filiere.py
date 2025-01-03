from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash
from ..db import Base, db
from .Ecole import Ecole
from uuid import uuid4
from datetime import datetime

class Filiere(db.Model):
    """filiere model to map the serie table
    """
    __tablename__ = 'filiere'
    id_filiere = mapped_column(String(128), primary_key=True, nullable=False)
    nom = mapped_column(String(10), nullable=False)
    debouches = mapped_column(Text(), nullable=True)
    bourses = mapped_column(Integer(), nullable=True)
    semi_bourses = mapped_column(Integer(), nullable=True)
    code = mapped_column(String(128), nullable=True)
    #formule = mapped_column(String(150), nullable=False)
    categorie = mapped_column(String(20), nullable=True)
    id_ecole = mapped_column(String(128), ForeignKey(Ecole.id_ecole), nullable=True)
    matiere = db.relationship('Matiere', secondary='matiere_filiere', back_populates = 'filiere')
    serie = db.relationship('Serie', secondary = 'filiere_serie', back_populates = 'filiere')
    created_at = mapped_column(DateTime, default=datetime.now())
    updated_at = mapped_column(DateTime, default=datetime.now())
    deleted_at = mapped_column(DateTime, nullable=True)

    def __init__(self, nom, debouches, bourses, semi_bourses, categorie):
        """Initiate the model object with column values
        """
        self.id_filiere = str(uuid4())
        self.nom = nom
        self.debouches = debouches
        self.bourses = bourses
        self.semi_bourses = semi_bourses
        #self.formule = formule
        self.categorie = categorie
        self.created_at = datetime.now()

    def __str__(self):
        """Return a string representation of a serie
        """
        return "Filiere: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a serie
        """
        return "Ecole: {}".format(self.nom)