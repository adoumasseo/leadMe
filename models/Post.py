from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime
from .User import User
from uuid import uuid4
from ..db import db

class Post(db.Model):
    __tablename__ = 'posts'
    id_post = mapped_column(String(128), primary_key=True, nullable=False, default=lambda: str(uuid4()))
    titre = mapped_column(String(255), nullable=False)
    contenu = mapped_column(String, nullable=False)
    adresse = mapped_column(String, nullable=True)
    imagePath = mapped_column(String(255), nullable=True)
    created_at = mapped_column(DateTime, default=datetime.now)
    updated_at = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = mapped_column(DateTime, nullable=True)
    user_id = mapped_column(String(128), ForeignKey(User.id), nullable=False)

    user = relationship('User', back_populates='posts')

    def __init__(self, titre, contenu, adresse, imagePath, user_id):
        self.titre = titre
        self.adresse = adresse
        self.contenu = contenu
        self.imagePath = imagePath
        self.user_id = user_id

    def __repr__(self):
        return f"<Post {self.titre}>"
