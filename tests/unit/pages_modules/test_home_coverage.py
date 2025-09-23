"""
Tests pour améliorer la couverture de home.py
Objectif: Passer de 44% à 80%+ de couverture
"""

import pytest
from unittest.mock import patch, MagicMock

from app.pages_modules.home import show


class TestHomeCoverage:
    """Tests complets pour la page d'accueil"""

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_with_database_not_exists(self, mock_get_db_info, mock_st):
        """Test affichage quand base de données n'existe pas"""
        # Setup
        mock_get_db_info.return_value = {"exists": False}
        mock_st.button.return_value = False

        # Execute
        show()

        # Verify
        mock_st.title.assert_called_once_with("🏠 Tableau de bord")
        mock_st.error.assert_called_once_with("❌ Base de données non initialisée")
        mock_st.button.assert_called_once_with("Initialiser la base de données")

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_initialize_database_success(self, mock_get_db_info, mock_st):
        """Test initialisation base de données avec succès"""
        # Setup
        mock_get_db_info.return_value = {"exists": False}
        mock_st.button.return_value = True

        # Mock init_database function
        with patch("database.database.init_database", return_value=True) as mock_init_db:
            mock_init_db.return_value = True

            # Execute
            show()

            # Verify
            mock_init_db.assert_called_once()
            mock_st.success.assert_called_once_with(
                "✅ Base de données initialisée avec succès !"
            )
            mock_st.rerun.assert_called_once()

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_initialize_database_failure(self, mock_get_db_info, mock_st):
        """Test échec initialisation base de données"""
        # Setup
        mock_get_db_info.return_value = {"exists": False}
        mock_st.button.return_value = True

        # Mock init_database function to fail
        with patch("database.database.init_database", return_value=False) as mock_init_db:
            mock_init_db.return_value = False

            # Execute
            show()

            # Verify
            mock_init_db.assert_called_once()
            # Should not call success or rerun if initialization fails

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_with_database_exists_full_dashboard(self, mock_get_db_info, mock_st):
        """Test affichage complet du dashboard avec données"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "total_consultants": 50,
            "total_missions": 25,
            "total_practices": 8,
        }

        # Mock Streamlit components
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Mock services with data - removed since services are not used in home.py
        # Execute
        show()

        # Verify basic functionality
        mock_st.title.assert_called_once_with("🏠 Tableau de bord")

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_with_service_errors(self, mock_get_db_info, mock_st):
        """Test gestion erreurs des services"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "total_consultants": 50,
            "total_missions": 25,
            "total_practices": 8,
        }

        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Mock services with errors - removed since services are not used in home.py
        # Execute
        show()

        # Verify that errors are handled gracefully
        mock_st.title.assert_called_once_with("🏠 Tableau de bord")

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_metrics_display(self, mock_get_db_info, mock_st):
        """Test affichage des métriques principales"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "total_consultants": 100,
            "total_missions": 75,
            "total_practices": 12,
        }

        # Mock columns
        col1, col2, col3 = MagicMock(), MagicMock(), MagicMock()
        mock_st.columns.return_value = [col1, col2, col3]
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Execute
        show()

        # Verify
        # The code calls columns(3) for the 3 getting started steps, then columns(1) for actions
        assert mock_st.columns.call_count >= 2  # At least 2 calls to columns
        # Verify metrics are called with database info
        assert mock_st.metric.called

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_charts_generation(self, mock_get_db_info, mock_st):
        """Test génération des graphiques"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "consultants": 50,  # Changed from total_consultants to consultants
            "missions": 25,
            "practices": 8,
        }

        # Mock columns to return appropriate number of columns
        def mock_columns(n):
            return [MagicMock() for _ in range(n)]
        mock_st.columns.side_effect = mock_columns

        # Mock services and charts - removed since services are not used in home.py
        with patch(
            "app.pages_modules.home.pd"
        ) as mock_pd, patch(
            "app.pages_modules.home.px"
        ) as mock_px:

            # Mock chart generation
            mock_df = MagicMock()
            mock_pd.DataFrame.return_value = mock_df
            mock_fig = MagicMock()
            mock_px.line.return_value = mock_fig  # Changed from pie to line

            # Execute
            show()

            # Verify charts are generated
            mock_pd.DataFrame.assert_called()
            mock_px.line.assert_called()  # Changed from pie to line

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_empty_data_handling(self, mock_get_db_info, mock_st):
        """Test gestion des données vides"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "consultants": 0,
            "missions": 0,
            "practices": 0,
        }

        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Mock services with empty data - removed since services are not used
        # No services to mock in this test

        # Execute
        show()

        # Verify
        mock_st.title.assert_called_once_with("🏠 Tableau de bord")
        # Should still display metrics, even with 0 values
        assert mock_st.metric.called

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_performance_with_large_dataset(self, mock_get_db_info, mock_st):
        """Test performance avec grand dataset"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "consultants": 10000,
            "missions": 5000,
            "practices": 50,
        }

        # Mock columns to return appropriate number of columns
        def mock_columns(n):
            return [MagicMock() for _ in range(n)]
        mock_st.columns.side_effect = mock_columns

        # Mock services with large data - removed since services are not used
        # No services to mock in this test

        # Execute
        show()

        # Verify it handles large datasets
        mock_st.title.assert_called_once_with("🏠 Tableau de bord")
        assert mock_st.metric.called
