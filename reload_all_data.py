#!/usr/bin/env python3
"""
Script orchestrateur pour recharger TOUTES les données Consultator dans le bon ordre :
1. Personnes (BM + Consultants) via reset_and_reimport_vsa_complete.py
2. Missions via import_vsa_missions_complet.py
3. Langues (génération automatique)
4. Compétences (génération automatique)

Ce script utilise les scripts existants et les complète avec la génération de langues/compétences.
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Ajouter le répertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(__file__))

# Importer les fonctions des scripts existants
from reset_and_reimport_vsa_complete import reset_and_reimport_vsa_data
from import_vsa_missions_complet import import_vsa_missions_complet

# Importer les modèles
from app.database.database import get_database_session
from app.database.models import (
    Consultant, Langue, ConsultantLangue, 
    Competence, ConsultantCompetence
)


# ==================== CONFIGURATION ====================

EXCEL_VSA_PATH = r"C:\Users\b302gja\Documents\VSA Personnes.xlsx"

# Liste complète des langues
LANGUES_DISPONIBLES = [
    "Français", "Anglais", "Espagnol", "Allemand", "Italien", 
    "Portugais", "Arabe", "Chinois", "Japonais", "Russe",
    "Néerlandais", "Polonais", "Turc", "Coréen", "Hindi"
]

NIVEAUX_LANGUE = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Compétences par catégorie
COMPETENCES_PAR_CATEGORIE = {
    "Langages de programmation": [
        "Python", "Java", "JavaScript", "TypeScript", "C#", "C++", "Go", "Rust",
        "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R", "MATLAB"
    ],
    "Frameworks & Libraries": [
        "React", "Angular", "Vue.js", "Spring Boot", "Django", "Flask", "FastAPI",
        "Node.js", "Express", ".NET Core", "ASP.NET", "Laravel", "Symfony"
    ],
    "Data & Analytics": [
        "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "Apache Spark", "Apache Kafka", "Airflow", "Tableau", "Power BI",
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform",
        "Ansible", "Jenkins", "GitLab CI", "GitHub Actions", "CircleCI"
    ],
    "Architecture & Design": [
        "Microservices", "Architecture Cloud", "API REST", "GraphQL",
        "Event-Driven Architecture", "Domain-Driven Design", "SOLID",
        "Design Patterns", "Architecture Hexagonale"
    ],
    "Méthodologies": [
        "Agile", "Scrum", "Kanban", "SAFe", "DevOps", "CI/CD",
        "Test-Driven Development", "Behavior-Driven Development"
    ],
    "Outils & Technologies": [
        "Git", "JIRA", "Confluence", "Postman", "Swagger", "SonarQube",
        "Splunk", "Datadog", "Prometheus", "Grafana"
    ],
    "Finance & Banking": [
        "Trading Systems", "Risk Management", "Regulatory Compliance",
        "Bloomberg Terminal", "Reuters", "Murex", "Summit", "Calypso"
    ]
}


# ==================== FONCTIONS GÉNÉRATION LANGUES ====================

def generate_languages_for_consultants():
    """Génère 2-4 langues par consultant avec niveaux réalistes"""
    print("\n" + "=" * 70)
    print("🌍 GÉNÉRATION DES LANGUES")
    print("=" * 70 + "\n")
    
    languages_created = []
    
    with get_database_session() as session:
        # Récupérer tous les consultants
        consultants = session.query(Consultant).all()
        print(f"👥 {len(consultants)} consultants à traiter\n")
        
        # Créer les langues dans la table Langue si nécessaire
        existing_languages = {lang.nom: lang.id for lang in session.query(Langue).all()}
        
        for lang_name in LANGUES_DISPONIBLES:
            if lang_name not in existing_languages:
                lang = Langue(nom=lang_name)
                session.add(lang)
                session.flush()
                existing_languages[lang_name] = lang.id
        
        session.commit()
        print(f"✅ {len(existing_languages)} langues disponibles dans le référentiel\n")
        
        # Assigner langues aux consultants
        for consultant in consultants:
            # Français natif pour tous
            niveau_francais = random.choice([4, 5])  # C1 ou C2 = niveau 4 ou 5
            cl_fr = ConsultantLangue(
                consultant_id=consultant.id,
                langue_id=existing_languages["Français"],
                niveau=niveau_francais,
                commentaire="Langue maternelle"
            )
            session.add(cl_fr)
            languages_created.append(cl_fr)
            
            # Anglais pour la plupart (85%)
            if random.random() < 0.85:
                niveau_anglais = random.choice([2, 3, 4])  # B1-C1 = niveau 2 à 4
                cl_en = ConsultantLangue(
                    consultant_id=consultant.id,
                    langue_id=existing_languages["Anglais"],
                    niveau=niveau_anglais,
                    commentaire="TOEIC" if random.random() < 0.3 else None
                )
                session.add(cl_en)
                languages_created.append(cl_en)
            
            # 1-2 langues supplémentaires pour certains (30%)
            if random.random() < 0.3:
                autres_langues = [l for l in LANGUES_DISPONIBLES if l not in ["Français", "Anglais"]]
                nb_autres = random.randint(1, 2)
                
                for lang_name in random.sample(autres_langues, k=min(nb_autres, len(autres_langues))):
                    niveau = random.choice([2, 3, 4])  # A2-C1 = niveau 2 à 4
                    cl = ConsultantLangue(
                        consultant_id=consultant.id,
                        langue_id=existing_languages[lang_name],
                        niveau=niveau,
                        commentaire=None
                    )
                    session.add(cl)
                    languages_created.append(cl)
        
        session.commit()
    
    print(f"✅ {len(languages_created)} associations consultant-langue créées")
    print(f"📊 Moyenne: {len(languages_created) / len(consultants):.1f} langues par consultant\n")
    
    return languages_created


# ==================== FONCTIONS GÉNÉRATION COMPÉTENCES ====================

def generate_skills_for_consultants():
    """Génère 8-15 compétences par consultant avec niveaux d'expérience"""
    print("\n" + "=" * 70)
    print("🎯 GÉNÉRATION DES COMPÉTENCES")
    print("=" * 70 + "\n")
    
    skills_created = []
    
    with get_database_session() as session:
        # Récupérer tous les consultants
        consultants = session.query(Consultant).all()
        print(f"👥 {len(consultants)} consultants à traiter\n")
        
        # Créer toutes les compétences dans la table Competence
        existing_skills = {skill.nom: skill.id for skill in session.query(Competence).all()}
        
        for categorie, competences in COMPETENCES_PAR_CATEGORIE.items():
            for comp_name in competences:
                if comp_name not in existing_skills:
                    skill = Competence(
                        nom=comp_name,
                        categorie=categorie,
                        description=f"Compétence en {comp_name}"
                    )
                    session.add(skill)
                    session.flush()
                    existing_skills[comp_name] = skill.id
        
        session.commit()
        print(f"✅ {len(existing_skills)} compétences disponibles dans le référentiel")
        print(f"📋 Réparties en {len(COMPETENCES_PAR_CATEGORIE)} catégories\n")
        
        # Assigner compétences aux consultants
        for consultant in consultants:
            # Sélectionner 8-15 compétences aléatoires
            nb_skills = random.randint(8, 15)
            all_skills = list(existing_skills.items())
            selected_skills = random.sample(all_skills, k=min(nb_skills, len(all_skills)))
            
            for skill_name, skill_id in selected_skills:
                # Années d'expérience réalistes
                annees_experience = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15])
                
                # Niveau selon années d'expérience
                if annees_experience <= 2:
                    niveau = random.choice(["debutant", "debutant", "intermediaire"])
                elif annees_experience <= 5:
                    niveau = random.choice(["intermediaire", "intermediaire", "expert"])
                else:
                    niveau = random.choice(["expert", "expert", "expert"])
                
                cs = ConsultantCompetence(
                    consultant_id=consultant.id,
                    competence_id=skill_id,
                    niveau_maitrise=niveau,
                    annees_experience=annees_experience,
                    certifications=f"Certified {skill_name} Professional" if random.random() < 0.08 else None,
                    projets_realises=None
                )
                session.add(cs)
                skills_created.append(cs)
            
            # Commit périodique
            if len(skills_created) % 500 == 0:
                session.commit()
                print(f"💾 {len(skills_created)} associations créées...")
        
        session.commit()
    
    print(f"\n✅ {len(skills_created)} associations consultant-compétence créées")
    print(f"📊 Moyenne: {len(skills_created) / len(consultants):.1f} compétences par consultant\n")
    
    return skills_created


# ==================== SCRIPT PRINCIPAL ====================

def reload_all_data():
    """Orchestre le rechargement complet de toutes les données"""
    
    print("\n" + "=" * 70)
    print("🚀 RECHARGEMENT COMPLET DE CONSULTATOR")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 70 + "\n")
    
    try:
        # ========== ÉTAPE 1: Personnes (BM + Consultants) ==========
        print("📋 ÉTAPE 1/4 - IMPORT DES PERSONNES")
        print("-" * 70)
        success = reset_and_reimport_vsa_data(EXCEL_VSA_PATH)
        
        if not success:
            print("\n❌ Échec de l'import des personnes")
            return False
        
        print("\n✅ Import des personnes terminé avec succès\n")
        
        # ========== ÉTAPE 2: Missions ==========
        print("\n" + "=" * 70)
        print("📋 ÉTAPE 2/4 - IMPORT DES MISSIONS")
        print("-" * 70)
        vsa_stats, classic_stats = import_vsa_missions_complet()
        print("\n✅ Import des missions terminé avec succès\n")
        
        # ========== ÉTAPE 3: Langues ==========
        print("\n" + "=" * 70)
        print("📋 ÉTAPE 3/4 - GÉNÉRATION DES LANGUES")
        print("-" * 70)
        languages = generate_languages_for_consultants()
        print("✅ Génération des langues terminée\n")
        
        # ========== ÉTAPE 4: Compétences ==========
        print("\n" + "=" * 70)
        print("📋 ÉTAPE 4/4 - GÉNÉRATION DES COMPÉTENCES")
        print("-" * 70)
        skills = generate_skills_for_consultants()
        print("✅ Génération des compétences terminée\n")
        
        # ========== RÉSUMÉ FINAL ==========
        print("\n" + "=" * 70)
        print("📊 RÉSUMÉ FINAL DU RECHARGEMENT")
        print("=" * 70)
        
        with get_database_session() as session:
            from app.database.models import BusinessManager, ConsultantBusinessManager, Mission
            
            total_bm = session.query(BusinessManager).count()
            total_consultants = session.query(Consultant).count()
            total_relations = session.query(ConsultantBusinessManager).count()
            total_missions = session.query(Mission).count()
            total_languages = session.query(ConsultantLangue).count()
            total_skills = session.query(ConsultantCompetence).count()
            
            print(f"\n👔 Business Managers:              {total_bm}")
            print(f"👥 Consultants:                    {total_consultants}")
            print(f"🔗 Relations BM-Consultant:        {total_relations}")
            print(f"💼 Missions:                       {total_missions}")
            print(f"🌍 Langues (associations):         {total_languages}")
            print(f"🎯 Compétences (associations):     {total_skills}")
        
        print("\n" + "=" * 70)
        print("🎉 RECHARGEMENT COMPLET TERMINÉ AVEC SUCCÈS!")
        print("=" * 70)
        print("\n💡 Vous pouvez maintenant tester toutes les fonctionnalités:")
        print("   ✅ Gestion des consultants et Business Managers")
        print("   ✅ Suivi des missions et facturation")
        print("   ✅ Gestion des compétences et langues")
        print("   ✅ Tableaux de bord et analytics")
        print("   ✅ Recherche avancée par compétences\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = reload_all_data()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur")
        exit(130)
    except Exception as e:
        print(f"\n❌ ERREUR FATALE: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
