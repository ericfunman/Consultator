"""
Tests unitaires pour le module consultant_info
Couvre les fonctions de validation et mise à jour des informations
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.pages_modules.consultant_info import update_consultant_info
from app.pages_modules.consultant_info import validate_info_form


class TestConsultantInfoValidation:
    """Tests pour les fonctions de validation des informations consultant"""

    @patch('app.pages_modules.consultant_info.st')
    def test_validate_info_form_valid_data(self, mock_st):
        """Test de validation avec des données valides"""
        result = validate_info_form("John", "Doe", "john.doe@example.com")

        assert result is True
        # Vérifier qu'aucune erreur n'a été affichée
        mock_st.error.assert_not_called()

    @patch('app.pages_modules.consultant_info.st')
    def test_validate_info_form_missing_prenom(self, mock_st):
        """Test de validation avec prénom manquant"""
        result = validate_info_form("", "Doe", "john.doe@example.com")

        assert result is False
        mock_st.error.assert_called_with("❌ Le prénom est obligatoire")

    @patch('app.pages_modules.consultant_info.st')
    def test_validate_info_form_missing_nom(self, mock_st):
        """Test de validation avec nom manquant"""
        result = validate_info_form("John", "", "john.doe@example.com")

        assert result is False
        mock_st.error.assert_called_with("❌ Le nom est obligatoire")

    @patch('app.pages_modules.consultant_info.st')
    def test_validate_info_form_missing_email(self, mock_st):
        """Test de validation avec email manquant"""
        result = validate_info_form("John", "Doe", "")

        assert result is False
        mock_st.error.assert_called_with("❌ L'email est obligatoire")

    @patch('app.pages_modules.consultant_info.st')
    def test_validate_info_form_invalid_email(self, mock_st):
        """Test de validation avec email invalide"""
        result = validate_info_form("John", "Doe", "invalid-email")

        assert result is False
        mock_st.error.assert_called_with("❌ L'email doit être valide")

    @patch('app.pages_modules.consultant_info.st')
    def test_validate_info_form_multiple_errors(self, mock_st):
        """Test de validation avec plusieurs erreurs"""
        result = validate_info_form("", "", "invalid-email")

        assert result is False
        # Vérifier que toutes les erreurs ont été affichées
        assert mock_st.error.call_count == 3
        mock_st.error.assert_any_call("❌ Le prénom est obligatoire")
        mock_st.error.assert_any_call("❌ Le nom est obligatoire")
        mock_st.error.assert_any_call("❌ L'email doit être valide")


class TestConsultantInfoUpdate:
    """Tests pour la mise à jour des informations consultant"""

    @patch('app.pages_modules.consultant_info.st')
    @patch('app.pages_modules.consultant_info.get_database_session')
    def test_update_consultant_info_success(self, mock_get_session, mock_st):
        """Test de mise à jour réussie"""
        # Mock de la session et du consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "John"
        mock_consultant.nom = "Doe"
        mock_consultant.email = "john.doe@example.com"
        mock_consultant.salaire_actuel = 50000

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_consultant
        # Pas de conflit d'email
        mock_session.query.return_value.filter.return_value.first.side_effect = [mock_consultant, None]
        mock_get_session.return_value.__enter__.return_value = mock_session

        data = {
            "prenom": "Jane",
            "nom": "Smith",
            "email": "jane.smith@example.com",
            "telephone": "0123456789",
            "salaire_actuel": 60000,
            "disponibilite": True,
            "notes": "Test notes",
            "commentaire": "Augmentation"
        }

        result = update_consultant_info(1, data)

        assert result is True
        # Vérifier que les informations ont été mises à jour
        assert mock_consultant.prenom == "Jane"
        assert mock_consultant.nom == "Smith"
        assert mock_consultant.email == "jane.smith@example.com"
        assert mock_consultant.telephone == "0123456789"
        assert mock_consultant.salaire_actuel == 60000
        assert mock_consultant.disponibilite is True
        assert mock_consultant.notes == "Test notes"

        mock_session.commit.assert_called_once()
        mock_st.info.assert_called_with("✅ Informations du consultant mises à jour")

    @patch('app.pages_modules.consultant_info.st')
    @patch('app.pages_modules.consultant_info.get_database_session')
    def test_update_consultant_info_consultant_not_found(self, mock_get_session, mock_st):
        """Test de mise à jour avec consultant introuvable"""
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_get_session.return_value.__enter__.return_value = mock_session

        data = {"prenom": "John", "nom": "Doe", "email": "john@example.com"}
        result = update_consultant_info(999, data)

        assert result is False
        mock_st.error.assert_called_with("❌ Consultant introuvable")

    @patch('app.pages_modules.consultant_info.st')
    @patch('app.pages_modules.consultant_info.get_database_session')
    def test_update_consultant_info_email_conflict(self, mock_get_session, mock_st):
        """Test de mise à jour avec conflit d'email"""
        # Mock consultant existant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock consultant avec email conflictuel
        mock_existing = MagicMock()
        mock_existing.id = 2

        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.side_effect = [mock_consultant, mock_existing]
        mock_get_session.return_value.__enter__.return_value = mock_session

        data = {"prenom": "John", "nom": "Doe", "email": "existing@example.com"}
        result = update_consultant_info(1, data)

        assert result is False
        mock_st.error.assert_called_with("❌ Cet email est déjà utilisé par un autre consultant")

    @patch('app.pages_modules.consultant_info.st')
    @patch('app.pages_modules.consultant_info.get_database_session')
    def test_update_consultant_info_salary_change_with_history(self, mock_get_session, mock_st):
        """Test de mise à jour avec changement de salaire et historique"""
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.salaire_actuel = 50000

        mock_session = MagicMock()
        # Configurer les mocks pour les différents appels query
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query

        # Premier appel: récupérer le consultant
        mock_filter1 = MagicMock()
        mock_query.filter.return_value = mock_filter1
        mock_filter1.first.return_value = mock_consultant

        # Mock pour vérifier l'unicité de l'email (pas de conflit)
        # On utilise side_effect pour gérer les appels multiples
        mock_filter1.first.side_effect = [mock_consultant, None]

        mock_get_session.return_value.__enter__.return_value = mock_session

        data = {
            "prenom": "John",
            "nom": "Doe",
            "email": "john@example.com",
            "telephone": "0123456789",
            "salaire_actuel": 60000,
            "disponibilite": True,
            "notes": "Test notes",
            "commentaire": "Augmentation méritée"
        }

        result = update_consultant_info(1, data)

        assert result is True
        # Vérifier que session.add a été appelé pour l'historique de salaire
        mock_session.add.assert_called_once()

    @patch('app.pages_modules.consultant_info.st')
    @patch('app.pages_modules.consultant_info.get_database_session')
    def test_update_consultant_info_database_error(self, mock_get_session, mock_st):
        """Test de mise à jour avec erreur de base de données"""
        mock_session = MagicMock()
        mock_session.query.side_effect = Exception("Database connection failed")
        mock_get_session.return_value.__enter__.return_value = mock_session

        data = {"prenom": "John", "nom": "Doe", "email": "john@example.com"}
        result = update_consultant_info(1, data)

        assert result is False
        mock_st.error.assert_called_once()
        error_message = mock_st.error.call_args[0][0]
        assert "Erreur lors de la mise à jour" in error_message
