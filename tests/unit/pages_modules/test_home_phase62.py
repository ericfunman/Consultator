"""
Tests Phase 62: home.py - Page d'accueil dashboard
Objectif: Tester les fonctions d'affichage du dashboard
Cible: 59 lignes manquantes → ~15 tests
Focus: show(), show_dashboard_charts(), show_getting_started()
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
import pytest
import pandas as pd
import sys
import os

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# Import du module à tester
import app.pages_modules.home as home


class TestShowFunction(unittest.TestCase):
    """Tests pour show() - fonction principale"""

    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_database_not_initialized(self, mock_db_info, mock_st):
        """Test affichage quand la base de données n'est pas initialisée"""
        # Setup
        mock_db_info.return_value = {"exists": False}
        mock_st.button.return_value = False
        
        # Execute
        home.show()
        
        # Assert
        mock_st.title.assert_called_with("🏠 Tableau de bord")
        mock_st.error.assert_called_with("❌ Base de données non initialisée")
        mock_st.button.assert_called_with("Initialiser la base de données")

    @patch('database.database.init_database')
    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_initialize_database_clicked(self, mock_db_info, mock_st, mock_init_db):
        """Test initialisation de la base de données via bouton"""
        # Setup
        mock_db_info.return_value = {"exists": False}
        mock_st.button.return_value = True  # Bouton cliqué
        mock_init_db.return_value = True
        
        # Execute
        home.show()
        
        # Assert
        mock_init_db.assert_called_once()
        mock_st.success.assert_called_with("✅ Base de données initialisée avec succès !")
        mock_st.rerun.assert_called_once()

    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_database_initialized_no_consultants(self, mock_db_info, mock_st):
        """Test affichage avec base initialisée mais sans consultants"""
        # Setup
        mock_db_info.return_value = {
            "exists": True,
            "consultants": 0,
            "missions": 0
        }
        mock_st.columns.return_value = [Mock(), Mock(), Mock()]
        
        # Execute
        home.show()
        
        # Assert
        mock_st.title.assert_called_with("🏠 Tableau de bord")
        mock_st.metric.assert_called()  # Les métriques sont affichées

    @patch('app.pages_modules.home.show_getting_started')
    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_calls_getting_started_when_no_consultants(self, mock_db_info, mock_st, mock_getting_started):
        """Test que show_getting_started est appelé quand il n'y a pas de consultants"""
        # Setup
        mock_db_info.return_value = {
            "exists": True,
            "consultants": 0,
            "missions": 5
        }
        mock_st.columns.return_value = [Mock(), Mock(), Mock()]
        
        # Execute
        home.show()
        
        # Assert
        mock_getting_started.assert_called_once()

    @patch('app.pages_modules.home.show_dashboard_charts')
    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_calls_dashboard_charts_when_consultants_exist(self, mock_db_info, mock_st, mock_dashboard_charts):
        """Test que show_dashboard_charts est appelé quand il y a des consultants"""
        # Setup
        mock_db_info.return_value = {
            "exists": True,
            "consultants": 10,
            "missions": 5
        }
        mock_st.columns.return_value = [Mock(), Mock(), Mock()]
        
        # Execute
        home.show()
        
        # Assert
        mock_dashboard_charts.assert_called_once()

    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_displays_metrics_with_data(self, mock_db_info, mock_st):
        """Test affichage des métriques avec données"""
        # Setup
        mock_db_info.return_value = {
            "exists": True,
            "consultants": 60,
            "missions": 120
        }
        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_col3 = Mock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]
        
        # Execute
        home.show()
        
        # Assert
        mock_st.columns.assert_called()
        # Vérifier que metric est appelé (au moins 3 fois pour les 3 colonnes)
        assert mock_st.metric.call_count >= 3


class TestShowDashboardCharts(unittest.TestCase):
    """Tests pour show_dashboard_charts()"""

    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.pd.DataFrame')
    @patch('app.pages_modules.home.px')
    def test_show_dashboard_charts_displays_revenue_chart(self, mock_px, mock_dataframe, mock_st):
        """Test affichage du graphique des revenus"""
        # Setup
        mock_st.columns.return_value = [Mock(), Mock()]
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df
        mock_fig = Mock()
        mock_px.line.return_value = mock_fig
        
        # Execute
        home.show_dashboard_charts()
        
        # Assert
        mock_st.subheader.assert_any_call("💰 Évolution des revenus")
        mock_px.line.assert_called_once()
        mock_st.plotly_chart.assert_called()

    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.pd.DataFrame')
    def test_show_dashboard_charts_displays_activities_table(self, mock_dataframe, mock_st):
        """Test affichage du tableau d'activités récentes"""
        # Setup
        mock_st.columns.return_value = [Mock(), Mock()]
        mock_df_revenus = MagicMock()
        mock_df_activites = MagicMock()
        mock_dataframe.side_effect = [mock_df_revenus, mock_df_activites]
        
        # Execute
        home.show_dashboard_charts()
        
        # Assert
        mock_st.subheader.assert_any_call("📋 Activités récentes")
        mock_st.dataframe.assert_called_once()

    @patch('app.pages_modules.home.st')
    def test_show_dashboard_charts_creates_revenue_data(self, mock_st):
        """Test que les données de revenus sont créées correctement"""
        # Setup
        mock_st.columns.return_value = [Mock(), Mock()]
        
        # Execute
        home.show_dashboard_charts()
        
        # Assert
        # Vérifier que la fonction s'exécute sans erreur
        assert mock_st.subheader.call_count >= 2  # Au moins 2 subheaders


class TestShowGettingStarted(unittest.TestCase):
    """Tests pour show_getting_started()"""

    @patch('app.pages_modules.home.st')
    def test_show_getting_started_displays_steps(self, mock_st):
        """Test affichage des étapes pour commencer"""
        # Setup
        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_col3 = Mock()
        mock_st.columns.side_effect = [
            [mock_col1, mock_col2, mock_col3],  # First columns() call for steps
            [Mock()]  # Second columns() call for quick actions
        ]
        mock_st.button.return_value = False
        
        # Execute
        home.show_getting_started()
        
        # Assert
        mock_st.subheader.assert_any_call("🚀 Commencez avec Consultator")
        # Vérifier que markdown est appelé plusieurs fois (3 étapes)
        assert mock_st.markdown.call_count >= 3

    @patch('app.pages_modules.home.st')
    def test_show_getting_started_displays_quick_actions(self, mock_st):
        """Test affichage des actions rapides"""
        # Setup
        mock_st.columns.side_effect = [
            [Mock(), Mock(), Mock()],  # Steps
            [Mock()]  # Quick actions
        ]
        mock_st.button.return_value = False
        
        # Execute
        home.show_getting_started()
        
        # Assert
        mock_st.subheader.assert_any_call("⚡ Actions rapides")
        mock_st.button.assert_called()

    @patch('app.pages_modules.home.st')
    def test_show_getting_started_button_click_navigates(self, mock_st):
        """Test clic sur bouton 'Ajouter un consultant' navigue vers consultants"""
        # Setup
        mock_st.columns.side_effect = [
            [Mock(), Mock(), Mock()],
            [Mock()]
        ]
        mock_st.button.return_value = True  # Bouton cliqué
        
        # Execute
        home.show_getting_started()
        
        # Assert
        mock_st.switch_page.assert_called_with("pages/consultants.py")

    @patch('app.pages_modules.home.st')
    def test_show_getting_started_displays_tips_expander(self, mock_st):
        """Test affichage de l'expander avec conseils"""
        # Setup
        mock_st.columns.side_effect = [
            [Mock(), Mock(), Mock()],
            [Mock()]
        ]
        mock_st.button.return_value = False
        mock_expander = MagicMock()
        mock_st.expander.return_value.__enter__.return_value = mock_expander
        
        # Execute
        home.show_getting_started()
        
        # Assert
        mock_st.expander.assert_called_with("💡 Conseils pour bien commencer")


class TestConstants(unittest.TestCase):
    """Tests pour les constantes du module"""

    def test_detail_column_constant_defined(self):
        """Test que la constante DETAIL_COLUMN est définie"""
        assert hasattr(home, 'DETAIL_COLUMN')
        assert home.DETAIL_COLUMN == "Détail"


class TestModuleStructure(unittest.TestCase):
    """Tests de structure du module"""

    def test_module_has_show_function(self):
        """Test que le module a une fonction show()"""
        assert hasattr(home, 'show')
        assert callable(home.show)

    def test_module_has_show_dashboard_charts_function(self):
        """Test que le module a une fonction show_dashboard_charts()"""
        assert hasattr(home, 'show_dashboard_charts')
        assert callable(home.show_dashboard_charts)

    def test_module_has_show_getting_started_function(self):
        """Test que le module a une fonction show_getting_started()"""
        assert hasattr(home, 'show_getting_started')
        assert callable(home.show_getting_started)


if __name__ == "__main__":
    unittest.main()
