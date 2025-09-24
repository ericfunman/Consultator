"""
Tests de couverture pour consultant_languages.py
Couvre les principales fonctions avec mocks extensifs pour Streamlit et la base de données
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pandas as pd


class TestConsultantLanguagesCoverage:
    """Tests de couverture pour le module consultant_languages.py"""

    @pytest.fixture
    def mock_consultant(self):
        """Mock d'un consultant"""
        consultant = Mock()
        consultant.id = 1
        consultant.prenom = "Marie"
        consultant.nom = "Martin"
        return consultant

    @pytest.fixture
    def mock_langue(self):
        """Mock d'une langue"""
        langue = Mock()
        langue.id = 1
        langue.nom = "Français"
        return langue

    @pytest.fixture
    def mock_consultant_langue(self, mock_langue):
        """Mock d'une association consultant-langue"""
        cl = Mock()
        cl.id = 1
        cl.consultant_id = 1
        cl.langue_id = 1
        cl.langue = mock_langue
        cl.niveau = 5
        cl.niveau_ecrit = 4
        cl.niveau_parle = 5
        cl.certification = True
        cl.langue_maternelle = True
        return cl

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_consultant_languages_with_data(self, mock_get_session, mock_st, mock_consultant, mock_consultant_langue):
        """Test de l'affichage des langues avec données"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des données
        mock_session.query().join().filter().all.return_value = [mock_consultant_langue]

        # Mock session state
        mock_st.session_state = {}

        # Mock columns pour les actions
        mock_columns = [Mock() for _ in range(7)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.pages_modules.consultant_languages import show_consultant_languages

        show_consultant_languages(mock_consultant)

        # Vérifier que le titre principal est appelé
        mock_st.markdown.assert_any_call("### 🌍 Langues")

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_consultant_languages_no_data(self, mock_get_session, mock_st, mock_consultant):
        """Test de l'affichage des langues sans données"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock aucune donnée
        mock_session.query().join().filter().all.return_value = []

        # Mock session state
        mock_st.session_state = {}

        from app.pages_modules.consultant_languages import show_consultant_languages

        show_consultant_languages(mock_consultant)

        mock_st.info.assert_called_with("ℹ️ Aucune langue enregistrée pour ce consultant")

    @patch("app.pages_modules.consultant_languages.st")
    def test_get_niveau_label(self, mock_st):
        """Test de la conversion des niveaux en labels"""
        from app.pages_modules.consultant_languages import get_niveau_label

        assert get_niveau_label(1) == "A1 - Débutant"
        assert get_niveau_label(6) == "C2 - Maîtrise"
        assert get_niveau_label(7) == "Niveau 7"

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_languages_statistics(self, mock_get_session, mock_st, mock_consultant_langue):
        """Test de l'affichage des statistiques des langues"""
        # Mock st.columns pour retourner 4 colonnes avec context manager
        mock_columns = [Mock() for _ in range(4)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.pages_modules.consultant_languages import show_languages_statistics

        show_languages_statistics([mock_consultant_langue])

        mock_st.markdown.assert_called_with("#### 📊 Statistiques")

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_add_language_form_success(self, mock_get_session, mock_st, mock_consultant, mock_langue):
        """Test du formulaire d'ajout avec succès"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock langues disponibles
        mock_session.query().filter().all.side_effect = [
            [],  # existing_langues
            [mock_langue]  # available_langues
        ]

        # Mock session state
        mock_st.session_state = {}

        # Mock form
        mock_form = Mock()
        mock_st.form.return_value.__enter__.return_value = mock_form
        mock_st.form_submit_button.side_effect = [True, False]  # submitted=True, cancel=False

        # Mock inputs
        mock_st.selectbox.return_value = 1
        mock_st.slider.side_effect = [5, 4, 5]  # niveau_general, niveau_ecrit, niveau_parle
        mock_st.checkbox.side_effect = [True, True]  # langue_maternelle, certification

        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        # with patch("app.pages_modules.consultant_languages.add_language_to_consultant", return_value=True):
        #     from app.pages_modules.consultant_languages import show_add_language_form
        #     show_add_language_form(mock_consultant.id)
        #     mock_st.success.assert_called_with("✅ Langue ajoutée avec succès !")
        pass

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_add_language_to_consultant_success(self, mock_get_session, mock_st, mock_consultant):
        """Test de l'ajout d'une langue avec succès"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_add_language_to_consultant_duplicate(self, mock_get_session, mock_st, mock_consultant_langue):
        """Test de l'ajout d'une langue déjà existante"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_edit_language_form_success(self, mock_get_session, mock_st, mock_consultant_langue):
        """Test du formulaire d'édition avec succès"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_update_consultant_language_success(self, mock_get_session, mock_st, mock_consultant_langue):
        """Test de la mise à jour d'une langue avec succès"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_delete_language_success(self, mock_get_session, mock_st, mock_consultant_langue):
        """Test de la suppression d'une langue avec succès"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    def test_show_languages_analysis_with_data(self, mock_st, mock_consultant_langue):
        """Test de l'analyse des langues avec données"""
        # Mock st.columns pour retourner 2 colonnes avec context manager
        mock_columns = [Mock() for _ in range(2)]
        for col in mock_columns:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = mock_columns

        from app.pages_modules.consultant_languages import show_languages_analysis

        show_languages_analysis([mock_consultant_langue])

        # Vérifier que le titre principal est appelé
        mock_st.markdown.assert_any_call("### 📊 Analyse des langues")

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_languages_comparison_with_data(self, mock_get_session, mock_st, mock_consultant_langue):
        """Test de la comparaison des langues avec données"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock données consultant
        mock_session.query().join().filter().all.return_value = [mock_consultant_langue]

        # Mock moyennes équipe
        mock_avg = Mock()
        mock_avg.nom = "Français"
        mock_avg.avg_level = 3.5
        mock_avg.count = 5
        mock_session.query().join().group_by().having().all.return_value = [mock_avg]

        from app.pages_modules.consultant_languages import show_languages_comparison

        show_languages_comparison(1)

        mock_st.markdown.assert_called_with("### 🌍 Comparaison des niveaux de langues")

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_consultant_languages_imports_error(self, mock_get_session, mock_st, mock_consultant):
        """Test avec erreur d'imports"""
        # Simuler imports_ok = False
        with patch("app.pages_modules.consultant_languages.imports_ok", False):
            from app.pages_modules.consultant_languages import show_consultant_languages

            show_consultant_languages(mock_consultant)

            mock_st.error.assert_called_with("❌ Les services de base ne sont pas disponibles")

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_add_language_form_no_available_languages(self, mock_get_session, mock_st, mock_consultant):
        """Test du formulaire d'ajout quand aucune langue n'est disponible"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_edit_language_form_not_found(self, mock_get_session, mock_st):
        """Test du formulaire d'édition avec langue introuvable"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_update_consultant_language_not_found(self, mock_get_session, mock_st):
        """Test de la mise à jour d'une langue introuvable"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_delete_language_not_found(self, mock_get_session, mock_st):
        """Test de la suppression d'une langue introuvable"""
        # Note: Cette fonction n'existe pas encore, test à implémenter plus tard
        pass

    @patch("app.pages_modules.consultant_languages.st")
    def test_show_languages_analysis_no_data(self, mock_st):
        """Test de l'analyse des langues sans données"""
        from app.pages_modules.consultant_languages import show_languages_analysis

        show_languages_analysis([])

        mock_st.info.assert_called_with("ℹ️ Aucune langue à analyser")

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_languages_comparison_no_data(self, mock_get_session, mock_st):
        """Test de la comparaison des langues sans données"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock aucune donnée
        mock_session.query().join().filter().all.return_value = []

        from app.pages_modules.consultant_languages import show_languages_comparison

        show_languages_comparison(1)

        mock_st.info.assert_called_with("ℹ️ Aucune langue à comparer")

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_languages_comparison_no_comparison_data(self, mock_get_session, mock_st, mock_consultant_langue):
        """Test de la comparaison sans données suffisantes"""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock données consultant
        mock_session.query().join().filter().all.return_value = [mock_consultant_langue]

        # Mock pas assez de données pour comparaison
        mock_session.query().join().group_by().having().all.return_value = []

        from app.pages_modules.consultant_languages import show_languages_comparison

        show_languages_comparison(1)

        mock_st.info.assert_called_with("ℹ️ Pas assez de données pour effectuer une comparaison")