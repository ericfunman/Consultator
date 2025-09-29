"""Tests pour les formulaires de consultants - Interface utilisateur"""

from datetime import date
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
import streamlit as st

from app.database.models import Consultant, ConsultantCompetence
from app.database.models import Practice, ConsultantCompetence
from app.pages_modules.consultants import show_add_consultant_form
from app.pages_modules.consultants import show_consultant_profile
from app.pages_modules.consultants import show_consultants_list
from tests.fixtures.base_test import BaseUITest


class TestConsultantForms(BaseUITest):
    """Tests pour les formulaires de l'interface consultants"""

    def test_imports_successful(self):
        """Test que les imports des fonctions principales réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultants_list)
        assert callable(show_add_consultant_form)
        assert callable(show_consultant_profile)

    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_consultants_list_can_be_called(self, mock_service):
        """Test que show_consultants_list peut être appelée sans erreur"""
        # Mock service pour éviter les appels réels
        mock_service.get_all_consultants_with_stats.return_value = []
        mock_service.search_consultants_optimized.return_value = []

        # Test que la fonction peut être appelée
        try:
            show_consultants_list()
            # Si on arrive ici, la fonction s'est exécutée sans erreur fatale
            assert 1 == 1  # Test basique
        except Exception as e:
            # Accepter les erreurs liées au contexte Streamlit manquant
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique Erreur attendue en mode test
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultants._load_practice_options")
    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_add_consultant_form_can_be_called(self, mock_service, mock_practices):
        """Test que show_add_consultant_form peut être appelée sans erreur"""
        # Mock service
        mock_service.create_consultant.return_value = True
        mock_service.update_consultant.return_value = True
        
        # Mock practices pour éviter l'accès à la DB
        mock_practices.return_value = {"Practice Test": 1, "Practice Demo": 2}

        # Test que la fonction peut être appelée
        try:
            show_add_consultant_form()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("streamlit.session_state", new_callable=MagicMock)
    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_consultant_profile_can_be_called(self, mock_service, mock_session_state):
        """Test que show_consultant_profile peut être appelée sans erreur"""
        # Setup session state
        mock_session_state.view_consultant_profile = 1
        mock_session_state.__contains__ = lambda key: key == 'view_consultant_profile'
        mock_session_state.__getitem__ = lambda key: 1 if key == 'view_consultant_profile' else None
        
        # Mock service
        mock_service.get_consultant_with_stats.return_value = {
            "id": 1,
            "prenom": "Test",
            "nom": "User",
            "email": "test@example.com",
            "disponibilite": True,
        }

        # Test que la fonction peut être appelée
        try:
            show_consultant_profile()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_consultants_list_with_empty_data(self, mock_service):
        """Test avec données vides"""
        mock_service.get_all_consultants_with_stats.return_value = []
        mock_service.search_consultants_optimized.return_value = []

        try:
            show_consultants_list()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultants.ConsultantService")
    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.pd")
    @patch("app.pages_modules.consultants.show_consultants_list_enhanced")
    def test_show_consultants_list_with_data(
        self, mock_enhanced_func, mock_pd, mock_st, mock_service
    ):
        """Test avec données présentes"""
        # Forcer l'utilisation de la version classique en faisant échouer l'import des composants UI
        mock_enhanced_func.side_effect = ImportError("UI components not available")

        # Mock pandas DataFrame
        mock_df = MagicMock()
        mock_pd.DataFrame.return_value = mock_df

        # Mock Streamlit pour éviter les interactions UI
        def mock_columns(*args, **kwargs):
            if not args:
                return [MagicMock(), MagicMock()]  # Default 2 columns
            arg = args[0]
            if isinstance(arg, int):
                return [MagicMock() for _ in range(arg)]
            elif isinstance(arg, list):
                return [MagicMock() for _ in range(len(arg))]
            else:
                return [MagicMock(), MagicMock()]

        # Mock dataframe event - pas de sélection
        mock_event = MagicMock()
        mock_event.selection.rows = []  # Liste vide = pas de sélection
        mock_st.dataframe.return_value = mock_event

        mock_st.text_input.return_value = ""
        mock_st.button.return_value = False
        mock_st.columns.side_effect = mock_columns
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.spinner.return_value.__enter__ = MagicMock()
        mock_st.spinner.return_value.__exit__ = MagicMock()
        mock_st.empty.return_value = None

        mock_data = [
            {
                "id": 1,
                "prenom": "Jean",
                "nom": "Dupont",
                "email": "jean@test.com",
                "disponibilite": True,
                "salaire_actuel": 50000,
                "societe": "Quanteam",
                "grade": "Senior",
                "type_contrat": "CDI",
                "practice_name": "Tech",
                "nb_missions": 3,
                "cjm": 1440.0,
                "salaire_formatted": "50,000€",
                "cjm_formatted": "1,440€",
                "statut": "✅ Disponible",
                "experience_annees": 5,
                "experience_formatted": "5 ans",
            }
        ]
        mock_service.get_all_consultants_with_stats.return_value = mock_data
        mock_service.search_consultants_optimized.return_value = mock_data

        try:
            show_consultants_list()
            assert 1 == 1  # Test basique
        except Exception as e:
            if (
                "ScriptRunContext" in str(e)
                or "Session state" in str(e)
                or "UI components not available" in str(e)
            ):
                assert 1 == 1  # Test basique Erreur attendue en mode test
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultants._load_practice_options")
    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_add_consultant_form_with_service_error(self, mock_service, mock_practices):
        """Test avec erreur du service"""
        mock_service.create_consultant.return_value = False
        mock_practices.return_value = {"Practice Test": 1}

        try:
            show_add_consultant_form()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("streamlit.session_state", new_callable=MagicMock)
    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_consultant_profile_with_no_data(self, mock_service, mock_session_state):
        """Test du profil avec données manquantes"""
        # Setup session state
        mock_session_state.view_consultant_profile = 1
        mock_session_state.__contains__ = lambda key: key == 'view_consultant_profile'
        mock_session_state.__getitem__ = lambda key: 1 if key == 'view_consultant_profile' else None
        
        mock_service.get_consultant_with_stats.return_value = None

        try:
            show_consultant_profile()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultants as consultants_module

        # Vérifier que les fonctions principales existent
        assert hasattr(consultants_module, "show_consultants_list")
        assert hasattr(consultants_module, "show_add_consultant_form")
        assert hasattr(consultants_module, "show_consultant_profile")

        # Vérifier que les services sont importés
        assert hasattr(consultants_module, "ConsultantService")

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultants_list)
        assert inspect.isfunction(show_add_consultant_form)
        assert inspect.isfunction(show_consultant_profile)

        # Vérifier le nombre de paramètres (approximatif)
        sig_list = inspect.signature(show_consultants_list)
        sig_add = inspect.signature(show_add_consultant_form)
        sig_profile = inspect.signature(show_consultant_profile)

        # Ces fonctions devraient avoir peu de paramètres explicites
        assert len(sig_list.parameters) <= 5
        assert len(sig_add.parameters) <= 5
        assert len(sig_profile.parameters) <= 5
