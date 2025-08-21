"""
Configuration pytest pour Consultator
Tests automatiques avec coverage et validation de non-régression
"""

import pytest
import sys
import os
from pathlib import Path

# Ajouter le répertoire app au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Configuration de base de données de test
TEST_DATABASE_URL = "sqlite:///test_consultator.db"

@pytest.fixture(scope="session")
def test_db():
    """Base de données de test"""
    from database.database import init_database, get_database_session
    from database.models import Base
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Créer engine de test
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)
    
    # Session de test
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestSessionLocal
    
    # Cleanup
    Base.metadata.drop_all(engine)
    test_db_file = Path("test_consultator.db")
    if test_db_file.exists():
        test_db_file.unlink()

@pytest.fixture
def db_session(test_db):
    """Session de base de données pour chaque test"""
    session = test_db()
    try:
        yield session
    finally:
        session.close()

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
