"""
Configuration pytest alternative avec fichier temporaire Windows-safe
Pour remplacer conftest.py si la solution in-memory ne convient pas
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

# Ajouter les répertoires nécessaires au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, "app"))
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def temp_db_dir():
    """Créer un répertoire temporaire pour la base de test"""
    temp_dir = tempfile.mkdtemp(prefix="consultator_test_")
    yield temp_dir
    # Cleanup avec retry pour Windows
    for attempt in range(3):
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            break
        except (OSError, PermissionError):
            import time

            time.sleep(0.1)  # Attendre 100ms puis retry


@pytest.fixture(scope="session")
def test_db_with_file(temp_db_dir):
    """Base de données de test avec fichier temporaire Windows-safe"""
    from app.database.database import get_database_session
    from app.database.database import init_database
    from app.database.models import Base

    # Fichier dans répertoire temporaire
    db_path = os.path.join(temp_db_dir, "test_consultator.db")
    TEST_DATABASE_URL = f"sqlite:///{db_path}"

    # Configuration SQLite pour Windows
    engine = create_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_timeout=20,
        pool_recycle=300,
        connect_args={
            "check_same_thread": False,  # Autoriser multi-threading
            "timeout": 20,  # Timeout connexion
            "isolation_level": None,  # Autocommit mode
        },
    )

    # Événement pour forcer la fermeture des connexions
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        # Optimisations SQLite pour tests
        cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
        cursor.execute("PRAGMA synchronous=NORMAL")  # Synchronisation rapide
        cursor.execute("PRAGMA temp_store=MEMORY")  # Temp en mémoire
        cursor.execute("PRAGMA mmap_size=268435456")  # Memory mapping
        cursor.close()

    # Créer les tables
    Base.metadata.create_all(engine)

    # Session de test
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,  # Éviter les accès DB après commit
    )

    yield TestSessionLocal

    # Cleanup robuste
    try:
        # Fermer toutes les connexions
        engine.dispose()

        # Forcer la fermeture avec retry
        for attempt in range(5):
            try:
                if os.path.exists(db_path):
                    os.remove(db_path)
                    break
            except (OSError, PermissionError):
                import time

                time.sleep(0.2)  # Attendre 200ms
                if attempt == 4:
                    # Dernier recours : marquer pour suppression au redémarrage
                    try:
                        os.rename(db_path, f"{db_path}.delete_me")
                    except BaseException:
                        pass
    except Exception:
        pass  # Ignore les erreurs de cleanup


@pytest.fixture
def db_session_robust(test_db_with_file):
    """Session de base de données robuste pour Windows"""
    session = test_db_with_file()
    transaction = session.begin()

    try:
        yield session
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise
    finally:
        # Fermeture en 3 étapes
        try:
            session.expunge_all()  # 1. Détacher objets
            session.close()  # 2. Fermer session
        except Exception:
            pass

        # 3. Force garbage collection
        import gc

        gc.collect()


# Fixtures de données identiques


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
        "experience_annees": 5,
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
        "statut": "En cours",
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
