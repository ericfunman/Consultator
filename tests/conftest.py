"""
Configuration pytest pour Consultator
Tests automatiques avec coverage et validation de non-régression
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Ajouter les répertoires nécessaires au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, "app"))
sys.path.insert(0, project_root)

# Configuration de base de données de test
TEST_DATABASE_URL = "sqlite:///:memory:"  # Base en mémoire - pas de fichier


@pytest.fixture(scope="session")
def test_db():
    """Base de données de test en mémoire (Windows-safe)"""
    try:
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
            pool_recycle=300,  # Recycler les connexions
        )
        Base.metadata.create_all(engine)

        # Session de test
        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        yield TestSessionLocal

        # Cleanup automatique (mémoire libérée)
        try:
            Base.metadata.drop_all(engine)
            engine.dispose()  # Fermer toutes les connexions
        except Exception as exc:
            pass  # Ignore les erreurs de cleanup
    except ImportError as e:
        # Si les modules de l'app ne sont pas disponibles, retourner un mock
        from unittest.mock import MagicMock

        pytest.skip(f"Modules de l'application non disponibles: {e}")
        yield MagicMock()


@pytest.fixture
def db_session(test_db):
    """Session de base de données pour chaque test avec gestion robuste"""
    session = test_db()
    try:
        yield session
        # Commit des changements si pas d'erreur
        session.commit()
    except Exception as exc:
        # En cas d'erreur, faire un rollback explicite
        try:
            session.rollback()
        except Exception as exc:
            pass  # Ignorer les erreurs de rollback
        raise
    finally:
        try:
            session.expunge_all()  # Détacher tous les objets
            session.close()
        except Exception as exc:
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


# ===== FIXTURES POUR CORRIGER LES ERREURS =====


@pytest.fixture(scope="function")
def mock_sqlalchemy_models():
    """Mock des modèles SQLAlchemy pour éviter les erreurs de query - scope function pour isolation"""
    from datetime import date
    from datetime import datetime
    from unittest.mock import MagicMock
    from unittest.mock import patch

    # Mock des modèles principaux avec support SQLAlchemy
    mock_consultant = MagicMock()
    mock_consultant.id = 1
    mock_consultant.nom = "Dupont"
    mock_consultant.prenom = "Jean"
    mock_consultant.email = "jean.dupont@test.com"
    mock_consultant.telephone = "0123456789"
    mock_consultant.date_entree = date.today()
    mock_consultant.disponibilite = True
    mock_consultant.salaire_souhaite = 45000
    mock_consultant.experience_annees = 5
    # Ajouter les attributs nécessaires pour les relations
    mock_consultant.practice = MagicMock()
    mock_consultant.practice.nom = "Data Science"
    mock_consultant.business_manager = MagicMock()
    mock_consultant.business_manager.nom = "Martin"
    mock_consultant.business_manager.prenom = "Sophie"

    mock_practice = MagicMock()
    mock_practice.id = 1
    mock_practice.nom = "Data Science"
    mock_practice.actif = True

    mock_business_manager = MagicMock()
    mock_business_manager.id = 1
    mock_business_manager.nom = "Martin"
    mock_business_manager.prenom = "Sophie"
    mock_business_manager.email = "sophie.martin@test.com"

    # Mock des autres modèles nécessaires
    mock_mission = MagicMock()
    mock_mission.id = 1
    mock_mission.client = "Test Corp"
    mock_mission.role = "Developer"
    mock_mission.date_debut = date.today()
    mock_mission.date_fin = None
    mock_mission.statut = "en_cours"
    mock_mission.technologies_utilisees = "Python, Django"
    mock_mission.description = "Test mission"
    mock_mission.revenus_generes = 50000

    mock_competence = MagicMock()
    mock_competence.id = 1
    mock_competence.nom = "Python"
    mock_competence.categorie = "Langage"
    mock_competence.type_competence = "technique"

    mock_consultant_competence = MagicMock()
    mock_consultant_competence.id = 1
    mock_consultant_competence.niveau_maitrise = "Avancé"
    mock_consultant_competence.annees_experience = 3

    mock_langue = MagicMock()
    mock_langue.id = 1
    mock_langue.nom = "Français"
    mock_langue.code_iso = "FR"

    mock_consultant_langue = MagicMock()
    mock_consultant_langue.id = 1
    mock_consultant_langue.niveau = 5
    mock_consultant_langue.niveau_label = "Natiff"
    mock_consultant_langue.commentaire = "Langue maternelle"

    # Mock des classes de modèles pour les queries SQLAlchemy avec support des opérations
    mock_consultant_class = MagicMock()
    # Simuler les colonnes SQLAlchemy pour les expressions avec tous les opérateurs nécessaires
    mock_consultant_class.id = MagicMock()
    mock_consultant_class.id.__eq__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.__ne__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.__gt__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.__lt__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.__ge__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.__le__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.like = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.ilike = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.in_ = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.is_ = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.isnot = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.desc = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.asc = MagicMock(return_value=MagicMock())
    mock_consultant_class.id.label = MagicMock(return_value=MagicMock())

    mock_consultant_class.nom = MagicMock()
    mock_consultant_class.nom.__eq__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.nom.__ne__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.nom.like = MagicMock(return_value=MagicMock())
    mock_consultant_class.nom.ilike = MagicMock(return_value=MagicMock())
    mock_consultant_class.nom.in_ = MagicMock(return_value=MagicMock())
    mock_consultant_class.nom.label = MagicMock(return_value=MagicMock())

    mock_consultant_class.prenom = MagicMock()
    mock_consultant_class.prenom.__eq__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.prenom.like = MagicMock(return_value=MagicMock())
    mock_consultant_class.prenom.ilike = MagicMock(return_value=MagicMock())
    mock_consultant_class.prenom.label = MagicMock(return_value=MagicMock())

    mock_consultant_class.email = MagicMock()
    mock_consultant_class.email.__eq__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.email.like = MagicMock(return_value=MagicMock())
    mock_consultant_class.email.ilike = MagicMock(return_value=MagicMock())
    mock_consultant_class.email.label = MagicMock(return_value=MagicMock())

    mock_consultant_class.telephone = MagicMock()
    mock_consultant_class.date_entree = MagicMock()
    mock_consultant_class.disponibilite = MagicMock()
    mock_consultant_class.disponibilite.__eq__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.disponibilite.__ne__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.disponibilite.is_ = MagicMock(return_value=MagicMock())
    mock_consultant_class.disponibilite.isnot = MagicMock(return_value=MagicMock())
    mock_consultant_class.disponibilite.label = MagicMock(return_value=MagicMock())

    mock_consultant_class.salaire_souhaite = MagicMock()
    mock_consultant_class.experience_annees = MagicMock()
    mock_consultant_class.practice_id = MagicMock()
    mock_consultant_class.practice_id.__eq__ = MagicMock(return_value=MagicMock())
    mock_consultant_class.practice_id.is_ = MagicMock(return_value=MagicMock())
    mock_consultant_class.practice_id.isnot = MagicMock(return_value=MagicMock())
    mock_consultant_class.date_creation = MagicMock()
    mock_consultant_class.derniere_maj = MagicMock()

    mock_practice_class = MagicMock()
    mock_practice_class.id = MagicMock()
    mock_practice_class.id.__eq__ = MagicMock(return_value=MagicMock())
    mock_practice_class.id.__ne__ = MagicMock(return_value=MagicMock())
    mock_practice_class.id.__gt__ = MagicMock(return_value=MagicMock())
    mock_practice_class.id.__lt__ = MagicMock(return_value=MagicMock())
    mock_practice_class.id.like = MagicMock(return_value=MagicMock())
    mock_practice_class.id.ilike = MagicMock(return_value=MagicMock())
    mock_practice_class.id.in_ = MagicMock(return_value=MagicMock())
    mock_practice_class.id.label = MagicMock(return_value=MagicMock())

    mock_practice_class.nom = MagicMock()
    mock_practice_class.nom.__eq__ = MagicMock(return_value=MagicMock())
    mock_practice_class.nom.__ne__ = MagicMock(return_value=MagicMock())
    mock_practice_class.nom.like = MagicMock(return_value=MagicMock())
    mock_practice_class.nom.ilike = MagicMock(return_value=MagicMock())
    mock_practice_class.nom.in_ = MagicMock(return_value=MagicMock())
    mock_practice_class.nom.label = MagicMock(return_value=MagicMock())

    mock_practice_class.actif = MagicMock()
    mock_practice_class.actif.__eq__ = MagicMock(return_value=MagicMock())
    mock_practice_class.actif.__ne__ = MagicMock(return_value=MagicMock())
    mock_practice_class.actif.is_ = MagicMock(return_value=MagicMock())
    mock_practice_class.actif.isnot = MagicMock(return_value=MagicMock())
    mock_practice_class.actif.label = MagicMock(return_value=MagicMock())

    # Mock des fonctions SQLAlchemy communes
    mock_func = MagicMock()
    mock_func.count = MagicMock(return_value=MagicMock())

    # Patch des modèles et classes avec gestion des imports
    patches = []
    try:
        # Patch des modèles principaux - seulement si disponibles
        try:
            patches.append(
                patch("app.database.models.Consultant", mock_consultant_class)
            )
            patches.append(patch("app.database.models.Practice", mock_practice_class))
            patches.append(patch("app.database.models.BusinessManager", MagicMock()))
            patches.append(patch("app.database.models.Mission", MagicMock()))
            patches.append(patch("app.database.models.Competence", MagicMock()))
            patches.append(
                patch("app.database.models.ConsultantCompetence", MagicMock())
            )
            patches.append(patch("app.database.models.Langue", MagicMock()))
            patches.append(patch("app.database.models.ConsultantLangue", MagicMock()))
            patches.append(patch("sqlalchemy.func", mock_func))
        except ImportError:
            # Si les modules ne sont pas disponibles, ne pas patcher
            pass

        # Démarrer tous les patches
        for p in patches:
            p.start()

        yield {
            "consultant": mock_consultant,
            "practice": mock_practice,
            "business_manager": mock_business_manager,
            "mission": mock_mission,
            "competence": mock_competence,
            "consultant_competence": mock_consultant_competence,
            "langue": mock_langue,
            "consultant_langue": mock_consultant_langue,
            "consultant_class": mock_consultant_class,
            "practice_class": mock_practice_class,
        }

    finally:
        # Arrêter tous les patches
        for p in patches:
            p.stop()


@pytest.fixture(scope="function")
def mock_session_state():
    """Mock du session state Streamlit avec les clés nécessaires - scope function pour isolation"""
    from unittest.mock import MagicMock
    from unittest.mock import patch

    # Créer un mock de session_state frais pour chaque test
    class MockSessionState(dict):
        def __init__(self):
            super().__init__()
            # Initialiser tous les attributs courants utilisés dans les tests
            self.view_consultant_profile = 1
            self.selected_consultant_id = 1
            self.show_add_form = False
            self.search_query = ""
            self.filter_practice = None
            self.filter_disponibilite = None
            self.show_dashboard_charts = MagicMock()
            self.get_database_info = MagicMock()
            self.st = MagicMock()
            self.view_business_manager_profile = 1
            self.selected_business_manager_id = 1
            self.show_add_bm_form = False
            self.bm_search_query = ""
            self.current_page = "consultants"
            self.page_size = 10
            self.sort_by = "nom"
            self.sort_order = "asc"
            self.search_results = []
            self.current_page_num = 1
            self.filters = {}
            self.show_filters = False
            self.selected_practice = None
            self.selected_bm = None
            self.selected_competence = None
            self.selected_langue = None
            self.min_experience = 0
            self.max_experience = 20
            self.min_salaire = 0
            self.max_salaire = 100000
            self.disponibilite = None
            self.chat_messages = []
            self.chat_input = ""
            self.show_chat = False
            self.uploaded_file = None
            self.cv_analysis_result = None
            self.show_cv_analysis = False
            self.selected_cv = None
            self.show_cv_details = False
            self.current_view = "search"
            self.navigation_history = []
            self.user_role = "user"
            self.user_permissions = []
            self.last_action = None
            self.error_message = None
            self.success_message = None
            self.warning_message = None
            self.info_message = None

        def __setattr__(self, name, value):
            # Permettre l'accès comme attribut et comme dict
            super().__setattr__(name, value)
            if name not in ["clear", "keys", "values", "items", "get", "pop", "update"]:
                self[name] = value

        def __getattr__(self, name):
            # Permettre l'accès comme attribut
            try:
                return self[name]
            except KeyError:
                # Retourner None pour les attributs non définis au lieu de lever une erreur
                return None

        def get(self, key, default=None):
            return super().get(key, default)

        def __contains__(self, key):
            return key in dict(self)

    mock_session_state = MockSessionState()

    with patch("streamlit.session_state", mock_session_state):
        yield mock_session_state


@pytest.fixture(scope="function", autouse=True)
def mock_streamlit_complete():
    """Mock complet de Streamlit avec tous les composants nécessaires - scope function pour isolation"""
    from datetime import date
    from unittest.mock import MagicMock
    from unittest.mock import patch

    # Utiliser un context manager plus simple avec moins de patches
    mock_patches = {}

    # Liste des fonctions Streamlit à mocker
    streamlit_functions = [
        "title",
        "header",
        "subheader",
        "write",
        "success",
        "error",
        "warning",
        "info",
        "columns",
        "tabs",
        "form",
        "form_submit_button",
        "text_input",
        "text_area",
        "selectbox",
        "checkbox",
        "button",
        "table",
        "dataframe",
        "date_input",
        "number_input",
        "file_uploader",
        "rerun",
        "metric",
        "expander",
        "empty",
        "radio",
    ]

    # Créer les patches
    patches = []
    for func in streamlit_functions:
        patch_obj = patch(f"streamlit.{func}")
        patches.append(patch_obj)

    # Ajouter un patch spécifique pour le module consultants qui pose problème
    try:
        patches.append(patch("app.pages_modules.consultants.st.tabs"))
    except ImportError:
        # Le module n'est pas encore importé, c'est normal
        pass

    # Démarrer tous les patches
    started_patches = []
    for patch_obj in patches:
        started_patches.append(patch_obj.start())
        if len(started_patches) <= len(streamlit_functions):
            mock_patches[streamlit_functions[len(started_patches) - 1]] = (
                started_patches[-1]
            )

    try:
        # Configuration des mocks
        mock_patches["columns"].return_value = [MagicMock(), MagicMock()]
        
        # Mock tabs pour retourner des context managers appropriés
        class MockTabContextManager(MagicMock):
            def __enter__(self):
                return self
            def __exit__(self, *exc):
                pass
        
        mock_patches["tabs"].return_value = [MockTabContextManager(), MockTabContextManager(), MockTabContextManager()]
        
        # Configurer aussi le patch spécifique si disponible
        if len(started_patches) > len(streamlit_functions):
            specific_tabs_patch = started_patches[-1]
            specific_tabs_patch.return_value = [MockTabContextManager(), MockTabContextManager(), MockTabContextManager()]
        
        mock_patches["form"].return_value.__enter__ = MagicMock(return_value=None)
        mock_patches["form"].return_value.__exit__ = MagicMock(return_value=None)
        mock_patches["form_submit_button"].return_value = False
        mock_patches["file_uploader"].return_value = None
        mock_patches["dataframe"].return_value = MagicMock()
        mock_patches["expander"].return_value.__enter__ = MagicMock(return_value=None)
        mock_patches["expander"].return_value.__exit__ = MagicMock(return_value=None)
        mock_patches["radio"].return_value = "Option 1"

        # Mock des inputs avec valeurs par défaut appropriées
        mock_patches["text_input"].side_effect = [
            "Dupont",
            "Jean",
            "jean.dupont@test.com",
            "0123456789",
            "",
        ]

        # Mock date_input qui accepte les objets date
        def mock_date_input_func(label, value=None, **kwargs):
            if isinstance(value, date):
                return value
            return date.today()

        mock_patches["date_input"].side_effect = mock_date_input_func

        mock_patches["text_area"].return_value = "Description test"
        mock_patches["selectbox"].return_value = None
        mock_patches["checkbox"].return_value = True
        mock_patches["button"].return_value = False
        mock_patches["number_input"].return_value = 45000

        yield mock_patches

    finally:
        # Arrêter tous les patches
        for patch_obj in patches:
            patch_obj.stop()


@pytest.fixture(scope="function", autouse=True)
def mock_sqlalchemy_models_global():
    """Mock global des modèles SQLAlchemy pour tous les tests"""
    from unittest.mock import MagicMock
    from unittest.mock import patch

    # Créer des mocks simples pour les modèles
    class MockPractice:
        def __init__(self, id=1, nom="Data Science", actif=True):
            self.id = id
            self.nom = nom
            self.actif = actif

    class MockConsultant:
        def __init__(self, id=1, nom="Dupont", prenom="Jean", email="test@test.com"):
            self.id = id
            self.nom = nom
            self.prenom = prenom
            self.email = email
            self.telephone = "0123456789"
            self.date_entree = "2023-01-01"
            self.disponibilite = True
            self.salaire_souhaite = 45000
            self.experience_annees = 5
            self.practice_id = 1
            self.date_creation = "2023-01-01"
            self.derniere_maj = "2023-01-01"
            # Mock des relations
            self.business_manager_gestions = []
            self.practice = MockPractice()
            self.missions = []
            self.competences = []
            self.langues = []
            self.cvs = []
            self.salaires = []

        @property
        def nom_complet(self):
            return f"{self.prenom} {self.nom}"

        @property
        def business_manager_actuel(self):
            """Retourne le Business Manager actuel du consultant"""
            for cbm in self.business_manager_gestions:
                if cbm.date_fin is None:
                    return cbm.business_manager
            return None

    # Mock du query builder qui intercepte toutes les queries
    class MockQuery:
        def __init__(self, *entities):
            self.entities = entities

        def filter(self, *conditions):
            return self

        def all(self):
            # Retourner des mocks appropriés selon le type d'entité
            if self.entities:
                entity_name = str(self.entities[0]).lower()
                if "practice" in entity_name:
                    return [MockPractice(id=1, nom="Data Science", actif=True)]
                elif "consultant" in entity_name:
                    return [MockConsultant(id=1, nom="Dupont", prenom="Jean")]
            return [MockPractice(id=1, nom="Data Science", actif=True)]

        def first(self):
            results = self.all()
            return results[0] if results else None

        def count(self):
            return len(self.all())

        def limit(self, n):
            return self

        def offset(self, n):
            return self

    # Mock de la session qui intercepte complètement les queries
    class MockSession:
        def query(self, *entities):
            return MockQuery(*entities)

        def add(self, obj):
            pass

        def commit(self):
            pass

        def rollback(self):
            pass

        def close(self):
            pass

        def delete(self, obj):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    mock_session = MockSession()

    # Patch seulement les modules qui existent réellement
    patches = []
    try:
        # Patch des sessions de base de données - seulement si les modules sont disponibles
        try:
            patches.append(
                patch(
                    "app.database.database.get_database_session",
                    return_value=mock_session,
                )
            )
            patches.append(
                patch("app.database.database.session_local", return_value=mock_session)
            )
        except ImportError:
            # Si les modules de l'app ne sont pas disponibles, ne pas patcher
            pass

        # Démarrer tous les patches
        for p in patches:
            p.start()

        yield

    finally:
        # Arrêter tous les patches
        for p in patches:
            p.stop()


@pytest.fixture(scope="function")
def sample_date_data():
    """Données de test avec dates correctement formatées - scope function pour isolation"""
    from datetime import date
    from datetime import datetime
    from datetime import timedelta

    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Créer un objet avec attributs pour compatibilité
    class DateData:
        def __init__(self):
            self.date_entree = today
            self.date_naissance = date(1990, 1, 1)
            self.date_disponibilite = today
            self.datetime_creation = datetime.now()
            self.date_iso = today.isoformat()
            self.today = today
            self.tomorrow = tomorrow
            self.now = datetime.now()

        def __getitem__(self, key):
            return getattr(self, key)

        def __contains__(self, key):
            return hasattr(self, key)

    return DateData()


@pytest.fixture(scope="function")
def mock_services():
    """Mock des services métier principaux - scope function pour isolation"""
    from unittest.mock import MagicMock
    from unittest.mock import patch

    # Mock ConsultantService
    mock_consultant_service = MagicMock()
    mock_consultant_service.get_all_consultants = MagicMock(return_value=[])
    mock_consultant_service.get_consultant_by_id = MagicMock(return_value=None)
    mock_consultant_service.create_consultant = MagicMock(return_value=MagicMock(id=1))
    mock_consultant_service.update_consultant = MagicMock(return_value=True)
    mock_consultant_service.delete_consultant = MagicMock(return_value=True)
    mock_consultant_service.search_consultants = MagicMock(return_value=[])

    # Mock BusinessManagerService
    mock_bm_service = MagicMock()
    mock_bm_service.get_all_business_managers = MagicMock(return_value=[])
    mock_bm_service.get_business_manager_by_id = MagicMock(return_value=None)
    mock_bm_service.create_business_manager = MagicMock(return_value=MagicMock(id=1))
    mock_bm_service.update_business_manager = MagicMock(return_value=True)
    mock_bm_service.delete_business_manager = MagicMock(return_value=True)

    # Mock PracticeService
    mock_practice_service = MagicMock()
    mock_practice_service.get_all_practices = MagicMock(return_value=[])
    mock_practice_service.get_practice_by_id = MagicMock(return_value=None)

    # Essayer de patcher seulement si les modules sont disponibles
    try:
        with patch(
            "services.consultant_service.ConsultantService", mock_consultant_service
        ), patch(
            "services.business_manager_service.BusinessManagerService", mock_bm_service
        ), patch(
            "services.practice_service.PracticeService", mock_practice_service
        ):
            yield {
                "consultant_service": mock_consultant_service,
                "business_manager_service": mock_bm_service,
                "practice_service": mock_practice_service,
            }
    except ImportError:
        # Si les modules de services ne sont pas disponibles, retourner quand même les mocks
        yield {
            "consultant_service": mock_consultant_service,
            "business_manager_service": mock_bm_service,
            "practice_service": mock_practice_service,
        }


# Mock global pour ConsultantService utilisé dans les tests
mock_consultant_service = MagicMock()
mock_consultant_service.get_all_consultants_with_stats.return_value = []
mock_consultant_service.search_consultants_optimized.return_value = []
mock_consultant_service.get_consultant_by_email.return_value = None
mock_consultant_service.create_consultant.return_value = True
mock_consultant_service.update_consultant.return_value = True
mock_consultant_service.delete_consultant.return_value = True


@pytest.fixture(scope="function", autouse=True)
def auto_mocks(request):
    """Mocks automatiques appliqués à tous les tests pour corriger les erreurs communes"""
    from datetime import date
    from unittest.mock import MagicMock
    from unittest.mock import patch

    # Skip streamlit mocking for UI tests and v122 tests to avoid DeltaGeneratorSingleton conflicts
    test_file_name = request.fspath.basename if hasattr(request, "fspath") else ""
    is_ui_test = "test_ui_" in test_file_name or "test_v122" in test_file_name

    patches = []

    try:
        if not is_ui_test:
            # Mock session state avec toutes les clés nécessaires utilisant la classe améliorée
            class MockSessionState(dict):
                def __init__(self):
                    super().__init__()
                    # Initialiser tous les attributs courants utilisés dans les tests
                    self.view_consultant_profile = 1
                    self.selected_consultant_id = 1
                    self.show_add_form = False
                    self.search_query = ""
                    self.filter_practice = None
                    self.filter_disponibilite = None
                    self.show_dashboard_charts = MagicMock()
                    self.get_database_info = MagicMock()
                    self.st = MagicMock()
                    self.view_business_manager_profile = 1
                    self.selected_business_manager_id = 1
                    self.show_add_bm_form = False
                    self.bm_search_query = ""
                    self.current_page = "consultants"
                    self.page_size = 10
                    self.sort_by = "nom"
                    self.sort_order = "asc"
                    self.search_results = []
                    self.current_page_num = 1
                    self.filters = {}
                    self.show_filters = False
                    self.selected_practice = None
                    self.selected_bm = None
                    self.selected_competence = None
                    self.selected_langue = None
                    self.min_experience = 0
                    self.max_experience = 20
                    self.min_salaire = 0
                    self.max_salaire = 100000
                    self.disponibilite = None
                    self.chat_messages = []
                    self.chat_input = ""
                    self.show_chat = False
                    self.uploaded_file = None
                    self.cv_analysis_result = None
                    self.show_cv_analysis = False
                    self.selected_cv = None
                    self.show_cv_details = False
                    self.current_view = "search"
                    self.navigation_history = []
                    self.user_role = "user"
                    self.user_permissions = []
                    self.last_action = None
                    self.error_message = None
                    self.success_message = None
                    self.warning_message = None
                    self.info_message = None

                def __setattr__(self, name, value):
                    # Permettre l'accès comme attribut et comme dict
                    super().__setattr__(name, value)
                    if name not in [
                        "clear",
                        "keys",
                        "values",
                        "items",
                        "get",
                        "pop",
                        "update",
                    ]:
                        self[name] = value

                def __getattr__(self, name):
                    # Permettre l'accès comme attribut
                    try:
                        return self[name]
                    except KeyError:
                        # Retourner None pour les attributs non définis au lieu de lever une erreur
                        return None

                def get(self, key, default=None):
                    return super().get(key, default)

                def __contains__(self, key):
                    return key in dict(self)

            mock_session = MockSessionState()

            # Patch streamlit.session_state directement seulement pour les tests non-UI
            patches.append(patch("streamlit.session_state", mock_session))

            # Mock date_input amélioré
            def mock_date_input_func(label, value=None, **kwargs):
                if isinstance(value, date):
                    return value
                return date.today()

            patches.append(
                patch("streamlit.date_input", side_effect=mock_date_input_func)
            )

        # Démarrer tous les patches
        for p in patches:
            p.start()

        yield

    finally:
        # Arrêter tous les patches
        for p in patches:
            p.stop()


@pytest.fixture(scope="function", autouse=True)
def mock_streamlit_singleton():
    """Mock pour éviter les erreurs DeltaGeneratorSingleton dans les tests UI"""
    # Supprimé car DeltaGeneratorSingleton n'existe pas dans cette version de Streamlit
    yield


@pytest.fixture(scope="function", autouse=True)
def disable_streamlit_cache():
    """Disable Streamlit caching during tests to avoid pickling mock objects"""
    from unittest.mock import MagicMock
    from unittest.mock import patch

    def mock_cache_data(*args, **kwargs):
        """Mock cache_data decorator that just returns the original function"""
        if len(args) == 1 and callable(args[0]):
            # Used as @st.cache_data
            return args[0]
        else:
            # Used as @st.cache_data(ttl=300)
            def decorator(func):
                return func

            return decorator

    def mock_cache_resource(*args, **kwargs):
        """Mock cache_resource decorator that just returns the original function"""
        if len(args) == 1 and callable(args[0]):
            # Used as @st.cache_resource
            return args[0]
        else:
            # Used as @st.cache_resource
            def decorator(func):
                return func

            return decorator

    patches = []
    try:
        patches.append(patch("streamlit.cache_data", mock_cache_data))
        patches.append(patch("streamlit.cache_resource", mock_cache_resource))

        # Démarrer les patches
        for p in patches:
            p.start()

        yield

    finally:
        # Arrêter les patches
        for p in patches:
            p.stop()


@pytest.fixture(scope="function")
def mock_session():
    """Mock de session de base de données pour les tests qui en ont besoin"""
    from unittest.mock import MagicMock

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()
    mock_session.delete = MagicMock()
    mock_session.query = MagicMock()

    return mock_session


@pytest.fixture(scope="function")
def mock_database_session():
    """Mock de session de base de données pour les tests qui utilisent cette fixture spécifique"""
    from unittest.mock import MagicMock

    mock_session = MagicMock()
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()
    mock_session.delete = MagicMock()
    mock_session.query = MagicMock()

    # Mock du query builder qui intercepte toutes les queries
    class MockQuery:
        def __init__(self, *entities):
            self.entities = entities

        def filter(self, *conditions):
            return self

        def all(self):
            # Retourner des mocks appropriés selon le type d'entité
            if self.entities:
                entity_name = str(self.entities[0]).lower()
                if "practice" in entity_name:
                    return [MockPractice(id=1, nom="Data Science", actif=True)]
                elif "consultant" in entity_name:
                    return [MockConsultant(id=1, nom="Dupont", prenom="Jean")]
            return []

        def first(self):
            results = self.all()
            return results[0] if results else None

        def count(self):
            return len(self.all())

        def limit(self, n):
            return self

        def offset(self, n):
            return self

    # Créer des mocks simples pour les modèles
    class MockPractice:
        def __init__(self, id=1, nom="Data Science", actif=True):
            self.id = id
            self.nom = nom
            self.actif = actif

    class MockConsultant:
        def __init__(self, id=1, nom="Dupont", prenom="Jean", email="test@test.com"):
            self.id = id
            self.nom = nom
            self.prenom = prenom
            self.email = email
            self.telephone = "0123456789"
            self.date_entree = "2023-01-01"
            self.disponibilite = True
            self.salaire_souhaite = 45000
            self.experience_annees = 5
            self.practice_id = 1
            self.date_creation = "2023-01-01"
            self.derniere_maj = "2023-01-01"
            # Mock des relations
            self.business_manager_gestions = []
            self.practice = MockPractice()
            self.missions = []
            self.competences = []
            self.langues = []
            self.cvs = []
            self.salaires = []

        @property
        def nom_complet(self):
            return f"{self.prenom} {self.nom}"

        @property
        def business_manager_actuel(self):
            """Retourne le Business Manager actuel du consultant"""
            for cbm in self.business_manager_gestions:
                if cbm.date_fin is None:
                    return cbm.business_manager
            return None

    mock_session.query.side_effect = lambda *entities: MockQuery(*entities)

    return mock_session


@pytest.fixture(scope="function")
def ui_test_streamlit_mock():
    """Special fixture for UI tests to avoid DeltaGeneratorSingleton conflicts"""
    from unittest.mock import MagicMock

    class UIStreamlitMock:
        """Mock for UI tests that doesn't try to import actual streamlit"""

        def __init__(self):
            self.session_state = MagicMock()
            self.session_state.view_consultant_profile = 1

        def __getattr__(self, name):
            """Return appropriate mocks for streamlit functions"""
            if name == "columns":
                return MagicMock(side_effect=lambda n: [MagicMock() for _ in range(n)])
            elif name == "tabs":
                return MagicMock(side_effect=lambda items: [MagicMock() for _ in items])
            elif name in ["button", "form_submit_button"]:
                return MagicMock(return_value=False)
            elif name in ["text_input", "selectbox"]:
                return MagicMock(return_value="")
            elif name == "container":
                mock_ctx = MagicMock()
                mock_ctx.__enter__ = MagicMock(return_value=mock_ctx)
                mock_ctx.__exit__ = MagicMock(return_value=None)
                return MagicMock(return_value=mock_ctx)
            else:
                return MagicMock()

    return UIStreamlitMock()
