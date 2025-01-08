from app.extensions import db
from app.database.models.user import User
from app.database.models.university import Universite
from app.database.models.ecole import Ecole
from app.database.models.matiere import Matiere
from app.database.models.filiere import Filiere
from app.database.models.post import Post
from app.database.models.associations import MatiereFiliere, Moyenne, Note, Coefficient
import random


def seed_ecoles():
    """Seed the Ecole entity with random data."""
    universities = db.session.query(Universite).all()
    if not universities:
        print("No Universite records found. Seed Universites before Ecoles.")
        return

    ecoles = []
    for university in universities:
        ecole = Ecole(
            nom=f"Ecole of {university.nom} {random.randint(0, 1000)}",
            code=f"Code-{university.id_universite}-{random.randint(100, 999)}",
            university=university
        )
        ecoles.append(ecole)
    
    try:
        db.session.bulk_save_objects(ecoles)
        db.session.commit()
        print(f"Seeded {len(ecoles)} Ecoles successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding Ecoles: {e}")
