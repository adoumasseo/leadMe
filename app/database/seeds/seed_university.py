from app.extensions import db
from app.database.models.user import User
from app.database.models.university import Universite
from app.database.models.ecole import Ecole
from app.database.models.matiere import Matiere
from app.database.models.filiere import Filiere
from app.database.models.post import Post
from app.database.models.associations import MatiereFiliere, Moyenne, Note, Coefficient, FiliereSerie

def seed_universite():
    """A fct to seed universite entity"""
    universities = [
        Universite(
            nom="Universite d'Abomey-Calavi",
            code="UAC"
        ),
        Universite(
            nom="Université de Parakou",
            code="UP"
        )
    ]
    db.session.bulk_save_objects(universities)
    db.session.commit()
    print("University seed successfully")
    