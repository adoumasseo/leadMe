from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import PrimaryKeyConstraint
from app.database.models.filiere import Filiere
from app.database.models.matiere import Matiere
from app.database.models.serie import Serie
from app.database.models.user import User
from app.extensions import db


class Moyenne(db.Model):
    __tablename__ = "moyennes"
    id_filiere = mapped_column(db.String(128), db.ForeignKey(Filiere.id_filiere), nullable=False)
    id_user = mapped_column(db.String(128), db.ForeignKey(User.id_user), nullable=False)
    average = mapped_column(db.Float, nullable=True)
    
    __table_args__ = (
            PrimaryKeyConstraint('id_filiere', 'id_user'),
    )
    
    filiere = relationship("Filiere", back_populates="moyennes")
    user = relationship("User", back_populates="moyennes")

  
class MatiereFiliere(db.Model):
    __tablename__ = "matiere_filiere"
    id_filiere = mapped_column(db.String(128), db.ForeignKey(Filiere.id_filiere), nullable=False)
    id_matiere = mapped_column(db.String(128), db.ForeignKey(Matiere.id_matiere), nullable=False)
    
    __table_args__ = (
            PrimaryKeyConstraint('id_filiere', 'id_matiere'),
    )
    
    filiere = relationship("Filiere", back_populates="matierefiliere")
    matiere = relationship("Matiere", back_populates="matierefiliere")

class Coefficiant(db.Model):
    __tablename__ = "coefficiant"
    id_serie = mapped_column(db.String(128), db.ForeignKey(Serie.id_serie), nullable=False)
    id_matiere = mapped_column(db.String(128), db.ForeignKey(Matiere.id_matiere), nullable=False)
    
    __table_args__ = (
            PrimaryKeyConstraint('id_filiere', 'id_matiere'),
    )
    
    serie = relationship("Serie", back_populates="coefficiant")
    matiere = relationship("Matiere", back_populates="coefficiant")