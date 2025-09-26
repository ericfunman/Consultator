"""
Tests de couverture complète pour technology_widget.py
Visant 90%+ de couverture pour améliorer le score global
"""

from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

import pytest

from app.components.technology_widget import TECHNOLOGY_CATEGORIES
from app.components.technology_widget import _add_custom_technology_if_needed
from app.components.technology_widget import _display_custom_technologies_list
from app.components.technology_widget import _display_search_results
from app.components.technology_widget import _display_technologies_by_category
from app.components.technology_widget import _handle_add_technology
from app.components.technology_widget import _handle_delete_technology
from app.components.technology_widget import _handle_form_submission
from app.components.technology_widget import _parse_current_technologies
from app.components.technology_widget import _render_add_technology_form
from app.components.technology_widget import _render_add_technology_form_main
from app.components.technology_widget import _render_add_technology_tab
from app.components.technology_widget import _render_multiselect_interface
from app.components.technology_widget import _render_technologies_search_tab
from app.components.technology_widget import show_technologies_referentiel


class TestParseTechnologies:
    """Tests pour _parse_current_technologies"""

    def test_parse_empty_technologies(self):
        """Test avec technologies vides"""
        result = _parse_current_technologies("", ["Python", "Java"])
        assert result == []

        result = _parse_current_technologies(None, ["Python", "Java"])
        assert result == []

    def test_parse_exact_match(self):
        """Test avec correspondance exacte"""
        all_techs = ["Python", "Java", "JavaScript"]
        result = _parse_current_technologies("Python, Java", all_techs)
        assert result == ["Python", "Java"]

    def test_parse_case_insensitive(self):
        """Test correspondance insensible à la casse"""
        all_techs = ["Python", "Java", "JavaScript"]
        result = _parse_current_technologies("python, JAVA", all_techs)
        assert result == ["Python", "Java"]

    @patch("app.components.technology_widget._add_custom_technology_if_needed")
    def test_parse_custom_technology(self, mock_add_custom):
        """Test ajout technologie personnalisée"""
        mock_add_custom.return_value = True
        all_techs = ["Python", "Java"]
        result = _parse_current_technologies("Python, CustomTech", all_techs)
        assert result == ["Python", "CustomTech"]
        mock_add_custom.assert_called_once_with("CustomTech")

    def test_parse_whitespace_handling(self):
        """Test gestion des espaces"""
        all_techs = ["Python", "Java", "JavaScript"]
        result = _parse_current_technologies("  Python  ,   Java   ", all_techs)
        assert result == ["Python", "Java"]


class TestAddCustomTechnology:
    """Tests pour _add_custom_technology_if_needed"""

    @patch("app.components.technology_widget.TechnologyService")
    def test_add_custom_technology(self, mock_tech_service):
        """Test ajout technologie personnalisée"""
        mock_tech_service.add_custom_technology.return_value = True
        result = _add_custom_technology_if_needed("CustomTech")
        assert result is True
        mock_tech_service.add_custom_technology.assert_called_once_with(
            "CustomTech", "Personnalisés"
        )


class TestRenderAddTechnologyForm:
    """Tests pour _render_add_technology_form"""

    @patch("app.components.technology_widget.st")
    def test_form_not_shown_when_flag_false(self, mock_st):
        """Test formulaire non affiché quand flag = False"""
        mock_st.session_state.get.return_value = False
        _render_add_technology_form("test_key")
        mock_st.expander.assert_not_called()

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget._handle_add_technology")
    def test_form_shown_and_handled(self, mock_handle_add, mock_st):
        """Test formulaire affiché et gestion des actions"""
        # Setup session state
        mock_st.session_state.get.return_value = True

        # Mock form elements
        mock_st.text_input.return_value = "NewTech"
        mock_st.selectbox.return_value = "Personnalisés"

        # Mock columns
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        # Mock buttons - confirm button clicked
        mock_col1.__enter__.return_value = mock_col1
        mock_col2.__enter__.return_value = mock_col2
        mock_st.button.side_effect = [True, False]  # Confirm=True, Cancel=False

        _render_add_technology_form("test_key")

        # Verify form elements were called
        mock_st.expander.assert_called_once()
        mock_st.text_input.assert_called_once()
        mock_st.selectbox.assert_called_once()
        mock_handle_add.assert_called_once_with("NewTech", "Personnalisés", "test_key")

    @patch("app.components.technology_widget.st")
    def test_form_cancel_button(self, mock_st):
        """Test bouton annuler"""
        # Setup session state
        mock_st.session_state.get.return_value = True

        # Mock form elements
        mock_st.text_input.return_value = "NewTech"
        mock_st.selectbox.return_value = "Personnalisés"

        # Mock columns
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        # Mock buttons - cancel button clicked
        mock_col1.__enter__.return_value = mock_col1
        mock_col2.__enter__.return_value = mock_col2
        mock_st.button.side_effect = [False, True]

        _render_add_technology_form("test_key")

        # Verify rerun is called when cancel button is clicked
        mock_st.rerun.assert_called_once()


class TestHandleAddTechnology:
    """Tests pour _handle_add_technology"""

    @patch("app.components.technology_widget.st")
    def test_handle_add_empty_name(self, mock_st):
        """Test avec nom vide"""
        _handle_add_technology("", "Personnalisés", "test_key")
        mock_st.error.assert_called_once_with(
            "⚠️ Veuillez saisir le nom de la technologie"
        )

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    def test_handle_add_success(self, mock_tech_service, mock_st):
        """Test ajout réussi"""
        mock_tech_service.add_custom_technology.return_value = True
        mock_st.session_state = {}

        _handle_add_technology("NewTech", "Personnalisés", "test_key")

        mock_tech_service.add_custom_technology.assert_called_once_with(
            "NewTech", "Personnalisés"
        )
        mock_st.success.assert_called_once_with("✅ Technologie 'NewTech' ajoutée !")
        assert mock_st.session_state.get("show_add_tech_test_key") == False
        mock_st.rerun.assert_called_once()

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    def test_handle_add_already_exists(self, mock_tech_service, mock_st):
        """Test technologie déjà existante"""
        mock_tech_service.add_custom_technology.return_value = False

        _handle_add_technology("ExistingTech", "Personnalisés", "test_key")

        mock_st.error.assert_called_once_with("❌ Cette technologie existe déjà")


class TestRenderMultiselectInterface:
    """Tests pour _render_multiselect_interface"""

    @patch("app.components.technology_widget.st")
    def test_multiselect_interface(self, mock_st):
        """Test interface multiselect"""
        # Mock columns
        mock_col_main, mock_col_other = MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col_main, mock_col_other]

        # Mock multiselect return
        mock_st.multiselect.return_value = ["Python", "Java"]

        # Mock button not clicked
        mock_st.button.return_value = False

        all_techs = ["Python", "Java", "JavaScript"]
        current_techs = ["Python"]

        result = _render_multiselect_interface(
            "Test Label", all_techs, current_techs, "test_key", "Help text"
        )

        assert result == ["Python", "Java"]
        mock_st.multiselect.assert_called_once()
        mock_st.button.assert_called_once()

    @patch("app.components.technology_widget.st")
    def test_multiselect_add_button_clicked(self, mock_st):
        """Test clic sur bouton ajouter"""
        # Mock columns
        mock_col_main, mock_col_other = MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col_main, mock_col_other]

        # Mock multiselect return
        mock_st.multiselect.return_value = ["Python"]

        # Mock button clicked
        mock_st.button.return_value = True
        mock_st.session_state = {}

        all_techs = ["Python", "Java"]
        current_techs = ["Python"]

        result = _render_multiselect_interface(
            "Test Label", all_techs, current_techs, "test_key", None
        )

        assert result == ["Python"]
        assert mock_st.session_state.get("show_add_tech_test_key") == True


class TestRenderTechnologiesSearchTab:
    """Tests pour _render_technologies_search_tab"""

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    @patch("app.components.technology_widget._display_search_results")
    def test_search_with_query(self, mock_display_search, mock_tech_service, mock_st):
        """Test recherche avec query"""
        mock_st.text_input.return_value = "Python"
        mock_tech_service.get_technologies_by_category.return_value = {}

        _render_technologies_search_tab()

        mock_display_search.assert_called_once_with("Python")

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    @patch("app.components.technology_widget._display_technologies_by_category")
    def test_search_without_query(self, mock_display_cat, mock_tech_service, mock_st):
        """Test sans query de recherche"""
        mock_st.text_input.return_value = ""
        mock_tech_service.get_technologies_by_category.return_value = {
            "Test": ["Python"]
        }

        _render_technologies_search_tab()

        mock_display_cat.assert_called_once_with({"Test": ["Python"]})


class TestDisplaySearchResults:
    """Tests pour _display_search_results"""

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    def test_display_search_results(self, mock_tech_service, mock_st):
        """Test affichage résultats de recherche"""
        mock_tech_service.search_technologies.return_value = [
            "Python",
            "PyTorch",
            "Pandas",
        ]

        # Mock columns
        mock_cols = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols

        _display_search_results("Py")

        mock_tech_service.search_technologies.assert_called_once_with("Py")
        mock_st.write.assert_called()  # Called for count and results


class TestDisplayTechnologiesByCategory:
    """Tests pour _display_technologies_by_category"""

    @patch("app.components.technology_widget.st")
    def test_display_by_category(self, mock_st):
        """Test affichage par catégorie"""
        technologies = {
            "Langages": ["Python", "Java", "JavaScript"],
            "Frameworks": ["React", "Django"],
        }

        # Mock expander and columns
        mock_expander = MagicMock()
        mock_st.expander.return_value = mock_expander
        mock_cols = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols

        _display_technologies_by_category(technologies)

        # Should create expander for each category
        assert mock_st.expander.call_count == 2
        # Verify expander calls - en considérant les appels de contexte
        expander_calls = [call[0][0] for call in mock_st.expander.call_args_list]
        expected_titles = [
            "📁 Langages (3 technologies)",
            "📁 Frameworks (2 technologies)",
        ]
        assert expander_calls == expected_titles


class TestRenderAddTechnologyTab:
    """Tests pour _render_add_technology_tab"""

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget._render_add_technology_form_main")
    @patch("app.components.technology_widget._display_custom_technologies_list")
    def test_render_add_technology_tab(
        self, mock_display_list, mock_render_form, mock_st
    ):
        """Test rendu onglet d'ajout"""
        _render_add_technology_tab()

        mock_st.markdown.assert_called()  # Multiple markdown calls
        mock_render_form.assert_called_once()
        mock_display_list.assert_called_once()


class TestRenderAddTechnologyFormMain:
    """Tests pour _render_add_technology_form_main"""

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget._handle_form_submission")
    def test_form_main_submit(self, mock_handle_submission, mock_st):
        """Test soumission formulaire principal"""
        # Mock form elements
        mock_st.text_input.return_value = "NewTech"
        mock_st.selectbox.return_value = "Personnalisés"
        mock_st.text_area.return_value = "Description"
        mock_st.form_submit_button.return_value = True

        _render_add_technology_form_main()

        mock_handle_submission.assert_called_once_with("NewTech", "Personnalisés")

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget._handle_form_submission")
    def test_form_main_no_submit(self, mock_handle_submission, mock_st):
        """Test sans soumission"""
        mock_st.form_submit_button.return_value = False

        _render_add_technology_form_main()

        mock_handle_submission.assert_not_called()


class TestHandleFormSubmission:
    """Tests pour _handle_form_submission"""

    @patch("app.components.technology_widget.st")
    def test_handle_form_empty_name(self, mock_st):
        """Test soumission avec nom vide"""
        _handle_form_submission("", "Personnalisés")
        mock_st.error.assert_called_once_with(
            "⚠️ Veuillez saisir le nom de la technologie"
        )

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    def test_handle_form_success(self, mock_tech_service, mock_st):
        """Test soumission réussie"""
        mock_tech_service.add_custom_technology.return_value = True

        _handle_form_submission("NewTech", "Personnalisés")

        mock_tech_service.add_custom_technology.assert_called_once_with(
            "NewTech", "Personnalisés"
        )
        mock_st.success.assert_called_once_with(
            "✅ Technologie 'NewTech' ajoutée avec succès !"
        )
        mock_st.rerun.assert_called_once()

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    def test_handle_form_already_exists(self, mock_tech_service, mock_st):
        """Test technologie déjà existante"""
        mock_tech_service.add_custom_technology.return_value = False

        _handle_form_submission("ExistingTech", "Personnalisés")

        mock_st.error.assert_called_once_with("❌ Cette technologie existe déjà")


class TestDisplayCustomTechnologiesList:
    """Tests pour _display_custom_technologies_list"""

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    def test_display_empty_custom_list(self, mock_tech_service, mock_st):
        """Test liste personnalisées vide"""
        mock_tech_service.get_custom_technologies.return_value = []

        _display_custom_technologies_list()

        mock_st.info.assert_called_once_with(
            "ℹ️ Aucune technologie personnalisée ajoutée"
        )

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    @patch("app.components.technology_widget._handle_delete_technology")
    def test_display_custom_list_with_items(
        self, mock_handle_delete, mock_tech_service, mock_st
    ):
        """Test liste avec technologies personnalisées"""
        custom_techs = [
            {"id": 1, "nom": "CustomTech1", "categorie": "Personnalisés"},
            {"id": 2, "nom": "CustomTech2", "categorie": "Custom"},
        ]
        mock_tech_service.get_custom_technologies.return_value = custom_techs

        # Mock columns
        mock_cols = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.columns.return_value = mock_cols

        # Mock delete button clicked for first tech
        mock_st.button.side_effect = [True, False]  # First delete clicked, second not

        _display_custom_technologies_list()

        # Should call columns for each tech
        assert mock_st.columns.call_count == 2
        mock_handle_delete.assert_called_once_with(1)


class TestHandleDeleteTechnology:
    """Tests pour _handle_delete_technology"""

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    def test_handle_delete_success(self, mock_tech_service, mock_st):
        """Test suppression réussie"""
        mock_tech_service.delete_custom_technology.return_value = True

        _handle_delete_technology(1)

        mock_tech_service.delete_custom_technology.assert_called_once_with(1)
        mock_st.success.assert_called_once_with("✅ Technologie supprimée !")
        mock_st.rerun.assert_called_once()

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget.TechnologyService")
    def test_handle_delete_failure(self, mock_tech_service, mock_st):
        """Test échec suppression"""
        mock_tech_service.delete_custom_technology.return_value = False

        _handle_delete_technology(1)

        mock_tech_service.delete_custom_technology.assert_called_once_with(1)
        mock_st.success.assert_not_called()
        mock_st.rerun.assert_not_called()


class TestShowTechnologiesReferentiel:
    """Tests pour show_technologies_referentiel"""

    @patch("app.components.technology_widget.st")
    @patch("app.components.technology_widget._render_technologies_search_tab")
    @patch("app.components.technology_widget._render_add_technology_tab")
    def test_show_technologies_referentiel(
        self, mock_render_add_tab, mock_render_search_tab, mock_st
    ):
        """Test affichage principal référentiel"""
        # Mock tabs
        mock_tab1, mock_tab2 = MagicMock(), MagicMock()
        mock_st.tabs.return_value = [mock_tab1, mock_tab2]

        show_technologies_referentiel()

        mock_st.subheader.assert_called_once_with("📚 Référentiel des Technologies")
        mock_st.tabs.assert_called_once()
        mock_render_search_tab.assert_called_once()
        mock_render_add_tab.assert_called_once()


class TestConstants:
    """Tests pour les constantes"""

    def test_technology_categories_defined(self):
        """Test que les catégories sont définies"""
        assert isinstance(TECHNOLOGY_CATEGORIES, list)
        assert len(TECHNOLOGY_CATEGORIES) > 0
        assert "Personnalisés" in TECHNOLOGY_CATEGORIES
        assert "Langages de programmation" in TECHNOLOGY_CATEGORIES
