from app.extensions import db
from app.database.models.user import User
from app.database.models.university import Universite
from app.database.models.ecole import Ecole
from app.database.models.matiere import Matiere
from app.database.models.filiere import Filiere
from app.database.models.post import Post
from app.database.models.associations import MatiereFiliere, Moyenne, Note, Coefficient, FiliereSerie
import random


def seed_ecoles():
    """Seed the Ecole entity with random data."""
    universities = db.session.query(Universite).all()
    if not universities:
        print("No Universite records found. Seed Universites before Ecoles.")
        return
    
    ecoles_UAC = [
        {"nom": "Institut National de l'Eau", "code": "INE"},
        {"nom": "Ecole Nationale D'Economie Appliquée et de Management", "code": "ENEAM"},
        {"nom": "Ecole Polytechnique d'Abomey-Calavi", "code": "EPAC"},
    ]

    ecoles_UP = [
        {"nom": "Faculté d'Agronomie", "code": "FA"},
        {"nom": "Institut Universitaire de Technologie", "code": "IUT"},
        {"nom": "Faculté des Sciences Economiques et de Gestion", "code": "FASEG"},
    ]
    
    ecoles = []
    for university in universities:
        if university.code == 'UAC':
            for school in ecoles_UAC:
                ecole = Ecole(
                    nom=school["nom"],
                    code=school["code"],
                    id_universite=university.id_universite
                )   
                ecoles.append(ecole)
        elif university.code == 'UP':
            for school in ecoles_UP:
                ecole = Ecole(
                    nom=school["nom"],
                    code=school["code"],
                    id_universite=university.id_universite
                )
                ecoles.append(ecole)
                
    try:
        db.session.bulk_save_objects(ecoles)
        db.session.commit()
        print(f"Seeded {len(ecoles)} Ecoles successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding Ecoles: {e}")
