"""
Tests pour le module home.py - Version simplifiée et fonctionnelle
Tests basés uniquement sur les fonctions qui existent réellement
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


class TestHomeFunctional(unittest.TestCase):
    """Tests fonctionnels pour le module home.py"""

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

    @patch('app.pages_modules.home.show_dashboard_charts')
    @patch('streamlit.markdown')
    @patch('streamlit.metric')
    @patch('streamlit.columns')
    @patch('streamlit.title')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_with_data(self, mock_get_db_info, mock_title, mock_columns, 
                           mock_metric, mock_markdown, mock_charts):
        """Test de la fonction show avec des données"""
        # Setup
        mock_get_db_info.return_value = self.db_info_with_data
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show
        show()
        
        # Vérifications
        mock_title.assert_called_once_with("🏠 Tableau de bord")
        mock_get_db_info.assert_called_once()
        mock_columns.assert_called_with(3)
        mock_metric.assert_called()
        mock_charts.assert_called_once()

    @patch('app.pages_modules.home.show_getting_started')
    @patch('streamlit.markdown')
    @patch('streamlit.metric')
    @patch('streamlit.columns')
    @patch('streamlit.title')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_with_empty_data(self, mock_get_db_info, mock_title, mock_columns, 
                                 mock_metric, mock_markdown, mock_getting_started):
        """Test de la fonction show avec données vides"""
        # Setup
        mock_get_db_info.return_value = self.db_info_empty
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show
        show()
        
        # Vérifications
        mock_get_db_info.assert_called_once()
        mock_getting_started.assert_called_once()

    @patch('streamlit.button')
    @patch('streamlit.error')
    @patch('streamlit.title')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_database_not_exists(self, mock_get_db_info, mock_title, mock_error, mock_button):
        """Test quand la base de données n'existe pas"""
        # Setup
        mock_get_db_info.return_value = self.db_info_not_exists
        mock_button.return_value = False  # Bouton pas cliqué
        
        from app.pages_modules.home import show
        show()
        
        # Vérifications
        mock_get_db_info.assert_called_once()
        mock_error.assert_called_once_with("❌ Base de données non initialisée")

    @patch('streamlit.switch_page')
    @patch('streamlit.expander')
    @patch('streamlit.button')
    @patch('streamlit.markdown')
    @patch('streamlit.container')
    @patch('streamlit.columns')
    @patch('streamlit.subheader')
    def test_show_getting_started(self, mock_subheader, mock_columns, mock_container,
                                 mock_markdown, mock_button, mock_expander, mock_switch_page):
        """Test de la fonction show_getting_started"""
        # Setup
        mock_columns.side_effect = [[self.mock_col, self.mock_col, self.mock_col], [self.mock_col]]
        mock_button.return_value = False
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock()
        mock_expander.return_value.__enter__ = Mock()
        mock_expander.return_value.__exit__ = Mock()
        
        from app.pages_modules.home import show_getting_started
        show_getting_started()
        
        # Vérifications
        self.assertEqual(mock_subheader.call_count, 2)
        self.assertEqual(mock_columns.call_count, 2)
        mock_button.assert_called_once_with("➕ Ajouter un consultant", type="primary")
        mock_expander.assert_called_once_with("💡 Conseils pour bien commencer")

    @patch('streamlit.switch_page')
    @patch('streamlit.expander')
    @patch('streamlit.button')
    @patch('streamlit.markdown')
    @patch('streamlit.container')
    @patch('streamlit.columns')
    @patch('streamlit.subheader')
    def test_show_getting_started_button_click(self, mock_subheader, mock_columns, 
                                              mock_container, mock_markdown, mock_button, 
                                              mock_expander, mock_switch_page):
        """Test du clic sur le bouton d'ajout de consultant"""
        # Setup
        mock_columns.side_effect = [[self.mock_col, self.mock_col, self.mock_col], [self.mock_col]]
        mock_button.return_value = True  # Bouton cliqué
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock()
        mock_expander.return_value.__enter__ = Mock()
        mock_expander.return_value.__exit__ = Mock()
        
        from app.pages_modules.home import show_getting_started
        show_getting_started()
        
        # Vérifications - Le bouton a été cliqué
        mock_button.assert_called_once_with("➕ Ajouter un consultant", type="primary")
        mock_switch_page.assert_called_once_with("pages/consultants.py")

    @patch('streamlit.dataframe')
    @patch('streamlit.subheader')
    @patch('streamlit.plotly_chart')
    @patch('streamlit.columns')
    def test_show_dashboard_charts(self, mock_columns, mock_plotly_chart, 
                                  mock_subheader, mock_dataframe):
        """Test de show_dashboard_charts"""
        # Setup
        mock_columns.return_value = [self.mock_col, self.mock_col]
        
        from app.pages_modules.home import show_dashboard_charts
        show_dashboard_charts()
        
        # Vérifications
        mock_columns.assert_called_with(2)
        mock_plotly_chart.assert_called_once()
        mock_subheader.assert_called()
        mock_dataframe.assert_called_once()


if __name__ == '__main__':
    unittest.main()