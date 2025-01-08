from app.extensions import db
from app.database.models.user import User
from app.database.models.university import Universite
from app.database.models.ecole import Ecole
from app.database.models.matiere import Matiere
from app.database.models.filiere import Filiere
from app.database.models.post import Post
from app.database.models.associations import MatiereFiliere, Moyenne, Note, Coefficient
import random

def seed_filieres():
    """Seed the Filiere entity with random data."""
    ecoles = db.session.query(Ecole).all()
    if not ecoles:
        print("No Ecole records found. Seed Ecoles before Filieres.")
        return

    filieres = []
    possible_filiere_names = [
        "Informatique", "Biologie", "Gestion", "Marketing", 
        "Chimie", "Droit", "Architecture", "Médecine"
    ]
    debouches_examples = [
        "Industrie", "Recherche", "Entrepreneuriat", "Administration"
    ]
    
    for ecole in ecoles:
        for _ in range(random.randint(2, 5)):  # Create 2 to 5 filieres per ecole
            nom = random.choice(possible_filiere_names)
            debouches = random.choice(debouches_examples)
            bourses = random.randint(5, 50)  # Random number of bourses
            semi_bourses = random.randint(10, 100)  # Random number of semi-bourses
            
            filiere = Filiere(
                nom=f"{nom} - {ecole.nom}",
                debouches=debouches,
                bourses=bourses,
                semi_bourses=semi_bourses,
                ecole=ecole
            )
            filieres.append(filiere)

    try:
        db.session.bulk_save_objects(filieres)
        db.session.commit()
        print(f"Seeded {len(filieres)} Filieres successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding Filieres: {e}")
