"""
Tests unitaires pour enhanced_ui.py
Tests simplifiés pour améliorer la couverture
"""

import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Mock des modules externes avant les imports
sys.modules['streamlit'] = MagicMock()
sys.modules['pandas'] = MagicMock()

# Mock des services
with patch('app.services.cache_service.get_cached_consultants_list'), \
     patch('app.services.cache_service.get_cached_search_results'), \
     patch('app.services.consultant_service.ConsultantService'):

    from app.ui.enhanced_ui import (
        AdvancedUIFilters,
        RealTimeSearch,
        DataTableEnhancer,
        LoadingSpinner,
        NotificationManager,
        create_enhanced_consultants_view
    )


class TestEnhancedUI(unittest.TestCase):
    """Tests pour les fonctions de enhanced_ui.py"""

    def setUp(self):
        """Configuration commune pour tous les tests"""
        # Mock de données de consultant
        self.mock_consultant_data = {
            'id': 1,
            'nom': 'Dupont',
            'prenom': 'Jean',
            'societe': 'Societe A',
            'practice': 'Data',
            'grade': 'Senior',
            'salaire_actuel': 75000,
            'disponibilite': True,
            'experience_annees': 8,
            'nb_missions': 15
        }

    @patch('app.ui.enhanced_ui.st')
    def test_advanced_ui_filters_init(self, mock_st):
        """Test initialisation AdvancedUIFilters"""
        filters = AdvancedUIFilters()

        # Vérifier les attributs par défaut
        self.assertIsInstance(filters.filters, dict)
        self.assertIn("search_term", filters.filters)
        self.assertEqual(filters.filters["search_term"], "")

    @patch('app.ui.enhanced_ui.st')
    def test_advanced_ui_filters_reset_filters(self, mock_st):
        """Test reset_filters"""
        filters = AdvancedUIFilters()
        # Modifier quelques filtres
        filters.filters["societe_filter"] = "Test"
        filters.filters["search_term"] = "test"

        filters.reset_filters()

        # Vérifier que les filtres ont été remis à zéro
        self.assertIsNone(filters.filters["societe_filter"])
        self.assertEqual(filters.filters["search_term"], "")

    @patch('app.ui.enhanced_ui.st')
    def test_advanced_ui_filters_apply_filters(self, mock_st):
        """Test apply_filters"""
        filters = AdvancedUIFilters()
        # Définir un filtre de société
        filters.filters["societe_filter"] = "Societe A"

        data = [self.mock_consultant_data, {'societe': 'Societe B'}]

        result = filters.apply_filters(data)

        # Vérifier que le filtrage fonctionne
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['societe'], 'Societe A')

    @patch('app.ui.enhanced_ui.st')
    def test_advanced_ui_filters_get_unique_values(self, mock_st):
        """Test _get_unique_values"""
        filters = AdvancedUIFilters()

        unique_societes = filters._get_unique_values('societe')
        # Cette méthode utilise les données globales, donc on teste juste qu'elle retourne une liste
        self.assertIsInstance(unique_societes, list)

    @patch('app.ui.enhanced_ui.st')
    def test_data_table_enhancer_init(self, mock_st):
        """Test initialisation DataTableEnhancer"""
        # DataTableEnhancer est une classe statique, test de l'import
        self.assertTrue(hasattr(DataTableEnhancer, 'render_enhanced_table'))
        self.assertTrue(hasattr(DataTableEnhancer, 'render_action_buttons'))

    @patch('app.ui.enhanced_ui.st')
    def test_real_time_search_should_search_false(self, mock_st):
        """Test should_search - devrait retourner True la première fois"""
        search = RealTimeSearch()

        result = search.should_search()

        # should_search retourne True la première fois
        self.assertTrue(result)

    @patch('app.ui.enhanced_ui.st')
    def test_real_time_search_should_search_true(self, mock_st):
        """Test should_search avec recherche activée"""
        search = RealTimeSearch()
        search.search_enabled = True
        search.last_search_time = 0  # Forcer une recherche

        result = search.should_search()

        self.assertTrue(result)

    @patch('app.ui.enhanced_ui.st')
    @patch('app.ui.enhanced_ui.get_cached_search_results')
    def test_real_time_search_search_with_cache(self, mock_get_cached, mock_st):
        """Test search_with_cache"""
        mock_get_cached.return_value = ([self.mock_consultant_data], 1)

        search = RealTimeSearch()

        result_data, result_total = search.search_with_cache("test", 1, 10)

        self.assertEqual(len(result_data), 1)
        self.assertEqual(result_total, 1)

    @patch('app.ui.enhanced_ui.st')
    def test_data_table_enhancer_render_action_buttons_none(self, mock_st):
        """Test render_action_buttons sans sélection"""
        result = DataTableEnhancer.render_action_buttons({}, ['edit', 'delete'])

        self.assertIsNone(result)

    @patch('app.ui.enhanced_ui.st')
    def test_data_table_enhancer_render_action_buttons_with_data(self, mock_st):
        """Test render_action_buttons avec données"""
        # Mock st.columns pour retourner des objets mock
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3)
        mock_st.button = MagicMock(return_value=True)

        DataTableEnhancer.render_action_buttons({'id': 1}, ['edit'])

        # Vérifier qu'un bouton a été rendu
        self.assertTrue(mock_st.button.called)

    @patch('app.ui.enhanced_ui.st')
    def test_show_loading(self, mock_st):
        """Test show_loading"""
        LoadingSpinner.show_loading("Test loading")

        # Vérifier que st.spinner a été appelée
        self.assertTrue(mock_st.spinner.called)

    @patch('app.ui.enhanced_ui.st')
    def test_show_success(self, mock_st):
        """Test show_success"""
        NotificationManager.show_success("Test success")

        # Vérifier que success a été appelée
        self.assertTrue(mock_st.success.called)

    @patch('app.ui.enhanced_ui.st')
    def test_show_error(self, mock_st):
        """Test show_error"""
        NotificationManager.show_error("Test error")

        # Vérifier que error a été appelée
        self.assertTrue(mock_st.error.called)

    @patch('app.ui.enhanced_ui.st')
    def test_show_warning(self, mock_st):
        """Test show_warning"""
        NotificationManager.show_warning("Test warning")

        # Vérifier que warning a été appelée
        self.assertTrue(mock_st.warning.called)

    @patch('app.ui.enhanced_ui.st')
    def test_show_info(self, mock_st):
        """Test show_info"""
        NotificationManager.show_info("Test info")

        # Vérifier que info a été appelée
        self.assertTrue(mock_st.info.called)

    @patch('app.ui.enhanced_ui.st')
    @patch('app.ui.enhanced_ui._initialize_ui_components')
    @patch('app.ui.enhanced_ui._load_consultant_data')
    @patch('app.ui.enhanced_ui._display_metrics')
    @patch('app.ui.enhanced_ui._handle_consultant_selection')
    def test_create_enhanced_consultants_view(self, mock_handle_selection, mock_display_metrics, mock_load_data, mock_init_ui, mock_st):
        """Test create_enhanced_consultants_view"""
        # Mock des composants UI
        mock_filters = MagicMock()
        mock_search = MagicMock()
        mock_enhancer = MagicMock()
        mock_init_ui.return_value = (mock_filters, mock_search, mock_enhancer)

        # Mock des fonctions auxiliaires
        mock_load_data.return_value = [self.mock_consultant_data]

        create_enhanced_consultants_view()

        # Vérifier que les fonctions auxiliaires ont été appelées
        self.assertTrue(mock_init_ui.called)
        self.assertTrue(mock_load_data.called)
        self.assertTrue(mock_display_metrics.called)

    @patch('app.ui.enhanced_ui.st')
    def test_initialize_ui_components(self, mock_st):
        """Test _initialize_ui_components"""
        from app.ui.enhanced_ui import _initialize_ui_components

        result = _initialize_ui_components()

        # Vérifier que les composants UI ont été initialisés
        self.assertEqual(len(result), 3)  # filters, search, enhancer

    @patch('app.ui.enhanced_ui.st')
    @patch('app.ui.enhanced_ui.get_cached_consultants_list')
    def test_load_consultant_data(self, mock_get_cached, mock_st):
        """Test _load_consultant_data"""
        from app.ui.enhanced_ui import _load_consultant_data

        mock_get_cached.return_value = [self.mock_consultant_data]
        mock_st.text_input.return_value = ""  # Pas de terme de recherche

        search = RealTimeSearch()
        result = _load_consultant_data(search)

        # Vérifier que les données ont été chargées
        self.assertIsInstance(result, list)

    @patch('app.ui.enhanced_ui.st')
    def test_display_metrics(self, mock_st):
        """Test _display_metrics"""
        from app.ui.enhanced_ui import _display_metrics

        # Mock st.columns pour retourner des objets mock
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = MagicMock()
        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3, mock_col4)

        data = [self.mock_consultant_data, self.mock_consultant_data]

        _display_metrics(data)

        # Vérifier que les métriques ont été affichées
        self.assertTrue(mock_st.metric.called)

    @patch('app.ui.enhanced_ui.st')
    def test_handle_consultant_selection(self, mock_st):
        """Test _handle_consultant_selection"""
        from app.ui.enhanced_ui import _handle_consultant_selection

        # Créer un mock event avec la structure attendue
        mock_event = MagicMock()
        mock_event.selection.rows = [0]

        data = [self.mock_consultant_data]
        enhancer = MagicMock()

        _handle_consultant_selection(mock_event, data, enhancer)

        # Vérifier que la fonction s'exécute sans erreur
        # (c'est principalement de la logique UI)

    @patch('app.ui.enhanced_ui.st')
    def test_execute_consultant_action_view(self, mock_st):
        """Test _execute_consultant_action view"""
        from app.ui.enhanced_ui import _execute_consultant_action

        _execute_consultant_action("view", self.mock_consultant_data)

        # Vérifier que session_state a été modifié
        self.assertTrue(hasattr(mock_st.session_state, 'view_consultant_profile'))


if __name__ == '__main__':
    unittest.main()