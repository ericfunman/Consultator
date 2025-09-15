"""Tests pour le module consultant_languages - Interface utilisateur"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from app.pages_modules.consultant_languages import show_consultant_languages
from tests.fixtures.base_test import BaseUITest


class TestConsultantLanguages(BaseUITest):
    """Tests pour le module de langues consultant"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultant_languages)

    @patch('app.pages_modules.consultant_languages.imports_ok', True)
    @patch('app.pages_modules.consultant_languages.ConsultantService')
    def test_show_consultant_languages_basic(self, mock_service):
        """Test d'affichage basique des langues"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_languages(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_languages.imports_ok', False)
    def test_show_consultant_languages_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        mock_consultant = Mock()
        mock_consultant.id = 1

        try:
            show_consultant_languages(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_show_consultant_languages_no_consultant(self):
        """Test d'affichage sans consultant"""
        try:
            show_consultant_languages(None)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_languages.imports_ok', True)
    @patch('app.pages_modules.consultant_languages.ConsultantService')
    def test_show_consultant_languages_with_data(self, mock_service):
        """Test d'affichage avec données de langues"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock langues
        mock_langues = [
            {
                'id': 1,
                'nom': 'Français',
                'niveau_ecrit': 5,
                'niveau_parle': 5,
                'certification': 'DELF B2',
                'maternelle': True,
                'niveau_ecrit_label': 'Langue maternelle',
                'niveau_parle_label': 'Langue maternelle'
            },
            {
                'id': 2,
                'nom': 'Anglais',
                'niveau_ecrit': 4,
                'niveau_parle': 4,
                'certification': 'TOEIC 950',
                'maternelle': False,
                'niveau_ecrit_label': 'Courant',
                'niveau_parle_label': 'Courant'
            },
            {
                'id': 3,
                'nom': 'Espagnol',
                'niveau_ecrit': 2,
                'niveau_parle': 3,
                'certification': None,
                'maternelle': False,
                'niveau_ecrit_label': 'Intermédiaire',
                'niveau_parle_label': 'Intermédiaire+'
            }
        ]

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_langues.return_value = mock_langues
        mock_service_instance.get_consultant_langues_stats.return_value = {
            'total_langues': 3,
            'langues_maternelles': 1,
            'langues_certifiees': 2,
            'niveau_moyen_ecrit': 3.67,
            'niveau_moyen_parle': 4.0
        }
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_languages(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_languages.imports_ok', True)
    @patch('app.pages_modules.consultant_languages.ConsultantService')
    def test_show_consultant_languages_empty(self, mock_service):
        """Test d'affichage avec langues vides"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service avec liste vide
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_langues.return_value = []
        mock_service_instance.get_consultant_langues_stats.return_value = {
            'total_langues': 0,
            'langues_maternelles': 0,
            'langues_certifiees': 0,
            'niveau_moyen_ecrit': 0.0,
            'niveau_moyen_parle': 0.0
        }
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_languages(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_languages.imports_ok', True)
    @patch('app.pages_modules.consultant_languages.ConsultantService')
    def test_show_consultant_languages_service_error(self, mock_service):
        """Test d'affichage avec erreur de service"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_langues.side_effect = Exception("Service error")
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_languages(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_languages as languages_module

        # Vérifier que les fonctions principales existent
        assert hasattr(languages_module, 'show_consultant_languages')

        # Vérifier que les variables d'import existent
        assert hasattr(languages_module, 'imports_ok')
        assert hasattr(languages_module, 'ConsultantService')

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultant_languages)

        # Vérifier le nombre de paramètres
        sig_languages = inspect.signature(show_consultant_languages)

        # Doit avoir au moins un paramètre (consultant)
        assert len(sig_languages.parameters) >= 1
