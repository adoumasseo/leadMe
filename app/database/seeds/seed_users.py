from app.extensions import db
from app.database.models.user import User
from app.database.models.university import Universite
from app.database.models.ecole import Ecole
from app.database.models.matiere import Matiere
from app.database.models.filiere import Filiere
from app.database.models.post import Post
from app.database.models.associations import MatiereFiliere, Moyenne, Note, Coefficient
from faker import Faker

fake = Faker()

def seed_users():
    """Function to seed the database with sample users."""
    users = [
        User(
            prenom="ADMIN",
            nom="ADMIN",
            matricule=None,
            email=fake.email(),
            password=fake.password(),
            serie=None,
            role="admin"
        ),
        User(
            prenom="Ortniel",
            nom="ADOUMASSE",
            matricule=None,
            email="adoumasseo@gmail.com",
            password="admin@admin",
            serie=None,
            role="admin"
        )
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Seeded users table successfully!")

