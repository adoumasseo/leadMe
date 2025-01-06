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
    id_filiere = mapped_column(db.String(128), primary_key=True, nullable=False)
    nom = mapped_column(db.String(10), nullable=False)
    debouches = mapped_column(db.Text(), nullable=True)
    bourses = mapped_column(db.Integer(), nullable=True)
    semi_bourses = mapped_column(db.Integer(), nullable=True)
    code = mapped_column(db.String(128), nullable=True)
    id_ecole = mapped_column(db.String(128), db.ForeignKey(Ecole.id_ecole), nullable=False)
    ecole = relationship("Ecole", back_populates="filieres")
    created_at = mapped_column(db.DateTime, default=datetime.utcnow())
    updated_at = mapped_column(db.DateTime, default=datetime.utcnow(),onupdate=datetime.now)
    deleted_at = mapped_column(db.DateTime, nullable=True)

    moyennes = relationship("Moyenne", back_populates="filiere")
    users = association_proxy("moyennes", "user")
    
    matierefiliere = relationship("MatiereFiliere", back_populates="filiere")
    matieres = association_proxy("matierefiliere", "matiere")


    def __init__(self, nom, debouches, bourses, semi_bourses):
        """Initiate the model object with column values
        """
        self.id_filiere = str(uuid4())
        self.nom = nom
        self.debouches = debouches
        self.bourses = bourses
        self.semi_bourses = semi_bourses
        self.created_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of a serie
        """
        return "Filiere: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a serie
        """
        return "Ecole: {}".format(self.nom)