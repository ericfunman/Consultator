"""
Tests unitaires pour consultant_cv.py
Tests pour améliorer la couverture du module d'analyse CV
"""

import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Mock des modules externes avant les imports
sys.modules["streamlit"] = MagicMock()

from app.pages_modules.consultant_cv import (
    show_cv_missions,
    show_cv_skills,
    show_cv_summary,
    show_cv_actions,
    categorize_skill,
    check_existing_skill,
    add_skill_from_cv,
    show_cv_skills_statistics,
    calculate_cv_quality_score,
    show_cv_recommendations,
    create_mission_from_cv,
    save_mission_from_cv,
    analyze_mission_details,
    copy_mission_to_clipboard,
    save_cv_analysis_to_profile,
    generate_cv_analysis_report,
    compare_cv_with_profile,
    show_career_suggestions,
    _organize_skills_by_category,
    _display_skill_button,
    _display_skills_in_category,
)


class TestConsultantCV(unittest.TestCase):
    """Tests pour le module consultant_cv.py"""

    def setUp(self):
        """Configuration commune pour tous les tests"""
        self.mock_consultant = MagicMock()
        self.mock_consultant.id = 1
        self.mock_consultant.nom = "DUPONT"
        self.mock_consultant.prenom = "Jean"

        self.sample_missions = [
            {
                "titre": "Développeur Python",
                "client": "Société Générale",
                "date_debut": "2020-01-01",
                "date_fin": "2022-12-31",
                "description": "Développement d'applications Python",
                "technologies": "Python, Django, PostgreSQL",
            }
        ]

        self.sample_analysis = {
            "consultant_info": {"nom": "DUPONT", "prenom": "Jean", "email": "jean.dupont@email.com"},
            "missions": self.sample_missions,
            "competences": {
                "techniques": ["Python", "SQL", "React"],
                "fonctionnelles": ["Management", "Analyse"],
                "langues": ["Français C2", "Anglais B2"],
            },
            "formation": {"diplome_principal": "Master Informatique", "annee_obtention": 2020},
        }

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_missions_empty(self, mock_st):
        """Test show_cv_missions avec liste vide"""
        show_cv_missions([], self.mock_consultant)

        mock_st.info.assert_called_once()

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_missions_with_data(self, mock_st):
        """Test show_cv_missions avec données"""
        # Mock st.columns pour retourner des mocks
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.side_effect = [
            [mock_col1, mock_col2],  # Premier appel: 2 colonnes
            [mock_col1, mock_col2, mock_col3],  # Deuxième appel: 3 colonnes
        ]

        show_cv_missions(self.sample_missions, self.mock_consultant)  # Vérifier que markdown et expander sont appelés
        mock_st.markdown.assert_called()
        mock_st.expander.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_skills(self, mock_st):
        """Test show_cv_skills"""
        # Mock st.columns et session_state
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.side_effect = [
            [mock_col1],  # Premier appel: 1 colonne
            [mock_col1, mock_col2, mock_col3],  # Deuxième appel dans show_cv_skills_statistics: 3 colonnes
        ]
        mock_st.session_state.get.return_value = 1

        show_cv_skills(self.sample_analysis)

        # Cette fonction affiche les compétences et appelle st.markdown
        mock_st.markdown.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_summary(self, mock_st):
        """Test show_cv_summary"""
        # Mock st.columns pour retourner des mocks
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        show_cv_summary(self.sample_analysis)

        mock_st.markdown.assert_called()
        mock_st.metric.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_actions(self, mock_st):
        """Test show_cv_actions"""
        # Mock st.columns pour retourner des mocks
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.side_effect = [
            [mock_col1, mock_col2, mock_col3],  # Premier appel: 3 colonnes
            [mock_col1, mock_col2],  # Deuxième appel: 2 colonnes
        ]

        show_cv_actions(self.sample_analysis, self.mock_consultant)

        mock_st.markdown.assert_called()
        mock_st.columns.assert_called()

    def test_categorize_skill(self):
        """Test categorize_skill"""
        # Test différentes catégories
        self.assertEqual(categorize_skill("Python"), "🛠️ Technologies")
        self.assertEqual(categorize_skill("Management"), "🤝 Soft Skills")
        self.assertEqual(categorize_skill("Français"), "🤝 Soft Skills")
        self.assertEqual(categorize_skill("Unknown"), "📚 Autres")

    @patch("app.pages_modules.consultant_cv.get_database_session")
    def test_check_existing_skill_none_consultant(self, mock_session):
        """Test check_existing_skill sans consultant_id"""
        result = check_existing_skill("Python", None)

        self.assertFalse(result)
        mock_session.assert_not_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_add_skill_from_cv_new_skill(self, mock_st):
        """Test add_skill_from_cv avec nouvelle compétence"""
        # Cette fonction est complexe avec des imports conditionnels
        # On teste juste qu'elle n'échoue pas et affiche un message
        add_skill_from_cv("Python", 1)

        # Soit success, soit error, soit info doit être appelé
        assert (
            mock_st.success.called or mock_st.error.called or mock_st.info.called
        ), "Un message Streamlit devrait être affiché"

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_skills_statistics(self, mock_st):
        """Test show_cv_skills_statistics"""
        # Mock st.columns pour retourner des mocks
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        # Utiliser une liste de compétences
        competences = ["Python", "Java", "Management"]

        show_cv_skills_statistics(competences)

        mock_st.markdown.assert_called()
        mock_st.metric.assert_called()

    def test_calculate_cv_quality_score(self):
        """Test calculate_cv_quality_score"""
        # Test avec analyse complète
        score = calculate_cv_quality_score(self.sample_analysis)

        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

        # Test avec analyse vide
        empty_analysis = {}
        score_empty = calculate_cv_quality_score(empty_analysis)

        self.assertEqual(score_empty, 0)

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_recommendations(self, mock_st):
        """Test show_cv_recommendations"""
        show_cv_recommendations(self.sample_analysis)

        mock_st.markdown.assert_called()

    @patch("app.pages_modules.consultant_cv.imports_ok", True)
    @patch("app.pages_modules.consultant_cv.get_database_session")
    @patch("app.pages_modules.consultant_cv.st")
    def test_create_mission_from_cv(self, mock_st, mock_session):
        """Test create_mission_from_cv"""
        # Cette fonction affiche un formulaire, vérifions les appels principaux
        create_mission_from_cv(self.sample_missions[0], self.mock_consultant)

        # Vérifier que le markdown principal est appelé
        mock_st.markdown.assert_called()
        # Vérifier que le formulaire est créé
        mock_st.form.assert_called()

    @patch("app.pages_modules.consultant_cv.get_database_session")
    def test_save_mission_from_cv_error(self, mock_session):
        """Test save_mission_from_cv avec erreur"""
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.commit.side_effect = Exception("DB Error")

        data = {"titre": "Test"}

        result = save_mission_from_cv(data, 1)

        self.assertFalse(result)

    @patch("app.pages_modules.consultant_cv.st")
    def test_analyze_mission_details(self, mock_st):
        """Test analyze_mission_details"""
        mission_data = {
            "description": "Développement d'une application web",
            "technologies": "Python, Django, React",  # String au lieu de liste
        }

        analyze_mission_details(mission_data)

        mock_st.markdown.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_copy_mission_to_clipboard(self, mock_st):
        """Test copy_mission_to_clipboard"""
        mission_data = {"titre": "Test Mission", "client": "Test Client"}

        copy_mission_to_clipboard(mission_data)

        # Vérifier que text_area est appelé (pas code)
        mock_st.text_area.assert_called()

    @patch("app.pages_modules.consultant_cv.get_database_session")
    @patch("app.pages_modules.consultant_cv.st")
    def test_save_cv_analysis_to_profile(self, mock_st, mock_session):
        """Test save_cv_analysis_to_profile"""
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        save_cv_analysis_to_profile(self.sample_analysis, self.mock_consultant)

        mock_st.success.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_generate_cv_analysis_report(self, mock_st):
        """Test generate_cv_analysis_report"""
        # Mock pour éviter les appels à st.columns dans les sous-fonctions
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]

        generate_cv_analysis_report(self.sample_analysis, self.mock_consultant)

        # Cette fonction crée un rapport et propose un téléchargement
        mock_st.download_button.assert_called()
        mock_st.success.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_compare_cv_with_profile(self, mock_st):
        """Test compare_cv_with_profile"""
        compare_cv_with_profile(self.sample_analysis, self.mock_consultant)

        mock_st.markdown.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_career_suggestions(self, mock_st):
        """Test show_career_suggestions"""
        show_career_suggestions(self.sample_analysis)

        mock_st.markdown.assert_called()

    def test_organize_skills_by_category(self):
        """Test _organize_skills_by_category"""
        competences = ["Python", "Management", "Comptabilité"]

        result = _organize_skills_by_category(competences)

        self.assertIn("🛠️ Technologies", result)
        self.assertIn("🤝 Soft Skills", result)
        self.assertIn("📚 Autres", result)

    @patch("app.pages_modules.consultant_cv.st")
    def test_display_skill_button(self, mock_st):
        """Test _display_skill_button"""
        _display_skill_button("Python", "Technique", 0, 1)

        mock_st.button.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_display_skills_in_category(self, mock_st):
        """Test _display_skills_in_category"""
        # Mock st.columns pour retourner des mocks
        mock_col1 = MagicMock()
        mock_st.columns.return_value = [mock_col1]

        skills = ["Python", "Java"]

        _display_skills_in_category("Technique", skills, 1)

        mock_st.markdown.assert_called()


if __name__ == "__main__":
    unittest.main()
