"""
Script pour générer des missions fictives pour les consultants
Crée des missions réalistes avec des clients, dates, et rémunérations
"""

import os
import sys
import random
from datetime import timedelta, date
from typing import List, Dict

# Ajouter le chemin de l'application
current_dir = os.path.dirname(__file__)
app_dir = os.path.join(current_dir, "app")
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

try:
    from database.database import get_database_session, init_database
    from database.models import Consultant, Mission

    print("✅ Imports réussis")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

# Données fictives pour les clients (noms seulement)
CLIENTS_DATA = [
    "Société Générale",
    "BNP Paribas",
    "Crédit Agricole",
    "Orange",
    "EDF",
    "SNCF Connect",
    "Airbus",
    "Thales",
    "Capgemini",
    "Accenture",
    "Dassault Systèmes",
    "L'Oréal",
    "Renault",
    "PSA Peugeot",
    "Carrefour",
    "LVMH",
    "Danone",
    "Total Energies",
    "Veolia",
    "Bouygues",
]

# Types de missions par secteur (simplifié)
MISSION_TYPES = [
    "Transformation digitale",
    "Migration vers le cloud AWS",
    "Développement application mobile",
    "Mise en place architecture microservices",
    "Projet de dématérialisation",
    "Refonte système de paiement",
    "Conformité réglementaire RGPD",
    "Optimisation des processus métier",
    "Déploiement réseau 5G",
    "Modernisation SI client",
    "Développement portail web",
    "Projet IoT entreprise",
    "Smart Grid et compteurs intelligents",
    "Plateforme de trading énergétique",
    "Système de gestion maintenance",
    "Application mobile terrain",
    "Système de réservation nouvelle génération",
    "Optimisation planification",
    "Plateforme data analytics",
    "Modernisation infrastructure",
    "Système de maintenance prédictive",
    "Plateforme de conception collaborative",
    "Application de suivi production",
    "Système qualité et traçabilité",
    "Système de communication sécurisé",
    "Plateforme de cybersécurité",
    "Application de géolocalisation",
    "Audit architecture SI",
    "Accompagnement méthodes agiles",
    "Stratégie cloud native",
    "Développement nouvelles fonctionnalités",
    "Intégration intelligence artificielle",
    "Optimisation performance logiciel",
    "Système embarqué véhicule connecté",
    "Application mobile conducteur",
    "Système de production intelligent",
    "Infrastructure véhicule autonome",
]


def generate_random_date(start_year: int = 2020, end_year: int = 2025) -> date:
    """Génère une date aléatoire entre les années spécifiées"""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)

    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    return start_date + timedelta(days=random_days)


def generate_missions_for_consultant(
    consultant_id: int, consultant_name: str
) -> List[Dict]:
    """Génère 2-5 missions pour un consultant"""

    num_missions = random.randint(2, 5)
    missions = []

    print(f"  👤 Génération de {num_missions} missions pour {consultant_name}")

    for i in range(num_missions):
        # Sélectionner un client aléatoire
        client_nom = random.choice(CLIENTS_DATA)

        # Sélectionner un type de mission
        mission_type = random.choice(MISSION_TYPES)
        nom_mission = f"{mission_type} - {client_nom}"

        # Générer les dates
        date_debut = generate_random_date(2022, 2024)

        # 70% de chance que la mission soit terminée
        statut_en_cours = random.random() < 0.3

        if statut_en_cours:
            date_fin = None
            statut = "en_cours"
            # Mission en cours depuis au moins 1 mois
            if date_debut > date.today() - timedelta(days=30):
                date_debut = date.today() - timedelta(days=random.randint(30, 200))
        else:
            # Mission terminée
            statut = "terminee"
            duration_days = random.randint(30, 365)  # Entre 1 mois et 1 an
            date_fin = date_debut + timedelta(days=duration_days)

            # S'assurer que la mission terminée ne dépasse pas aujourd'hui
            if date_fin > date.today():
                date_fin = date.today() - timedelta(days=random.randint(1, 30))

        # Calculer la rémunération
        # TJM entre 400€ et 1200€ selon l'expérience
        tjm = random.randint(400, 1200)
        taux_journalier = tjm  # Pour compatibilité

        # Calculer les revenus générés (estimation)
        if date_fin:
            duration_days = (date_fin - date_debut).days
            jours_travailles = max(1, int(duration_days * 5 / 7))  # 5 jours par semaine
            revenus_generes = tjm * jours_travailles
        else:
            # Mission en cours - estimation depuis le début
            duration_days = (date.today() - date_debut).days
            jours_travailles = max(1, int(duration_days * 5 / 7))
            revenus_generes = tjm * jours_travailles

        # Rôle/poste sur la mission
        roles = [
            "Développeur Full Stack",
            "Architecte Solution",
            "Lead Developer",
            "Consultant Technique",
            "Chef de Projet Technique",
            "Développeur Backend",
            "Développeur Frontend",
            "DevOps Engineer",
            "Data Engineer",
            "Analyste Fonctionnel",
            "Scrum Master",
            "Product Owner Technique",
        ]
        role = random.choice(roles)

        # Technologies utilisées
        tech_sets = [
            "Java, Spring Boot, Angular, PostgreSQL, Docker",
            "Python, Django, React, MongoDB, AWS",
            "C#, .NET Core, Azure, SQL Server, Kubernetes",
            "Node.js, Express, Vue.js, Redis, GCP",
            "PHP, Symfony, MySQL, Docker, Jenkins",
            "Kotlin, Android, Firebase, API REST",
            "Swift, iOS, Core Data, CloudKit",
            "Go, Kubernetes, Docker, AWS, Terraform",
            "Python, FastAPI, React, PostgreSQL, Docker",
            "TypeScript, NestJS, Angular, MongoDB, Azure",
        ]

        technologies_utilisees = random.choice(tech_sets)

        # Description de mission
        descriptions = [
            f"Mission de {mission_type.lower()} pour {client_nom}. Collaboration étroite avec les équipes techniques et métier pour délivrer une solution robuste et scalable.",
            f"Projet {mission_type.lower()} dans le cadre de la transformation digitale de {client_nom}. Mise en place d'une architecture moderne et performante.",
            f"Développement et mise en œuvre de {mission_type.lower()} pour optimiser les processus métier de {client_nom}. Approche agile avec livraisons itératives.",
            f"Accompagnement de {client_nom} sur le projet {mission_type.lower()} avec une méthodologie DevOps et des pratiques de développement modernes.",
        ]

        description = random.choice(descriptions)

        mission_data = {
            "consultant_id": consultant_id,
            "nom_mission": nom_mission,
            "client": client_nom,
            "role": role,
            "description": description,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "statut": statut,
            "taux_journalier": taux_journalier,
            "tjm": tjm,
            "revenus_generes": revenus_generes,
            "technologies_utilisees": technologies_utilisees,
        }

        missions.append(mission_data)

    return missions


def create_missions():
    """Crée les missions pour tous les consultants"""
    print("🎯 Création des missions...")

    with get_database_session() as session:
        # Vérifier si des missions existent déjà
        existing_missions = session.query(Mission).count()
        if existing_missions > 0:
            print(f"ℹ️ {existing_missions} missions déjà présentes")
            try:
                # Security: Validation stricte de l'input utilisateur
                user_input = (
                    input(
                        "Voulez-vous supprimer les missions existantes et en créer de nouvelles ? (y/N): "
                    )
                    .strip()
                    .lower()
                )
                # Limiter aux réponses autorisées
                if user_input not in ["y", "yes", "n", "no", ""]:
                    print("❌ Réponse invalide. Opération annulée")
                    return

                if user_input not in ["y", "yes"]:
                    print("❌ Opération annulée")
                    return
            except (EOFError, KeyboardInterrupt):
                print("\n❌ Opération annulée")
                return

            # Supprimer les missions existantes
            session.query(Mission).delete()
            session.commit()
            print("🗑️ Missions existantes supprimées")

        # Récupérer tous les consultants
        consultants = session.query(Consultant).all()
        if not consultants:
            print("❌ Aucun consultant trouvé. Veuillez d'abord créer des consultants.")
            return

        print(f"👥 {len(consultants)} consultants trouvés")

        total_missions = 0

        for consultant in consultants:
            consultant_name = f"{consultant.prenom} {consultant.nom}"
            missions_data = generate_missions_for_consultant(
                consultant.id, consultant_name
            )

            # Créer les missions en base
            for mission_data in missions_data:
                mission = Mission(**mission_data)
                session.add(mission)
                total_missions += 1

        session.commit()
        print(f"✅ {total_missions} missions créées avec succès !")

        # Statistiques
        missions_en_cours = (
            session.query(Mission).filter(Mission.statut == "en_cours").count()
        )
        missions_terminees = (
            session.query(Mission).filter(Mission.statut == "terminee").count()
        )
        total_revenus = (
            session.query(Mission.revenus_generes)
            .filter(Mission.revenus_generes.isnot(None))
            .all()
        )
        total_revenus_sum = sum(r[0] for r in total_revenus if r[0])

        print(f"📊 Statistiques:")
        print(f"  🔄 Missions en cours: {missions_en_cours}")
        print(f"  ✅ Missions terminées: {missions_terminees}")
        print(f"  📈 Total missions: {total_missions}")
        print(f"  💰 Revenus générés: {total_revenus_sum:,.0f}€")


def main():
    """Fonction principale"""
    print("🚀 Génération des données de missions fictives")
    print("=" * 50)

    try:
        # Initialiser la base de données si nécessaire
        init_database()

        # Créer les missions
        create_missions()

        print("\n" + "=" * 50)
        print("✅ Génération terminée avec succès !")
        print(
            "Vous pouvez maintenant tester les fonctionnalités de missions dans l'application."
        )

    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
