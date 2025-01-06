from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime
from uuid import uuid4
from app.extensions import db
from app.database.models.user import User

class Post(db.Model):
    __tablename__ = 'posts'
    id_post = mapped_column(db.String(128), primary_key=True, nullable=False, default=lambda: str(uuid4()))
    titre = mapped_column(db.String(255), nullable=False)
    contenu = mapped_column(db.String, nullable=False)
    adresse = mapped_column(db.String, nullable=True)
    imagePath = mapped_column(db.String(255), nullable=True)
    created_at = mapped_column(db.DateTime, default=datetime.utcnow)
    updated_at = mapped_column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = mapped_column(db.DateTime, nullable=True)
    user_id = mapped_column(db.String(128), db.ForeignKey(User.id_user), nullable=False)

    user = relationship('User', back_populates='posts')

    def __init__(self, titre, contenu, adresse, imagePath, user_id):
        self.titre = titre
        self.adresse = adresse
        self.contenu = contenu
        self.imagePath = imagePath
        self.user_id = user_id

    def __repr__(self):
        return f"<Post {self.titre}>"
