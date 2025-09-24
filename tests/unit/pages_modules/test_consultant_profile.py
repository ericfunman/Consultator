"""
Tests de couverture pour consultant_profile.py
Visant à améliorer la couverture de 12% vers 80%+
"""

import pytest
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime, date
import json

from app.pages_modules.consultant_profile import (
    show, _load_consultant_data, _show_consultant_not_found,
    _display_consultant_header, _display_consultant_metrics,
    _display_consultant_tabs, show_consultant_profile,
    show_cv_analysis_fullwidth, show_cv_missions_tab,
    show_cv_skills_tab, show_cv_summary_tab, show_cv_actions_tab,
    categorize_skill, calculate_cv_quality_score
)


class TestConsultantProfileBasic:
    """Tests de base pour les fonctions principales de consultant_profile.py"""

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_basic_display(self, mock_st):
        """Test de la fonction show() - affichage basique"""
        # Mock session_state pour éviter l'affichage du profil
        mock_st.session_state = MagicMock()
        mock_st.session_state.get.return_value = None

        # Mock st.tabs pour retourner 2 onglets
        mock_tab1, mock_tab2 = MagicMock(), MagicMock()
        mock_st.tabs.return_value = [mock_tab1, mock_tab2]

        show()

        # Vérifier que le titre est affiché
        mock_st.title.assert_called_with("👥 Gestion des consultants")
        mock_st.markdown.assert_called_with("### Gérez les profils de vos consultants")

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_with_profile_view(self, mock_st):
        """Test de show() avec affichage de profil"""
        # Mock session_state avec __contains__ pour supporter 'in' operator
        mock_session_state = MagicMock()
        mock_session_state.__contains__ = lambda self, key: key == "view_consultant_profile"
        mock_session_state.view_consultant_profile = 1
        mock_st.session_state = mock_session_state

        with patch('app.pages_modules.consultant_profile.show_consultant_profile') as mock_show_profile:
            show()

            # Vérifier que show_consultant_profile est appelée
            mock_show_profile.assert_called_once()

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_imports_not_ok(self, mock_st):
        """Test de show() quand les imports échouent"""
        with patch('app.pages_modules.consultant_profile.imports_ok', False):
            show()

            # Vérifier que l'erreur est affichée
            mock_st.error.assert_called_with("❌ Les services de base ne sont pas disponibles")
            mock_st.info.assert_called_with("Vérifiez que tous les modules sont correctement installés")

    @patch('app.pages_modules.consultant_profile.st')
    @patch('app.pages_modules.consultant_profile.get_database_session')
    def test_load_consultant_data_success(self, mock_session, mock_st):
        """Test de chargement réussi des données consultant"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.telephone = "0123456789"
        mock_consultant.salaire_actuel = 50000
        mock_consultant.disponibilite = True
        mock_consultant.notes = "Test notes"
        mock_consultant.date_creation = datetime(2024, 1, 1)
        mock_consultant.practice = MagicMock()
        mock_consultant.practice.nom = "Test Practice"

        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_consultant
        mock_session_instance.query.return_value = mock_query

        result_data, result_session = _load_consultant_data(1)

        assert result_data is not None
        assert result_data["prenom"] == "Jean"
        assert result_data["nom"] == "Dupont"
        assert result_session == mock_session_instance

    @patch('app.pages_modules.consultant_profile.st')
    @patch('app.pages_modules.consultant_profile.get_database_session')
    def test_load_consultant_data_not_found(self, mock_session, mock_st):
        """Test de chargement de consultant non trouvé"""
        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query qui retourne None
        mock_query = MagicMock()
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_session_instance.query.return_value = mock_query

        result_data, result_session = _load_consultant_data(999)

        assert result_data is None
        assert result_session is None

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_consultant_not_found(self, mock_st):
        """Test d'affichage d'erreur consultant non trouvé"""
        _show_consultant_not_found(999)

        # Vérifier que l'erreur est affichée
        mock_st.error.assert_called_with("❌ Consultant introuvable (ID: 999)")
        mock_st.warning.assert_called_with("💡 Vérifiez que l'ID est correct et que le consultant existe dans la base de données")

    @patch('app.pages_modules.consultant_profile.st')
    def test_display_consultant_header(self, mock_st):
        """Test d'affichage de l'en-tête consultant"""
        # Mock données consultant
        consultant_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean@test.com",
            "telephone": "0123456789",
            "date_creation": datetime(2024, 1, 1)
        }

        # Mock st.columns pour retourner 2 colonnes
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        _display_consultant_header(consultant_data)

        # Vérifier que le titre est affiché
        mock_st.title.assert_called_with("👤 Profil de Jean Dupont")

    @patch('app.pages_modules.consultant_profile.st')
    @patch('app.pages_modules.consultant_profile.get_database_session')
    def test_display_consultant_metrics(self, mock_session, mock_st):
        """Test d'affichage des métriques consultant"""
        # Mock données consultant
        consultant_data = {
            "id": 1,
            "salaire_actuel": 50000,
            "disponibilite": True,
            "date_creation": datetime(2024, 1, 1),
            "practice_name": "Test Practice"
        }

        # Mock st.columns pour retourner 5 colonnes
        mock_st.columns.return_value = [MagicMock() for _ in range(5)]

        _display_consultant_metrics(consultant_data)

        # Vérifier que les métriques sont affichées
        mock_st.metric.assert_called()

    @patch('app.pages_modules.consultant_profile.st')
    def test_display_consultant_tabs(self, mock_st):
        """Test d'affichage des onglets consultant"""
        # Mock st.tabs pour retourner 5 onglets
        mock_tabs = [MagicMock() for _ in range(5)]
        mock_st.tabs.return_value = mock_tabs

        _display_consultant_tabs(1)

        # Vérifier que les onglets sont créés
        mock_st.tabs.assert_called_once()
        args, _ = mock_st.tabs.call_args
        assert len(args[0]) == 5  # 5 onglets
        assert "📋 Informations" in args[0]
        assert "💼 Compétences" in args[0]
        assert "🌍 Langues" in args[0]
        assert "� Missions" in args[0]
        assert "� Documents" in args[0]

    @patch('app.pages_modules.consultant_profile.st')
    @patch('app.pages_modules.consultant_profile._load_consultant_data')
    @patch('app.pages_modules.consultant_profile._show_consultant_not_found')
    def test_show_consultant_profile_not_found(self, mock_show_not_found, mock_load_data, mock_st):
        """Test d'affichage de profil consultant non trouvé"""
        # Mock session_state
        mock_st.session_state = MagicMock()
        mock_st.session_state.view_consultant_profile = 999

        # Mock chargement qui retourne None
        mock_load_data.return_value = (None, None)

        show_consultant_profile()

        # Vérifier que la fonction d'erreur est appelée
        mock_show_not_found.assert_called_with(999)

    @patch('app.pages_modules.consultant_profile.st')
    @patch('app.pages_modules.consultant_profile._load_consultant_data')
    @patch('app.pages_modules.consultant_profile._display_consultant_header')
    @patch('app.pages_modules.consultant_profile._display_consultant_metrics')
    @patch('app.pages_modules.consultant_profile._display_consultant_tabs')
    def test_show_consultant_profile_success(self, mock_display_tabs, mock_display_metrics,
                                           mock_display_header, mock_load_data, mock_st):
        """Test d'affichage réussi du profil consultant"""
        # Mock session_state
        mock_st.session_state = MagicMock()
        mock_st.session_state.view_consultant_profile = 1

        # Mock consultant data
        mock_consultant_data = {
            "id": 1,
            "prenom": "Jean",
            "nom": "Dupont"
        }
        mock_load_data.return_value = (mock_consultant_data, MagicMock())

        show_consultant_profile()

        # Vérifier que les fonctions d'affichage sont appelées
        mock_display_header.assert_called_with(mock_consultant_data)
        mock_display_metrics.assert_called_with(mock_consultant_data)
        mock_display_tabs.assert_called_with(1)


class TestCVAnalysisFunctions:
    """Tests pour les fonctions d'analyse CV"""

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_cv_analysis_fullwidth_no_analysis(self, mock_st):
        """Test d'analyse CV sans données"""
        # Mock session_state
        mock_st.session_state = MagicMock()
        mock_st.session_state.get.return_value = None

        show_cv_analysis_fullwidth()

        # Vérifier que rien n'est affiché quand il n'y a pas d'analyse
        mock_st.markdown.assert_not_called()

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_cv_analysis_fullwidth_with_analysis(self, mock_st):
        """Test d'analyse CV avec données"""
        # Mock session_state
        mock_st.session_state = MagicMock()
        mock_st.session_state.cv_analysis = {
            "analysis": {"missions": [], "competences": []},
            "consultant": MagicMock(),
            "file_name": "test_cv.pdf"
        }

        # Mock st.tabs pour les onglets d'analyse
        mock_tabs = [MagicMock() for _ in range(4)]
        mock_st.tabs.return_value = mock_tabs

        # Mock st.columns pour l'en-tête
        mock_st.columns.return_value = [MagicMock() for _ in range(3)]

        show_cv_analysis_fullwidth()

        # Vérifier que les onglets sont créés
        mock_st.tabs.assert_called_once()

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_cv_missions_tab(self, mock_st):
        """Test d'affichage de l'onglet missions CV"""
        missions = [
            {"titre": "Développeur Senior", "client": "Tech Corp", "periode": "2020-2023"},
            {"titre": "Chef de projet", "client": "Consult Corp", "periode": "2018-2020"}
        ]

        show_cv_missions_tab(missions)

        # Vérifier que les missions sont affichées
        mock_st.markdown.assert_called_with("### � Missions détectées")

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_cv_skills_tab(self, mock_st):
        """Test d'affichage de l'onglet compétences CV"""
        analysis = {
            "competences": ["Python", "Java", "SQL", "React", "Docker"]
        }

        show_cv_skills_tab(analysis)

        # Vérifier que les compétences sont affichées
        mock_st.markdown.assert_called_with("### 🛠️ Compétences détectées")

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_cv_summary_tab(self, mock_st):
        """Test d'affichage de l'onglet résumé CV"""
        analysis = {
            "missions": [{"title": "Dev", "company": "Test"}, {"title": "PM", "company": "Test2"}],
            "competences": ["Python", "Java"],
            "contact": {"email": "test@test.com", "phone": "0123456789"},
            "resume": "Test resume"
        }

        # Mock st.columns pour retourner 3 colonnes
        mock_st.columns.return_value = [MagicMock() for _ in range(3)]

        show_cv_summary_tab(analysis)

        # Vérifier que le résumé est affiché
        mock_st.markdown.assert_called_with("### � Résumé de l'analyse")
        mock_st.metric.assert_called()

    @patch('app.pages_modules.consultant_profile.st')
    def test_show_cv_actions_tab(self, mock_st):
        """Test d'affichage de l'onglet actions CV"""
        # Mock st.columns pour retourner 2 colonnes
        mock_st.columns.return_value = [MagicMock() for _ in range(2)]

        show_cv_actions_tab()

        # Vérifier que les actions sont affichées
        mock_st.markdown.assert_called_with("### 💾 Actions disponibles")


class TestUtilityFunctions:
    """Tests pour les fonctions utilitaires"""

    def test_categorize_skill_technical(self):
        """Test de catégorisation compétence technique"""
        result = categorize_skill("Python")
        assert result == "💻 Langages de programmation"

    def test_categorize_skill_database(self):
        """Test de catégorisation compétence base de données"""
        result = categorize_skill("MySQL")
        assert result == "🗄️ Bases de données"

    def test_categorize_skill_cloud(self):
        """Test de catégorisation compétence cloud"""
        result = categorize_skill("AWS")
        assert result == "☁️ Cloud & DevOps"

    def test_categorize_skill_unknown(self):
        """Test de catégorisation compétence inconnue"""
        result = categorize_skill("Compétence inconnue")
        assert result == "🛠️ Autres technologies"

    def test_calculate_cv_quality_score_perfect(self):
        """Test de calcul du score qualité CV parfait"""
        analysis = {
            "missions": [{"title": "Dev"}, {"title": "PM"}, {"title": "Lead"}, {"title": "Arch"}, {"title": "CTO"}],  # 5 missions = 30 points
            "competences": ["Python", "Java", "SQL", "React", "Docker", "Kubernetes", "AWS", "Terraform", "Jenkins", "Git"],  # 10 compétences = 30 points
            "contact": {"email": "test@test.com", "phone": "0123456789", "linkedin": "linkedin.com/in/test"},  # contact complet = 20 points
            "resume": "Test resume"  # résumé = 20 points
        }

        score = calculate_cv_quality_score(analysis)

        assert score == 100  # Score parfait

    def test_calculate_cv_quality_score_minimal(self):
        """Test de calcul du score qualité CV minimal"""
        analysis = {
            "missions": [],  # 0 missions = 0 points
            "competences": [],  # 0 compétences = 0 points
            "contact": {},  # contact vide = 0 points
            # pas de resume = 0 points
        }

        score = calculate_cv_quality_score(analysis)

        assert score == 0  # Score nul

    def test_calculate_cv_quality_score_medium(self):
        """Test de calcul du score qualité CV moyen"""
        analysis = {
            "missions": [{"title": "Dev"}, {"title": "PM"}],  # 2 missions = 10 points
            "competences": ["Python", "Java", "SQL"],  # 3 compétences = 10 points
            "contact": {"email": "test@test.com"},  # contact partiel = 10 points
            # pas de resume = 0 points
        }

        score = calculate_cv_quality_score(analysis)

        assert score == 30  # Score moyen