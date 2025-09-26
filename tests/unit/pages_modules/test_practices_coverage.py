"""
Tests pour practices.py - Couverture complète
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pandas as pd
import pytest

# Mock de pandas si nécessaire
pd_mock = MagicMock() if pd is None else pd


class TestPracticesPage:
    """Tests pour la page practices.py"""

    @patch("app.pages_modules.practices.st.title")
    @patch("app.pages_modules.practices.st.tabs")
    @patch("app.pages_modules.practices.st.columns")
    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.st.button")
    @patch("app.pages_modules.practices.st.subheader")
    @patch("app.pages_modules.practices.st.expander")
    @patch("app.pages_modules.practices.PracticeService.get_all_practices")
    def test_show_main_function(
        self,
        mock_get_practices,
        mock_expander,
        mock_subheader,
        mock_button,
        mock_write,
        mock_columns,
        mock_tabs,
        mock_title,
    ):
        """Test de la fonction principale show()"""
        from app.pages_modules.practices import show

        # Configuration des mocks
        mock_tab1, mock_tab2, mock_tab3 = MagicMock(), MagicMock(), MagicMock()
        mock_tabs.return_value = (mock_tab1, mock_tab2, mock_tab3)

        # Mock pour éviter les appels à la vraie DB
        mock_get_practices.return_value = []

        # Mock st.columns pour toutes les utilisations
        mock_columns.return_value = (MagicMock(), MagicMock(), MagicMock())

        # Mock expander context
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = mock_expander_context
        mock_expander.return_value.__exit__ = MagicMock()

        # Appel de la fonction
        show()

        # Vérifications
        mock_title.assert_called_once_with("🏢 Gestion des Practices")
        # st.tabs est appelé plusieurs fois (dans show() et dans les fonctions internes)
        assert mock_tabs.call_count >= 1

    @patch("app.pages_modules.practices.st.subheader")
    @patch("app.pages_modules.practices.st.columns")
    @patch("app.pages_modules.practices.st.metric")
    @patch("app.pages_modules.practices.st.expander")
    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.PracticeService.get_practice_statistics")
    @patch("app.pages_modules.practices.PracticeService.get_all_practices")
    def test_show_practice_overview_with_data(
        self,
        mock_get_all,
        mock_get_stats,
        mock_write,
        mock_expander,
        mock_metric,
        mock_columns,
        mock_subheader,
    ):
        """Test de show_practice_overview avec données"""
        from app.pages_modules.practices import show_practice_overview

        # Mock des données
        mock_stats = {
            "total_practices": 5,
            "total_consultants": 25,
            "active_practices": 4,
        }
        mock_get_stats.return_value = mock_stats

        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"
        mock_practice.description = "Description test"
        mock_practice.responsable = "John Doe"
        mock_practice.actif = True
        mock_get_all.return_value = [mock_practice]

        # Configuration des mocks UI
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_columns.return_value = (mock_col1, mock_col2, mock_col3)
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = mock_expander_context
        mock_expander.return_value.__exit__ = MagicMock()

        # Appel de la fonction
        show_practice_overview()

        # Vérifications
        mock_subheader.assert_any_call("📊 Vue d'ensemble des Practices")
        mock_subheader.assert_any_call("Liste des Practices")
        mock_get_stats.assert_called_once()
        mock_get_all.assert_called_once()
        mock_columns.assert_called_once_with(3)
        mock_metric.assert_any_call("Total Practices", 5)
        mock_metric.assert_any_call("Consultants assignés", 25)
        mock_metric.assert_any_call("Practices actives", 4)

    @patch("app.pages_modules.practices.st.error")
    @patch("app.pages_modules.practices.PracticeService.get_practice_statistics")
    def test_show_practice_overview_with_error(self, mock_get_stats, mock_error):
        """Test de show_practice_overview avec erreur"""
        from app.pages_modules.practices import show_practice_overview

        # Mock d'erreur
        mock_get_stats.side_effect = Exception("Test error")

        # Appel de la fonction
        show_practice_overview()

        # Vérifications
        mock_error.assert_called_once()
        assert "Erreur lors du chargement" in mock_error.call_args[0][0]

    @patch("app.pages_modules.practices.st.subheader")
    @patch("app.pages_modules.practices.st.warning")
    @patch("app.pages_modules.practices.PracticeService.get_all_practices")
    @patch("app.pages_modules.practices._display_practice_interface")
    def test_show_consultants_by_practice_no_practices(
        self, mock_display, mock_get_all, mock_warning, mock_subheader
    ):
        """Test de show_consultants_by_practice sans practices"""
        from app.pages_modules.practices import show_consultants_by_practice

        # Mock aucune practice
        mock_get_all.return_value = []

        # Appel de la fonction
        show_consultants_by_practice()

        # Vérifications
        mock_subheader.assert_called_with("👥 Consultants par Practice")
        mock_get_all.assert_called_once()
        mock_warning.assert_called_with("Aucune practice trouvée.")
        mock_display.assert_not_called()

    @patch("app.pages_modules.practices.st.subheader")
    @patch("app.pages_modules.practices.st.error")
    @patch("app.pages_modules.practices.st.exception")
    @patch("app.pages_modules.practices.PracticeService.get_all_practices")
    def test_show_consultants_by_practice_with_error(
        self, mock_get_all, mock_exception, mock_error, mock_subheader
    ):
        """Test de show_consultants_by_practice avec erreur"""
        from app.pages_modules.practices import show_consultants_by_practice

        # Mock d'erreur
        mock_get_all.side_effect = Exception("Test error")

        # Appel de la fonction
        show_consultants_by_practice()

        # Vérifications
        mock_subheader.assert_called_with("👥 Consultants par Practice")
        mock_error.assert_called_once()
        mock_exception.assert_called_once()

    @patch("app.pages_modules.practices.st.columns")
    @patch("app.pages_modules.practices.st.selectbox")
    @patch("app.pages_modules.practices._display_practice_tabs")
    def test_display_practice_interface_with_selection(
        self, mock_display_tabs, mock_selectbox, mock_columns
    ):
        """Test de _display_practice_interface avec sélection"""
        from app.pages_modules.practices import _display_practice_interface

        # Mock des practices
        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"
        practices = [mock_practice]

        # Mock du selectbox
        mock_selectbox.return_value = mock_practice

        # Mock des colonnes (st.columns([2, 1]) retourne 2 éléments)
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_columns.return_value = (mock_col1, mock_col2)

        # Appel de la fonction
        _display_practice_interface(practices)

        # Vérifications
        mock_columns.assert_called_once_with([2, 1])
        mock_selectbox.assert_called_once()
        mock_display_tabs.assert_called_once_with(mock_practice)

    @patch("app.pages_modules.practices.st.tabs")
    @patch("app.pages_modules.practices._display_consultants_list_tab")
    @patch("app.pages_modules.practices._display_assign_consultant_tab")
    @patch("app.pages_modules.practices._display_practice_actions_tab")
    def test_display_practice_tabs(
        self, mock_actions_tab, mock_assign_tab, mock_list_tab, mock_tabs
    ):
        """Test de _display_practice_tabs"""
        from app.pages_modules.practices import _display_practice_tabs

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.id = 1
        mock_practice.nom = "Test Practice"

        # Configuration des mocks
        mock_tab1, mock_tab2, mock_tab3 = MagicMock(), MagicMock(), MagicMock()
        mock_tabs.return_value = (mock_tab1, mock_tab2, mock_tab3)

        # Appel de la fonction
        _display_practice_tabs(mock_practice)

        # Vérifications
        mock_tabs.assert_called_once()
        mock_list_tab.assert_called_once_with(mock_practice)
        mock_assign_tab.assert_called_once_with(mock_practice)
        mock_actions_tab.assert_called_once_with(mock_practice)

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.st.info")
    @patch("app.pages_modules.practices.PracticeService.get_consultants_by_practice")
    @patch("app.pages_modules.practices._render_consultants_table")
    def test_display_consultants_list_tab_with_data(
        self, mock_render_table, mock_get_consultants, mock_info, mock_write
    ):
        """Test de _display_consultants_list_tab avec données"""
        from app.pages_modules.practices import _display_consultants_list_tab

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.id = 1

        # Mock des consultants
        mock_get_consultants.return_value = {
            "Test Practice": ["consultant1", "consultant2"]
        }

        # Appel de la fonction
        _display_consultants_list_tab(mock_practice)

        # Vérifications
        mock_get_consultants.assert_called_once_with(1)
        mock_render_table.assert_called_once()
        mock_info.assert_not_called()

    @patch("app.pages_modules.practices.st.info")
    @patch("app.pages_modules.practices.PracticeService.get_consultants_by_practice")
    def test_display_consultants_list_tab_no_data(
        self, mock_get_consultants, mock_info
    ):
        """Test de _display_consultants_list_tab sans données"""
        from app.pages_modules.practices import _display_consultants_list_tab

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.id = 1

        # Mock aucun consultant
        mock_get_consultants.return_value = None

        # Appel de la fonction
        _display_consultants_list_tab(mock_practice)

        # Vérifications
        mock_get_consultants.assert_called_once_with(1)
        mock_info.assert_called_with("Aucun consultant assigné à cette practice.")

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices._display_consultants_dataframe")
    @patch("app.pages_modules.practices._display_remove_consultant_section")
    @patch("app.pages_modules.practices._prepare_consultants_table_data")
    def test_render_consultants_table_with_data(
        self, mock_prepare_data, mock_remove_section, mock_display_df, mock_write
    ):
        """Test de _render_consultants_table avec données"""
        from app.pages_modules.practices import _render_consultants_table

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Mock des consultants
        mock_consultant1 = MagicMock()
        mock_consultant1.id = 1
        mock_consultant1.nom = "Doe"
        mock_consultant1.prenom = "John"
        mock_consultant1.email = "john@test.com"
        mock_consultant1.grade = "Senior"
        mock_consultant1.disponibilite = True
        mock_consultant1.salaire_actuel = 50000

        consultants = [mock_consultant1]
        consultants_dict = {"Test Practice": consultants}

        # Mock des données préparées
        mock_prepare_data.return_value = [{"ID": 1, "Nom": "Doe", "Prénom": "John"}]

        # Appel de la fonction
        _render_consultants_table(consultants_dict, mock_practice)

        # Vérifications
        mock_write.assert_called_with(
            "**1 consultant(s) dans la practice Test Practice**"
        )
        mock_prepare_data.assert_called_once_with(consultants)
        mock_display_df.assert_called_once()
        mock_remove_section.assert_called_once()

    def test_prepare_consultants_table_data(self):
        """Test de _prepare_consultants_table_data"""
        from app.pages_modules.practices import _prepare_consultants_table_data

        # Mock des consultants
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.nom = "Doe"
        mock_consultant.prenom = "John"
        mock_consultant.email = "john@test.com"
        mock_consultant.grade = "Senior"
        mock_consultant.disponibilite = True
        mock_consultant.salaire_actuel = 50000

        consultants = [mock_consultant]

        # Appel de la fonction
        result = _prepare_consultants_table_data(consultants)

        # Vérifications
        assert len(result) == 1
        assert result[0]["ID"] == 1
        assert result[0]["Nom"] == "Doe"
        assert result[0]["Prénom"] == "John"
        assert result[0]["Email"] == "john@test.com"
        assert result[0]["Grade"] == "Senior"
        assert result[0]["Disponible"] == "✅"
        assert result[0]["Salaire"] == "50,000€"

    def test_format_consultant_salary_with_value(self):
        """Test de _format_consultant_salary avec valeur"""
        from app.pages_modules.practices import _format_consultant_salary

        # Mock consultant avec salaire
        mock_consultant = MagicMock()
        mock_consultant.salaire_actuel = 45000

        result = _format_consultant_salary(mock_consultant)

        assert result == "45,000€"

    def test_format_consultant_salary_without_value(self):
        """Test de _format_consultant_salary sans valeur"""
        from app.pages_modules.practices import _format_consultant_salary

        # Mock consultant sans salaire
        mock_consultant = MagicMock()
        del mock_consultant.salaire_actuel  # Simule l'absence d'attribut

        result = _format_consultant_salary(mock_consultant)

        assert result == "Non défini"

    @patch("app.pages_modules.practices.st.dataframe")
    @patch("app.pages_modules.practices._get_column_config")
    @patch("app.pages_modules.practices._display_consultants_simple_list")
    def test_display_consultants_dataframe_with_pandas(
        self, mock_simple_list, mock_get_config, mock_dataframe
    ):
        """Test de _display_consultants_dataframe avec pandas"""
        from app.pages_modules.practices import _display_consultants_dataframe

        # Mock des données
        consultant_data = [{"ID": 1, "Nom": "Doe"}]

        # Appel de la fonction
        _display_consultants_dataframe(consultant_data)

        # Vérifications
        mock_dataframe.assert_called_once()
        mock_simple_list.assert_not_called()

    @patch("app.pages_modules.practices.st.write")
    def test_display_consultants_dataframe_without_pandas(self, mock_write):
        """Test de _display_consultants_dataframe sans pandas"""
        # Simuler pandas non disponible
        import app.pages_modules.practices as practices_module
        from app.pages_modules.practices import _display_consultants_dataframe

        original_pd = practices_module.pd
        practices_module.pd = None

        try:
            # Mock des données
            consultant_data = [
                {
                    "ID": 1,
                    "Nom": "Doe",
                    "Prénom": "John",
                    "Grade": "Senior",
                    "Email": "test@test.com",
                    "Salaire": "50,000€",
                }
            ]

            # Appel de la fonction
            _display_consultants_dataframe(consultant_data)

            # Vérifications - devrait appeler _display_consultants_simple_list qui utilise st.write
            mock_write.assert_called_once_with(
                "**John Doe** - Senior - test@test.com - 50,000€"
            )
        finally:
            # Restaurer pandas
            practices_module.pd = original_pd

    def test_get_column_config(self):
        """Test de _get_column_config"""
        from app.pages_modules.practices import _get_column_config

        config = _get_column_config()

        # Vérifications de base
        assert "ID" in config
        assert "Nom" in config
        assert "Prénom" in config
        assert "Email" in config
        assert "Grade" in config
        assert "Disponible" in config
        assert "Salaire" in config

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.st.selectbox")
    @patch("app.pages_modules.practices.st.button")
    @patch("app.pages_modules.practices._handle_remove_consultant")
    def test_display_remove_consultant_section(
        self, mock_handle_remove, mock_button, mock_selectbox, mock_write
    ):
        """Test de _display_remove_consultant_section"""
        from app.pages_modules.practices import (
            _display_remove_consultant_section,
        )

        # Mock des consultants
        mock_consultant = MagicMock()
        mock_consultant.prenom = "John"
        mock_consultant.nom = "Doe"
        consultants = [mock_consultant]

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Mock du selectbox et bouton
        mock_selectbox.return_value = mock_consultant
        mock_button.return_value = False  # Bouton non cliqué

        # Appel de la fonction
        _display_remove_consultant_section(consultants, mock_practice)

        # Vérifications
        mock_write.assert_called_with("**Retirer un consultant de la practice:**")
        mock_selectbox.assert_called_once()
        mock_button.assert_called_once()
        mock_handle_remove.assert_not_called()

    @patch("app.pages_modules.practices.st.success")
    @patch("app.pages_modules.practices.st.rerun")
    @patch("app.pages_modules.practices.PracticeService.assign_consultant_to_practice")
    def test_handle_remove_consultant_success(
        self, mock_assign, mock_rerun, mock_success
    ):
        """Test de _handle_remove_consultant avec succès"""
        from app.pages_modules.practices import _handle_remove_consultant

        # Mock des objets
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "John"
        mock_consultant.nom = "Doe"

        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Mock succès
        mock_assign.return_value = True

        # Appel de la fonction
        _handle_remove_consultant(mock_consultant, mock_practice)

        # Vérifications
        mock_assign.assert_called_once_with(1, None)
        mock_success.assert_called_once()
        mock_rerun.assert_called_once()

    @patch("app.pages_modules.practices.st.error")
    @patch("app.pages_modules.practices.PracticeService.assign_consultant_to_practice")
    def test_handle_remove_consultant_failure(self, mock_assign, mock_error):
        """Test de _handle_remove_consultant avec échec"""
        from app.pages_modules.practices import _handle_remove_consultant

        # Mock des objets
        mock_consultant = MagicMock()
        mock_consultant.id = 1  # Ajouter l'attribut id
        mock_consultant.prenom = "John"
        mock_consultant.nom = "Doe"

        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Mock échec
        mock_assign.return_value = False

        # Appel de la fonction
        _handle_remove_consultant(mock_consultant, mock_practice)

        # Vérifications
        mock_assign.assert_called_once_with(1, None)
        mock_error.assert_called_with("❌ Erreur lors du retrait du consultant")

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.st.info")
    @patch("app.pages_modules.practices._get_available_consultants")
    @patch("app.pages_modules.practices._display_consultant_assignment_interface")
    def test_display_assign_consultant_tab_with_consultants(
        self, mock_display_interface, mock_get_available, mock_info, mock_write
    ):
        """Test de _display_assign_consultant_tab avec consultants disponibles"""
        from app.pages_modules.practices import _display_assign_consultant_tab

        # Mock de la practice
        mock_practice = MagicMock()

        # Mock consultants disponibles
        mock_consultant = MagicMock()
        mock_get_available.return_value = [mock_consultant]

        # Appel de la fonction
        _display_assign_consultant_tab(mock_practice)

        # Vérifications
        mock_write.assert_called_with("**Affecter un consultant à la practice:**")
        mock_get_available.assert_called_once_with(mock_practice)
        mock_display_interface.assert_called_once()
        mock_info.assert_not_called()

    @patch("app.pages_modules.practices.st.info")
    @patch("app.pages_modules.practices._get_available_consultants")
    def test_display_assign_consultant_tab_no_consultants(
        self, mock_get_available, mock_info
    ):
        """Test de _display_assign_consultant_tab sans consultants disponibles"""
        from app.pages_modules.practices import _display_assign_consultant_tab

        # Mock de la practice
        mock_practice = MagicMock()

        # Mock aucun consultant disponible
        mock_get_available.return_value = []

        # Appel de la fonction
        _display_assign_consultant_tab(mock_practice)

        # Vérifications
        mock_get_available.assert_called_once_with(mock_practice)
        mock_info.assert_called_with(
            "Tous les consultants sont déjà affectés à cette practice."
        )

    @patch(
        "app.services.consultant_service.ConsultantService.get_all_consultants_objects"
    )
    def test_get_available_consultants(self, mock_get_all):
        """Test de _get_available_consultants"""
        from app.pages_modules.practices import _get_available_consultants

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.id = 1

        # Mock des consultants
        mock_consultant1 = MagicMock()
        mock_consultant1.practice_id = None  # Disponible

        mock_consultant2 = MagicMock()
        mock_consultant2.practice_id = 2  # Dans une autre practice

        mock_consultant3 = MagicMock()
        mock_consultant3.practice_id = 1  # Déjà dans cette practice

        mock_get_all.return_value = [
            mock_consultant1,
            mock_consultant2,
            mock_consultant3,
        ]

        # Appel de la fonction
        result = _get_available_consultants(mock_practice)

        # Vérifications
        assert len(result) == 2
        assert mock_consultant1 in result
        assert mock_consultant2 in result
        assert mock_consultant3 not in result

    @patch("app.pages_modules.practices.st.selectbox")
    @patch("app.pages_modules.practices.st.button")
    @patch("app.pages_modules.practices._display_consultant_details")
    @patch("app.pages_modules.practices._handle_assign_consultant")
    def test_display_consultant_assignment_interface(
        self, mock_handle_assign, mock_display_details, mock_button, mock_selectbox
    ):
        """Test de _display_consultant_assignment_interface"""
        from app.pages_modules.practices import (
            _display_consultant_assignment_interface,
        )

        # Mock des données
        mock_consultant = MagicMock()
        mock_consultant.prenom = "John"
        mock_consultant.nom = "Doe"
        mock_consultant.grade = "Senior"
        available_consultants = [mock_consultant]

        mock_practice = MagicMock()

        # Mock du selectbox et bouton
        mock_selectbox.return_value = mock_consultant
        mock_button.return_value = False  # Bouton non cliqué

        # Appel de la fonction
        _display_consultant_assignment_interface(available_consultants, mock_practice)

        # Vérifications
        mock_selectbox.assert_called_once()
        mock_display_details.assert_called_once_with(mock_consultant)
        mock_button.assert_called_once()
        mock_handle_assign.assert_not_called()

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.st.columns")
    @patch("app.pages_modules.practices._get_consultant_current_practice")
    def test_display_consultant_details(
        self, mock_get_current_practice, mock_columns, mock_write
    ):
        """Test de _display_consultant_details"""
        from app.pages_modules.practices import _display_consultant_details

        # Mock du consultant
        mock_consultant = MagicMock()
        mock_consultant.email = "john@test.com"
        mock_consultant.grade = "Senior"
        mock_consultant.salaire_actuel = 50000

        # Mock de la practice actuelle
        mock_get_current_practice.return_value = "Autre Practice"

        # Configuration des colonnes
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_columns.return_value = (mock_col1, mock_col2)

        # Appel de la fonction
        _display_consultant_details(mock_consultant)

        # Vérifications
        mock_columns.assert_called_once_with(2)
        mock_get_current_practice.assert_called_once_with(mock_consultant)
        # Vérifier que les writes ont été appelés dans les bonnes colonnes

    @patch("app.pages_modules.practices.PracticeService.get_practice_by_id")
    def test_get_consultant_current_practice_with_practice(self, mock_get_practice):
        """Test de _get_consultant_current_practice avec practice existante"""
        from app.pages_modules.practices import (
            _get_consultant_current_practice,
        )

        # Mock du consultant
        mock_consultant = MagicMock()
        mock_consultant.practice_id = 1

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"
        mock_get_practice.return_value = mock_practice

        # Appel de la fonction
        result = _get_consultant_current_practice(mock_consultant)

        # Vérifications
        mock_get_practice.assert_called_once_with(1)
        assert result == "Test Practice"

    @patch("app.pages_modules.practices.PracticeService.get_practice_by_id")
    def test_get_consultant_current_practice_no_practice(self, mock_get_practice):
        """Test de _get_consultant_current_practice sans practice"""
        from app.pages_modules.practices import (
            _get_consultant_current_practice,
        )

        # Mock du consultant sans practice
        mock_consultant = MagicMock()
        mock_consultant.practice_id = None

        # Appel de la fonction
        result = _get_consultant_current_practice(mock_consultant)

        # Vérifications
        mock_get_practice.assert_not_called()
        assert result == "Aucune"

    @patch("app.pages_modules.practices.st.success")
    @patch("app.pages_modules.practices.st.rerun")
    @patch("app.pages_modules.practices.PracticeService.assign_consultant_to_practice")
    def test_handle_assign_consultant_success(
        self, mock_assign, mock_rerun, mock_success
    ):
        """Test de _handle_assign_consultant avec succès"""
        from app.pages_modules.practices import _handle_assign_consultant

        # Mock des objets
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "John"
        mock_consultant.nom = "Doe"

        mock_practice = MagicMock()
        mock_practice.id = 1
        mock_practice.nom = "Test Practice"

        # Mock succès
        mock_assign.return_value = True

        # Appel de la fonction
        _handle_assign_consultant(mock_consultant, mock_practice)

        # Vérifications
        mock_assign.assert_called_once_with(1, 1)
        mock_success.assert_called_once()
        mock_rerun.assert_called_once()

    @patch("app.pages_modules.practices.st.error")
    @patch("app.pages_modules.practices.PracticeService.assign_consultant_to_practice")
    def test_handle_assign_consultant_failure(self, mock_assign, mock_error):
        """Test de _handle_assign_consultant avec échec"""
        from app.pages_modules.practices import _handle_assign_consultant

        # Mock des objets
        mock_consultant = MagicMock()
        mock_consultant.prenom = "John"
        mock_consultant.nom = "Doe"

        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Mock échec
        mock_assign.return_value = False

        # Appel de la fonction
        _handle_assign_consultant(mock_consultant, mock_practice)

        # Vérifications
        mock_error.assert_called_with("❌ Erreur lors de l'affectation du consultant")

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.st.columns")
    @patch("app.pages_modules.practices._display_practice_statistics")
    @patch("app.pages_modules.practices._display_practice_export_options")
    def test_display_practice_actions_tab(
        self, mock_export_options, mock_statistics, mock_columns, mock_write
    ):
        """Test de _display_practice_actions_tab"""
        from app.pages_modules.practices import _display_practice_actions_tab

        # Mock de la practice
        mock_practice = MagicMock()

        # Configuration des colonnes
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_columns.return_value = (mock_col1, mock_col2)

        # Appel de la fonction
        _display_practice_actions_tab(mock_practice)

        # Vérifications
        mock_write.assert_called_with("**Actions sur la practice:**")
        mock_columns.assert_called_once_with(2)
        mock_statistics.assert_called_once_with(mock_practice)
        mock_export_options.assert_called_once_with(mock_practice)

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.st.metric")
    @patch("app.pages_modules.practices.PracticeService.get_practice_statistics")
    def test_display_practice_statistics_with_data(
        self, mock_get_stats, mock_metric, mock_write
    ):
        """Test de _display_practice_statistics avec données"""
        from app.pages_modules.practices import _display_practice_statistics

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Mock des statistiques
        mock_stats = {
            "practices_detail": [
                {
                    "nom": "Test Practice",
                    "total_consultants": 10,
                    "consultants_actifs": 8,
                    "responsable": "John Doe",
                }
            ]
        }
        mock_get_stats.return_value = mock_stats

        # Appel de la fonction
        _display_practice_statistics(mock_practice)

        # Vérifications
        mock_write.assert_any_call("**Statistiques de la practice:**")
        mock_metric.assert_any_call("Total consultants", 10)
        mock_metric.assert_any_call("Consultants actifs", 8)
        mock_write.assert_any_call("**Responsable:** John Doe")

    @patch("app.pages_modules.practices.st.error")
    @patch("app.pages_modules.practices.PracticeService.get_practice_statistics")
    def test_display_practice_statistics_with_error(self, mock_get_stats, mock_error):
        """Test de _display_practice_statistics avec erreur"""
        from app.pages_modules.practices import _display_practice_statistics

        # Mock de la practice
        mock_practice = MagicMock()

        # Mock d'erreur
        mock_get_stats.side_effect = Exception("Test error")

        # Appel de la fonction
        _display_practice_statistics(mock_practice)

        # Vérifications
        mock_error.assert_called_once()

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.st.button")
    @patch("app.pages_modules.practices._handle_csv_export")
    def test_display_practice_export_options(
        self, mock_handle_csv, mock_button, mock_write
    ):
        """Test de _display_practice_export_options"""
        from app.pages_modules.practices import (
            _display_practice_export_options,
        )

        # Mock de la practice
        mock_practice = MagicMock()

        # Mock bouton non cliqué
        mock_button.return_value = False

        # Appel de la fonction
        _display_practice_export_options(mock_practice)

        # Vérifications
        mock_write.assert_called_with("**Export des données:**")
        mock_button.assert_called_once()
        mock_handle_csv.assert_not_called()

    @patch("app.pages_modules.practices.st.error")
    @patch("app.pages_modules.practices.PracticeService.get_consultants_by_practice")
    def test_handle_csv_export_no_data(self, mock_get_consultants, mock_error):
        """Test de _handle_csv_export sans données"""
        from app.pages_modules.practices import _handle_csv_export

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.id = 1

        # Mock aucune donnée
        mock_get_consultants.return_value = None

        # Appel de la fonction
        _handle_csv_export(mock_practice)

        # Vérifications
        mock_get_consultants.assert_called_once_with(1)
        mock_error.assert_not_called()  # Pas d'erreur si pas de données

    @patch("app.pages_modules.practices.st.error")
    @patch("app.pages_modules.practices.PracticeService.get_consultants_by_practice")
    def test_handle_csv_export_with_error(self, mock_get_consultants, mock_error):
        """Test de _handle_csv_export avec erreur"""
        from app.pages_modules.practices import _handle_csv_export

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.id = 1

        # Mock d'erreur
        mock_get_consultants.side_effect = Exception("Test error")

        # Appel de la fonction
        _handle_csv_export(mock_practice)

        # Vérifications
        mock_error.assert_called_once()

    @patch("app.pages_modules.practices._process_csv_export")
    @patch("app.pages_modules.practices.PracticeService.get_consultants_by_practice")
    def test_handle_csv_export_with_data(self, mock_get_consultants, mock_process_csv):
        """Test de _handle_csv_export avec données"""
        from app.pages_modules.practices import _handle_csv_export

        # Mock de la practice
        mock_practice = MagicMock()
        mock_practice.id = 1

        # Mock des données
        mock_get_consultants.return_value = {"Test Practice": ["consultant1"]}

        # Appel de la fonction
        _handle_csv_export(mock_practice)

        # Vérifications
        mock_get_consultants.assert_called_once_with(1)
        mock_process_csv.assert_called_once()

    @patch("app.pages_modules.practices._prepare_csv_export_data")
    @patch("app.pages_modules.practices._generate_csv_download")
    def test_process_csv_export(self, mock_generate_download, mock_prepare_data):
        """Test de _process_csv_export"""
        from app.pages_modules.practices import _process_csv_export

        # Mock des données
        consultants_dict = {"Test Practice": ["consultant1", "consultant2"]}
        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Mock des données préparées
        mock_prepare_data.return_value = [{"ID": 1, "Nom": "Doe"}]

        # Appel de la fonction
        _process_csv_export(consultants_dict, mock_practice)

        # Vérifications
        mock_prepare_data.assert_called_once()
        mock_generate_download.assert_called_once()

    def test_prepare_csv_export_data(self):
        """Test de _prepare_csv_export_data"""
        from app.pages_modules.practices import _prepare_csv_export_data

        # Mock des consultants
        mock_consultant1 = MagicMock()
        mock_consultant1.id = 1
        mock_consultant1.nom = "Doe"
        mock_consultant1.prenom = "John"
        mock_consultant1.email = "john@test.com"
        mock_consultant1.grade = "Senior"
        mock_consultant1.disponibilite = True
        mock_consultant1.salaire_actuel = 50000

        mock_consultant2 = MagicMock()
        mock_consultant2.id = 2
        mock_consultant2.nom = "Smith"
        mock_consultant2.prenom = "Jane"
        mock_consultant2.email = "jane@test.com"
        mock_consultant2.grade = "Junior"
        mock_consultant2.disponibilite = False
        mock_consultant2.salaire_actuel = 35000

        consultants = [mock_consultant1, mock_consultant2]
        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Appel de la fonction
        result = _prepare_csv_export_data(consultants, mock_practice)

        # Vérifications
        assert len(result) == 2
        assert result[0]["ID"] == 1
        assert result[0]["Nom"] == "Doe"
        assert result[0]["Prénom"] == "John"
        assert result[0]["Practice"] == "Test Practice"
        assert result[1]["ID"] == 2
        assert result[1]["Nom"] == "Smith"

    @patch("app.pages_modules.practices.st.download_button")
    @patch("app.pages_modules.practices.st.success")
    def test_generate_csv_download(self, mock_success, mock_download_button):
        """Test de _generate_csv_download"""
        from app.pages_modules.practices import _generate_csv_download

        # Mock des données
        export_data = [{"ID": 1, "Nom": "Doe"}]
        mock_practice = MagicMock()
        mock_practice.nom = "Test Practice"

        # Appel de la fonction
        _generate_csv_download(export_data, mock_practice)

        # Vérifications
        mock_download_button.assert_called_once()
        mock_success.assert_called_once_with("✅ Export prêt au téléchargement!")

    @patch("app.pages_modules.practices.st.subheader")
    @patch("app.pages_modules.practices._display_practice_creation_form")
    @patch("app.pages_modules.practices._display_existing_practices_list")
    def test_show_practice_management(
        self, mock_display_existing, mock_display_creation, mock_subheader
    ):
        """Test de show_practice_management"""
        from app.pages_modules.practices import show_practice_management

        # Appel de la fonction
        show_practice_management()

        # Vérifications
        mock_subheader.assert_called_with("⚙️ Gestion des Practices")
        mock_display_creation.assert_called_once()
        mock_display_existing.assert_called_once()

    @patch("app.pages_modules.practices.st.expander")
    @patch("app.pages_modules.practices._render_practice_creation_form")
    def test_display_practice_creation_form(self, mock_render_form, mock_expander):
        """Test de _display_practice_creation_form"""
        from app.pages_modules.practices import _display_practice_creation_form

        # Configuration du mock expander
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = mock_expander_context
        mock_expander.return_value.__exit__ = MagicMock()

        # Appel de la fonction
        _display_practice_creation_form()

        # Vérifications
        mock_expander.assert_called_once_with("➕ Créer une nouvelle practice")
        mock_render_form.assert_called_once()

    @patch("app.pages_modules.practices.st.form")
    @patch("app.pages_modules.practices.st.text_input")
    @patch("app.pages_modules.practices.st.text_area")
    @patch("app.pages_modules.practices.st.form_submit_button")
    @patch("app.pages_modules.practices._handle_practice_creation")
    def test_render_practice_creation_form(
        self,
        mock_handle_creation,
        mock_submit_button,
        mock_text_area,
        mock_text_input,
        mock_form,
    ):
        """Test de _render_practice_creation_form"""
        from app.pages_modules.practices import _render_practice_creation_form

        # Configuration des mocks
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = mock_form_context
        mock_form.return_value.__exit__ = MagicMock()

        # Mock des inputs
        mock_text_input.side_effect = [
            "Test Practice",
            "John Doe",
        ]  # nom et responsable
        mock_text_area.return_value = "Description test"
        mock_submit_button.return_value = False  # Bouton non soumis

        # Appel de la fonction
        _render_practice_creation_form()

        # Vérifications
        mock_form.assert_called_once_with("create_practice_form")
        assert mock_text_input.call_count == 2  # nom et responsable
        mock_text_area.assert_called_once()
        mock_submit_button.assert_called_once()
        mock_handle_creation.assert_not_called()

    @patch("app.pages_modules.practices.st.error")
    def test_handle_practice_creation_empty_name(self, mock_error):
        """Test de _handle_practice_creation avec nom vide"""
        from app.pages_modules.practices import _handle_practice_creation

        # Appel de la fonction avec nom vide
        _handle_practice_creation("", "Description", "Responsable")

        # Vérifications
        mock_error.assert_called_with("❌ Le nom de la practice est obligatoire.")

    @patch("app.pages_modules.practices.st.success")
    @patch("app.pages_modules.practices.st.rerun")
    @patch("app.pages_modules.practices.PracticeService.create_practice")
    def test_handle_practice_creation_success(
        self, mock_create, mock_rerun, mock_success
    ):
        """Test de _handle_practice_creation avec succès"""
        from app.pages_modules.practices import _handle_practice_creation

        # Mock succès
        mock_create.return_value = True

        # Appel de la fonction
        _handle_practice_creation("Test Practice", "Description", "Responsable")

        # Vérifications
        mock_create.assert_called_once_with(
            nom="Test Practice", description="Description", responsable="Responsable"
        )
        mock_success.assert_called_once()
        mock_rerun.assert_called_once()

    @patch("app.pages_modules.practices.st.error")
    @patch("app.pages_modules.practices.PracticeService.create_practice")
    def test_handle_practice_creation_failure(self, mock_create, mock_error):
        """Test de _handle_practice_creation avec échec"""
        from app.pages_modules.practices import _handle_practice_creation

        # Mock échec
        mock_create.return_value = False

        # Appel de la fonction
        _handle_practice_creation("Test Practice", "Description", "Responsable")

        # Vérifications
        mock_error.assert_called_with("❌ Erreur lors de la création de la practice.")

    @patch("app.pages_modules.practices.st.write")
    @patch("app.pages_modules.practices.PracticeService.get_all_practices")
    @patch("app.pages_modules.practices._render_practices_table")
    def test_display_existing_practices_list_with_data(
        self, mock_render_table, mock_get_all, mock_write
    ):
        """Test de _display_existing_practices_list avec données"""
        from app.pages_modules.practices import (
            _display_existing_practices_list,
        )

        # Mock des practices
        mock_practice = MagicMock()
        mock_get_all.return_value = [mock_practice]

        # Appel de la fonction
        _display_existing_practices_list()

        # Vérifications
        mock_write.assert_called_with("**Practices existantes:**")
        mock_get_all.assert_called_once()
        mock_render_table.assert_called_once_with([mock_practice])

    @patch("app.pages_modules.practices.st.columns")
    @patch("app.pages_modules.practices.st.button")
    @patch("app.pages_modules.practices.st.write")
    def test_render_practices_table(self, mock_write, mock_button, mock_columns):
        """Test de _render_practices_table"""
        from app.pages_modules.practices import _render_practices_table

        # Mock des practices
        mock_practice1 = MagicMock()
        mock_practice1.nom = "Practice 1"
        mock_practice1.actif = True

        mock_practice2 = MagicMock()
        mock_practice2.nom = "Practice 2"
        mock_practice2.actif = False

        practices = [mock_practice1, mock_practice2]

        # Configuration des colonnes
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_columns.return_value = (mock_col1, mock_col2, mock_col3)

        # Mock bouton non cliqué
        mock_button.return_value = False

        # Appel de la fonction
        _render_practices_table(practices)

        # Vérifications
        assert mock_columns.call_count == 2  # Une fois par practice
        mock_write.assert_any_call("🏢 Practice 1")
        mock_write.assert_any_call("🏢 Practice 2")
        mock_write.assert_any_call("✅ Actif")
        mock_write.assert_any_call("❌ Inactif")
        assert mock_button.call_count == 2  # Un bouton par practice
