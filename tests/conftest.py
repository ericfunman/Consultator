"""
Configuration pytest pour Consultator
Tests automatiques avec coverage et validation de non-régression
"""

import pytest
import sys
import os
from pathlib import Path

# Ajouter les répertoires nécessaires au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, 'app'))
sys.path.insert(0, project_root)

# Configuration de base de données de test
TEST_DATABASE_URL = "sqlite:///:memory:"  # Base en mémoire - pas de fichier

@pytest.fixture(scope="session")
def test_db():
    """Base de données de test en mémoire (Windows-safe)"""
    from app.database.database import init_database, get_database_session
    from app.database.models import Base
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
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
        # Rollback en cas d'erreur
        session.rollback()
        raise
    finally:
        # Fermeture propre de la session
        try:
            session.expunge_all()  # Détacher tous les objets
            session.close()
        except Exception:
            pass  # Ignore les erreurs de fermeture

@pytest.fixture
def sample_consultant_data():
    """Données de test pour un consultant"""
    return {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@test.com",
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
    import streamlit as st
    from unittest.mock import MagicMock
    
    # Mock des fonctions Streamlit
    st.write = MagicMock()
    st.error = MagicMock()
    st.success = MagicMock()
    st.warning = MagicMock()
    st.info = MagicMock()
    
    return st
