"""
Script de génération de données de test pour valider les performances
Génère 1000 consultants avec 2000 documents et 10000 missions minimum
"""

import os
import random
import sys
from datetime import date
from datetime import datetime
from datetime import timedelta

from faker import Faker

# Ajouter le dossier app au path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from database.database import get_database_session
from database.database import init_database
from database.models import CV
from database.models import BusinessManager
from database.models import Competence
from database.models import Consultant
from database.models import ConsultantBusinessManager
from database.models import ConsultantCompetence
from database.models import Mission
from database.models import Practice

fake = Faker("fr_FR")

# Listes de données réalistes
PRACTICES = [
    ("Data Engineering", "Practice spécialisée en ingénierie de données"),
    ("Data Science", "Practice d'analyse et science des données"),
    ("Cloud & DevOps", "Practice cloud et automatisation"),
    ("Frontend Development", "Practice développement front-end"),
    ("Backend Development", "Practice développement back-end"),
    ("Cybersécurité", "Practice sécurité informatique"),
    ("Consultation Métier", "Practice conseil fonctionnel"),
    ("Architecture IT", "Practice architecture technique"),
]

COMPETENCES_TECHNIQUES = [
    ("Python", "Backend", "Langage de programmation"),
    ("Java", "Backend", "Langage de programmation"),
    ("JavaScript", "Frontend", "Langage de programmation"),
    ("TypeScript", "Frontend", "Langage de programmation"),
    ("React", "Frontend", "Framework frontend"),
    ("Angular", "Frontend", "Framework frontend"),
    ("Vue.js", "Frontend", "Framework frontend"),
    ("Spring Boot", "Backend", "Framework Java"),
    ("Django", "Backend", "Framework Python"),
    ("Flask", "Backend", "Framework Python"),
    ("Node.js", "Backend", "Runtime JavaScript"),
    ("PostgreSQL", "Database", "Base de données relationnelle"),
    ("MongoDB", "Database", "Base de données NoSQL"),
    ("Redis", "Database", "Cache et base de données"),
    ("Docker", "DevOps", "Conteneurisation"),
    ("Kubernetes", "DevOps", "Orchestration de conteneurs"),
    ("AWS", "Cloud", "Amazon Web Services"),
    ("Azure", "Cloud", "Microsoft Azure"),
    ("GCP", "Cloud", "Google Cloud Platform"),
    ("Terraform", "DevOps", "Infrastructure as Code"),
    ("Jenkins", "DevOps", "CI/CD"),
    ("GitLab CI", "DevOps", "CI/CD"),
    ("Apache Spark", "Data", "Traitement de données"),
    ("Apache Kafka", "Data", "Streaming de données"),
    ("Elasticsearch", "Data", "Moteur de recherche"),
    ("Tableau", "Data", "Visualisation de données"),
    ("Power BI", "Data", "Visualisation Microsoft"),
    ("Jupyter", "Data", "Notebooks de données"),
    ("TensorFlow", "AI/ML", "Machine Learning"),
    ("PyTorch", "AI/ML", "Deep Learning"),
    ("Scikit-learn", "AI/ML", "Machine Learning"),
]

COMPETENCES_FONCTIONNELLES = [
    ("Gestion de projet", "Management", "Pilotage de projets"),
    ("Scrum Master", "Methodologie", "Agilité Scrum"),
    ("Product Owner", "Methodologie", "Gestion produit"),
    ("Business Analysis", "Analyse", "Analyse métier"),
    ("UX/UI Design", "Design", "Expérience utilisateur"),
    ("Architecture Solution", "Architecture", "Conception solution"),
    ("Conseil Transformation", "Conseil", "Accompagnement changement"),
    ("Formation", "Conseil", "Transmission de compétences"),
    ("Leadership", "Management", "Encadrement d'équipes"),
    ("Communication", "Soft Skills", "Communication interpersonnelle"),
]

CLIENTS = [
    "BNP Paribas",
    "Société Générale",
    "Crédit Agricole",
    "BPCE",
    "Crédit Mutuel",
    "AXA",
    "Allianz",
    "Generali",
    "MAIF",
    "Groupama",
    "Orange",
    "SFR",
    "Bouygues Telecom",
    "Free",
    "EDF",
    "Engie",
    "TotalEnergies",
    "Schneider Electric",
    "Airbus",
    "Thales",
    "Dassault Systèmes",
    "Capgemini",
    "Atos",
    "Sopra Steria",
    "Worldline",
    "Devoteam",
    "SNCF",
    "Air France-KLM",
    "Accor",
    "Carrefour",
    "L'Oréal",
    "Danone",
    "Michelin",
    "Peugeot PSA",
    "Ministère de l'Intérieur",
    "Ministère des Finances",
    "CNAM",
    "Pôle Emploi",
    "La Poste",
    "RATP",
    "Veolia",
    "Vinci",
]

BUSINESS_MANAGERS = [
    ("Jean", "Dupont", "j.dupont@consultator.fr"),
    ("Marie", "Martin", "m.martin@consultator.fr"),
    ("Pierre", "Bernard", "p.bernard@consultator.fr"),
    ("Sophie", "Durand", "s.durand@consultator.fr"),
    ("Marc", "Moreau", "m.moreau@consultator.fr"),
    ("Isabelle", "Petit", "i.petit@consultator.fr"),
    ("Laurent", "Robert", "l.robert@consultator.fr"),
    ("Nathalie", "Richard", "n.richard@consultator.fr"),
    ("Olivier", "Dubois", "o.dubois@consultator.fr"),
    ("Catherine", "Leroy", "c.leroy@consultator.fr"),
]


def create_practices(session):
    """Crée les practices"""
    print("🏢 Création des practices...")

    practices = []
    for nom, description in PRACTICES:
        # Vérifier si elle existe déjà
        existing = session.query(Practice).filter(Practice.nom == nom).first()
        if not existing:
            practice = Practice(
                nom=nom,
                description=description,
                responsable=fake.name(),
                date_creation=fake.date_time_between(start_date="-2y", end_date="now"),
            )
            session.add(practice)
            practices.append(practice)
        else:
            practices.append(existing)

    session.flush()
    print(f"✅ {len(practices)} practices disponibles")
    return practices


def create_competences(session):
    """Crée les compétences techniques et fonctionnelles"""
    print("🔧 Création des compétences...")

    competences = []

    # Compétences techniques
    for nom, categorie, description in COMPETENCES_TECHNIQUES:
        # Vérifier si elle existe déjà
        existing = session.query(Competence).filter(Competence.nom == nom).first()
        if not existing:
            competence = Competence(
                nom=nom,
                categorie=categorie,
                type_competence="technique",
                description=description,
                niveau_requis=random.choice(["junior", "medior", "senior"]),
            )
            session.add(competence)
            competences.append(competence)
        else:
            competences.append(existing)

    # Compétences fonctionnelles
    for nom, categorie, description in COMPETENCES_FONCTIONNELLES:
        # Vérifier si elle existe déjà
        existing = session.query(Competence).filter(Competence.nom == nom).first()
        if not existing:
            competence = Competence(
                nom=nom,
                categorie=categorie,
                type_competence="fonctionnelle",
                description=description,
                niveau_requis=random.choice(["junior", "medior", "senior"]),
            )
            session.add(competence)
            competences.append(competence)
        else:
            competences.append(existing)

    session.flush()
    print(f"✅ {len(competences)} compétences disponibles")
    return competences


def create_business_managers(session):
    """Crée les business managers"""
    print("👨‍💼 Création des business managers...")

    business_managers = []
    for prenom, nom, email in BUSINESS_MANAGERS:
        # Vérifier si il existe déjà
        existing = (
            session.query(BusinessManager)
            .filter(BusinessManager.email == email)
            .first()
        )
        if not existing:
            bm = BusinessManager(
                prenom=prenom,
                nom=nom,
                email=email,
                telephone=fake.phone_number(),
                date_creation=fake.date_time_between(start_date="-2y", end_date="now"),
                notes=fake.text(max_nb_chars=100) if random.random() < 0.3 else None,
            )
            session.add(bm)
            business_managers.append(bm)
        else:
            business_managers.append(existing)

    session.flush()
    print(f"✅ {len(business_managers)} business managers disponibles")
    return business_managers


def create_consultants(session, practices, business_managers, nb_consultants=1000):
    """Crée les consultants"""
    print(f"👥 Création de {nb_consultants} consultants...")

    consultants = []
    email_counter = 0  # Compteur pour garantir l'unicité des emails

    for i in range(nb_consultants):
        if i % 100 == 0:
            print(f"  📝 Création consultant {i+1}/{nb_consultants}")

        # Générer des données consultant
        prenom = fake.first_name()
        nom = fake.last_name()
        # Utiliser un compteur incrémental pour garantir l'unicité
        email_counter += 1
        email = f"{prenom.lower()}.{nom.lower()}.{email_counter}@email.com"

        consultant = Consultant(
            prenom=prenom,
            nom=nom,
            email=email,
            telephone=fake.phone_number(),
            salaire_actuel=random.randint(35000, 80000),
            practice_id=random.choice(practices).id,
            disponibilite=random.choice([True, False]),
            notes=fake.text(max_nb_chars=200) if random.random() < 0.2 else None,
            date_creation=fake.date_time_between(start_date="-2y", end_date="now"),
            derniere_maj=fake.date_time_between(start_date="-6m", end_date="now"),
        )

        session.add(consultant)
        consultants.append(consultant)

        # Attribution d'un business manager
        if random.random() < 0.9:  # 90% des consultants ont un BM
            bm = random.choice(business_managers)
            date_debut = fake.date_between(start_date="-1y", end_date="now")

            cbm = ConsultantBusinessManager(
                consultant=consultant,
                business_manager=bm,
                date_debut=date_debut,
                date_fin=(
                    None
                    if random.random() < 0.8
                    else fake.date_between(start_date=date_debut, end_date="now")
                ),
                commentaire=(
                    fake.text(max_nb_chars=100) if random.random() < 0.2 else None
                ),
            )
            session.add(cbm)

    session.flush()
    print(f"✅ {len(consultants)} consultants créés")
    return consultants


def create_consultant_competences(session, consultants, competences):
    """Attribue des compétences aux consultants"""
    print("🔗 Attribution des compétences aux consultants...")

    competences_count = 0

    for i, consultant in enumerate(consultants):
        if i % 200 == 0:
            print(f"  🔧 Compétences pour consultant {i+1}/{len(consultants)}")

        # Chaque consultant a entre 3 et 15 compétences
        nb_competences = random.randint(3, 15)
        consultant_competences = random.sample(competences, nb_competences)

        for competence in consultant_competences:
            cc = ConsultantCompetence(
                consultant_id=consultant.id,
                competence_id=competence.id,
                annees_experience=round(random.uniform(0.5, 10.0), 1),
                niveau_maitrise=random.choice(["debutant", "intermediaire", "expert"]),
                projets_realises=(
                    fake.text(max_nb_chars=100) if random.random() < 0.3 else None
                ),
                date_ajout=fake.date_time_between(start_date="-1y", end_date="now"),
            )
            session.add(cc)
            competences_count += 1

    session.flush()
    print(f"✅ {competences_count} attributions de compétences créées")


def create_missions(session, consultants, min_missions=10000):
    """Crée les missions pour les consultants"""
    print(f"🎯 Création d'au minimum {min_missions} missions...")

    missions_count = 0
    target_per_consultant = max(10, min_missions // len(consultants))

    for i, consultant in enumerate(consultants):
        if i % 100 == 0:
            print(f"  🎯 Missions pour consultant {i+1}/{len(consultants)}")

        # Chaque consultant a entre 5 et 20 missions
        nb_missions = random.randint(5, target_per_consultant + 10)

        for _ in range(nb_missions):
            # Dates de mission cohérentes
            date_debut = fake.date_between(start_date="-3y", end_date="now")

            # 70% de missions terminées, 30% en cours
            if random.random() < 0.7:
                date_fin = fake.date_between(start_date=date_debut, end_date="now")
                statut = "terminee"
            else:
                date_fin = None
                statut = "en_cours"

            client = random.choice(CLIENTS)

            mission = Mission(
                consultant_id=consultant.id,
                nom_mission=f"Mission {fake.word().title()} chez {client}",
                client=client,
                role=fake.job(),
                date_debut=date_debut,
                date_fin=date_fin,
                statut=statut,
                taux_journalier=random.randint(400, 1200),
                revenus_generes=random.randint(5000, 50000) if date_fin else 0,
                technologies_utilisees=", ".join(
                    random.sample(
                        [comp[0] for comp in COMPETENCES_TECHNIQUES],
                        random.randint(2, 6),
                    )
                ),
                description=fake.text(max_nb_chars=300),
            )

            session.add(mission)
            missions_count += 1

    session.flush()
    print(f"✅ {missions_count} missions créées")
    return missions_count


def create_cvs(session, consultants, min_cvs=2000):
    """Crée des entrées CV pour les consultants"""
    print(f"📄 Création d'au minimum {min_cvs} CVs...")

    cvs_count = 0
    target_per_consultant = max(2, min_cvs // len(consultants))

    for i, consultant in enumerate(consultants):
        if i % 200 == 0:
            print(f"  📄 CVs pour consultant {i+1}/{len(consultants)}")

        # Chaque consultant a entre 1 et 3 CVs
        nb_cvs = random.randint(1, target_per_consultant + 1)

        for j in range(nb_cvs):
            cv = CV(
                consultant_id=consultant.id,
                fichier_nom=f"CV_{consultant.prenom}_{consultant.nom}_{j+1}.pdf",
                fichier_path=f"/uploads/cv_{consultant.id}_{j+1}.pdf",
                contenu_extrait=fake.text(max_nb_chars=1000),
                date_upload=fake.date_time_between(start_date="-1y", end_date="now"),
                taille_fichier=random.randint(100000, 2000000),  # 100KB à 2MB
            )

            session.add(cv)
            cvs_count += 1

    session.flush()
    print(f"✅ {cvs_count} CVs créés")
    return cvs_count


def generate_test_data():
    """Génère toutes les données de test"""
    print("🚀 Génération des données de test pour validation des performances")
    print("=" * 60)

    # Initialiser la base de données
    init_database()

    start_time = datetime.now()

    with get_database_session() as session:
        try:
            # 1. Créer les données de référence
            practices = create_practices(session)
            competences = create_competences(session)
            business_managers = create_business_managers(session)

            session.commit()
            print("✅ Données de référence commitées")

            # 2. Créer les consultants
            consultants = create_consultants(
                session, practices, business_managers, 1000
            )
            session.commit()
            print("✅ Consultants committés")

            # 3. Attribuer des compétences
            create_consultant_competences(session, consultants, competences)
            session.commit()
            print("✅ Compétences consultants committées")

            # 4. Créer les missions
            missions_count = create_missions(session, consultants, 10000)
            session.commit()
            print("✅ Missions committées")

            # 5. Créer les CVs
            cvs_count = create_cvs(session, consultants, 2000)
            session.commit()
            print("✅ CVs committés")

            end_time = datetime.now()
            duration = end_time - start_time

            print("=" * 60)
            print("🎉 GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
            print(f"⏱️  Durée totale: {duration}")
            print(f"👥 Consultants: {len(consultants)}")
            print(f"🎯 Missions: {missions_count}")
            print(f"📄 CVs: {cvs_count}")
            print(f"🔧 Compétences: {len(competences)}")
            print(f"🏢 Practices: {len(practices)}")
            print(f"👨‍💼 Business Managers: {len(business_managers)}")
            print("=" * 60)

        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            session.rollback()
            raise


if __name__ == "__main__":
    generate_test_data()
