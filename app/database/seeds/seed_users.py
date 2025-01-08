from app.extensions import db
from app.database.models.user import User
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
        )
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Seeded users table successfully!")
