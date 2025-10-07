"""
Tests unitaires pour consultant_list.py - Phase 32
Coverage target: 85% → 92%+ (gain estimé +7%)

Stratégie:
- Fonctions de conversion et formatage de données
- Logique de filtrage (recherche, practice, entité, disponibilité)
- Affichage de statistiques
- Export et génération de rapports

Fonctions clés à tester (~36 lignes manquantes):
- _convert_consultants_to_dataframe, _apply_filters
- _display_statistics, _get_display_columns, _create_column_config
- export_to_excel, generate_consultants_report
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import pandas as pd
from datetime import date, datetime
import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestConvertConsultantsToDataframe(unittest.TestCase):
    """Tests pour _convert_consultants_to_dataframe"""

    def test_convert_consultants_to_dataframe_full(self):
        """Test conversion consultants complets"""
        from app.pages_modules.consultant_list import _convert_consultants_to_dataframe

        practice = Mock(nom="Data")
        consultant = Mock(
            id=1,
            prenom="Jean",
            nom="Dupont",
            email="jean@test.com",
            telephone="0123456789",
            salaire_actuel=50000,
            disponibilite=True,
            date_disponibilite=date(2024, 1, 1),
            grade="Senior",
            type_contrat="CDI",
            practice=practice,
            entite="Paris",
            date_creation=datetime(2020, 1, 1),
        )

        result = _convert_consultants_to_dataframe([consultant])

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["Prénom"], "Jean")
        self.assertEqual(result.iloc[0]["Practice"], "Data")

    def test_convert_consultants_to_dataframe_minimal(self):
        """Test conversion consultants minimaux"""
        from app.pages_modules.consultant_list import _convert_consultants_to_dataframe

        consultant = Mock(
            id=2,
            prenom="Marie",
            nom="Martin",
            email="marie@test.com",
            telephone=None,
            salaire_actuel=None,
            disponibilite=False,
            date_disponibilite=None,
            grade=None,
            type_contrat=None,
            practice=None,
            entite=None,
            date_creation=None,
        )

        result = _convert_consultants_to_dataframe([consultant])

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["Salaire annuel"], 0)
        self.assertEqual(result.iloc[0]["Practice"], "Non affecté")
        self.assertEqual(result.iloc[0]["Entité"], "N/A")

    def test_convert_consultants_to_dataframe_empty(self):
        """Test conversion liste vide"""
        from app.pages_modules.consultant_list import _convert_consultants_to_dataframe

        result = _convert_consultants_to_dataframe([])

        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 0)


class TestApplyFilters(unittest.TestCase):
    """Tests pour _apply_filters"""

    def setUp(self):
        """Setup DataFrame de test"""
        self.df = pd.DataFrame(
            {
                "ID": [1, 2, 3],
                "Prénom": ["Jean", "Marie", "Paul"],
                "Nom": ["Dupont", "Martin", "Bernard"],
                "Email": ["jean@test.com", "marie@test.com", "paul@test.com"],
                "Practice": ["Data", "Quant", "Data"],
                "Entité": ["Paris", "Lyon", "Paris"],
                "Disponibilité": ["✅ Disponible", "🔴 En mission", "✅ Disponible"],
            }
        )

    def test_apply_filters_search_term(self):
        """Test filtre par terme de recherche"""
        from app.pages_modules.consultant_list import _apply_filters

        result = _apply_filters(self.df, "Jean", "Tous", "Tous", "Tous")

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["Prénom"], "Jean")

    def test_apply_filters_practice(self):
        """Test filtre par practice"""
        from app.pages_modules.consultant_list import _apply_filters

        result = _apply_filters(self.df, "", "Data", "Tous", "Tous")

        self.assertEqual(len(result), 2)
        self.assertTrue(all(result["Practice"] == "Data"))

    def test_apply_filters_entite(self):
        """Test filtre par entité"""
        from app.pages_modules.consultant_list import _apply_filters

        result = _apply_filters(self.df, "", "Tous", "Paris", "Tous")

        self.assertEqual(len(result), 2)
        self.assertTrue(all(result["Entité"] == "Paris"))

    def test_apply_filters_availability(self):
        """Test filtre par disponibilité"""
        from app.pages_modules.consultant_list import _apply_filters

        result = _apply_filters(self.df, "", "Tous", "Tous", "Disponible")

        self.assertEqual(len(result), 2)
        self.assertTrue(all(result["Disponibilité"] == "✅ Disponible"))

    def test_apply_filters_combined(self):
        """Test filtres combinés"""
        from app.pages_modules.consultant_list import _apply_filters

        result = _apply_filters(self.df, "Jean", "Data", "Paris", "Disponible")

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["Prénom"], "Jean")

    def test_apply_filters_no_results(self):
        """Test filtres sans résultats"""
        from app.pages_modules.consultant_list import _apply_filters

        result = _apply_filters(self.df, "NonExistant", "Tous", "Tous", "Tous")

        self.assertEqual(len(result), 0)

    def test_apply_filters_tous(self):
        """Test filtre 'Tous' (aucun filtre)"""
        from app.pages_modules.consultant_list import _apply_filters

        result = _apply_filters(self.df, "", "Tous", "Tous", "Tous")

        self.assertEqual(len(result), 3)


class TestGetDisplayColumns(unittest.TestCase):
    """Tests pour _get_display_columns"""

    def test_get_display_columns_returns_list(self):
        """Test retour liste de colonnes"""
        from app.pages_modules.consultant_list import _get_display_columns

        result = _get_display_columns()

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_get_display_columns_contains_key_columns(self):
        """Test présence colonnes clés"""
        from app.pages_modules.consultant_list import _get_display_columns

        result = _get_display_columns()

        self.assertIn("Prénom", result)
        self.assertIn("Nom", result)
        self.assertIn("Email", result)


class TestCreateColumnConfig(unittest.TestCase):
    """Tests pour _create_column_config"""

    def test_create_column_config_returns_dict(self):
        """Test retour dictionnaire"""
        from app.pages_modules.consultant_list import _create_column_config

        result = _create_column_config()

        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)

    def test_create_column_config_contains_key_columns(self):
        """Test présence configuration colonnes clés"""
        from app.pages_modules.consultant_list import _create_column_config

        result = _create_column_config()

        self.assertIn("Prénom", result)
        self.assertIn("Nom", result)


class TestDisplayStatistics(unittest.TestCase):
    """Tests pour _display_statistics"""

    @patch("app.pages_modules.consultant_list.st")
    def test_display_statistics_basic(self, mock_st):
        """Test affichage statistiques basique"""
        from app.pages_modules.consultant_list import _display_statistics

        df = pd.DataFrame(
            {
                "Disponibilité": ["✅ Disponible", "🔴 En mission", "✅ Disponible"],
                "Salaire annuel": [50000, 60000, 70000],
            }
        )

        # Mock st.columns pour retourner des contextes mockés
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4]

        _display_statistics(df)

        # Vérifie que st.metric a été appelé 4 fois (une par colonne)
        self.assertEqual(mock_st.metric.call_count, 4)

    @patch("app.pages_modules.consultant_list.st")
    def test_display_statistics_empty(self, mock_st):
        """Test affichage statistiques avec DataFrame vide"""
        from app.pages_modules.consultant_list import _display_statistics

        df = pd.DataFrame({"Disponibilité": [], "Salaire annuel": []})

        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4]

        _display_statistics(df)

        mock_st.metric.assert_called()


class TestExportToExcel(unittest.TestCase):
    """Tests pour export_to_excel"""

    @patch("app.pages_modules.consultant_list.st")
    def test_export_to_excel_basic(self, mock_st):
        """Test export Excel basique"""
        from app.pages_modules.consultant_list import export_to_excel

        df = pd.DataFrame(
            {
                "Prénom": ["Jean", "Marie"],
                "Nom": ["Dupont", "Martin"],
                "Email": ["jean@test.com", "marie@test.com"],
            }
        )

        export_to_excel(df)

        # Vérifie que st.download_button a été appelé
        mock_st.download_button.assert_called_once()

    @patch("app.pages_modules.consultant_list.st")
    def test_export_to_excel_empty(self, mock_st):
        """Test export Excel DataFrame vide"""
        from app.pages_modules.consultant_list import export_to_excel

        df = pd.DataFrame()

        export_to_excel(df)

        # Devrait quand même appeler download_button
        mock_st.download_button.assert_called_once()


class TestGenerateConsultantsReport(unittest.TestCase):
    """Tests pour generate_consultants_report"""

    @patch("app.pages_modules.consultant_list.st")
    def test_generate_consultants_report_basic(self, mock_st):
        """Test génération rapport basique"""
        from app.pages_modules.consultant_list import generate_consultants_report

        df = pd.DataFrame(
            {
                "Prénom": ["Jean", "Marie"],
                "Nom": ["Dupont", "Martin"],
                "Practice": ["Data", "Quant"],
                "Disponibilité": ["✅ Disponible", "🔴 En mission"],
                "Salaire annuel": [50000, 60000],
            }
        )

        # Mock st.columns pour retourner des contextes mockés
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        generate_consultants_report(df)

        # Vérifie que st.markdown a été appelé (pour le titre)
        mock_st.markdown.assert_called()
        # Vérifie que st.columns a été appelé
        mock_st.columns.assert_called()

    @patch("app.pages_modules.consultant_list.st")
    def test_generate_consultants_report_empty(self, mock_st):
        """Test génération rapport avec DataFrame vide"""
        from app.pages_modules.consultant_list import generate_consultants_report

        df = pd.DataFrame(
            {
                "Prénom": [],
                "Nom": [],
                "Practice": [],
                "Disponibilité": [],
                "Salaire annuel": [],
            }
        )

        generate_consultants_report(df)

        # Devrait gérer le cas vide (probablement avec une erreur)
        # On vérifie juste qu'il a essayé d'afficher quelque chose
        self.assertTrue(
            mock_st.markdown.called or mock_st.error.called or mock_st.warning.called
        )


if __name__ == "__main__":
    unittest.main()
