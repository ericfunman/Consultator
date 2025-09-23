"""
Tests pour le module consultant_info.py
Couverture des fonctions de gestion des informations personnelles du consultant
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class TestConsultantInfo:
    """Tests pour les fonctions de gestion des informations du consultant"""

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.imports_ok", True)
    def test_show_consultant_info_success(self, mock_session, mock_st):
        """Test affichage informations consultant avec succès"""
        from app.pages_modules.consultant_info import show_consultant_info

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean.dupont@email.com"
        mock_consultant.telephone = "0123456789"
        mock_consultant.disponibilite = True
        mock_consultant.salaire_actuel = 50000
        mock_consultant.notes = "Notes test"
        mock_consultant.date_creation = date.today()

        # Mock practice
        mock_practice = MagicMock()
        mock_practice.nom = "Data Science"
        mock_consultant.practice = mock_practice

        # Mock session et données
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock salary history query
        mock_salary_query = MagicMock()
        mock_session_instance.query.return_value = mock_salary_query
        mock_salary_query.filter.return_value = mock_salary_query
        mock_salary_query.order_by.return_value = mock_salary_query
        mock_salary_query.limit.return_value = mock_salary_query
        mock_salary_query.all.return_value = []

        # Mock UI elements
        mock_st.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
        mock_st.button.return_value = False  # No button clicks

        show_consultant_info(mock_consultant)

        # Vérifier que les éléments principaux sont affichés
        assert mock_st.markdown.called
        assert mock_st.columns.called

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.imports_ok", True)
    def test_show_consultant_info_no_consultant(self, mock_st):
        """Test affichage informations sans consultant"""
        from app.pages_modules.consultant_info import show_consultant_info

        show_consultant_info(None)

        # Vérifier qu'une erreur est affichée
        mock_st.error.assert_called_with("❌ Consultant non fourni")

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.imports_ok", False)
    def test_show_consultant_info_imports_failed(self, mock_st):
        """Test affichage informations avec imports échoués"""
        from app.pages_modules.consultant_info import show_consultant_info

        mock_consultant = MagicMock()
        show_consultant_info(mock_consultant)

        # Vérifier qu'une erreur est affichée
        mock_st.error.assert_called_with("❌ Les services de base ne sont pas disponibles")

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    def test_show_salary_history_success(self, mock_session, mock_st):
        """Test affichage historique salarial avec succès"""
        from app.pages_modules.consultant_info import show_salary_history

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock salary records
        mock_salary1 = MagicMock()
        mock_salary1.date_debut = date.today()
        mock_salary1.salaire = 45000
        mock_salary1.commentaire = "Augmentation annuelle"

        mock_salary2 = MagicMock()
        mock_salary2.date_debut = date.today() - relativedelta(months=12)
        mock_salary2.salaire = 42000
        mock_salary2.commentaire = "Embauche"

        # Setup query chain
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [mock_salary1, mock_salary2]

        show_salary_history(1)

        # Vérifier que le markdown est appelé
        assert mock_st.markdown.called

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    def test_show_salary_history_empty(self, mock_session, mock_st):
        """Test affichage historique salarial vide"""
        from app.pages_modules.consultant_info import show_salary_history

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Setup query chain for empty results
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []

        show_salary_history(1)

        # Vérifier que rien n'est affiché pour l'historique
        # (pas d'appel à markdown pour l'historique)
        calls = [call for call in mock_st.markdown.call_args_list
                if "Évolution salariale récente" in str(call)]
        assert len(calls) == 0

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    def test_show_detailed_salary_history_success(self, mock_session, mock_st):
        """Test affichage historique salarial détaillé avec succès"""
        from app.pages_modules.consultant_info import show_detailed_salary_history

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock salary records
        mock_salary1 = MagicMock()
        mock_salary1.date_debut = date.today()
        mock_salary1.salaire = 50000
        mock_salary1.commentaire = "Promotion"

        mock_salary2 = MagicMock()
        mock_salary2.date_debut = date.today() - relativedelta(months=12)
        mock_salary2.salaire = 45000
        mock_salary2.commentaire = "Augmentation"

        # Setup query chain
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [mock_salary1, mock_salary2]

        # Mock UI elements
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.button.return_value = False  # Don't close

        show_detailed_salary_history(1)

        # Vérifier que les éléments sont affichés
        assert mock_st.markdown.called
        assert mock_st.columns.called

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    def test_show_detailed_salary_history_empty(self, mock_session, mock_st):
        """Test affichage historique salarial détaillé vide"""
        from app.pages_modules.consultant_info import show_detailed_salary_history

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Setup query chain for empty results
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = []

        show_detailed_salary_history(1)

        # Vérifier que le message d'information est affiché
        mock_st.info.assert_called_with("ℹ️ Aucun historique salarial trouvé")

    @patch("app.pages_modules.consultant_info.st")
    def test_show_edit_info_form_success(self, mock_st):
        """Test affichage formulaire modification informations"""
        from app.pages_modules.consultant_info import show_edit_info_form

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean.dupont@email.com"
        mock_consultant.telephone = "0123456789"
        mock_consultant.salaire_actuel = 50000
        mock_consultant.disponibilite = True
        mock_consultant.notes = "Notes test"

        # Mock form inputs and UI elements
        mock_st.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]
        mock_st.text_input.return_value = "Jean"
        mock_st.number_input.return_value = 50000
        mock_st.checkbox.return_value = True
        mock_st.text_area.return_value = "Notes test"

        show_edit_info_form(mock_consultant)

        # Vérifier que le formulaire est affiché
        assert mock_st.markdown.called
        assert mock_st.form.called

    def test_validate_info_form_valid(self):
        """Test validation formulaire informations valide"""
        from app.pages_modules.consultant_info import validate_info_form

        with patch("app.pages_modules.consultant_info.st"):
            result = validate_info_form("Jean", "Dupont", "jean.dupont@email.com")

            assert result is True

    def test_validate_info_form_missing_prenom(self):
        """Test validation formulaire informations prénom manquant"""
        from app.pages_modules.consultant_info import validate_info_form

        with patch("app.pages_modules.consultant_info.st") as mock_st:
            result = validate_info_form("", "Dupont", "jean.dupont@email.com")

            assert result is False
            mock_st.error.assert_called_with("❌ Le prénom est obligatoire")

    def test_validate_info_form_missing_nom(self):
        """Test validation formulaire informations nom manquant"""
        from app.pages_modules.consultant_info import validate_info_form

        with patch("app.pages_modules.consultant_info.st") as mock_st:
            result = validate_info_form("Jean", "", "jean.dupont@email.com")

            assert result is False
            mock_st.error.assert_called_with("❌ Le nom est obligatoire")

    def test_validate_info_form_invalid_email(self):
        """Test validation formulaire informations email invalide"""
        from app.pages_modules.consultant_info import validate_info_form

        with patch("app.pages_modules.consultant_info.st") as mock_st:
            result = validate_info_form("Jean", "Dupont", "invalid-email")

            assert result is False
            mock_st.error.assert_called_with("❌ L'email doit être valide")

    @patch("app.pages_modules.consultant_info.ConsultantSalaire")
    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    def test_update_consultant_info_success(self, mock_session, mock_st, mock_salary_class):
        """Test mise à jour informations consultant avec succès"""
        from app.pages_modules.consultant_info import update_consultant_info

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.salaire_actuel = 45000

        # Setup queries - first for consultant lookup, second for email uniqueness check
        mock_query1 = MagicMock()
        mock_query2 = MagicMock()
        mock_session_instance.query.side_effect = [mock_query1, mock_query2]
        
        # First query returns the consultant
        mock_query1.filter.return_value.first.return_value = mock_consultant
        
        # Second query for email uniqueness returns None (no existing email)
        mock_query2.filter.return_value.first.return_value = None

        # Mock salary history class
        mock_salary_instance = MagicMock()
        mock_salary_class.return_value = mock_salary_instance

        test_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@email.com",
            "telephone": "0123456789",
            "salaire_actuel": 50000,  # Changed salary
            "disponibilite": True,
            "notes": "Updated notes",
            "commentaire": "Augmentation annuelle"
        }

        result = update_consultant_info(1, test_data)

        assert result is True
        mock_session_instance.commit.assert_called()

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    def test_update_consultant_info_consultant_not_found(self, mock_session, mock_st):
        """Test mise à jour informations consultant introuvable"""
        from app.pages_modules.consultant_info import update_consultant_info

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query returns None
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        test_data = {"prenom": "Jean", "nom": "Dupont", "email": "jean.dupont@email.com"}

        result = update_consultant_info(999, test_data)

        assert result is False
        mock_st.error.assert_called_with("❌ Consultant introuvable")

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    def test_update_consultant_info_email_exists(self, mock_session, mock_st):
        """Test mise à jour informations email déjà utilisé"""
        from app.pages_modules.consultant_info import update_consultant_info

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock existing consultant with same email
        mock_existing = MagicMock()
        mock_existing.id = 2

        # Setup queries
        mock_query1 = MagicMock()
        mock_session_instance.query.return_value = mock_query1
        mock_query1.filter.return_value.first.side_effect = [mock_consultant, mock_existing]

        test_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "existing@email.com",
            "salaire_actuel": 50000
        }

        result = update_consultant_info(1, test_data)

        assert result is False
        mock_st.error.assert_called_with("❌ Cet email est déjà utilisé par un autre consultant")

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info.get_database_session")
    def test_generate_consultant_report_success(self, mock_session, mock_st):
        """Test génération rapport consultant avec succès"""
        from app.pages_modules.consultant_info import generate_consultant_report

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean.dupont@email.com"
        mock_consultant.disponibilite = True
        mock_consultant.salaire_actuel = 50000

        # Mock practice
        mock_practice = MagicMock()
        mock_practice.nom = "Data Science"
        mock_consultant.practice = mock_practice

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock statistics queries
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 5  # 5 compétences and 5 missions

        generate_consultant_report(mock_consultant)

        # Vérifier que le rapport est généré
        assert mock_st.markdown.called
        assert mock_st.write.called
        assert mock_st.success.called

    @patch("app.pages_modules.consultant_info.st")
    def test_generate_consultant_report_no_practice(self, mock_st):
        """Test génération rapport consultant sans practice"""
        from app.pages_modules.consultant_info import generate_consultant_report

        # Mock consultant without practice
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean.dupont@email.com"
        mock_consultant.disponibilite = True
        mock_consultant.salaire_actuel = 50000
        mock_consultant.practice = None

        generate_consultant_report(mock_consultant)

        # Vérifier que le rapport est généré avec "Non affecté"
        assert mock_st.markdown.called
        assert mock_st.write.called