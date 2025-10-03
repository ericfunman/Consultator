"""
Tests pour le module consultant_forms.py
Couverture des fonctions d'ajout, modification et suppression de consultants
"""

from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest


class TestConsultantForms:
    """Tests pour les formulaires de gestion des consultants"""

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_show_add_consultant_form_success(self, mock_session, mock_st):
        """Test affichage formulaire ajout consultant avec succès"""
        # Mock session et practices
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock practice
        mock_practice = MagicMock()
        mock_practice.id = 1
        mock_practice.nom = "Test Practice"
        mock_session_instance.query.return_value.all.return_value = [mock_practice]

        # Mock form submission
        mock_st.form.return_value.__enter__.return_value = None
        mock_st.form.return_value.__exit__.return_value = None
        mock_st.form_submit_button.return_value = True

        # Mock form inputs
        mock_st.text_input.side_effect = [
            "Jean",
            "Dupont",
            "jean@test.com",
            "0123456789",
        ]
        mock_st.number_input.return_value = 50000
        mock_st.selectbox.return_value = 1
        mock_st.checkbox.return_value = True
        mock_st.text_area.return_value = "Test notes"

        from app.pages_modules.consultant_forms import show_add_consultant_form

        show_add_consultant_form()

        # Vérifier que les éléments UI sont appelés
        assert mock_st.markdown.called
        assert mock_st.form.called

    @patch("app.pages_modules.consultant_forms.st")
    def test_show_add_consultant_form_no_practices(self, mock_st):
        """Test affichage formulaire quand aucune practice"""
        with patch("app.pages_modules.consultant_forms.get_database_session") as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session_instance.query.return_value.all.return_value = []

            from app.pages_modules.consultant_forms import (
                show_add_consultant_form,
            )

            show_add_consultant_form()

            mock_st.warning.assert_called_with("⚠️ Aucune practice trouvée. Veuillez créer des practices d'abord.")

    def test_validate_consultant_form_valid(self):
        """Test validation formulaire avec données valides"""
        from app.pages_modules.consultant_forms import validate_consultant_form

        with patch("app.pages_modules.consultant_forms.st"):
            result = validate_consultant_form("Jean", "Dupont", "jean@test.com", 1)

            assert result is True

    def test_validate_consultant_form_missing_prenom(self):
        """Test validation formulaire prénom manquant"""
        from app.pages_modules.consultant_forms import validate_consultant_form

        with patch("app.pages_modules.consultant_forms.st") as mock_st:
            result = validate_consultant_form("", "Dupont", "jean@test.com", 1)

            assert result is False
            mock_st.error.assert_called_with("❌ Le prénom est obligatoire")

    def test_validate_consultant_form_missing_nom(self):
        """Test validation formulaire nom manquant"""
        from app.pages_modules.consultant_forms import validate_consultant_form

        with patch("app.pages_modules.consultant_forms.st") as mock_st:
            result = validate_consultant_form("Jean", "", "jean@test.com", 1)

            assert result is False
            mock_st.error.assert_called_with("❌ Le nom est obligatoire")

    def test_validate_consultant_form_invalid_email(self):
        """Test validation formulaire email invalide"""
        from app.pages_modules.consultant_forms import validate_consultant_form

        with patch("app.pages_modules.consultant_forms.st") as mock_st:
            result = validate_consultant_form("Jean", "Dupont", "invalid-email", 1)

            assert result is False
            mock_st.error.assert_called_with("❌ L'email doit être valide")

    def test_validate_consultant_form_missing_practice(self):
        """Test validation formulaire practice manquante"""
        from app.pages_modules.consultant_forms import validate_consultant_form

        with patch("app.pages_modules.consultant_forms.st") as mock_st:
            result = validate_consultant_form("Jean", "Dupont", "jean@test.com", None)

            assert result is False
            mock_st.error.assert_called_with("❌ La practice est obligatoire")

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_create_consultant_success(self, mock_session, mock_st):
        """Test création consultant avec succès"""
        from app.pages_modules.consultant_forms import create_consultant

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock existing check (no existing consultant)
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        # Mock consultant creation
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        test_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Test notes",
        }

        result = create_consultant(test_data)

        assert result is True
        mock_session_instance.add.assert_called()
        mock_session_instance.commit.assert_called()

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_create_consultant_email_exists(self, mock_session, mock_st):
        """Test création consultant email déjà existant"""
        from app.pages_modules.consultant_forms import create_consultant

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock existing consultant with same email
        mock_existing = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_existing

        test_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Test notes",
        }

        result = create_consultant(test_data)

        assert result is False
        mock_st.error.assert_called_with("❌ Un consultant avec cet email existe déjà")

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_show_edit_consultant_form_success(self, mock_session, mock_st):
        """Test affichage formulaire modification consultant"""
        from app.pages_modules.consultant_forms import (
            show_edit_consultant_form,
        )

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.telephone = "0123456789"
        mock_consultant.salaire_actuel = 50000
        mock_consultant.practice_id = 1
        mock_consultant.disponibilite = True
        mock_consultant.notes = "Test notes"

        # Mock practice
        mock_practice = MagicMock()
        mock_practice.id = 1
        mock_practice.nom = "Test Practice"

        # Setup query chain
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_consultant

        # Second query for practices
        mock_session_instance.query.return_value.all.return_value = [mock_practice]

        # Mock form
        mock_st.form.return_value.__enter__.return_value = None
        mock_st.form.return_value.__exit__.return_value = None
        mock_st.form_submit_button.return_value = False  # No submission

        show_edit_consultant_form(1)

        assert mock_st.markdown.called

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_show_edit_consultant_form_not_found(self, mock_session, mock_st):
        """Test affichage formulaire consultant introuvable"""
        from app.pages_modules.consultant_forms import (
            show_edit_consultant_form,
        )

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query returns None
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        show_edit_consultant_form(999)

        mock_st.error.assert_called_with("❌ Consultant introuvable")

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_update_consultant_success(self, mock_session, mock_st):
        """Test mise à jour consultant avec succès"""
        from app.pages_modules.consultant_forms import update_consultant

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Setup query
        mock_query = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_consultant

        # Mock email check (no conflict)
        mock_session_instance.query.return_value.filter.return_value.first.side_effect = [
            mock_consultant,
            None,
        ]

        test_data = {
            "prenom": "Jean-Marie",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 55000,
            "practice_id": 1,
            "disponibilite": True,
            "notes": "Updated notes",
        }

        result = update_consultant(1, test_data)

        assert result is True
        mock_session_instance.commit.assert_called()

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_update_consultant_not_found(self, mock_session, mock_st):
        """Test mise à jour consultant introuvable"""
        from app.pages_modules.consultant_forms import update_consultant

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query returns None
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        test_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "practice_id": 1,
        }

        result = update_consultant(999, test_data)

        assert result is False
        mock_st.error.assert_called_with("❌ Consultant introuvable")

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_delete_consultant_success(self, mock_session, mock_st):
        """Test suppression consultant avec succès"""
        from app.pages_modules.consultant_forms import delete_consultant

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Setup query
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_consultant

        result = delete_consultant(1)

        assert result is True
        mock_session_instance.delete.assert_called_with(mock_consultant)
        mock_session_instance.commit.assert_called()

    @patch("app.pages_modules.consultant_forms.st")
    @patch("app.pages_modules.consultant_forms.get_database_session")
    def test_delete_consultant_not_found(self, mock_session, mock_st):
        """Test suppression consultant introuvable"""
        from app.pages_modules.consultant_forms import delete_consultant

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query returns None
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        result = delete_consultant(999)

        assert result is False
        mock_st.error.assert_called_with("❌ Consultant introuvable")
