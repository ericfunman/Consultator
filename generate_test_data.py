#!/usr/bin/env python3
"""
Script pour générer 1000 consultants de test pour Consultator
Version optimisée avec données réalistes françaises
"""

import os
import random
import sys
from datetime import date, datetime, timedelta
from faker import Faker

# Ajouter le répertoire app au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app.database.database import get_database_session, init_database
from app.database.models import (
    Consultant,
    Practice,
    BusinessManager,
    Competence,
    ConsultantCompetence,
    Mission,
    Langue,
    ConsultantLangue,
    ConsultantBusinessManager,
)

# Configuration
fake = Faker("fr_FR")
NB_CONSULTANTS = 1000

# Données de référence
PRACTICES = [
    "Data Science",
    "Frontend",
    "Backend",
    "DevOps",
    "Mobile",
    "Cloud",
    "IA/ML",
    "Cybersécurité",
    "Blockchain",
    "IoT",
]

BUSINESS_MANAGERS = [
    "Marie Dubois",
    "Pierre Martin",
    "Sophie Bernard",
    "Jean Durand",
    "Claire Moreau",
    "Philippe Leroy",
    "Nathalie Rousseau",
    "Marc Petit",
]

COMPETENCES_TECH = [
    "Python",
    "JavaScript",
    "Java",
    "React",
    "Angular",
    "Vue.js",
    "Node.js",
    "Django",
    "Flask",
    "Spring Boot",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "Git",
    "Jenkins",
    "GitLab",
    "Terraform",
    "Ansible",
]

COMPETENCES_FONCTIONNELLES = [
    "Gestion de projet",
    "Architecture logicielle",
    "UX/UI Design",
    "Analyse fonctionnelle",
    "Tests automatisés",
    "Agilité",
    "Scrum",
    "DevOps",
    "Sécurité",
    "Performance",
    "Big Data",
    "Machine Learning",
]

LANGUES = [
    ("Français", "Natif"),
    ("Anglais", "Courant"),
    ("Espagnol", "Intermédiaire"),
    ("Allemand", "Notions"),
    ("Italien", "Notions"),
    ("Mandarin", "Débutant"),
]

GRADES = ["Junior", "Confirmé", "Senior", "Expert", "Principal", "Architecte"]

CLIENTS = [
    "BNP Paribas",
    "Société Générale",
    "Crédit Agricole",
    "Orange",
    "SFR",
    "Bouygues",
    "SNCF",
    "Air France",
    "Renault",
    "Peugeot",
    "L'Oréal",
    "Danone",
    "Total",
    "EDF",
    "Airbus",
    "Thales",
    "Capgemini",
    "Accenture",
]


def create_practices():
    """Créer les practices"""
    print("🏢 Création des practices...")
    practices = []

    with get_database_session() as session:
        for i, practice_name in enumerate(PRACTICES):
            existing = (
                session.query(Practice).filter(Practice.nom == practice_name).first()
            )
            if not existing:
                practice = Practice(
                    nom=practice_name,
                    description=f"Practice {practice_name}",
                    responsable=random.choice(BUSINESS_MANAGERS),
                    date_creation=datetime.now(),
                    actif=True,
                )
                session.add(practice)
                practices.append(practice)

        session.commit()
        # Récupérer toutes les practices (existantes + nouvelles)
        all_practices = session.query(Practice).all()
        print(
            f"✅ {len(practices)} nouvelles practices créées ({len(all_practices)} total)"
        )
    return all_practices


def create_business_managers():
    """Créer les business managers"""
    print("👔 Création des business managers...")
    managers = []

    with get_database_session() as session:
        for manager_name in BUSINESS_MANAGERS:
            parts = manager_name.split()
            email = f"{parts[0].lower()}.{parts[-1].lower()}@consultator.com"

            existing = (
                session.query(BusinessManager)
                .filter(BusinessManager.email == email)
                .first()
            )
            if not existing:
                manager = BusinessManager(
                    nom=parts[-1],
                    prenom=parts[0],
                    email=email,
                    telephone=fake.phone_number(),
                    actif=True,
                )
                session.add(manager)
                managers.append(manager)

        session.commit()
        # Récupérer tous les managers (existants + nouveaux)
        all_managers = session.query(BusinessManager).all()
        print(
            f"✅ {len(managers)} nouveaux business managers créés ({len(all_managers)} total)"
        )
    return all_managers


def create_competences():
    """Créer les compétences"""
    print("⚡ Création des compétences...")
    competences = []

    with get_database_session() as session:
        # Compétences techniques
        for comp_name in COMPETENCES_TECH:
            existing = (
                session.query(Competence).filter(Competence.nom == comp_name).first()
            )
            if not existing:
                competence = Competence(
                    nom=comp_name,
                    categorie="Technique",
                    description=f"Compétence technique {comp_name}",
                )
                session.add(competence)
                competences.append(competence)

        # Compétences fonctionnelles
        for comp_name in COMPETENCES_FONCTIONNELLES:
            existing = (
                session.query(Competence).filter(Competence.nom == comp_name).first()
            )
            if not existing:
                competence = Competence(
                    nom=comp_name,
                    categorie="Fonctionnelle",
                    description=f"Compétence fonctionnelle {comp_name}",
                )
                session.add(competence)
                competences.append(competence)

        session.commit()
        # Récupérer toutes les compétences (existantes + nouvelles)
        all_competences = session.query(Competence).all()
        print(
            f"✅ {len(competences)} nouvelles compétences créées ({len(all_competences)} total)"
        )
    return all_competences


def create_langues():
    """Créer les langues"""
    print("🌍 Création des langues...")
    langues = []

    with get_database_session() as session:
        for langue_nom, _ in LANGUES:
            if not session.query(Langue).filter(Langue.nom == langue_nom).first():
                langue = Langue(nom=langue_nom, code_iso=langue_nom[:2].lower())
                session.add(langue)
                langues.append(langue)

        session.commit()
        print(f"✅ {len(langues)} langues créées")
    return langues


def create_consultants(practices, managers, competences, langues):
    """Créer 1000 consultants avec données réalistes"""
    print(f"👥 Génération de {NB_CONSULTANTS} consultants...")

    consultants_created = 0
    batch_size = 50

    for batch in range(0, NB_CONSULTANTS, batch_size):
        batch_consultants = []

        with get_database_session() as session:
            # Récupérer les IDs des practices, managers, etc.
            practice_ids = [p.id for p in session.query(Practice).all()]
            manager_ids = [m.id for m in session.query(BusinessManager).all()]
            competence_ids = [c.id for c in session.query(Competence).all()]
            langue_ids = [l.id for l in session.query(Langue).all()]

            for i in range(min(batch_size, NB_CONSULTANTS - batch)):
                consultant_number = batch + i + 1

                # Données personnelles
                sexe = random.choice(["M", "F"])
                if sexe == "M":
                    prenom = fake.first_name_male()
                else:
                    prenom = fake.first_name_female()

                nom = fake.last_name()

                # Calcul de l'âge et de l'expérience
                age = random.randint(22, 60)
                experience = min(age - 22, random.randint(0, 35))

                # Grade basé sur l'expérience
                if experience < 2:
                    grade = "Junior"
                elif experience < 5:
                    grade = "Confirmé"
                elif experience < 10:
                    grade = "Senior"
                elif experience < 15:
                    grade = "Expert"
                else:
                    grade = random.choice(["Principal", "Architecte"])

                # Données de contact avec numéro unique
                email = f"{prenom.lower()}.{nom.lower()}.{consultant_number:04d}@consultator-test.com"

                # Salaire basé sur le grade
                salaire_base = {
                    "Junior": random.randint(35000, 45000),
                    "Confirmé": random.randint(45000, 60000),
                    "Senior": random.randint(60000, 80000),
                    "Expert": random.randint(80000, 100000),
                    "Principal": random.randint(100000, 130000),
                    "Architecte": random.randint(120000, 150000),
                }

                consultant = Consultant(
                    nom=nom,
                    prenom=prenom,
                    email=email,
                    telephone=fake.phone_number(),
                    date_entree_societe=fake.date_between(
                        start_date="-10y", end_date="today"
                    ),
                    grade=grade,
                    practice_id=random.choice(practice_ids),
                    salaire_actuel=salaire_base[grade],
                    disponibilite=random.choice([True, False]),
                )

                session.add(consultant)
                session.flush()  # Pour obtenir l'ID

                # Affecter un business manager au consultant
                manager_id = random.choice(manager_ids)
                consultant_manager = ConsultantBusinessManager(
                    consultant_id=consultant.id,
                    business_manager_id=manager_id,
                    date_debut=consultant.date_entree_societe
                    or fake.date_between(start_date="-5y", end_date="today"),
                )
                session.add(consultant_manager)

                # Compétences (3-8 par consultant)
                nb_competences = random.randint(3, 8)
                consultant_competences = random.sample(competence_ids, nb_competences)

                for comp_id in consultant_competences:
                    consultant_comp = ConsultantCompetence(
                        consultant_id=consultant.id,
                        competence_id=comp_id,
                        niveau_maitrise=random.choice(
                            ["debutant", "intermediaire", "avance", "expert"]
                        ),
                        annees_experience=random.randint(0, min(experience, 15)),
                    )
                    session.add(consultant_comp)

                # Langues (1-3 par consultant)
                nb_langues = random.randint(1, min(3, len(langue_ids)))
                consultant_langues = random.sample(langue_ids, nb_langues)

                for langue_id in consultant_langues:
                    niveau_num = random.randint(1, 5)  # 1=Débutant à 5=Natif
                    consultant_langue = ConsultantLangue(
                        consultant_id=consultant.id,
                        langue_id=langue_id,
                        niveau=niveau_num,
                    )
                    session.add(consultant_langue)

                batch_consultants.append(consultant)

            session.commit()
            consultants_created += len(batch_consultants)
            print(
                f"✅ Batch {batch//batch_size + 1}: {len(batch_consultants)} consultants créés (Total: {consultants_created})"
            )

    return consultants_created


def create_missions(nb_missions=200):
    """Créer des missions d'exemple"""
    print(f"📋 Création de {nb_missions} missions...")

    with get_database_session() as session:
        consultant_ids = [c.id for c in session.query(Consultant).all()]

        for i in range(nb_missions):
            consultant_id = random.choice(consultant_ids)

            # Dates de mission
            date_debut = fake.date_between(start_date="-2y", end_date="today")
            duree_jours = random.randint(30, 365)
            date_fin = date_debut + timedelta(days=duree_jours)

            mission = Mission(
                consultant_id=consultant_id,
                client=random.choice(CLIENTS),
                nom_mission=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                date_debut=date_debut,
                date_fin=date_fin,
                taux_journalier=random.randint(400, 1200),
                statut=random.choice(["En cours", "Terminée", "Planifiée"]),
            )
            session.add(mission)

        session.commit()
        print(f"✅ {nb_missions} missions créées")


def main():
    """Script principal"""
    print("🚀 Génération de données de test pour Consultator")
    print("=" * 60)

    # Initialiser la base de données
    print("🔧 Initialisation de la base de données...")
    init_database()
    print("✅ Base de données initialisée")

    # Créer les données de référence
    practices = create_practices()
    managers = create_business_managers()
    competences = create_competences()
    langues = create_langues()

    # Créer les consultants
    nb_consultants = create_consultants(practices, managers, competences, langues)

    # Créer des missions
    create_missions()

    print("\n" + "=" * 60)
    print(f"🎉 Génération terminée avec succès !")
    print(f"📊 Résumé:")
    print(f"   • {len(PRACTICES)} practices")
    print(f"   • {len(BUSINESS_MANAGERS)} business managers")
    print(f"   • {len(COMPETENCES_TECH + COMPETENCES_FONCTIONNELLES)} compétences")
    print(f"   • {len(LANGUES)} langues")
    print(f"   • {nb_consultants} consultants")
    print(f"   • 200 missions")
    print("=" * 60)


if __name__ == "__main__":
    main()
