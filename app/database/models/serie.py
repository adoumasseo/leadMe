from sqlalchemy.orm import  mapped_column
from app.extensions import db
from uuid import uuid4
from datetime import datetime

class Serie(db.Model):
    """Serie model to map the serie table
    """
    __tablename__ = 'serie'
    id_serie = mapped_column(db.String(128), primary_key=True, nullable=False)
    nom = mapped_column(db.String(10), nullable=False)
    created_at = mapped_column(db.DateTime, default=datetime.utcnow())
    updated_at = mapped_column(db.DateTime, default=datetime.utcnow())
    deleted_at = mapped_column(db.DateTime, default=None)
    
    users = db.relationship("User", back_populates="serie")
    
    def __init__(self, nom):
        """Initiate the model object with column values
        """
        self.id_serie = str(uuid4())
        self.nom = nom
        self.created_at = datetime.utcnow()

    def __str__(self):
        """Return a string representation of a serie
        """
        return "Serie: {}".format(self.nom)

    def __repr__(self):
        """Return a string representation of a serie
        """
        return "Serie: {}".format(self.nom)
        