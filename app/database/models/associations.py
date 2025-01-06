from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import PrimaryKeyConstraint
from app.database.models.filiere import Filiere
from app.database.models.matiere import Matiere
from app.database.models.serie import Serie
from app.database.models.user import User
from app.extensions import db


class Moyenne(db.Model):
    __tablename__ = "moyennes"
    id_filiere = mapped_column(String(128), ForeignKey(Filiere.id_filiere), nullable=False)
    id_user = mapped_column(String(128), ForeignKey(User.id_user), nullable=False)
    average = mapped_column(Float, nullable=True)
    
    __table_args__ = (
            PrimaryKeyConstraint('id_filiere', 'id_user'),
    )
    
    filiere = relationship("Filiere", back_populates="moyennes")
    user = relationship("User", back_populates="moyennes")

  
class MatiereFiliere(db.Model):
    __tablename__ = "matiere_filiere"
    id_filiere = mapped_column(String(128), ForeignKey(Filiere.id_filiere), nullable=False)
    id_matiere = mapped_column(String(128), ForeignKey(Matiere.id_matiere), nullable=False)
    
    __table_args__ = (
            PrimaryKeyConstraint('id_filiere', 'id_matiere'),
    )
    
    filiere = relationship("Filiere", back_populates="matierefiliere")
    matiere = relationship("Matiere", back_populates="matierefiliere")

class Coefficient(db.Model):
    __tablename__ = "coefficients"
    id_serie = mapped_column(String(128), ForeignKey(Serie.id_serie), nullable=False)
    id_matiere = mapped_column(String(128), ForeignKey(Matiere.id_matiere), nullable=False)
    coe = mapped_column(Float, nullable=False)
    __table_args__ = (
            PrimaryKeyConstraint('id_serie', 'id_matiere'),
    )
    
    serie = relationship("Serie", back_populates="coefficient")
    matiere = relationship("Matiere", back_populates="coefficient")
    
class Note(db.Model):
    __tablename__ = "notes"
    id_user = mapped_column(String(128), ForeignKey(User.id_user), nullable=False)
    id_matiere = mapped_column(String(128), ForeignKey(Matiere.id_matiere), nullable=False)
    mark = mapped_column(Float, nullable=False)
    __table_args__ = (
            PrimaryKeyConstraint('id_user', 'id_matiere'),
    )
    
    user = relationship("User", back_populates="notes")
    matiere = relationship("Matiere", back_populates="notes")