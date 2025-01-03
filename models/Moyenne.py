from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash
from ..db import Base, db
from .Filiere import Filiere
from .User import User
from uuid import uuid4
from datetime import datetime

class Moyenne(db.Model):
    """Moyenne model to map the serie table
    """
    __tablename__ = 'moyenne'
    id_moyenne = mapped_column(String(128), primary_key=True, nullable=False)
    id_filiere = mapped_column(String(128), ForeignKey(Filiere.id_filiere), nullable=False)
    id_user = mapped_column(String(128), ForeignKey(User.id), nullable=False)
    moyennecalc = mapped_column(Float(), nullable=False)
    created_at = mapped_column(DateTime, default=datetime.now())
    updated_at = mapped_column(DateTime, default=datetime.now())
    deleted_at = mapped_column(DateTime, nullable=True)

    def __init__(self, id_filiere, id_user, moyennecalc):
        """Initiate the model object with column values
        """
        self.id_moyenne = str(uuid4())
        self.id_filiere = id_filiere
        self.id_user = id_user
        self.moyennecalc = moyennecalc
        self.created_at = datetime.now()

    def __str__(self):
        """Return a string representation of a Moyenne
        """
        return "Moyenne: {}".format(self.moyennecalc)

    def __repr__(self):
        """Return a string representation of a Moyenne
        """
        return "Moyenne: {}".format(self.moyennecalc)