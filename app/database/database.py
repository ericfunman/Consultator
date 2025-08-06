"""
Configuration et initialisation de la base de données
Gère la connexion SQLite et la création des tables
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Consultant, Competence, ConsultantCompetence, Mission, CV

# Configuration de la base de données
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'consultator.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database_session():
    """Retourne une session de base de données"""
    return SessionLocal()

def init_database():
    """Initialise la base de données et crée les tables"""
    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        
        print(f"✅ Base de données initialisée: {DATABASE_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
        return False

def reset_database():
    """Remet à zéro la base de données (supprime et recrée toutes les tables)"""
    try:
        # Supprimer toutes les tables
        Base.metadata.drop_all(bind=engine)
        
        # Recréer toutes les tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Base de données remise à zéro")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la remise à zéro: {e}")
        return False

def check_database_exists():
    """Vérifie si la base de données existe"""
    return os.path.exists(DATABASE_PATH)

def get_database_info():
    """Retourne des informations sur la base de données"""
    if not check_database_exists():
        return {"exists": False}
    
    try:
        with get_database_session() as session:
            consultant_count = session.query(Consultant).count()
            competence_count = session.query(Competence).count()
            mission_count = session.query(Mission).count()
            
            return {
                "exists": True,
                "path": DATABASE_PATH,
                "consultants": consultant_count,
                "competences": competence_count,
                "missions": mission_count
            }
    except Exception as e:
        return {"exists": True, "error": str(e)}
