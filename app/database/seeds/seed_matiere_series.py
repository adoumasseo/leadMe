from app.extensions import db
from app.database.models import Serie, Matiere, Coefficient

def seed_series_and_matieres():
    # Step 1: Define series and their corresponding matieres with coefficients
    series_data = {
        "Serie A": {
            "Mathematics": 4.5,
            "Physics": 3.8,
            "Chemistry": 3.2,
            "Biology": 2.5,
            "History": 2.0,
            "Geography": 1.5,
        },
        "Serie B": {
            "Mathematics": 4.0,
            "Physics": 3.5,
            "Chemistry": 3.0,
            "Biology": 3.5,
            "History": 2.5,
            "Geography": 2.0,
        },
        "Serie C": {
            "Mathematics": 5.0,
            "Physics": 4.5,
            "Chemistry": 4.0,
            "Biology": 2.0,
            "History": 1.0,
            "Geography": 1.5,
        },
        "Serie D": {
            "Mathematics": 3.0,
            "Physics": 3.0,
            "Chemistry": 2.5,
            "Biology": 4.0,
            "History": 3.0,
            "Geography": 2.5,
        },
    }

    # Step 2: Create Series and Matieres
    created_series = {}
    created_matieres = {}

    for serie_name in series_data.keys():
        serie = Serie(nom=serie_name)
        db.session.add(serie)
        created_series[serie_name] = serie  # Track the created Serie

    for matiere_name in set(m for s in series_data.values() for m in s.keys()):
        matiere = Matiere(nom=matiere_name)
        db.session.add(matiere)
        created_matieres[matiere_name] = matiere  # Track the created Matiere

    # Step 3: Commit Series and Matieres to get their IDs
    db.session.commit()

    # Step 4: Assign specified coefficients to relationships
    coefficients = []
    for serie_name, matieres_with_coeffs in series_data.items():
        serie = created_series[serie_name]
        for matiere_name, coeff_value in matieres_with_coeffs.items():
            matiere = created_matieres[matiere_name]
            coefficient = Coefficient()
            coefficient.id_serie = serie.id_serie
            coefficient.id_matiere = matiere.id_matiere,
            coefficient.coe = coeff_value
            coefficients.append(coefficient)

    try:
        db.session.bulk_save_objects(coefficients)
        db.session.commit()
        print("Seeded Series, Matieres, and Coefficients successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding: {e}")

# Call the seeder function
if __name__ == "__main__":
    seed_series_and_matieres()
