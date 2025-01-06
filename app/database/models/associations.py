from sqlalchemy.orm import mapped_column, relationship
from app.database.models.filiere import Filiere
from app.database.models.user import User
from app.extensions import db


class Moyenne(db.Model):
    __tablename__ = "moyennes"
    id_filiere = mapped_column(db.String(128), db.ForeignKey(Filiere.id_filiere), nullable=False)
    id_user = mapped_column(db.String(128), db.ForeignKey(User.id_user), nullable=False)
    average = mapped_column(db.Float, nullable=True)
    filiere = relationship("Filiere", back_populates="filieres")
    user = relationship("User", back_populates="users")