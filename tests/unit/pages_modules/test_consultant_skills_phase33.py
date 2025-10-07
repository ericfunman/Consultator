"""
Tests unitaires pour consultant_skills.py - Phase 33
Coverage target: 83% → 90%+ (gain estimé +7%)

Stratégie:
- Fonctions utilitaires (get_niveau_label, _create_skill_data_row)
- Organisation données (_organize_skills_by_category, _load_consultant_competences)
- CRUD compétences (add_skill_to_consultant, delete_skill)
- Affichage statistiques (show_skills_statistics)

Fonctions clés à tester (~55 lignes manquantes):
- get_niveau_label, _create_skill_data_row, _organize_skills_by_category
- add_skill_to_consultant, delete_skill
- show_skills_statistics, show_skills_analysis
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os
from datetime import datetime, date

# Ajouter le chemin du module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestGetNiveauLabel(unittest.TestCase):
    """Tests pour get_niveau_label"""

    def test_get_niveau_label_niveau1(self):
        """Test niveau 1 (Débutant)"""
        from app.pages_modules.consultant_skills import get_niveau_label

        result = get_niveau_label(1)

        self.assertEqual(result, "Débutant")

    def test_get_niveau_label_niveau3(self):
        """Test niveau 3 (Avancé)"""
        from app.pages_modules.consultant_skills import get_niveau_label

        result = get_niveau_label(3)

        self.assertEqual(result, "Avancé")

    def test_get_niveau_label_niveau5(self):
        """Test niveau 5 (Maître)"""
        from app.pages_modules.consultant_skills import get_niveau_label

        result = get_niveau_label(5)

        self.assertEqual(result, "Maître")

    def test_get_niveau_label_niveau_inconnu(self):
        """Test niveau inconnu"""
        from app.pages_modules.consultant_skills import get_niveau_label

        result = get_niveau_label(10)

        self.assertEqual(result, "Niveau 10")


class TestOrganizeSkillsByCategory(unittest.TestCase):
    """Tests pour _organize_skills_by_category"""

    def test_organize_skills_by_category_basic(self):
        """Test organisation basique"""
        from app.pages_modules.consultant_skills import _organize_skills_by_category

        # Mock compétences
        cc1 = Mock(
            id=1,
            competence=Mock(nom="Python", categorie="Programmation"),
            niveau=4,
            annees_experience=5,
            certification=True,
            date_acquisition=date(2020, 1, 1),
        )
        cc2 = Mock(
            id=2,
            competence=Mock(nom="Java", categorie="Programmation"),
            niveau=3,
            annees_experience=3,
            certification=False,
            date_acquisition=date(2021, 1, 1),
        )

        result = _organize_skills_by_category([cc1, cc2])

        self.assertIn("Programmation", result)
        self.assertEqual(len(result["Programmation"]), 2)
        self.assertEqual(result["Programmation"][0]["nom"], "Python")

    def test_organize_skills_by_category_empty(self):
        """Test organisation liste vide"""
        from app.pages_modules.consultant_skills import _organize_skills_by_category

        result = _organize_skills_by_category([])

        self.assertEqual(result, {})

    def test_organize_skills_by_category_multiple_categories(self):
        """Test organisation avec plusieurs catégories"""
        from app.pages_modules.consultant_skills import _organize_skills_by_category

        cc1 = Mock(
            id=1,
            competence=Mock(nom="Python", categorie="Programmation"),
            niveau=4,
            annees_experience=5,
            certification=True,
            date_acquisition=date(2020, 1, 1),
        )
        cc2 = Mock(
            id=2,
            competence=Mock(nom="SQL", categorie="Base de données"),
            niveau=3,
            annees_experience=3,
            certification=False,
            date_acquisition=date(2021, 1, 1),
        )

        result = _organize_skills_by_category([cc1, cc2])

        self.assertIn("Programmation", result)
        self.assertIn("Base de données", result)
        self.assertEqual(len(result["Programmation"]), 1)
        self.assertEqual(len(result["Base de données"]), 1)

    def test_organize_skills_by_category_no_category(self):
        """Test organisation sans catégorie (Autre)"""
        from app.pages_modules.consultant_skills import _organize_skills_by_category

        cc = Mock(
            id=1,
            competence=Mock(nom="Compétence X", categorie=None),
            niveau=2,
            annees_experience=1,
            certification=False,
            date_acquisition=date(2022, 1, 1),
        )

        result = _organize_skills_by_category([cc])

        self.assertIn("Autre", result)
        self.assertEqual(len(result["Autre"]), 1)


class TestCreateSkillDataRow(unittest.TestCase):
    """Tests pour _create_skill_data_row"""

    def test_create_skill_data_row_complete(self):
        """Test création ligne complète"""
        from app.pages_modules.consultant_skills import _create_skill_data_row

        skill = {
            "id": 1,
            "nom": "Python",
            "niveau": 4,
            "annees_experience": 5,
            "certification": True,
            "date_acquisition": date(2020, 1, 1),
        }

        result = _create_skill_data_row(skill)

        self.assertEqual(result["Compétence"], "Python")
        self.assertEqual(result["Niveau"], "Expert")
        self.assertEqual(result["Expérience"], "5 an(s)")
        self.assertEqual(result["Certification"], "✅")
        self.assertEqual(result["Actions"], "edit_1")

    def test_create_skill_data_row_minimal(self):
        """Test création ligne minimale"""
        from app.pages_modules.consultant_skills import _create_skill_data_row

        skill = {
            "id": 2,
            "nom": "Java",
            "niveau": 2,
            "annees_experience": None,
            "certification": False,
            "date_acquisition": None,
        }

        result = _create_skill_data_row(skill)

        self.assertEqual(result["Compétence"], "Java")
        self.assertEqual(result["Niveau"], "Intermédiaire")
        self.assertEqual(result["Expérience"], "N/A")
        self.assertEqual(result["Certification"], "❌")


class TestAddSkillToConsultant(unittest.TestCase):
    """Tests pour add_skill_to_consultant"""

    @patch("app.pages_modules.consultant_skills.ConsultantCompetence")
    @patch("app.pages_modules.consultant_skills.get_database_session")
    @patch("app.pages_modules.consultant_skills.st")
    def test_add_skill_to_consultant_success(self, mock_st, mock_get_session, mock_cc_class):
        """Test ajout compétence réussi"""
        from app.pages_modules.consultant_skills import add_skill_to_consultant

        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        # Mock ConsultantCompetence instance
        mock_cc_instance = Mock()
        mock_cc_class.return_value = mock_cc_instance

        data = {
            "competence_id": 1,
            "niveau": 4,
            "annees_experience": 5,
            "certification": True,
        }

        result = add_skill_to_consultant(1, data)

        self.assertTrue(result)
        mock_session.add.assert_called_once_with(mock_cc_instance)
        mock_session.commit.assert_called_once()

    @patch("app.pages_modules.consultant_skills.get_database_session")
    @patch("app.pages_modules.consultant_skills.st")
    def test_add_skill_to_consultant_already_exists(self, mock_st, mock_get_session):
        """Test ajout compétence déjà existante"""
        from app.pages_modules.consultant_skills import add_skill_to_consultant

        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        # Simuler une compétence existante
        mock_session.query.return_value.filter.return_value.first.return_value = Mock()

        data = {
            "competence_id": 1,
            "niveau": 4,
            "annees_experience": 5,
            "certification": True,
        }

        result = add_skill_to_consultant(1, data)

        self.assertFalse(result)
        mock_st.error.assert_called_once()

    @patch("app.pages_modules.consultant_skills.get_database_session")
    @patch("app.pages_modules.consultant_skills.st")
    def test_add_skill_to_consultant_exception(self, mock_st, mock_get_session):
        """Test ajout compétence avec exception"""
        from app.pages_modules.consultant_skills import add_skill_to_consultant

        mock_get_session.side_effect = Exception("Database error")

        data = {
            "competence_id": 1,
            "niveau": 4,
            "annees_experience": 5,
            "certification": True,
        }

        result = add_skill_to_consultant(1, data)

        self.assertFalse(result)
        mock_st.error.assert_called()


class TestDeleteSkill(unittest.TestCase):
    """Tests pour delete_skill"""

    @patch("app.pages_modules.consultant_skills.get_database_session")
    @patch("app.pages_modules.consultant_skills.st")
    def test_delete_skill_success(self, mock_st, mock_get_session):
        """Test suppression compétence réussie"""
        from app.pages_modules.consultant_skills import delete_skill

        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_cc = Mock(id=1)
        mock_session.query.return_value.filter.return_value.first.return_value = mock_cc

        result = delete_skill(1)

        self.assertTrue(result)
        mock_session.delete.assert_called_once_with(mock_cc)
        mock_session.commit.assert_called_once()

    @patch("app.pages_modules.consultant_skills.get_database_session")
    @patch("app.pages_modules.consultant_skills.st")
    def test_delete_skill_not_found(self, mock_st, mock_get_session):
        """Test suppression compétence inexistante"""
        from app.pages_modules.consultant_skills import delete_skill

        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = delete_skill(999)

        self.assertFalse(result)
        mock_st.error.assert_called()

    @patch("app.pages_modules.consultant_skills.get_database_session")
    @patch("app.pages_modules.consultant_skills.st")
    def test_delete_skill_exception(self, mock_st, mock_get_session):
        """Test suppression compétence avec exception"""
        from app.pages_modules.consultant_skills import delete_skill

        mock_get_session.side_effect = Exception("Database error")

        result = delete_skill(1)

        self.assertFalse(result)
        mock_st.error.assert_called()


class TestShowSkillsStatistics(unittest.TestCase):
    """Tests pour show_skills_statistics"""

    @patch("app.pages_modules.consultant_skills.st")
    def test_show_skills_statistics_basic(self, mock_st):
        """Test affichage statistiques basiques"""
        from app.pages_modules.consultant_skills import show_skills_statistics

        cc1 = Mock(niveau=4, certification=True, annees_experience=5)
        cc2 = Mock(niveau=3, certification=False, annees_experience=3)
        cc3 = Mock(niveau=5, certification=True, annees_experience=7)

        # Mock st.columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4]

        show_skills_statistics([cc1, cc2, cc3])

        # Vérifie que st.columns a été appelé
        mock_st.columns.assert_called()

    @patch("app.pages_modules.consultant_skills.st")
    def test_show_skills_statistics_empty(self, mock_st):
        """Test affichage statistiques avec liste vide"""
        from app.pages_modules.consultant_skills import show_skills_statistics

        # Liste vide, la fonction retourne directement sans appeler st.columns
        show_skills_statistics([])

        # Vérifie que st.columns n'a PAS été appelé (fonction return early)
        mock_st.columns.assert_not_called()


if __name__ == "__main__":
    unittest.main()
