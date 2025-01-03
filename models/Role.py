from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash
from ..db import db
from uuid import uuid4
from datetime import datetime

class Role(db.Model):
    """Role model to map the role table
    """
    __tablename__ = 'role'
    id_role = mapped_column(String(128), primary_key=True, nullable=False)
    nom = mapped_column(String(10), nullable=False)
    created_at = mapped_column(DateTime, default=datetime.now())
    updated_at = mapped_column(DateTime, default=datetime.now())
    deleted_at = mapped_column(DateTime, default=None)

    def __init__(self, nom):
        """Initiate the model object with column values
        """
        self.id_role = str(uuid4())
        self.nom = nom
        self.created_at = datetime.now()

    def __str__(self):
        """Return a string representation of a Role
        """
        return "Role: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a Role
        """
        return "Role: {}".format(self.nom)