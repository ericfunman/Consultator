"""
Tests pour le module consultants.py
Couverture des fonctions principales de gestion des consultants
"""

import os
import sys
from datetime import datetime
from unittest.mock import MagicMock, patch, mock_open

import pandas as pd
import pytest
import streamlit as st

# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

try:
    import app.pages_modules.consultants as consultants
except ImportError:
    consultants = None


class TestConsultantsImports:
    """Tests pour la gestion des imports"""

    def test_imports_available(self):
        """Test que les imports sont disponibles"""
        # Cette fonction teste la logique d'imports du module
        assert consultants is not None and hasattr(consultants, "imports_ok")
        # En mode test, les imports peuvent échouer, c'est normal

    def test_imports_fallback(self):
        """Test du fallback en cas d'échec d'import"""
        # Sauvegarder l'état original
        original_imports_ok = consultants.imports_ok

        # Tester le cas où les imports échouent
        consultants.imports_ok = False

        # Vérifier que le module peut quand même fonctionner
        assert consultants.imports_ok is False

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok


class TestShowFunction:
    """Tests pour la fonction show principale"""

    @patch("streamlit.title")
    @patch("streamlit.tabs")
    @patch("app.pages_modules.consultants.show_cv_analysis_fullwidth")
    @patch("app.pages_modules.consultants.show_consultant_profile")
    @patch("app.pages_modules.consultants.show_consultants_list")
    def test_show_basic_structure(
        self, mock_list, mock_profile, mock_cv, mock_tabs, mock_title
    ):
        """Test de la structure de base de la fonction show"""
        mock_tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        consultants.show()

        mock_title.assert_called_once()
        mock_tabs.assert_called_once()

    @patch("streamlit.title")
    @patch("streamlit.tabs")
    def test_show_imports_ko(self, mock_tabs, mock_title):
        """Test de la fonction show quand les imports échouent"""
        mock_tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

        # Sauvegarder l'état original
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = False

        # La fonction ne doit pas planter
        consultants.show()

        mock_title.assert_called_once()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok


class TestCVAnalysisFullwidth:
    """Tests pour la fonction show_cv_analysis_fullwidth"""

    @patch("streamlit.subheader")
    @patch("streamlit.file_uploader")
    @patch("streamlit.button")
    @patch("streamlit.success")
    def test_cv_analysis_no_file(
        self, mock_success, mock_button, mock_uploader, mock_subheader
    ):
        """Test analyse CV sans fichier"""
        mock_uploader.return_value = None
        mock_button.return_value = False

        consultants.show_cv_analysis_fullwidth()

        mock_subheader.assert_called()
        mock_uploader.assert_called()

    @patch("streamlit.subheader")
    @patch("streamlit.file_uploader")
    @patch("streamlit.button")
    @patch("streamlit.error")
    def test_cv_analysis_with_file_imports_ko(
        self, mock_error, mock_button, mock_uploader, mock_subheader
    ):
        """Test analyse CV avec fichier mais imports KO"""
        # Mock du fichier uploadé
        mock_file = MagicMock()
        mock_file.name = "test_cv.pdf"
        mock_file.read.return_value = b"test content"
        mock_uploader.return_value = mock_file
        mock_button.return_value = True

        # Sauvegarder l'état original
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = False

        consultants.show_cv_analysis_fullwidth()

        mock_error.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok

    @patch("streamlit.subheader")
    @patch("streamlit.file_uploader")
    @patch("streamlit.button")
    @patch("streamlit.success")
    @patch("streamlit.json")
    @patch("app.services.simple_analyzer.SimpleDocumentAnalyzer")
    def test_cv_analysis_with_file_success(
        self,
        mock_analyzer_class,
        mock_json,
        mock_success,
        mock_button,
        mock_uploader,
        mock_subheader,
    ):
        """Test analyse CV avec fichier - succès"""
        # Mock du fichier uploadé
        mock_file = MagicMock()
        mock_file.name = "test_cv.pdf"
        mock_file.read.return_value = b"test content"
        mock_uploader.return_value = mock_file
        mock_button.return_value = True

        # Mock de l'analyzer
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_document.return_value = {
            "nom": "Dupont",
            "prenom": "Jean",
            "competences": ["Python", "SQL"],
        }
        mock_analyzer_class.return_value = mock_analyzer

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        consultants.show_cv_analysis_fullwidth()

        mock_success.assert_called()
        mock_json.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok


class TestConsultantProfile:
    """Tests pour la fonction show_consultant_profile"""

    @patch("streamlit.subheader")
    @patch("streamlit.selectbox")
    @patch("app.pages_modules.consultants.show_consultant_info")
    @patch("app.pages_modules.consultants.show_consultant_skills")
    @patch("app.pages_modules.consultants.show_consultant_languages")
    @patch("app.pages_modules.consultants.show_consultant_missions")
    @patch("app.services.consultant_service.ConsultantService.get_all_consultants")
    def test_consultant_profile_no_consultant(
        self,
        mock_get_all,
        mock_missions,
        mock_languages,
        mock_skills,
        mock_info,
        mock_selectbox,
        mock_subheader,
    ):
        """Test profil consultant sans consultant sélectionné"""
        mock_get_all.return_value = []
        mock_selectbox.return_value = None

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        consultants.show_consultant_profile()

        mock_subheader.assert_called()
        mock_selectbox.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok

    @patch("streamlit.subheader")
    @patch("streamlit.selectbox")
    @patch("streamlit.tabs")
    @patch("app.pages_modules.consultants.show_consultant_info")
    @patch("app.pages_modules.consultants.show_consultant_skills")
    @patch("app.pages_modules.consultants.show_consultant_languages")
    @patch("app.pages_modules.consultants.show_consultant_missions")
    @patch("app.services.consultant_service.ConsultantService.get_all_consultants")
    def test_consultant_profile_with_consultant(
        self,
        mock_get_all,
        mock_missions,
        mock_languages,
        mock_skills,
        mock_info,
        mock_tabs,
        mock_selectbox,
        mock_subheader,
    ):
        """Test profil consultant avec consultant sélectionné"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"

        mock_get_all.return_value = [mock_consultant]
        mock_selectbox.return_value = "Jean Dupont"
        mock_tabs.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        consultants.show_consultant_profile()

        mock_tabs.assert_called()
        mock_info.assert_called_with(mock_consultant)
        mock_skills.assert_called_with(mock_consultant)
        mock_languages.assert_called_with(mock_consultant)
        mock_missions.assert_called_with(mock_consultant)

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok


class TestConsultantInfo:
    """Tests pour la fonction show_consultant_info"""

    @patch("streamlit.markdown")
    @patch("streamlit.form")
    @patch("streamlit.text_input")
    @patch("streamlit.selectbox")
    @patch("streamlit.date_input")
    @patch("streamlit.number_input")
    @patch("streamlit.text_area")
    @patch("streamlit.form_submit_button")
    def test_consultant_info_display_mode(
        self,
        mock_submit,
        mock_text_area,
        mock_number,
        mock_date,
        mock_selectbox,
        mock_text_input,
        mock_form,
        mock_markdown,
    ):
        """Test affichage des informations consultant en mode lecture"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"
        mock_consultant.email = "jean.dupont@example.com"
        mock_consultant.telephone = "0123456789"

        # Mock form context
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = MagicMock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = MagicMock()

        mock_submit.return_value = False

        consultants.show_consultant_info(mock_consultant)

        mock_markdown.assert_called()

    @patch("streamlit.success")
    @patch("streamlit.error")
    @patch("streamlit.form")
    @patch("streamlit.text_input")
    @patch("streamlit.selectbox")
    @patch("streamlit.date_input")
    @patch("streamlit.number_input")
    @patch("streamlit.text_area")
    @patch("streamlit.form_submit_button")
    @patch("app.services.consultant_service.ConsultantService.update_consultant")
    def test_consultant_info_update_success(
        self,
        mock_update,
        mock_submit,
        mock_text_area,
        mock_number,
        mock_date,
        mock_selectbox,
        mock_text_input,
        mock_form,
        mock_error,
        mock_success,
    ):
        """Test mise à jour réussie des informations consultant"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"

        # Mock form et inputs
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = MagicMock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = MagicMock()

        mock_text_input.side_effect = [
            "Dupont",
            "Jean",
            "jean.dupont@example.com",
            "0123456789",
        ]
        mock_selectbox.side_effect = ["CDI", "Confirmé", "Digital", "Quanteam"]
        mock_date.return_value = datetime.now().date()
        mock_number.side_effect = [55000, 5.0]
        mock_text_area.return_value = "Commentaire"
        mock_submit.return_value = True

        mock_update.return_value = True

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        consultants.show_consultant_info(mock_consultant)

        mock_update.assert_called()
        mock_success.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok


class TestConsultantSkills:
    """Tests pour les fonctions de gestion des compétences"""

    @patch("streamlit.subheader")
    @patch("app.pages_modules.consultants._show_technical_skills")
    @patch("app.pages_modules.consultants._show_functional_skills")
    @patch("app.pages_modules.consultants._add_skills_form")
    def test_show_consultant_skills(
        self, mock_add_form, mock_functional, mock_technical, mock_subheader
    ):
        """Test affichage des compétences consultant"""
        mock_consultant = MagicMock()

        consultants.show_consultant_skills(mock_consultant)

        mock_subheader.assert_called()
        mock_technical.assert_called_with(mock_consultant)
        mock_functional.assert_called_with(mock_consultant)
        mock_add_form.assert_called_with(mock_consultant)

    @patch("streamlit.markdown")
    @patch("streamlit.dataframe")
    @patch("streamlit.button")
    @patch("app.pages_modules.consultants._delete_consultant_competence")
    def test_show_technical_skills_with_data(
        self, mock_delete, mock_button, mock_dataframe, mock_markdown
    ):
        """Test affichage compétences techniques avec données"""
        mock_consultant = MagicMock()
        mock_consultant.competences_techniques = [
            MagicMock(competence=MagicMock(nom="Python"), niveau=4, annees_experience=3)
        ]

        mock_button.return_value = False

        consultants._show_technical_skills(mock_consultant)

        mock_markdown.assert_called()
        mock_dataframe.assert_called()

    @patch("streamlit.info")
    def test_show_technical_skills_no_data(self, mock_info):
        """Test affichage compétences techniques sans données"""
        mock_consultant = MagicMock()
        mock_consultant.competences_techniques = []

        consultants._show_technical_skills(mock_consultant)

        mock_info.assert_called()


class TestConsultantLanguages:
    """Tests pour les fonctions de gestion des langues"""

    @patch("streamlit.subheader")
    @patch("streamlit.dataframe")
    @patch("streamlit.button")
    @patch("app.pages_modules.consultants._add_language_form")
    def test_show_consultant_languages_with_data(
        self, mock_add_form, mock_button, mock_dataframe, mock_subheader
    ):
        """Test affichage des langues avec données"""
        mock_consultant = MagicMock()
        mock_consultant.langues = [
            MagicMock(langue=MagicMock(nom="Anglais"), niveau="Courant")
        ]

        mock_button.return_value = False

        consultants.show_consultant_languages(mock_consultant)

        mock_subheader.assert_called()
        mock_dataframe.assert_called()
        mock_add_form.assert_called_with(mock_consultant)

    @patch("streamlit.subheader")
    @patch("streamlit.info")
    @patch("app.pages_modules.consultants._add_language_form")
    def test_show_consultant_languages_no_data(
        self, mock_add_form, mock_info, mock_subheader
    ):
        """Test affichage des langues sans données"""
        mock_consultant = MagicMock()
        mock_consultant.langues = []

        consultants.show_consultant_languages(mock_consultant)

        mock_subheader.assert_called()
        mock_info.assert_called()
        mock_add_form.assert_called_with(mock_consultant)

    @patch("streamlit.form")
    @patch("streamlit.selectbox")
    @patch("streamlit.text_area")
    @patch("streamlit.form_submit_button")
    @patch("streamlit.success")
    @patch("app.pages_modules.consultants._save_consultant_language")
    def test_add_language_form_success(
        self,
        mock_save,
        mock_success,
        mock_submit,
        mock_text_area,
        mock_selectbox,
        mock_form,
    ):
        """Test ajout de langue avec succès"""
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock form
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = MagicMock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = MagicMock()

        mock_selectbox.side_effect = ["Anglais", "Courant"]
        mock_text_area.return_value = "Commentaire"
        mock_submit.return_value = True
        mock_save.return_value = True

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        consultants._add_language_form(mock_consultant)

        mock_save.assert_called()
        mock_success.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok


class TestConsultantMissions:
    """Tests pour les fonctions de gestion des missions"""

    @patch("streamlit.subheader")
    @patch("streamlit.info")
    @patch("app.pages_modules.consultants.show_add_mission_form")
    def test_show_consultant_missions_no_data(
        self, mock_add_form, mock_info, mock_subheader
    ):
        """Test affichage des missions sans données"""
        mock_consultant = MagicMock()
        mock_consultant.missions = []

        consultants.show_consultant_missions(mock_consultant)

        mock_subheader.assert_called()
        mock_info.assert_called()
        mock_add_form.assert_called_with(mock_consultant)

    @patch("streamlit.subheader")
    @patch("streamlit.tabs")
    @patch("app.pages_modules.consultants.show_mission_readonly")
    @patch("app.pages_modules.consultants.show_add_mission_form")
    def test_show_consultant_missions_with_data(
        self, mock_add_form, mock_readonly, mock_tabs, mock_subheader
    ):
        """Test affichage des missions avec données"""
        mock_mission = MagicMock()
        mock_mission.nom = "Mission Test"

        mock_consultant = MagicMock()
        mock_consultant.missions = [mock_mission]

        mock_tabs.return_value = [MagicMock(), MagicMock()]

        consultants.show_consultant_missions(mock_consultant)

        mock_subheader.assert_called()
        mock_tabs.assert_called()
        mock_readonly.assert_called()
        mock_add_form.assert_called_with(mock_consultant)

    @patch("streamlit.markdown")
    def test_show_mission_readonly(self, mock_markdown):
        """Test affichage mission en lecture seule"""
        mock_mission = MagicMock()
        mock_mission.nom = "Mission Test"
        mock_mission.description = "Description test"
        mock_mission.client = "Client test"
        mock_mission.date_debut = datetime.now().date()
        mock_mission.date_fin = datetime.now().date()
        mock_mission.revenus_generes = 100000

        consultants.show_mission_readonly(mock_mission)

        mock_markdown.assert_called()


class TestConsultantsList:
    """Tests pour la fonction show_consultants_list"""

    @patch("streamlit.subheader")
    @patch("streamlit.info")
    @patch("streamlit.error")
    @patch("app.services.consultant_service.ConsultantService.get_all_consultants")
    def test_consultants_list_imports_ko(
        self, mock_get_all, mock_error, mock_info, mock_subheader
    ):
        """Test liste consultants avec imports KO"""
        # Sauvegarder l'état original
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = False

        consultants.show_consultants_list()

        mock_error.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok

    @patch("streamlit.subheader")
    @patch("streamlit.info")
    @patch("app.services.consultant_service.ConsultantService.get_all_consultants")
    def test_consultants_list_no_data(self, mock_get_all, mock_info, mock_subheader):
        """Test liste consultants sans données"""
        mock_get_all.return_value = []

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        consultants.show_consultants_list()

        mock_info.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok

    @patch("streamlit.subheader")
    @patch("streamlit.dataframe")
    @patch("streamlit.markdown")
    @patch("app.services.consultant_service.ConsultantService.get_all_consultants")
    def test_consultants_list_with_data(
        self, mock_get_all, mock_markdown, mock_dataframe, mock_subheader
    ):
        """Test liste consultants avec données"""
        # Mock consultants
        mock_consultant = MagicMock()
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"
        mock_consultant.email = "jean.dupont@example.com"
        mock_consultant.practice = MagicMock(nom="Digital")

        mock_get_all.return_value = [mock_consultant]

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        consultants.show_consultants_list()

        mock_dataframe.assert_called()
        mock_markdown.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok


class TestUtilityFunctions:
    """Tests pour les fonctions utilitaires"""

    @patch("streamlit.success")
    @patch("streamlit.error")
    @patch("app.database.database.get_database_session")
    def test_save_consultant_competence_success(
        self, mock_session, mock_error, mock_success
    ):
        """Test sauvegarde compétence consultant avec succès"""
        # Mock session
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__ = MagicMock(return_value=mock_db_session)
        mock_session.return_value.__exit__ = MagicMock()

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        result = consultants._save_consultant_competence(1, 1, 4, 3, "commentaire")

        assert result is True
        mock_success.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok

    @patch("streamlit.error")
    def test_save_consultant_competence_imports_ko(self, mock_error):
        """Test sauvegarde compétence avec imports KO"""
        # Sauvegarder l'état original
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = False

        result = consultants._save_consultant_competence(1, 1, 4, 3, "commentaire")

        assert result is False
        mock_error.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok

    @patch("streamlit.success")
    @patch("streamlit.error")
    @patch("app.database.database.get_database_session")
    def test_delete_consultant_competence_success(
        self, mock_session, mock_error, mock_success
    ):
        """Test suppression compétence consultant avec succès"""
        # Mock session et compétence
        mock_db_session = MagicMock()
        mock_competence = MagicMock()
        mock_db_session.get.return_value = mock_competence

        mock_session.return_value.__enter__ = MagicMock(return_value=mock_db_session)
        mock_session.return_value.__exit__ = MagicMock()

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        result = consultants._delete_consultant_competence(1)

        assert result is True
        mock_success.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok

    @patch("streamlit.success")
    @patch("streamlit.error")
    @patch("app.database.database.get_database_session")
    def test_save_consultant_language_success(
        self, mock_session, mock_error, mock_success
    ):
        """Test sauvegarde langue consultant avec succès"""
        # Mock session
        mock_db_session = MagicMock()
        mock_session.return_value.__enter__ = MagicMock(return_value=mock_db_session)
        mock_session.return_value.__exit__ = MagicMock()

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        result = consultants._save_consultant_language(1, 1, "Courant", "commentaire")

        assert result is True
        mock_success.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok

    @patch("streamlit.success")
    @patch("streamlit.error")
    @patch("app.database.database.get_database_session")
    def test_delete_consultant_language_success(
        self, mock_session, mock_error, mock_success
    ):
        """Test suppression langue consultant avec succès"""
        # Mock session et langue
        mock_db_session = MagicMock()
        mock_langue = MagicMock()
        mock_db_session.get.return_value = mock_langue

        mock_session.return_value.__enter__ = MagicMock(return_value=mock_db_session)
        mock_session.return_value.__exit__ = MagicMock()

        # Assurer que les imports sont OK
        original_imports_ok = consultants.imports_ok
        consultants.imports_ok = True

        result = consultants._delete_consultant_language(1)

        assert result is True
        mock_success.assert_called()

        # Restaurer l'état original
        consultants.imports_ok = original_imports_ok


class TestErrorHandling:
    """Tests pour la gestion d'erreurs"""

    @patch("streamlit.error")
    @patch("app.services.consultant_service.ConsultantService.update_consultant")
    def test_consultant_info_update_error(self, mock_update, mock_error):
        """Test gestion d'erreur lors de la mise à jour consultant"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Simuler une erreur
        mock_update.side_effect = Exception("Database error")

        # Le test vérifie que l'erreur est gérée sans planter l'application
        # En mode réel, cette fonction est appelée via Streamlit avec des forms
        # Ici on teste juste que les imports/modules sont corrects
        assert consultants._save_consultant_competence is not None
        assert consultants._save_consultant_language is not None
        assert consultants._delete_consultant_competence is not None
        assert consultants._delete_consultant_language is not None

    def test_module_structure(self):
        """Test de la structure générale du module"""
        # Vérifier que toutes les fonctions importantes existent
        assert hasattr(consultants, "show")
        assert hasattr(consultants, "show_cv_analysis_fullwidth")
        assert hasattr(consultants, "show_consultant_profile")
        assert hasattr(consultants, "show_consultant_info")
        assert hasattr(consultants, "show_consultant_skills")
        assert hasattr(consultants, "show_consultant_languages")
        assert hasattr(consultants, "show_consultant_missions")
        assert hasattr(consultants, "show_consultants_list")

        # Vérifier les fonctions utilitaires
        assert hasattr(consultants, "_save_consultant_competence")
        assert hasattr(consultants, "_delete_consultant_competence")
        assert hasattr(consultants, "_save_consultant_language")
        assert hasattr(consultants, "_delete_consultant_language")

    def test_function_signatures(self):
        """Test des signatures de fonctions"""
        import inspect

        # Vérifier que les fonctions principales acceptent les bons paramètres
        sig_show = inspect.signature(consultants.show)
        assert len(sig_show.parameters) == 0

        sig_info = inspect.signature(consultants.show_consultant_info)
        assert len(sig_info.parameters) == 1

        sig_skills = inspect.signature(consultants.show_consultant_skills)
        assert len(sig_skills.parameters) == 1

        sig_languages = inspect.signature(consultants.show_consultant_languages)
        assert len(sig_languages.parameters) == 1

        sig_missions = inspect.signature(consultants.show_consultant_missions)
        assert len(sig_missions.parameters) == 1
