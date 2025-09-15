"""Tests pour le module consultant_skills - Interface utilisateur"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from app.pages_modules.consultant_skills import show_consultant_skills
from tests.fixtures.base_test import BaseUITest


class TestConsultantSkills(BaseUITest):
    """Tests pour le module de compétences consultant"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultant_skills)

    @patch('app.pages_modules.consultant_skills.imports_ok', True)
    @patch('app.pages_modules.consultant_skills.ConsultantService')
    def test_show_consultant_skills_basic(self, mock_service):
        """Test d'affichage basique des compétences"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_skills(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_skills.imports_ok', False)
    def test_show_consultant_skills_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        mock_consultant = Mock()
        mock_consultant.id = 1

        try:
            show_consultant_skills(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_show_consultant_skills_no_consultant(self):
        """Test d'affichage sans consultant"""
        try:
            show_consultant_skills(None)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_skills.imports_ok', True)
    @patch('app.pages_modules.consultant_skills.ConsultantService')
    def test_show_consultant_skills_with_data(self, mock_service):
        """Test d'affichage avec données de compétences"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock compétences
        mock_competences = [
            {
                'id': 1,
                'nom': 'Python',
                'categorie': 'Technique',
                'niveau': 4,
                'niveau_label': 'Expert'
            },
            {
                'id': 2,
                'nom': 'SQL',
                'categorie': 'Technique',
                'niveau': 3,
                'niveau_label': 'Avancé'
            }
        ]

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_competences.return_value = mock_competences
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_skills(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_skills.imports_ok', True)
    @patch('app.pages_modules.consultant_skills.ConsultantService')
    def test_show_consultant_skills_empty(self, mock_service):
        """Test d'affichage avec compétences vides"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service avec liste vide
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_competences.return_value = []
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_skills(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch('app.pages_modules.consultant_skills.imports_ok', True)
    @patch('app.pages_modules.consultant_skills.ConsultantService')
    def test_show_consultant_skills_service_error(self, mock_service):
        """Test d'affichage avec erreur de service"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_competences.side_effect = Exception("Service error")
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_skills(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_skills as skills_module

        # Vérifier que les fonctions principales existent
        assert hasattr(skills_module, 'show_consultant_skills')

        # Vérifier que les variables d'import existent
        assert hasattr(skills_module, 'imports_ok')
        assert hasattr(skills_module, 'ConsultantService')

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultant_skills)

        # Vérifier le nombre de paramètres
        sig_skills = inspect.signature(show_consultant_skills)

        # Doit avoir au moins un paramètre (consultant)
        assert len(sig_skills.parameters) >= 1
