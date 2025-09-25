"""
Tests de couverture pour consultant_missions.py
"""

import pytest
from unittest.mock import Mock, patch
from datetime import date


class TestConsultantMissionsCoverage:
    """Tests de couverture pour le module consultant_missions.py"""

    @pytest.fixture
    def mock_consultant(self):
        """Mock d'un consultant"""
        consultant = Mock()
        consultant.id = 1
        consultant.prenom = "Marie"
        consultant.nom = "Martin"
        return consultant

    @pytest.fixture
    def mock_client(self):
        """Mock d'un client"""
        client = Mock()
        client.id = 1
        client.nom = "Société Générale"
        return client

    @pytest.fixture
    def mock_mission_active(self, mock_client):
        """Mock d'une mission active"""
        mission = Mock()
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
        return mission

    @patch("app.pages_modules.consultant_missions.show_missions_statistics")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_with_data(self, mock_st, mock_get_session, mock_show_stats, mock_consultant, mock_mission_active, mocker):
        """Test de l'affichage des missions avec données"""
        # Set imports_ok to True
        mocker.patch("app.pages_modules.consultant_missions.imports_ok", True)
        
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock the SQLAlchemy query chain properly
        mock_query = Mock()
        mock_options = Mock()
        mock_filtered = Mock()
        mock_ordered = Mock()

        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_options
        mock_options.filter.return_value = mock_filtered
        mock_filtered.order_by.return_value = mock_ordered
        mock_ordered.all.return_value = [mock_mission_active]

        # Mock show_missions_statistics to do nothing
        mock_show_stats.return_value = None

        from app.pages_modules.consultant_missions import show_consultant_missions
        show_consultant_missions(mock_consultant)

        # Vérifier que st.markdown a été appelé pour le titre
        mock_st.markdown.assert_called_with("### 🚀 Missions")

    @patch("app.pages_modules.consultant_missions.joinedload")
    @patch("app.pages_modules.consultant_missions.show_add_mission_form")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_no_data(self, mock_st, mock_get_session, mock_show_add, mock_joinedload, mock_consultant):
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

        from app.pages_modules.consultant_missions import show_consultant_missions
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
            date_fin=date(2024, 6, 30)
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
            date_fin=None
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
            date_fin=date(2024, 1, 1)
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
            date_fin=None
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

        from app.pages_modules.consultant_missions import show_missions_statistics

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

        from app.pages_modules.consultant_missions import show_missions_analysis

        missions = [mock_mission_active]
        show_missions_analysis(missions)

        mock_st.markdown.assert_any_call("### 📊 Analyse des missions")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues(self, mock_st, mock_mission_active):
        """Test de l'analyse des revenus"""
        # Mock st.columns pour les statistiques
        mock_columns = [Mock() for _ in range(3)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.pages_modules.consultant_missions import show_missions_revenues

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

        from app.pages_modules.consultant_missions import show_mission_full_details

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
        from app.pages_modules.consultant_missions import show_missions_statistics

        missions = []
        show_missions_statistics(missions)

        # Vérifier que rien n'est affiché pour la liste vide (fonction retourne tôt)
        mock_st.info.assert_not_called()

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_analysis_empty_list(self, mock_st):
        """Test de l'analyse avec liste vide"""
        from app.pages_modules.consultant_missions import show_missions_analysis

        missions = []
        show_missions_analysis(missions)

        # Vérifier que st.info a été appelé pour la liste vide
        mock_st.info.assert_called_with("ℹ️ Aucune mission à analyser")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_missions_revenues_empty_list(self, mock_st):
        """Test de l'analyse des revenus avec liste vide"""
        from app.pages_modules.consultant_missions import show_missions_revenues

        missions = []
        show_missions_revenues(missions)

        # Vérifier que st.info a été appelé pour la liste vide
        mock_st.info.assert_called_with("ℹ️ Aucune mission pour analyser les revenus")

    @patch("app.pages_modules.consultant_missions.imports_ok", False)
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_imports_failed(self, mock_st, mock_consultant):
        """Test de l'affichage quand les imports ont échoué"""
        from app.pages_modules.consultant_missions import show_consultant_missions

        show_consultant_missions(mock_consultant)

        mock_st.error.assert_called_once_with("❌ Les services de base ne sont pas disponibles")

    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_no_consultant(self, mock_st):
        """Test de l'affichage sans consultant fourni"""
        from app.pages_modules.consultant_missions import show_consultant_missions

        show_consultant_missions(None)

        mock_st.error.assert_called_once_with("❌ Consultant non fourni")

    @patch("app.pages_modules.consultant_missions.joinedload")
    @patch("app.pages_modules.consultant_missions.show_add_mission_form")
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_show_consultant_missions_empty_list(self, mock_st, mock_get_session, mock_show_add, mock_joinedload, mock_consultant):
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

        from app.pages_modules.consultant_missions import show_consultant_missions
        show_consultant_missions(mock_consultant)

        # Vérifier que st.info a été appelé pour les missions vides
        mock_st.info.assert_called_with("ℹ️ Aucune mission enregistrée pour ce consultant")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_missing_title(self, mock_st):
        """Test de validation de formulaire avec titre manquant"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form("", 1, date(2024, 1, 1), False, date(2024, 1, 2))

        assert result is False
        mock_st.error.assert_called_with("❌ Le titre de la mission est obligatoire")

    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_missing_client(self, mock_st):
        """Test de validation de formulaire avec client manquant"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form("Test Mission", None, date(2024, 1, 1), False, date(2024, 1, 2))

        assert result is False
        mock_st.error.assert_called_with("❌ Le client est obligatoire")



    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_invalid_dates(self, mock_st):
        """Test de validation de formulaire avec dates invalides"""
        from app.pages_modules.consultant_missions import validate_mission_form

        result = validate_mission_form("Test Mission", 1, date(2024, 1, 15), False, date(2024, 1, 10))

        assert result is False
        mock_st.error.assert_called_with("❌ La date de fin doit être postérieure à la date de début")

    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_create_mission_database_error(self, mock_st, mock_get_session):
        """Test de création de mission avec erreur de base de données"""
        from app.pages_modules.consultant_missions import create_mission

        # Mock de la session qui lève une exception
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.add.side_effect = Exception("Database error")

        data = {
            "titre": "Test Mission",
            "client_id": 1,
            "date_debut": date.today(),
            "date_fin": None,
            "en_cours": True,
            "taux_journalier": 450,
            "tjm": 450,
            "salaire_mensuel": 0,
            "description": "Test",
            "competences_requises": "Python"
        }

        result = create_mission(1, data)

        assert result is False
        mock_st.error.assert_called_with("❌ Erreur lors de la création de la mission: Database error")

    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_update_mission_not_found(self, mock_st, mock_get_session):
        """Test de mise à jour de mission inexistante"""
        from app.pages_modules.consultant_missions import update_mission

        # Mock de la session qui ne trouve pas la mission
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        data = {
            "titre": "Updated Mission",
            "client_id": 1,
            "date_debut": date.today(),
            "date_fin": None,
            "en_cours": True,
            "taux_journalier": 450,
            "salaire_mensuel": 0,
            "description": "Updated",
            "competences_requises": "Python"
        }

        result = update_mission(999, data)

        assert result is False
        mock_st.error.assert_called_with("❌ Mission introuvable")

    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_delete_mission_not_found(self, mock_st, mock_get_session):
        """Test de suppression de mission inexistante"""
        from app.pages_modules.consultant_missions import delete_mission

        # Mock de la session qui ne trouve pas la mission
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = delete_mission(999)

        assert result is False
        mock_st.error.assert_called_with("❌ Mission introuvable")

    @patch("app.pages_modules.consultant_missions._load_clients_for_mission")
    @patch("app.pages_modules.consultant_missions.st")
    def test_render_mission_general_info_no_clients(self, mock_st, mock_load_clients):
        """Test du rendu des informations générales sans clients"""
        from app.pages_modules.consultant_missions import _render_mission_general_info

        # Mock qui retourne un dictionnaire vide
        mock_load_clients.return_value = {}

        result = _render_mission_general_info()

        assert result == (None, None, None, None, None)
        mock_st.warning.assert_called_with("⚠️ Aucun client trouvé. Veuillez créer des clients d'abord.")

    @patch("app.pages_modules.consultant_missions.show_missions_revenues")
    def test_show_missions_analysis_empty_list(self, mock_show_revenues, mock_mission_active):
        """Test de l'analyse des missions avec liste vide"""
        from app.pages_modules.consultant_missions import show_missions_analysis

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            show_missions_analysis([])

            mock_st.markdown.assert_called_with("### 📊 Analyse des missions")
            mock_st.info.assert_called_with("ℹ️ Aucune mission à analyser")

    def test_show_missions_revenues_empty_list(self):
        """Test de l'affichage des revenus avec liste vide"""
        from app.pages_modules.consultant_missions import show_missions_revenues

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            show_missions_revenues([])

            mock_st.markdown.assert_called_with("### 📈 Analyse des revenus")
            mock_st.info.assert_called_with("ℹ️ Aucune mission pour analyser les revenus")

    def test_display_mission_period_with_dates(self, mock_mission_active):
        """Test de l'affichage de la période avec dates"""
        from app.pages_modules.consultant_missions import _display_mission_period

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            _display_mission_period(mock_mission_active)

            mock_st.markdown.assert_called_with("**📅 Période**")
            mock_st.write.assert_any_call("**Début :** 01/01/2024")

    def test_display_mission_period_ongoing(self):
        """Test de l'affichage de la période pour mission en cours"""
        from app.pages_modules.consultant_missions import _display_mission_period

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
        from app.pages_modules.consultant_missions import _display_mission_remuneration

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            _display_mission_remuneration(mock_mission_active)

            mock_st.markdown.assert_called_with("**💰 Rémunération**")
            mock_st.write.assert_called_with("**TJM Mission :** 450€")

    def test_display_mission_remuneration_with_old_rate(self):
        """Test de l'affichage de la rémunération avec ancien taux"""
        from app.pages_modules.consultant_missions import _display_mission_remuneration

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

    def test_display_mission_actions(self, mock_mission_active):
        """Test de l'affichage des actions de mission"""
        from app.pages_modules.consultant_missions import _display_mission_actions

        with patch("app.pages_modules.consultant_missions.st") as mock_st:
            # Mock st.columns to return mock column objects that support context manager
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

            _display_mission_actions(mock_mission_active)

            # Vérifie que les boutons sont créés
            assert mock_st.button.called

    def test_load_mission_for_edit_not_found(self):
        """Test du chargement de mission inexistante pour édition"""
        from app.pages_modules.consultant_missions import _load_mission_for_edit

        with patch("app.pages_modules.consultant_missions.get_database_session") as mock_get_session, \
             patch("app.pages_modules.consultant_missions.joinedload"):
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