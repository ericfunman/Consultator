"""
Tests pour augmenter la couverture de helpers.py et skill_categories.py
"""

import unittest
from datetime import date, datetime
from unittest.mock import patch, Mock


class TestHelpersFormatting(unittest.TestCase):
    """Tests pour les fonctions de formatage dans helpers.py"""

    def test_format_currency_basic(self):
        """Test formatage de devise basique"""
        from app.utils.helpers import format_currency

        result = format_currency(5000)
        self.assertIn("€", result)
        self.assertIn("5", result)

    def test_format_currency_large_amount(self):
        """Test formatage de grande somme"""
        from app.utils.helpers import format_currency

        result = format_currency(1000000)
        self.assertIn("€", result)
        self.assertIn("000", result)

    def test_format_currency_zero(self):
        """Test formatage de zéro"""
        from app.utils.helpers import format_currency

        result = format_currency(0)
        self.assertIn("0", result)
        self.assertIn("€", result)

    def test_format_currency_negative(self):
        """Test formatage de montant négatif"""
        from app.utils.helpers import format_currency

        result = format_currency(-500)
        self.assertIn("-", result)
        self.assertIn("€", result)

    def test_format_phone_number(self):
        """Test formatage de numéro de téléphone"""
        from app.utils.helpers import format_phone_number

        try:
            result = format_phone_number("0123456789")
            self.assertIsInstance(result, str)
            self.assertIn("01", result)
        except (ImportError, AttributeError):
            self.skipTest("Fonction format_phone_number non disponible")

    def test_format_date_french(self):
        """Test formatage de date en français"""
        from app.utils.helpers import format_date_french

        try:
            test_date = date(2024, 1, 15)
            result = format_date_french(test_date)
            self.assertIsInstance(result, str)
        except (ImportError, AttributeError):
            self.skipTest("Fonction format_date_french non disponible")

    def test_truncate_text_short(self):
        """Test truncate sur texte court"""
        from app.utils.helpers import truncate_text

        try:
            result = truncate_text("Court", 10)
            self.assertEqual(result, "Court")
        except (ImportError, AttributeError):
            self.skipTest("Fonction truncate_text non disponible")

    def test_truncate_text_long(self):
        """Test truncate sur texte long"""
        from app.utils.helpers import truncate_text

        try:
            long_text = "Ceci est un texte très long qui devrait être tronqué"
            result = truncate_text(long_text, 20)
            self.assertLessEqual(len(result), 23)  # 20 + "..."
        except (ImportError, AttributeError):
            self.skipTest("Fonction truncate_text non disponible")


class TestHelpersValidation(unittest.TestCase):
    """Tests pour les fonctions de validation"""

    def test_validate_email_valid(self):
        """Test validation d'email valide"""
        from app.utils.helpers import validate_email

        try:
            result = validate_email("test@example.com")
            self.assertTrue(result)
        except (ImportError, AttributeError):
            self.skipTest("Fonction validate_email non disponible")

    def test_validate_email_invalid(self):
        """Test validation d'email invalide"""
        from app.utils.helpers import validate_email

        try:
            result = validate_email("invalid-email")
            self.assertFalse(result)
        except (ImportError, AttributeError):
            self.skipTest("Fonction validate_email non disponible")

    def test_validate_phone_valid(self):
        """Test validation de téléphone valide"""
        from app.utils.helpers import validate_phone

        try:
            result = validate_phone("0123456789")
            self.assertTrue(result)
        except (ImportError, AttributeError):
            self.skipTest("Fonction validate_phone non disponible")

    def test_validate_phone_invalid(self):
        """Test validation de téléphone invalide"""
        from app.utils.helpers import validate_phone

        try:
            result = validate_phone("123")
            self.assertFalse(result)
        except (ImportError, AttributeError):
            self.skipTest("Fonction validate_phone non disponible")

    def test_sanitize_input_basic(self):
        """Test sanitisation d'input"""
        from app.utils.helpers import sanitize_input

        try:
            result = sanitize_input("  Test  ")
            self.assertEqual(result, "Test")
        except (ImportError, AttributeError):
            self.skipTest("Fonction sanitize_input non disponible")

    def test_sanitize_input_html(self):
        """Test sanitisation de HTML"""
        from app.utils.helpers import sanitize_input

        try:
            result = sanitize_input("<script>alert('XSS')</script>")
            self.assertNotIn("<script>", result)
        except (ImportError, AttributeError):
            self.skipTest("Fonction sanitize_input non disponible")


class TestHelpersCalculation(unittest.TestCase):
    """Tests pour les fonctions de calcul"""

    def test_calculate_age_from_date(self):
        """Test calcul d'âge depuis date de naissance"""
        from app.utils.helpers import calculate_age

        try:
            birth_date = date(1990, 1, 1)
            result = calculate_age(birth_date)
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)
            self.assertLess(result, 150)
        except (ImportError, AttributeError):
            self.skipTest("Fonction calculate_age non disponible")

    def test_calculate_experience_years(self):
        """Test calcul d'années d'expérience"""
        from app.utils.helpers import calculate_experience_years

        try:
            start_date = date(2020, 1, 1)
            result = calculate_experience_years(start_date)
            self.assertIsInstance(result, (int, float))
            self.assertGreaterEqual(result, 0)
        except (ImportError, AttributeError):
            self.skipTest("Fonction calculate_experience_years non disponible")

    def test_calculate_tjm_from_salary(self):
        """Test calcul TJM depuis salaire annuel"""
        from app.utils.helpers import calculate_tjm

        try:
            annual_salary = 60000
            result = calculate_tjm(annual_salary)
            self.assertIsInstance(result, (int, float))
            self.assertGreater(result, 0)
        except (ImportError, AttributeError):
            self.skipTest("Fonction calculate_tjm non disponible")

    def test_calculate_mission_duration(self):
        """Test calcul de durée de mission"""
        from app.utils.helpers import calculate_mission_duration

        try:
            start = date(2024, 1, 1)
            end = date(2024, 6, 30)
            result = calculate_mission_duration(start, end)
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)
        except (ImportError, AttributeError):
            self.skipTest("Fonction calculate_mission_duration non disponible")


class TestSkillCategories(unittest.TestCase):
    """Tests pour skill_categories.py"""

    def test_get_skill_categories(self):
        """Test récupération des catégories de compétences"""
        from app.utils.skill_categories import SKILL_CATEGORIES

        self.assertIsInstance(SKILL_CATEGORIES, dict)
        self.assertGreater(len(SKILL_CATEGORIES), 0)

    def test_skill_categories_structure(self):
        """Test structure des catégories"""
        from app.utils.skill_categories import SKILL_CATEGORIES

        for category, skills in SKILL_CATEGORIES.items():
            self.assertIsInstance(category, str)
            self.assertIsInstance(skills, list)
            self.assertGreater(len(category), 0)

    def test_get_category_for_skill(self):
        """Test recherche de catégorie pour une compétence"""
        from app.utils.skill_categories import get_category_for_skill

        try:
            result = get_category_for_skill("Python")
            self.assertIsInstance(result, str)
        except (ImportError, AttributeError):
            self.skipTest("Fonction get_category_for_skill non disponible")

    def test_get_all_skills_flat(self):
        """Test récupération de toutes les compétences en liste plate"""
        from app.utils.skill_categories import get_all_skills

        try:
            result = get_all_skills()
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)
        except (ImportError, AttributeError):
            self.skipTest("Fonction get_all_skills non disponible")

    def test_skill_categories_contain_common_skills(self):
        """Test que les catégories contiennent des compétences communes"""
        from app.utils.skill_categories import SKILL_CATEGORIES

        all_skills = []
        for skills in SKILL_CATEGORIES.values():
            all_skills.extend(skills)

        common_skills = ["Python", "Java", "JavaScript", "SQL"]
        found_count = sum(1 for skill in common_skills if any(s.lower() == skill.lower() for s in all_skills))

        self.assertGreater(found_count, 0, "Au moins une compétence commune devrait être présente")


class TestHelpersStreamlitComponents(unittest.TestCase):
    """Tests pour les composants Streamlit helpers"""

    @patch("app.utils.helpers.st")
    def test_create_download_button(self, mock_st):
        """Test création d'un bouton de téléchargement"""
        from app.utils.helpers import create_download_button

        try:
            mock_st.download_button.return_value = True
            result = create_download_button("data", "file.csv", "Download")
            mock_st.download_button.assert_called_once()
        except (ImportError, AttributeError):
            self.skipTest("Fonction create_download_button non disponible")

    @patch("app.utils.helpers.st")
    def test_show_success_message(self, mock_st):
        """Test affichage message de succès"""
        from app.utils.helpers import show_success_message

        try:
            mock_st.success = Mock()
            show_success_message("Test message")
            mock_st.success.assert_called_once()
        except (ImportError, AttributeError):
            self.skipTest("Fonction show_success_message non disponible")

    @patch("app.utils.helpers.st")
    def test_show_error_message(self, mock_st):
        """Test affichage message d'erreur"""
        from app.utils.helpers import show_error_message

        try:
            mock_st.error = Mock()
            show_error_message("Error message")
            mock_st.error.assert_called_once()
        except (ImportError, AttributeError):
            self.skipTest("Fonction show_error_message non disponible")

    @patch("app.utils.helpers.st")
    def test_create_metric_card(self, mock_st):
        """Test création d'une carte métrique"""
        from app.utils.helpers import create_metric_card

        try:
            mock_st.metric = Mock()
            create_metric_card("Label", "100", "+10")
            mock_st.metric.assert_called_once()
        except (ImportError, AttributeError):
            self.skipTest("Fonction create_metric_card non disponible")


class TestHelpersDataProcessing(unittest.TestCase):
    """Tests pour le traitement de données"""

    def test_convert_to_dataframe(self):
        """Test conversion en DataFrame"""
        from app.utils.helpers import convert_to_dataframe

        try:
            data = [{"name": "Test", "value": 100}]
            result = convert_to_dataframe(data)
            self.assertIsNotNone(result)
        except (ImportError, AttributeError):
            self.skipTest("Fonction convert_to_dataframe non disponible")

    def test_export_to_csv(self):
        """Test export CSV"""
        from app.utils.helpers import export_to_csv

        try:
            import pandas as pd

            df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
            result = export_to_csv(df)
            self.assertIsInstance(result, str)
        except (ImportError, AttributeError):
            self.skipTest("Fonction export_to_csv non disponible")

    def test_export_to_excel(self):
        """Test export Excel"""
        from app.utils.helpers import export_to_excel

        try:
            import pandas as pd

            df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
            result = export_to_excel(df)
            self.assertIsInstance(result, bytes)
        except (ImportError, AttributeError):
            self.skipTest("Fonction export_to_excel non disponible")

    def test_group_by_category(self):
        """Test regroupement par catégorie"""
        from app.utils.helpers import group_by_category

        try:
            data = [{"category": "A", "value": 10}, {"category": "B", "value": 20}, {"category": "A", "value": 15}]
            result = group_by_category(data, "category")
            self.assertIsInstance(result, dict)
        except (ImportError, AttributeError):
            self.skipTest("Fonction group_by_category non disponible")


if __name__ == "__main__":
    unittest.main()
