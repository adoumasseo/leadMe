from sqlalchemy.orm import  mapped_column
from app.extensions import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy

class Matiere(db.Model):
    """Serie model to map the matiere table
    """
    __tablename__ = 'matiere'
    id_matiere = mapped_column(db.String(128), primary_key=True, nullable=False)
    nom = mapped_column(db.String(10), nullable=False)
    created_at = mapped_column(db.DateTime, default=datetime.utcnow())
    updated_at = mapped_column(db.DateTime, default=datetime.utcnow())
    deleted_at = mapped_column(db.DateTime, default=None)
    
    matierefiliere = db.relationship("MatiereFiliere", back_populates="matiere")
    filieres = association_proxy("matierefiliere", "filiere")


    def __init__(self, nom, coefficient):
        """Initiate the model object with column values
        """
        self.id_matiere = str(uuid4())
        self.nom = nom
        self.created_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of a matiere
        """
        return "Matiere: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a matiere
        """
        return "Matiere: {}".format(self.nom)