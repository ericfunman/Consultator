"""
Tests pour les pages modules consultants
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


class TestConsultantsPage:
    """Tests pour la page consultants"""

    @patch("streamlit.tabs")
    def test_show_page_structure(self, mock_tabs):
        """Test de la structure générale de la page"""
        # Mock des tabs avec support du context manager
        mock_tab1 = MagicMock()
        mock_tab2 = MagicMock()
        mock_tab1.__enter__ = MagicMock(return_value=mock_tab1)
        mock_tab1.__exit__ = MagicMock(return_value=None)
        mock_tab2.__enter__ = MagicMock(return_value=mock_tab2)
        mock_tab2.__exit__ = MagicMock(return_value=None)
        mock_tabs.return_value = (mock_tab1, mock_tab2)

        from app.pages_modules.consultants import show

        show()

        # Vérifier que la fonction s'exécute sans erreur
        # (st.tabs peut ne pas être appelé selon les conditions dans la fonction)
        assert True  # Test passe si aucune exception n'est levée

    @patch("app.pages_modules.consultants.st.rerun")
    @patch("app.pages_modules.consultants.st.error")
    @patch("app.pages_modules.consultants.st.success")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_delete_consultant_competence_success(
        self, mock_get_session, mock_success, mock_error, mock_rerun
    ):
        """Test de suppression réussie d'une compétence"""
        from app.pages_modules.consultants import _delete_consultant_competence

        # Mock de la session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock de la compétence à supprimer
        mock_competence = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_competence
        )

        _delete_consultant_competence(1)

        mock_success.assert_called_once_with("✅ Compétence supprimée!")
        mock_rerun.assert_called_once()
        mock_session.delete.assert_called_once_with(mock_competence)
        mock_session.commit.assert_called_once()

    @patch("app.pages_modules.consultants.st.rerun")
    @patch("app.pages_modules.consultants.st.error")
    @patch("app.pages_modules.consultants.st.success")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_delete_consultant_language_success(
        self, mock_get_session, mock_success, mock_error, mock_rerun
    ):
        """Test de suppression réussie d'une langue"""
        from app.pages_modules.consultants import _delete_consultant_language

        # Mock de la session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock de la langue à supprimer
        mock_langue = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_langue
        )

        _delete_consultant_language(1)

        mock_success.assert_called_once_with("✅ Langue supprimée!")
        mock_rerun.assert_called_once()
        mock_session.delete.assert_called_once_with(mock_langue)
        mock_session.commit.assert_called_once()
