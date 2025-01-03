from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash
from ..db import Base, db
from uuid import uuid4
from datetime import datetime

class Matiere(db.Model):
    """Serie model to map the matiere table
    """
    __tablename__ = 'matiere'
    id_matiere = mapped_column(String(128), primary_key=True, nullable=False)
    nom = mapped_column(String(10), nullable=False)
    coefficient = mapped_column(Integer, nullable=False)
    serie = db.relationship('Serie', secondary = 'coefficient', back_populates = 'matiere')
    filiere = db.relationship('Filiere', secondary = 'matiere_filiere', back_populates = 'matiere')
    created_at = mapped_column(DateTime, default=datetime.now())
    updated_at = mapped_column(DateTime, default=datetime.now())
    deleted_at = mapped_column(DateTime, default=None)

    def __init__(self, nom, coefficient):
        """Initiate the model object with column values
        """
        self.id_matiere = str(uuid4())
        self.nom = nom
        self.coefficient = coefficient
        self.created_at = datetime.now()

    def __str__(self):
        """Return a string representation of a matiere
        """
        return "Matiere: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a matiere
        """
        return "Matiere: {}".format(self.nom)