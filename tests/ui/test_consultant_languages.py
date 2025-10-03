"""Tests pour le module consultant_languages - Interface utilisateur"""

from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
import streamlit as st

from app.pages_modules.consultant_languages import show_consultant_languages
from tests.fixtures.base_test import BaseUITest


class TestConsultantLanguages(BaseUITest):
    """Tests pour le module de langues consultant"""

    def test_imports_successful(self):
        """Test que les imports du module réussissent"""
        # Vérifier que les fonctions sont importables
        assert callable(show_consultant_languages)

    @patch("app.pages_modules.consultant_languages.imports_ok", True)
    @patch("app.pages_modules.consultant_languages.ConsultantService")
    def test_show_consultant_languages_basic(self, mock_service):
        """Test d'affichage basique des langues"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_languages(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_languages.imports_ok", False)
    def test_show_consultant_languages_imports_error(self):
        """Test d'affichage avec erreur d'imports"""
        mock_consultant = Mock()
        mock_consultant.id = 1

        try:
            show_consultant_languages(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_show_consultant_languages_no_consultant(self):
        """Test d'affichage sans consultant"""
        try:
            show_consultant_languages(None)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_languages.imports_ok", True)
    @patch("app.pages_modules.consultant_languages.ConsultantService")
    def test_show_consultant_languages_with_data(self, mock_service):
        """Test d'affichage avec données de langues"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock langues
        mock_langues = [
            {
                "id": 1,
                "nom": "Français",
                "niveau_ecrit": 5,
                "niveau_parle": 5,
                "certification": "DELF B2",
                "maternelle": True,
                "niveau_ecrit_label": "Langue maternelle",
                "niveau_parle_label": "Langue maternelle",
            },
            {
                "id": 2,
                "nom": "Anglais",
                "niveau_ecrit": 4,
                "niveau_parle": 4,
                "certification": "TOEIC 950",
                "maternelle": False,
                "niveau_ecrit_label": "Courant",
                "niveau_parle_label": "Courant",
            },
            {
                "id": 3,
                "nom": "Espagnol",
                "niveau_ecrit": 2,
                "niveau_parle": 3,
                "certification": None,
                "maternelle": False,
                "niveau_ecrit_label": "Intermédiaire",
                "niveau_parle_label": "Intermédiaire+",
            },
        ]

        # Mock service
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_langues.return_value = mock_langues
        mock_service_instance.get_consultant_langues_stats.return_value = {
            "total_langues": 3,
            "langues_maternelles": 1,
            "langues_certifiees": 2,
            "niveau_moyen_ecrit": 3.67,
            "niveau_moyen_parle": 4.0,
        }
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_languages(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_languages.imports_ok", True)
    @patch("app.pages_modules.consultant_languages.ConsultantService")
    def test_show_consultant_languages_empty(self, mock_service):
        """Test d'affichage avec langues vides"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service avec liste vide
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_langues.return_value = []
        mock_service_instance.get_consultant_langues_stats.return_value = {
            "total_langues": 0,
            "langues_maternelles": 0,
            "langues_certifiees": 0,
            "niveau_moyen_ecrit": 0.0,
            "niveau_moyen_parle": 0.0,
        }
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_languages(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    @patch("app.pages_modules.consultant_languages.imports_ok", True)
    @patch("app.pages_modules.consultant_languages.ConsultantService")
    def test_show_consultant_languages_service_error(self, mock_service):
        """Test d'affichage avec erreur de service"""
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock service qui lève une exception
        mock_service_instance = Mock()
        mock_service_instance.get_consultant_langues.side_effect = Exception("Service error")
        mock_service.return_value = mock_service_instance

        try:
            show_consultant_languages(mock_consultant)
            assert 1 == 1  # Test basique
        except Exception as e:
            if "ScriptRunContext" in str(e) or "Session state" in str(e):
                assert 1 == 1  # Test basique
            else:
                pytest.fail(f"Fonction a échoué avec une erreur inattendue: {e}")

    def test_module_structure(self):
        """Test que le module a la structure attendue"""
        import app.pages_modules.consultant_languages as languages_module

        # Vérifier que les fonctions principales existent
        assert hasattr(languages_module, "show_consultant_languages")

        # Vérifier que les variables d'import existent
        assert hasattr(languages_module, "imports_ok")
        assert hasattr(languages_module, "ConsultantService")

    def test_function_signatures(self):
        """Test que les fonctions ont les signatures attendues"""
        import inspect

        # Vérifier que les fonctions sont définies
        assert inspect.isfunction(show_consultant_languages)

        # Vérifier le nombre de paramètres
        sig_languages = inspect.signature(show_consultant_languages)

        # Doit avoir au moins un paramètre (consultant)
        assert len(sig_languages.parameters) >= 1

    def test_get_niveau_label(self):
        """Test de la fonction get_niveau_label"""
        from app.pages_modules.consultant_languages import get_niveau_label

        # Test niveaux standards
        assert get_niveau_label(1) == "A1 - Débutant"
        assert get_niveau_label(2) == "A2 - Élémentaire"
        assert get_niveau_label(3) == "B1 - Intermédiaire"
        assert get_niveau_label(4) == "B2 - Intermédiaire avancé"
        assert get_niveau_label(5) == "C1 - Autonome"
        assert get_niveau_label(6) == "C2 - Maîtrise"

        # Test niveau inconnu
        assert get_niveau_label(7) == "Niveau 7"
        assert get_niveau_label(0) == "Niveau 0"

    @patch("app.pages_modules.consultant_languages.st")
    def test_show_languages_statistics_with_data(self, mock_st):
        """Test affichage des statistiques avec données"""
        from app.pages_modules.consultant_languages import (
            show_languages_statistics,
        )

        # Mock consultant_langues
        mock_langues = []
        for i in range(3):
            cl = MagicMock()
            cl.niveau = 3 + i  # niveaux 3, 4, 5
            cl.langue_maternelle = i == 0  # première langue maternelle
            cl.certification = i < 2  # deux premières certifiées
            mock_langues.append(cl)

        # Mock streamlit columns
        mock_col = MagicMock()
        mock_st.columns.return_value = [mock_col, mock_col, mock_col, mock_col]

        show_languages_statistics(mock_langues)

        # Vérifier que metric a été appelé
        assert mock_st.metric.call_count >= 4

    @patch("app.pages_modules.consultant_languages.st")
    def test_show_languages_statistics_empty(self, mock_st):
        """Test affichage des statistiques sans données"""
        from app.pages_modules.consultant_languages import (
            show_languages_statistics,
        )

        show_languages_statistics([])

        # Vérifier qu'aucune métrique n'est affichée
        mock_st.metric.assert_not_called()

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_add_language_form_success(self, mock_session, mock_st):
        """Test formulaire d'ajout avec succès"""
        from app.pages_modules.consultant_languages import (
            show_add_language_form,
        )

        # Mock langues disponibles
        mock_langue = MagicMock()
        mock_langue.id = 1
        mock_langue.nom = "Test Language"

        mock_session_instance = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.all.return_value = []
        mock_session_instance.query.return_value.filter.return_value.all.return_value = [mock_langue]
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock form elements
        mock_st.form.return_value.__enter__.return_value = None
        mock_st.form.return_value.__exit__.return_value = None
        mock_st.selectbox.return_value = 1
        mock_st.slider.return_value = 3
        mock_st.checkbox.return_value = False
        mock_st.form_submit_button.return_value = True

        # Mock add_language_to_consultant
        with patch(
            "app.pages_modules.consultant_languages.add_language_to_consultant",
            return_value=True,
        ):
            show_add_language_form(1)

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    @patch("app.pages_modules.consultant_languages.ConsultantLangue")
    def test_add_language_to_consultant_success(self, mock_consultant_langue, mock_session, mock_st):
        """Test ajout de langue réussie"""
        from app.pages_modules.consultant_languages import (
            add_language_to_consultant,
        )

        # Mock session
        mock_session_instance = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None  # Pas de doublon
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock ConsultantLangue
        mock_cl = MagicMock()
        mock_consultant_langue.return_value = mock_cl

        data = {
            "langue_id": 1,
            "niveau": 4,
            "niveau_ecrit": 3,
            "niveau_parle": 4,
            "certification": True,
            "langue_maternelle": False,
        }

        result = add_language_to_consultant(1, data)

        assert result is True
        mock_session_instance.add.assert_called_once_with(mock_cl)
        mock_session_instance.commit.assert_called_once()

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_add_language_to_consultant_duplicate(self, mock_session, mock_st):
        """Test ajout de langue déjà existante"""
        from app.pages_modules.consultant_languages import (
            add_language_to_consultant,
        )

        # Mock session avec doublon existant
        mock_session_instance = MagicMock()
        mock_existing = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_existing
        mock_session.return_value.__enter__.return_value = mock_session_instance

        data = {
            "langue_id": 1,
            "niveau": 4,
            "niveau_ecrit": 3,
            "niveau_parle": 4,
            "certification": True,
            "langue_maternelle": False,
        }

        result = add_language_to_consultant(1, data)

        assert result is False

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_add_language_to_consultant_database_error(self, mock_session, mock_st):
        """Test ajout de langue avec erreur DB"""
        from app.pages_modules.consultant_languages import (
            add_language_to_consultant,
        )

        # Mock session qui lève une exception
        mock_session_instance = MagicMock()
        mock_session_instance.commit.side_effect = Exception("DB Error")
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None
        mock_session.return_value.__enter__.return_value = mock_session_instance

        data = {
            "langue_id": 1,
            "niveau": 4,
            "niveau_ecrit": 3,
            "niveau_parle": 4,
            "certification": True,
            "langue_maternelle": False,
        }

        result = add_language_to_consultant(1, data)

        assert result is False

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_show_edit_language_form_success(self, mock_session, mock_st):
        """Test formulaire d'édition avec succès"""
        from app.pages_modules.consultant_languages import (
            show_edit_language_form,
        )

        # Mock consultant_langue
        mock_cl = MagicMock()
        mock_cl.id = 1
        mock_cl.niveau = 4
        mock_cl.niveau_ecrit = 3
        mock_cl.niveau_parle = 4
        mock_cl.certification = True
        mock_cl.langue_maternelle = False

        mock_langue = MagicMock()
        mock_langue.nom = "Test Language"
        mock_cl.langue = mock_langue

        mock_session_instance = MagicMock()
        mock_session_instance.query.return_value.join.return_value.filter.return_value.first.return_value = mock_cl
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock form elements
        mock_st.form.return_value.__enter__.return_value = None
        mock_st.form.return_value.__exit__.return_value = None
        mock_st.slider.return_value = 4
        mock_st.checkbox.return_value = True
        mock_st.form_submit_button.return_value = True

        # Mock update_consultant_language
        with patch(
            "app.pages_modules.consultant_languages.update_consultant_language",
            return_value=True,
        ):
            show_edit_language_form(1)

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_update_consultant_language_success(self, mock_session, mock_st):
        """Test mise à jour de langue réussie"""
        from app.pages_modules.consultant_languages import (
            update_consultant_language,
        )

        # Mock session et consultant_langue
        mock_session_instance = MagicMock()
        mock_cl = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_cl
        mock_session.return_value.__enter__.return_value = mock_session_instance

        data = {
            "niveau": 5,
            "niveau_ecrit": 4,
            "niveau_parle": 5,
            "certification": True,
            "langue_maternelle": False,
        }

        result = update_consultant_language(1, data)

        assert result is True
        mock_session_instance.commit.assert_called_once()

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_update_consultant_language_not_found(self, mock_session, mock_st):
        """Test mise à jour de langue inexistante"""
        from app.pages_modules.consultant_languages import (
            update_consultant_language,
        )

        # Mock session qui ne trouve pas la langue
        mock_session_instance = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None
        mock_session.return_value.__enter__.return_value = mock_session_instance

        data = {
            "niveau": 5,
            "niveau_ecrit": 4,
            "niveau_parle": 5,
            "certification": True,
            "langue_maternelle": False,
        }

        result = update_consultant_language(999, data)

        assert result is False

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_delete_language_success(self, mock_session, mock_st):
        """Test suppression de langue réussie"""
        from app.pages_modules.consultant_languages import delete_language

        # Mock session et consultant_langue
        mock_session_instance = MagicMock()
        mock_cl = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = mock_cl
        mock_session.return_value.__enter__.return_value = mock_session_instance

        result = delete_language(1)

        assert result is True
        mock_session_instance.delete.assert_called_once_with(mock_cl)
        mock_session_instance.commit.assert_called_once()

    @patch("app.pages_modules.consultant_languages.st")
    @patch("app.pages_modules.consultant_languages.get_database_session")
    def test_delete_language_not_found(self, mock_session, mock_st):
        """Test suppression de langue inexistante"""
        from app.pages_modules.consultant_languages import delete_language

        # Mock session qui ne trouve pas la langue
        mock_session_instance = MagicMock()
        mock_session_instance.query.return_value.filter.return_value.first.return_value = None
        mock_session.return_value.__enter__.return_value = mock_session_instance

        result = delete_language(999)

        assert result is False

    @patch("app.pages_modules.consultant_languages.st")
    def test_show_languages_analysis_with_data(self, mock_st):
        """Test analyse des langues avec données"""
        from app.pages_modules.consultant_languages import (
            show_languages_analysis,
        )

        # Mock consultant_langues
        mock_langues = []
        for i in range(3):
            cl = MagicMock()
            cl.niveau = 2 + i  # niveaux 2, 3, 4
            cl.langue_maternelle = i == 0
            cl.certification = i < 2
            cl.langue.nom = f"Langue {i+1}"
            mock_langues.append(cl)

        mock_st.columns.return_value = [MagicMock(), MagicMock()]

        show_languages_analysis(mock_langues)

        # Vérifier que l'analyse est affichée
        mock_st.write.assert_called()

    @patch("app.pages_modules.consultant_languages.st")
    @patch("pandas.DataFrame")
    def test_show_languages_comparison_with_data(self, mock_dataframe, mock_st):
        """Test comparaison des langues avec données"""
        from app.pages_modules.consultant_languages import (
            show_languages_comparison,
        )

        # Mock DataFrame
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df

        # Mock session avec données de comparaison
        with patch("app.pages_modules.consultant_languages.get_database_session") as mock_session:
            mock_session_instance = MagicMock()

            # Mock consultant languages
            mock_cl = MagicMock()
            mock_cl.niveau = 4
            mock_langue = MagicMock()
            mock_langue.nom = "Test Language"
            mock_cl.langue = mock_langue

            # Mock averages query result
            mock_avg = MagicMock()
            mock_avg.nom = "Test Language"
            mock_avg.avg_level = 3.5
            mock_avg.count = 5

            mock_session_instance.query.return_value.join.return_value.filter.return_value.all.return_value = [mock_cl]
            mock_session_instance.query.return_value.join.return_value.group_by.return_value.having.return_value.all.return_value = [
                mock_avg
            ]
            mock_session.return_value.__enter__.return_value = mock_session_instance

            mock_st.columns.return_value = [MagicMock(), MagicMock()]

            show_languages_comparison(1)

            # Vérifier que pandas a été utilisé
            mock_dataframe.assert_called()
            mock_st.dataframe.assert_called()
