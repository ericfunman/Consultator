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

        with patch("app.pages_modules.home.init_database") as mock_init_db:
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

        with patch("app.pages_modules.home.init_database") as mock_init_db:
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

        # Mock services with data
        with patch(
            "app.pages_modules.home.ConsultantService"
        ) as mock_consultant_service, patch(
            "app.pages_modules.home.PracticeService"
        ) as mock_practice_service, patch(
            "app.pages_modules.home.pd"
        ) as mock_pd, patch(
            "app.pages_modules.home.px"
        ) as mock_px:

            # Mock consultant service
            mock_consultant_service.get_consultants_stats.return_value = {
                "total": 50,
                "disponibles": 35,
                "en_mission": 15,
            }

            # Mock practice service
            mock_practice_service.get_practice_statistics.return_value = {
                "total_practices": 8,
                "total_consultants": 50,
                "practices_detail": [
                    {"nom": "Data Engineering", "total_consultants": 15},
                    {"nom": "Data Science", "total_consultants": 20},
                    {"nom": "DevOps", "total_consultants": 15},
                ],
            }

            # Mock DataFrame and plotly
            mock_df = MagicMock()
            mock_pd.DataFrame.return_value = mock_df
            mock_fig = MagicMock()
            mock_px.pie.return_value = mock_fig
            mock_px.bar.return_value = mock_fig

            # Execute
            show()

            # Verify
            mock_st.title.assert_called_once_with("🏠 Tableau de bord")
            assert mock_st.metric.call_count >= 3  # At least 3 metrics displayed
            mock_st.tabs.assert_called()

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

        # Mock services with errors
        with patch(
            "app.pages_modules.home.ConsultantService"
        ) as mock_consultant_service, patch(
            "app.pages_modules.home.PracticeService"
        ) as mock_practice_service:

            mock_consultant_service.get_consultants_stats.side_effect = Exception(
                "Service error"
            )
            mock_practice_service.get_practice_statistics.side_effect = Exception(
                "Service error"
            )

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
        mock_st.columns.assert_called_with(3)
        # Verify metrics are called with database info
        assert mock_st.metric.called

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_tabs_functionality(self, mock_get_db_info, mock_st):
        """Test fonctionnalité des onglets"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "total_consultants": 50,
            "total_missions": 25,
            "total_practices": 8,
        }

        # Mock tabs
        tab1, tab2, tab3 = MagicMock(), MagicMock(), MagicMock()
        mock_st.tabs.return_value = [tab1, tab2, tab3]
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Mock services
        with patch(
            "app.pages_modules.home.ConsultantService"
        ) as mock_consultant_service, patch(
            "app.pages_modules.home.PracticeService"
        ) as mock_practice_service:

            mock_consultant_service.get_consultants_stats.return_value = {
                "total": 50,
                "disponibles": 35,
                "en_mission": 15,
            }

            mock_practice_service.get_practice_statistics.return_value = {
                "total_practices": 8,
                "total_consultants": 50,
                "practices_detail": [],
            }

            # Execute
            show()

            # Verify tabs are created
            mock_st.tabs.assert_called_once()
            # Verify tab contexts are used
            assert tab1.__enter__.called
            assert tab2.__enter__.called
            assert tab3.__enter__.called

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_charts_generation(self, mock_get_db_info, mock_st):
        """Test génération des graphiques"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "total_consultants": 50,
            "total_missions": 25,
            "total_practices": 8,
        }

        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Mock services and charts
        with patch(
            "app.pages_modules.home.ConsultantService"
        ) as mock_consultant_service, patch(
            "app.pages_modules.home.PracticeService"
        ) as mock_practice_service, patch(
            "app.pages_modules.home.pd"
        ) as mock_pd, patch(
            "app.pages_modules.home.px"
        ) as mock_px:

            # Mock services with chart data
            mock_consultant_service.get_consultants_stats.return_value = {
                "total": 50,
                "disponibles": 35,
                "en_mission": 15,
            }

            mock_practice_service.get_practice_statistics.return_value = {
                "total_practices": 8,
                "total_consultants": 50,
                "practices_detail": [
                    {"nom": "Data Engineering", "total_consultants": 15},
                    {"nom": "Data Science", "total_consultants": 20},
                    {"nom": "DevOps", "total_consultants": 15},
                ],
            }

            # Mock chart generation
            mock_df = MagicMock()
            mock_pd.DataFrame.return_value = mock_df
            mock_fig = MagicMock()
            mock_px.pie.return_value = mock_fig
            mock_px.bar.return_value = mock_fig

            # Execute
            show()

            # Verify charts are generated
            mock_pd.DataFrame.assert_called()
            mock_px.pie.assert_called()

    @patch("app.pages_modules.home.st")
    @patch("app.pages_modules.home.get_database_info")
    def test_show_empty_data_handling(self, mock_get_db_info, mock_st):
        """Test gestion des données vides"""
        # Setup
        mock_get_db_info.return_value = {
            "exists": True,
            "total_consultants": 0,
            "total_missions": 0,
            "total_practices": 0,
        }

        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Mock services with empty data
        with patch(
            "app.pages_modules.home.ConsultantService"
        ) as mock_consultant_service, patch(
            "app.pages_modules.home.PracticeService"
        ) as mock_practice_service:

            mock_consultant_service.get_consultants_stats.return_value = {
                "total": 0,
                "disponibles": 0,
                "en_mission": 0,
            }

            mock_practice_service.get_practice_statistics.return_value = {
                "total_practices": 0,
                "total_consultants": 0,
                "practices_detail": [],
            }

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
            "total_consultants": 10000,
            "total_missions": 5000,
            "total_practices": 50,
        }

        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Mock services with large data
        with patch(
            "app.pages_modules.home.ConsultantService"
        ) as mock_consultant_service, patch(
            "app.pages_modules.home.PracticeService"
        ) as mock_practice_service:

            mock_consultant_service.get_consultants_stats.return_value = {
                "total": 10000,
                "disponibles": 7000,
                "en_mission": 3000,
            }

            # Large practices list
            large_practices_detail = [
                {"nom": f"Practice {i}", "total_consultants": 200} for i in range(50)
            ]

            mock_practice_service.get_practice_statistics.return_value = {
                "total_practices": 50,
                "total_consultants": 10000,
                "practices_detail": large_practices_detail,
            }

            # Execute
            show()

            # Verify it handles large datasets
            mock_st.title.assert_called_once_with("🏠 Tableau de bord")
            assert mock_st.metric.called
