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

    @patch('streamlit.title')
    @patch('streamlit.tabs')
    def test_show_page_structure(self, mock_tabs, mock_title):
        """Test de la structure générale de la page"""
        # Mock des tabs
        mock_tab1 = Mock()
        mock_tab2 = Mock()
        mock_tabs.return_value = [mock_tab1, mock_tab2]

        from app.pages_modules.consultants import show

        show()

        mock_title.assert_called_with("👥 Gestion des Consultants")
        mock_tabs.assert_called_with(["Liste des consultants", "Ajouter un consultant"])

    @patch('streamlit.columns')
    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('streamlit.dataframe')
    @patch('streamlit.selectbox')
    @patch('pandas.DataFrame')
    def test_show_consultants_list_basic(self, mock_dataframe, mock_selectbox, mock_button, mock_text_input, mock_columns):
        """Test de l'affichage de la liste des consultants"""
        # Mock des éléments UI
        mock_columns.return_value = [Mock(), Mock(), Mock()]
        mock_text_input.return_value = ""
        mock_selectbox.return_value = "Tous"
        mock_button.return_value = False

        # Mock DataFrame
        mock_df = Mock()
        mock_dataframe.return_value = mock_df

        from app.pages_modules.consultants import show_consultants_list

        show_consultants_list()

        # Vérifier que les éléments de base sont appelés
        mock_columns.assert_called()
        mock_text_input.assert_called()
        mock_selectbox.assert_called()

    @patch('streamlit.columns')
    @patch('streamlit.subheader')
    @patch('streamlit.write')
    @patch('streamlit.metric')
    def test_show_consultant_info_basic(self, mock_metric, mock_write, mock_subheader, mock_columns):
        """Test de l'affichage des informations consultant"""
        # Mock du consultant
        consultant = Mock()
        consultant.id = 1
        consultant.nom = "Dupont"
        consultant.prenom = "Jean"
        consultant.email = "jean.dupont@email.com"
        consultant.nom_complet = "Jean Dupont"
        consultant.grade = "Senior"
        consultant.type_contrat = "CDI"
        consultant.salaire_actuel = 50000.0
        consultant.disponibilite = True
        consultant.statut_societe = "En poste"
        consultant.date_disponibilite = "ASAP"
        consultant.experience_annees = 5.5

        # Mock des colonnes
        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_columns.return_value = [mock_col1, mock_col2]

        from app.pages_modules.consultants import show_consultant_info

        show_consultant_info(consultant)

        # Vérifier que les métriques sont affichées
        assert mock_metric.call_count >= 4  # Au moins 4 métriques
        mock_subheader.assert_called_with("👤 Informations générales")

    @patch('streamlit.expander')
    @patch('streamlit.write')
    @patch('streamlit.columns')
    def test_show_consultant_skills_basic(self, mock_columns, mock_write, mock_expander):
        """Test de l'affichage des compétences"""
        # Mock du consultant
        consultant = Mock()
        consultant.competences = []

        # Mock de l'expander
        mock_expander_context = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = Mock(return_value=None)

        from app.pages_modules.consultants import show_consultant_skills

        show_consultant_skills(consultant)

        mock_expander.assert_called_with("🎯 Compétences techniques & fonctionnelles")

    @patch('streamlit.expander')
    @patch('streamlit.write')
    @patch('streamlit.columns')
    def test_show_consultant_languages_basic(self, mock_columns, mock_write, mock_expander):
        """Test de l'affichage des langues"""
        # Mock du consultant
        consultant = Mock()
        consultant.langues = []

        # Mock de l'expander
        mock_expander_context = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = Mock(return_value=None)

        from app.pages_modules.consultants import show_consultant_languages

        show_consultant_languages(consultant)

        mock_expander.assert_called_with("🌍 Langues")

    @patch('streamlit.expander')
    @patch('streamlit.write')
    @patch('streamlit.columns')
    @patch('streamlit.button')
    def test_show_consultant_missions_basic(self, mock_button, mock_columns, mock_write, mock_expander):
        """Test de l'affichage des missions"""
        # Mock du consultant
        consultant = Mock()
        consultant.missions = []

        # Mock de l'expander
        mock_expander_context = Mock()
        mock_expander.return_value.__enter__ = Mock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = Mock(return_value=None)

        from app.pages_modules.consultants import show_consultant_missions

        show_consultant_missions(consultant)

        mock_expander.assert_called_with("📋 Missions")

    @patch('streamlit.columns')
    @patch('streamlit.write')
    @patch('streamlit.metric')
    def test_show_mission_readonly_basic(self, mock_metric, mock_write, mock_columns):
        """Test de l'affichage en lecture seule d'une mission"""
        # Mock de la mission
        mission = Mock()
        mission.nom_mission = "Projet ABC"
        mission.client = "Client XYZ"
        mission.role = "Développeur"
        mission.date_debut = "2024-01-01"
        mission.date_fin = "2024-06-30"
        mission.statut = "terminee"
        mission.tjm = 650.0
        mission.revenus_generes = 97500.0
        mission.technologies_utilisees = "Python, Django"
        mission.description = "Description du projet"
        mission.duree_jours = 180

        # Mock des colonnes
        mock_col1 = Mock()
        mock_col2 = Mock()
        mock_columns.return_value = [mock_col1, mock_col2]

        from app.pages_modules.consultants import show_mission_readonly

        show_mission_readonly(mission)

        # Vérifier que les informations de base sont affichées
        mock_write.assert_called()
        mock_metric.assert_called()

    @patch('streamlit.form')
    @patch('streamlit.text_input')
    @patch('streamlit.date_input')
    @patch('streamlit.selectbox')
    @patch('streamlit.number_input')
    @patch('streamlit.text_area')
    @patch('streamlit.form_submit_button')
    def test_show_add_mission_form_basic(self, mock_form_submit, mock_text_area, mock_number_input, mock_selectbox, mock_date_input, mock_text_input, mock_form):
        """Test du formulaire d'ajout de mission"""
        # Mock du consultant
        consultant = Mock()
        consultant.id = 1

        # Mock du formulaire
        mock_form_context = Mock()
        mock_form.return_value.__enter__ = Mock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = Mock(return_value=None)

        # Mock des inputs
        mock_text_input.return_value = "Nouveau Projet"
        mock_date_input.return_value = "2024-01-01"
        mock_selectbox.return_value = "en_cours"
        mock_number_input.return_value = 600.0
        mock_text_area.return_value = "Description"
        mock_form_submit.return_value = False

        from app.pages_modules.consultants import show_add_mission_form

        show_add_mission_form(consultant)

        # Vérifier que le formulaire est créé
        mock_form.assert_called_with("add_mission_form")
        mock_text_input.assert_called()
        mock_date_input.assert_called()

    @patch('streamlit.columns')
    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_save_consultant_competence_success(self, mock_error, mock_success, mock_button, mock_text_input, mock_columns):
        """Test de sauvegarde réussie d'une compétence"""
        from app.pages_modules.consultants import _save_consultant_competence

        # Mock des paramètres
        consultant_id = 1
        competence_id = 1
        annees_experience = 3.5
        niveau_maitrise = "avance"
        certifications = "Certif ABC"
        projets_realises = "Projet X, Projet Y"

        # Mock des inputs
        mock_text_input.return_value = "Certif ABC"

        # Simuler une sauvegarde réussie
        with patch('app.pages_modules.consultants.ConsultantService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.add_competence_to_consultant.return_value = True

            _save_consultant_competence(
                consultant_id, competence_id, annees_experience,
                niveau_maitrise, certifications, projets_realises
            )

            mock_service_instance.add_competence_to_consultant.assert_called_once()
            mock_success.assert_called()

    @patch('streamlit.columns')
    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_save_consultant_competence_failure(self, mock_error, mock_success, mock_button, mock_text_input, mock_columns):
        """Test de sauvegarde échouée d'une compétence"""
        from app.pages_modules.consultants import _save_consultant_competence

        # Simuler une sauvegarde échouée
        with patch('app.pages_modules.consultants.ConsultantService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.add_competence_to_consultant.return_value = False

            _save_consultant_competence(1, 1, 2.0, "intermediaire", "", "")

            mock_error.assert_called()

    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_delete_consultant_competence_success(self, mock_error, mock_success):
        """Test de suppression réussie d'une compétence"""
        from app.pages_modules.consultants import _delete_consultant_competence

        with patch('app.pages_modules.consultants.ConsultantService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.remove_competence_from_consultant.return_value = True

            _delete_consultant_competence(1)

            mock_service_instance.remove_competence_from_consultant.assert_called_once_with(1)
            mock_success.assert_called()

    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_delete_consultant_competence_failure(self, mock_error, mock_success):
        """Test de suppression échouée d'une compétence"""
        from app.pages_modules.consultants import _delete_consultant_competence

        with patch('app.pages_modules.consultants.ConsultantService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.remove_competence_from_consultant.return_value = False

            _delete_consultant_competence(1)

            mock_error.assert_called()

    @patch('streamlit.columns')
    @patch('streamlit.selectbox')
    @patch('streamlit.button')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_save_consultant_language_success(self, mock_error, mock_success, mock_button, mock_selectbox, mock_columns):
        """Test de sauvegarde réussie d'une langue"""
        from app.pages_modules.consultants import _save_consultant_language

        with patch('app.pages_modules.consultants.ConsultantService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.add_language_to_consultant.return_value = True

            _save_consultant_language(1, 1, 4, "Certification TOEIC")

            mock_service_instance.add_language_to_consultant.assert_called_once()
            mock_success.assert_called()

    @patch('streamlit.columns')
    @patch('streamlit.selectbox')
    @patch('streamlit.button')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_save_consultant_language_failure(self, mock_error, mock_success, mock_button, mock_selectbox, mock_columns):
        """Test de sauvegarde échouée d'une langue"""
        from app.pages_modules.consultants import _save_consultant_language

        with patch('app.pages_modules.consultants.ConsultantService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.add_language_to_consultant.return_value = False

            _save_consultant_language(1, 1, 3, "")

            mock_error.assert_called()

    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_delete_consultant_language_success(self, mock_error, mock_success):
        """Test de suppression réussie d'une langue"""
        from app.pages_modules.consultants import _delete_consultant_language

        with patch('app.pages_modules.consultants.ConsultantService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.remove_language_from_consultant.return_value = True

            _delete_consultant_language(1)

            mock_service_instance.remove_language_from_consultant.assert_called_once_with(1)
            mock_success.assert_called()

    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_delete_consultant_language_failure(self, mock_error, mock_success):
        """Test de suppression échouée d'une langue"""
        from app.pages_modules.consultants import _delete_consultant_language

        with patch('app.pages_modules.consultants.ConsultantService') as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.remove_language_from_consultant.return_value = False

            _delete_consultant_language(1)

            mock_error.assert_called()
