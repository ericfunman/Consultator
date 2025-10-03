#!/usr/bin/env python3
"""
Script complet pour recharger toutes les données de Consultator :
1. Personnes (consultants + Business Managers) depuis VSA Personnes.xlsx
2. Missions depuis VSA Personnes.xlsx (colonnes de missions)
3. Langues pour chaque consultant
4. Compétences avec niveaux d'expérience
"""

from datetime import datetime, timedelta
import pandas as pd
import random
from app.database.database import get_database_session, reset_database, init_database
from app.database.models import (
    BusinessManager, Consultant, ConsultantBusinessManager, 
    Mission, Language, ConsultantLanguage, Skill, ConsultantSkill, Practice
)


# ==================== CONFIGURATION ====================

EXCEL_VSA_PATH = r"C:\Users\b302gja\Documents\VSA Personnes.xlsx"

# Liste complète des langues avec niveaux réalistes
LANGUES_DISPONIBLES = [
    "Français", "Anglais", "Espagnol", "Allemand", "Italien", 
    "Portugais", "Arabe", "Chinois", "Japonais", "Russe",
    "Néerlandais", "Polonais", "Turc", "Coréen", "Hindi"
]

NIVEAUX_LANGUE = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Compétences par catégorie (référentiel étendu)
COMPETENCES_PAR_CATEGORIE = {
    "Languages de programmation": [
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

# Clients fréquents dans la finance
CLIENTS_FINANCE = [
    "Société Générale", "BNP Paribas", "Crédit Agricole", "BPCE", "Natixis",
    "AXA", "Allianz", "CNP Assurances", "Amundi", "Euronext",
    "Crédit Mutuel", "La Banque Postale", "HSBC France", "Barclays",
    "JP Morgan", "Goldman Sachs", "Morgan Stanley"
]

TYPES_MISSIONS = [
    "développement", "architecture", "data_science", "devops",
    "consulting", "product_owner", "scrum_master", "tech_lead"
]

STATUTS_MISSIONS = ["termine", "en_cours", "a_venir"]


# ==================== FONCTIONS UTILITAIRES ====================

def classify_person_by_job_title(job_title: str) -> str:
    """Classifie une personne comme BM ou Consultant"""
    if pd.isna(job_title):
        return "consultant"
    
    job_lower = job_title.lower()
    
    bm_patterns = ["business manager", "senior business manager"]
    
    if "directeur de practice" in job_lower:
        return "consultant"
    
    return "bm" if any(p in job_lower for p in bm_patterns) else "consultant"


def is_laurence_oziel(firstname: str, lastname: str, email: str) -> bool:
    """Identifie spécifiquement Laurence Oziel (BM)"""
    if pd.isna(firstname) or pd.isna(lastname):
        return False
    
    return (
        (firstname.strip().lower() == "laurence" and lastname.strip().lower() == "oziel") or
        (pd.notna(email) and email.strip().lower() == "laurence.oziel@quanteam.fr")
    )


def generate_missions_from_excel(df: pd.DataFrame, consultants_map: dict, practices: dict):
    """
    Génère des missions depuis les colonnes du fichier Excel VSA
    + missions aléatoires supplémentaires pour enrichir les données
    """
    missions_created = []
    
    with get_database_session() as session:
        # Parcourir chaque consultant
        for _, row in df.iterrows():
            if pd.isna(row.get("firstname")) or pd.isna(row.get("lastname")):
                continue
            
            consultant_key = f"{row['firstname']} {row['lastname']}".strip()
            consultant_id = consultants_map.get(consultant_key)
            
            if not consultant_id:
                continue
            
            # Extraire les missions depuis les colonnes Excel (si elles existent)
            # Colonnes possibles : Mission1, Mission2, Client1, Client2, etc.
            missions_from_excel = []
            for i in range(1, 6):  # Jusqu'à 5 missions possibles
                mission_col = f"Mission{i}"
                client_col = f"Client{i}"
                
                if mission_col in row and pd.notna(row[mission_col]):
                    missions_from_excel.append({
                        "titre": row[mission_col],
                        "client": row[client_col] if client_col in row and pd.notna(row[client_col]) else random.choice(CLIENTS_FINANCE),
                    })
            
            # Si pas de missions dans Excel, générer 2-4 missions aléatoires
            nb_missions = len(missions_from_excel) if missions_from_excel else random.randint(2, 4)
            
            for i in range(nb_missions):
                # Utiliser mission Excel si disponible, sinon générer
                if i < len(missions_from_excel):
                    mission_data = missions_from_excel[i]
                    titre = mission_data["titre"]
                    client = mission_data["client"]
                else:
                    type_mission = random.choice(TYPES_MISSIONS)
                    titre = f"{type_mission.replace('_', ' ').title()} - Projet {random.randint(1, 100)}"
                    client = random.choice(CLIENTS_FINANCE)
                
                # Générer dates cohérentes
                date_debut = datetime.now().date() - timedelta(days=random.randint(30, 730))
                duree_jours = random.randint(60, 365)
                date_fin_prevue = date_debut + timedelta(days=duree_jours)
                
                # Statut selon la date
                statut = "termine" if date_fin_prevue < datetime.now().date() else random.choice(["en_cours", "termine"])
                
                # TJM réaliste
                tjm = random.randint(400, 900)
                
                # Practice aléatoire
                practice_id = random.choice(list(practices.values())) if practices else None
                
                mission = Mission(
                    consultant_id=consultant_id,
                    practice_id=practice_id,
                    titre=titre,
                    client=client,
                    description=f"Mission de {titre.lower()} pour {client}",
                    date_debut=date_debut,
                    date_fin_prevue=date_fin_prevue,
                    date_fin_reelle=date_fin_prevue if statut == "termine" else None,
                    tjm=tjm,
                    statut=statut,
                    type_mission=random.choice(TYPES_MISSIONS),
                    technologies_utilisees=", ".join(random.sample([c for cat in COMPETENCES_PAR_CATEGORIE.values() for c in cat], k=random.randint(3, 6))),
                    date_creation=datetime.now()
                )
                
                session.add(mission)
                missions_created.append(mission)
        
        session.commit()
    
    return missions_created


def generate_languages_for_consultants(consultants_ids: list):
    """Génère 2-4 langues par consultant avec niveaux réalistes"""
    languages_created = []
    
    with get_database_session() as session:
        # Créer les langues dans la table Language si nécessaire
        existing_languages = {lang.nom: lang.id for lang in session.query(Language).all()}
        
        for lang_name in LANGUES_DISPONIBLES:
            if lang_name not in existing_languages:
                lang = Language(nom=lang_name, date_creation=datetime.now())
                session.add(lang)
                session.flush()
                existing_languages[lang_name] = lang.id
        
        session.commit()
        
        # Assigner langues aux consultants
        for consultant_id in consultants_ids:
            # Français natif pour tous
            niveau_francais = random.choice(["C1", "C2"])
            cl_fr = ConsultantLanguage(
                consultant_id=consultant_id,
                language_id=existing_languages["Français"],
                niveau=niveau_francais,
                certification=None,
                date_certification=None,
                date_creation=datetime.now()
            )
            session.add(cl_fr)
            languages_created.append(cl_fr)
            
            # Anglais pour la plupart (80%)
            if random.random() < 0.8:
                niveau_anglais = random.choice(["B1", "B2", "C1", "C2"])
                cl_en = ConsultantLanguage(
                    consultant_id=consultant_id,
                    language_id=existing_languages["Anglais"],
                    niveau=niveau_anglais,
                    certification="TOEIC" if random.random() < 0.3 else None,
                    date_creation=datetime.now()
                )
                session.add(cl_en)
                languages_created.append(cl_en)
            
            # 1-2 langues supplémentaires pour certains (40%)
            if random.random() < 0.4:
                autres_langues = [l for l in LANGUES_DISPONIBLES if l not in ["Français", "Anglais"]]
                nb_autres = random.randint(1, 2)
                
                for lang_name in random.sample(autres_langues, k=nb_autres):
                    niveau = random.choice(["A2", "B1", "B2", "C1"])
                    cl = ConsultantLanguage(
                        consultant_id=consultant_id,
                        language_id=existing_languages[lang_name],
                        niveau=niveau,
                        date_creation=datetime.now()
                    )
                    session.add(cl)
                    languages_created.append(cl)
        
        session.commit()
    
    return languages_created


def generate_skills_for_consultants(consultants_ids: list):
    """Génère 8-15 compétences par consultant avec niveaux d'expérience"""
    skills_created = []
    
    with get_database_session() as session:
        # Créer toutes les compétences dans la table Skill
        existing_skills = {skill.nom: skill.id for skill in session.query(Skill).all()}
        
        for categorie, competences in COMPETENCES_PAR_CATEGORIE.items():
            for comp_name in competences:
                if comp_name not in existing_skills:
                    skill = Skill(
                        nom=comp_name,
                        categorie=categorie,
                        description=f"Compétence en {comp_name}",
                        date_creation=datetime.now()
                    )
                    session.add(skill)
                    session.flush()
                    existing_skills[comp_name] = skill.id
        
        session.commit()
        
        # Assigner compétences aux consultants
        for consultant_id in consultants_ids:
            # Sélectionner 8-15 compétences aléatoires
            nb_skills = random.randint(8, 15)
            all_skills = list(existing_skills.items())
            selected_skills = random.sample(all_skills, k=nb_skills)
            
            for skill_name, skill_id in selected_skills:
                # Années d'expérience réalistes
                annees_experience = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15])
                
                # Niveau selon années d'expérience
                if annees_experience <= 2:
                    niveau = random.choice(["junior", "junior", "intermediaire"])
                elif annees_experience <= 5:
                    niveau = random.choice(["intermediaire", "intermediaire", "senior"])
                else:
                    niveau = random.choice(["senior", "senior", "expert"])
                
                cs = ConsultantSkill(
                    consultant_id=consultant_id,
                    skill_id=skill_id,
                    niveau=niveau,
                    annees_experience=annees_experience,
                    derniere_utilisation=datetime.now().date() - timedelta(days=random.randint(0, 365)),
                    certification=f"Certified {skill_name} Professional" if random.random() < 0.1 else None,
                    date_creation=datetime.now()
                )
                session.add(cs)
                skills_created.append(cs)
        
        session.commit()
    
    return skills_created


# ==================== SCRIPT PRINCIPAL ====================

def reload_complete_data():
    """Script principal de rechargement complet des données"""
    
    print("\n" + "=" * 70)
    print("🔄 RECHARGEMENT COMPLET DES DONNÉES CONSULTATOR")
    print("=" * 70 + "\n")
    
    # ========== ÉTAPE 1: Reset base de données ==========
    print("🗑️  ÉTAPE 1: Suppression complète de la base de données...")
    reset_database()
    print("✅ Base de données vidée\n")
    
    print("🏗️  ÉTAPE 2: Recréation des tables...")
    init_database()
    print("✅ Tables recréées\n")
    
    # ========== ÉTAPE 2: Lecture fichier Excel ==========
    print(f"📊 ÉTAPE 3: Lecture du fichier Excel VSA...")
    try:
        df = pd.read_excel(EXCEL_VSA_PATH, sheet_name=0)
        print(f"✅ {len(df)} lignes lues depuis Excel\n")
    except Exception as e:
        print(f"❌ Erreur lecture Excel: {e}")
        return False
    
    # ========== ÉTAPE 3: Classification personnes ==========
    print("🔍 ÉTAPE 4: Classification des personnes...")
    
    def classify_with_override(row):
        if is_laurence_oziel(row["firstname"], row["lastname"], row.get("email", "")):
            return "bm"
        return classify_person_by_job_title(row["job_title"])
    
    df["classification"] = df.apply(classify_with_override, axis=1)
    
    classifications = df["classification"].value_counts()
    print(f"👥 {classifications.get('consultant', 0)} consultants")
    print(f"👔 {classifications.get('bm', 0)} business managers\n")
    
    # Identifier BM avec consultants
    bm_with_consultants = set()
    for _, row in df.iterrows():
        if row["classification"] == "consultant":
            manager_name = row["ManagerName"]
            if pd.notna(manager_name):
                bm_with_consultants.add(manager_name.strip())
    
    # Forcer Laurence
    laurence_row = df[df.apply(lambda x: is_laurence_oziel(x["firstname"], x["lastname"], x.get("email", "")), axis=1)]
    if not laurence_row.empty:
        laurence_name = f"{laurence_row.iloc[0]['firstname']} {laurence_row.iloc[0]['lastname']}".strip()
        bm_with_consultants.add(laurence_name)
    
    # ========== ÉTAPE 4: Créer Practices ==========
    print("🏢 ÉTAPE 5: Création des Practices...")
    practices = {}
    practice_names = ["Data & AI", "Cloud & DevOps", "Finance & Trading", "Architecture", "Digital & Web"]
    
    with get_database_session() as session:
        for practice_name in practice_names:
            practice = Practice(
                nom=practice_name,
                description=f"Practice {practice_name}",
                actif=True,
                date_creation=datetime.now()
            )
            session.add(practice)
            session.flush()
            practices[practice_name] = practice.id
        session.commit()
    
    print(f"✅ {len(practices)} practices créées\n")
    
    # ========== ÉTAPE 5: Créer Business Managers ==========
    print("👤 ÉTAPE 6: Création des Business Managers...")
    created_bms = {}
    bm_count = 0
    
    with get_database_session() as session:
        for _, row in df.iterrows():
            if row["classification"] == "bm":
                manager_name = f"{row['firstname']} {row['lastname']}".strip()
                
                if manager_name not in bm_with_consultants and not is_laurence_oziel(row["firstname"], row["lastname"], row.get("email", "")):
                    continue
                
                bm = BusinessManager(
                    nom=row["lastname"].strip(),
                    prenom=row["firstname"].strip(),
                    email=row["email"].strip().lower() if pd.notna(row["email"]) else f"{row['firstname'].lower()}.{row['lastname'].lower()}@quanteam.fr",
                    telephone=row["mobile_number"] if pd.notna(row["mobile_number"]) else None,
                    actif=True,
                    date_creation=datetime.now(),
                )
                
                session.add(bm)
                session.flush()
                created_bms[manager_name] = bm.id
                bm_count += 1
        
        session.commit()
    
    print(f"✅ {bm_count} Business Managers créés\n")
    
    # ========== ÉTAPE 6: Créer Consultants ==========
    print("👥 ÉTAPE 7: Création des consultants avec relations BM...")
    consultant_count = 0
    relations_count = 0
    consultants_map = {}
    consultants_ids = []
    
    with get_database_session() as session:
        for _, row in df.iterrows():
            if row["classification"] != "consultant":
                continue
            
            # Trouver BM
            bm_id = None
            manager_name = row["ManagerName"]
            if pd.notna(manager_name):
                bm_id = created_bms.get(manager_name.strip())
            
            # Créer consultant
            consultant = Consultant(
                nom=row["lastname"].strip(),
                prenom=row["firstname"].strip(),
                email=row["email"].strip().lower() if pd.notna(row["email"]) else f"{row['firstname'].lower()}.{row['lastname'].lower()}@quanteam.fr",
                telephone=row["mobile_number"] if pd.notna(row["mobile_number"]) else None,
                salaire_actuel=float(row["Salaire"]) if pd.notna(row["Salaire"]) else None,
                disponibilite=row["UseActive"].strip().lower() == "active" if pd.notna(row["UseActive"]) else True,
                date_entree_societe=pd.to_datetime(row["contract_date"]).date() if pd.notna(row["contract_date"]) else None,
                type_contrat="cdi",
                societe=row["EntiteCollab"].strip() if pd.notna(row["EntiteCollab"]) else "Quanteam",
                entite=row["EntiteCollab"].strip() if pd.notna(row["EntiteCollab"]) else None,
                actif=row["UseActive"].strip().lower() == "active" if pd.notna(row["UseActive"]) else True,
                date_creation=datetime.now(),
            )
            
            session.add(consultant)
            session.flush()
            
            consultant_key = f"{row['firstname']} {row['lastname']}".strip()
            consultants_map[consultant_key] = consultant.id
            consultants_ids.append(consultant.id)
            
            # Relation BM-consultant
            if bm_id:
                cbm = ConsultantBusinessManager(
                    consultant_id=consultant.id,
                    business_manager_id=bm_id,
                    date_debut=pd.to_datetime(row["contract_date"]).date() if pd.notna(row["contract_date"]) else datetime.now().date(),
                    date_creation=datetime.now(),
                )
                session.add(cbm)
                relations_count += 1
            
            consultant_count += 1
        
        session.commit()
    
    print(f"✅ {consultant_count} consultants créés")
    print(f"🔗 {relations_count} relations BM-consultant établies\n")
    
    # ========== ÉTAPE 7: Générer Missions ==========
    print("💼 ÉTAPE 8: Génération des missions...")
    missions = generate_missions_from_excel(df, consultants_map, practices)
    print(f"✅ {len(missions)} missions créées\n")
    
    # ========== ÉTAPE 8: Générer Langues ==========
    print("🌍 ÉTAPE 9: Génération des langues...")
    languages = generate_languages_for_consultants(consultants_ids)
    print(f"✅ {len(languages)} associations consultant-langue créées\n")
    
    # ========== ÉTAPE 9: Générer Compétences ==========
    print("🎯 ÉTAPE 10: Génération des compétences...")
    skills = generate_skills_for_consultants(consultants_ids)
    print(f"✅ {len(skills)} associations consultant-compétence créées\n")
    
    # ========== RÉSUMÉ FINAL ==========
    print("=" * 70)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 70)
    
    with get_database_session() as session:
        total_bm = session.query(BusinessManager).count()
        total_consultants = session.query(Consultant).count()
        total_relations = session.query(ConsultantBusinessManager).count()
        total_missions = session.query(Mission).count()
        total_languages = session.query(ConsultantLanguage).count()
        total_skills = session.query(ConsultantSkill).count()
        total_practices = session.query(Practice).count()
        
        print(f"👔 Business Managers:          {total_bm}")
        print(f"👥 Consultants:                {total_consultants}")
        print(f"🔗 Relations BM-Consultant:    {total_relations}")
        print(f"💼 Missions:                   {total_missions}")
        print(f"🌍 Langues (associations):     {total_languages}")
        print(f"🎯 Compétences (associations): {total_skills}")
        print(f"🏢 Practices:                  {total_practices}")
    
    print("=" * 70)
    print("\n🎉 RECHARGEMENT TERMINÉ AVEC SUCCÈS!")
    print("💡 Vous pouvez maintenant tester toutes les fonctionnalités de Consultator\n")
    
    return True


if __name__ == "__main__":
    try:
        success = reload_complete_data()
        if not success:
            print("\n❌ Erreur lors du rechargement")
            exit(1)
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
