from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash
from ..db import Base, db
from .Universites import Universite
from uuid import uuid4
from datetime import datetime

class Ecole(db.Model):
    """ecole model to map the serie table
    """
    __tablename__ = 'ecole'
    id_ecole = mapped_column(String(128), primary_key=True, nullable=False)
    nom = mapped_column(String(10), nullable=False)
    code= mapped_column(String(10), nullable=False)
    id_universite = mapped_column(String(128), ForeignKey(Universite.id_universite), nullable=False)
    code = mapped_column(String(128), nullable=True)
    created_at = mapped_column(DateTime, default=datetime.now())
    updated_at = mapped_column(DateTime, default=datetime.now())
    deleted_at = mapped_column(DateTime, default=None)
    universite = relationship("Universite", back_populates="ecoles")

    def __init__(self, nom, code):
        """Initiate the model object with column values
        """
        self.id_ecole = str(uuid4())
        self.nom = nom
        self.code = code
        self.created_at = datetime.now()

    def __str__(self):
        """Return a string representation of a serie
        """
        return "Ecole: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a serie
        """
        return "Ecole: {}".format(self.nom)