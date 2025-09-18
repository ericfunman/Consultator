"""
Tests pour le module home.py
"""

import pytest
from unittest.mock import Mock, patch
from app.pages_modules.home import show
from tests.fixtures.base_test import BaseUITest


class TestHomeModule(BaseUITest):
    """Tests pour le module home"""

    @patch("app.pages_modules.home.get_database_info")
    @patch("streamlit.title")
    @patch("streamlit.error")
    @patch("streamlit.button")
    def test_show_database_not_initialized(
        self, mock_button, mock_error, mock_title, mock_get_db_info
    ):
        """Test de show() quand la base de données n'est pas initialisée"""
        # Mock base de données non initialisée
        mock_get_db_info.return_value = {"exists": False}
        mock_button.return_value = False

        # Test
        show()

        # Vérifications
        mock_title.assert_called_once_with("🏠 Tableau de bord")
        mock_get_db_info.assert_called_once()
        mock_error.assert_called_once_with("❌ Base de données non initialisée")
        mock_button.assert_called_once_with("Initialiser la base de données")

    @patch("app.pages_modules.home.get_database_info")
    @patch("streamlit.title")
    @patch("streamlit.error")
    @patch("streamlit.button")
    @patch("streamlit.success")
    @patch("streamlit.rerun")
    @patch("database.database.init_database")
    def test_show_database_initialization_success(
        self,
        mock_init_db,
        mock_rerun,
        mock_success,
        mock_button,
        mock_error,
        mock_title,
        mock_get_db_info,
    ):
        """Test de show() avec initialisation réussie de la base de données"""
        # Mock base de données non initialisée puis initialisée
        mock_get_db_info.return_value = {"exists": False}
        mock_button.return_value = True
        mock_init_db.return_value = True

        # Test
        show()

        # Vérifications
        mock_title.assert_called_once_with("🏠 Tableau de bord")
        mock_init_db.assert_called_once()
        mock_success.assert_called_once_with(
            "✅ Base de données initialisée avec succès !"
        )
        mock_rerun.assert_called_once()

    @patch("app.pages_modules.home.get_database_info")
    @patch("streamlit.title")
    @patch("streamlit.columns")
    @patch("streamlit.metric")
    @patch("app.pages_modules.home.show_dashboard_charts")
    def test_show_with_data(
        self, mock_show_charts, mock_metric, mock_columns, mock_title, mock_get_db_info
    ):
        """Test de show() avec des données existantes"""
        # Mock base de données avec données
        mock_get_db_info.return_value = {
            "exists": True,
            "consultants": 45,
            "missions": 23,
        }

        # Mock colonnes
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]

        # Test
        show()

        # Vérifications
        mock_title.assert_called_once_with("🏠 Tableau de bord")
        mock_columns.assert_called_once_with(3)
        mock_metric.assert_any_call(
            label="👥 Consultants", value=45, delta="Actifs dans la practice"
        )
        mock_metric.assert_any_call(
            label="💼 Missions", value=23, delta="En cours et terminées"
        )
        mock_show_charts.assert_called_once()

    @patch("app.pages_modules.home.get_database_info")
    @patch("streamlit.title")
    @patch("streamlit.columns")
    @patch("streamlit.metric")
    @patch("app.pages_modules.home.show_getting_started")
    def test_show_without_data(
        self,
        mock_show_getting_started,
        mock_metric,
        mock_columns,
        mock_title,
        mock_get_db_info,
    ):
        """Test de show() sans données (consultants = 0)"""
        # Mock base de données sans données
        mock_get_db_info.return_value = {
            "exists": True,
            "consultants": 0,
            "missions": 0,
        }

        # Mock colonnes
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]

        # Test
        show()

        # Vérifications
        mock_title.assert_called_once_with("🏠 Tableau de bord")
        mock_show_getting_started.assert_called_once()
