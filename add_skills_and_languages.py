"""
Script pour ajouter des compétences techniques et des langues aux consultants
Simule 1-2 langues par consultant et 3-4 compétences techniques
"""

import sys
import os
import random
from datetime import datetime

# Ajouter le chemin vers le module app
current_dir = os.path.dirname(__file__)
app_dir = os.path.join(current_dir, "app")
sys.path.insert(0, app_dir)

try:
    from database.database import get_database_session
    from database.models import (
        Consultant, 
        Competence, 
        ConsultantCompetence, 
        Langue, 
        ConsultantLangue
    )
    print("✅ Imports réussis")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

# Données de référence pour les langues
LANGUES_DATA = [
    {"nom": "Français", "code_iso": "FR", "description": "Langue française"},
    {"nom": "Anglais", "code_iso": "EN", "description": "Langue anglaise"},
    {"nom": "Espagnol", "code_iso": "ES", "description": "Langue espagnole"},
    {"nom": "Allemand", "code_iso": "DE", "description": "Langue allemande"},
    {"nom": "Italien", "code_iso": "IT", "description": "Langue italienne"},
    {"nom": "Portugais", "code_iso": "PT", "description": "Langue portugaise"},
    {"nom": "Arabe", "code_iso": "AR", "description": "Langue arabe"},
    {"nom": "Chinois", "code_iso": "ZH", "description": "Langue chinoise"},
    {"nom": "Japonais", "code_iso": "JA", "description": "Langue japonaise"},
    {"nom": "Russe", "code_iso": "RU", "description": "Langue russe"},
]

# Données de référence pour les compétences techniques
COMPETENCES_DATA = [
    # Frontend
    {"nom": "React", "categorie": "Frontend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Vue.js", "categorie": "Frontend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Angular", "categorie": "Frontend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "JavaScript", "categorie": "Frontend", "type_competence": "technique", "niveau_requis": "junior"},
    {"nom": "TypeScript", "categorie": "Frontend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "HTML/CSS", "categorie": "Frontend", "type_competence": "technique", "niveau_requis": "junior"},
    {"nom": "Sass/SCSS", "categorie": "Frontend", "type_competence": "technique", "niveau_requis": "junior"},
    
    # Backend
    {"nom": "Java", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Spring Boot", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Python", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Django", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "FastAPI", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Node.js", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Express.js", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "C#", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": ".NET Core", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "PHP", "categorie": "Backend", "type_competence": "technique", "niveau_requis": "junior"},
    
    # Base de données
    {"nom": "PostgreSQL", "categorie": "Database", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "MySQL", "categorie": "Database", "type_competence": "technique", "niveau_requis": "junior"},
    {"nom": "MongoDB", "categorie": "Database", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Redis", "categorie": "Database", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Oracle", "categorie": "Database", "type_competence": "technique", "niveau_requis": "senior"},
    {"nom": "SQL Server", "categorie": "Database", "type_competence": "technique", "niveau_requis": "medior"},
    
    # Cloud & DevOps
    {"nom": "AWS", "categorie": "Cloud", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Azure", "categorie": "Cloud", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "GCP", "categorie": "Cloud", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Docker", "categorie": "DevOps", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Kubernetes", "categorie": "DevOps", "type_competence": "technique", "niveau_requis": "senior"},
    {"nom": "Jenkins", "categorie": "DevOps", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "GitLab CI/CD", "categorie": "DevOps", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Terraform", "categorie": "DevOps", "type_competence": "technique", "niveau_requis": "senior"},
    
    # Data & IA
    {"nom": "Python Data", "categorie": "Data", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Pandas", "categorie": "Data", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "NumPy", "categorie": "Data", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Scikit-learn", "categorie": "Data", "type_competence": "technique", "niveau_requis": "senior"},
    {"nom": "TensorFlow", "categorie": "AI", "type_competence": "technique", "niveau_requis": "senior"},
    {"nom": "PyTorch", "categorie": "AI", "type_competence": "technique", "niveau_requis": "senior"},
    {"nom": "Power BI", "categorie": "Data", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Tableau", "categorie": "Data", "type_competence": "technique", "niveau_requis": "medior"},
    
    # Mobile
    {"nom": "React Native", "categorie": "Mobile", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "Flutter", "categorie": "Mobile", "type_competence": "technique", "niveau_requis": "medior"},
    {"nom": "iOS Swift", "categorie": "Mobile", "type_competence": "technique", "niveau_requis": "senior"},
    {"nom": "Android Kotlin", "categorie": "Mobile", "type_competence": "technique", "niveau_requis": "senior"},
]

def create_languages():
    """Crée les langues de référence dans la base"""
    print("📝 Création des langues de référence...")
    
    with get_database_session() as session:
        # Vérifier si des langues existent déjà
        existing_count = session.query(Langue).count()
        if existing_count > 0:
            print(f"ℹ️  {existing_count} langues déjà présentes, on continue...")
            return
        
        langues_created = 0
        for langue_data in LANGUES_DATA:
            # Vérifier si la langue existe déjà
            existing = session.query(Langue).filter(Langue.nom == langue_data["nom"]).first()
            if not existing:
                langue = Langue(**langue_data)
                session.add(langue)
                langues_created += 1
        
        session.commit()
        print(f"✅ {langues_created} nouvelles langues créées")

def create_competences():
    """Crée les compétences de référence dans la base"""
    print("🛠️  Création des compétences de référence...")
    
    with get_database_session() as session:
        # Vérifier si des compétences existent déjà
        existing_count = session.query(Competence).count()
        if existing_count > 0:
            print(f"ℹ️  {existing_count} compétences déjà présentes, on continue...")
            return
        
        competences_created = 0
        for comp_data in COMPETENCES_DATA:
            # Vérifier si la compétence existe déjà
            existing = session.query(Competence).filter(Competence.nom == comp_data["nom"]).first()
            if not existing:
                competence = Competence(**comp_data)
                session.add(competence)
                competences_created += 1
        
        session.commit()
        print(f"✅ {competences_created} nouvelles compétences créées")

def assign_languages_to_consultants():
    """Assigne 1-2 langues aléatoires à chaque consultant"""
    print("🗣️  Attribution des langues aux consultants...")
    
    with get_database_session() as session:
        consultants = session.query(Consultant).all()
        langues = session.query(Langue).all()
        
        if not langues:
            print("❌ Aucune langue trouvée, créez d'abord les langues")
            return
        
        # Niveaux de langue (1-5 échelle CECRL)
        niveaux_langue = [1, 2, 3, 4, 5]  # A1, A2, B1, B2, C1-C2
        
        consultants_updated = 0
        total_langues_assigned = 0
        
        for consultant in consultants:
            # Vérifier si le consultant a déjà des langues
            existing_langs = session.query(ConsultantLangue).filter(
                ConsultantLangue.consultant_id == consultant.id
            ).count()
            
            if existing_langs > 0:
                continue  # Passer si déjà des langues
            
            # Assigner 1-2 langues aléatoires
            nb_langues = random.randint(1, 2)
            langues_choisies = random.sample(langues, nb_langues)
            
            # Français obligatoire pour la plupart (80%)
            if random.random() < 0.8:
                francais = next((l for l in langues if l.nom == "Français"), None)
                if francais and francais not in langues_choisies:
                    if len(langues_choisies) >= 2:
                        langues_choisies[1] = francais  # Remplacer une langue
                    else:
                        langues_choisies.append(francais)
            
            for langue in langues_choisies:
                niveau = random.choice(niveaux_langue)
                # Français généralement niveau élevé
                if langue.nom == "Français":
                    niveau = random.choice([4, 5])
                # Anglais généralement bon niveau aussi
                elif langue.nom == "Anglais":
                    niveau = random.choice([3, 4, 5])
                
                consultant_langue = ConsultantLangue(
                    consultant_id=consultant.id,
                    langue_id=langue.id,
                    niveau=niveau,
                    commentaire=f"Niveau {niveau}/5 - Ajouté automatiquement",
                    date_ajout=datetime.now()
                )
                session.add(consultant_langue)
                total_langues_assigned += 1
            
            consultants_updated += 1
        
        session.commit()
        print(f"✅ {consultants_updated} consultants mis à jour avec {total_langues_assigned} langues au total")

def assign_skills_to_consultants():
    """Assigne 3-4 compétences techniques aléatoires à chaque consultant"""
    print("🛠️  Attribution des compétences aux consultants...")
    
    with get_database_session() as session:
        consultants = session.query(Consultant).all()
        competences = session.query(Competence).filter(
            Competence.type_competence == "technique"
        ).all()
        
        if not competences:
            print("❌ Aucune compétence technique trouvée, créez d'abord les compétences")
            return
        
        # Niveaux de maîtrise et années d'expérience
        niveaux_maitrise = ["debutant", "intermediaire", "expert"]
        
        consultants_updated = 0
        total_competences_assigned = 0
        
        for consultant in consultants:
            # Vérifier si le consultant a déjà des compétences
            existing_skills = session.query(ConsultantCompetence).filter(
                ConsultantCompetence.consultant_id == consultant.id
            ).count()
            
            if existing_skills > 0:
                continue  # Passer si déjà des compétences
            
            # Assigner 3-4 compétences aléatoires
            nb_competences = random.randint(3, 4)
            competences_choisies = random.sample(competences, min(nb_competences, len(competences)))
            
            for competence in competences_choisies:
                # Générer des données réalistes
                niveau = random.choice(niveaux_maitrise)
                
                # Années d'expérience basées sur le niveau
                if niveau == "debutant":
                    experience = round(random.uniform(0.5, 2.0), 1)
                elif niveau == "intermediaire":
                    experience = round(random.uniform(2.0, 5.0), 1)
                else:  # expert
                    experience = round(random.uniform(5.0, 12.0), 1)
                
                consultant_competence = ConsultantCompetence(
                    consultant_id=consultant.id,
                    competence_id=competence.id,
                    annees_experience=experience,
                    niveau_maitrise=niveau,
                    certifications=None  # Peut être ajouté plus tard
                )
                session.add(consultant_competence)
                total_competences_assigned += 1
            
            consultants_updated += 1
        
        session.commit()
        print(f"✅ {consultants_updated} consultants mis à jour avec {total_competences_assigned} compétences au total")

def main():
    """Fonction principale"""
    print("🚀 Début de l'ajout des langues et compétences aux consultants")
    print("=" * 60)
    
    try:
        # 1. Créer les langues de référence
        create_languages()
        
        # 2. Créer les compétences de référence
        create_competences()
        
        # 3. Assigner les langues aux consultants
        assign_languages_to_consultants()
        
        # 4. Assigner les compétences aux consultants
        assign_skills_to_consultants()
        
        print("=" * 60)
        print("🎉 Processus terminé avec succès !")
        
        # Afficher les statistiques finales
        with get_database_session() as session:
            total_consultants = session.query(Consultant).count()
            total_langues_assigned = session.query(ConsultantLangue).count()
            total_competences_assigned = session.query(ConsultantCompetence).count()
            
            print(f"📊 Statistiques finales :")
            print(f"   👥 Total consultants: {total_consultants}")
            print(f"   🗣️  Total langues assignées: {total_langues_assigned}")
            print(f"   🛠️  Total compétences assignées: {total_competences_assigned}")
            
            if total_consultants > 0:
                avg_langues = round(total_langues_assigned / total_consultants, 1)
                avg_competences = round(total_competences_assigned / total_consultants, 1)
                print(f"   📈 Moyenne langues/consultant: {avg_langues}")
                print(f"   📈 Moyenne compétences/consultant: {avg_competences}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()