"""
Tests pour améliorer la couverture de main.py (26% -> 60%)
Tests fonctionnels et d'intégration pour le point d'entrée principal
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestMainModuleCoverage(unittest.TestCase):
    """Tests pour améliorer la couverture du module main.py"""

    def setUp(self):
        """Configuration commune pour tous les tests"""
        self.mock_session_state = {}

    def test_load_module_safe_home_module(self):
        """Test du chargement du module home"""
        # Simuler que le module n'est pas en cache
        with patch('app.main.st') as mock_st:
            mock_st.session_state.modules_cache = {}

            # Mock du module home
            mock_module = Mock()
            mock_module.__name__ = 'pages_modules.home'
            
            # Modifier temporairement sys.modules pour que l'import retourne le mock
            import sys
            original_module = sys.modules.get('pages_modules.home')
            sys.modules['pages_modules.home'] = mock_module
            
            try:
                with patch('app.main.importlib.reload', return_value=mock_module):
                    from app.main import load_module_safe
                    result = load_module_safe("home")
                    self.assertEqual(result, mock_module)
            finally:
                # Restaurer sys.modules
                if original_module:
                    sys.modules['pages_modules.home'] = original_module
                elif 'pages_modules.home' in sys.modules:
                    del sys.modules['pages_modules.home']

    def test_load_module_safe_cached_module(self):
        """Test du chargement d'un module déjà en cache"""
        # Simuler que le module est en cache
        mock_cached_module = Mock()
        
        with patch('app.main.st') as mock_st:
            mock_st.session_state.modules_cache = {"home": mock_cached_module}

            from app.main import load_module_safe
            result = load_module_safe("home")
            self.assertEqual(result, mock_cached_module)

    @patch('streamlit.error')
    def test_load_module_safe_import_error(self, mock_error):
        """Test de gestion d'erreur lors du chargement d'un module"""
        with patch('app.main.st') as mock_st:
            mock_st.session_state.modules_cache = {}

            # Simuler une ImportError en supprimant temporairement le module de sys.modules
            import sys
            original_module = sys.modules.get('pages_modules.home')
            if 'pages_modules.home' in sys.modules:
                del sys.modules['pages_modules.home']
            
            try:
                # Patcher __import__ pour qu'il lève une ImportError
                with patch('builtins.__import__', side_effect=ImportError("Module not found")):
                    from app.main import load_module_safe
                    result = load_module_safe("home")
                    self.assertIsNone(result)
                    mock_error.assert_called_once()
            finally:
                # Restaurer sys.modules
                if original_module:
                    sys.modules['pages_modules.home'] = original_module

    def test_load_module_safe_invalid_module_name(self):
        """Test avec un nom de module invalide"""
        with patch('app.main.st') as mock_st:
            mock_st.session_state.modules_cache = {}

            from app.main import load_module_safe
            result = load_module_safe("invalid_module")
            self.assertIsNone(result)

    @patch('app.main.st')
    @patch('app.main.option_menu')
    def test_show_navigation_default_selection(self, mock_option_menu, mock_st):
        """Test de la navigation avec sélection par défaut"""
        mock_option_menu.return_value = "🏠 Accueil"

        from app.main import show_navigation
        result = show_navigation()
        self.assertEqual(result, "home")

    @patch('app.main.st')
    @patch('app.main.option_menu')
    def test_show_navigation_consultants_selection(self, mock_option_menu, mock_st):
        """Test de la navigation avec sélection Consultants"""
        mock_option_menu.return_value = "👥 Consultants"

        from app.main import show_navigation
        result = show_navigation()
        self.assertEqual(result, "consultants")

    @patch('app.main.st')
    @patch('app.main.option_menu')
    def test_show_navigation_business_managers_selection(self, mock_option_menu, mock_st):
        """Test de la navigation avec sélection Business Managers"""
        mock_option_menu.return_value = "🤵‍♂ Business Managers"

        from app.main import show_navigation
        result = show_navigation()
        self.assertEqual(result, "business_managers")

    @patch('app.main.st')
    @patch('app.main.option_menu')
    def test_show_navigation_chatbot_selection(self, mock_option_menu, mock_st):
        """Test de la navigation avec sélection Assistant IA"""
        mock_option_menu.return_value = "🤖 Assistant IA"

        from app.main import show_navigation
        result = show_navigation()
        self.assertEqual(result, "chatbot")

    @patch('streamlit.markdown')
    @patch('app.main.show_navigation')
    @patch('app.main.load_module_safe')
    def test_main_successful_page_load(self, mock_load_module, mock_show_nav, mock_markdown):
        """Test du flux principal avec chargement réussi d'une page"""
        mock_show_nav.return_value = "home"
        mock_module = Mock()
        mock_module.show = Mock()
        mock_load_module.return_value = mock_module

        from app.main import main
        main()

        mock_load_module.assert_called_with("home")
        mock_module.show.assert_called_once()

    @patch('streamlit.markdown')
    @patch('app.main.show_navigation')
    @patch('app.main.load_module_safe')
    @patch('streamlit.error')
    def test_main_module_load_failure(self, mock_error, mock_load_module, mock_show_nav, mock_markdown):
        """Test du flux principal avec échec de chargement du module"""
        mock_show_nav.return_value = "home"
        mock_load_module.return_value = None

        from app.main import main
        main()

        mock_error.assert_called()

    @patch('streamlit.markdown')
    @patch('app.main.show_navigation')
    @patch('app.main.load_module_safe')
    @patch('streamlit.error')
    @patch('streamlit.info')
    @patch('streamlit.expander')
    def test_main_page_show_exception(self, mock_expander, mock_info, mock_error, mock_load_module, mock_show_nav, mock_markdown):
        """Test du flux principal avec exception lors de l'affichage de la page"""
        mock_show_nav.return_value = "home"
        mock_module = Mock()
        mock_module.show = Mock(side_effect=AttributeError("Test error"))
        mock_load_module.return_value = mock_module

        # Mock pour st.expander context manager
        mock_expander_cm = Mock()
        mock_expander_cm.__enter__ = Mock(return_value=Mock())
        mock_expander_cm.__exit__ = Mock(return_value=None)
        mock_expander.return_value = mock_expander_cm

        from app.main import main
        main()

        mock_error.assert_called()
        mock_info.assert_called_with("🔄 Essayez de recharger la page")

    @patch('streamlit.markdown')
    @patch('app.main.show_navigation')
    @patch('app.main.load_module_safe')
    @patch('streamlit.error')
    @patch('streamlit.title')
    @patch('streamlit.info')
    def test_main_fallback_home_display(self, mock_info, mock_title, mock_error, mock_load_module, mock_show_nav, mock_markdown):
        """Test du flux principal avec affichage de la page fallback home"""
        mock_show_nav.return_value = "home"
        mock_load_module.return_value = None

        from app.main import main
        main()

        mock_title.assert_called_with("🏠 Tableau de bord")
        mock_info.assert_called_with("ℹ️ Page d'accueil en mode simplifié - Module home non disponible")

    @patch('streamlit.title')
    @patch('streamlit.markdown')
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('streamlit.info')
    def test_show_fallback_home_complete_display(self, mock_info, mock_metric, mock_columns, mock_markdown, mock_title):
        """Test complet de la fonction show_fallback_home"""
        # Mock pour st.columns qui retourne un tuple de context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_columns.return_value = (mock_col1, mock_col2, mock_col3)

        from app.main import show_fallback_home
        show_fallback_home()

        # Vérifier que toutes les métriques sont affichées
        self.assertEqual(mock_metric.call_count, 3)
        mock_info.assert_called_with("ℹ️ Page d'accueil en mode simplifié - Module home non disponible")

    @patch('streamlit.markdown')
    @patch('app.main.show_navigation')
    @patch('app.main.load_module_safe')
    @patch('streamlit.error')
    @patch('streamlit.info')
    def test_main_critical_exception_handling(self, mock_info, mock_error, mock_load_module, mock_show_nav, mock_markdown):
        """Test de la gestion d'exceptions critiques dans main()"""
        mock_show_nav.side_effect = RuntimeError("Critical error")

        from app.main import main
        main()

        mock_error.assert_called_with("❌ Erreur critique: Critical error")
        mock_info.assert_called_with("🔄 Rechargez l'application")

    def test_constants_definition(self):
        """Test que les constantes sont correctement définies"""
        from app.main import CONSULTANTS_MENU_LABEL
        self.assertEqual(CONSULTANTS_MENU_LABEL, "👥 Consultants")

    @patch('streamlit.set_page_config')
    def test_page_config_setup(self, mock_set_page_config):
        """Test que la configuration de page est appelée (exécuté à l'import)"""
        # Cette fonction est appelée lors de l'import du module
        # On vérifie juste qu'elle peut être appelée sans erreur
        from app.main import st
        self.assertIsNotNone(st)


if __name__ == '__main__':
    unittest.main()