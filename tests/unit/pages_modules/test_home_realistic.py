"""
Tests pour le module home.py - Version réaliste
Tests basés sur le vrai contenu du module
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Ajouter le répertoire racine au path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)


class TestHomeRealistic(unittest.TestCase):
    """Tests pour le module home.py"""

    def setUp(self):
        """Setup pour chaque test"""
        self.db_info_with_data = {
            "exists": True,
            "consultants": 25,
            "missions": 15,
            "revenues": 120000
        }
        
        self.db_info_empty = {
            "exists": True,
            "consultants": 0,
            "missions": 0,
            "revenues": 0
        }
        
        self.db_info_not_exists = {
            "exists": False
        }
        
        # Mock column avec support context manager
        self.mock_col = MagicMock()
        self.mock_col.__enter__ = MagicMock(return_value=self.mock_col)
        self.mock_col.__exit__ = MagicMock(return_value=None)

    @patch('app.pages_modules.home.get_database_info')
    def test_show_with_data(self, mock_get_db_info):
        """Test de la fonction show avec des données"""
        # Setup
        mock_get_db_info.return_value = self.db_info_with_data
        
        with patch('streamlit.title') as mock_title, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('app.pages_modules.home.show_dashboard_charts') as mock_charts:
            
            mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
            
            # Import et exécution
            from app.pages_modules.home import show
            show()
            
            # Vérifications
            mock_title.assert_called_once_with("🏠 Tableau de bord")
            mock_get_db_info.assert_called_once()
            mock_columns.assert_called_with(3)
            self.assertEqual(mock_metric.call_count, 3)
            mock_markdown.assert_called_with("---")
            mock_charts.assert_called_once()

    @patch('app.pages_modules.home.get_database_info')
    def test_show_with_empty_data(self, mock_get_db_info):
        """Test de la fonction show sans données"""
        # Setup
        mock_get_db_info.return_value = self.db_info_empty
        
        with patch('streamlit.title'), \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.metric'), \
             patch('streamlit.markdown'), \
             patch('app.pages_modules.home.show_getting_started') as mock_getting_started:
            
            mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
            
            # Import et exécution
            from app.pages_modules.home import show
            show()
            
            # Vérifications
            mock_getting_started.assert_called_once()

    @patch('app.pages_modules.home.get_database_info')
    def test_show_database_not_exists(self, mock_get_db_info):
        """Test avec base de données non existante"""
        # Setup
        mock_get_db_info.return_value = self.db_info_not_exists
        
        with patch('streamlit.title'), \
             patch('streamlit.error') as mock_error, \
             patch('streamlit.button') as mock_button:
            
            mock_button.return_value = False
            
            # Import et exécution
            from app.pages_modules.home import show
            show()
            
            # Vérifications
            mock_error.assert_called_once_with("❌ Base de données non initialisée")
            mock_button.assert_called_once_with("Initialiser la base de données")

    @patch('app.pages_modules.home.get_database_info')
    @patch('database.database.init_database')
    def test_database_initialization_success(self, mock_init_db, mock_get_db_info):
        """Test d'initialisation réussie de la base de données"""
        # Setup
        mock_get_db_info.return_value = self.db_info_not_exists
        mock_init_db.return_value = True
        
        with patch('streamlit.title'), \
             patch('streamlit.error'), \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.success') as mock_success, \
             patch('streamlit.rerun') as mock_rerun:
            
            mock_button.return_value = True
            
            # Import et exécution
            from app.pages_modules.home import show
            show()
            
            # Vérifications
            mock_init_db.assert_called_once()
            mock_success.assert_called_once_with("✅ Base de données initialisée avec succès !")
            mock_rerun.assert_called_once()

    def test_show_dashboard_charts(self):
        """Test de la fonction show_dashboard_charts"""
        with patch('streamlit.columns') as mock_columns, \
             patch('streamlit.subheader') as mock_subheader, \
             patch('streamlit.plotly_chart') as mock_plotly, \
             patch('streamlit.dataframe') as mock_dataframe, \
             patch('plotly.express.line') as mock_px_line:
            
            # Setup
            mock_columns.return_value = [self.mock_col, self.mock_col]
            mock_fig = Mock()
            mock_px_line.return_value = mock_fig
            
            # Import et exécution
            from app.pages_modules.home import show_dashboard_charts
            show_dashboard_charts()
            
            # Vérifications
            mock_columns.assert_called_once_with(2)
            self.assertEqual(mock_subheader.call_count, 2)
            mock_plotly.assert_called_once()
            mock_dataframe.assert_called_once()
            mock_px_line.assert_called_once()

    def test_show_getting_started(self):
        """Test de la fonction show_getting_started"""
        with patch('streamlit.subheader') as mock_subheader, \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.container') as mock_container, \
             patch('streamlit.markdown') as mock_markdown, \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.expander') as mock_expander, \
             patch('streamlit.switch_page') as mock_switch_page:
            
            # Setup
            mock_columns.side_effect = [[self.mock_col, self.mock_col, self.mock_col], [self.mock_col]]
            mock_button.return_value = False
            mock_container.return_value.__enter__ = Mock()
            mock_container.return_value.__exit__ = Mock()
            mock_expander.return_value.__enter__ = Mock()
            mock_expander.return_value.__exit__ = Mock()
            
            # Import et exécution
            from app.pages_modules.home import show_getting_started
            show_getting_started()
            
            # Vérifications
            self.assertEqual(mock_subheader.call_count, 2)
            self.assertEqual(mock_columns.call_count, 2)
            mock_button.assert_called_once_with("➕ Ajouter un consultant", type="primary")
            mock_expander.assert_called_once_with("💡 Conseils pour bien commencer")

    def test_show_getting_started_button_click(self):
        """Test du clic sur le bouton d'ajout de consultant"""
        with patch('streamlit.subheader'), \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.container') as mock_container, \
             patch('streamlit.markdown'), \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.expander') as mock_expander, \
             patch('streamlit.switch_page') as mock_switch_page:
            
            # Setup
            mock_columns.side_effect = [[self.mock_col, self.mock_col, self.mock_col], [self.mock_col]]
            mock_button.return_value = True
            mock_container.return_value.__enter__ = Mock()
            mock_container.return_value.__exit__ = Mock()
            mock_expander.return_value.__enter__ = Mock()
            mock_expander.return_value.__exit__ = Mock()
            
            # Import et exécution
            from app.pages_modules.home import show_getting_started
            show_getting_started()
            
            # Vérifications
            mock_switch_page.assert_called_once_with("pages/consultants.py")

    def test_detail_column_constant(self):
        """Test de la constante DETAIL_COLUMN"""
        from app.pages_modules.home import DETAIL_COLUMN
        self.assertEqual(DETAIL_COLUMN, "Détail")

    def test_module_imports(self):
        """Test des imports du module"""
        try:
            from app.pages_modules import home
            from app.pages_modules.home import show, show_dashboard_charts, show_getting_started
            from app.pages_modules.home import DETAIL_COLUMN
            # Si on arrive ici, tous les imports ont réussi
            self.assertIsNotNone(home)
            self.assertIsNotNone(show)
            self.assertIsNotNone(show_dashboard_charts)
            self.assertIsNotNone(show_getting_started)
            self.assertIsNotNone(DETAIL_COLUMN)
        except ImportError as e:
            self.fail(f"Import failed: {e}")

    def test_path_setup(self):
        """Test de la configuration des chemins"""
        from app.pages_modules.home import current_dir, parent_dir
        self.assertTrue(os.path.exists(current_dir))
        self.assertTrue(os.path.exists(parent_dir))

    @patch('app.pages_modules.home.get_database_info')
    def test_metrics_content(self, mock_get_db_info):
        """Test du contenu des métriques"""
        # Setup
        mock_get_db_info.return_value = self.db_info_with_data
        
        with patch('streamlit.title'), \
             patch('streamlit.columns') as mock_columns, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.markdown'), \
             patch('app.pages_modules.home.show_dashboard_charts'):
            
            mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
            
            # Import et exécution
            from app.pages_modules.home import show
            show()
            
            # Vérifications des appels aux colonnes
            self.mock_col.__enter__.assert_called()
            
            # Vérification que metric est appelé 3 fois
            self.assertEqual(mock_metric.call_count, 3)

    def test_dashboard_charts_data_generation(self):
        """Test de la génération des données dans dashboard_charts"""
        with patch('streamlit.columns') as mock_columns, \
             patch('streamlit.subheader'), \
             patch('streamlit.plotly_chart'), \
             patch('streamlit.dataframe'), \
             patch('plotly.express.line') as mock_px_line:
            
            # Setup
            mock_columns.return_value = [self.mock_col, self.mock_col]
            mock_fig = Mock()
            mock_px_line.return_value = mock_fig
            
            # Import et exécution
            from app.pages_modules.home import show_dashboard_charts
            show_dashboard_charts()
            
            # Vérifications
            mock_px_line.assert_called_once()


if __name__ == '__main__':
    unittest.main()