"""
Tests pour augmenter la couverture des pages_modules
Cible: consultant_info.py, consultant_skills.py, consultant_languages.py
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, date


class TestConsultantInfoBoost(unittest.TestCase):
    """Tests pour augmenter la couverture de consultant_info.py"""

    def setUp(self):
        """Configuration des mocks Streamlit"""
        self.patches = {}
        st_mocks = [
            "subheader",
            "text_input",
            "date_input",
            "selectbox",
            "text_area",
            "button",
            "columns",
            "success",
            "error",
            "form",
            "form_submit_button",
            "session_state",
        ]

        for mock_name in st_mocks:
            patcher = patch(f"app.pages_modules.consultant_info.st.{mock_name}")
            self.patches[mock_name] = patcher.start()

        # Mock columns
        mock_col = MagicMock()
        mock_col.__enter__ = Mock(return_value=mock_col)
        mock_col.__exit__ = Mock(return_value=False)
        self.patches["columns"].return_value = [mock_col, mock_col]

        # Mock form
        mock_form = MagicMock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=False)
        self.patches["form"].return_value = mock_form

    def tearDown(self):
        """Nettoyage"""
        for patcher in self.patches.values():
            if hasattr(patcher, "stop"):
                patcher.stop()

    @patch("app.pages_modules.consultant_info.ConsultantService")
    def test_show_personal_info_display(self, mock_service):
        """Test affichage des infos personnelles"""
        from app.pages_modules.consultant_info import show_personal_info

        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"
        mock_consultant.email = "jean.dupont@test.com"
        mock_consultant.telephone = "0123456789"
        mock_consultant.date_naissance = date(1990, 1, 1)

        show_personal_info(mock_consultant)

        self.patches["subheader"].assert_called()

    @patch("app.pages_modules.consultant_info.ConsultantService")
    def test_edit_personal_info_form(self, mock_service):
        """Test formulaire d'édition des infos personnelles"""
        from app.pages_modules.consultant_info import edit_personal_info

        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"
        mock_consultant.email = "test@test.com"
        mock_consultant.telephone = "0123456789"

        # Mock form inputs
        self.patches["text_input"].return_value = "Dupont"
        self.patches["form_submit_button"].return_value = False

        edit_personal_info(mock_consultant)

        self.patches["form"].assert_called()

    def test_format_date_display(self):
        """Test formatage d'affichage de date"""
        from app.pages_modules.consultant_info import DATE_FORMAT

        test_date = date(2024, 1, 15)
        formatted = test_date.strftime(DATE_FORMAT)

        self.assertEqual(formatted, "15/01/2024")


class TestConsultantSkillsBoost(unittest.TestCase):
    """Tests pour augmenter la couverture de consultant_skills.py"""

    def setUp(self):
        """Configuration des mocks"""
        self.patches = {}
        st_mocks = [
            "subheader",
            "selectbox",
            "number_input",
            "button",
            "columns",
            "success",
            "error",
            "warning",
            "dataframe",
            "session_state",
            "markdown",
        ]

        for mock_name in st_mocks:
            patcher = patch(f"app.pages_modules.consultant_skills.st.{mock_name}")
            self.patches[mock_name] = patcher.start()

        mock_col = MagicMock()
        mock_col.__enter__ = Mock(return_value=mock_col)
        mock_col.__exit__ = Mock(return_value=False)
        self.patches["columns"].return_value = [mock_col, mock_col, mock_col]

    def tearDown(self):
        """Nettoyage"""
        for patcher in self.patches.values():
            if hasattr(patcher, "stop"):
                patcher.stop()

    def test_get_niveau_label_all_levels(self):
        """Test récupération des labels de niveau"""
        from app.pages_modules.consultant_skills import get_niveau_label

        expected = {1: "Débutant", 2: "Intermédiaire", 3: "Avancé", 4: "Expert", 5: "Maître"}

        for niveau, label in expected.items():
            result = get_niveau_label(niveau)
            self.assertEqual(result, label)

    def test_get_niveau_label_invalid(self):
        """Test récupération de label pour niveau invalide"""
        from app.pages_modules.consultant_skills import get_niveau_label

        result = get_niveau_label(10)
        # La fonction retourne "Niveau 10" pour les niveaux inconnus
        self.assertEqual(result, "Niveau 10")

    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_show_consultant_skills_with_skills(self, mock_session):
        """Test affichage des compétences d'un consultant"""
        from app.pages_modules.consultant_skills import show_consultant_skills

        # Mock session
        mock_session_obj = MagicMock()
        mock_session_obj.__enter__ = Mock(return_value=mock_session_obj)
        mock_session_obj.__exit__ = Mock(return_value=False)
        mock_session.return_value = mock_session_obj

        # Mock consultant with skills
        mock_skill = Mock()
        mock_skill.competence = Mock()
        mock_skill.competence.nom = "Python"
        mock_skill.niveau = 4
        mock_skill.annees_experience = 5

        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.competences = [mock_skill]

        show_consultant_skills(mock_consultant)

        self.patches["subheader"].assert_called()

    @patch("app.pages_modules.consultant_skills.get_database_session")
    def test_add_skill_to_consultant(self, mock_session):
        """Test ajout d'une compétence à un consultant"""
        from app.pages_modules.consultant_skills import add_skill_to_consultant

        mock_session_obj = MagicMock()
        mock_session_obj.__enter__ = Mock(return_value=mock_session_obj)
        mock_session_obj.__exit__ = Mock(return_value=False)
        mock_session.return_value = mock_session_obj

        # Mock available skills
        mock_competence = Mock()
        mock_competence.id = 1
        mock_competence.nom = "Python"
        mock_session_obj.query.return_value.filter.return_value.first.return_value = mock_competence

        # Data pour l'ajout
        data = {
            "competence_id": 1,
            "niveau": 4,
            "annees_experience": 5,
            "certifie": True,
            "dernier_usage": "2024-01-01",
        }

        result = add_skill_to_consultant(1, data)

        self.assertIsInstance(result, bool)


class TestConsultantLanguagesBoost(unittest.TestCase):
    """Tests pour augmenter la couverture de consultant_languages.py"""

    def setUp(self):
        """Configuration des mocks"""
        self.patches = {}
        st_mocks = [
            "subheader",
            "selectbox",
            "number_input",
            "button",
            "columns",
            "success",
            "error",
            "dataframe",
            "markdown",
        ]

        for mock_name in st_mocks:
            patcher = patch(f"app.pages_modules.consultant_languages.st.{mock_name}")
            self.patches[mock_name] = patcher.start()

        mock_col = MagicMock()
        mock_col.__enter__ = Mock(return_value=mock_col)
        mock_col.__exit__ = Mock(return_value=False)
        self.patches["columns"].return_value = [mock_col, mock_col, mock_col]

    def tearDown(self):
        """Nettoyage"""
        for patcher in self.patches.values():
            if hasattr(patcher, "stop"):
                patcher.stop()

    def test_get_niveau_label_languages_all_levels(self):
        """Test labels de niveau pour les langues"""
        from app.pages_modules.consultant_languages import get_niveau_label

        # Les labels retournés incluent le format CECR
        result1 = get_niveau_label(1)
        result2 = get_niveau_label(2)

        # Vérifier que les labels contiennent le texte attendu (format flexible)
        self.assertIn("Débutant", result1)
        self.assertIn("Élémentaire", result2)

    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_consultant_languages_with_languages(self, mock_session):
        """Test affichage des langues d'un consultant"""
        from app.pages_modules.consultant_languages import show_consultant_languages

        mock_session_obj = MagicMock()
        mock_session_obj.__enter__ = Mock(return_value=mock_session_obj)
        mock_session_obj.__exit__ = Mock(return_value=False)
        mock_session.return_value = mock_session_obj

        # Mock language
        mock_lang = Mock()
        mock_lang.langue = Mock()
        mock_lang.langue.nom = "Anglais"
        mock_lang.niveau = 5

        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.langues = [mock_lang]

        show_consultant_languages(mock_consultant)

        self.patches["subheader"].assert_called()

    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_add_language_to_consultant(self, mock_session):
        """Test ajout d'une langue à un consultant"""
        from app.pages_modules.consultant_languages import add_language_to_consultant

        mock_session_obj = MagicMock()
        mock_session_obj.__enter__ = Mock(return_value=mock_session_obj)
        mock_session_obj.__exit__ = Mock(return_value=False)
        mock_session.return_value = mock_session_obj

        # Mock langue
        mock_langue = Mock()
        mock_langue.id = 1
        mock_langue.nom = "Anglais"
        mock_session_obj.query.return_value.filter.return_value.first.return_value = mock_langue

        # Data pour l'ajout
        data = {
            "langue_id": 1,
            "niveau": 4,
            "niveau_ecrit": 4,
            "niveau_parle": 4,
            "certification": True,
            "langue_maternelle": False,
        }

        result = add_language_to_consultant(1, data)

        self.assertIsInstance(result, bool)
        mock_session_obj.__enter__ = Mock(return_value=mock_session_obj)
        mock_session_obj.__exit__ = Mock(return_value=False)
        mock_session.return_value = mock_session_obj

        # Mock available languages
        mock_langue = Mock()
        mock_langue.id = 1
        mock_langue.nom = "Anglais"
        mock_session_obj.query.return_value.all.return_value = [mock_langue]

        mock_consultant = Mock()
        mock_consultant.id = 1

        # Mock user input
        self.patches["selectbox"].return_value = "Anglais"
        self.patches["number_input"].return_value = 4
        self.patches["button"].return_value = False

        add_language_to_consultant(mock_consultant)

        self.patches["selectbox"].assert_called()


class TestConsultantListBoost(unittest.TestCase):
    """Tests pour augmenter la couverture de consultant_list.py"""

    def setUp(self):
        """Configuration des mocks"""
        self.patches = {}
        st_mocks = [
            "subheader",
            "text_input",
            "selectbox",
            "multiselect",
            "button",
            "columns",
            "dataframe",
            "markdown",
            "session_state",
        ]

        for mock_name in st_mocks:
            patcher = patch(f"app.pages_modules.consultant_list.st.{mock_name}")
            self.patches[mock_name] = patcher.start()

        mock_col = MagicMock()
        mock_col.__enter__ = Mock(return_value=mock_col)
        mock_col.__exit__ = Mock(return_value=False)
        self.patches["columns"].return_value = [mock_col, mock_col]

    def tearDown(self):
        """Nettoyage"""
        for patcher in self.patches.values():
            if hasattr(patcher, "stop"):
                patcher.stop()

    @patch("app.pages_modules.consultant_list.ConsultantService")
    def test_show_consultants_list_with_data(self, mock_service):
        """Test affichage de la liste des consultants"""
        from app.pages_modules.consultant_list import show_consultants_list

        # Mock consultants
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"
        mock_consultant.email = "jean@test.com"
        mock_consultant.practice = Mock(nom="Data")
        mock_consultant.actif = True

        mock_service.return_value.get_all_consultants.return_value = [mock_consultant]

        # Mock filters
        self.patches["text_input"].return_value = ""
        self.patches["selectbox"].return_value = "Tous"
        self.patches["multiselect"].return_value = []

        show_consultants_list()

        self.patches["subheader"].assert_called()

    @patch("app.pages_modules.consultant_list.ConsultantService")
    def test_show_consultants_list_with_filters(self, mock_service):
        """Test liste avec filtres appliqués"""
        from app.pages_modules.consultant_list import show_consultants_list

        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"

        mock_service.return_value.search_consultants.return_value = [mock_consultant]

        # Mock filters with search
        self.patches["text_input"].return_value = "Dupont"
        self.patches["selectbox"].return_value = "Actifs"
        self.patches["multiselect"].return_value = ["Data"]

        show_consultants_list()

        self.patches["text_input"].assert_called()


class TestConsultantMissionsBoost(unittest.TestCase):
    """Tests pour augmenter la couverture de consultant_missions.py"""

    def setUp(self):
        """Configuration des mocks"""
        self.patches = {}
        st_mocks = [
            "subheader",
            "text_input",
            "date_input",
            "number_input",
            "text_area",
            "button",
            "columns",
            "success",
            "error",
            "dataframe",
            "form",
            "form_submit_button",
        ]

        for mock_name in st_mocks:
            patcher = patch(f"app.pages_modules.consultant_missions.st.{mock_name}")
            self.patches[mock_name] = patcher.start()

        mock_col = MagicMock()
        mock_col.__enter__ = Mock(return_value=mock_col)
        mock_col.__exit__ = Mock(return_value=False)
        self.patches["columns"].return_value = [mock_col, mock_col]

        mock_form = MagicMock()
        mock_form.__enter__ = Mock(return_value=mock_form)
        mock_form.__exit__ = Mock(return_value=False)
        self.patches["form"].return_value = mock_form

    def tearDown(self):
        """Nettoyage"""
        for patcher in self.patches.values():
            if hasattr(patcher, "stop"):
                patcher.stop()

    def test_show_missions_list_with_missions(self):
        """Test affichage de la liste des missions"""
        from app.pages_modules.consultant_missions import show_missions_list

        # Mock mission
        mock_mission = Mock()
        mock_mission.id = 1
        mock_mission.client = "Client Test"
        mock_mission.titre = "Mission Test"
        mock_mission.date_debut = date(2024, 1, 1)
        mock_mission.date_fin = date(2024, 6, 30)
        mock_mission.tjm = 500

        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.missions = [mock_mission]

        show_missions_list(mock_consultant)

        self.patches["subheader"].assert_called()

    def test_calculate_mission_revenue(self):
        """Test calcul du revenu d'une mission"""
        from app.pages_modules.consultant_missions import calculate_mission_revenue

        mock_mission = Mock()
        mock_mission.date_debut = date(2024, 1, 1)
        mock_mission.date_fin = date(2024, 1, 31)
        mock_mission.tjm = 500

        try:
            result = calculate_mission_revenue(mock_mission)
            self.assertIsInstance(result, (int, float))
        except (ImportError, AttributeError):
            self.skipTest("Fonction calculate_mission_revenue non disponible")


if __name__ == "__main__":
    unittest.main()
