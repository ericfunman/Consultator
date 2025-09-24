"""
Tests de couverture pour consultant_languages.py
Visant à améliorer la couverture de 14% vers 80%+
"""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from app.pages_modules.consultant_languages import (
    get_niveau_label, show_languages_statistics,
    show_languages_analysis, show_languages_comparison,
    _create_language_data_table, _display_language_table,
    add_language_to_consultant, update_consultant_language, delete_language,
    show_consultant_languages
)


class TestLanguageBasicFunctions:
    """Tests pour les fonctions de base des langues"""

    @patch('app.pages_modules.consultant_languages.st')
    def test_create_language_data_table(self, mock_st):
        """Test de création du tableau de données langues"""
        # Mock objets ConsultantLangue
        mock_langue1 = MagicMock()
        mock_langue1.nom = "Français"

        mock_langue2 = MagicMock()
        mock_langue2.nom = "Anglais"

        mock_cl1 = MagicMock()
        mock_cl1.id = 1
        mock_cl1.langue = mock_langue1
        mock_cl1.niveau = 5
        mock_cl1.niveau_ecrit = 5
        mock_cl1.niveau_parle = 5
        mock_cl1.certification = True
        mock_cl1.langue_maternelle = True

        mock_cl2 = MagicMock()
        mock_cl2.id = 2
        mock_cl2.langue = mock_langue2
        mock_cl2.niveau = 4
        mock_cl2.niveau_ecrit = 4
        mock_cl2.niveau_parle = 3
        mock_cl2.certification = False
        mock_cl2.langue_maternelle = False

        consultant_langues = [mock_cl1, mock_cl2]

        result = _create_language_data_table(consultant_langues)

        # Vérifier que c'est un DataFrame pandas
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ["id", "Langue", "Niveau", "Niveau écrit", "Niveau parlé", "Certification", "Langue maternelle"]

    @patch('app.pages_modules.consultant_languages.st')
    def test_display_language_table(self, mock_st):
        """Test d'affichage du tableau langues"""
        # Mock DataFrame avec les bonnes colonnes
        df = pd.DataFrame({
            "Langue": ["Français", "Anglais"],
            "Niveau": ["C1 - Autonome", "B2 - Intermédiaire avancé"],
            "Niveau écrit": ["C1 - Autonome", "B2 - Intermédiaire avancé"],
            "Niveau parlé": ["C1 - Autonome", "B1 - Intermédiaire"],
            "Certification": ["✅", "❌"],
            "Langue maternelle": ["✅", "❌"]
        })

        _display_language_table(df)

        # Vérifier que le tableau est affiché
        mock_st.dataframe.assert_called_once()


class TestLanguageUtilityFunctions:
    """Tests pour les fonctions utilitaires des langues"""

    def test_get_niveau_label_c2(self):
        """Test de conversion niveau C2"""
        result = get_niveau_label(6)
        assert result == "C2 - Maîtrise"

    def test_get_niveau_label_c1(self):
        """Test de conversion niveau C1"""
        result = get_niveau_label(5)
        assert result == "C1 - Autonome"

    def test_get_niveau_label_b2(self):
        """Test de conversion niveau B2"""
        result = get_niveau_label(4)
        assert result == "B2 - Intermédiaire avancé"

    def test_get_niveau_label_b1(self):
        """Test de conversion niveau B1"""
        result = get_niveau_label(3)
        assert result == "B1 - Intermédiaire"

    def test_get_niveau_label_a2(self):
        """Test de conversion niveau A2"""
        result = get_niveau_label(2)
        assert result == "A2 - Élémentaire"

    def test_get_niveau_label_a1(self):
        """Test de conversion niveau A1"""
        result = get_niveau_label(1)
        assert result == "A1 - Débutant"

    def test_get_niveau_label_unknown(self):
        """Test de conversion niveau inconnu"""
        result = get_niveau_label(0)
        assert result == "Niveau 0"


class TestLanguageStatistics:
    """Tests pour les statistiques des langues"""

    @patch('app.pages_modules.consultant_languages.st')
    def test_show_languages_statistics_empty(self, mock_st):
        """Test des statistiques avec liste vide"""
        show_languages_statistics([])
        # Vérifier que rien n'est affiché pour une liste vide
        mock_st.markdown.assert_not_called()

    @patch('app.pages_modules.consultant_languages.st')
    def test_show_languages_statistics_with_data(self, mock_st):
        """Test des statistiques avec données"""
        # Mock objets ConsultantLangue
        mock_cl1 = MagicMock()
        mock_cl1.niveau = 5
        mock_cl1.langue_maternelle = True
        mock_cl1.certification = True

        mock_cl2 = MagicMock()
        mock_cl2.niveau = 4
        mock_cl2.langue_maternelle = False
        mock_cl2.certification = False

        langues = [mock_cl1, mock_cl2]

        # Mock st.columns pour les métriques
        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        show_languages_statistics(langues)

        # Vérifier que les métriques sont affichées
        mock_st.metric.assert_called()


class TestLanguageAnalysis:
    """Tests pour l'analyse des langues"""

    @patch('app.pages_modules.consultant_languages.st')
    def test_show_languages_analysis_empty(self, mock_st):
        """Test d'analyse avec liste vide"""
        show_languages_analysis([])
        # Vérifier que le message d'information est affiché
        mock_st.info.assert_called_with("ℹ️ Aucune langue à analyser")

    @patch('app.pages_modules.consultant_languages.st')
    def test_show_languages_analysis_with_data(self, mock_st):
        """Test d'analyse avec données"""
        # Mock objets ConsultantLangue
        mock_langue1 = MagicMock()
        mock_langue1.nom = "Français"

        mock_langue2 = MagicMock()
        mock_langue2.nom = "Anglais"

        mock_cl1 = MagicMock()
        mock_cl1.niveau = 5
        mock_cl1.langue = mock_langue1
        mock_cl1.langue_maternelle = True
        mock_cl1.certification = True

        mock_cl2 = MagicMock()
        mock_cl2.niveau = 4
        mock_cl2.langue = mock_langue2
        mock_cl2.langue_maternelle = False
        mock_cl2.certification = False

        langues = [mock_cl1, mock_cl2]

        # Mock st.columns pour les analyses
        mock_st.columns.return_value = [MagicMock(), MagicMock()]

        show_languages_analysis(langues)

        # Vérifier que l'analyse est affichée
        mock_st.markdown.assert_any_call("### 📊 Analyse des langues")

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_show_languages_comparison(self, mock_session, mock_st):
        """Test d'affichage de la comparaison des langues"""
        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock données de comparaison
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []
        mock_session_instance.query.return_value = mock_query

        show_languages_comparison(1)

        # Vérifier que la comparaison est affichée
        mock_st.markdown.assert_called_with("### 🌍 Comparaison des niveaux de langues")


class TestLanguageDisplay:
    """Tests pour les fonctions d'affichage des langues"""

    @patch('app.pages_modules.consultant_languages._handle_form_display')
    @patch('app.pages_modules.consultant_languages._display_general_actions')
    @patch('app.pages_modules.consultant_languages.show_languages_statistics')
    @patch('app.pages_modules.consultant_languages._display_language_actions')
    @patch('app.pages_modules.consultant_languages._display_language_table')
    @patch('app.pages_modules.consultant_languages._create_language_data_table')
    @patch('app.pages_modules.consultant_languages._get_consultant_languages_data')
    @patch('app.pages_modules.consultant_languages.st')
    def test_show_consultant_languages_with_data(self, mock_st, mock_get_data, mock_create_table,
                                                mock_display_table, mock_display_actions, mock_stats,
                                                mock_general_actions, mock_handle_form):
        """Test d'affichage des langues avec données"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock données langues
        mock_langues = [MagicMock(), MagicMock()]
        mock_get_data.return_value = mock_langues

        # Mock DataFrame
        mock_df = MagicMock()
        mock_create_table.return_value = mock_df

        # Mock imports_ok
        with patch('app.pages_modules.consultant_languages.imports_ok', True):
            show_consultant_languages(mock_consultant)

        # Vérifier les appels
        mock_get_data.assert_called_once_with(1)
        mock_create_table.assert_called_once_with(mock_langues)
        mock_display_table.assert_called_once_with(mock_df)
        mock_display_actions.assert_called_once_with(mock_df)
        mock_stats.assert_called_once_with(mock_langues)
        mock_general_actions.assert_called_once_with(mock_consultant)
        mock_handle_form.assert_called_once_with(mock_consultant)

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages._get_consultant_languages_data')
    @patch('app.pages_modules.consultant_languages.show_add_language_form')
    def test_show_consultant_languages_empty(self, mock_show_form, mock_get_data, mock_st):
        """Test d'affichage des langues sans données"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock données vides
        mock_get_data.return_value = []

        # Mock imports_ok
        with patch('app.pages_modules.consultant_languages.imports_ok', True):
            show_consultant_languages(mock_consultant)

        # Vérifier que le formulaire d'ajout est appelé
        mock_show_form.assert_called_once_with(1)

    @patch('app.pages_modules.consultant_languages.st')
    def test_show_consultant_languages_no_imports(self, mock_st):
        """Test d'affichage quand les imports ont échoué"""
        mock_consultant = MagicMock()

        # Mock imports_ok à False
        with patch('app.pages_modules.consultant_languages.imports_ok', False):
            show_consultant_languages(mock_consultant)

        # Vérifier message d'erreur
        mock_st.error.assert_called_once_with("❌ Les services de base ne sont pas disponibles")

    @patch('app.pages_modules.consultant_languages.st')
    def test_show_consultant_languages_no_consultant(self, mock_st):
        """Test d'affichage sans consultant"""
        # Mock imports_ok
        with patch('app.pages_modules.consultant_languages.imports_ok', True):
            show_consultant_languages(None)

        # Vérifier message d'erreur
        mock_st.error.assert_called_once_with("❌ Consultant non fourni")

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.st.rerun')
    def test_display_language_actions(self, mock_rerun, mock_st):
        """Test d'affichage des actions par langue"""
        # Mock DataFrame
        df = pd.DataFrame({
            'id': [1, 2],
            'Langue': ['Français', 'Anglais'],
            'Niveau': ['C1', 'B2'],
            'Niveau écrit': ['C1', 'B2'],
            'Niveau parlé': ['B2', 'B1'],
            'Certification': ['✅', '❌'],
            'Langue maternelle': ['✅', '❌']
        })

        # Mock st.columns pour retourner des context managers
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = MagicMock()
        mock_col5 = MagicMock()
        mock_col6 = MagicMock()
        mock_col7 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4, mock_col5, mock_col6, mock_col7]

        from app.pages_modules.consultant_languages import _display_language_actions
        _display_language_actions(df)

        # Vérifier que les colonnes sont créées
        mock_st.columns.assert_called()

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.st.rerun')
    def test_display_general_actions(self, mock_rerun, mock_st):
        """Test d'affichage des actions générales"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = 1

        # Mock st.columns pour retourner des context managers
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        # Mock show_languages_analysis pour éviter l'appel à st.columns(2)
        with patch('app.pages_modules.consultant_languages.show_languages_analysis'):
            from app.pages_modules.consultant_languages import _display_general_actions
            _display_general_actions(mock_consultant)

        # Vérifier que les colonnes sont créées
        mock_st.columns.assert_called()


class TestLanguageForms:
    """Tests pour les formulaires d'ajout et modification des langues"""

    @patch('app.pages_modules.consultant_languages.Langue')
    @patch('app.pages_modules.consultant_languages.ConsultantLangue')
    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_show_add_language_form_success(self, mock_session, mock_st, mock_consultant_langue, mock_langue):
        """Test du formulaire d'ajout avec succès"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock langues disponibles
        mock_langue1 = MagicMock()
        mock_langue1.id = 1
        mock_langue1.nom = "Anglais"
        mock_langue2 = MagicMock()
        mock_langue2.id = 2
        mock_langue2.nom = "Espagnol"

        # Mock queries
        mock_existing_query = MagicMock()
        mock_existing_query.all.return_value = []  # Aucune langue existante
        mock_session_instance.query.return_value = mock_existing_query

        mock_available_query = MagicMock()
        mock_available_query.filter.return_value = mock_available_query
        mock_available_query.all.return_value = [mock_langue1, mock_langue2]
        mock_session_instance.query.side_effect = [mock_existing_query, mock_available_query]

        # Mock formulaire Streamlit
        mock_form = MagicMock()
        mock_st.form.return_value.__enter__.return_value = mock_form
        mock_st.selectbox.return_value = 1
        mock_st.slider.side_effect = [4, 4, 3]  # niveau_general, niveau_ecrit, niveau_parle
        mock_st.checkbox.side_effect = [True, False]  # certification, langue_maternelle
        mock_st.form_submit_button.side_effect = [True, False]  # submitted=True, cancel=False

        # Mock add_language_to_consultant
        with patch('app.pages_modules.consultant_languages.add_language_to_consultant', return_value=True):
            from app.pages_modules.consultant_languages import show_add_language_form
            show_add_language_form(1)

        # Vérifier que le formulaire est créé
        mock_st.form.assert_called()

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_show_add_language_form_no_available_languages(self, mock_session, mock_st):
        """Test du formulaire quand toutes les langues sont déjà associées"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock première query (langues existantes)
        mock_existing_cl1 = MagicMock()
        mock_existing_cl1.langue_id = 1
        mock_existing_cl2 = MagicMock()
        mock_existing_cl2.langue_id = 2

        mock_existing_query = MagicMock()
        mock_existing_query.filter.return_value = mock_existing_query
        mock_existing_query.all.return_value = [mock_existing_cl1, mock_existing_cl2]

        # Mock deuxième query (langues disponibles) - retourne vide
        mock_available_query = MagicMock()
        mock_available_query.filter.return_value = mock_available_query
        mock_available_query.all.return_value = []

        # Mock session.query pour retourner différents mocks
        mock_session_instance.query.side_effect = [mock_existing_query, mock_available_query]

        from app.pages_modules.consultant_languages import show_add_language_form
        show_add_language_form(1)

        # Vérifier message d'avertissement
        mock_st.warning.assert_called_with("⚠️ Toutes les langues existantes sont déjà associées à ce consultant")

    @patch('app.pages_modules.consultant_languages.ConsultantLangue')
    @patch('app.pages_modules.consultant_languages.Langue')
    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_show_edit_language_form_success(self, mock_session, mock_st, mock_langue, mock_consultant_langue):
        """Test du formulaire de modification avec succès"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant langue existante
        mock_cl = MagicMock()
        mock_cl.id = 1
        mock_cl.niveau = 4
        mock_cl.niveau_ecrit = 4
        mock_cl.niveau_parle = 3
        mock_cl.certification = True
        mock_cl.langue_maternelle = False
        mock_cl.langue.nom = "Anglais"

        # Mock query
        mock_query = MagicMock()
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_cl
        mock_session_instance.query.return_value = mock_query

        # Mock formulaire
        mock_form = MagicMock()
        mock_st.form.return_value.__enter__.return_value = mock_form
        mock_st.slider.side_effect = [5, 5, 4]  # nouveaux niveaux
        mock_st.checkbox.side_effect = [True, True]  # certification, langue_maternelle
        mock_st.form_submit_button.side_effect = [True, False]  # submitted=True, cancel=False

        # Mock update_consultant_language
        with patch('app.pages_modules.consultant_languages.update_consultant_language', return_value=True):
            from app.pages_modules.consultant_languages import show_edit_language_form
            show_edit_language_form(1)

        # Vérifier que le formulaire est créé
        mock_st.form.assert_called()

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_show_edit_language_form_not_found(self, mock_session, mock_st):
        """Test du formulaire de modification quand la langue n'existe pas"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query - langue non trouvée
        mock_query = MagicMock()
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_session_instance.query.return_value = mock_query

        from app.pages_modules.consultant_languages import show_edit_language_form
        show_edit_language_form(1)

        # Vérifier message d'erreur
        mock_st.error.assert_called_with("❌ Langue introuvable")

    @patch('app.pages_modules.consultant_languages.ConsultantLangue')
    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_add_language_to_consultant_success(self, mock_session, mock_st, mock_consultant_langue_class):
        """Test d'ajout réussi d'une langue"""
        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query pour vérifier doublon - doit retourner None pour .first()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Pas de doublon
        mock_session_instance.query.return_value = mock_query

        # Mock ConsultantLangue class
        mock_consultant_langue_instance = MagicMock()
        mock_consultant_langue_class.return_value = mock_consultant_langue_instance

        # Mock données complètes
        data = {
            "langue_id": 1,
            "niveau": 4,
            "niveau_ecrit": 4,
            "niveau_parle": 3,
            "certification": True,
            "langue_maternelle": False
        }

        result = add_language_to_consultant(1, data)

        assert result is True
        # Vérifier que l'ajout en base est fait
        mock_session_instance.add.assert_called_once_with(mock_consultant_langue_instance)
        mock_session_instance.commit.assert_called_once()

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_update_consultant_language_success(self, mock_session, mock_st):
        """Test de mise à jour réussie d'une langue"""
        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant langue existante
        mock_consultant_langue = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_consultant_langue
        mock_session_instance.query.return_value = mock_query

        # Mock données complètes
        data = {
            "niveau": 5,
            "niveau_ecrit": 5,
            "niveau_parle": 4,
            "certification": True,
            "langue_maternelle": True
        }

        result = update_consultant_language(1, data)

        assert result is True
        # Vérifier que la mise à jour est faite
        mock_session_instance.commit.assert_called_once()

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_delete_language_success(self, mock_session, mock_st):
        """Test de suppression réussie d'une langue"""
        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock consultant langue existante
        mock_consultant_langue = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_consultant_langue
        mock_session_instance.query.return_value = mock_query

        result = delete_language(1)

        assert result is True
        # Vérifier que la suppression est faite
        mock_session_instance.delete.assert_called_once()
        mock_session_instance.commit.assert_called_once()


class TestLanguageCRUDErrorCases:
    """Tests pour les cas d'erreur des opérations CRUD des langues"""

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_add_language_to_consultant_duplicate(self, mock_session, mock_st):
        """Test d'ajout d'une langue déjà existante"""
        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query pour vérifier doublon - retourne une langue existante
        mock_existing_langue = MagicMock()
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_existing_langue  # Doublon trouvé
        mock_session_instance.query.return_value = mock_query

        # Mock données
        data = {
            "langue_id": 1,
            "niveau": 4,
            "niveau_ecrit": 4,
            "niveau_parle": 3,
            "certification": True,
            "langue_maternelle": False
        }

        result = add_language_to_consultant(1, data)

        assert result is False
        # Vérifier que l'erreur est affichée
        mock_st.error.assert_called_with("❌ Cette langue est déjà associée au consultant")
        # Vérifier qu'aucun ajout n'est fait
        mock_session_instance.add.assert_not_called()
        mock_session_instance.commit.assert_not_called()

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_update_consultant_language_not_found(self, mock_session, mock_st):
        """Test de mise à jour d'une langue inexistante"""
        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query - langue non trouvée
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Langue non trouvée
        mock_session_instance.query.return_value = mock_query

        # Mock données
        data = {
            "niveau": 5,
            "niveau_ecrit": 5,
            "niveau_parle": 4,
            "certification": True,
            "langue_maternelle": True
        }

        result = update_consultant_language(1, data)

        assert result is False
        # Vérifier que l'erreur est affichée
        mock_st.error.assert_called_with("❌ Langue introuvable")
        # Vérifier qu'aucune mise à jour n'est faite
        mock_session_instance.commit.assert_not_called()

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_delete_language_not_found(self, mock_session, mock_st):
        """Test de suppression d'une langue inexistante"""
        # Mock session DB
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query - langue non trouvée
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Langue non trouvée
        mock_session_instance.query.return_value = mock_query

        result = delete_language(1)

        assert result is False
        # Vérifier que l'erreur est affichée
        mock_st.error.assert_called_with("❌ Langue introuvable")
        # Vérifier qu'aucune suppression n'est faite
        mock_session_instance.delete.assert_not_called()
        mock_session_instance.commit.assert_not_called()

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_add_language_to_consultant_db_error(self, mock_session, mock_st):
        """Test d'ajout avec erreur de base de données"""
        # Mock session DB qui lève une exception
        mock_session_instance = MagicMock()
        mock_session_instance.commit.side_effect = Exception("DB Error")
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query pour vérifier doublon - pas de doublon
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_session_instance.query.return_value = mock_query

        # Mock ConsultantLangue
        with patch('app.pages_modules.consultant_languages.ConsultantLangue') as mock_langue_class:
            mock_langue_instance = MagicMock()
            mock_langue_class.return_value = mock_langue_instance

            # Mock données
            data = {
                "langue_id": 1,
                "niveau": 4,
                "niveau_ecrit": 4,
                "niveau_parle": 3,
                "certification": True,
                "langue_maternelle": False
            }

            result = add_language_to_consultant(1, data)

            assert result is False
            # Vérifier que l'erreur est affichée
            mock_st.error.assert_called_with("❌ Erreur lors de l'ajout de la langue: DB Error")


class TestLanguageComparison:
    """Tests pour la comparaison des langues"""

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_show_languages_comparison_no_data(self, mock_session, mock_st):
        """Test de comparaison sans données"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock query - aucune langue
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = []
        mock_session_instance.query.return_value = mock_query

        show_languages_comparison(1)

        # Vérifier message d'information
        mock_st.info.assert_called_with("ℹ️ Pas assez de données pour effectuer une comparaison")

    @patch('app.pages_modules.consultant_languages.st')
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_show_languages_comparison_with_data(self, mock_session, mock_st):
        """Test de comparaison avec données"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock langues du consultant
        mock_langue_fr = MagicMock()
        mock_langue_fr.nom = "Français"
        mock_cl_fr = MagicMock()
        mock_cl_fr.langue = mock_langue_fr
        mock_cl_fr.niveau = 5

        mock_langue_en = MagicMock()
        mock_langue_en.nom = "Anglais"
        mock_cl_en = MagicMock()
        mock_cl_en.langue = mock_langue_en
        mock_cl_en.niveau = 4

        # Mock query consultant
        mock_consultant_query = MagicMock()
        mock_consultant_query.filter.return_value = mock_consultant_query
        mock_consultant_query.all.return_value = [mock_cl_fr, mock_cl_en]

        # Mock moyennes équipe
        mock_avg_fr = MagicMock()
        mock_avg_fr.nom = "Français"
        mock_avg_fr.avg_level = 4.5
        mock_avg_fr.count = 5

        mock_avg_en = MagicMock()
        mock_avg_en.nom = "Anglais"
        mock_avg_en.avg_level = 3.8
        mock_avg_en.count = 3

        # Mock query moyennes
        mock_avg_query = MagicMock()
        mock_avg_query.join.return_value = mock_avg_query
        mock_avg_query.group_by.return_value = mock_avg_query
        mock_avg_query.having.return_value = mock_avg_query
        mock_avg_query.all.return_value = [mock_avg_fr, mock_avg_en]

        # Mock session.query pour retourner différents résultats
        mock_session_instance.query.side_effect = [mock_consultant_query, mock_avg_query]

        # Mock st.columns pour métriques
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        # Mock pandas pour éviter l'import réel
        with patch('builtins.__import__') as mock_import:
            mock_pandas = MagicMock()
            mock_import.return_value = mock_pandas
            show_languages_comparison(1)

        # Vérifier que la fonction s'exécute sans erreur
        mock_st.markdown.assert_called_with("### 🌍 Comparaison des niveaux de langues")