"""
Tests unitaires pour consultant_cv.py - Amélioration de la couverture
Tests simplifiés pour éviter les problèmes de mocking complexes
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, List, Any


class TestConsultantCV:
    """Tests pour les fonctions de consultant_cv.py"""

    def test_categorize_skill(self):
        """Test de categorize_skill"""
        from app.pages_modules.consultant_cv import categorize_skill

        # Tests de différentes compétences
        assert categorize_skill("Python") == "🛠️ Technologies"
        assert categorize_skill("Anglais") == "🤝 Soft Skills"
        assert categorize_skill("Management") == "🤝 Soft Skills"
        assert categorize_skill("Unknown skill") == "📚 Autres"

    def test_calculate_cv_quality_score(self):
        """Test de calculate_cv_quality_score"""
        from app.pages_modules.consultant_cv import calculate_cv_quality_score

        # Test avec données complètes
        analysis = {
            "competences": ["Python", "Java", "SQL"],
            "missions": [{"titre": "Dev"}, {"titre": "Lead"}],
            "formations": ["Master"],
            "langues": ["Anglais", "Français"],
        }

        score = calculate_cv_quality_score(analysis)
        assert isinstance(score, int)
        assert 0 <= score <= 100

        # Test avec données minimales
        analysis_min = {}
        score_min = calculate_cv_quality_score(analysis_min)
        assert score_min == 0

    def test_organize_skills_by_category(self):
        """Test de _organize_skills_by_category"""
        from app.pages_modules.consultant_cv import _organize_skills_by_category

        competences = ["Python", "Anglais", "Management", "SQL", "Espagnol"]

        result = _organize_skills_by_category(competences)

        assert isinstance(result, dict)
        assert "🛠️ Technologies" in result
        assert "🤝 Soft Skills" in result
        assert "📚 Autres" in result

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_missions_empty(self, mock_st):
        """Test de show_cv_missions avec liste vide"""
        from app.pages_modules.consultant_cv import show_cv_missions

        consultant = Mock()
        consultant.id = 1

        show_cv_missions([], consultant)

        mock_st.info.assert_called_with("ℹ️ Aucune mission détectée dans le CV")

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_skills_empty_analysis(self, mock_st):
        """Test de show_cv_skills avec analyse vide"""
        from app.pages_modules.consultant_cv import show_cv_skills

        show_cv_skills({})

        mock_st.info.assert_called_with("ℹ️ Aucune compétence détectée dans le CV")

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_skills_empty_competences(self, mock_st):
        """Test de show_cv_skills avec compétences vides"""
        from app.pages_modules.consultant_cv import show_cv_skills

        analysis = {"competences": []}

        show_cv_skills(analysis)

        mock_st.info.assert_called_with("ℹ️ Aucune compétence détectée dans le CV")

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_summary_empty(self, mock_st):
        """Test de show_cv_summary avec analyse vide"""
        from app.pages_modules.consultant_cv import show_cv_summary

        show_cv_summary({})

        mock_st.info.assert_called_with("ℹ️ Analyse non disponible")

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_recommendations(self, mock_st):
        """Test de show_cv_recommendations"""
        from app.pages_modules.consultant_cv import show_cv_recommendations

        analysis = {"recommendations": ["Ajouter plus de détails techniques", "Mettre en avant les certifications"]}

        show_cv_recommendations(analysis)

        mock_st.markdown.assert_called_with("**💡 Recommandations :**")

    @patch("app.pages_modules.consultant_cv.st")
    def test_analyze_mission_details(self, mock_st):
        """Test de analyze_mission_details"""
        from app.pages_modules.consultant_cv import analyze_mission_details

        mission_data = {
            "titre": "Développeur Full Stack",
            "description": "Développement d'une application web",
            "technologies": "React, Node.js, MongoDB",
        }

        analyze_mission_details(mission_data)

        mock_st.markdown.assert_called()
        mock_st.write.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_display_skill_button(self, mock_st):
        """Test de _display_skill_button"""
        from app.pages_modules.consultant_cv import _display_skill_button

        _display_skill_button("Python", "🛠️ Technologies", 0, 1)

        mock_st.button.assert_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_cv_skills_statistics_empty(self, mock_st):
        """Test de show_cv_skills_statistics avec liste vide"""
        from app.pages_modules.consultant_cv import show_cv_skills_statistics

        show_cv_skills_statistics([])

        # Ne devrait rien faire
        mock_st.markdown.assert_not_called()

    @patch("app.pages_modules.consultant_cv.st")
    def test_copy_mission_to_clipboard(self, mock_st):
        """Test de copy_mission_to_clipboard"""
        from app.pages_modules.consultant_cv import copy_mission_to_clipboard

        mission_data = {"titre": "Test Mission", "client": "Test Client", "periode": "2023-2024"}

        copy_mission_to_clipboard(mission_data)

        # Vérifier qu'une notification est affichée
        assert mock_st.success.called or mock_st.info.called

    @patch("app.pages_modules.consultant_cv.st")
    def test_compare_cv_with_profile(self, mock_st):
        """Test de compare_cv_with_profile"""
        from app.pages_modules.consultant_cv import compare_cv_with_profile

        # Mock consultant
        consultant = Mock()
        consultant.id = 1

        analysis = {"competences": ["Python", "Java"], "missions": [{"titre": "Dev Python"}]}

        # Mock ConsultantService
        with patch("app.pages_modules.consultant_cv.ConsultantService") as mock_service:
            mock_service_instance = Mock()
            mock_service.return_value = mock_service_instance
            mock_service_instance.get_consultant_competences.return_value = ["Python", "SQL"]

            compare_cv_with_profile(analysis, consultant)

            mock_st.markdown.assert_called_with("### 🔄 Comparaison CV / Profil")

    @patch("app.pages_modules.consultant_cv.st")
    def test_show_career_suggestions(self, mock_st):
        """Test de show_career_suggestions"""
        from app.pages_modules.consultant_cv import show_career_suggestions

        analysis = {"competences": ["Python", "Java", "Management"], "experience_years": 5}

        show_career_suggestions(analysis)

        mock_st.markdown.assert_called_with("### 📈 Suggestions d'évolution")
