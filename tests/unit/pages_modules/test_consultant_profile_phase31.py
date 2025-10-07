"""
Tests unitaires pour consultant_profile.py - Phase 31
Coverage target: 70% → 85%+ (gain estimé +15%)

Stratégie:
- Fonctions utilitaires (categorize_skill, calculate_cv_quality_score)
- Fonctions d'affichage (_display_consultant_header, _display_consultant_metrics)
- Gestion des données (_load_consultant_data, _show_consultant_not_found)
- Fonctions de tabs CV (show_cv_missions_tab, show_cv_skills_tab)

Fonctions clés à tester (~80 lignes manquantes):
- categorize_skill: catégorisation par langages/BDD/Cloud/méthodologies
- calculate_cv_quality_score: calcul score missions/compétences/contact/résumé
- _display_consultant_header, _display_consultant_metrics
- show_cv_missions_tab, show_cv_skills_tab, show_cv_summary_tab
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os
from datetime import datetime

# Ajouter le chemin du module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestCategorizeSkill(unittest.TestCase):
    """Tests pour categorize_skill"""

    def test_categorize_skill_programming_exact(self):
        """Test catégorisation langage programmation (exact)"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("python"), "💻 Langages de programmation")
        self.assertEqual(categorize_skill("Java"), "💻 Langages de programmation")
        self.assertEqual(categorize_skill("JavaScript"), "💻 Langages de programmation")

    def test_categorize_skill_programming_substring(self):
        """Test catégorisation langage programmation (substring)"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("Python 3.9"), "💻 Langages de programmation")
        self.assertEqual(categorize_skill("Java Spring"), "💻 Langages de programmation")

    def test_categorize_skill_database_exact(self):
        """Test catégorisation base de données (exact)"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("sql"), "🗄️ Bases de données")
        self.assertEqual(categorize_skill("MySQL"), "🗄️ Bases de données")
        self.assertEqual(categorize_skill("PostgreSQL"), "🗄️ Bases de données")
        self.assertEqual(categorize_skill("MongoDB"), "🗄️ Bases de données")

    def test_categorize_skill_database_substring(self):
        """Test catégorisation BDD (substring)"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("PostgreSQL Advanced"), "🗄️ Bases de données")

    def test_categorize_skill_cloud_devops_exact(self):
        """Test catégorisation Cloud & DevOps (exact)"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("aws"), "☁️ Cloud & DevOps")
        self.assertEqual(categorize_skill("Azure"), "☁️ Cloud & DevOps")
        self.assertEqual(categorize_skill("Docker"), "☁️ Cloud & DevOps")
        self.assertEqual(categorize_skill("Kubernetes"), "☁️ Cloud & DevOps")

    def test_categorize_skill_cloud_devops_substring(self):
        """Test catégorisation Cloud & DevOps (substring)"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("AWS Lambda"), "☁️ Cloud & DevOps")
        self.assertEqual(categorize_skill("DevOps Engineer"), "☁️ Cloud & DevOps")

    def test_categorize_skill_methodologies_exact(self):
        """Test catégorisation méthodologies (exact)"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("agile"), "📋 Méthodologies")
        self.assertEqual(categorize_skill("Scrum"), "📋 Méthodologies")
        self.assertEqual(categorize_skill("Kanban"), "📋 Méthodologies")

    def test_categorize_skill_methodologies_substring(self):
        """Test catégorisation méthodologies (substring)"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("Agile Coach"), "📋 Méthodologies")

    def test_categorize_skill_other(self):
        """Test catégorisation autres technologies"""
        from app.pages_modules.consultant_profile import categorize_skill

        self.assertEqual(categorize_skill("Photoshop"), "🛠️ Autres technologies")
        self.assertEqual(categorize_skill("Excel"), "🛠️ Autres technologies")
        self.assertEqual(categorize_skill("Unknown Skill"), "🛠️ Autres technologies")


class TestCalculateCVQualityScore(unittest.TestCase):
    """Tests pour calculate_cv_quality_score"""

    def test_calculate_cv_quality_score_perfect(self):
        """Test score parfait (100)"""
        from app.pages_modules.consultant_profile import calculate_cv_quality_score

        analysis = {
            "missions": [{"title": f"Mission {i}"} for i in range(5)],  # 30 points
            "competences": [f"Skill {i}" for i in range(10)],  # 30 points
            "contact": {"email": "test@test.com", "phone": "0123456789", "linkedin": "profile"},  # 20 points
            "resume": "Professional summary text",  # 20 points
        }

        score = calculate_cv_quality_score(analysis)
        self.assertEqual(score, 100)

    def test_calculate_cv_quality_score_missions_only(self):
        """Test score missions uniquement"""
        from app.pages_modules.consultant_profile import calculate_cv_quality_score

        # 5+ missions = 30 points
        analysis = {"missions": [{"title": f"Mission {i}"} for i in range(5)]}
        self.assertEqual(calculate_cv_quality_score(analysis), 30)

        # 3-4 missions = 20 points
        analysis = {"missions": [{"title": f"Mission {i}"} for i in range(3)]}
        self.assertEqual(calculate_cv_quality_score(analysis), 20)

        # 1-2 missions = 10 points
        analysis = {"missions": [{"title": "Mission 1"}]}
        self.assertEqual(calculate_cv_quality_score(analysis), 10)

    def test_calculate_cv_quality_score_competences_only(self):
        """Test score compétences uniquement"""
        from app.pages_modules.consultant_profile import calculate_cv_quality_score

        # 10+ compétences = 30 points
        analysis = {"competences": [f"Skill {i}" for i in range(10)]}
        self.assertEqual(calculate_cv_quality_score(analysis), 30)

        # 5-9 compétences = 20 points
        analysis = {"competences": [f"Skill {i}" for i in range(5)]}
        self.assertEqual(calculate_cv_quality_score(analysis), 20)

        # 1-4 compétences = 10 points
        analysis = {"competences": ["Skill 1"]}
        self.assertEqual(calculate_cv_quality_score(analysis), 10)

    def test_calculate_cv_quality_score_contact_only(self):
        """Test score contact uniquement"""
        from app.pages_modules.consultant_profile import calculate_cv_quality_score

        # 3 champs = 20 points
        analysis = {"contact": {"email": "test@test.com", "phone": "0123", "linkedin": "profile"}}
        self.assertEqual(calculate_cv_quality_score(analysis), 20)

        # 1-2 champs = 10 points
        analysis = {"contact": {"email": "test@test.com"}}
        self.assertEqual(calculate_cv_quality_score(analysis), 10)

    def test_calculate_cv_quality_score_resume_only(self):
        """Test score résumé uniquement"""
        from app.pages_modules.consultant_profile import calculate_cv_quality_score

        analysis = {"resume": "Some professional summary"}
        self.assertEqual(calculate_cv_quality_score(analysis), 20)

    def test_calculate_cv_quality_score_empty(self):
        """Test score vide (0)"""
        from app.pages_modules.consultant_profile import calculate_cv_quality_score

        analysis = {}
        self.assertEqual(calculate_cv_quality_score(analysis), 0)

    def test_calculate_cv_quality_score_partial(self):
        """Test score partiel"""
        from app.pages_modules.consultant_profile import calculate_cv_quality_score

        analysis = {
            "missions": [{"title": "Mission 1"}],  # 10 points
            "competences": ["Skill 1", "Skill 2"],  # 10 points
            "contact": {"email": "test@test.com"},  # 10 points
        }

        score = calculate_cv_quality_score(analysis)
        self.assertEqual(score, 30)

    def test_calculate_cv_quality_score_capped_at_100(self):
        """Test score plafonné à 100"""
        from app.pages_modules.consultant_profile import calculate_cv_quality_score

        # Même avec des valeurs excessives, le score reste à 100
        analysis = {
            "missions": [{"title": f"Mission {i}"} for i in range(100)],
            "competences": [f"Skill {i}" for i in range(100)],
            "contact": {"email": "test@test.com", "phone": "0123", "linkedin": "profile"},
            "resume": "Summary",
        }

        score = calculate_cv_quality_score(analysis)
        self.assertEqual(score, 100)


class TestDisplayFunctions(unittest.TestCase):
    """Tests pour les fonctions d'affichage"""

    @patch("app.pages_modules.consultant_profile.st")
    def test_display_consultant_header(self, mock_st):
        """Test affichage header consultant"""
        from app.pages_modules.consultant_profile import _display_consultant_header

        # Mock st.columns pour retourner 2 colonnes
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        consultant_data = {"prenom": "Jean", "nom": "Dupont", "practice_name": "Data"}

        _display_consultant_header(consultant_data)

        mock_st.columns.assert_called_once()
        mock_st.title.assert_called_once()

    @patch("app.pages_modules.consultant_profile.st")
    def test_display_consultant_metrics(self, mock_st):
        """Test affichage métriques consultant"""
        from app.pages_modules.consultant_profile import _display_consultant_metrics

        # Mock st.columns pour retourner 5 colonnes
        mock_cols = [MagicMock() for _ in range(5)]
        mock_st.columns.return_value = mock_cols

        consultant_data = {
            "salaire_actuel": 50000,
            "disponibilite": True,
            "date_creation": datetime(2020, 1, 1),  # Utiliser datetime au lieu de string
            "practice_name": "Data",
        }

        _display_consultant_metrics(consultant_data)

        # Vérifier que st.columns est appelé avec 5 colonnes
        mock_st.columns.assert_called_once_with(5)
        # Vérifier que st.metric est appelé (sans vérifier les colonnes contextes)
        self.assertGreater(mock_st.metric.call_count, 0)

    @patch("app.pages_modules.consultant_profile.st")
    @patch("app.pages_modules.consultant_profile.get_database_session")
    def test_show_consultant_not_found(self, mock_session, mock_st):
        """Test affichage consultant non trouvé"""
        from app.pages_modules.consultant_profile import _show_consultant_not_found

        # Mock database session
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.all.return_value = []

        _show_consultant_not_found(123)

        mock_st.error.assert_called_once()
        mock_st.warning.assert_called_once()


class TestShowCVTabs(unittest.TestCase):
    """Tests pour les fonctions de tabs CV"""

    @patch("app.pages_modules.consultant_profile.st")
    def test_show_cv_missions_tab_with_missions(self, mock_st):
        """Test affichage tab missions avec données"""
        from app.pages_modules.consultant_profile import show_cv_missions_tab

        # Mock expander
        mock_expander = MagicMock()
        mock_st.expander.return_value.__enter__.return_value = mock_expander

        missions = [
            {"titre": "Mission 1", "client": "Company A", "periode": "2020-2021"},
            {"titre": "Mission 2", "client": "Company B", "periode": "2021-2022"},
        ]

        show_cv_missions_tab(missions)

        mock_st.markdown.assert_called()
        # Vérifier que des expanders sont créés (2 missions)
        self.assertEqual(mock_st.expander.call_count, 2)

    @patch("app.pages_modules.consultant_profile.st")
    def test_show_cv_missions_tab_empty(self, mock_st):
        """Test affichage tab missions vide"""
        from app.pages_modules.consultant_profile import show_cv_missions_tab

        show_cv_missions_tab([])

        mock_st.info.assert_called_once()

    @patch("app.pages_modules.consultant_profile.st")
    @patch("app.pages_modules.consultant_profile.categorize_skill")
    def test_show_cv_skills_tab_with_skills(self, mock_categorize, mock_st):
        """Test affichage tab compétences avec données"""
        from app.pages_modules.consultant_profile import show_cv_skills_tab

        mock_categorize.return_value = "💻 Langages de programmation"

        analysis = {"competences": ["Python", "Java", "SQL"]}

        show_cv_skills_tab(analysis)

        mock_st.markdown.assert_called()
        # Vérifier que categorize_skill est appelé pour chaque compétence
        self.assertEqual(mock_categorize.call_count, 3)

    @patch("app.pages_modules.consultant_profile.st")
    def test_show_cv_skills_tab_empty(self, mock_st):
        """Test affichage tab compétences vide"""
        from app.pages_modules.consultant_profile import show_cv_skills_tab

        analysis = {"competences": []}

        show_cv_skills_tab(analysis)

        mock_st.info.assert_called_once()

    @patch("app.pages_modules.consultant_profile.st")
    @patch("app.pages_modules.consultant_profile.calculate_cv_quality_score")
    def test_show_cv_summary_tab(self, mock_score, mock_st):
        """Test affichage tab résumé"""
        from app.pages_modules.consultant_profile import show_cv_summary_tab

        mock_score.return_value = 75

        # Mock st.columns pour retourner 3 colonnes
        mock_cols = [MagicMock() for _ in range(3)]
        mock_st.columns.return_value = mock_cols

        analysis = {
            "resume": "Professional summary",
            "missions": [{"title": "Mission 1"}],
            "competences": ["Skill 1", "Skill 2"],
            "contact": {"email": "test@test.com"},
        }

        show_cv_summary_tab(analysis)

        mock_st.markdown.assert_called()
        mock_score.assert_called_once_with(analysis)
        # Vérifier affichage du score
        mock_st.metric.assert_called()

    @patch("app.pages_modules.consultant_profile.st")
    def test_show_cv_actions_tab(self, mock_st):
        """Test affichage tab actions"""
        from app.pages_modules.consultant_profile import show_cv_actions_tab

        # Mock st.columns pour retourner 2 colonnes
        mock_cols = [MagicMock() for _ in range(2)]
        mock_st.columns.return_value = mock_cols

        show_cv_actions_tab()

        mock_st.markdown.assert_called()
        # Vérifier que des boutons sont créés
        self.assertGreater(mock_st.button.call_count, 0)


class TestLoadConsultantData(unittest.TestCase):
    """Tests pour _load_consultant_data"""

    @patch("app.pages_modules.consultant_profile.get_database_session")
    def test_load_consultant_data_found(self, mock_session):
        """Test chargement consultant trouvé"""
        from app.pages_modules.consultant_profile import _load_consultant_data

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        mock_consultant = Mock(
            id=1,
            prenom="Jean",
            nom="Dupont",
            email="jean@test.com",
            telephone="0123456789",
            salaire_actuel=50000,
            disponibilite=True,
            notes="Notes",
            date_creation="2020-01-01",
            practice=Mock(nom="Data"),
        )

        mock_db.query.return_value.options.return_value.filter.return_value.first.return_value = mock_consultant

        consultant_data, _ = _load_consultant_data(1)

        self.assertIsNotNone(consultant_data)
        self.assertEqual(consultant_data["id"], 1)
        self.assertEqual(consultant_data["nom"], "Dupont")
        self.assertEqual(consultant_data["practice_name"], "Data")

    @patch("app.pages_modules.consultant_profile.get_database_session")
    def test_load_consultant_data_not_found(self, mock_session):
        """Test chargement consultant non trouvé"""
        from app.pages_modules.consultant_profile import _load_consultant_data

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        mock_db.query.return_value.options.return_value.filter.return_value.first.return_value = None

        consultant_data, _ = _load_consultant_data(999)

        self.assertIsNone(consultant_data)

    @patch("app.pages_modules.consultant_profile.get_database_session")
    def test_load_consultant_data_no_practice(self, mock_session):
        """Test chargement consultant sans practice"""
        from app.pages_modules.consultant_profile import _load_consultant_data

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        mock_consultant = Mock(
            id=2,
            prenom="Marie",
            nom="Martin",
            email="marie@test.com",
            telephone="0123",
            salaire_actuel=45000,
            disponibilite=False,
            notes="",
            date_creation="2021-01-01",
            practice=None,
        )

        mock_db.query.return_value.options.return_value.filter.return_value.first.return_value = mock_consultant

        consultant_data, _ = _load_consultant_data(2)

        self.assertIsNotNone(consultant_data)
        self.assertEqual(consultant_data["practice_name"], "Non affecté")


if __name__ == "__main__":
    unittest.main()
