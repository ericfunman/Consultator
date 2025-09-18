"""Tests unitaires pour le module consultant_forms"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import streamlit as st

# Import des fonctions à tester
from app.pages_modules.consultant_forms import (
    validate_consultant_form,
    create_consultant,
    update_consultant,
    delete_consultant,
    show_add_consultant_form,
    show_edit_consultant_form,
)

# Import des modèles pour les mocks
from app.database.models import Consultant, Practice


class TestValidateConsultantForm:
    """Tests pour la fonction validate_consultant_form"""

    @patch("streamlit.error")
    def test_validate_form_valid_data(self, mock_error):
        """Test validation avec données valides"""
        result = validate_consultant_form("Jean", "Dupont", "jean@test.com", 1)

        assert result is True
        mock_error.assert_not_called()

    @patch("streamlit.error")
    def test_validate_form_missing_prenom(self, mock_error):
        """Test validation avec prénom manquant"""
        result = validate_consultant_form("", "Dupont", "jean@test.com", 1)

        assert result is False
        mock_error.assert_called_with("❌ Le prénom est obligatoire")

    @patch("streamlit.error")
    def test_validate_form_missing_nom(self, mock_error):
        """Test validation avec nom manquant"""
        result = validate_consultant_form("Jean", "", "jean@test.com", 1)

        assert result is False
        mock_error.assert_called_with("❌ Le nom est obligatoire")

    @patch("streamlit.error")
    def test_validate_form_missing_email(self, mock_error):
        """Test validation avec email manquant"""
        result = validate_consultant_form("Jean", "Dupont", "", 1)

        assert result is False
        mock_error.assert_called_with("❌ L'email est obligatoire")

    @patch("streamlit.error")
    def test_validate_form_invalid_email(self, mock_error):
        """Test validation avec email invalide"""
        result = validate_consultant_form("Jean", "Dupont", "invalid-email", 1)

        assert result is False
        mock_error.assert_called_with("❌ L'email doit être valide")

    @patch("streamlit.error")
    def test_validate_form_missing_practice(self, mock_error):
        """Test validation avec practice manquante"""
        result = validate_consultant_form("Jean", "Dupont", "jean@test.com", None)

        assert result is False
        mock_error.assert_called_with("❌ La practice est obligatoire")

    @patch("streamlit.error")
    def test_validate_form_multiple_errors(self, mock_error):
        """Test validation avec plusieurs erreurs"""
        result = validate_consultant_form("", "", "", None)

        assert result is False
        assert mock_error.call_count == 4  # 4 erreurs attendues


class TestCreateConsultant:
    """Tests pour la fonction create_consultant"""

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    @patch("streamlit.info")
    def test_create_consultant_success(self, mock_info, mock_error, mock_session):
        """Test création réussie d'un consultant"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant existant (aucun trouvé)
        mock_session_instance.query.return_value.filter.return_value.first.return_value = (
            None
        )

        # Mock consultant créé
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock Consultant class
        with patch(
            "app.pages_modules.consultant_forms.Consultant",
            return_value=mock_consultant,
        ):
            data = {
                "prenom": "Jean",
                "nom": "Dupont",
                "email": "jean@test.com",
                "telephone": "0123456789",
                "salaire_actuel": 50000,
                "practice_id": 1,
                "disponibilite": True,
                "notes": "Test notes",
            }

            result = create_consultant(data)

            assert result is True
            mock_session_instance.add.assert_called_once_with(mock_consultant)
            mock_session_instance.commit.assert_called_once()
            mock_info.assert_called_once()

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    def test_create_consultant_duplicate_email(self, mock_error, mock_session):
        """Test création avec email déjà existant"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant existant
        mock_existing = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = (
            mock_existing
        )

        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Test notes",
        }

        result = create_consultant(data)

        assert result is False
        mock_error.assert_called_with("❌ Un consultant avec cet email existe déjà")
        mock_session_instance.add.assert_not_called()
        mock_session_instance.commit.assert_not_called()

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    def test_create_consultant_database_error(self, mock_error, mock_session):
        """Test création avec erreur de base de données"""
        # Mock session qui lève une exception
        mock_session_instance = MagicMock()
        mock_session_instance.commit.side_effect = Exception("Database error")
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant existant (aucun trouvé)
        mock_session_instance.query.return_value.filter.return_value.first.return_value = (
            None
        )

        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Test notes",
        }

        result = create_consultant(data)

        assert result is False
        mock_error.assert_called_with(
            "❌ Erreur lors de la création du consultant: Database error"
        )


class TestUpdateConsultant:
    """Tests pour la fonction update_consultant"""

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    @patch("streamlit.info")
    def test_update_consultant_success(self, mock_info, mock_error, mock_session):
        """Test mise à jour réussie d'un consultant"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant existant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_session_instance.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )

        # Mock email existant pour un autre consultant (aucun trouvé)
        mock_session_instance.query.return_value.filter.return_value.first.side_effect = [
            mock_consultant,
            None,
        ]

        data = {
            "prenom": "Jean-Marie",
            "nom": "Dupont",
            "email": "jean.marie@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 55000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Updated notes",
        }

        result = update_consultant(1, data)

        assert result is True
        mock_session_instance.commit.assert_called_once()
        mock_info.assert_called_once_with("✅ Consultant Jean-Marie Dupont modifié")

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    def test_update_consultant_not_found(self, mock_error, mock_session):
        """Test mise à jour d'un consultant inexistant"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant non trouvé
        mock_session_instance.query.return_value.filter.return_value.first.return_value = (
            None
        )

        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Test notes",
        }

        result = update_consultant(999, data)

        assert result is False
        mock_error.assert_called_with("❌ Consultant introuvable")
        mock_session_instance.commit.assert_not_called()

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    def test_update_consultant_duplicate_email(self, mock_error, mock_session):
        """Test mise à jour avec email déjà utilisé par un autre consultant"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant existant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_session_instance.query.return_value.filter.return_value.first.side_effect = [
            mock_consultant,
            MagicMock(),
        ]

        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "existing@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Test notes",
        }

        result = update_consultant(1, data)

        assert result is False
        mock_error.assert_called_with("❌ Un autre consultant utilise déjà cet email")
        mock_session_instance.commit.assert_not_called()

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    def test_update_consultant_database_error(self, mock_error, mock_session):
        """Test mise à jour avec erreur de base de données"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session_instance.commit.side_effect = Exception("Database error")
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant existant
        mock_consultant = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.side_effect = [
            mock_consultant,
            None,
        ]

        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Test notes",
        }

        result = update_consultant(1, data)

        assert result is False
        mock_error.assert_called_with(
            "❌ Erreur lors de la modification du consultant: Database error"
        )


class TestDeleteConsultant:
    """Tests pour la fonction delete_consultant"""

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    @patch("streamlit.info")
    def test_delete_consultant_success(self, mock_info, mock_error, mock_session):
        """Test suppression réussie d'un consultant"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant existant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_session_instance.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )

        result = delete_consultant(1)

        assert result is True
        mock_session_instance.delete.assert_called_once_with(mock_consultant)
        mock_session_instance.commit.assert_called_once()
        mock_info.assert_called_with("✅ Consultant supprimé de la base de données")

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    def test_delete_consultant_not_found(self, mock_error, mock_session):
        """Test suppression d'un consultant inexistant"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant non trouvé
        mock_session_instance.query.return_value.filter.return_value.first.return_value = (
            None
        )

        result = delete_consultant(999)

        assert result is False
        mock_error.assert_called_with("❌ Consultant introuvable")
        mock_session_instance.delete.assert_not_called()
        mock_session_instance.commit.assert_not_called()

    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    def test_delete_consultant_database_error(self, mock_error, mock_session):
        """Test suppression avec erreur de base de données"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session_instance.commit.side_effect = Exception("Database error")
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant existant
        mock_consultant = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = (
            mock_consultant
        )

        result = delete_consultant(1)

        assert result is False
        mock_error.assert_called_with(
            "❌ Erreur lors de la suppression du consultant: Database error"
        )


class TestShowForms:
    """Tests pour les fonctions d'affichage des formulaires"""

    @patch("app.pages_modules.consultant_forms.imports_ok", False)
    @patch("streamlit.error")
    def test_show_add_form_imports_error(self, mock_error):
        """Test affichage formulaire ajout avec erreur d'imports"""
        show_add_consultant_form()

        mock_error.assert_called_with("❌ Les services de base ne sont pas disponibles")

    @patch("app.pages_modules.consultant_forms.imports_ok", False)
    @patch("streamlit.error")
    def test_show_edit_form_imports_error(self, mock_error):
        """Test affichage formulaire modification avec erreur d'imports"""
        show_edit_consultant_form(1)

        mock_error.assert_called_with("❌ Les services de base ne sont pas disponibles")

    @patch("app.pages_modules.consultant_forms.imports_ok", True)
    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.markdown")
    @patch("streamlit.warning")
    def test_show_add_form_no_practices(
        self, mock_warning, mock_markdown, mock_session
    ):
        """Test affichage formulaire ajout sans practices disponibles"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock practices vides
        mock_session_instance.query.return_value.all.return_value = []

        show_add_consultant_form()

        mock_warning.assert_called_with(
            "⚠️ Aucune practice trouvée. Veuillez créer des practices d'abord."
        )

    @patch("app.pages_modules.consultant_forms.imports_ok", True)
    @patch("app.pages_modules.consultant_forms.get_database_session")
    @patch("streamlit.error")
    def test_show_edit_form_consultant_not_found(self, mock_error, mock_session):
        """Test affichage formulaire modification consultant inexistant"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant non trouvé
        mock_session_instance.query.return_value.options.return_value.filter.return_value.first.return_value = (
            None
        )

        show_edit_consultant_form(999)

        mock_error.assert_called_with("❌ Consultant introuvable")
