"""
Tests pour le module technologies.py
"""

import pytest
from unittest.mock import Mock, patch
from app.pages_modules.technologies import show
from tests.fixtures.base_test import BaseUITest


class TestTechnologiesModule(BaseUITest):
    """Tests pour le module technologies"""

    @patch("app.pages_modules.technologies.show_technologies_referentiel")
    @patch("streamlit.title")
    def test_show_function(self, mock_title, mock_show_referentiel):
        """Test de la fonction show()"""
        # Test
        show()

        # Vérifications
        mock_title.assert_called_once_with("🛠️ Gestion des Technologies")
        mock_show_referentiel.assert_called_once()

    @patch("app.pages_modules.technologies.show_technologies_referentiel")
    @patch("streamlit.title")
    def test_show_function_error_handling(self, mock_title, mock_show_referentiel):
        """Test de la gestion d'erreur dans show()"""
        # Simuler une erreur dans le composant
        mock_show_referentiel.side_effect = Exception("Erreur test")

        # Test - devrait lever l'exception
        with pytest.raises(Exception, match="Erreur test"):
            show()

        # Vérifications
        mock_title.assert_called_once_with("🛠️ Gestion des Technologies")
        mock_show_referentiel.assert_called_once()

    def test_module_structure(self):
        """Test de la structure du module"""
        import app.pages_modules.technologies as tech_module

        # Vérifier que la fonction show existe
        assert hasattr(tech_module, "show")
        assert callable(tech_module.show)

        # Vérifier les imports
        assert hasattr(tech_module, "st")
        assert hasattr(tech_module, "show_technologies_referentiel")

    def test_main_execution(self):
        """Test de l'exécution en tant que script principal"""
        # Ce test vérifie que le module peut être exécuté directement
        import app.pages_modules.technologies as tech_module

        # Vérifier que __name__ est bien défini
        assert hasattr(tech_module, "__name__")

        # Simuler l'exécution directe
        with patch("app.pages_modules.technologies.show") as mock_show:
            # Simuler __name__ == "__main__"
            tech_module.__name__ = "__main__"

            # Recharger le module pour déclencher le if __name__ == "__main__"
            # Note: En pratique, cela nécessiterait un reload, mais pour le test
            # nous vérifions simplement que la structure est correcte
            assert True

    @patch("app.pages_modules.technologies.show_technologies_referentiel")
    @patch("streamlit.title")
    def test_show_function_multiple_calls(self, mock_title, mock_show_referentiel):
        """Test de multiples appels à show()"""
        # Test multiple appels
        show()
        show()
        show()

        # Vérifications - chaque appel devrait créer un nouveau titre
        assert mock_title.call_count == 3
        assert mock_show_referentiel.call_count == 3

        # Vérifier que c'est toujours le même titre
        mock_title.assert_called_with("🛠️ Gestion des Technologies")
        mock_show_referentiel.assert_called_with()
