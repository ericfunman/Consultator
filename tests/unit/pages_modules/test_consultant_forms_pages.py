"""
Tests pour les pages modules consultant forms
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Ajouter le r�pertoire parent au path pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class TestConsultantList:
    """Tests pour l'affichage de la liste des consultants"""

    @patch("app.pages_modules.consultant_list.st")
    @patch("app.pages_modules.consultant_list.get_database_session")
    def test_show_consultants_list_error(self, mock_get_session, mock_st):
        """Test de l'affichage avec erreur du service"""
        # Mock de la session qui l�ve une exception
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.side_effect = Exception("Erreur DB")

        from app.pages_modules.consultant_list import show_consultants_list

        show_consultants_list()

        # V�rifier qu'une erreur est affich�e
        mock_st.error.assert_called_with("? Erreur lors du chargement de la liste des consultants: Erreur DB")


class TestConsultantProfile:
    """Tests pour l'affichage du profil consultant"""

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_consultant_profile_success(self, mock_st):
        """Test de l'affichage du profil consultant"""
        # Mock du session state
        mock_st.session_state.view_consultant_profile = 1

        from app.pages_modules.consultant_profile import show_consultant_profile

        # Test que la fonction s'ex�cute sans erreur
        try:
            show_consultant_profile()
            success = True
        except Exception as exc:
            success = False

        assert success, "La fonction devrait s'ex�cuter sans erreur"

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_consultant_profile_not_found(self, mock_st):
        """Test de l'affichage quand le consultant n'est pas trouv�"""
        # Mock du session state
        mock_st.session_state.view_consultant_profile = 999

        # Mock de la session et de la query qui retourne None
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        with patch('app.pages_modules.consultant_profile.get_database_session') as mock_get_session:
            mock_get_session.return_value.__enter__.return_value = mock_session
            mock_get_session.return_value.__exit__.return_value = None

            from app.pages_modules.consultant_profile import show_consultant_profile

            show_consultant_profile()

            # V�rifier qu'une erreur est affich�e
            mock_st.error.assert_called_with("? Consultant introuvable (ID: 999)")

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_consultant_profile_error(self, mock_st):
        """Test de l'affichage avec erreur du service"""
        # Mock du session state
        mock_st.session_state.view_consultant_profile = 1

        # Mock de la session qui l�ve une exception
        with patch('app.pages_modules.consultant_profile.get_database_session') as mock_get_session:
            mock_get_session.return_value.__enter__.side_effect = Exception("Erreur DB")

            from app.pages_modules.consultant_profile import show_consultant_profile

            show_consultant_profile()

            # V�rifier qu'une erreur est affich�e
            mock_st.error.assert_called()
