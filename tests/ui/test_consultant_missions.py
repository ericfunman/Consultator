"""Tests pour le module consultant_missions - Interface utilisateur"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from app.pages_modules.consultant_missions import show_consultant_missions
from tests.fixtures.base_test import BaseUITest


class TestConsultantMissions(BaseUITest):
    """Tests pour le module de missions consultant"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultant_missions)

    @patch('app.pages_modules.consultant_missions.imports_ok', True)
    @patch('app.pages_modules.consultant_missions.ConsultantService')
    def test_show_consultant_missions_basic(self, mock_service):
        """Test d'affichage basique des missions"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_missions.imports_ok', False)
    def test_show_consultant_missions_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        mock_consultant = Mock()
        mock_consultant.id = 1

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_show_consultant_missions_no_consultant(self):
        """Test d'affichage sans consultant"""
        try:
            show_consultant_missions(None)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_missions.imports_ok', True)
    @patch('app.pages_modules.consultant_missions.ConsultantService')
    def test_show_consultant_missions_with_data(self, mock_service):
        """Test d'affichage avec données de missions"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock missions
        mock_missions = [
            {
                'id': 1,
                'nom': 'Projet Web E-commerce',
                'client_nom': 'Client A',
                'date_debut': '2023-01-01',
                'date_fin': '2023-06-30',
                'statut': 'Terminée',
                'description': 'Développement d\'une plateforme e-commerce',
                'technologies': ['Python', 'Django', 'React'],
                'tarif_journalier': 550.0,
                'duree_jours': 120
            },
            {
                'id': 2,
                'nom': 'API REST Microservices',
                'client_nom': 'Client B',
                'date_debut': '2023-07-01',
                'date_fin': None,
                'statut': 'En cours',
                'description': 'Développement d\'API REST',
                'technologies': ['Python', 'FastAPI', 'Docker'],
                'tarif_journalier': 600.0,
                'duree_jours': None
            }
        ]

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_missions.return_value = mock_missions
        mock_service_instance.get_consultant_missions_stats.return_value = {
            'total_missions': 2,
            'missions_actives': 1,
            'missions_terminees': 1,
            'total_jours': 120,
            'ca_total': 66000.0
        }
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_missions.imports_ok', True)
    @patch('app.pages_modules.consultant_missions.ConsultantService')
    def test_show_consultant_missions_empty(self, mock_service):
        """Test d'affichage avec missions vides"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service avec liste vide
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_missions.return_value = []
        mock_service_instance.get_consultant_missions_stats.return_value = {
            'total_missions': 0,
            'missions_actives': 0,
            'missions_terminees': 0,
            'total_jours': 0,
            'ca_total': 0.0
        }
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_missions.imports_ok', True)
    @patch('app.pages_modules.consultant_missions.ConsultantService')
    def test_show_consultant_missions_service_error(self, mock_service):
        """Test d'affichage avec erreur de service"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_missions.side_effect = Exception("Service error")
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_missions(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_missions as missions_module

        # Vérifier que les fonctions principales existent
        assert hasattr(missions_module, 'show_consultant_missions')

        # Vérifier que les variables d'import existent
        assert hasattr(missions_module, 'imports_ok')
        assert hasattr(missions_module, 'ConsultantService')

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultant_missions)

        # Vérifier le nombre de paramètres
        sig_missions = inspect.signature(show_consultant_missions)

        # Doit avoir au moins un paramètre (consultant)
        assert len(sig_missions.parameters) >= 1
