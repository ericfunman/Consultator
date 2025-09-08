"""
Configuration et initialisation de la base de données
Gère la connexion SQLite et la création des tables
Optimisé pour gérer 1000+ consultants avec cache et connexion singleton
"""

import os

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.orm import sessionmaker

from .models import CV
from .models import Base
from .models import Competence
from .models import Consultant
from .models import ConsultantCompetence
from .models import Mission
from .models import Practice

# Configuration de la base de données
DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    '..',
    'data',
    'consultator.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Variable globale pour le contrôle d'initialisation
_database_initialized = False


@st.cache_resource
def get_database_engine():
    """Retourne l'engine de base de données avec cache Streamlit"""
    return create_engine(
        DATABASE_URL,
        echo=False,
        poolclass=pool.StaticPool,
        connect_args={
            "check_same_thread": False,
            "timeout": 30
        },
        pool_pre_ping=True,
        pool_recycle=3600
    )


@st.cache_resource
def get_session_factory():
    """Retourne la factory de sessions avec cache Streamlit"""
    engine = get_database_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database_session():
    """Retourne une session de base de données optimisée"""
    SessionLocal = get_session_factory()
    return SessionLocal()


# Alias pour compatibilité (certains fichiers peuvent avoir l'ancien nom)
get_session = get_database_session


@st.cache_data(ttl=300)  # Cache pendant 5 minutes
def is_database_initialized():
    """Vérifie si la base de données est déjà initialisée (avec cache)"""
    global _database_initialized
    if _database_initialized:
        return True

    if check_database_exists():
        _database_initialized = True
        return True
    return False


def init_database():
    """Initialise la base de données et crée les tables (une seule fois)"""
    global _database_initialized

    # Vérification rapide si déjà initialisée
    if _database_initialized:
        return True

    # Vérification avec cache
    if is_database_initialized():
        return True

    try:
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

        # Obtenir l'engine via le cache
        engine = get_database_engine()

        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)

        # Marquer comme initialisée
        _database_initialized = True

        print(f"✅ Base de données initialisée: {DATABASE_PATH}")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
        return False


def reset_database():
    """Remet à zéro la base de données (supprime et recrée toutes les tables)"""
    global _database_initialized

    try:
        # Obtenir l'engine via le cache
        engine = get_database_engine()

        # Supprimer toutes les tables
        Base.metadata.drop_all(bind=engine)

        # Recréer toutes les tables
        Base.metadata.create_all(bind=engine)

        # Réinitialiser le flag
        _database_initialized = True

        # Vider le cache
        is_database_initialized.clear()

        print("✅ Base de données remise à zéro")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la remise à zéro: {e}")
        return False


def check_database_exists():
    """Vérifie si la base de données existe"""
    return os.path.exists(DATABASE_PATH)


@st.cache_data(ttl=600)  # Cache pendant 10 minutes
def get_database_info():
    """Retourne des informations sur la base de données (avec cache)"""
    if not check_database_exists():
        return {"exists": False}

    try:
        with get_database_session() as session:
            consultant_count = session.query(Consultant).count()
            competence_count = session.query(Competence).count()
            mission_count = session.query(Mission).count()
            practice_count = session.query(Practice).count()

            return {
                "exists": True,
                "path": DATABASE_PATH,
                "consultants": consultant_count,
                "competences": competence_count,
                "missions": mission_count,
                "practices": practice_count
            }
    except Exception as e:
        return {"exists": True, "error": str(e)}
