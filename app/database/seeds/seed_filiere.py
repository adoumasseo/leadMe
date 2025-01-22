from app.extensions import db
from app.database.models.filiere import Filiere
from app.database.models.ecole import Ecole


def seed_filieres():
    """Seed the Filiere entity with provided data."""
    ecoles = db.session.query(Ecole).all()
    if not ecoles:
        print("No Ecole records found. Seed Ecoles before Filieres.")
        return

    # Define filieres for specific ecoles
    filieres_data = {
        "INE": [
            {
                "nom": "Hydrologie quantitative et Gestion intégrée des Ressources",
                "debouches": "Hydrologues, hydrogéologues ; Chimistes des eaux ; auto-emploi;",
                "bourses": 30,
                "semi_bourses": 8,
            },
            {
                "nom": "Hydrogéologie et Gestion intégrée des Ressources",
                "debouches": "Hydrologues, hydrogéologues ; Chimistes des eaux ; auto-emploi;",
                "bourses": 18,
                "semi_bourses": 5,
            },
            {
                "nom": "Génie rural et Maîtrise de l’Eau",
                "debouches": "Hydrologues, hydrogéologues ; Chimistes des eaux ; auto-emploi;",
                "bourses": 14,
                "semi_bourses": 4,
            },
        ],
        "ENEAM": [
            {
                "nom": "Assurance",
                "debouches": "Chargés de clientèle; Conseillers en négoce; Gestionnaire de patrimoine.",
                "bourses": 9,
                "semi_bourses": 3,
            },
            {
                "nom": "Analyse Informatique et Programmation",
                "debouches": "Technicien en réseaux informatiques ;Technicien en maintenance informatique ;Développeur d’applications (Desktop, Web, Mobile).",
                "bourses": 30,
                "semi_bourses": 7,
            },
        ],
        "EPAC": [
            {
                "nom": "Analyse Biomédicale",
                "debouches": "Technicien de laboratoire des centres de santé ; Assistant de recherche.",
                "bourses": 18,
                "semi_bourses": 7,
            },
            {
                "nom": "Génie d’Imagerie médicale et de Radiobiologie",
                "debouches": "Chefs chantiers; Techniciens d’étude en entreprise; Conducteurs des travaux; Laboratoires.",
                "bourses": 18,
                "semi_bourses": 7,
            },
        ],
        "FA": [
            {
                "nom": "Sciences et Techniques de Production Végétale",
                "debouches": "Technicien/Encadreur en production végétale; protection des végétaux; sélection variétale; gestion durable des terres; Enseignant des lycées agricoles.",
                "bourses": 19,
                "semi_bourses": 6,
            },
            {
                "nom": "Aménagement et Gestion des Ressources Naturelles",
                "debouches": "Technicien en aménagement et gestion des aires protégées; Cadre des eaux et forêts; Assistance dans les études de gestion et de conservation des aires protégées; Entrepreneur Agricole; Conseiller Agricole; Enseignant des lycées agricoles.",
                "bourses": 19,
                "semi_bourses": 5,
            },
        ],
        "IUT": [
            {
                "nom": "Gestion des Banques",
                "debouches": "Organismes financiers ou de gestion (établissement de crédits, entreprises commerciales de banque).",
                "bourses": 18,
                "semi_bourses": 6,
            },
            {
                "nom": "Informatique de Gestion",
                "debouches": "Technicien en réseaux informatiques ;Technicien en maintenance informatique ;Développeur d’applications (Desktop, Web, Mobile).",
                "bourses": 55,
                "semi_bourses": 14,
            },
        ],
        "FASEG": [
            {
                "nom": "Economie et Finance Inter-nationales",
                "debouches": "Auto emploi ; Cabinets Conseils en Politiques Economiques et Monétaires; Cabinets Conseils en Projets de Développement.",
                "bourses": 18,
                "semi_bourses": 6,
            },
            {
                "nom": "Economie et Finance des Collectivités Locales",
                "debouches": "Auto emploi ; Cabinets Conseils en Politiques Economiques et Monétaires; Cabinets Conseils en Projets de Développement.",
                "bourses": 55,
                "semi_bourses": 14,
            },
        ],
    }

    filieres = []

    for ecole in ecoles:
        ecole_filieres = filieres_data.get(ecole.code, [])
        for data in ecole_filieres:
            filiere = Filiere(
                nom=data["nom"],
                debouches=data["debouches"],
                bourses=data["bourses"],
                semi_bourses=data["semi_bourses"],
                ecole_id=ecole.id_ecole,
            )
            filieres.append(filiere)

    try:
        db.session.bulk_save_objects(filieres)
        db.session.commit()
        print(f"Seeded {len(filieres)} Filieres successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding Filieres: {e}")
