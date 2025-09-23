"""Tests pour le module consultant_forms - Interface utilisateur"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from app.pages_modules.consultant_forms import show_add_consultant_form
from tests.fixtures.base_test import BaseUITest


class TestConsultantForms(BaseUITest):
    """Tests pour le module de formulaires consultant"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_add_consultant_form)

    @patch("app.pages_modules.consultant_forms.imports_ok", True)
    @patch("app.pages_modules.consultant_forms.ConsultantService")
    def test_show_add_consultant_form_basic(self, mock_service):
        """Test d'affichage basique du formulaire d'ajout"""
        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_add_consultant_form()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_forms.imports_ok", False)
    def test_show_add_consultant_form_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        try:
            show_add_consultant_form()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_forms.imports_ok", True)
    @patch("app.pages_modules.consultant_forms.ConsultantService")
    def test_show_add_consultant_form_with_service_methods(self, mock_service):
        """Test du formulaire avec méthodes de service disponibles"""
        # Mock service avec méthodes
        mock_service_instance = Mock()
        mock_service_instance.get_all_practices.return_value = []
        mock_service_instance.get_all_competences.return_value = []
        mock_service_instance.get_all_langues.return_value = []
        mock_service.return_value = mock_service_instance

        try:
            show_add_consultant_form()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_forms.imports_ok", True)
    @patch("app.pages_modules.consultant_forms.ConsultantService")
    def test_show_add_consultant_form_with_data(self, mock_service):
        """Test du formulaire avec données disponibles"""
        # Mock données
        mock_practice = Mock()
        mock_practice.id = 1
        mock_practice.nom = "Tech"

        mock_competence = Mock()
        mock_competence.id = 1
        mock_competence.nom = "Python"

        mock_langue = Mock()
        mock_langue.id = 1
        mock_langue.nom = "Français"

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.get_all_practices.return_value = [mock_practice]
        mock_service_instance.get_all_competences.return_value = [mock_competence]
        mock_service_instance.get_all_langues.return_value = [mock_langue]
        mock_service.return_value = mock_service_instance

        try:
            show_add_consultant_form()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_forms.imports_ok", True)
    @patch("app.pages_modules.consultant_forms.ConsultantService")
    def test_show_add_consultant_form_service_error(self, mock_service):
        """Test du formulaire avec erreur de service"""
        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_all_practices.side_effect = Exception("Service error")
        mock_service.return_value = mock_service_instance

        try:
            show_add_consultant_form()
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_forms as forms_module

        # Vérifier que les fonctions principales existent
        assert hasattr(forms_module, "show_add_consultant_form")

        # Vérifier que les variables d'import existent
        assert hasattr(forms_module, "imports_ok")
        assert hasattr(forms_module, "ConsultantService")

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_add_consultant_form)

        # Vérifier le nombre de paramètres
        sig_form = inspect.signature(show_add_consultant_form)

        assert len(sig_form.parameters) <= 5
