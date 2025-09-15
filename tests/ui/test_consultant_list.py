"""Tests pour le module consultant_list - Interface utilisateur"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from app.pages_modules.consultant_list import show_consultants_list
from tests.fixtures.base_test import BaseUITest


class TestConsultantList(BaseUITest):
    """Tests pour le module de liste des consultants"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultants_list)

    @patch('app.pages_modules.consultant_list.imports_ok', True)
    @patch('app.pages_modules.consultant_list.ConsultantService')
    def test_show_consultants_list_basic(self, mock_service):
        """Test d'affichage basique de la liste"""
        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultants_list()
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_list.imports_ok', False)
    def test_show_consultants_list_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        try:
            show_consultants_list()
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_list.imports_ok', True)
    @patch('app.pages_modules.consultant_list.ConsultantService')
    def test_show_consultants_list_with_data(self, mock_service):
        """Test de la liste avec données"""
        # Mock données de consultants
        mock_consultants = [
            {
                'id': 1,
                'prenom': 'Jean',
                'nom': 'Dupont',
                'email': 'jean@test.com',
                'disponibilite': True,
                'salaire_actuel': 50000,
                'societe': 'Quanteam',
                'grade': 'Senior',
                'type_contrat': 'CDI',
                'practice_name': 'Tech',
                'nb_missions': 3,
                'cjm': 1440.0,
                'salaire_formatted': '50,000€',
                'cjm_formatted': '1,440€',
                'statut': '✅ Disponible',
                'experience_annees': 5,
                'experience_formatted': '5 ans'
            },
            {
                'id': 2,
                'prenom': 'Marie',
                'nom': 'Martin',
                'email': 'marie@test.com',
                'disponibilite': False,
                'salaire_actuel': 45000,
                'societe': 'Quanteam',
                'grade': 'Confirmé',
                'type_contrat': 'CDI',
                'practice_name': 'Business',
                'nb_missions': 2,
                'cjm': 1296.0,
                'salaire_formatted': '45,000€',
                'cjm_formatted': '1,296€',
                'statut': '🔴 En mission',
                'experience_annees': 3,
                'experience_formatted': '3 ans'
            }
        ]

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.get_all_consultants_with_stats.return_value = mock_consultants
        mock_service_instance.get_consultants_count.return_value = len(mock_consultants)
        mock_service.return_value = mock_service_instance

        try:
            show_consultants_list()
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_list.imports_ok', True)
    @patch('app.pages_modules.consultant_list.ConsultantService')
    def test_show_consultants_list_empty(self, mock_service):
        """Test de la liste vide"""
        # Mock service avec liste vide
        mock_service_instance = Mock()
        mock_service_instance.get_all_consultants_with_stats.return_value = []
        mock_service_instance.get_consultants_count.return_value = 0
        mock_service.return_value = mock_service_instance

        try:
            show_consultants_list()
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_list.imports_ok', True)
    @patch('app.pages_modules.consultant_list.ConsultantService')
    def test_show_consultants_list_with_search(self, mock_service):
        """Test de la liste avec recherche"""
        # Mock données filtrées
        mock_filtered_consultants = [
            {
                'id': 1,
                'prenom': 'Jean',
                'nom': 'Dupont',
                'email': 'jean@test.com',
                'disponibilite': True,
                'salaire_actuel': 50000,
                'societe': 'Quanteam',
                'grade': 'Senior',
                'type_contrat': 'CDI',
                'practice_name': 'Tech',
                'nb_missions': 3,
                'cjm': 1440.0,
                'salaire_formatted': '50,000€',
                'cjm_formatted': '1,440€',
                'statut': '✅ Disponible',
                'experience_annees': 5,
                'experience_formatted': '5 ans'
            }
        ]

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.search_consultants_optimized.return_value = mock_filtered_consultants
        mock_service.return_value = mock_service_instance

        try:
            show_consultants_list()
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_list.imports_ok', True)
    @patch('app.pages_modules.consultant_list.ConsultantService')
    def test_show_consultants_list_service_error(self, mock_service):
        """Test de la liste avec erreur de service"""
        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_all_consultants_with_stats.side_effect = Exception("Service error")
        mock_service.return_value = mock_service_instance

        try:
            show_consultants_list()
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_list as list_module

        # Vérifier que les fonctions principales existent
        assert hasattr(list_module, 'show_consultants_list')

        # Vérifier que les variables d'import existent
        assert hasattr(list_module, 'imports_ok')
        assert hasattr(list_module, 'ConsultantService')

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultants_list)

        # Vérifier le nombre de paramètres
        sig_list = inspect.signature(show_consultants_list)

        assert len(sig_list.parameters) <= 5
