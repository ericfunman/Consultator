"""
Configuration pytest pour Consultator
Tests automatiques avec coverage et validation de non-régression
"""

import os
import sys
from pathlib import Path

import pytest

# Ajouter les répertoires nécessaires au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, 'app'))
sys.path.insert(0, project_root)

# Configuration de base de données de test
TEST_DATABASE_URL = "sqlite:///:memory:"  # Base en mémoire - pas de fichier


@pytest.fixture(scope="session")
def test_db():
    """Base de données de test en mémoire (Windows-safe)"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app.database.database import get_database_session
    from app.database.database import init_database
    from app.database.models import Base

    # Créer engine de test en mémoire
    engine = create_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,  # Vérifier les connexions
        pool_recycle=300     # Recycler les connexions
    )
    Base.metadata.create_all(engine)

    # Session de test
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield TestSessionLocal

    # Cleanup automatique (mémoire libérée)
    try:
        Base.metadata.drop_all(engine)
        engine.dispose()  # Fermer toutes les connexions
    except Exception:
        pass  # Ignore les erreurs de cleanup


@pytest.fixture
def db_session(test_db):
    """Session de base de données pour chaque test avec gestion robuste"""
    session = test_db()
    try:
        yield session
        # Commit des changements si pas d'erreur
        session.commit()
    except Exception:
        # En cas d'erreur, faire un rollback explicite
        try:
            session.rollback()
        except Exception:
            pass  # Ignorer les erreurs de rollback
        raise
    finally:
        try:
            session.expunge_all()  # Détacher tous les objets
            session.close()
        except Exception:
            pass  # Ignorer les erreurs de fermeture


@pytest.fixture
def sample_consultant_data():
    """Données de test pour un consultant avec email unique"""
    import uuid
    unique_id = uuid.uuid4().hex[:8]
    return {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": f"jean.dupont.{unique_id}@test.com",
        "telephone": "0123456789",
        "disponibilite": True,
        "salaire_souhaite": 45000,
        "experience_annees": 5
    }


@pytest.fixture
def sample_mission_data():
    """Données de test pour une mission"""
    return {
        "titre": "Mission Test",
        "client": "Client Test",
        "description": "Description de test",
        "duree_mois": 6,
        "tarif_jour": 450,
        "statut": "En cours"
    }

# Configuration Streamlit pour les tests


@pytest.fixture
def streamlit_app():
    """Mock Streamlit pour les tests"""
    from unittest.mock import MagicMock

    import streamlit as st

    # Mock des fonctions Streamlit
    st.write = MagicMock()
    st.error = MagicMock()
    st.success = MagicMock()
    st.warning = MagicMock()
    st.info = MagicMock()

    return st
