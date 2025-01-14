from app.extensions import db
from app.database.models import Serie, Matiere, Coefficient 
import random

def seed_series_and_matieres():
    # Step 1: Define sample data
    series_data = ["Serie A", "Serie B", "Serie C", "Serie D"]
    matieres_data = ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography"]

    # Step 2: Create Series
    series = []
    for serie_name in series_data:
        serie = Serie(nom=serie_name)
        db.session.add(serie)
        series.append(serie)  # Keep track of created series

    # Step 3: Create Matieres
    matieres = []
    for matiere_name in matieres_data:
        matiere = Matiere(nom=matiere_name, coefficient=[])  # Empty coefficients initially
        db.session.add(matiere)
        matieres.append(matiere)  # Keep track of created matieres

    # Step 4: Commit Series and Matieres to get IDs
    db.session.commit()

    # Step 5: Assign random coefficients for relationships
    for serie in series:
        for matiere in matieres:
            coefficient_value = round(random.uniform(1.0, 5.0), 2)  # Random coefficient between 1.0 and 5.0
            coefficient = Coefficient()
            coefficient.id_serie = serie.id_serie
            coefficient.id_matiere = matiere.id_matiere,
            coefficient.coe = coefficient_value
            db.session.add(coefficient)

    # Step 6: Final Commit
    db.session.commit()
    print("Seeding completed successfully!")

# Call the seeder function
if __name__ == "__main__":
    seed_series_and_matieres()
