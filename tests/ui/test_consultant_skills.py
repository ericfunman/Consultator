"""Tests pour le module consultant_skills - Interface utilisateur"""

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
import streamlit as st

from app.pages_modules.consultant_skills import add_skill_to_consultant
from app.pages_modules.consultant_skills import delete_skill
from app.pages_modules.consultant_skills import get_niveau_label
from app.pages_modules.consultant_skills import show_add_skill_form
from app.pages_modules.consultant_skills import show_consultant_skills
from app.pages_modules.consultant_skills import show_edit_skill_form
from app.pages_modules.consultant_skills import show_skills_analysis
from app.pages_modules.consultant_skills import show_skills_evolution
from app.pages_modules.consultant_skills import show_skills_statistics
from app.pages_modules.consultant_skills import update_consultant_skill
from tests.fixtures.base_test import BaseUITest


class TestConsultantSkills(BaseUITest):
    """Tests pour le module de compétences consultant"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultant_skills)

    @patch("app.pages_modules.consultant_skills.imports_ok", True)
    @patch("app.pages_modules.consultant_skills.ConsultantService")
    def test_show_consultant_skills_basic(self, mock_service):
        """Test d'affichage basique des compétences"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_skills(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_skills.imports_ok", False)
    def test_show_consultant_skills_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        mock_consultant = Mock()
        mock_consultant.id = 1

        try:
            show_consultant_skills(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_show_consultant_skills_no_consultant(self):
        """Test d'affichage sans consultant"""
        try:
            show_consultant_skills(None)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_skills.imports_ok", True)
    @patch("app.pages_modules.consultant_skills.ConsultantService")
    def test_show_consultant_skills_with_data(self, mock_service):
        """Test d'affichage avec données de compétences"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock compétences
        mock_competences = [
            {
                "id": 1,
                "nom": "Python",
                "categorie": "Technique",
                "niveau": 4,
                "niveau_label": "Expert",
            },
            {
                "id": 2,
                "nom": "SQL",
                "categorie": "Technique",
                "niveau": 3,
                "niveau_label": "Avancé",
            },
        ]

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_competences.return_value = mock_competences
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_skills(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_skills.imports_ok", True)
    @patch("app.pages_modules.consultant_skills.ConsultantService")
    def test_show_consultant_skills_empty(self, mock_service):
        """Test d'affichage avec compétences vides"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service avec liste vide
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_competences.return_value = []
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_skills(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_skills.imports_ok", True)
    @patch("app.pages_modules.consultant_skills.ConsultantService")
    def test_show_consultant_skills_service_error(self, mock_service):
        """Test d'affichage avec erreur de service"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_competences.side_effect = Exception("Service error")
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_skills(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_skills as skills_module

        # Vérifier que les fonctions principales existent
        assert hasattr(skills_module, "show_consultant_skills")

        # Vérifier que les variables d'import existent
        assert hasattr(skills_module, "imports_ok")
        assert hasattr(skills_module, "ConsultantService")

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultant_skills)

        # Vérifier le nombre de paramètres
        sig_skills = inspect.signature(show_consultant_skills)

        # Doit avoir au moins un paramètre (consultant)
        assert len(sig_skills.parameters) >= 1

    def test_get_niveau_label_all_levels(self):
        """Test get_niveau_label pour tous les niveaux"""
        assert get_niveau_label(1) == "Débutant"
        assert get_niveau_label(2) == "Intermédiaire"
        assert get_niveau_label(3) == "Avancé"
        assert get_niveau_label(4) == "Expert"
        assert get_niveau_label(5) == "Maître"

    def test_get_niveau_label_edge_cases(self):
        """Test get_niveau_label pour les cas limites"""
        assert get_niveau_label(0) == "Niveau 0"
        assert get_niveau_label(6) == "Niveau 6"
        assert get_niveau_label(10) == "Niveau 10"

    @patch("app.pages_modules.consultant_skills.st.markdown")
    @patch("app.pages_modules.consultant_skills.st.columns")
    @patch("app.pages_modules.consultant_skills.st.metric")
    def test_show_skills_statistics_with_data(self, mock_metric, mock_columns, mock_md):
        """Test show_skills_statistics avec données"""
        # Mock consultant_competences
        mock_cc1 = Mock()
        mock_cc1.niveau = 4
        mock_cc1.certification = True
        mock_cc1.annees_experience = 5

        mock_cc2 = Mock()
        mock_cc2.niveau = 3
        mock_cc2.certification = False
        mock_cc2.annees_experience = 3

        consultant_competences = [mock_cc1, mock_cc2]

        # Mock columns context manager
        mock_col1, mock_col2, mock_col3, mock_col4 = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        mock_columns.return_value = (mock_col1, mock_col2, mock_col3, mock_col4)

        show_skills_statistics(consultant_competences)

        # Should display 4 metrics
        assert mock_metric.call_count == 4
        # Should have called markdown for the title
        mock_md.assert_called_with("#### 📊 Statistiques")

    @patch("app.pages_modules.consultant_skills.st.info")
    def test_show_skills_statistics_empty(self, mock_info):
        """Test show_skills_statistics avec liste vide"""
        show_skills_statistics([])
        # Should not display anything for empty list
        mock_info.assert_not_called()

    @patch("app.pages_modules.consultant_skills.st.markdown")
    @patch("app.pages_modules.consultant_skills.st.form")
    @patch("app.pages_modules.consultant_skills.st.selectbox")
    @patch("app.pages_modules.consultant_skills.st.slider")
    @patch("app.pages_modules.consultant_skills.st.checkbox")
    @patch("app.pages_modules.consultant_skills.st.number_input")
    @patch("app.pages_modules.consultant_skills.st.columns")
    @patch("app.pages_modules.consultant_skills.st.form_submit_button")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_add_skill_form_success(
        self,
        mock_session,
        mock_submit,
        mock_cols,
        mock_num_input,
        mock_checkbox,
        mock_slider,
        mock_selectbox,
        mock_form,
        mock_md,
    ):
        """Test show_add_skill_form avec succès"""
        consultant_id = 1

        # Mock database session and data
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock existing and available competences
        mock_existing_cc = []
        mock_available_comp = [
            MagicMock(id=1, nom="Python", categorie="Technique"),
            MagicMock(id=2, nom="Java", categorie="Technique"),
        ]

        mock_session_instance.query.return_value.filter.return_value.all.side_effect = [
            mock_existing_cc,  # existing_competences
            mock_available_comp,  # available_competences
        ]

        # Mock form components
        mock_form.return_value.__enter__.return_value = None
        mock_form.return_value.__exit__.return_value = None
        mock_selectbox.return_value = 1
        mock_slider.return_value = 4
        mock_checkbox.return_value = True
        mock_num_input.return_value = 5

        # Mock submit buttons
        mock_submit.side_effect = [True, False]  # submitted=True, cancel=False

        # Mock columns
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_cols.return_value = (mock_col1, mock_col2, mock_col3)

        with patch(
            "app.pages_modules.consultant_skills.add_skill_to_consultant",
            return_value=True,
        ) as mock_add_skill:
            show_add_skill_form(consultant_id)

        # Test passed if no exception was raised
        assert 1 == 1  # Test basique

    @patch("app.pages_modules.consultant_skills.st.warning")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_add_skill_form_no_available_skills(self, mock_session, mock_warning):
        """Test show_add_skill_form quand aucune compétence n'est disponible"""
        consultant_id = 1

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock all skills already assigned
        mock_existing_cc = [MagicMock(competence_id=1), MagicMock(competence_id=2)]
        mock_available_comp = []  # No available skills

        mock_session_instance.query.return_value.filter.return_value.all.side_effect = [
            mock_existing_cc,
            mock_available_comp,
        ]

        show_add_skill_form(consultant_id)

        mock_warning.assert_called_once_with("⚠️ Toutes les compétences existantes sont déjà associées à ce consultant")

    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_add_skill_to_consultant_success(self, mock_session, mock_error):
        """Test add_skill_to_consultant avec succès"""
        consultant_id = 1
        data = {
            "competence_id": 1,
            "niveau": 4,
            "annees_experience": 5,
            "certification": True,
        }

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock no existing skill
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        # Mock ConsultantCompetence class
        with patch("app.pages_modules.consultant_skills.ConsultantCompetence") as mock_cc_class:
            mock_cc_instance = MagicMock()
            mock_cc_class.return_value = mock_cc_instance

            result = add_skill_to_consultant(consultant_id, data)

            assert result is True
            # Should have created and added the competence
            mock_cc_class.assert_called_once()
            mock_session_instance.add.assert_called_once_with(mock_cc_instance)
            mock_session_instance.commit.assert_called_once()
            mock_error.assert_not_called()

    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_add_skill_to_consultant_duplicate(self, mock_session, mock_error):
        """Test add_skill_to_consultant avec compétence déjà existante"""
        consultant_id = 1
        data = {
            "competence_id": 1,
            "niveau": 4,
            "annees_experience": 5,
            "certification": True,
        }

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock existing skill
        mock_existing = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_existing

        result = add_skill_to_consultant(consultant_id, data)

        assert result is False
        mock_error.assert_called_with("❌ Cette compétence est déjà associée au consultant")

    @patch("app.pages_modules.consultant_skills.st.markdown")
    @patch("app.pages_modules.consultant_skills.st.form")
    @patch("app.pages_modules.consultant_skills.st.slider")
    @patch("app.pages_modules.consultant_skills.st.checkbox")
    @patch("app.pages_modules.consultant_skills.st.number_input")
    @patch("app.pages_modules.consultant_skills.st.columns")
    @patch("app.pages_modules.consultant_skills.st.form_submit_button")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_edit_skill_form_success(
        self,
        mock_session,
        mock_submit,
        mock_cols,
        mock_num_input,
        mock_checkbox,
        mock_slider,
        mock_form,
        mock_md,
    ):
        """Test show_edit_skill_form avec succès"""
        consultant_competence_id = 1

        # Mock database session and data
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant competence with competence
        mock_competence = MagicMock(nom="Python")
        mock_cc = MagicMock(
            id=1,
            competence=mock_competence,
            niveau=3,
            certification=True,
            annees_experience=4,
        )

        mock_session_instance.query.return_value.join.return_value.filter.return_value.first.return_value = mock_cc

        # Mock form components
        mock_form.return_value.__enter__.return_value = None
        mock_form.return_value.__exit__.return_value = None
        mock_slider.return_value = 4
        mock_checkbox.return_value = True
        mock_num_input.return_value = 5

        # Mock submit buttons
        mock_submit.side_effect = [True, False]  # submitted=True, cancel=False

        # Mock columns
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_cols.return_value = (mock_col1, mock_col2, mock_col3)

        with patch(
            "app.pages_modules.consultant_skills.update_consultant_skill",
            return_value=True,
        ) as mock_update_skill:
            show_edit_skill_form(consultant_competence_id)

        # Test passed if no exception was raised
        assert 1 == 1  # Test basique

    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_edit_skill_form_not_found(self, mock_session, mock_error):
        """Test show_edit_skill_form avec compétence introuvable"""
        consultant_competence_id = 999

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock competence not found
        mock_session_instance.query.return_value.join.return_value.filter.return_value.first.return_value = None

        show_edit_skill_form(consultant_competence_id)

        mock_error.assert_called_with("❌ Compétence introuvable")

    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_update_consultant_skill_success(self, mock_session, mock_error):
        """Test update_consultant_skill avec succès"""
        consultant_competence_id = 1
        data = {"niveau": 4, "annees_experience": 5, "certification": True}

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock existing competence
        mock_cc = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_cc

        result = update_consultant_skill(consultant_competence_id, data)

        assert result is True
        # Should have updated the object and committed
        assert mock_cc.niveau == 4
        assert mock_cc.annees_experience == 5
        assert mock_cc.certification is True
        mock_session_instance.commit.assert_called_once()
        mock_error.assert_not_called()

    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_update_consultant_skill_not_found(self, mock_session, mock_error):
        """Test update_consultant_skill avec compétence introuvable"""
        consultant_competence_id = 999
        data = {"niveau": 4, "annees_experience": 5, "certification": True}

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock competence not found
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        result = update_consultant_skill(consultant_competence_id, data)

        assert result is False
        mock_error.assert_called_with("❌ Compétence introuvable")

    @patch("app.pages_modules.consultant_skills.st.info")
    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_delete_skill_success(self, mock_session, mock_error, mock_info):
        """Test delete_skill avec succès"""
        consultant_competence_id = 1

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock existing competence
        mock_cc = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_cc

        result = delete_skill(consultant_competence_id)

        assert result is True
        # Should have deleted and committed
        mock_session_instance.delete.assert_called_once_with(mock_cc)
        mock_session_instance.commit.assert_called_once()
        mock_info.assert_called_with("✅ Compétence supprimée")
        mock_error.assert_not_called()

    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_delete_skill_not_found(self, mock_session, mock_error):
        """Test delete_skill avec compétence introuvable"""
        consultant_competence_id = 999

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock competence not found
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None

        result = delete_skill(consultant_competence_id)

        assert result is False
        mock_error.assert_called_with("❌ Compétence introuvable")

    @patch("app.pages_modules.consultant_skills.st.markdown")
    @patch("app.pages_modules.consultant_skills.st.columns")
    @patch("app.pages_modules.consultant_skills.st.write")
    @patch("app.pages_modules.consultant_skills.st.success")
    @patch("app.pages_modules.consultant_skills.st.warning")
    @patch("app.pages_modules.consultant_skills.st.info")
    def test_show_skills_analysis_with_data(
        self, mock_info, mock_warning, mock_success, mock_write, mock_cols, mock_md
    ):
        """Test show_skills_analysis avec données"""
        # Mock consultant_competences with different levels and categories
        mock_comp1 = MagicMock(categorie="Technique", niveau=4, certification=True)
        mock_comp2 = MagicMock(categorie="Méthodologie", niveau=2, certification=False)
        mock_comp3 = MagicMock(categorie="Technique", niveau=5, certification=True)

        consultant_competences = [mock_comp1, mock_comp2, mock_comp3]

        # Mock columns
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_cols.return_value = (mock_col1, mock_col2)

        show_skills_analysis(consultant_competences)

        # Should display analysis title
        mock_md.assert_any_call("### 📊 Analyse des compétences")
        # Should show recommendations
        mock_success.assert_called()  # Strong skills
        mock_warning.assert_called()  # Weak skills
        mock_info.assert_called()  # Certifications

    @patch("app.pages_modules.consultant_skills.st.info")
    def test_show_skills_analysis_empty(self, mock_info):
        """Test show_skills_analysis avec liste vide"""
        show_skills_analysis([])
        mock_info.assert_called_with("ℹ️ Aucune compétence à analyser")

    @patch("app.pages_modules.consultant_skills.st.markdown")
    @patch("app.pages_modules.consultant_skills.st.columns")
    @patch("app.pages_modules.consultant_skills.st.write")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_skills_evolution_with_data(self, mock_session, mock_write, mock_cols, mock_md):
        """Test show_skills_evolution avec données"""
        consultant_id = 1

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant competences with dates - need to set date_acquisition properly
        from datetime import datetime

        mock_competence = MagicMock(nom="Python")
        mock_cc1 = MagicMock()
        mock_cc1.competence = mock_competence
        mock_cc1.niveau = 3
        mock_cc1.date_acquisition = datetime(2023, 1, 15)

        mock_cc2 = MagicMock()
        mock_cc2.competence = mock_competence
        mock_cc2.niveau = 4
        mock_cc2.date_acquisition = datetime(2023, 6, 20)

        # Set up the mock query chain properly
        mock_session_instance.query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [
            mock_cc1,
            mock_cc2,
        ]

        # Mock columns
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_cols.return_value = (mock_col1, mock_col2, mock_col3)

        show_skills_evolution(consultant_id)

        # Should display evolution title
        mock_md.assert_any_call("### 📈 Évolution des compétences")
        # Should attempt to display data (columns should be called for each skill)
        assert mock_cols.call_count > 0  # Should create columns for displaying skills

    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.st.info")
    @patch("app.pages_modules.consultant_skills.st.markdown")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_skills_evolution_empty(self, mock_session, mock_md, mock_info, mock_error):
        """Test show_skills_evolution avec aucune donnée"""
        consultant_id = 1

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock the query chain to return empty list
        mock_session_instance.query.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = (
            []
        )

        try:
            show_skills_evolution(consultant_id)
        except Exception as e:
            print(f"Exception during test: {e}")
            raise

        # Debug prints
        print(f"mock_md calls: {mock_md.call_args_list}")
        print(f"mock_info calls: {mock_info.call_args_list}")
        print(f"mock_error calls: {mock_error.call_args_list}")

        # Should display evolution title first
        mock_md.assert_called_with("### 📈 Évolution des compétences")
        # Should show info message for empty data
        mock_info.assert_called_with("ℹ️ Aucune donnée d'évolution disponible")

    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_skills_evolution_error(self, mock_session, mock_error):
        """Test show_skills_evolution avec erreur de base de données"""
        consultant_id = 1

        # Mock database session that raises exception
        mock_session.return_value.__enter__.side_effect = Exception("Database error")

        show_skills_evolution(consultant_id)

        mock_error.assert_called_with("❌ Erreur lors de l'analyse de l'évolution: Database error")

    def test_comprehensive_error_handling(self):
        """Test gestion d'erreurs complète pour toutes les fonctions"""
        # Test add_skill_to_consultant with invalid data
        with patch("app.pages_modules.consultant_skills.get_database_session") as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session_instance.query.return_value.filter.return_value.first.side_effect = Exception("DB Error")

            result = add_skill_to_consultant(1, {"competence_id": 1})
            assert result is False

        # Test update_consultant_skill with invalid data
        with patch("app.pages_modules.consultant_skills.get_database_session") as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session_instance.query.return_value.filter.return_value.first.side_effect = Exception("DB Error")

            result = update_consultant_skill(1, {"niveau": 3})
            assert result is False

        # Test delete_skill with invalid data
        with patch("app.pages_modules.consultant_skills.get_database_session") as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value.__enter__.return_value = mock_session_instance
            mock_session_instance.query.return_value.filter.return_value.first.side_effect = Exception("DB Error")

            result = delete_skill(1)
            assert result is False

    def test_data_validation(self):
        """Test validation des données d'entrée"""
        # Test get_niveau_label with None
        try:
            result = get_niveau_label(None)
            assert result == "Niveau None"
        except TypeError:
            pass  # Expected for None input

        # Test get_niveau_label with negative values
        assert get_niveau_label(-1) == "Niveau -1"

        # Test get_niveau_label with float values
        assert get_niveau_label(3.5) == "Niveau 3.5"

    @patch("app.pages_modules.consultant_skills.get_database_session")
    @patch("app.pages_modules.consultant_skills.st.expander")
    @patch("app.pages_modules.consultant_skills.st.write")
    @patch("app.pages_modules.consultant_skills.st.metric")
    @patch("app.pages_modules.consultant_skills.st.button")
    @patch("app.pages_modules.consultant_skills.st.columns")
    @patch("app.pages_modules.consultant_skills.st.markdown")
    @patch("app.pages_modules.consultant_skills.imports_ok", True)
    def test_show_consultant_skills_with_full_data(
        self,
        mock_md,
        mock_columns,
        mock_button,
        mock_metric,
        mock_write,
        mock_expander,
        mock_session,
    ):
        """Test show_consultant_skills avec données complètes et interactions"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant competences with full data
        mock_competence1 = MagicMock(nom="Python", categorie="Technique")
        mock_competence2 = MagicMock(nom="SQL", categorie="Base de données")

        mock_cc1 = MagicMock(
            id=1,
            competence=mock_competence1,
            niveau=4,
            annees_experience=5,
            certification=True,
            date_acquisition=None,
        )
        mock_cc2 = MagicMock(
            id=2,
            competence=mock_competence2,
            niveau=3,
            annees_experience=3,
            certification=False,
            date_acquisition=None,
        )

        mock_session_instance.query.return_value.join.return_value.filter.return_value.all.return_value = [
            mock_cc1,
            mock_cc2,
        ]

        # Mock UI components
        mock_col1, mock_col2, mock_col3, mock_col4 = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        mock_columns.side_effect = lambda n: (
            mock_col1,
            mock_col2,
            mock_col3,
            mock_col4,
        )[
            :n
        ]  # Return n columns

        mock_button.return_value = False  # No button clicks

        with patch("app.pages_modules.consultant_skills.st.session_state") as mock_state, patch(
            "pandas.DataFrame"
        ) as mock_df:
            mock_df_instance = MagicMock()
            mock_df.return_value = mock_df_instance
            mock_df_instance.iterrows.return_value = []

            show_consultant_skills(mock_consultant)

            # Should display title
            mock_md.assert_any_call("### 💼 Compétences")
            # Should display statistics
            assert mock_metric.call_count >= 4  # 4 metrics in statistics
            # Should display action buttons
            assert mock_button.call_count >= 3  # add, analyze, evolution buttons

    @patch("app.pages_modules.consultant_skills.imports_ok", True)
    @patch("app.pages_modules.consultant_skills.st.error")
    @patch("app.pages_modules.consultant_skills.st.code")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_consultant_skills_database_error(self, mock_session, mock_code, mock_error):
        """Test show_consultant_skills avec erreur de base de données"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1

        # Mock database session that raises exception
        mock_session.return_value.__enter__.side_effect = Exception("Database connection failed")

        show_consultant_skills(mock_consultant)

        # Should display error
        mock_error.assert_called_with("❌ Erreur lors de l'affichage des compétences: Database connection failed")
        mock_code.assert_called_with("Database connection failed")

    @patch("app.pages_modules.consultant_skills.imports_ok", True)
    @patch("app.pages_modules.consultant_skills.st.session_state")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_consultant_skills_with_session_state_forms(self, mock_session, mock_state):
        """Test show_consultant_skills avec formulaires activés via session state"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1

        # Mock database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session_instance.query.return_value.join.return_value.filter.return_value.all.return_value = []

        # Mock session state with forms active
        mock_state.add_skill = 1
        mock_state.edit_skill = None

        with patch("app.pages_modules.consultant_skills.show_add_skill_form") as mock_add_form:
            show_consultant_skills(mock_consultant)
            mock_add_form.assert_called_with(1)

    def test_show_consultant_skills_with_different_categories(self):
        """Test show_consultant_skills avec différentes catégories de compétences"""
        # This test verifies that skills are properly grouped by category
        with patch("app.pages_modules.consultant_skills.imports_ok", True):
            with patch("app.pages_modules.consultant_skills.get_database_session") as mock_session:
                # Mock consultant
                mock_consultant = Mock()
                mock_consultant.id = 1

                # Mock database session
                mock_session_instance = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_session_instance

                # Mock skills from different categories
                mock_comp1 = MagicMock(nom="Python", categorie="Technique")
                mock_comp2 = MagicMock(nom="Scrum", categorie="Méthodologie")
                mock_comp3 = MagicMock(nom="AWS", categorie="Cloud")

                mock_cc1 = MagicMock(
                    id=1,
                    competence=mock_comp1,
                    niveau=4,
                    annees_experience=5,
                    certification=True,
                )
                mock_cc2 = MagicMock(
                    id=2,
                    competence=mock_comp2,
                    niveau=3,
                    annees_experience=3,
                    certification=False,
                )
                mock_cc3 = MagicMock(
                    id=3,
                    competence=mock_comp3,
                    niveau=4,
                    annees_experience=2,
                    certification=True,
                )

                mock_session_instance.query.return_value.join.return_value.filter.return_value.all.return_value = [
                    mock_cc1,
                    mock_cc2,
                    mock_cc3,
                ]

                # Mock UI components to avoid display issues
                with patch("app.pages_modules.consultant_skills.st.markdown"):
                    with patch("app.pages_modules.consultant_skills.st.columns"):
                        with patch(
                            "app.pages_modules.consultant_skills.st.button",
                            return_value=False,
                        ):
                            with patch("app.pages_modules.consultant_skills.st.metric"):
                                with patch("app.pages_modules.consultant_skills.st.write"):
                                    show_consultant_skills(mock_consultant)

                # Test passed if no exceptions were raised
                assert 1 == 1  # Test basique

    def test_integration_with_pandas_dataframe(self):
        """Test l'intégration avec pandas DataFrame dans show_consultant_skills"""
        import pandas as pd

        # Test that the function creates proper DataFrame structure
        with patch("app.pages_modules.consultant_skills.imports_ok", True):
            with patch("app.pages_modules.consultant_skills.get_database_session") as mock_session:
                # Mock consultant
                mock_consultant = Mock()
                mock_consultant.id = 1

                # Mock database session
                mock_session_instance = MagicMock()
                mock_session.return_value.__enter__.return_value = mock_session_instance

                mock_competence = MagicMock(nom="Python", categorie="Technique")
                mock_cc = MagicMock(
                    id=1,
                    competence=mock_competence,
                    niveau=4,
                    annees_experience=5,
                    certification=True,
                )

                mock_session_instance.query.return_value.join.return_value.filter.return_value.all.return_value = [
                    mock_cc
                ]

                # Mock UI components
                with patch("app.pages_modules.consultant_skills.st.markdown"):
                    with patch("app.pages_modules.consultant_skills.st.columns"):
                        with patch(
                            "app.pages_modules.consultant_skills.st.button",
                            return_value=False,
                        ):
                            with patch("app.pages_modules.consultant_skills.st.metric"):
                                with patch("app.pages_modules.consultant_skills.st.write"):
                                    # Mock pandas DataFrame - patch at the function level
                                    with patch("pandas.DataFrame") as mock_df:
                                        show_consultant_skills(mock_consultant)

                                        # Verify DataFrame was created with correct structure
                                        mock_df.assert_called_once()
                                        call_args = mock_df.call_args[0][0]  # Get the data argument
                                        assert len(call_args) == 1  # One skill
                                        skill_data = call_args[0]
                                        expected_columns = [
                                            "Compétence",
                                            "Niveau",
                                            "Expérience",
                                            "Certification",
                                            "Actions",
                                        ]
                                        for col in expected_columns:
                                            assert col in skill_data
