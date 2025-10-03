"""
Tests unitaires pour consultants.py - Version corrigée
Tests des fonctions internes avec mocking approprié
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import date, datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))


class MockSessionState:
    """Mock de st.session_state avec structure complète"""

    def __init__(self):
        self.data = {
            "consultant_id": 1,
            "consultants_filter": "",
            "consultants_search": "",
            "practice_filter": "Tous",
            "entite_filter": "Toutes",
            "availability_filter": "Tous",
            "selected_consultant_ids": [],
            "consultant_selection_method": "table",
            "show_export_options": False,
            "show_analysis_options": False,
            "edit_mode": False,
            "consultant_data": None,
            "consultant_db": None,
            "form_data": {},
        }

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __contains__(self, key):
        return key in self.data


class TestConsultantsFixedCoverage(unittest.TestCase):
    """Tests pour les fonctions spécifiques de consultants.py"""

    def setUp(self):
        """Setup des mocks communs"""
        self.mock_session_state = MockSessionState()
        self.mock_consultant = MagicMock()
        self.mock_consultant.date_entree = date(2022, 1, 1)
        self.mock_consultant.date_sortie = date(2023, 12, 31)
        self.mock_consultant.date_premiere_mission = date(2022, 1, 15)
        self.mock_consultant.id = 1
        self.mock_consultant.prenom = "Jean"
        self.mock_consultant.to_dict = lambda: {"prenom": "Jean", "nom": "Dupont", "practice_name": "Practice Test"}
        self.mock_consultant.nom = "Dupont"
        self.mock_consultant.email = "jean.dupont@test.com"
        self.mock_consultant.telephone = "0123456789"
        self.mock_consultant.salaire_actuel = 50000
        self.mock_consultant.disponibilite = "Disponible"
        self.mock_consultant.notes = "Notes test"
        self.mock_consultant.practice_id = 1
        self.mock_consultant.business_manager_actuel = None

        # Mock column
        self.mock_col = MagicMock()
        self.mock_col.__enter__ = Mock(return_value=self.mock_col)
        self.mock_col.__exit__ = Mock(return_value=None)

    def test_load_consultant_data_success(self):
        """Test _load_consultant_data avec succès"""
        consultant_id = 1
        mock_practice = MagicMock()
        mock_practice.nom = "Practice Test"
        self.mock_consultant.practice = mock_practice

        with patch("app.pages_modules.consultants.get_database_session") as mock_get_session:
            mock_session = MagicMock()
            mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = (
                self.mock_consultant
            )
            mock_get_session.return_value.__enter__.return_value = mock_session

            from app.pages_modules.consultants import _load_consultant_data

            result = _load_consultant_data(consultant_id)

            # Vérifications
            self.assertIsNotNone(result)
            consultant_data, consultant_db = result
            self.assertEqual(consultant_data["prenom"], "Jean")
            self.assertEqual(consultant_data["nom"], "Dupont")
            self.assertEqual(consultant_data["practice_name"], "Practice Test")

    def test_load_consultant_data_not_found(self):
        """Test _load_consultant_data consultant non trouvé"""
        consultant_id = 999

        with patch("app.pages_modules.consultants.get_database_session") as mock_get_session:
            mock_session = MagicMock()
            mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = None
            mock_get_session.return_value.__enter__.return_value = mock_session

            from app.pages_modules.consultants import _load_consultant_data

            result = _load_consultant_data(consultant_id)

            # Vérifications
            self.assertIsNotNone(result)
            consultant_data, consultant_db = result
            self.assertIsNone(consultant_data)
            self.assertIsNone(consultant_db)
            self.assertIsNone(consultant_data)
            self.assertIsNone(consultant_db)

    @patch("app.pages_modules.consultants.st.columns")
    @patch("app.pages_modules.consultants.st.title")
    @patch("app.pages_modules.consultants.st.markdown")
    def test_display_consultant_header(self, mock_markdown, mock_title, mock_columns):
        """Test _display_consultant_header"""
        mock_columns.return_value = (self.mock_col, self.mock_col)
        consultant_data = {"prenom": "Jean", "nom": "Dupont", "practice_name": "Practice Test"}

        from app.pages_modules.consultants import _display_consultant_header

        _display_consultant_header(consultant_data)

        # Vérifications
        mock_columns.assert_called_once_with([6, 1])
        mock_title.assert_called()

    def test_extract_business_manager_info_with_manager(self):
        """Test _extract_business_manager_info avec business manager"""
        mock_bm = MagicMock()
        mock_bm.nom_complet = "Marie Martin"
        mock_bm.email = "marie.martin@test.com"
        self.mock_consultant.business_manager_actuel = mock_bm

        from app.pages_modules.consultants import _extract_business_manager_info

        result = _extract_business_manager_info(self.mock_consultant)

        # Vérifications
        self.assertIsNotNone(result)
        bm_nom_complet, bm_email = result
        self.assertEqual(bm_nom_complet, "Marie Martin")
        self.assertEqual(bm_email, "marie.martin@test.com")

    def test_extract_business_manager_info_without_manager(self):
        """Test _extract_business_manager_info sans business manager"""
        self.mock_consultant.business_manager_actuel = None

        from app.pages_modules.consultants import _extract_business_manager_info

        result = _extract_business_manager_info(self.mock_consultant)

        # Vérifications
        bm_nom_complet, bm_email = result
        self.assertIsNone(bm_nom_complet)
        self.assertIsNone(bm_email)

    def test_get_current_practice_id_with_practice(self):
        """Test _get_current_practice_id avec practice"""
        self.mock_consultant.practice_id = 5

        from app.pages_modules.consultants import _get_current_practice_id

        result = _get_current_practice_id(self.mock_consultant)

        # Vérifications
        self.assertEqual(result, 5)

    def test_get_current_practice_id_without_practice(self):
        """Test _get_current_practice_id sans practice"""
        delattr(self.mock_consultant, "practice_id")

        from app.pages_modules.consultants import _get_current_practice_id

        result = _get_current_practice_id(self.mock_consultant)

        # Vérifications
        self.assertIsNone(result)

    def test_build_update_data_complete(self):
        """Test _build_update_data avec toutes les données"""
        form_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@test.com",
            "telephone": "0123456789",
            "salaire": 55000,  # Clé correcte
            "disponibilite": "Disponible",
            "notes": "Notes test",
            "selected_practice_id": 1,
            "societe": "France",
            "date_entree": date.today(),
            "date_sortie": None,
            "date_premiere_mission": None,
            "grade": "Senior",
            "type_contrat": "CDI",
        }

        from app.pages_modules.consultants import _build_update_data

        result = _build_update_data(form_data)

        # Vérifications
        self.assertIsInstance(result, dict)
        self.assertEqual(result["prenom"], "Jean")
        self.assertEqual(result["nom"], "Dupont")
        self.assertEqual(result["email"], "jean.dupont@test.com")
        self.assertEqual(result["salaire_actuel"], 55000)

    @patch("app.pages_modules.consultants.st.columns")
    @patch("app.pages_modules.consultants.st.text_input")
    @patch("app.pages_modules.consultants.st.number_input")
    @patch("app.pages_modules.consultants.st.selectbox")
    @patch("app.pages_modules.consultants.st.info")
    def test_render_basic_consultant_fields(self, mock_info, mock_select, mock_number, mock_text, mock_columns):
        """Test _render_basic_consultant_fields"""
        # Setup
        mock_columns.return_value = (self.mock_col, self.mock_col)
        mock_text.side_effect = ["Jean", "jean.dupont@test.com", "Non assigné", "Dupont", "0123456789"]
        mock_select.side_effect = ["Senior", "CDI", "Disponible"]
        mock_number.return_value = 50000

        with patch("app.services.practice_service.PracticeService") as mock_practice_service:
            mock_practice_service.get_all_practices.return_value = []

            from app.pages_modules.consultants import _render_basic_consultant_fields

            # Signature correcte de la fonction
            result = _render_basic_consultant_fields(
                self.mock_consultant,
                {"Practice Test": 1},  # practice_options comme dictionnaire
                1,  # current_practice_id
                "Marie Martin",  # bm_nom_complet
                "marie.martin@test.com",  # bm_email
            )

            # Vérifications
            mock_columns.assert_called()
            mock_text.assert_called()

    @patch("app.pages_modules.consultants.get_database_session")
    @patch("app.pages_modules.consultants.st.subheader")
    @patch("app.pages_modules.consultants.st.markdown")
    def test_manage_salary_history(self, mock_markdown, mock_subheader, mock_session):
        """Test _manage_salary_history"""
        # Setup mock consultant avec attributs nécessaires
        self.mock_consultant.id = 1
        self.mock_consultant.salaire_actuel = None  # Pas de salaire actuel

        # Setup mock session context manager
        mock_context = MagicMock()
        mock_session.return_value = mock_context
        mock_context.__enter__.return_value = mock_context
        mock_context.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

        from app.pages_modules.consultants import _manage_salary_history

        # Mock st.info car il sera appelé quand salaires est vide
        with patch("app.pages_modules.consultants.st.info") as mock_info:
            _manage_salary_history(self.mock_consultant)
            mock_info.assert_called_with("📊 Aucun historique de salaire disponible")

        # Vérifications
        mock_subheader.assert_called()
        mock_markdown.assert_called()

    @patch("app.pages_modules.consultants.st.form")
    @patch("app.pages_modules.consultants.st.selectbox")
    @patch("streamlit.slider")
    @patch("app.pages_modules.consultants.st.form_submit_button")
    def test_add_technical_skill_form_no_submit(self, mock_submit, mock_slider, mock_select, mock_form):
        """Test _add_technical_skill_form sans soumission"""
        # Setup
        mock_form.return_value.__enter__ = Mock()
        mock_form.return_value.__exit__ = Mock()
        mock_select.side_effect = ["Backend", "Python", "Expert"]  # Catégorie, compétence, niveau
        mock_slider.return_value = 3
        mock_submit.return_value = False

        with patch("app.services.technology_service.TechnologyService") as mock_tech_service:
            mock_tech_service.get_all_technologies.return_value = []

            from app.pages_modules.consultants import _add_technical_skill_form

            _add_technical_skill_form(self.mock_consultant)

            # Vérifications
            mock_submit.assert_called()

    @patch("app.pages_modules.consultants.st.selectbox")
    @patch("app.pages_modules.consultants.st.slider")
    @patch("app.pages_modules.consultants.st.form_submit_button")
    @patch("app.pages_modules.consultants.st.success")
    def test_add_technical_skill_form_success(self, mock_success, mock_form_submit_button, mock_slider, mock_selectbox):
        """Test _add_technical_skill_form avec succès"""
        # Setup - Enlever les références à mock_form
        mock_selectbox.side_effect = ["Backend", "Python", "Expert"]  # Catégorie, compétence, niveau
        mock_slider.return_value = 3
        mock_form_submit_button.return_value = True

        with patch("app.services.consultant_service.ConsultantService") as mock_service, patch(
            "app.services.technology_service.TechnologyService"
        ) as mock_tech_service, patch("app.pages_modules.consultants.get_database_session") as mock_get_session, patch(
            "app.pages_modules.consultants.st.rerun"
        ):

            # Mock session
            mock_session = MagicMock()
            mock_get_session.return_value.__enter__.return_value = mock_session
            mock_session.query.return_value.filter.return_value.first.return_value = None  # Pas de compétence existante

            mock_tech_service.get_all_technologies.return_value = []
            mock_service.add_technical_skill_to_consultant.return_value = True

            from app.pages_modules.consultants import _add_technical_skill_form

            _add_technical_skill_form(self.mock_consultant)

            # Vérifications
            mock_success.assert_called()

    @patch("app.pages_modules.consultants.st.selectbox")
    @patch("app.pages_modules.consultants.st.slider")
    @patch("app.pages_modules.consultants.st.form_submit_button")
    @patch("app.pages_modules.consultants.st.success")
    def test_add_functional_skill_form_success(
        self, mock_success, mock_form_submit_button, mock_slider, mock_selectbox
    ):
        """Test _add_functional_skill_form avec succès"""
        # Setup - Enlever les références à mock_form
        mock_selectbox.side_effect = [
            "Banque de Détail",
            "Conseil clientèle particuliers",
            "Expert",
        ]  # Catégorie, compétence, niveau
        mock_slider.return_value = 4
        mock_form_submit_button.return_value = True

        with patch("app.services.consultant_service.ConsultantService") as mock_service, patch(
            "app.pages_modules.consultants.get_database_session"
        ) as mock_get_session, patch("app.pages_modules.consultants.st.rerun") as mock_rerun:

            # Mock session
            mock_session = MagicMock()
            mock_get_session.return_value.__enter__.return_value = mock_session
            mock_session.query.return_value.filter.return_value.first.return_value = None  # Pas de compétence existante

            mock_service.get_functional_skills.return_value = []
            mock_service.add_functional_skill_to_consultant.return_value = True

            from app.pages_modules.consultants import _add_functional_skill_form

            _add_functional_skill_form(self.mock_consultant)

            # Vérifications
            mock_success.assert_called()

    def test_should_add_initial_salary_entry_true(self):
        """Test _should_add_initial_salary_entry retourne True"""
        mock_consultant = MagicMock()
        mock_consultant.salaire_actuel = 50000
        salaires = []  # Pas d'historique

        from app.pages_modules.consultants import _should_add_initial_salary_entry

        result = _should_add_initial_salary_entry(mock_consultant, salaires)

        # Vérifications
        self.assertTrue(result)

    def test_should_add_initial_salary_entry_false_no_salary(self):
        """Test _should_add_initial_salary_entry retourne False sans salaire"""
        mock_consultant = MagicMock()
        mock_consultant.salaire_actuel = None
        salaires = []

        from app.pages_modules.consultants import _should_add_initial_salary_entry

        result = _should_add_initial_salary_entry(mock_consultant, salaires)

        # Vérifications
        self.assertFalse(result)

    @patch("app.pages_modules.consultants.st.date_input")
    @patch("app.pages_modules.consultants.st.selectbox")
    def test_render_date_entree_field(self, mock_select, mock_date):
        """Test _render_date_entree_field"""
        mock_date.return_value = date.today()
        # Mock consultant avec vraie date
        self.mock_consultant.date_entree = date(2022, 1, 1)

        from app.pages_modules.consultants import _render_date_entree_field

        result = _render_date_entree_field(self.mock_consultant)

        # Vérifications
        mock_date.assert_called()
        self.assertEqual(result, date.today())

    @patch("app.pages_modules.consultants.st.date_input")
    def test_render_date_sortie_field(self, mock_date):
        """Test _render_date_sortie_field"""
        mock_date.return_value = date.today()
        # Mock consultant avec vraie date
        self.mock_consultant.date_sortie = date(2023, 12, 31)

        from app.pages_modules.consultants import _render_date_sortie_field

        result = _render_date_sortie_field(self.mock_consultant)

        # Vérifications
        mock_date.assert_called()
        self.assertEqual(result, date.today())

    @patch("app.pages_modules.consultants.st.date_input")
    def test_render_date_premiere_mission_field(self, mock_date):
        """Test _render_date_premiere_mission_field"""
        mock_date.return_value = date.today()
        # Mock consultant avec vraie date
        self.mock_consultant.date_premiere_mission = date(2022, 1, 15)

        from app.pages_modules.consultants import _render_date_premiere_mission_field

        result = _render_date_premiere_mission_field(self.mock_consultant)

        # Vérifications
        mock_date.assert_called()
        self.assertEqual(result, date.today())

    @patch("app.pages_modules.consultants.st.selectbox")
    def test_render_societe_field(self, mock_select):
        """Test _render_societe_field"""
        mock_select.return_value = "France"

        from app.pages_modules.consultants import _render_societe_field

        result = _render_societe_field(self.mock_consultant)

        # Vérifications
        mock_select.assert_called()
        self.assertEqual(result, "France")

    @patch("app.pages_modules.consultants.st.write")
    @patch("app.pages_modules.consultants.st.info")
    def test_display_no_functional_skills_message(self, mock_info, mock_write):
        """Test _display_no_functional_skills_message"""
        from app.pages_modules.consultants import _display_no_functional_skills_message

        _display_no_functional_skills_message()

        # Vérifications
        mock_info.assert_called()


if __name__ == "__main__":
    unittest.main()
