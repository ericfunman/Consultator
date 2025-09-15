"""
Script simple pour générer des données de test de base
"""

import sys
import os
from datetime import datetime
from faker import Faker

# Ajouter le dossier app au path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.database.database import get_database_session, init_database
from app.database.models import Practice, BusinessManager, Consultant, Competence

fake = Faker("fr_FR")

def create_basic_data():
    """Crée des données de test de base"""
    print("🚀 Génération de données de test simples")
    print("=" * 50)

    # Initialiser la base de données
    init_database()

    # Générer un suffixe unique pour éviter les conflits
    import time
    unique_suffix = str(int(time.time()))[-4:]  # 4 derniers chiffres du timestamp

    with get_database_session() as session:
        try:
            # 1. Créer quelques practices
            print("🏢 Création des practices...")
            practices_data = [
                (f"Data Engineering {unique_suffix}", "Ingénierie des données"),
                (f"Data Science {unique_suffix}", "Science des données"),
                (f"Cloud & DevOps {unique_suffix}", "Cloud et automatisation"),
                (f"Frontend Development {unique_suffix}", "Développement frontend"),
                (f"Backend Development {unique_suffix}", "Développement backend")
            ]

            practices = []
            for nom, description in practices_data:
                practice = Practice(
                    nom=nom,
                    description=description,
                    responsable=fake.name(),
                    actif=True,
                    date_creation=datetime.now()
                )
                session.add(practice)
                practices.append(practice)

            session.commit()
            print(f"✅ {len(practices)} practices créées")

            # 2. Créer quelques business managers
            print("👨‍💼 Création des business managers...")
            bm_data = [
                ("Dupont", "Jean", f"j.dupont{unique_suffix}@consultator.fr"),
                ("Martin", "Marie", f"m.martin{unique_suffix}@consultator.fr"),
                ("Bernard", "Pierre", f"p.bernard{unique_suffix}@consultator.fr"),
                ("Durand", "Sophie", f"s.durand{unique_suffix}@consultator.fr"),
                ("Moreau", "Marc", f"m.moreau{unique_suffix}@consultator.fr")
            ]

            business_managers = []
            for nom, prenom, email in bm_data:
                bm = BusinessManager(
                    nom=nom,
                    prenom=prenom,
                    email=email,
                    telephone=fake.phone_number(),
                    actif=True,
                    date_creation=datetime.now()
                )
                session.add(bm)
                business_managers.append(bm)

            session.commit()
            print(f"✅ {len(business_managers)} business managers créés")

            # 3. Créer quelques consultants
            print("👥 Création des consultants...")
            consultants_data = [
                ("Dupont", "Jean", f"jean.dupont{unique_suffix}@email.com", 65000),
                ("Martin", "Marie", f"marie.martin{unique_suffix}@email.com", 58000),
                ("Bernard", "Pierre", f"pierre.bernard{unique_suffix}@email.com", 72000),
                ("Durand", "Sophie", f"sophie.durand{unique_suffix}@email.com", 55000),
                ("Moreau", "Marc", f"marc.moreau{unique_suffix}@email.com", 68000),
                ("Petit", "Isabelle", f"isabelle.petit{unique_suffix}@email.com", 61000),
                ("Robert", "Laurent", f"laurent.robert{unique_suffix}@email.com", 69000),
                ("Richard", "Nathalie", f"nathalie.richard{unique_suffix}@email.com", 56000),
                ("Dubois", "Olivier", f"olivier.dubois{unique_suffix}@email.com", 73000),
                ("Leroy", "Catherine", f"catherine.leroy{unique_suffix}@email.com", 59000)
            ]

            consultants = []
            for nom, prenom, email, salaire in consultants_data:
                consultant = Consultant(
                    nom=nom,
                    prenom=prenom,
                    email=email,
                    telephone=fake.phone_number(),
                    salaire_actuel=salaire,
                    practice_id=practices[len(consultants) % len(practices)].id,
                    disponibilite=fake.boolean(),
                    date_creation=datetime.now(),
                    derniere_maj=datetime.now()
                )
                session.add(consultant)
                consultants.append(consultant)

            session.commit()
            print(f"✅ {len(consultants)} consultants créés")

            # 4. Créer quelques compétences
            print("🔧 Création des compétences...")
            competences_data = [
                ("Python", "Backend", "Langage de programmation"),
                ("Java", "Backend", "Langage de programmation"),
                ("JavaScript", "Frontend", "Langage de programmation"),
                ("React", "Frontend", "Framework frontend"),
                ("SQL", "Database", "Langage de base de données"),
                ("AWS", "Cloud", "Services cloud"),
                ("Docker", "DevOps", "Conteneurisation"),
                ("Git", "DevOps", "Contrôle de version")
            ]

            competences = []
            for nom, categorie, description in competences_data:
                competence = Competence(
                    nom=nom,
                    categorie=categorie,
                    type_competence="technique",
                    description=description
                )
                session.add(competence)
                competences.append(competence)

            session.commit()
            print(f"✅ {len(competences)} compétences créées")

            print("=" * 50)
            print("🎉 DONNÉES DE TEST CRÉÉES AVEC SUCCÈS!")
            print(f"🏢 Practices: {len(practices)}")
            print(f"👨‍💼 Business Managers: {len(business_managers)}")
            print(f"👥 Consultants: {len(consultants)}")
            print(f"🔧 Compétences: {len(competences)}")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Erreur lors de la création des données: {e}")
            session.rollback()
            raise

if __name__ == "__main__":
    create_basic_data()
