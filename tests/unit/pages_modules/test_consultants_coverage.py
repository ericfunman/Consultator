"""
Tests de couverture pour consultants.py
Couvre les principales fonctions avec mocks extensifs pour Streamlit et la base de données
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
import pandas as pd


class TestConsultantsCoverage:
    """Tests de couverture pour le module consultants.py"""

    @pytest.fixture
    def mock_session(self):
        """Mock de session de base de données"""
        session = Mock()
        return session

    @pytest.fixture
    def mock_consultant(self):
        """Mock d'un consultant"""
        consultant = Mock()
        consultant.id = 1
        consultant.prenom = "Jean"
        consultant.nom = "Dupont"
        consultant.email = "jean.dupont@example.com"
        consultant.telephone = "01.23.45.67.89"
        consultant.salaire_actuel = 50000
        consultant.disponibilite = True
        consultant.notes = "Consultant expérimenté"
        consultant.date_creation = datetime.now()
        consultant.practice = Mock()
        consultant.practice.nom = "Data Science"
        return consultant

    @pytest.fixture
    def mock_mission(self):
        """Mock d'une mission"""
        mission = Mock()
        mission.id = 1
        mission.nom_mission = "Développement API"
        mission.client = "Société Générale"
        mission.role = "Lead Developer"
        mission.date_debut = date(2023, 1, 1)
        mission.date_fin = date(2023, 6, 30)
        mission.statut = "terminee"
        mission.revenus_generes = 75000
        mission.technologies_utilisees = "Python, FastAPI, PostgreSQL"
        mission.description = "Développement d'une API REST"
        return mission

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_function_with_imports_ok(self, mock_get_session, mock_st):
        """Test de la fonction show() avec imports réussis"""
        # Configuration des mocks
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock st.tabs pour retourner des context managers
        mock_tab1 = Mock()
        mock_tab1.__enter__ = Mock(return_value=mock_tab1)
        mock_tab1.__exit__ = Mock(return_value=None)
        mock_tab2 = Mock()
        mock_tab2.__enter__ = Mock(return_value=mock_tab2)
        mock_tab2.__exit__ = Mock(return_value=None)
        mock_st.tabs.return_value = (mock_tab1, mock_tab2)

        # Mock des imports
        with patch("app.pages_modules.consultants.imports_ok", True):
            with patch(
                "app.pages_modules.consultants.show_consultants_list"
            ) as mock_show_list:
                with patch(
                    "app.pages_modules.consultants.show_add_consultant_form"
                ) as mock_show_form:
                    # Import et appel de la fonction
                    from app.pages_modules.consultants import show

                    # Exécution
                    show()

                    # Vérifications
                    mock_st.title.assert_called_with("👥 Gestion des consultants")
                    mock_show_list.assert_called_once()
                    mock_show_form.assert_called_once()

    @patch("app.pages_modules.consultants.st")
    def test_show_function_with_imports_failed(self, mock_st):
        """Test de la fonction show() avec imports échoués"""
        with patch("app.pages_modules.consultants.imports_ok", False):
            from app.pages_modules.consultants import show

            show()

            mock_st.error.assert_called_with(
                "❌ Les services de base ne sont pas disponibles"
            )

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_consultant_profile_success(
        self, mock_get_session, mock_st, mock_consultant
    ):
        """Test de l'affichage du profil consultant avec succès"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Mock both queries - first one for loading consultant data, second one for tabs
        mock_session.query().options().filter().first.return_value = mock_consultant
        mock_session.query().filter().first.return_value = mock_consultant

        # Mock session state correctement
        mock_st.session_state = Mock()
        mock_st.session_state.view_consultant_profile = 1

        # Mock columns to return context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock tabs to return context managers
        mock_tab1 = Mock()
        mock_tab1.__enter__ = Mock(return_value=mock_tab1)
        mock_tab1.__exit__ = Mock(return_value=None)
        mock_tab2 = Mock()
        mock_tab2.__enter__ = Mock(return_value=mock_tab2)
        mock_tab2.__exit__ = Mock(return_value=None)
        mock_tab3 = Mock()
        mock_tab3.__enter__ = Mock(return_value=mock_tab3)
        mock_tab3.__exit__ = Mock(return_value=None)
        mock_tab4 = Mock()
        mock_tab4.__enter__ = Mock(return_value=mock_tab4)
        mock_tab4.__exit__ = Mock(return_value=None)
        mock_tab5 = Mock()
        mock_tab5.__enter__ = Mock(return_value=mock_tab5)
        mock_tab5.__exit__ = Mock(return_value=None)
        mock_st.tabs.return_value = (
            mock_tab1,
            mock_tab2,
            mock_tab3,
            mock_tab4,
            mock_tab5,
        )

        # Mock the functions to avoid actual execution
        with patch("app.pages_modules.consultants.show_consultant_info") as mock_info:
            with patch(
                "app.pages_modules.consultants.show_consultant_skills"
            ) as mock_skills:
                with patch(
                    "app.pages_modules.consultants.show_consultant_languages"
                ) as mock_lang:
                    with patch(
                        "app.pages_modules.consultants.show_consultant_missions"
                    ) as mock_miss:
                        with patch(
                            "app.pages_modules.consultants.show_consultant_documents"
                        ) as mock_docs:
                            from app.pages_modules.consultants import (
                                show_consultant_profile,
                            )

                            show_consultant_profile()

                            # Just check that title was called for now
                            mock_st.title.assert_called_with("👤 Profil de Jean Dupont")

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_consultant_profile_not_found(self, mock_get_session, mock_st):
        """Test de l'affichage du profil consultant introuvable"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query().options().filter().first.return_value = None

        # Mock session state correctement
        mock_st.session_state = Mock()
        mock_st.session_state.view_consultant_profile = 999

        from app.pages_modules.consultants import show_consultant_profile

        show_consultant_profile()

        mock_st.error.assert_called_with("❌ Consultant introuvable")

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_consultant_info_form_submission(
        self, mock_service, mock_get_session, mock_st, mock_consultant
    ):
        """Test de la soumission du formulaire d'informations consultant"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock the consultant returned by the query with proper attributes
        class MockConsultant:
            def __init__(self):
                self.prenom = "Jean"
                self.nom = "Dupont"
                self.email = "jean@example.com"
                self.telephone = "01.23.45.67.89"
                self.salaire_actuel = 50000
                self.disponibilite = True
                self.notes = "Consultant expérimenté"
                self.practice_id = 1
                self.business_manager_actuel = None  # Important: None, not Mock
                self.societe = "Quanteam"
                self.date_entree_societe = date(2020, 1, 1)
                self.date_sortie_societe = None
                self.date_premiere_mission = date(2020, 6, 1)
                self.grade = "Confirmé"
                self.type_contrat = "CDI"

        mock_consultant_db = MockConsultant()

        # Configure the query chain properly to return our mock consultant
        mock_query_chain = Mock()
        mock_query_chain.options.return_value = mock_query_chain
        mock_query_chain.filter.return_value = mock_query_chain
        mock_query_chain.first.return_value = mock_consultant_db

        # Mock practices query
        mock_practice = Mock()
        mock_practice.nom = "Data Science"
        mock_practice.id = 1
        mock_practice_query = Mock()
        mock_practice_query.filter.return_value = mock_practice_query
        mock_practice_query.all.return_value = [mock_practice]

        # Set up session.query to return different things based on the model
        def query_side_effect(model):
            if hasattr(model, "__name__") and model.__name__ == "Consultant":
                return mock_query_chain
            elif hasattr(model, "__name__") and model.__name__ == "ConsultantSalaire":
                # Mock empty salary history
                mock_salary_query = Mock()
                mock_salary_query.filter.return_value = mock_salary_query
                mock_salary_query.order_by.return_value = mock_salary_query
                mock_salary_query.all.return_value = []
                return mock_salary_query
            else:  # Practice or other models
                return mock_practice_query

        mock_session.query.side_effect = query_side_effect  # Mock du service
        mock_service.update_consultant.return_value = True
        mock_service.get_consultant_by_email.return_value = (
            None  # No existing consultant with this email
        )

        # Mock du formulaire avec context manager
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form
        mock_st.form_submit_button.return_value = True

        # Mock des colonnes avec context managers - handle dynamic column counts
        def mock_columns_side_effect(num_cols_or_weights):
            if isinstance(num_cols_or_weights, list):
                num_cols = len(num_cols_or_weights)
            else:
                num_cols = num_cols_or_weights

            columns = []
            for i in range(num_cols):
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                columns.append(mock_col)
            return tuple(columns)

        mock_st.columns.side_effect = mock_columns_side_effect

        # Mock des inputs - use return_value instead of side_effect for simplicity
        mock_st.text_input.return_value = "Test Value"
        mock_st.number_input.return_value = 55000
        mock_st.checkbox.return_value = True
        mock_st.selectbox.return_value = "Test Option"
        mock_st.date_input.return_value = date(2020, 1, 1)
        mock_st.text_area.return_value = "Notes mises à jour"

        from app.pages_modules.consultants import show_consultant_info

        show_consultant_info(mock_consultant)

        mock_service.update_consultant.assert_called_once()

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_consultant_skills_technical(
        self, mock_get_session, mock_st, mock_consultant
    ):
        """Test de l'affichage des compétences techniques"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des compétences
        mock_competence = Mock()
        mock_competence.nom = "Python"
        mock_competence.categorie = "Langage"
        mock_competence.type_competence = "technique"

        mock_consultant_comp = Mock()
        mock_consultant_comp.niveau_maitrise = "avancé"
        mock_consultant_comp.annees_experience = 5

        # Set up the mock to return competencies when queried
        mock_query = Mock()
        mock_query.join.return_value.filter.return_value.all.return_value = [
            (mock_consultant_comp, mock_competence)
        ]
        mock_session.query.return_value = mock_query

        # Mock missions for technologies
        mock_mission = Mock()
        mock_mission.technologies_utilisees = "Python, Django"
        mock_session.query().filter().all.return_value = [mock_mission]

        # Mock des colonnes avec context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_col4 = Mock()
        mock_col4.__enter__ = Mock(return_value=mock_col4)
        mock_col4.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2, mock_col3, mock_col4)

        from app.pages_modules.consultants import _show_technical_skills

        _show_technical_skills(mock_consultant)

        # Vérifier qu'au moins une écriture a été faite
        assert mock_st.write.called or mock_st.subheader.called

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_consultant_languages(
        self, mock_get_session, mock_st, mock_consultant
    ):
        """Test de l'affichage des langues du consultant"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des langues
        mock_langue = Mock()
        mock_langue.nom = "Anglais"
        mock_langue.code_iso = "EN"

        mock_consultant_langue = Mock()
        mock_consultant_langue.langue = mock_langue
        mock_consultant_langue.niveau_label = "Avancé"
        mock_consultant_langue.commentaire = "TOEIC 900"

        mock_session.query().join().filter().all.return_value = [mock_consultant_langue]

        from app.pages_modules.consultants import show_consultant_languages

        show_consultant_languages(mock_consultant)

        mock_st.subheader.assert_called_with("🌍 Langues parlées")

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_consultant_missions_with_data(
        self, mock_get_session, mock_st, mock_consultant, mock_mission
    ):
        """Test de l'affichage des missions avec données"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query().filter().order_by().all.return_value = [mock_mission]

        from app.pages_modules.consultants import show_consultant_missions

        show_consultant_missions(mock_consultant)

        mock_st.subheader.assert_called_with("🚀 Historique des missions")

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_consultants_list_classic(
        self, mock_service, mock_get_session, mock_st
    ):
        """Test de la liste classique des consultants"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des données
        mock_consultants = [
            {
                "id": 1,
                "prenom": "Jean",
                "nom": "Dupont",
                "email": "jean@example.com",
                "societe": "Quanteam",
                "grade": "Confirmé",
                "type_contrat": "CDI",
                "salaire_actuel": 50000,
                "disponibilite": True,
                "practice_name": "Data Science",
                "experience_annees": 5,
                "nb_missions": 3,
                "salaire_formatted": "50 000€",
                "cjm_formatted": "2 083€",
                "experience_formatted": "5 ans",
                "statut": "Disponible",
            }
        ]

        mock_service.get_all_consultants_with_stats.return_value = mock_consultants

        # Mock dataframe
        mock_event = Mock()
        mock_event.selection.rows = []
        mock_st.dataframe.return_value = mock_event

        from app.pages_modules.consultants import show_consultants_list_classic

        show_consultants_list_classic()

        mock_st.text_input.assert_called()

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    @patch("app.pages_modules.consultants.ConsultantService")
    def test_show_add_consultant_form_success(
        self, mock_service, mock_get_session, mock_st
    ):
        """Test de l'ajout réussi d'un consultant"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock practice
        mock_practice = Mock()
        mock_practice.nom = "Data Science"
        mock_practice.id = 1
        mock_session.query().filter().all.return_value = [mock_practice]

        # Mock du service
        mock_service.get_consultant_by_email.return_value = None
        mock_service.create_consultant.return_value = True

        # Mock du formulaire avec context manager
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form
        mock_st.form_submit_button.return_value = True

        # Mock des colonnes avec context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock des inputs
        mock_st.text_input.side_effect = [
            "Jean",
            "jean@example.com",
            "01.23.45.67.89",
            "Dupont",
        ]
        mock_st.number_input.return_value = 50000
        mock_st.checkbox.return_value = True
        mock_st.selectbox.side_effect = ["Data Science", "Quanteam", "Confirmé", "CDI"]
        mock_st.date_input.side_effect = [date(2020, 1, 1), None, None]
        mock_st.text_area.return_value = "Nouveau consultant"

        from app.pages_modules.consultants import show_add_consultant_form

        show_add_consultant_form()

        mock_service.create_consultant.assert_called_once()

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_save_mission_changes_success(
        self, mock_get_session, mock_st, mock_mission
    ):
        """Test de la sauvegarde des modifications de mission"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query().filter().first.return_value = mock_mission

        mission_data = {
            "nom_mission": "Nouvelle mission",
            "client": "Nouveau client",
            "role": "Nouveau rôle",
            "date_debut": date(2023, 1, 1),
            "date_fin": date(2023, 12, 31),
            "statut": "en_cours",
            "revenus_generes": 80000,
            "technologies_utilisees": "Python, Django",
            "description": "Nouvelle description",
        }

        from app.pages_modules.consultants import save_mission_changes

        save_mission_changes(1, mission_data)

        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_with("✅ Mission mise à jour avec succès !")

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_delete_mission_success(self, mock_get_session, mock_st, mock_mission):
        """Test de la suppression d'une mission"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query().filter().first.return_value = mock_mission

        from app.pages_modules.consultants import delete_mission

        delete_mission(1)

        mock_session.delete.assert_called_once_with(mock_mission)
        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_with("✅ Mission supprimée avec succès !")

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_add_new_mission_success(self, mock_get_session, mock_st):
        """Test de l'ajout d'une nouvelle mission"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        mission_data = {
            "nom_mission": "Nouvelle mission",
            "client": "Nouveau client",
            "role": "Développeur",
            "date_debut": date(2023, 1, 1),
            "date_fin": date(2023, 12, 31),
            "statut": "en_cours",
            "revenus_generes": 60000,
            "technologies_utilisees": "Python, React",
            "description": "Description de la mission",
        }

        from app.pages_modules.consultants import add_new_mission

        add_new_mission(1, mission_data)

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_with("✅ Nouvelle mission ajoutée avec succès !")

    @patch("app.pages_modules.consultants.st")
    def test_show_cv_analysis_fullwidth(self, mock_st):
        """Test de l'affichage de l'analyse CV en pleine largeur"""

        # Create a simple session state that works with 'in' operator
        class SimpleSessionState:
            def __init__(self):
                self.cv_analysis = {
                    "analysis": {"missions": [], "competences": {}},
                    "consultant": Mock(prenom="Jean", nom="Dupont"),
                    "file_name": "cv.pdf",
                }

            def __contains__(self, key):
                return key == "cv_analysis"

            def __delattr__(self, name):
                pass  # Allow deletion without error

        mock_st.session_state = SimpleSessionState()

        # Mock des tabs avec context managers
        mock_tab1 = Mock()
        mock_tab1.__enter__ = Mock(return_value=mock_tab1)
        mock_tab1.__exit__ = Mock(return_value=None)
        mock_tab2 = Mock()
        mock_tab2.__enter__ = Mock(return_value=mock_tab2)
        mock_tab2.__exit__ = Mock(return_value=None)
        mock_tab3 = Mock()
        mock_tab3.__enter__ = Mock(return_value=mock_tab3)
        mock_tab3.__exit__ = Mock(return_value=None)
        mock_tab4 = Mock()
        mock_tab4.__enter__ = Mock(return_value=mock_tab4)
        mock_tab4.__exit__ = Mock(return_value=None)
        mock_st.tabs.return_value = (mock_tab1, mock_tab2, mock_tab3, mock_tab4)

        # Mock columns for different calls - the function needs different numbers of columns
        def mock_columns_side_effect(num_cols_or_weights):
            if isinstance(num_cols_or_weights, list):
                num_cols = len(num_cols_or_weights)
            else:
                num_cols = num_cols_or_weights

            columns = []
            for i in range(num_cols):
                mock_col = Mock()
                mock_col.__enter__ = Mock(return_value=mock_col)
                mock_col.__exit__ = Mock(return_value=None)
                columns.append(mock_col)
            return tuple(columns)

        mock_st.columns.side_effect = mock_columns_side_effect

        from app.pages_modules.consultants import show_cv_analysis_fullwidth

        show_cv_analysis_fullwidth()

        # Verify that some UI components were called (relaxed assertion)
        assert (
            mock_st.tabs.called or mock_st.markdown.called or mock_st.container.called
        )

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_mission_readonly(self, mock_get_session, mock_st, mock_mission):
        """Test de l'affichage en lecture seule d'une mission"""
        # Set mission attributes to avoid formatting issues
        mock_mission.client = "Test Client"
        mock_mission.role = "Developer"
        mock_mission.date_debut = date(2023, 1, 1)
        mock_mission.date_fin = date(2023, 12, 31)
        mock_mission.technologies_utilisees = "Python, Django"
        mock_mission.description = "Test mission"
        mock_mission.tjm = None  # Set to None to avoid formatting
        mock_mission.taux_journalier = None
        mock_mission.revenus_generes = 50000

        # Mock des colonnes avec context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        from app.pages_modules.consultants import show_mission_readonly

        show_mission_readonly(mock_mission)

        mock_st.write.assert_called()

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_mission_edit_form(self, mock_get_session, mock_st, mock_mission):
        """Test du formulaire d'édition de mission"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query().filter().first.return_value = mock_mission

        # Mock du formulaire avec context manager
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form
        mock_st.form_submit_button.return_value = False  # Pas de soumission

        # Mock des colonnes avec context managers (need 3 for the buttons section)
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_col3 = Mock()
        mock_col3.__enter__ = Mock(return_value=mock_col3)
        mock_col3.__exit__ = Mock(return_value=None)
        mock_st.columns.side_effect = [
            (mock_col1, mock_col2),
            (mock_col1, mock_col2, mock_col3),
        ]  # First call returns 2, second returns 3

        from app.pages_modules.consultants import show_mission_edit_form

        show_mission_edit_form(mock_mission)

        mock_st.form.assert_called_with(f"edit_mission_{mock_mission.id}")

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_show_add_mission_form(self, mock_get_session, mock_st, mock_consultant):
        """Test du formulaire d'ajout de mission"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du formulaire avec context manager
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form
        mock_st.form_submit_button.return_value = False  # Pas de soumission

        # Mock des colonnes avec context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        from app.pages_modules.consultants import show_add_mission_form

        show_add_mission_form(mock_consultant)

        mock_st.markdown.assert_called_with("### ➕ Ajouter une nouvelle mission")

    # Tests pour les formulaires de compétences

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_add_technical_skill_form(self, mock_get_session, mock_st, mock_consultant):
        """Test du formulaire d'ajout de compétence technique"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du formulaire avec context manager
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form
        mock_st.form_submit_button.return_value = False  # Pas de soumission

        # Mock des colonnes avec context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock selectbox to return strings - need 3 values: category, competence, level
        mock_st.selectbox.side_effect = ["Langage", "Python", "Intermédiaire"]

        # Mock COMPETENCES_TECHNIQUES to include "Langage"
        mock_competences = {"Langage": ["Python", "Java", "JavaScript"]}
        with patch("utils.skill_categories.COMPETENCES_TECHNIQUES", mock_competences):
            from app.pages_modules.consultants import _add_technical_skill_form

            _add_technical_skill_form(mock_consultant)

            # Check that selectbox was called at least 3 times
            assert mock_st.selectbox.call_count >= 3

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_add_functional_skill_form(
        self, mock_get_session, mock_st, mock_consultant
    ):
        """Test du formulaire d'ajout de compétence fonctionnelle"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du formulaire avec context manager
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form
        mock_st.form_submit_button.return_value = False  # Pas de soumission

        # Mock des colonnes avec context managers
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        # Mock selectbox pour retourner une valeur - need 3 values: category, competence, level
        mock_st.selectbox.side_effect = ["Gestion de projet", "Agile", "Avancé"]

        # Mock COMPETENCES_FONCTIONNELLES to include "Gestion de projet"
        mock_competences = {"Gestion de projet": ["Agile", "Scrum", "Kanban"]}
        with patch(
            "utils.skill_categories.COMPETENCES_FONCTIONNELLES", mock_competences
        ):
            from app.pages_modules.consultants import _add_functional_skill_form

            _add_functional_skill_form(mock_consultant)

            # Check that selectbox was called at least 3 times
            assert mock_st.selectbox.call_count >= 3

    @patch("app.pages_modules.consultants.st")
    @patch("app.pages_modules.consultants.get_database_session")
    def test_add_language_form(self, mock_get_session, mock_st, mock_consultant):
        """Test du formulaire d'ajout de langue"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock langues disponibles
        mock_langue = Mock()
        mock_langue.id = 1
        mock_langue.nom = "Anglais"
        mock_langue.code_iso = "EN"
        mock_session.query().order_by().all.return_value = [mock_langue]

        # Mock langues assignées (aucune)
        mock_session.query().filter().all.return_value = []

        # Mock du formulaire avec context manager
        mock_form = Mock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=None)
        mock_st.form.return_value = mock_form
        mock_st.form_submit_button.return_value = False  # Pas de soumission

        # Mock columns
        mock_col1 = Mock()
        mock_col1.__enter__ = Mock(return_value=mock_col1)
        mock_col1.__exit__ = Mock(return_value=None)
        mock_col2 = Mock()
        mock_col2.__enter__ = Mock(return_value=mock_col2)
        mock_col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = (mock_col1, mock_col2)

        from app.pages_modules.consultants import _add_language_form

        _add_language_form(mock_consultant)

        # Check that selectbox was called (for language selection)
        assert mock_st.selectbox.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
