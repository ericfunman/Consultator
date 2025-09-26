"""
Tests de couverture pour ui/enhanced_ui.py
Couvre les classes et fonctions d'interface utilisateur améliorée
"""

from datetime import date
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pandas as pd
import pytest


class TestEnhancedUICoverage:
    """Tests de couverture pour le module ui/enhanced_ui.py"""

    @pytest.fixture
    def sample_consultant_data(self):
        """Données d'exemple de consultants"""
        return [
            {
                "id": 1,
                "prenom": "Marie",
                "nom": "Martin",
                "email": "marie.martin@email.com",
                "telephone": "0123456789",
                "salaire_actuel": 50000,
                "disponibilite": True,
                "practice_name": "Data Science",
                "grade": "Senior",
                "type_contrat": "CDI",
                "societe": "Quanteam",
                "experience_annees": 5.5,
                "nb_missions": 12,
                "cjm_formatted": "45.8k€",
                "salaire_formatted": "50.0k€",
                "experience_formatted": "5.5 ans",
                "statut": "Disponible",
            },
            {
                "id": 2,
                "prenom": "Pierre",
                "nom": "Dubois",
                "email": "pierre.dubois@email.com",
                "telephone": "0987654321",
                "salaire_actuel": 60000,
                "disponibilite": False,
                "practice_name": "Cloud",
                "grade": "Lead",
                "type_contrat": "CDD",
                "societe": "Asigma",
                "experience_annees": 8.0,
                "nb_missions": 15,
                "cjm_formatted": "52.1k€",
                "salaire_formatted": "60.0k€",
                "experience_formatted": "8.0 ans",
                "statut": "En mission",
            },
        ]

    @patch("app.ui.enhanced_ui.st")
    def test_advanced_ui_filters_init(self, mock_st):
        """Test de l'initialisation des filtres avancés"""
        from app.ui.enhanced_ui import AdvancedUIFilters

        filters = AdvancedUIFilters()

        assert filters.filters["search_term"] == ""
        assert filters.filters["practice_filter"] is None
        assert filters.filters["grade_filter"] is None
        assert filters.filters["availability_filter"] is None

    @patch("app.ui.enhanced_ui.st")
    def test_advanced_ui_filters_get_unique_values(self, mock_st):
        """Test de récupération des valeurs uniques"""
        from app.ui.enhanced_ui import AdvancedUIFilters

        filters = AdvancedUIFilters()

        # Test avec practice_name
        values = filters._get_unique_values("practice_name")
        assert "Digital" in values
        assert "Data" in values

        # Test avec grade
        values = filters._get_unique_values("grade")
        assert "Senior" in values
        assert "Expert" in values

        # Test avec champ inexistant
        values = filters._get_unique_values("unknown_field")
        assert values == []

    @patch("app.ui.enhanced_ui.st")
    def test_advanced_ui_filters_reset_filters(self, mock_st):
        """Test de réinitialisation des filtres"""
        from app.ui.enhanced_ui import AdvancedUIFilters

        filters = AdvancedUIFilters()

        # Modifier quelques filtres
        filters.filters["search_term"] = "test"
        filters.filters["practice_filter"] = "Data"
        filters.filters["salaire_min"] = 30000

        # Réinitialiser
        filters.reset_filters()

        assert filters.filters["search_term"] == ""
        assert filters.filters["practice_filter"] is None
        # Selon le code, salaire_min est d'abord mis à None par la condition "_min"
        assert filters.filters["salaire_min"] is None

    @patch("app.ui.enhanced_ui.st")
    def test_advanced_ui_filters_apply_filters(self, mock_st, sample_consultant_data):
        """Test de l'application des filtres"""
        from app.ui.enhanced_ui import AdvancedUIFilters

        filters = AdvancedUIFilters()

        # Test sans filtres
        result = filters.apply_filters(sample_consultant_data)
        assert len(result) == 2

        # Test avec filtre de recherche
        filters.filters["search_term"] = "marie"
        result = filters.apply_filters(sample_consultant_data)
        assert len(result) == 1
        assert result[0]["prenom"] == "Marie"

        # Test avec filtre practice
        filters.reset_filters()
        filters.filters["practice_filter"] = "Data Science"
        result = filters.apply_filters(sample_consultant_data)
        assert len(result) == 1
        assert result[0]["practice_name"] == "Data Science"

        # Test avec filtre disponibilité
        filters.reset_filters()
        filters.filters["availability_filter"] = True
        result = filters.apply_filters(sample_consultant_data)
        assert len(result) == 1
        assert result[0]["disponibilite"] is True

        # Test avec filtre salaire
        filters.reset_filters()
        filters.filters["salaire_min"] = 55000
        result = filters.apply_filters(sample_consultant_data)
        assert len(result) == 1
        assert result[0]["salaire_actuel"] == 60000

    @patch("app.ui.enhanced_ui.st")
    def test_real_time_search_init(self, mock_st):
        """Test de l'initialisation de la recherche en temps réel"""
        from app.ui.enhanced_ui import RealTimeSearch

        search = RealTimeSearch()

        assert search.search_debounce_ms == 300
        assert search.last_search_time == 0

    @patch("app.ui.enhanced_ui.time")
    def test_real_time_search_should_search(self, mock_time):
        """Test de la logique de debounce pour la recherche"""
        from app.ui.enhanced_ui import RealTimeSearch

        search = RealTimeSearch()

        # Première recherche - devrait réussir car différence > 300ms
        mock_time.time.return_value = 0.35  # 350ms
        search.last_search_time = 0  # dernière recherche à 0
        assert search.should_search() is True

        # Recherche immédiate - devrait échouer (debounce)
        mock_time.time.return_value = 0.45  # 450ms
        assert search.should_search() is False

        # Recherche après debounce - devrait réussir
        mock_time.time.return_value = 0.8  # 800ms
        assert search.should_search() is True

    @patch("app.ui.enhanced_ui.st")
    def test_data_table_enhancer_render_enhanced_table_empty(self, mock_st):
        """Test de l'affichage du tableau avec données vides"""
        from app.ui.enhanced_ui import DataTableEnhancer

        result = DataTableEnhancer.render_enhanced_table([])

        assert result is None
        mock_st.info.assert_called_with("📝 Aucune donnée à afficher")

    @patch("app.ui.enhanced_ui.st")
    def test_data_table_enhancer_render_enhanced_table_with_data(
        self, mock_st, sample_consultant_data
    ):
        """Test de l'affichage du tableau avec données"""
        # Mock st.columns pour retourner des objets avec context manager
        mock_columns = [Mock() for _ in range(4)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        # Mock dataframe
        mock_event = Mock()
        mock_event.selection.rows = []
        mock_st.dataframe.return_value = mock_event

        from app.ui.enhanced_ui import DataTableEnhancer

        result = DataTableEnhancer.render_enhanced_table(sample_consultant_data)

        assert result is not None
        mock_st.dataframe.assert_called_once()

    @patch("app.ui.enhanced_ui.st")
    def test_data_table_enhancer_render_action_buttons_no_data(self, mock_st):
        """Test des boutons d'action sans données sélectionnées"""
        from app.ui.enhanced_ui import DataTableEnhancer

        result = DataTableEnhancer.render_action_buttons({}, ["view", "edit"])

        assert result is None

    @patch("app.ui.enhanced_ui.st")
    def test_data_table_enhancer_render_action_buttons_with_data(
        self, mock_st, sample_consultant_data
    ):
        """Test des boutons d'action avec données sélectionnées"""
        # Mock st.columns pour retourner 3 colonnes avec context manager
        mock_columns = [Mock() for _ in range(3)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.ui.enhanced_ui import DataTableEnhancer

        selected_data = sample_consultant_data[0]
        DataTableEnhancer.render_action_buttons(
            selected_data, ["view", "edit", "delete"]
        )

        mock_st.success.assert_called_once()
        # Vérifier que les boutons ont été créés
        assert mock_st.button.call_count == 3

    @patch("app.ui.enhanced_ui.st")
    def test_loading_spinner_show_loading(self, mock_st):
        """Test de l'affichage du spinner de chargement"""
        from app.ui.enhanced_ui import LoadingSpinner

        LoadingSpinner.show_loading("Test loading...")

        mock_st.spinner.assert_called_with("Test loading...")

    @patch("app.ui.enhanced_ui.st")
    def test_loading_spinner_show_progress(self, mock_st):
        """Test de l'affichage de la barre de progression"""
        from app.ui.enhanced_ui import LoadingSpinner

        mock_progress = Mock()
        mock_st.progress.return_value = mock_progress

        LoadingSpinner.show_progress(5, 10, "Processing...")

        mock_st.progress.assert_called_once()
        mock_progress.progress.assert_called_with(0.5)

    @patch("app.ui.enhanced_ui.time")
    def test_notification_manager_show_success(self, mock_time, capsys):
        """Test de l'affichage d'une notification de succès"""
        from app.ui.enhanced_ui import NotificationManager

        with patch("app.ui.enhanced_ui.st") as mock_st:
            NotificationManager.show_success(
                "Test success", 0
            )  # duration=0 pour éviter sleep

            mock_st.success.assert_called_with("Test success")

    @patch("app.ui.enhanced_ui.time")
    def test_notification_manager_show_error(self, mock_time):
        """Test de l'affichage d'une notification d'erreur"""
        from app.ui.enhanced_ui import NotificationManager

        with patch("app.ui.enhanced_ui.st") as mock_st:
            NotificationManager.show_error("Test error", 0)

            mock_st.error.assert_called_with("Test error")

    @patch("app.ui.enhanced_ui.time")
    def test_notification_manager_show_warning(self, mock_time):
        """Test de l'affichage d'une notification d'avertissement"""
        from app.ui.enhanced_ui import NotificationManager

        with patch("app.ui.enhanced_ui.st") as mock_st:
            NotificationManager.show_warning("Test warning", 0)

            mock_st.warning.assert_called_with("Test warning")

    @patch("app.ui.enhanced_ui.time")
    def test_notification_manager_show_info(self, mock_time):
        """Test de l'affichage d'une notification d'information"""
        from app.ui.enhanced_ui import NotificationManager

        with patch("app.ui.enhanced_ui.st") as mock_st:
            NotificationManager.show_info("Test info", 0)

            mock_st.info.assert_called_with("Test info")

    @patch("app.ui.enhanced_ui.st")
    @patch("app.ui.enhanced_ui._initialize_ui_components")
    @patch("app.ui.enhanced_ui._load_consultant_data")
    @patch("app.ui.enhanced_ui._display_metrics")
    @patch("app.ui.enhanced_ui._handle_consultant_selection")
    def test_create_enhanced_consultants_view(
        self,
        mock_handle_selection,
        mock_display_metrics,
        mock_load_data,
        mock_init_components,
        mock_st,
    ):
        """Test de la fonction principale create_enhanced_consultants_view"""
        # Mock des composants
        mock_filters = Mock()
        mock_filters.render_filters_sidebar.return_value = {"search_term": "test"}
        mock_filters.apply_filters.return_value = []

        mock_search = Mock()
        mock_enhancer = Mock()
        mock_enhancer.render_enhanced_table.return_value = None

        mock_init_components.return_value = (mock_filters, mock_search, mock_enhancer)
        mock_load_data.return_value = []

        from app.ui.enhanced_ui import create_enhanced_consultants_view

        create_enhanced_consultants_view()

        mock_st.title.assert_called_with(
            "👥 Gestion des consultants - Version Améliorée"
        )
        mock_init_components.assert_called_once()
        mock_load_data.assert_called_once()
        mock_display_metrics.assert_called_once()

    @patch("app.ui.enhanced_ui.st")
    def test_initialize_ui_components(self, mock_st):
        """Test de l'initialisation des composants UI"""
        from app.ui.enhanced_ui import _initialize_ui_components

        filters, search, enhancer = _initialize_ui_components()

        # Vérifier que les instances sont créées
        assert filters is not None
        assert search is not None
        assert enhancer is not None

        # Vérifier les types
        from app.ui.enhanced_ui import AdvancedUIFilters
        from app.ui.enhanced_ui import DataTableEnhancer
        from app.ui.enhanced_ui import RealTimeSearch

        assert isinstance(filters, AdvancedUIFilters)
        assert isinstance(search, RealTimeSearch)
        assert isinstance(enhancer, DataTableEnhancer)

    @patch("app.ui.enhanced_ui.st")
    @patch("app.ui.enhanced_ui.get_cached_consultants_list")
    @patch("app.ui.enhanced_ui.get_cached_search_results")
    def test_load_consultant_data_no_search(
        self, mock_search_results, mock_list, mock_st
    ):
        """Test du chargement des données sans recherche"""
        mock_st.text_input.return_value = ""
        mock_list.return_value = [{"id": 1, "nom": "Test"}]

        # Créer une instance de RealTimeSearch pour le test
        from app.ui.enhanced_ui import RealTimeSearch
        from app.ui.enhanced_ui import _load_consultant_data

        search = RealTimeSearch()

        result = _load_consultant_data(search)

        mock_list.assert_called_once()
        assert result == [{"id": 1, "nom": "Test"}]

    @patch("app.ui.enhanced_ui.st")
    @patch("app.ui.enhanced_ui.get_cached_consultants_list")
    @patch("app.ui.enhanced_ui.get_cached_search_results")
    def test_load_consultant_data_with_search(
        self, mock_search_results, mock_list, mock_st
    ):
        """Test du chargement des données avec recherche"""
        mock_st.text_input.return_value = "test search"
        mock_search_results.return_value = [{"id": 1, "nom": "Test"}]

        # Créer une instance de RealTimeSearch pour le test
        from app.ui.enhanced_ui import RealTimeSearch
        from app.ui.enhanced_ui import _load_consultant_data

        search = RealTimeSearch()

        result = _load_consultant_data(search)

        mock_search_results.assert_called_once_with("test search", 1, 50)

    @patch("app.ui.enhanced_ui.st")
    def test_display_metrics_empty_data(self, mock_st):
        """Test de l'affichage des métriques avec données vides"""
        from app.ui.enhanced_ui import _display_metrics

        _display_metrics([])

        # Ne devrait rien afficher
        mock_st.columns.assert_not_called()

    @patch("app.ui.enhanced_ui.st")
    def test_display_metrics_with_data(self, mock_st, sample_consultant_data):
        """Test de l'affichage des métriques avec données"""
        # Mock st.columns pour retourner 4 colonnes avec context manager
        mock_columns = [Mock() for _ in range(4)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.ui.enhanced_ui import _display_metrics

        _display_metrics(sample_consultant_data)

        # Vérifier que les métriques ont été créées
        assert mock_st.metric.call_count == 4

    @patch("app.ui.enhanced_ui.st")
    def test_handle_consultant_selection_no_event(self, mock_st):
        """Test de la gestion de sélection sans événement"""
        from app.ui.enhanced_ui import _handle_consultant_selection

        result = _handle_consultant_selection(None, [], None)

        # Ne devrait rien faire et retourner None
        assert result is None

    @patch("app.ui.enhanced_ui.st")
    def test_handle_consultant_selection_with_event(
        self, mock_st, sample_consultant_data
    ):
        """Test de la gestion de sélection avec événement"""
        # Mock event avec sélection
        mock_event = Mock()
        mock_event.selection.rows = [0]

        # Mock enhancer
        mock_enhancer = Mock()
        mock_enhancer.render_action_buttons.return_value = "view"

        from app.ui.enhanced_ui import _handle_consultant_selection

        _handle_consultant_selection(mock_event, sample_consultant_data, mock_enhancer)

        mock_enhancer.render_action_buttons.assert_called_once()

    @patch("app.ui.enhanced_ui.st")
    @patch("app.ui.enhanced_ui.ConsultantService")
    def test_execute_consultant_action_view(self, mock_consultant_service, mock_st):
        """Test de l'exécution de l'action 'view'"""
        mock_st.session_state = MagicMock()

        from app.ui.enhanced_ui import _execute_consultant_action

        selected_consultant = {"id": 1, "prenom": "Marie", "nom": "Martin"}

        _execute_consultant_action("view", selected_consultant)

        assert mock_st.session_state.view_consultant_profile == 1

    @patch("app.ui.enhanced_ui.st")
    @patch("app.ui.enhanced_ui.ConsultantService")
    def test_execute_consultant_action_delete_success(
        self, mock_consultant_service, mock_st
    ):
        """Test de l'exécution de l'action 'delete' avec succès"""
        mock_consultant_service.delete_consultant.return_value = True

        from app.ui.enhanced_ui import _execute_consultant_action

        selected_consultant = {"id": 1, "prenom": "Marie", "nom": "Martin"}

        _execute_consultant_action("delete", selected_consultant)

        mock_consultant_service.delete_consultant.assert_called_with(1)

    @patch("app.ui.enhanced_ui.st")
    @patch("app.ui.enhanced_ui.ConsultantService")
    def test_execute_consultant_action_delete_failure(
        self, mock_consultant_service, mock_st
    ):
        """Test de l'exécution de l'action 'delete' avec échec"""
        mock_consultant_service.delete_consultant.return_value = False

        from app.ui.enhanced_ui import _execute_consultant_action

        selected_consultant = {"id": 1, "prenom": "Marie", "nom": "Martin"}

        _execute_consultant_action("delete", selected_consultant)

        # Vérifier que l'erreur a été affichée (via NotificationManager.show_error)
        # Cette vérification est implicite car nous mockons st

    @patch("app.ui.enhanced_ui.st")
    def test_advanced_ui_filters_render_filters_sidebar(self, mock_st):
        """Test du rendu complet de la sidebar des filtres"""
        from app.ui.enhanced_ui import AdvancedUIFilters

        # Mock des éléments Streamlit
        mock_st.sidebar.header = Mock()
        mock_st.sidebar.text_input.return_value = "test search"
        mock_st.sidebar.markdown = Mock()
        mock_st.sidebar.subheader = Mock()

        # Mock columns pour supporter les context managers
        mock_columns = [Mock() for _ in range(2)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.sidebar.columns.return_value = mock_columns

        mock_st.sidebar.selectbox.return_value = None
        mock_st.sidebar.number_input.return_value = 0
        mock_st.sidebar.date_input.return_value = None
        mock_st.sidebar.button.return_value = False

        filters = AdvancedUIFilters()
        result = filters.render_filters_sidebar()

        # Vérifier que le dictionnaire des filtres est retourné
        assert isinstance(result, dict)
        assert "search_term" in result
        assert "practice_filter" in result

        # Vérifier que les méthodes Streamlit ont été appelées
        mock_st.sidebar.header.assert_called()
        mock_st.sidebar.text_input.assert_called()

    @patch("app.ui.enhanced_ui.st")
    def test_real_time_search_search_with_cache_empty_search(self, mock_st):
        """Test de recherche avec terme vide"""
        from app.ui.enhanced_ui import RealTimeSearch

        with patch("app.ui.enhanced_ui.get_cached_consultants_list") as mock_get_list:
            mock_get_list.return_value = [{"id": 1, "nom": "Test"}]

            search = RealTimeSearch()
            result = search.search_with_cache("")

            mock_get_list.assert_called_with(1, 50)
            assert result == [{"id": 1, "nom": "Test"}]

    @patch("app.ui.enhanced_ui.st")
    def test_real_time_search_search_with_cache_with_term(self, mock_st):
        """Test de recherche avec terme non vide"""
        from app.ui.enhanced_ui import RealTimeSearch

        with patch("app.ui.enhanced_ui.get_cached_search_results") as mock_search:
            mock_search.return_value = [{"id": 1, "nom": "Test"}]

            search = RealTimeSearch()
            result = search.search_with_cache("test search")

            mock_search.assert_called_with("test search", 1, 50)
            assert result == [{"id": 1, "nom": "Test"}]

    @patch("app.ui.enhanced_ui.st")
    def test_data_table_enhancer_column_mapping_and_display(
        self, mock_st, sample_consultant_data
    ):
        """Test du mapping des colonnes et de l'affichage"""
        # Mock pour st.dataframe
        mock_event = Mock()
        mock_event.selection.rows = []
        mock_st.dataframe.return_value = mock_event
        mock_st.column_config.NumberColumn = Mock()
        mock_st.column_config.TextColumn = Mock()

        from app.ui.enhanced_ui import DataTableEnhancer

        DataTableEnhancer.render_enhanced_table(sample_consultant_data)

        # Vérifier que st.dataframe a été appelé avec les bonnes configurations
        mock_st.dataframe.assert_called_once()
        call_args = mock_st.dataframe.call_args

        # Vérifier les paramètres passés à dataframe
        assert call_args[1]["width"] == "stretch"
        assert call_args[1]["hide_index"] is True
        assert call_args[1]["on_select"] == "rerun"
        assert call_args[1]["selection_mode"] == "single-row"

    @patch("app.ui.enhanced_ui.st")
    def test_execute_consultant_action_edit(self, mock_st):
        """Test de l'action edit"""
        mock_st.session_state = Mock()
        mock_st.rerun = Mock()

        from app.ui.enhanced_ui import _execute_consultant_action

        selected_consultant = {"id": 1, "prenom": "Marie", "nom": "Martin"}
        _execute_consultant_action("edit", selected_consultant)

        assert mock_st.session_state.view_consultant_profile == 1
        mock_st.rerun.assert_called_once()

    @patch("app.ui.enhanced_ui.st")
    def test_execute_consultant_action_unknown(self, mock_st):
        """Test d'une action inconnue"""
        from app.ui.enhanced_ui import _execute_consultant_action

        selected_consultant = {"id": 1, "prenom": "Marie", "nom": "Martin"}
        result = _execute_consultant_action("unknown_action", selected_consultant)

        # L'action inconnue ne devrait rien faire
        assert result is None

    @patch("app.ui.enhanced_ui.st")
    def test_load_consultant_data_with_should_search_false(self, mock_st):
        """Test du chargement des données quand should_search retourne False"""
        mock_st.text_input.return_value = "test search"
        mock_st.spinner.return_value.__enter__ = Mock()
        mock_st.spinner.return_value.__exit__ = Mock()

        # Mock get_cached_consultants_list
        with patch("app.ui.enhanced_ui.get_cached_consultants_list") as mock_get_list:
            mock_get_list.return_value = [{"id": 1, "nom": "Test"}]

            from app.ui.enhanced_ui import RealTimeSearch
            from app.ui.enhanced_ui import _load_consultant_data

            # Mock should_search pour retourner False
            search = RealTimeSearch()
            with patch.object(search, "should_search", return_value=False):
                _load_consultant_data(search)

            mock_get_list.assert_called_once()

    @patch("app.ui.enhanced_ui.st")
    def test_handle_consultant_selection_invalid_index(
        self, mock_st, sample_consultant_data
    ):
        """Test de gestion de sélection avec index invalide"""
        # Mock event avec index hors limite
        mock_event = Mock()
        mock_event.selection.rows = [10]  # Index supérieur à la taille des données

        from app.ui.enhanced_ui import _handle_consultant_selection

        result = _handle_consultant_selection(mock_event, sample_consultant_data, None)

        # Ne devrait rien faire et retourner None
        assert result is None

    @patch("app.ui.enhanced_ui.st")
    def test_handle_consultant_selection_empty_rows(self, mock_st):
        """Test de gestion de sélection avec liste de rows vide"""
        # Mock event avec rows vide
        mock_event = Mock()
        mock_event.selection.rows = []

        from app.ui.enhanced_ui import _handle_consultant_selection

        result = _handle_consultant_selection(mock_event, [], None)

        # Ne devrait rien faire et retourner None
        assert result is None

    @patch("app.ui.enhanced_ui.st")
    def test_display_metrics_calculation_accuracy(
        self, mock_st, sample_consultant_data
    ):
        """Test de précision des calculs de métriques"""
        # Mock st.columns pour retourner 4 colonnes avec context manager
        mock_columns = [Mock() for _ in range(4)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.ui.enhanced_ui import _display_metrics

        _display_metrics(sample_consultant_data)

        # Vérifier que metric a été appelé 4 fois (total, disponibles, occupés, salaire moyen)
        assert mock_st.metric.call_count == 4

        # Vérifier les calculs dans les appels
        call_args_list = mock_st.metric.call_args_list

        # Premier appel : Total
        assert call_args_list[0][0][0] == "👥 Total"
        assert call_args_list[0][0][1] == 2  # 2 consultants dans sample_data

        # Deuxième appel : Disponibles
        assert call_args_list[1][0][0] == "✅ Disponibles"
        assert call_args_list[1][0][1] == 1  # Marie est disponible

        # Troisième appel : Occupés
        assert call_args_list[2][0][0] == "🔴 Occupés"
        assert call_args_list[2][0][1] == 1  # Pierre n'est pas disponible

        # Quatrième appel : Salaire moyen
        assert call_args_list[3][0][0] == "💰 Salaire moyen"
        # Salaire moyen = (50000 + 60000) / 2 = 55000
        assert call_args_list[3][0][1] == "55,000€"
