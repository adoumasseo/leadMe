from app.extensions import db
from app.database.models import Filiere, Matiere, MatiereFiliere 

def seed_series_and_matieres():
    matieres = db.session.query(Matiere).all()
    filieres = db.session.query(Filiere).all()
    if not matieres or not filieres:
        print("Matieres or Filiere not found")
    
    # Step 5: Assign random coefficients for relationships
    for matiere in matieres:
        for filiere in filieres:
            matiere_filiere = MatiereFiliere()
            matiere_filiere.id_filiere = filiere.id_filiere
            matiere_filiere.id_matiere = matiere.id_matiere
            db.session.add(matiere_filiere)

    # Step 6: Final Commit
    db.session.commit()
    print("Seeding completed successfully!")

# Call the seeder function
if __name__ == "__main__":
    seed_series_and_matieres()
