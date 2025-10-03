"""
Tests de couverture pour consultant_missions.py
"""

from datetime import date
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest


class TestConsultantMissionsCoverage:
    """Tests de couverture pour le module consultant_missions.py"""

    @pytest.fixture
    def mock_consultant(self):
        """Mock d'un consultant"""
        consultant = MagicMock()
        consultant.id = 1
        consultant.prenom = "Marie"
        consultant.nom = "Martin"
        return consultant

    @pytest.fixture
    def mock_client(self):
        """Mock d'un client"""
        client = MagicMock()
        client.id = 1
        client.nom = "Société Générale"
        return client

    @pytest.fixture
    def mock_mission_active(self, mock_client):
        """Mock d'une mission active"""
        mission = MagicMock()
        mission.id = 1
        mission.titre = "Projet Data Analytics"
        mission.client = mock_client
        mission.client_id = mock_client.id
        mission.date_debut = date(2024, 1, 1)
        mission.date_fin = None
        mission.en_cours = True
        mission.taux_journalier = 450
        mission.tjm = 450
        mission.salaire_mensuel = 0
        mission.description = "Développement d'un système d'analyse de données"
        mission.competences_requises = "Python, SQL, Docker"
        return mission

    @patch("app.pages_modules.consultant_missions.show_missions_statistics")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_with_data(
        self,
        mock_st,
        mock_get_session,
        mock_show_stats,
        mock_consultant,
        mock_mission_active,
    ):
        """Test de l'affichage des missions avec données"""
        # Set imports_ok to True
        import app.pages_modules.consultant_missions as cm_module

        cm_module.imports_ok = True

        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock the SQLAlchemy query chain properly
        mock_query = MagicMock()
        mock_options = MagicMock()
        mock_filtered = MagicMock()
        mock_ordered = MagicMock()

        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_options
        mock_options.filter.return_value = mock_filtered
        mock_filtered.order_by.return_value = mock_ordered
        mock_ordered.all.return_value = [mock_mission_active]

        # Mock show_missions_statistics to do nothing
        mock_show_stats.return_value = None

        from app.pages_modules.consultant_missions import (
            show_consultant_missions,
        )

        show_consultant_missions(mock_consultant)

        # Vérifier que st.markdown a été appelé pour le titre
        mock_st.markdown.assert_called_with("### 🚀 Missions")

    @patch("app.pages_modules.consultant_missions.joinedload")
    @patch("app.pages_modules.consultant_missions.show_add_mission_form")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_no_data(
        self, mock_st, mock_get_session, mock_show_add, mock_joinedload, mock_consultant
    ):
        """Test de l'affichage des missions sans données"""
        # Patch imports_ok and the model classes before importing the module
        import app.pages_modules.consultant_missions as cm_module

        cm_module.imports_ok = True
        # Create mock classes for the models
        mock_mission_class = Mock()
        mock_client_class = Mock()
        cm_module.Mission = mock_mission_class
        cm_module.Client = mock_client_class

        mock_session = Mock()
        # Properly mock the context manager
        mock_get_session.return_value.__enter__ = Mock(return_value=mock_session)
        mock_get_session.return_value.__exit__ = Mock(return_value=None)

        # Mock joinedload to return a mock
        mock_joinedload.return_value = Mock()

        # Mock the SQLAlchemy query chain properly
        mock_query = Mock()
        mock_options = Mock()
        mock_filtered = Mock()
        mock_ordered = Mock()

        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_options
        mock_options.filter.return_value = mock_filtered
        mock_filtered.order_by.return_value = mock_ordered
        mock_ordered.all.return_value = []

        # Mock show_add_mission_form to do nothing
        mock_show_add.return_value = None

        from app.pages_modules.consultant_missions import (
            show_consultant_missions,
        )

        show_consultant_missions(mock_consultant)

        # Vérifier que st.info a été appelé pour les missions vides
        mock_st.info.assert_called_with("ℹ️ Aucune mission enregistrée pour ce consultant")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_valid(self, mock_st):
        """Test de validation de formulaire valide"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="Test Mission",
            client_id=1,
            date_debut=date(2024, 1, 1),
            en_cours=False,
            date_fin=date(2024, 6, 30),
        )

        assert result is True

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_invalid_title(self, mock_st):
        """Test de validation avec titre invalide"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="",
            client_id=1,
            date_debut=date(2024, 1, 1),
            en_cours=True,
            date_fin=None,
        )

        assert result is False
        mock_st.error.assert_called_with("❌ Le titre de la mission est obligatoire")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_invalid_dates(self, mock_st):
        """Test de validation avec dates invalides"""
        from app.pages_modules.consultant_missions import validate_mission_form

        # Test avec date de fin avant date de début
        result = validate_mission_form(
            titre="Test Mission",
            client_id=1,
            date_debut=date(2024, 6, 30),
            en_cours=False,
            date_fin=date(2024, 1, 1),
        )

        assert result is False
        mock_st.error.assert_called_with("❌ La date de fin doit être postérieure à la date de début")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_missing_client(self, mock_st):
        """Test de validation avec client manquant"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form(
            titre="Test Mission",
            client_id=None,
            date_debut=date(2024, 1, 1),
            en_cours=True,
            date_fin=None,
        )

        assert result is False
        mock_st.error.assert_called_with("❌ Le client est obligatoire")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_invalid_rates(self, mock_st):
        """Test de validation avec taux invalides - ce test n'est pas applicable car validate_mission_form ne valide pas les taux"""
        # validate_mission_form ne valide que les champs de base (titre, client, dates)
        # Les validations de taux sont faites ailleurs dans le code
        # Ce test est donc retiré car non applicable
        pass

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_statistics(self, mock_st, mock_mission_active):
        """Test de l'affichage des statistiques des missions"""
        # Mock st.columns pour les statistiques
        mock_columns = [Mock() for _ in range(4)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.pages_modules.consultant_missions import (
            show_missions_statistics,
        )

        missions = [mock_mission_active]
        show_missions_statistics(missions)

        # Vérifier que st.metric a été appelé pour chaque statistique
        assert mock_st.metric.call_count == 4

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_analysis(self, mock_st, mock_mission_active):
        """Test de l'analyse des missions"""
        # Mock st.columns pour l'analyse
        mock_columns = [Mock() for _ in range(2)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.pages_modules.consultant_missions import (
            show_missions_analysis,
        )

        missions = [mock_mission_active]
        show_missions_analysis(missions)

        mock_st.markdown.assert_any_call("### 📊 Analyse des missions")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues(self, mock_st, mock_mission_active):
        """Test de l'analyse des revenus"""
        # Mock st.columns pour retourner des context managers
        mock_col1 = MagicMock()
        mock_col1.__enter__ = MagicMock(return_value=mock_col1)
        mock_col1.__exit__ = MagicMock(return_value=None)
        mock_col2 = MagicMock()
        mock_col2.__enter__ = MagicMock(return_value=mock_col2)
        mock_col2.__exit__ = MagicMock(return_value=None)
        mock_col3 = MagicMock()
        mock_col3.__enter__ = MagicMock(return_value=mock_col3)
        mock_col3.__exit__ = MagicMock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3)

        # Mock st.dataframe to avoid issues with pandas - use MagicMock for Python 3.11 compatibility
        mock_st.dataframe = MagicMock(return_value=None)

        from app.pages_modules.consultant_missions import (
            show_missions_revenues,
        )

        missions = [mock_mission_active]
        show_missions_revenues(missions)

        mock_st.markdown.assert_any_call("### 📈 Analyse des revenus")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_mission_full_details(self, mock_st, mock_mission_active):
        """Test de l'affichage des détails complets"""
        # Mock st.columns pour les détails
        mock_columns = [Mock() for _ in range(2)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        # Mock session state
        mock_st.session_state = {}

        # Mock bouton
        mock_st.button.return_value = False  # Bouton non cliqué

        from app.pages_modules.consultant_missions import (
            show_mission_full_details,
        )

        show_mission_full_details(mock_mission_active)

        mock_st.markdown.assert_any_call("### 📋 Détails complets de la mission")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_mission_details(self, mock_st, mock_mission_active):
        """Test de l'affichage des détails d'une mission"""
        # Mock st.columns pour les détails
        mock_columns_details = [Mock() for _ in range(2)]
        for col in mock_columns_details:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)

        # Mock st.columns pour les actions
        mock_columns_actions = [Mock() for _ in range(3)]
        for col in mock_columns_actions:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)

        mock_st.columns.side_effect = [mock_columns_details, mock_columns_actions]

        # Mock session state
        mock_st.session_state = {}

        # Mock boutons
        mock_st.button.side_effect = [False, False, False]  # Aucun bouton cliqué

        from app.pages_modules.consultant_missions import show_mission_details

        show_mission_details(mock_mission_active)

        # Vérifier que les informations de base sont affichées
        mock_st.markdown.assert_any_call("**📅 Période**")
        mock_st.markdown.assert_any_call("**🏢 Client**")
        mock_st.markdown.assert_any_call("**💰 Rémunération**")
        mock_st.markdown.assert_any_call("**📊 Informations**")
        mock_st.markdown.assert_any_call("**🛠️ Compétences requises**")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_statistics_empty_list(self, mock_st):
        """Test des statistiques avec liste vide"""
        from app.pages_modules.consultant_missions import (
            show_missions_statistics,
        )

        missions = []
        show_missions_statistics(missions)

        # Vérifier que rien n'est affiché pour la liste vide (fonction retourne tôt)
        mock_st.info.assert_not_called()

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_analysis_empty_list(self, mock_st):
        """Test de l'analyse avec liste vide"""
        from app.pages_modules.consultant_missions import (
            show_missions_analysis,
        )

        missions = []
        show_missions_analysis(missions)

        # Vérifier que st.info a été appelé pour la liste vide
        mock_st.info.assert_called_with("ℹ️ Aucune mission à analyser")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues_empty_list(self, mock_st):
        """Test de l'analyse des revenus avec liste vide"""
        from app.pages_modules.consultant_missions import (
            show_missions_revenues,
        )

        missions = []
        show_missions_revenues(missions)

        # Vérifier que st.info a été appelé pour la liste vide
        mock_st.info.assert_called_with("ℹ️ Aucune mission pour analyser les revenus")

    @patch("app.pages_modules.consultant_missions.imports_ok", False)
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_imports_failed(self, mock_st, mock_consultant):
        """Test de l'affichage quand les imports ont échoué"""
        from app.pages_modules.consultant_missions import (
            show_consultant_missions,
        )

        show_consultant_missions(mock_consultant)

        mock_st.error.assert_called_once_with("❌ Les services de base ne sont pas disponibles")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_no_consultant(self, mock_st):
        """Test de l'affichage sans consultant fourni"""
        from app.pages_modules.consultant_missions import (
            show_consultant_missions,
        )

        show_consultant_missions(None)

        mock_st.error.assert_called_once_with("❌ Consultant non fourni")

    @patch("app.pages_modules.consultant_missions.joinedload")
    @patch("app.pages_modules.consultant_missions.show_add_mission_form")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_empty_list(
        self, mock_st, mock_get_session, mock_show_add, mock_joinedload, mock_consultant
    ):
        """Test de l'affichage avec une liste de missions vide"""
        # Patch imports_ok and the model classes before importing the module
        import app.pages_modules.consultant_missions as cm_module

        cm_module.imports_ok = True
        # Create mock classes for the models
        mock_mission_class = Mock()
        mock_client_class = Mock()
        cm_module.Mission = mock_mission_class
        cm_module.Client = mock_client_class

        mock_session = Mock()
        # Properly mock the context manager
        mock_get_session.return_value.__enter__ = Mock(return_value=mock_session)
        mock_get_session.return_value.__exit__ = Mock(return_value=None)

        # Mock joinedload to return a mock
        mock_joinedload.return_value = Mock()

        # Mock the SQLAlchemy query chain properly
        mock_query = Mock()
        mock_options = Mock()
        mock_filtered = Mock()
        mock_ordered = Mock()

        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_options
        mock_options.filter.return_value = mock_filtered
        mock_filtered.order_by.return_value = mock_ordered
        mock_ordered.all.return_value = []

        # Mock show_add_mission_form to do nothing
        mock_show_add.return_value = None

        from app.pages_modules.consultant_missions import (
            show_consultant_missions,
        )

        show_consultant_missions(mock_consultant)

        # Vérifier que st.info a été appelé pour les missions vides
        mock_st.info.assert_called_with("ℹ️ Aucune mission enregistrée pour ce consultant")

    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_remuneration(self, mock_st):
        """Test du rendu des champs de rémunération"""
        from app.pages_modules.consultant_missions import (
            _render_mission_remuneration,
        )

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3)
        mock_st.number_input.side_effect = [
            450,
            500,
            6000,
        ]  # taux_journalier, tjm, salaire_mensuel

        result = _render_mission_remuneration()

        assert result == (450, 500, 6000)
        mock_st.markdown.assert_called_with("#### 💰 Rémunération")
        assert mock_st.number_input.call_count == 3

    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_description(self, mock_st):
        """Test du rendu des champs de description"""
        from app.pages_modules.consultant_missions import (
            _render_mission_description,
        )

        mock_st.text_area.side_effect = ["Description test", "Python, SQL"]

        result = _render_mission_description()

        assert result == ("Description test", "Python, SQL")
        mock_st.markdown.assert_called_with("#### 📝 Description")
        assert mock_st.text_area.call_count == 2

    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_load_clients_for_mission(self, mock_st, mock_get_session):
        """Test du chargement des clients pour les missions"""
        from app.pages_modules.consultant_missions import (
            _load_clients_for_mission,
        )

        # Mock de la session DB
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock des clients
        mock_client1 = Mock()
        mock_client1.id = 1
        mock_client1.nom = "Client A"
        mock_client2 = Mock()
        mock_client2.id = 2
        mock_client2.nom = "Client B"

        mock_session.query.return_value.all.return_value = [mock_client1, mock_client2]

        result = _load_clients_for_mission()

        expected = {1: "Client A", 2: "Client B"}
        assert result == expected

    @patch("app.pages_modules.consultant_missions._load_clients_for_mission")
    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_general_info_with_clients(self, mock_st, mock_load_clients):
        """Test du rendu des informations générales avec clients disponibles"""
        from datetime import date

        from app.pages_modules.consultant_missions import (
            _render_mission_general_info,
        )

        # Mock _load_clients_for_mission
        mock_load_clients.return_value = {1: "Client A", 2: "Client B"}

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock des inputs
        mock_st.text_input.return_value = "Test Mission"
        mock_st.selectbox.return_value = 1
        mock_st.date_input.side_effect = [date(2024, 1, 1), date(2024, 6, 30)]
        mock_st.checkbox.return_value = False

        result = _render_mission_general_info()

        assert result == ("Test Mission", 1, date(2024, 1, 1), date(2024, 6, 30), False)
        mock_st.markdown.assert_called_with("#### 📋 Informations générales")

    @patch("app.pages_modules.consultant_missions._load_clients_for_mission")
    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_general_info_no_clients(self, mock_st, mock_load_clients):
        """Test du rendu des informations générales sans clients"""
        from app.pages_modules.consultant_missions import (
            _render_mission_general_info,
        )

        # Mock _load_clients_for_mission retournant un dict vide
        mock_load_clients.return_value = {}

        result = _render_mission_general_info()

        assert result == (None, None, None, None, None)
        mock_st.warning.assert_called_with("⚠️ Aucun client trouvé. Veuillez créer des clients d'abord.")

    @patch("app.pages_modules.consultant_missions.st")
    def test_render_edit_mission_general_info(self, mock_st, mock_mission_active):
        """Test du rendu des informations générales en édition"""
        from datetime import date

        from app.pages_modules.consultant_missions import (
            _render_edit_mission_general_info,
        )

        client_options = {1: "Client A", 2: "Client B"}

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock des inputs
        mock_st.text_input.return_value = "Mission modifiée"
        mock_st.selectbox.return_value = 2
        mock_st.date_input.side_effect = [date(2024, 2, 1), date(2024, 7, 31)]
        mock_st.checkbox.return_value = False

        result = _render_edit_mission_general_info(mock_mission_active, client_options)

        assert result == (
            "Mission modifiée",
            2,
            date(2024, 2, 1),
            False,
            date(2024, 7, 31),
        )
        mock_st.markdown.assert_called_with("#### 📋 Informations générales")

    @patch("app.pages_modules.consultant_missions.st")
    def test_render_edit_mission_remuneration(self, mock_st, mock_mission_active):
        """Test du rendu de la rémunération en édition"""
        from app.pages_modules.consultant_missions import (
            _render_edit_mission_remuneration,
        )

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2)
        mock_st.number_input.side_effect = [
            500,
            7000,
        ]  # taux_journalier, salaire_mensuel

        result = _render_edit_mission_remuneration(mock_mission_active)

        assert result == (500, 7000)
        mock_st.markdown.assert_called_with("#### 💰 Rémunération")

    @patch("app.pages_modules.consultant_missions.st")
    def test_render_edit_mission_description(self, mock_st, mock_mission_active):
        """Test du rendu de la description en édition"""
        from app.pages_modules.consultant_missions import (
            _render_edit_mission_description,
        )

        mock_st.text_area.side_effect = ["Description modifiée", "Python, ML"]

        result = _render_edit_mission_description(mock_mission_active)

        assert result == ("Description modifiée", "Python, ML")
        mock_st.markdown.assert_called_with("#### 📝 Description")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_chronology_completed(self, mock_st, mock_mission_active):
        """Test de l'affichage de la chronologie pour mission terminée"""
        from datetime import date

        from app.pages_modules.consultant_missions import (
            _display_mission_chronology,
        )

        # Modifier la mission pour qu'elle soit terminée
        mock_mission_active.date_fin = date(2024, 6, 30)
        mock_mission_active.en_cours = False

        _display_mission_chronology(mock_mission_active)

        mock_st.markdown.assert_called_with("#### 📅 Chronologie")
        mock_st.write.assert_any_call("**Date de début :** 01/01/2024")
        mock_st.write.assert_any_call("**Date de fin :** 30/06/2024")
        # Vérifier que la durée est calculée (environ 5 mois)
        duration_calls = [call for call in mock_st.write.call_args_list if "Durée" in str(call)]
        assert len(duration_calls) > 0

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_chronology_ongoing(self, mock_st, mock_mission_active):
        """Test de l'affichage de la chronologie pour mission en cours"""
        from app.pages_modules.consultant_missions import (
            _display_mission_chronology,
        )

        _display_mission_chronology(mock_mission_active)

        mock_st.markdown.assert_called_with("#### 📅 Chronologie")
        mock_st.write.assert_any_call("**Date de début :** 01/01/2024")
        mock_st.write.assert_any_call("**Statut :** 🔄 En cours")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_financial_aspects(self, mock_st, mock_mission_active):
        """Test de l'affichage des aspects financiers"""
        from app.pages_modules.consultant_missions import (
            _display_mission_financial_aspects,
        )

        _display_mission_financial_aspects(mock_mission_active)

        mock_st.markdown.assert_called_with("#### 💰 Aspects financiers")
        mock_st.write.assert_any_call("**TJM Mission :** 450€")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_descriptions(self, mock_st, mock_mission_active):
        """Test de l'affichage des descriptions"""
        from app.pages_modules.consultant_missions import (
            _display_mission_descriptions,
        )

        _display_mission_descriptions(mock_mission_active)

        mock_st.markdown.assert_any_call("#### 📝 Description détaillée")
        mock_st.markdown.assert_any_call("#### 🛠️ Compétences requises")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_client_info(self, mock_st, mock_mission_active):
        """Test de l'affichage des informations client"""
        from app.pages_modules.consultant_missions import (
            _display_mission_client_info,
        )

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2)

        _display_mission_client_info(mock_mission_active)

        mock_st.markdown.assert_called_with("#### 🏢 Informations client")
        mock_st.write.assert_any_call("**Nom :** Société Générale")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_mission_full_details(self, mock_st, mock_mission_active):
        """Test de l'affichage des détails complets de mission"""
        from app.pages_modules.consultant_missions import (
            show_mission_full_details,
        )

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2)
        mock_st.button.return_value = False  # Bouton non cliqué

        show_mission_full_details(mock_mission_active)

        mock_st.markdown.assert_any_call("### 📋 Détails complets de la mission")
        # Vérifier que les fonctions d'affichage ont été appelées
        assert mock_st.markdown.call_count > 5  # Plusieurs sections

    def test_calculate_mission_statistics(self, mock_mission_active):
        """Test du calcul des statistiques de missions"""
        from app.pages_modules.consultant_missions import (
            _calculate_mission_statistics,
        )

        missions = [mock_mission_active]
        client_counts, status_counts = _calculate_mission_statistics(missions)

        assert client_counts == {"Société Générale": 1}
        assert status_counts["En cours"] == 1

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_missions_by_client_and_status(self, mock_st):
        """Test de l'affichage de la répartition par client et statut"""
        from app.pages_modules.consultant_missions import (
            _display_missions_by_client_and_status,
        )

        client_counts = {"Client A": 2, "Client B": 1}
        status_counts = {"En cours": 2, "Terminées": 1}

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2)

        _display_missions_by_client_and_status(client_counts, status_counts)

        mock_st.markdown.assert_any_call("#### 🏢 Répartition par client")
        mock_st.markdown.assert_any_call("#### 📊 Répartition par statut")

    def test_group_missions_by_year(self, mock_mission_active):
        """Test du groupement des missions par année"""
        from app.pages_modules.consultant_missions import (
            _group_missions_by_year,
        )

        missions = [mock_mission_active]
        result = _group_missions_by_year(missions)

        assert 2024 in result
        assert len(result[2024]) == 1

    def test_calculate_year_revenue(self, mock_mission_active):
        """Test du calcul des revenus par année"""
        from datetime import date

        from app.pages_modules.consultant_missions import (
            _calculate_year_revenue,
        )

        # Modifier la mission pour qu'elle soit terminée
        mock_mission_active.date_fin = date(2024, 6, 30)
        mock_mission_active.en_cours = False

        year_missions = [mock_mission_active]
        revenue = _calculate_year_revenue(year_missions, 2024)

        assert revenue > 0  # Devrait calculer des revenus

    @patch("app.pages_modules.consultant_missions.st")
    def test_analyze_missions_by_year(self, mock_st, mock_mission_active):
        """Test de l'analyse temporelle des missions"""
        from app.pages_modules.consultant_missions import (
            _analyze_missions_by_year,
        )

        missions = [mock_mission_active]
        _analyze_missions_by_year(missions)

        mock_st.markdown.assert_called_with("#### 📈 Analyse temporelle")
        mock_st.write.assert_any_call("**2024 :** 1 mission(s)")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_analysis_with_data(self, mock_st, mock_mission_active):
        """Test de l'analyse complète des missions avec données"""
        from app.pages_modules.consultant_missions import (
            show_missions_analysis,
        )

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2)

        missions = [mock_mission_active]
        show_missions_analysis(missions)

        mock_st.markdown.assert_any_call("### 📊 Analyse des missions")
        # Vérifier que les analyses ont été effectuées
        assert mock_st.markdown.call_count > 3

    def test_calculate_mission_revenue_completed(self, mock_mission_active):
        """Test du calcul des revenus pour mission terminée"""
        from datetime import date

        from app.pages_modules.consultant_missions import (
            _calculate_mission_revenue,
        )

        # Modifier la mission pour qu'elle soit terminée
        mock_mission_active.date_fin = date(2024, 6, 30)
        mock_mission_active.en_cours = False

        revenue = _calculate_mission_revenue(mock_mission_active)

        assert revenue > 0  # Devrait calculer des revenus

    def test_calculate_mission_revenue_ongoing(self, mock_mission_active):
        """Test du calcul des revenus pour mission en cours"""
        from app.pages_modules.consultant_missions import (
            _calculate_mission_revenue,
        )

        revenue = _calculate_mission_revenue(mock_mission_active)

        assert revenue > 0  # Devrait calculer des revenus estimés

    def test_build_revenue_data(self, mock_mission_active):
        """Test de construction des données de revenus"""
        from app.pages_modules.consultant_missions import _build_revenue_data

        missions = [mock_mission_active]
        revenue_data, total_revenue = _build_revenue_data(missions)

        assert len(revenue_data) == 1
        assert total_revenue > 0
        assert revenue_data[0]["Mission"] == "Projet Data Analytics"
        assert revenue_data[0]["Client"] == "Société Générale"

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_revenue_statistics(self, mock_st, mock_mission_active):
        """Test de l'affichage des statistiques de revenus"""
        from app.pages_modules.consultant_missions import (
            _display_revenue_statistics,
        )

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3)

        missions = [mock_mission_active]
        total_revenue = 10000

        _display_revenue_statistics(missions, total_revenue)

        # Vérifier que les métriques ont été créées
        assert mock_st.metric.call_count == 3

    @patch("app.pages_modules.consultant_missions._build_revenue_data")
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues_with_data(self, mock_st, mock_build_revenue, mock_mission_active):
        """Test de l'affichage des revenus avec données"""
        from app.pages_modules.consultant_missions import (
            show_missions_revenues,
        )

        # Mock _build_revenue_data
        revenue_data = [
            {
                "Mission": "Test Mission",
                "Client": "Test Client",
                "Revenus": 10000,
                "TJM": 450,
                "Statut": "En cours",
            }
        ]
        mock_build_revenue.return_value = (revenue_data, 10000)

        # Configure mock_st.dataframe to avoid issues
        mock_st.dataframe = MagicMock(return_value=None)

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3)

        missions = [mock_mission_active]
        show_missions_revenues(missions)

        mock_st.markdown.assert_called_with("### 📈 Analyse des revenus")
        # Vérifier que pandas a été importé et utilisé
        mock_st.dataframe.assert_called_once()

    @patch("app.pages_modules.consultant_missions._load_clients_for_mission")
    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_general_info_no_clients(self, mock_st, mock_load_clients):
        """Test du rendu des informations générales sans clients"""
        from app.pages_modules.consultant_missions import (
            _render_mission_general_info,
        )

        # Mock qui retourne un dictionnaire vide
        mock_load_clients.return_value = {}

        result = _render_mission_general_info()

        assert result == (None, None, None, None, None)
        mock_st.warning.assert_called_with("⚠️ Aucun client trouvé. Veuillez créer des clients d'abord.")

    @patch("app.pages_modules.consultant_missions.show_missions_revenues")
    def test_show_missions_analysis_empty_list(self, mock_show_revenues, mock_mission_active):
        """Test de l'analyse des missions avec liste vide"""
        from app.pages_modules.consultant_missions import (
            show_missions_analysis,
        )

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            show_missions_analysis([])

            mock_st.markdown.assert_called_with("### 📊 Analyse des missions")
            mock_st.info.assert_called_with("ℹ️ Aucune mission à analyser")

    def test_show_missions_revenues_empty_list(self):
        """Test de l'affichage des revenus avec liste vide"""
        from app.pages_modules.consultant_missions import (
            show_missions_revenues,
        )

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            show_missions_revenues([])

            mock_st.markdown.assert_called_with("### 📈 Analyse des revenus")
            mock_st.info.assert_called_with("ℹ️ Aucune mission pour analyser les revenus")

    def test_show_missions_revenues_no_revenue_data(self):
        """Test de l'affichage des revenus sans données de revenus"""
        from app.pages_modules.consultant_missions import (
            show_missions_revenues,
        )

        # Mission sans taux journalier
        mission_no_tjm = Mock()
        mission_no_tjm.taux_journalier = None
        mission_no_tjm.tjm = None
        mission_no_tjm.en_cours = True
        mission_no_tjm.date_debut = date(2024, 1, 1)
        mission_no_tjm.date_fin = None

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            show_missions_revenues([mission_no_tjm])

            mock_st.markdown.assert_called_with("### 📈 Analyse des revenus")
            mock_st.info.assert_called_with("ℹ️ Aucune donnée de revenus disponible")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_client_info_with_address_and_contact(self, mock_st, mock_mission_active):
        """Test de l'affichage des informations client avec adresse et contact"""
        from app.pages_modules.consultant_missions import (
            _display_mission_client_info,
        )

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mission avec client ayant adresse et contact
        mock_mission_active.client.adresse = "123 Rue de la Paix"
        mock_mission_active.client.contact_principal = "Jean Dupont"

        _display_mission_client_info(mock_mission_active)

        mock_st.markdown.assert_called_with("#### 🏢 Informations client")
        mock_st.write.assert_any_call("**Adresse :** 123 Rue de la Paix")
        mock_st.write.assert_any_call("**Contact :** Jean Dupont")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_descriptions_with_data(self, mock_st, mock_mission_active):
        """Test de l'affichage des descriptions avec données"""
        from app.pages_modules.consultant_missions import (
            _display_mission_descriptions,
        )

        _display_mission_descriptions(mock_mission_active)

        mock_st.markdown.assert_any_call("#### 📝 Description détaillée")
        mock_st.markdown.assert_any_call("#### 🛠️ Compétences requises")
        # La description complète est affichée, pas tronquée
        mock_st.write.assert_any_call("Développement d'un système d'analyse de données")
        # Les compétences sont passées comme Mock, vérifier qu'elles sont écrites
        assert mock_st.write.call_count >= 2

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_descriptions_no_description(self, mock_st):
        """Test de l'affichage des descriptions sans description"""
        from app.pages_modules.consultant_missions import (
            _display_mission_descriptions,
        )

        mission = Mock()
        mission.description = None
        mission.competences_requises = "Python, SQL"

        _display_mission_descriptions(mission)

        # Ne devrait pas afficher la section description
        mock_st.markdown.assert_called_once_with("#### 🛠️ Compétences requises")
        mock_st.write.assert_called_once_with("Python, SQL")

    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_descriptions_no_competences(self, mock_st):
        """Test de l'affichage des descriptions sans compétences"""
        from app.pages_modules.consultant_missions import (
            _display_mission_descriptions,
        )

        mission = Mock()
        mission.description = "Description test"
        mission.competences_requises = None

        _display_mission_descriptions(mission)

        # Ne devrait pas afficher la section compétences
        mock_st.markdown.assert_called_once_with("#### 📝 Description détaillée")
        mock_st.write.assert_called_once_with("Description test")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_edit_mission_form_exception_handling(self, mock_st):
        """Test de la gestion d'exception dans show_edit_mission_form"""
        from app.pages_modules.consultant_missions import (
            show_edit_mission_form,
        )

        # Mock pour lever une exception
        with patch(
            "app.pages_modules.consultant_missions._load_mission_for_edit",
            side_effect=Exception("Test error"),
        ):
            show_edit_mission_form(1)

            mock_st.error.assert_called_with("❌ Erreur lors du chargement du formulaire de modification: Test error")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_edit_mission_form_mission_not_found(self, mock_st):
        """Test de show_edit_mission_form quand la mission n'est pas trouvée"""
        from app.pages_modules.consultant_missions import (
            show_edit_mission_form,
        )

        # Mock pour retourner None (mission non trouvée)
        with patch(
            "app.pages_modules.consultant_missions._load_mission_for_edit",
            return_value=(None, {}),
        ):
            show_edit_mission_form(999)

            mock_st.error.assert_called_with("❌ Mission introuvable")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_imports_failed(self, mock_st):
        """Test de show_consultant_missions quand les imports ont échoué"""
        from app.pages_modules.consultant_missions import (
            show_consultant_missions,
        )

        # Mock pour que imports_ok soit False
        with patch("app.pages_modules.consultant_missions.imports_ok", False):
            show_consultant_missions(Mock())

            mock_st.error.assert_called_with("❌ Les services de base ne sont pas disponibles")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_no_consultant(self, mock_st):
        """Test de show_consultant_missions sans consultant"""
        from app.pages_modules.consultant_missions import (
            show_consultant_missions,
        )

        show_consultant_missions(None)

        mock_st.error.assert_called_with("❌ Consultant non fourni")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_exception_handling(self, mock_st):
        """Test de la gestion d'exception dans show_consultant_missions"""
        from app.pages_modules.consultant_missions import (
            show_consultant_missions,
        )

        consultant = Mock()
        consultant.id = 1

        # Mock pour lever une exception lors de la récupération des missions
        with patch("app.pages_modules.consultant_missions.get_database_session") as mock_get_session:
            mock_session = Mock()
            mock_get_session.return_value.__enter__.return_value = mock_session
            mock_get_session.return_value.__exit__.return_value = None

            # Lever une exception lors de la requête
            mock_session.query.side_effect = Exception("Database error")

            show_consultant_missions(consultant)

            mock_st.error.assert_called_with("❌ Erreur lors de l'affichage des missions: Database error")
            mock_st.code.assert_called_with("Database error")

    def test_display_mission_period_with_dates(self, mock_mission_active):
        """Test de l'affichage de la période avec dates"""
        from app.pages_modules.consultant_missions import (
            _display_mission_period,
        )

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            _display_mission_period(mock_mission_active)

            mock_st.markdown.assert_called_with("**📅 Période**")
            mock_st.write.assert_any_call("**Début :** 01/01/2024")

    def test_display_mission_period_ongoing(self):
        """Test de l'affichage de la période pour mission en cours"""
        from app.pages_modules.consultant_missions import (
            _display_mission_period,
        )

        mission = Mock()
        mission.date_debut = date(2024, 1, 1)
        mission.date_fin = None
        mission.en_cours = True

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            _display_mission_period(mission)

            mock_st.markdown.assert_called_with("**📅 Période**")
            mock_st.write.assert_any_call("**Début :** 01/01/2024")
            mock_st.write.assert_any_call("**Statut :** 🔄 En cours")

    def test_display_mission_remuneration_with_tjm(self, mock_mission_active):
        """Test de l'affichage de la rémunération avec TJM"""
        from app.pages_modules.consultant_missions import (
            _display_mission_remuneration,
        )

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            _display_mission_remuneration(mock_mission_active)

            mock_st.markdown.assert_called_with("**💰 Rémunération**")
            mock_st.write.assert_called_with("**TJM Mission :** 450€")

    def test_display_mission_remuneration_with_old_rate(self):
        """Test de l'affichage de la rémunération avec ancien taux"""
        from app.pages_modules.consultant_missions import (
            _display_mission_remuneration,
        )

        mission = Mock()
        mission.tjm = None
        mission.taux_journalier = 400
        mission.salaire_mensuel = 5000

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            _display_mission_remuneration(mission)

            mock_st.write.assert_any_call("**TJM (ancien) :** 400€")
            mock_st.write.assert_any_call("**Salaire mensuel :** 5,000€")

    def test_display_mission_info_with_description(self, mock_mission_active):
        """Test de l'affichage des informations avec description"""
        from app.pages_modules.consultant_missions import _display_mission_info

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            _display_mission_info(mock_mission_active)

            mock_st.markdown.assert_called_with("**📊 Informations**")
            mock_st.write.assert_called_with("**Description :** Développement d'un système d'analyse de données...")

    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.joinedload", create=True)
    def test_load_mission_for_edit_found(self, mock_joinedload, mock_get_session, mock_mission_active):
        """Test du chargement de mission existante pour édition"""
        from app.pages_modules.consultant_missions import (
            _load_mission_for_edit,
        )

        # Mock de la session DB
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock joinedload
        mock_joinedload.return_value = Mock()

        # Mock de la requête
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_mission_active

        # Mock des clients
        mock_client = Mock()
        mock_client.id = 1
        mock_client.nom = "Test Client"
        mock_session.query.return_value.all.return_value = [mock_client]

        mission, client_options = _load_mission_for_edit(1)

        assert mission == mock_mission_active
        assert client_options == {1: "Test Client"}

    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.joinedload", create=True)
    def test_load_mission_for_edit_not_found(self, mock_joinedload, mock_get_session):
        """Test du chargement de mission inexistante pour édition"""
        from app.pages_modules.consultant_missions import (
            _load_mission_for_edit,
        )

        # Mock de la session DB
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock joinedload
        mock_joinedload.return_value = Mock()

        # Mock de la requête qui ne trouve rien
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        mission, client_options = _load_mission_for_edit(999)

        assert mission is None
        assert client_options == {}

    @patch("app.pages_modules.consultant_missions.validate_mission_form")
    @patch("app.pages_modules.consultant_missions.update_mission")
    @patch("app.pages_modules.consultant_missions.st")
    def test_handle_mission_update_success(self, mock_st, mock_update, mock_validate):
        """Test de la gestion de mise à jour réussie"""
        from app.pages_modules.consultant_missions import (
            _handle_mission_update,
        )

        mock_validate.return_value = True
        mock_update.return_value = True

        form_data = ("Titre", 1, date.today(), False, None, 450, 5000, "Desc", "Skills")

        _handle_mission_update(1, form_data)

        mock_st.success.assert_called_with("✅ Mission mise à jour avec succès !")
        mock_validate.assert_called_once()
        mock_update.assert_called_once()

    @patch("app.pages_modules.consultant_missions.st")
    def test_handle_mission_deletion(self, mock_st):
        """Test de la gestion de suppression de mission"""
        from app.pages_modules.consultant_missions import (
            _handle_mission_deletion,
        )

        mock_st.checkbox.return_value = True

        with patch("app.pages_modules.consultant_missions.delete_mission", return_value=True):
            _handle_mission_deletion(1)

        mock_st.warning.assert_called_with("⚠️ Cette action est irréversible !")

    @patch("app.pages_modules.consultant_missions.st")
    def test_handle_mission_cancellation(self, mock_st):
        """Test de l'annulation d'édition"""
        from app.pages_modules.consultant_missions import (
            _handle_mission_cancellation,
        )

        _handle_mission_cancellation()

        # Vérifier que la session state a été nettoyée
        assert "edit_mission" not in mock_st.session_state

    @patch("app.pages_modules.consultant_missions.st")
    def test_handle_edit_mission_buttons(self, mock_st):
        """Test de la gestion des boutons du formulaire d'édition"""
        from app.pages_modules.consultant_missions import (
            _handle_edit_mission_buttons,
        )

        # Mock st.columns pour retourner des context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)

        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3)
        mock_st.form_submit_button.side_effect = [True, False, False]  # Submit cliqué

        form_data = ("Titre", 1, date.today(), False, None, 450, 5000, "Desc", "Skills")

        with patch("app.pages_modules.consultant_missions._handle_mission_update") as mock_handle:
            _handle_edit_mission_buttons(1, form_data)

            mock_handle.assert_called_once_with(1, form_data)

    def test_load_mission_for_edit_not_found(self):
        """Test du chargement de mission inexistante pour édition"""
        from app.pages_modules.consultant_missions import (
            _load_mission_for_edit,
        )

        with patch("app.pages_modules.consultant_missions.get_database_session") as mock_get_session, patch(
            "app.pages_modules.consultant_missions.joinedload"
        ):
            mock_session = Mock()
            mock_get_session.return_value.__enter__.return_value = mock_session

            # Mock the query chain properly
            mock_query = Mock()
            mock_session.query.return_value = mock_query
            mock_query.options.return_value = mock_query
            mock_query.filter.return_value = mock_query
            mock_query.first.return_value = None

            result = _load_mission_for_edit(999)

            assert result == (None, {})

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues_no_data(self, mock_st):
        """Test de show_missions_revenues sans données"""
        from app.pages_modules.consultant_missions import (
            show_missions_revenues,
        )

        # Appeler avec une liste vide
        show_missions_revenues([])

        # Vérifier les appels pour le cas sans données
        mock_st.info.assert_called_with("ℹ️ Aucune mission pour analyser les revenus")
        mock_st.subheader.assert_not_called()  # Pas de sous-titres si pas de données

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_edit_mission_form_mission_not_found(self, mock_st):
        """Test de show_edit_mission_form quand la mission n'est pas trouvée"""
        from app.pages_modules.consultant_missions import (
            show_edit_mission_form,
        )

        # Mock pour retourner None (mission non trouvée)
        with patch(
            "app.pages_modules.consultant_missions._load_mission_for_edit",
            return_value=(None, {}),
        ):
            show_edit_mission_form(999)

            mock_st.error.assert_called_with("❌ Mission introuvable")
