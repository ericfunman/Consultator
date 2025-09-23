"""
Tests pour le module consultant_missions.py
Couverture des fonctions de gestion des missions des consultants
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class TestConsultantMissions:
    """Tests pour les fonctions de gestion des missions"""

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.imports_ok", True)
    def test_show_consultant_missions_success(self, mock_session, mock_st):
        """Test affichage missions consultant avec succès"""
        from app.pages_modules.consultant_missions import show_consultant_missions

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock session et missions
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock mission
        mock_mission = MagicMock()
        mock_mission.titre = "Test Mission"
        mock_mission.client.nom = "Test Client"
        mock_mission.date_debut = date.today()
        mock_mission.en_cours = True

        # Mock client
        mock_client = MagicMock()
        mock_client.nom = "Test Client"
        mock_mission.client = mock_client

        # Setup query chain
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [mock_mission]

        # Mock UI elements
        mock_st.expander.return_value.__enter__.return_value = None
        mock_st.expander.return_value.__exit__.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        show_consultant_missions(mock_consultant)

        # Vérifier que la fonction s'exécute sans erreur
        assert mock_st.markdown.called

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.imports_ok", True)
    def test_show_consultant_missions_no_missions(self, mock_session, mock_st):
        """Test affichage missions consultant sans missions"""
        from app.pages_modules.consultant_missions import show_consultant_missions

        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock session sans missions
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Setup query chain
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = []

        show_consultant_missions(mock_consultant)

        # Vérifier que la fonction s'exécute sans erreur
        assert mock_st.markdown.called

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_no_consultant(self, mock_st):
        """Test affichage missions sans consultant"""
        from app.pages_modules.consultant_missions import show_consultant_missions

        show_consultant_missions(None)

        # Vérifier qu'une erreur est affichée
        assert mock_st.error.called

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_mission_details(self, mock_st):
        """Test affichage détails d'une mission"""
        from app.pages_modules.consultant_missions import show_mission_details

        # Mock mission avec des valeurs numériques réelles
        mock_mission = MagicMock()
        mock_mission.date_debut = date.today()
        mock_mission.date_fin = None
        mock_mission.en_cours = True
        mock_mission.tjm = 500
        mock_mission.taux_journalier = 500
        mock_mission.salaire_mensuel = 10000
        mock_mission.description = "Test description"
        mock_mission.competences_requises = "Python, Django"

        # Mock client
        mock_client = MagicMock()
        mock_client.nom = "Test Client"
        mock_client.secteur = "Tech"
        mock_mission.client = mock_client

        # Mock UI elements - colonnes pour les détails (2) et actions (3)
        mock_st.columns.side_effect = lambda n: [MagicMock() for _ in range(n)]

        show_mission_details(mock_mission)

        assert mock_st.columns.called
        assert mock_st.markdown.called

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_statistics(self, mock_st):
        """Test affichage statistiques des missions"""
        from app.pages_modules.consultant_missions import show_missions_statistics

        # Mock missions avec des valeurs numériques réelles
        mock_mission1 = MagicMock()
        mock_mission1.en_cours = True
        mock_mission1.date_fin = None
        mock_mission1.taux_journalier = 500  # Valeur numérique réelle
        mock_mission1.date_debut = date.today()

        mock_mission2 = MagicMock()
        mock_mission2.en_cours = False
        mock_mission2.date_fin = date.today()
        mock_mission2.taux_journalier = 450  # Valeur numérique réelle
        mock_mission2.date_debut = date.today() - relativedelta(days=30)

        missions = [mock_mission1, mock_mission2]

        # Mock UI elements
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        mock_st.metric = MagicMock()  # Mock metric to avoid formatting issues

        show_missions_statistics(missions)

        assert mock_st.markdown.called
        assert mock_st.columns.called

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_statistics_empty(self, mock_st):
        """Test affichage statistiques sans missions"""
        from app.pages_modules.consultant_missions import show_missions_statistics

        show_missions_statistics([])

        # Ne devrait rien afficher
        assert not mock_st.markdown.called

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_add_mission_form_success(self, mock_session, mock_st):
        """Test affichage formulaire ajout mission avec succès"""
        from app.pages_modules.consultant_missions import show_add_mission_form

        # Mock session et clients
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock client
        mock_client = MagicMock()
        mock_client.id = 1
        mock_client.nom = "Test Client"
        mock_session_instance.query.return_value.all.return_value = [mock_client]

        # Mock form
        mock_st.form.return_value.__enter__.return_value = None
        mock_st.form.return_value.__exit__.return_value = None
        mock_st.form_submit_button.return_value = False  # No submission

        # Mock form inputs
        mock_st.text_input.return_value = "Test Mission"
        mock_st.selectbox.return_value = 1
        mock_st.date_input.return_value = date.today()
        mock_st.checkbox.return_value = True
        mock_st.number_input.return_value = 500
        mock_st.text_area.return_value = "Test description"

        show_add_mission_form(1)

        assert mock_st.markdown.called
        assert mock_st.form.called

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_add_mission_form_no_clients(self, mock_session, mock_st):
        """Test affichage formulaire ajout mission sans clients"""
        from app.pages_modules.consultant_missions import show_add_mission_form

        # Mock session sans clients
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session_instance.query.return_value.all.return_value = []

        show_add_mission_form(1)

        # Vérifier que la fonction s'exécute sans erreur
        assert mock_st.markdown.called

    def test_validate_mission_form_valid(self):
        """Test validation formulaire mission valide"""
        from app.pages_modules.consultant_missions import validate_mission_form

        with patch("app.pages_modules.consultant_missions.st"):
            result = validate_mission_form(
                "Test Mission", 1, date.today(), False, date.today() + relativedelta(days=30)
            )

            assert result is True

    def test_validate_mission_form_missing_title(self):
        """Test validation formulaire mission titre manquant"""
        from app.pages_modules.consultant_missions import validate_mission_form

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            result = validate_mission_form("", 1, date.today(), True, None)

            assert result is False
            mock_st.error.assert_called_with("❌ Le titre de la mission est obligatoire")

    def test_validate_mission_form_missing_client(self):
        """Test validation formulaire mission client manquant"""
        from app.pages_modules.consultant_missions import validate_mission_form

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            result = validate_mission_form("Test Mission", None, date.today(), True, None)

            assert result is False
            mock_st.error.assert_called_with("❌ Le client est obligatoire")

    def test_validate_mission_form_invalid_dates(self):
        """Test validation formulaire mission dates invalides"""
        from app.pages_modules.consultant_missions import validate_mission_form

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            result = validate_mission_form(
                "Test Mission", 1, date.today(), False, date.today() - relativedelta(days=1)
            )

            assert result is False
            mock_st.error.assert_called_with("❌ La date de fin doit être postérieure à la date de début")

    @patch("app.pages_modules.consultant_missions.Mission")
    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_create_mission_success(self, mock_session, mock_st, mock_mission_class):
        """Test création mission avec succès"""
        from app.pages_modules.consultant_missions import create_mission

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Mock Mission class
        mock_mission_instance = MagicMock()
        mock_mission_class.return_value = mock_mission_instance

        test_data = {
            "titre": "Test Mission",
            "client_id": 1,
            "date_debut": date.today(),
            "date_fin": None,
            "en_cours": True,
            "taux_journalier": 500,  # Valeur numérique réelle
            "tjm": 500,  # Valeur numérique réelle
            "salaire_mensuel": 10000,  # Valeur numérique réelle
            "description": "Test description",
            "competences_requises": "Python, Django"
        }

        result = create_mission(1, test_data)

        assert result is True
        mock_session_instance.add.assert_called_with(mock_mission_instance)
        mock_session_instance.commit.assert_called()

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_edit_mission_form_success(self, mock_session, mock_st):
        """Test affichage formulaire édition mission"""
        from app.pages_modules.consultant_missions import show_edit_mission_form

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock mission
        mock_mission = MagicMock()
        mock_mission.id = 1
        mock_mission.titre = "Test Mission"
        mock_mission.client_id = 1
        mock_mission.date_debut = date.today()
        mock_mission.date_fin = None
        mock_mission.en_cours = True
        mock_mission.taux_journalier = 500
        mock_mission.salaire_mensuel = None
        mock_mission.description = "Test description"
        mock_mission.competences_requises = "Python"

        # Mock client
        mock_client = MagicMock()
        mock_client.id = 1
        mock_client.nom = "Test Client"

        # Setup query chains
        mock_query1 = MagicMock()
        mock_session_instance.query.return_value = mock_query1
        mock_query1.options.return_value = mock_query1
        mock_query1.filter.return_value = mock_query1
        mock_query1.first.return_value = mock_mission

        # Second query for clients
        mock_session_instance.query.return_value.all.return_value = [mock_client]

        # Mock form
        mock_st.form.return_value.__enter__.return_value = None
        mock_st.form.return_value.__exit__.return_value = None
        mock_st.form_submit_button.return_value = False  # No submission

        show_edit_mission_form(1)

        assert mock_st.markdown.called

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_show_edit_mission_form_not_found(self, mock_session, mock_st):
        """Test affichage formulaire édition mission introuvable"""
        from app.pages_modules.consultant_missions import show_edit_mission_form

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query returns None
        mock_query = MagicMock()
        mock_session_instance.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        show_edit_mission_form(999)

        # Vérifier qu'une erreur est affichée
        assert mock_st.error.called

    @patch("app.pages_modules.consultant_missions.Mission")
    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_update_mission_success(self, mock_session, mock_st, mock_mission_class):
        """Test mise à jour mission avec succès"""
        from app.pages_modules.consultant_missions import update_mission

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock mission
        mock_mission = MagicMock()
        mock_mission.id = 1

        # Setup query
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_mission

        test_data = {
            "titre": "Updated Mission",
            "client_id": 1,
            "date_debut": date.today(),
            "date_fin": None,
            "en_cours": True,
            "taux_journalier": 550,  # Valeur numérique réelle
            "salaire_mensuel": 11000,  # Valeur numérique réelle
            "description": "Updated description",
            "competences_requises": "Python, Django"
        }

        result = update_mission(1, test_data)

        assert result is True
        mock_session_instance.commit.assert_called()

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_update_mission_not_found(self, mock_session, mock_st):
        """Test mise à jour mission introuvable"""
        from app.pages_modules.consultant_missions import update_mission

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query returns None
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        test_data = {"titre": "Test", "client_id": 1, "date_debut": date.today(), "en_cours": True}

        result = update_mission(999, test_data)

        assert result is False
        # Vérifier qu'une erreur est affichée
        assert mock_st.error.called

    @patch("app.pages_modules.consultant_missions.Mission")
    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_delete_mission_success(self, mock_session, mock_st, mock_mission_class):
        """Test suppression mission avec succès"""
        from app.pages_modules.consultant_missions import delete_mission

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock mission
        mock_mission = MagicMock()
        mock_mission.id = 1

        # Setup query
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_mission

        result = delete_mission(1)

        assert result is True
        mock_session_instance.delete.assert_called_with(mock_mission)
        mock_session_instance.commit.assert_called()

    @patch("app.pages_modules.consultant_missions.st")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    def test_delete_mission_not_found(self, mock_session, mock_st):
        """Test suppression mission introuvable"""
        from app.pages_modules.consultant_missions import delete_mission

        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query returns None
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        result = delete_mission(999)

        assert result is False
        # Vérifier qu'une erreur est affichée
        assert mock_st.error.called

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_mission_full_details(self, mock_st):
        """Test affichage détails complets d'une mission"""
        from app.pages_modules.consultant_missions import show_mission_full_details

        # Mock mission avec des valeurs numériques réelles
        mock_mission = MagicMock()
        mock_mission.id = 1
        mock_mission.date_debut = date.today()
        mock_mission.date_fin = date.today() + relativedelta(days=30)
        mock_mission.en_cours = False
        mock_mission.tjm = 500  # Valeur numérique réelle
        mock_mission.taux_journalier = 500  # Valeur numérique réelle
        mock_mission.salaire_mensuel = 10000  # Valeur numérique réelle
        mock_mission.description = "Test description"
        mock_mission.competences_requises = "Python, Django"

        # Mock client
        mock_client = MagicMock()
        mock_client.nom = "Test Client"
        mock_client.secteur = "Tech"
        mock_client.adresse = "123 Test St"
        mock_client.contact_principal = "John Doe"
        mock_mission.client = mock_client

        # Mock UI elements
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.button.return_value = False  # Don't close details

        show_mission_full_details(mock_mission)

        assert mock_st.markdown.called
        assert mock_st.columns.called

    @patch("app.pages_modules.consultant_missions._calculate_year_revenue")
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_analysis(self, mock_st, mock_calc_revenue):
        """Test affichage analyse des missions"""
        from app.pages_modules.consultant_missions import show_missions_analysis

        # Mock _calculate_year_revenue to return a real number
        mock_calc_revenue.return_value = 10000  # Return a real revenue value

        # Mock missions avec des valeurs numériques réelles
        mock_mission1 = MagicMock()
        mock_mission1.en_cours = True
        mock_mission1.date_debut = date.today()
        mock_mission1.taux_journalier = 500  # Valeur numérique réelle

        mock_mission2 = MagicMock()
        mock_mission2.en_cours = False
        mock_mission2.date_fin = date.today()
        mock_mission2.date_debut = date.today() - relativedelta(days=30)
        mock_mission2.taux_journalier = 450  # Valeur numérique réelle

        # Mock clients
        mock_client1 = MagicMock()
        mock_client1.nom = "Client A"
        mock_client2 = MagicMock()
        mock_client2.nom = "Client B"

        mock_mission1.client = mock_client1
        mock_mission2.client = mock_client2

        missions = [mock_mission1, mock_mission2]

        # Mock UI elements
        mock_st.columns.return_value = [MagicMock(), MagicMock()]

        show_missions_analysis(missions)

        assert mock_st.markdown.called

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_analysis_empty(self, mock_st):
        """Test affichage analyse missions sans données"""
        from app.pages_modules.consultant_missions import show_missions_analysis

        show_missions_analysis([])

        mock_st.info.assert_called_with("ℹ️ Aucune mission à analyser")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues(self, mock_st):
        """Test affichage analyse revenus des missions"""
        from app.pages_modules.consultant_missions import show_missions_revenues

        # Mock missions avec revenus
        mock_mission = MagicMock()
        mock_mission.titre = "Test Mission"
        mock_mission.taux_journalier = 500
        mock_mission.en_cours = False
        mock_mission.date_debut = date.today() - relativedelta(days=30)
        mock_mission.date_fin = date.today()

        # Mock client
        mock_client = MagicMock()
        mock_client.nom = "Test Client"
        mock_mission.client = mock_client

        missions = [mock_mission]

        # Mock UI elements
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        show_missions_revenues(missions)

        assert mock_st.markdown.called

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues_empty(self, mock_st):
        """Test affichage analyse revenus sans missions"""
        from app.pages_modules.consultant_missions import show_missions_revenues

        show_missions_revenues([])

        mock_st.info.assert_called_with("ℹ️ Aucune mission pour analyser les revenus")