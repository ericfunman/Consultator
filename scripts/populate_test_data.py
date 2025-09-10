#!/usr/bin/env python3
"""
Script pour peupler la base de données avec des données de test
Usage: python scripts/populate_test_data.py
"""

import os
import random
import sys
from datetime import date
from datetime import datetime
from datetime import timedelta

from app.database.database import get_session
from app.database.database import init_database
from app.database.models import Competence
from app.database.models import Consultant
from app.database.models import ConsultantCompetence
from app.database.models import Mission

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_test_consultants():
    """Crée des consultants de test"""

    base_consultants = [
        {
            "nom": "Dupont",
            "prenom": "Jean",
            "notes": "Consultant senior avec expertise en développement web",
        },
        {
            "nom": "Martin",
            "prenom": "Marie",
            "notes": "Spécialiste en data science et machine learning",
        },
        {
            "nom": "Bernard",
            "prenom": "Pierre",
            "notes": "Expert en cybersécurité et infrastructure cloud",
        },
        {
            "nom": "Durand",
            "prenom": "Sophie",
            "notes": "Consultante fonctionnelle spécialisée en finance",
        },
        {
            "nom": "Moreau",
            "prenom": "Paul",
            "notes": "Développeur full-stack avec expertise mobile",
        },
        {"nom": "Petit", "prenom": "Luc", "notes": "Consultant BI junior"},
        {"nom": "Roux", "prenom": "Julie", "notes": "Experte Power BI et SQL"},
        {"nom": "Lefevre", "prenom": "Nicolas", "notes": "Data engineer Python/Cloud"},
        {"nom": "Garnier", "prenom": "Claire", "notes": "Chef de projet digital"},
        {"nom": "Faure", "prenom": "Hugo", "notes": "Consultant DevOps"},
        {"nom": "Chevalier", "prenom": "Emma", "notes": "Analyste fonctionnelle"},
        {"nom": "Lambert", "prenom": "Lucas", "notes": "Développeur backend Java"},
        {"nom": "Bonnet", "prenom": "Camille", "notes": "Consultante cloud AWS"},
        {"nom": "Francois", "prenom": "Alice", "notes": "Data scientist IA"},
        {"nom": "Legrand", "prenom": "Antoine", "notes": "Expert sécurité SI"},
    ]

    consultants_data = []
    for i, base in enumerate(base_consultants):
        email = f"{base['prenom'].lower()}.{base['nom'].lower()}@email.com"
        telephone = f"01.{
            random.randint(
                10,
                99)}.{
            random.randint(
                10,
                99)}.{
                    random.randint(
                        10,
                        99)}.{
                            random.randint(
                                10,
                                99)}"
        salaire = float(random.randint(42000, 60000))
        disponibilite = random.choice([True, False])
        consultants_data.append(
            {
                "nom": base["nom"],
                "prenom": base["prenom"],
                "email": email,
                "telephone": telephone,
                "salaire_actuel": salaire,
                "disponibilite": disponibilite,
                "notes": base["notes"],
            }
        )

    session = get_session()
    consultants = []

    try:
        for data in consultants_data:
            # Vérifier si le consultant existe déjà
            existing = session.query(Consultant).filter_by(email=data["email"]).first()
            if not existing:
                consultant = Consultant(**data)
                session.add(consultant)
                consultants.append(consultant)

        session.commit()

        # Récupérer tous les consultants après commit pour avoir les IDs
        all_consultants = session.query(Consultant).all()
        print(
            f"✅ {
                len(consultants)} nouveaux consultants créés ({
                len(all_consultants)} total)"
        )
        return all_consultants

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur lors de la création des consultants: {e}")
        return []
    finally:
        session.close()


def create_test_competences():
    """Crée des compétences de test"""

    competences_data = [
        {
            "nom": "Python",
            "categorie": "Backend",
            "type_competence": "technique",
            "description": "Langage de programmation",
            "niveau_requis": "medior",
        },
        {
            "nom": "JavaScript",
            "categorie": "Frontend",
            "type_competence": "technique",
            "description": "Langage web",
            "niveau_requis": "junior",
        },
        {
            "nom": "React",
            "categorie": "Frontend",
            "type_competence": "technique",
            "description": "Framework JavaScript",
            "niveau_requis": "medior",
        },
        {
            "nom": "SQL",
            "categorie": "Data",
            "type_competence": "technique",
            "description": "Base de données",
            "niveau_requis": "junior",
        },
        {
            "nom": "Docker",
            "categorie": "DevOps",
            "type_competence": "technique",
            "description": "Conteneurisation",
            "niveau_requis": "medior",
        },
        {
            "nom": "AWS",
            "categorie": "Cloud",
            "type_competence": "technique",
            "description": "Amazon Web Services",
            "niveau_requis": "senior",
        },
        {
            "nom": "Agile Scrum",
            "categorie": "Méthodologie",
            "type_competence": "fonctionnelle",
            "description": "Méthode agile",
            "niveau_requis": "junior",
        },
        {
            "nom": "Finance",
            "categorie": "Domaine",
            "type_competence": "fonctionnelle",
            "description": "Secteur financier",
            "niveau_requis": "senior",
        },
    ]

    session = get_session()
    competences = []

    try:
        for data in competences_data:
            # Vérifier si la compétence existe déjà
            existing = session.query(Competence).filter_by(nom=data["nom"]).first()
            if not existing:
                competence = Competence(**data)
                session.add(competence)
                competences.append(competence)

        session.commit()

        # Récupérer toutes les compétences après commit
        all_competences = session.query(Competence).all()
        print(
            f"✅ {
                len(competences)} nouvelles compétences créées ({
                len(all_competences)} total)"
        )
        return all_competences

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur lors de la création des compétences: {e}")
        return []
    finally:
        session.close()


def create_test_missions(consultants):
    """Crée des missions de test pour les consultants"""

    if not consultants:
        print("⚠️ Aucun consultant disponible pour créer des missions")
        return []

    entreprises = [
        "BNP Paribas",
        "Société Générale",
        "AXA",
        "Orange",
        "Airbus",
        "Renault",
    ]
    types_mission = [
        "Développement web",
        "Analyse de données",
        "Conseil stratégique",
        "Formation technique",
        "Audit sécurité",
    ]

    session = get_session()
    missions = []

    try:
        for consultant in consultants:
            # Créer 1-2 missions par consultant
            nb_missions = random.randint(1, 2)

            for i in range(nb_missions):
                # Dates de mission
                date_debut = date.today() - timedelta(days=random.randint(30, 365))
                duree = random.randint(30, 180)  # 1-6 mois
                date_fin = date_debut + timedelta(days=duree)

                # Déterminer le statut selon les dates
                if date_fin < date.today():
                    statut = "terminee"
                elif date_debut <= date.today() <= date_fin:
                    statut = "en_cours"
                else:
                    statut = "planifiee"

                mission_data = {
                    "consultant_id": consultant.id,
                    "nom_mission": f"{random.choice(types_mission)} - Mission {i + 1}",
                    "client": random.choice(entreprises),
                    "role": f"Consultant {random.choice(['Senior', 'Junior', 'Lead'])}",
                    "date_debut": date_debut,
                    "date_fin": date_fin,
                    "statut": statut,
                    "taux_journalier": float(random.randint(400, 800)),
                    "revenus_generes": float(random.randint(10000, 50000)),
                    "technologies_utilisees": "Python, SQL, Docker",
                    "description": f"Mission de {random.choice(types_mission).lower()} pour {random.choice(entreprises)}",
                }

                mission = Mission(**mission_data)
                session.add(mission)
                missions.append(mission)

        session.commit()
        print(f"✅ {len(missions)} missions créées")
        return missions

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur lors de la création des missions: {e}")
        return []
    finally:
        session.close()


def create_consultant_competences(consultants, competences):
    """Associe les consultants aux compétences"""

    if not consultants or not competences:
        print(
            "⚠️ Pas assez de données pour créer les associations consultant-compétences"
        )
        return []

    session = get_session()
    associations = []

    try:
        for consultant in consultants:
            # Chaque consultant a 3-5 compétences
            nb_competences = random.randint(3, 5)
            selected_competences = random.sample(
                competences, min(nb_competences, len(competences))
            )

            for competence in selected_competences:
                association_data = {
                    "consultant_id": consultant.id,
                    "competence_id": competence.id,
                    "annees_experience": round(random.uniform(0.5, 8.0), 1),
                    "niveau_maitrise": random.choice(
                        ["debutant", "intermediaire", "expert"]
                    ),
                    "projets_realises": f"Projet {random.randint(1, 10)}, Projet {random.randint(11, 20)}",
                }

                # Vérifier si l'association existe déjà
                existing = (
                    session.query(ConsultantCompetence)
                    .filter_by(consultant_id=consultant.id, competence_id=competence.id)
                    .first()
                )

                if not existing:
                    association = ConsultantCompetence(**association_data)
                    session.add(association)
                    associations.append(association)

        session.commit()
        print(f"✅ {len(associations)} associations consultant-compétence créées")
        return associations

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur lors de la création des associations: {e}")
        return []
    finally:
        session.close()


def main():
    """Fonction principale"""
    print("🚀 Initialisation des données de test...")

    # Initialiser la base de données
    if not init_database():
        print("❌ Échec de l'initialisation de la base de données")
        return

    # Créer les données de test
    print("\n📊 Création des données de test...")

    consultants = create_test_consultants()
    competences = create_test_competences()
    missions = create_test_missions(consultants)
    associations = create_consultant_competences(consultants, competences)

    print("\n✅ Données de test créées avec succès !")
    print(f"   - {len(consultants)} consultants")
    print(f"   - {len(competences)} compétences")
    print(f"   - {len(missions)} missions")
    print(f"   - {len(associations)} associations consultant-compétence")
    print("\n🌐 Vous pouvez maintenant tester le chatbot !")


if __name__ == "__main__":
    main()
