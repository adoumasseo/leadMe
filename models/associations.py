from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash
from .Serie import Serie
from ..db import Base, db
from uuid import uuid4
from datetime import datetime

coefficient = db.Table(
  'coefficient',
  db.Column('id_matiere', String, db.ForeignKey('matiere.id_matiere')),
  db.Column('id_serie', String, db.ForeignKey('serie.id_serie')),
)

matiere_filiere = db.Table(
  'matiere_filiere',
  db.Column('id_matiere', String, db.ForeignKey('matiere.id_matiere')),
  db.Column('id_filiere', String, db.ForeignKey('filiere.id_filiere'))
)

filiere_serie = db.Table(
  'filiere_serie',
  db.Column('id_filiere', String, db.ForeignKey('filiere.id_filiere')),
  db.Column('id_serie', String, db.ForeignKey('serie.id_serie'))
)