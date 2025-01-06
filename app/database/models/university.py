from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from app.extensions import db
from uuid import uuid4
from datetime import datetime

class Universite(db.Model):
    """ Model of table university
    """
    __tablename__ = 'universities'
    id_universite = mapped_column(String(128), primary_key=True, nullable=False)
    nom = mapped_column(String(10), nullable=False)
    code = mapped_column(String(10), nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow())
    updated_at = mapped_column(DateTime, default=datetime.utcnow(), onupdate=datetime.now)
    deleted_at = mapped_column(DateTime, default=None)
    
    ecoles = relationship("Ecole", back_populates="university")

    def __init__(self, nom, code):
        """Initiate the model object with column values
        """
        self.id_universite = str(uuid4())
        self.nom = nom
        self.code = code
        self.created_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of a serie
        """
        return "Universite: {}, Code: {}".format(self.nom, self.code)

    def __repr__(self):
        """Return a string representation of a serie
        """
        return "Universite: {}, Code: {}".format(self.nom, self.code)
