#!/usr/bin/env python3
"""
Tests unitaires pour main.py - Point d'entrée de l'application Consultator
"""

import importlib
import os
import sys
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

# Mock streamlit avant l'import
sys.modules["streamlit"] = Mock()
sys.modules["streamlit_option_menu"] = Mock()

import app.main as main_module


class TestMainModule:
    """Tests pour le module principal main.py"""

    def setup_method(self):
        """Configuration avant chaque test"""
        # Reset du cache des modules
        if hasattr(main_module, "st") and hasattr(main_module.st, "session_state"):
            main_module.st.session_state.clear()

    @patch("app.main.st")
    def test_page_config(self, mock_st):
        """Test que la configuration de page est appelée"""
        # Recharger le module pour déclencher la configuration
        importlib.reload(main_module)

        # Vérifier que set_page_config a été appelée
        mock_st.set_page_config.assert_called_once()
        call_args = mock_st.set_page_config.call_args[1]

        assert call_args["page_title"] == "Consultator"
        assert call_args["page_icon"] == "🏢"
        assert call_args["layout"] == "wide"
        assert call_args["initial_sidebar_state"] == "expanded"

    @patch("app.main.st")
    def test_load_module_safe_home(self, mock_st):
        """Test du chargement du module home"""
        with patch("app.main.pages_modules.home") as mock_home:
            result = main_module.load_module_safe("home")
            assert result == mock_home

    @patch("app.main.st")
    def test_load_module_safe_consultants(self, mock_st):
        """Test du chargement du module consultants"""
        with patch("app.main.pages_modules.consultants") as mock_consultants:
            result = main_module.load_module_safe("consultants")
            assert result == mock_consultants

    @patch("app.main.st")
    def test_load_module_safe_invalid(self, mock_st):
        """Test du chargement d'un module invalide"""
        result = main_module.load_module_safe("invalid_module")
        assert result is None

    @patch("app.main.st")
    def test_load_module_safe_import_error(self, mock_st):
        """Test de gestion d'erreur d'import"""
        with patch(
            "app.main.pages_modules.home", side_effect=ImportError("Module not found")
        ):
            result = main_module.load_module_safe("home")
            assert result is None
            # Vérifier que l'erreur est affichée
            mock_st.error.assert_called_once()

    @patch("app.main.st")
    def test_load_module_safe_cache(self, mock_st):
        """Test que le cache des modules fonctionne"""
        with patch("app.main.pages_modules.home") as mock_home:
            # Premier appel
            result1 = main_module.load_module_safe("home")
            # Deuxième appel - devrait utiliser le cache
            result2 = main_module.load_module_safe("home")

            assert result1 == result2 == mock_home
            # importlib.reload devrait être appelé seulement une fois
            assert importlib.reload.call_count == 1

    @patch("app.main.st")
    @patch("app.main.option_menu")
    def test_show_navigation(self, mock_option_menu, mock_st):
        """Test de la fonction de navigation"""
        mock_option_menu.return_value = "🏠 Accueil"

        result = main_module.show_navigation()

        assert result == "home"
        mock_option_menu.assert_called_once()

    @patch("app.main.st")
    @patch("app.main.option_menu")
    def test_show_navigation_consultants(self, mock_option_menu, mock_st):
        """Test de navigation vers consultants"""
        mock_option_menu.return_value = "👥 Consultants"

        result = main_module.show_navigation()

        assert result == "consultants"

    @patch("app.main.st")
    @patch("app.main.option_menu")
    def test_show_navigation_default(self, mock_option_menu, mock_st):
        """Test de navigation avec valeur inconnue (fallback)"""
        mock_option_menu.return_value = "Page inconnue"

        result = main_module.show_navigation()

        assert result == "home"

    @patch("app.main.st")
    @patch("app.main.show_navigation")
    @patch("app.main.load_module_safe")
    def test_main_successful_page_load(self, mock_load_module, mock_show_nav, mock_st):
        """Test du chargement réussi d'une page"""
        mock_show_nav.return_value = "home"
        mock_module = Mock()
        mock_module.show = Mock()
        mock_load_module.return_value = mock_module

        main_module.main()

        mock_load_module.assert_called_once_with("home")
        mock_module.show.assert_called_once()

    @patch("app.main.st")
    @patch("app.main.show_navigation")
    @patch("app.main.load_module_safe")
    def test_main_module_without_show(self, mock_load_module, mock_show_nav, mock_st):
        """Test de chargement d'un module sans fonction show"""
        mock_show_nav.return_value = "home"
        mock_module = Mock()
        del mock_module.show  # Module sans fonction show
        mock_load_module.return_value = mock_module

        main_module.main()

        mock_st.error.assert_called_once()

    @patch("app.main.st")
    @patch("app.main.show_navigation")
    @patch("app.main.load_module_safe")
    def test_main_module_load_failure(self, mock_load_module, mock_show_nav, mock_st):
        """Test d'échec de chargement de module"""
        mock_show_nav.return_value = "invalid"
        mock_load_module.return_value = None

        main_module.main()

        mock_st.error.assert_called_once_with("❌ Module invalid non disponible")

    @patch("app.main.st")
    @patch("app.main.show_navigation")
    @patch("app.main.load_module_safe")
    def test_main_page_show_error(self, mock_load_module, mock_show_nav, mock_st):
        """Test d'erreur lors de l'affichage d'une page"""
        mock_show_nav.return_value = "home"
        mock_module = Mock()
        mock_module.show.side_effect = ValueError("Test error")
        mock_load_module.return_value = mock_module

        main_module.main()

        mock_st.error.assert_called_once()
        # Vérifier qu'un expander avec les détails d'erreur est créé
        mock_st.expander.assert_called_once()

    @patch("app.main.st")
    @patch("app.main.show_navigation")
    @patch("app.main.load_module_safe")
    def test_main_critical_error(self, mock_load_module, mock_show_nav, mock_st):
        """Test d'erreur critique dans main"""
        mock_show_nav.side_effect = RuntimeError("Critical error")

        main_module.main()

        mock_st.error.assert_called_once()

    @patch("app.main.st")
    def test_show_fallback_home(self, mock_st):
        """Test de la page d'accueil de fallback"""
        main_module.show_fallback_home()

        # Vérifier que le titre est affiché
        mock_st.title.assert_called_once_with("🏠 Tableau de bord")

        # Vérifier que les métriques sont affichées
        assert mock_st.metric.call_count == 3

        # Vérifier que l'info est affichée
        mock_st.info.assert_called_once()

    @patch("app.main.st")
    @patch("app.main.show_navigation")
    @patch("app.main.load_module_safe")
    def test_main_fallback_home_display(self, mock_load_module, mock_show_nav, mock_st):
        """Test que la page fallback s'affiche quand home n'est pas disponible"""
        mock_show_nav.return_value = "home"
        mock_load_module.return_value = None

        main_module.main()

        # Vérifier que show_fallback_home est appelée implicitement
        mock_st.title.assert_called_once_with("🏠 Consultator")


class TestConstants:
    """Tests pour les constantes"""

    def test_constants_defined(self):
        """Test que les constantes sont définies"""
        assert hasattr(main_module, "CONSULTANTS_MENU_LABEL")
        assert main_module.CONSULTANTS_MENU_LABEL == "👥 Consultants"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
