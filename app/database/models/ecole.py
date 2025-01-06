from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from app.database.models.university import Universite
from uuid import uuid4
from datetime import datetime

class Ecole(db.Model):
    """ Model of table ecole
    """
    __tablename__ = 'ecoles'
    id_ecole = mapped_column(db.String(128), primary_key=True, nullable=False)
    nom = mapped_column(db.String(10), nullable=False)
    code= mapped_column(db.String(10), nullable=False)
    id_universite = mapped_column(db.String(128), db.ForeignKey(Universite.id_universite), nullable=False, ondelete="CASCADE")
    code = mapped_column(db.String(128), nullable=True)
    created_at = mapped_column(db.DateTime, default=datetime.utcnow())
    updated_at = mapped_column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.now)
    deleted_at = mapped_column(db.DateTime, default=None)
    universite = relationship("Universite", back_populates="ecoles")
    filieres = relationship("Filiere", back_populates="ecole")

    def __init__(self, nom, code):
        """Initiate the model object with column values
        """
        self.id_ecole = str(uuid4())
        self.nom = nom
        self.code = code
        self.created_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of a serie
        """
        return "Ecole: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a serie
        """
        return "Ecole: {}".format(self.nom)