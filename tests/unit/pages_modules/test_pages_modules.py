"""
Tests pour les pages modules
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class TestHomePage:
    """Tests pour la page d'accueil"""

    @patch('streamlit.title')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_with_valid_database(self, mock_get_db_info, mock_metric, mock_columns, mock_title):
        """Test affichage de la page avec base de données valide"""
        # Mock de la base de données
        mock_get_db_info.return_value = {
            "exists": True,
            "consultants_count": 10,
            "missions_count": 25,
            "practices_count": 5
        }

        # Mock des colonnes
        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_col3 = Mock()
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]

        # Importer et tester
        from app.pages_modules.home import show

        # Ne devrait pas lever d'exception
        show()

        # Vérifier les appels
        mock_title.assert_called_with("🏠 Tableau de bord")
        mock_columns.assert_called_with(3)
        assert mock_metric.call_count >= 3  # Au moins 3 métriques

    @patch('streamlit.error')
    @patch('streamlit.button')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_with_invalid_database(self, mock_get_db_info, mock_button, mock_error):
        """Test affichage de la page avec base de données invalide"""
        # Mock de la base de données inexistante
        mock_get_db_info.return_value = {"exists": False}
        mock_button.return_value = False

        from app.pages_modules.home import show

        show()

        mock_error.assert_called_with("❌ Base de données non initialisée")
        mock_button.assert_called_with("Initialiser la base de données")

    @patch('streamlit.success')
    @patch('streamlit.rerun')
    @patch('streamlit.button')
    @patch('streamlit.error')
    @patch('app.pages_modules.home.get_database_info')
    @patch('app.pages_modules.home.init_database')
    def test_show_database_initialization(self, mock_init_db, mock_get_db_info, mock_error, mock_button, mock_rerun, mock_success):
        """Test de l'initialisation de la base de données"""
        # Mock de la base de données inexistante
        mock_get_db_info.return_value = {"exists": False}
        mock_button.return_value = True
        mock_init_db.return_value = True

        from app.pages_modules.home import show

        show()

        mock_init_db.assert_called_once()
        mock_success.assert_called_with("✅ Base de données initialisée avec succès !")
        mock_rerun.assert_called_once()


class TestConsultantsPage:
    """Tests pour la page consultants"""

    @patch('streamlit.title')
    @patch('streamlit.tabs')
    @patch('app.pages_modules.consultants.show_consultants_list')
    @patch('app.pages_modules.consultants.show_add_consultant_form')
    def test_show_consultants_page(self, mock_show_form, mock_show_list, mock_tabs, mock_title):
        """Test affichage de la page consultants"""
        # Mock des tabs
        mock_tab1 = Mock()
        mock_tab2 = Mock()
        mock_tabs.return_value = [mock_tab1, mock_tab2]

        from app.pages_modules.consultants import show

        show()

        mock_title.assert_called_with("👥 Gestion des Consultants")
        mock_tabs.assert_called_with(["Liste des consultants", "Ajouter un consultant"])


class TestMissionsPage:
    """Tests pour la page missions"""

    @patch('streamlit.title')
    @patch('streamlit.tabs')
    def test_show_missions_page(self, mock_tabs, mock_title):
        """Test affichage de la page missions"""
        # Mock des tabs
        mock_tab1 = Mock()
        mock_tab2 = Mock()
        mock_tabs.return_value = [mock_tab1, mock_tab2]

        from app.pages_modules.missions import show

        show()

        mock_title.assert_called_with("📋 Gestion des Missions")
        mock_tabs.assert_called_with(["Liste des missions", "Ajouter une mission"])


class TestPracticesPage:
    """Tests pour la page practices"""

    @patch('streamlit.title')
    @patch('streamlit.tabs')
    def test_show_practices_page(self, mock_tabs, mock_title):
        """Test affichage de la page practices"""
        # Mock des tabs
        mock_tab1 = Mock()
        mock_tab2 = Mock()
        mock_tabs.return_value = [mock_tab1, mock_tab2]

        from app.pages_modules.practices import show

        show()

        mock_title.assert_called_with("🏢 Gestion des Pratiques")
        mock_tabs.assert_called_with(["Liste des pratiques", "Ajouter une pratique"])


class TestSkillsPage:
    """Tests pour la page compétences"""

    @patch('streamlit.title')
    @patch('streamlit.tabs')
    def test_show_skills_page(self, mock_tabs, mock_title):
        """Test affichage de la page compétences"""
        # Mock des tabs
        mock_tab1 = Mock()
        mock_tab2 = Mock()
        mock_tabs.return_value = [mock_tab1, mock_tab2]

        from app.pages_modules.skills import show

        show()

        mock_title.assert_called_with("🎯 Gestion des Compétences")
        mock_tabs.assert_called_with(["Vue d'ensemble", "Gestion détaillée"])


class TestTechnologiesPage:
    """Tests pour la page technologies"""

    @patch('streamlit.title')
    @patch('streamlit.tabs')
    def test_show_technologies_page(self, mock_tabs, mock_title):
        """Test affichage de la page technologies"""
        # Mock des tabs
        mock_tab1 = Mock()
        mock_tab2 = Mock()
        mock_tabs.return_value = [mock_tab1, mock_tab2]

        from app.pages_modules.technologies import show

        show()

        mock_title.assert_called_with("💻 Gestion des Technologies")
        mock_tabs.assert_called_with(["Liste des technologies", "Ajouter une technologie"])
