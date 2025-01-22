from app.extensions import db
from app.database.models import Filiere, Matiere, MatiereFiliere

def seed_filiere_and_matieres():
    # Define specific Filiere-Matiere relationships
    filiere_matiere_map = {
        "Hydrologie quantitative et Gestion intégrée des Ressources": ["Mathématiques", "PCT", "SVT"],
        "Hydrogéologie et Gestion intégrée des Ressources":  ["Mathématiques", "PCT", "SVT"],
        "Génie rural et Maîtrise de l’Eau": ["Mathématiques", "PCT", "SVT"],
        "Assurance": ["Mathématiques", "Anglais", "Français"],
        "Analyse Informatique et Programmation": ["Mathématiques", "Anglais", "Français"],
        "Analyse Biomédicale": ["Mathématiques", "PCT", "SVT"],
        "Génie d’Imagerie médicale et de Radiobiologie": ["Mathématiques", "PCT", "SVT"],
        "Sciences et Techniques de Production Végétale": ["Mathématiques", "PCT", "SVT"],
        "Aménagement et Gestion des Ressources Naturelles": ["Mathématiques", "PCT", "SVT"],
        "Gestion des Banques": ["Mathématiques", "Anglais", "Français"],
        "Informatique de Gestion": ["Mathématiques", "Anglais", "Français"],
        "Economie et Finance Inter-nationales": ["Mathématiques", "Anglais", "Français"],
        "Economie et Finance des Collectivités Locales": ["Mathématiques", "Anglais", "Français"],
    }

    # Fetch all Filieres and Matieres from the database
    filieres = {f.nom: f for f in db.session.query(Filiere).all()}
    matieres = {m.nom: m for m in db.session.query(Matiere).all()}

    if not filieres or not matieres:
        print("No Filieres or Matieres found in the database.")
        return

    # Create the MatiereFiliere relationships
    matiere_filiere_relationships = []
    for filiere_name, matiere_names in filiere_matiere_map.items():
        filiere = filieres.get(filiere_name)
        if not filiere:
            print(f"Filiere '{filiere_name}' not found in the database. Skipping.")
            continue

        for matiere_name in matiere_names:
            matiere = matieres.get(matiere_name)
            if not matiere:
                print(f"Matiere '{matiere_name}' not found in the database. Skipping.")
                continue

            matiere_filiere = MatiereFiliere()
            matiere_filiere.id_filiere = filiere.id_filiere
            matiere_filiere.id_matiere = matiere.id_matiere
            matiere_filiere_relationships.append(matiere_filiere)

    # Add all relationships to the database
    try:
        db.session.bulk_save_objects(matiere_filiere_relationships)
        db.session.commit()
        print("Seeded Filiere-Matiere relationships successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding Filiere-Matiere relationships: {e}")

# Call the seeder function
if __name__ == "__main__":
    seed_filiere_and_matieres()
