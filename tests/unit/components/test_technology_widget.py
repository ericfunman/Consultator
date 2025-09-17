"""
Tests unitaires pour le composant technology_widget
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.components.technology_widget import technology_multiselect


class TestTechnologyMultiselect:
    """Tests pour la fonction technology_multiselect"""

    @patch('app.components.technology_widget.st')
    @patch('app.components.technology_widget.TechnologyService')
    def test_technology_multiselect_empty_current(self, mock_tech_service, mock_st):
        """Test avec technologies actuelles vides"""
        # Mock des technologies disponibles
        mock_tech_service.get_all_available_technologies.return_value = [
            "Python", "Java", "JavaScript"
        ]

        # Mock des colonnes Streamlit
        mock_col_main = MagicMock()
        mock_col_add = MagicMock()
        mock_st.columns.return_value = [mock_col_main, mock_col_add]

        # Mock du multiselect
        mock_st.multiselect.return_value = ["Python", "JavaScript"]

        result = technology_multiselect("Test label")

        # Vérifier que les bonnes technologies sont retournées
        assert result == "Python, JavaScript"
        mock_st.multiselect.assert_called_once()

    @patch('app.components.technology_widget.st')
    @patch('app.components.technology_widget.TechnologyService')
    def test_technology_multiselect_with_current_technologies(self, mock_tech_service, mock_st):
        """Test avec technologies actuelles existantes"""
        # Mock des technologies disponibles
        mock_tech_service.get_all_available_technologies.return_value = [
            "Python", "Java", "JavaScript", "React"
        ]

        # Mock des colonnes Streamlit
        mock_col_main = MagicMock()
        mock_col_add = MagicMock()
        mock_st.columns.return_value = [mock_col_main, mock_col_add]

        # Mock du multiselect
        mock_st.multiselect.return_value = ["Python", "React"]

        result = technology_multiselect("Test label", "Python, React")

        # Vérifier que les bonnes technologies sont retournées
        assert result == "Python, React"
        mock_st.multiselect.assert_called_once()

    @patch('app.components.technology_widget.st')
    @patch('app.components.technology_widget.TechnologyService')
    def test_technology_multiselect_case_insensitive_matching(self, mock_tech_service, mock_st):
        """Test du matching insensible à la casse"""
        # Mock des technologies disponibles
        mock_tech_service.get_all_available_technologies.return_value = [
            "Python", "Java", "JavaScript"
        ]

        # Mock des colonnes Streamlit
        mock_col_main = MagicMock()
        mock_col_add = MagicMock()
        mock_st.columns.return_value = [mock_col_main, mock_col_add]

        # Mock du multiselect
        mock_st.multiselect.return_value = ["Python"]

        result = technology_multiselect("Test label", "python")  # Minuscule

        # Vérifier que Python est reconnu malgré la casse
        assert result == "Python"
        mock_st.multiselect.assert_called_once()

    @patch('app.components.technology_widget.st')
    @patch('app.components.technology_widget.TechnologyService')
    def test_technology_multiselect_invalid_current_technologies(self, mock_tech_service, mock_st):
        """Test avec technologies actuelles invalides (non dans la liste)"""
        # Mock des technologies disponibles
        mock_tech_service.get_all_available_technologies.return_value = [
            "Python", "Java", "JavaScript"
        ]

        # Mock des colonnes Streamlit
        mock_col_main = MagicMock()
        mock_col_add = MagicMock()
        mock_st.columns.return_value = [mock_col_main, mock_col_add]

        # Mock du multiselect
        mock_st.multiselect.return_value = ["Python"]

        result = technology_multiselect("Test label", "Python, InvalidTech, AnotherInvalid")

        # Seules les technologies valides devraient être présélectionnées
        mock_st.multiselect.assert_called_once()
        _, kwargs = mock_st.multiselect.call_args
        assert kwargs['default'] == ["Python"]  # InvalidTech et AnotherInvalid sont ignorés
        assert result == "Python"

    @patch('app.components.technology_widget.st')
    @patch('app.components.technology_widget.TechnologyService')
    def test_technology_multiselect_empty_string(self, mock_tech_service, mock_st):
        """Test avec chaîne vide"""
        # Mock des technologies disponibles
        mock_tech_service.get_all_available_technologies.return_value = [
            "Python", "Java", "JavaScript"
        ]

        # Mock des colonnes Streamlit
        mock_col_main = MagicMock()
        mock_col_add = MagicMock()
        mock_st.columns.return_value = [mock_col_main, mock_col_add]

        # Mock du multiselect
        mock_st.multiselect.return_value = []

        result = technology_multiselect("Test label", "")

        assert result == ""
        mock_st.multiselect.assert_called_once()

    @patch('app.components.technology_widget.st')
    @patch('app.components.technology_widget.TechnologyService')
    def test_technology_multiselect_whitespace_handling(self, mock_tech_service, mock_st):
        """Test de la gestion des espaces et virgules"""
        # Mock des technologies disponibles
        mock_tech_service.get_all_available_technologies.return_value = [
            "Python", "Java", "JavaScript"
        ]

        # Mock des colonnes Streamlit
        mock_col_main = MagicMock()
        mock_col_add = MagicMock()
        mock_st.columns.return_value = [mock_col_main, mock_col_add]

        # Mock du multiselect
        mock_st.multiselect.return_value = ["Python", "Java"]

        result = technology_multiselect("Test label", "  Python  ,  , Java  ,   ")

        # Les espaces et virgules vides devraient être nettoyés
        mock_st.multiselect.assert_called_once()
        _, kwargs = mock_st.multiselect.call_args
        assert kwargs['default'] == ["Python", "Java"]
        assert result == "Python, Java"
