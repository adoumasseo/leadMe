from app.extensions import db
from app.database.models import Filiere, Serie, FiliereSerie

def seed_filiere_and_serie():
    series = db.session.query(Serie).all()
    filieres = db.session.query(Filiere).all()
    if not series or not filieres:
        print("Matieres or Filiere not found")
    
    # Step 5: Assign random coefficients for relationships
    for filiere in  filieres:
        for serie in series:
            filiere_serie = FiliereSerie()
            filiere_serie.id_filiere = filiere.id_filiere
            filiere_serie.id_serie = serie.id_serie
            db.session.add(filiere_serie)

    # Step 6: Final Commit
    db.session.commit()
    print("Seeding completed successfully!")

# Call the seeder function
if __name__ == "__main__":
    seed_filiere_and_serie()
