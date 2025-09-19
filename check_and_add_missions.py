"""
Script pour vérifier et s'assurer que chaque consultant a au moins une mission
Ajoute des missions aux consultants qui n'en ont pas
"""

import os
import sys
import random
from datetime import datetime, timedelta, date
from typing import List, Dict, Set

# Ajouter le chemin de l'application
current_dir = os.path.dirname(__file__)
app_dir = os.path.join(current_dir, 'app')
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

try:
    from database.database import get_database_session, init_database
    from database.models import Consultant, Mission
    from sqlalchemy import func
    print("✅ Imports réussis")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

# Données fictives pour les clients
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

# Types de missions
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
    "Infrastructure véhicule autonome"
]

def analyze_consultant_missions():
    """Analyse les consultants et leurs missions"""
    print("🔍 Analyse des missions par consultant...")
    
    with get_database_session() as session:
        # Récupérer tous les consultants
        consultants = session.query(Consultant).all()
        if not consultants:
            print("❌ Aucun consultant trouvé.")
            return [], []
        
        print(f"👥 {len(consultants)} consultants trouvés")
        
        consultants_with_missions = []
        consultants_without_missions = []
        
        for consultant in consultants:
            # Compter les missions pour ce consultant
            mission_count = session.query(Mission).filter(
                Mission.consultant_id == consultant.id
            ).count()
            
            consultant_name = f"{consultant.prenom} {consultant.nom}"
            
            if mission_count > 0:
                consultants_with_missions.append({
                    'id': consultant.id,
                    'name': consultant_name,
                    'mission_count': mission_count
                })
                print(f"  ✅ {consultant_name}: {mission_count} mission(s)")
            else:
                consultants_without_missions.append({
                    'id': consultant.id,
                    'name': consultant_name,
                    'consultant': consultant
                })
                print(f"  ❌ {consultant_name}: 0 mission")
        
        print(f"\n📊 Résumé:")
        print(f"  ✅ Consultants avec missions: {len(consultants_with_missions)}")
        print(f"  ❌ Consultants sans mission: {len(consultants_without_missions)}")
        
        return consultants_with_missions, consultants_without_missions

def generate_random_date(start_year: int = 2020, end_year: int = 2025) -> date:
    """Génère une date aléatoire entre les années spécifiées"""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    
    return start_date + timedelta(days=random_days)

def create_mission_for_consultant(consultant_id: int, consultant_name: str) -> Dict:
    """Crée une mission pour un consultant spécifique"""
    
    # Sélectionner un client aléatoire
    client_nom = random.choice(CLIENTS_DATA)
    
    # Sélectionner un type de mission
    mission_type = random.choice(MISSION_TYPES)
    nom_mission = f"{mission_type} - {client_nom}"
    
    # Générer les dates
    date_debut = generate_random_date(2022, 2024)
    
    # 60% de chance que la mission soit terminée pour avoir un historique
    statut_en_cours = random.random() < 0.4
    
    if statut_en_cours:
        date_fin = None
        statut = "en_cours"
        # Mission en cours depuis au moins 1 mois
        if date_debut > date.today() - timedelta(days=30):
            date_debut = date.today() - timedelta(days=random.randint(30, 180))
    else:
        # Mission terminée
        statut = "terminee"
        duration_days = random.randint(60, 300)  # Entre 2 mois et 10 mois
        date_fin = date_debut + timedelta(days=duration_days)
        
        # S'assurer que la mission terminée ne dépasse pas aujourd'hui
        if date_fin > date.today():
            date_fin = date.today() - timedelta(days=random.randint(1, 30))
    
    # Calculer la rémunération
    # TJM entre 450€ et 1100€ selon l'expérience
    tjm = random.randint(450, 1100)
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
        "Consultant Senior",
        "Expert Technique"
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
        "Java, Microservices, Kafka, Elasticsearch, AWS",
        "React Native, Node.js, GraphQL, MongoDB",
        "Flutter, Dart, Firebase, GCP",
        "Scala, Spark, Kafka, Cassandra, AWS"
    ]
    
    technologies_utilisees = random.choice(tech_sets)
    
    # Description de mission
    descriptions = [
        f"Mission de {mission_type.lower()} pour {client_nom}. Collaboration étroite avec les équipes techniques et métier pour délivrer une solution robuste et scalable. Mise en place de bonnes pratiques de développement et d'architecture.",
        f"Projet {mission_type.lower()} dans le cadre de la transformation digitale de {client_nom}. Conception et développement d'une architecture moderne et performante avec focus sur la qualité et la maintenabilité.",
        f"Développement et mise en œuvre de {mission_type.lower()} pour optimiser les processus métier de {client_nom}. Approche agile avec livraisons itératives et implication forte des utilisateurs finaux.",
        f"Accompagnement de {client_nom} sur le projet {mission_type.lower()} avec une méthodologie DevOps et des pratiques de développement modernes. Formation des équipes et transfert de compétences."
    ]
    
    description = random.choice(descriptions)
    
    print(f"  📝 Création mission: {nom_mission[:50]}... pour {consultant_name}")
    
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
        "technologies_utilisees": technologies_utilisees
    }
    
    return mission_data

def add_missions_to_consultants_without(consultants_without_missions: List[Dict]):
    """Ajoute des missions aux consultants qui n'en ont pas"""
    
    if not consultants_without_missions:
        print("✅ Tous les consultants ont déjà au moins une mission !")
        return 0
    
    print(f"\n🎯 Ajout de missions pour {len(consultants_without_missions)} consultants...")
    
    with get_database_session() as session:
        missions_added = 0
        
        for consultant_info in consultants_without_missions:
            consultant_id = consultant_info['id']
            consultant_name = consultant_info['name']
            
            # Créer 1 à 3 missions pour ce consultant
            num_missions = random.randint(1, 3)
            
            print(f"\n👤 {consultant_name} - Ajout de {num_missions} mission(s):")
            
            for i in range(num_missions):
                mission_data = create_mission_for_consultant(consultant_id, consultant_name)
                
                # Créer la mission en base
                mission = Mission(**mission_data)
                session.add(mission)
                missions_added += 1
        
        # Sauvegarder toutes les missions
        session.commit()
        
        print(f"\n✅ {missions_added} nouvelles missions créées avec succès !")
        return missions_added

def verify_all_consultants_have_missions():
    """Vérifie que tous les consultants ont maintenant au moins une mission"""
    print("\n🔍 Vérification finale...")
    
    with get_database_session() as session:
        # Requête pour trouver les consultants sans mission
        consultants_without_missions = session.query(Consultant).filter(
            ~Consultant.id.in_(
                session.query(Mission.consultant_id).distinct()
            )
        ).all()
        
        if consultants_without_missions:
            print(f"❌ {len(consultants_without_missions)} consultant(s) sans mission détecté(s):")
            for consultant in consultants_without_missions:
                print(f"  - {consultant.prenom} {consultant.nom}")
            return False
        else:
            # Statistiques finales
            total_consultants = session.query(Consultant).count()
            total_missions = session.query(Mission).count()
            
            print(f"✅ Tous les consultants ont au moins une mission !")
            print(f"📊 Statistiques finales:")
            print(f"  👥 Total consultants: {total_consultants}")
            print(f"  🎯 Total missions: {total_missions}")
            print(f"  📈 Moyenne missions/consultant: {total_missions/total_consultants:.1f}")
            
            return True

def main():
    """Fonction principale"""
    print("🚀 Vérification et ajout de missions pour tous les consultants")
    print("=" * 60)
    
    try:
        # Initialiser la base de données si nécessaire
        init_database()
        
        # Analyser la situation actuelle
        consultants_with_missions, consultants_without_missions = analyze_consultant_missions()
        
        # Ajouter des missions si nécessaire
        if consultants_without_missions:
            missions_added = add_missions_to_consultants_without(consultants_without_missions)
            
            # Vérification finale
            verify_all_consultants_have_missions()
            
            print(f"\n🎉 Mission accomplie ! {missions_added} nouvelles missions ajoutées.")
        else:
            print("\n🎉 Parfait ! Tous les consultants ont déjà au moins une mission.")
        
        print("\n" + "=" * 60)
        print("✅ Vérification terminée avec succès !")
        print("Vous pouvez maintenant tester l'application avec la certitude que chaque consultant a des missions.")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()