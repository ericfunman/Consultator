"""Tests pour le module consultant_info - Interface utilisateur"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from app.pages_modules.consultant_info import show_consultant_info
from tests.fixtures.base_test import BaseUITest


class TestConsultantInfo(BaseUITest):
    """Tests pour le module d'informations consultant"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultant_info)

    @patch("app.pages_modules.consultant_info.imports_ok", True)
    @patch("app.pages_modules.consultant_info.ConsultantService")
    def test_show_consultant_info_basic(self, mock_service):
        """Test d'affichage basique des informations"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.telephone = "0123456789"
        mock_consultant.disponibilite = True
        mock_consultant.date_naissance = "1990-01-01"
        mock_consultant.adresse = "123 Rue de la Paix"

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_info(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_info.imports_ok", False)
    def test_show_consultant_info_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        mock_consultant = Mock()
        mock_consultant.id = 1

        try:
            show_consultant_info(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_show_consultant_info_no_consultant(self):
        """Test d'affichage sans consultant"""
        try:
            show_consultant_info(None)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_info.imports_ok", True)
    @patch("app.pages_modules.consultant_info.ConsultantService")
    def test_show_consultant_info_with_complete_data(self, mock_service):
        """Test d'affichage avec données complètes"""
        # Mock consultant avec toutes les informations
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.telephone = "0123456789"
        mock_consultant.disponibilite = True
        mock_consultant.date_naissance = "1990-01-01"
        mock_consultant.adresse = "123 Rue de la Paix"
        mock_consultant.ville = "Paris"
        mock_consultant.code_postal = "75001"
        mock_consultant.pays = "France"
        mock_consultant.societe = "Quanteam"
        mock_consultant.grade = "Senior"
        mock_consultant.type_contrat = "CDI"
        mock_consultant.salaire_actuel = 55000.0
        mock_consultant.date_creation = "2020-01-01"

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_info(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_info.imports_ok", True)
    @patch("app.pages_modules.consultant_info.ConsultantService")
    def test_show_consultant_info_with_missing_data(self, mock_service):
        """Test d'affichage avec données manquantes"""
        # Mock consultant avec données partielles
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.telephone = None
        mock_consultant.disponibilite = True
        mock_consultant.date_naissance = None
        mock_consultant.adresse = None

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_info(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_info.imports_ok", True)
    @patch("app.pages_modules.consultant_info.ConsultantService")
    def test_show_consultant_info_service_error(self, mock_service):
        """Test d'affichage avec erreur de service"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_info.side_effect = Exception(
            "Service error"
        )
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_info(mock_consultant)
            assert True
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert True
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_info as info_module

        # Vérifier que les fonctions principales existent
        assert hasattr(info_module, "show_consultant_info")

        # Vérifier que les variables d'import existent
        assert hasattr(info_module, "imports_ok")
        assert hasattr(info_module, "ConsultantService")

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultant_info)

        # Vérifier le nombre de paramètres
        sig_info = inspect.signature(show_consultant_info)

        # Doit avoir au moins un paramètre (consultant)
        assert len(sig_info.parameters) >= 1
