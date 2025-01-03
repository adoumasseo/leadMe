from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash
from ..db import Base, db
from .Matiere import Matiere
from datetime import datetime
from uuid import uuid4

class Serie(db.Model):
    """Serie model to map the serie table
    """
    __tablename__ = 'serie'
    id_serie = mapped_column(String(128), primary_key=True, nullable=False)
    nom = mapped_column(String(10), nullable=False)
    matiere = db.relationship('Matiere', secondary = 'coefficient', back_populates = 'serie')
    filiere = db.relationship('Filiere', secondary = 'filiere_serie', back_populates = 'serie')
    created_at = mapped_column(DateTime, default=datetime.now())
    updated_at = mapped_column(DateTime, default=datetime.now())
    deleted_at = mapped_column(DateTime, default=None)

    def __init__(self, nom):
        """Initiate the model object with column values
        """
        self.id_serie = str(uuid4())
        self.nom = nom
        self.created_at = datetime.now()

    def __str__(self):
        """Return a string representation of a serie
        """
        return "Serie: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a serie
        """
        return "Serie: {}".format(self.nom)