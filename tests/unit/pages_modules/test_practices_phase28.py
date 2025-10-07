"""
Tests unitaires pour le module practices.py - Phase 28
Coverage target: 63.5% → 85%+ (gain estimé +21-22%)

Stratégie:
- Fonctions d'affichage de données et formatage
- Gestion d'assignation consultants
- Préparation de données pour tableaux
- Export CSV
- Création de practices

Fonctions clés à tester (89 lignes manquantes):
- _prepare_consultants_table_data, _format_consultant_salary
- _get_available_consultants, _get_consultant_current_practice
- _prepare_csv_export_data, _generate_csv_download
- _handle_practice_creation, _create_new_practice
- show_practice_overview, show_consultants_by_practice
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestFormatConsultantSalary(unittest.TestCase):
    """Tests pour _format_consultant_salary"""

    def test_format_consultant_salary_with_value(self):
        """Test formatage salaire avec valeur"""
        from app.pages_modules.practices import _format_consultant_salary

        consultant = Mock(salaire_actuel=50000)
        result = _format_consultant_salary(consultant)
        self.assertEqual(result, "50,000€")

    def test_format_consultant_salary_none(self):
        """Test formatage salaire None"""
        from app.pages_modules.practices import _format_consultant_salary

        consultant = Mock(salaire_actuel=None)
        result = _format_consultant_salary(consultant)
        self.assertEqual(result, "Non défini")

    def test_format_consultant_salary_zero(self):
        """Test formatage salaire 0 (comportement: considéré comme None)"""
        from app.pages_modules.practices import _format_consultant_salary

        consultant = Mock(salaire_actuel=0)
        result = _format_consultant_salary(consultant)
        # Salaire 0 est falsy, donc considéré comme non défini
        self.assertEqual(result, "Non défini")


class TestPrepareConsultantsTableData(unittest.TestCase):
    """Tests pour _prepare_consultants_table_data"""

    def test_prepare_consultants_table_data_full(self):
        """Test préparation données complètes"""
        from app.pages_modules.practices import _prepare_consultants_table_data

        consultant = Mock(
            id=1,
            nom="Dupont",
            prenom="Jean",
            email="jean@test.com",
            grade="Senior",
            disponibilite=True,
            salaire_actuel=60000,
        )

        result = _prepare_consultants_table_data([consultant])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["ID"], 1)
        self.assertEqual(result[0]["Nom"], "Dupont")
        self.assertEqual(result[0]["Prénom"], "Jean")
        self.assertEqual(result[0]["Disponible"], "✅")

    def test_prepare_consultants_table_data_minimal(self):
        """Test préparation données minimales"""
        from app.pages_modules.practices import _prepare_consultants_table_data

        consultant = Mock(id=2, nom="Martin", prenom="Marie", email="marie@test.com", spec=["id", "nom", "prenom", "email"])

        result = _prepare_consultants_table_data([consultant])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Grade"], "Non défini")
        self.assertEqual(result[0]["Disponible"], "❌")

    def test_prepare_consultants_table_data_empty(self):
        """Test préparation données vide"""
        from app.pages_modules.practices import _prepare_consultants_table_data

        result = _prepare_consultants_table_data([])
        self.assertEqual(result, [])

    def test_prepare_consultants_table_data_multiple(self):
        """Test préparation multiples consultants"""
        from app.pages_modules.practices import _prepare_consultants_table_data

        consultants = [
            Mock(id=1, nom="Dupont", prenom="Jean", email="jean@test.com", grade="Senior", disponibilite=True, salaire_actuel=50000),
            Mock(id=2, nom="Martin", prenom="Marie", email="marie@test.com", grade="Junior", disponibilite=False, salaire_actuel=40000),
        ]

        result = _prepare_consultants_table_data(consultants)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Nom"], "Dupont")
        self.assertEqual(result[1]["Nom"], "Martin")


class TestGetConsultantCurrentPractice(unittest.TestCase):
    """Tests pour _get_consultant_current_practice"""

    @patch("app.pages_modules.practices.PracticeService")
    def test_get_consultant_current_practice_found(self, mock_service):
        """Test récupération practice actuelle trouvée"""
        from app.pages_modules.practices import _get_consultant_current_practice

        practice = Mock(nom="Data")
        mock_service.get_practice_by_id.return_value = practice

        consultant = Mock(practice_id=1)
        result = _get_consultant_current_practice(consultant)

        self.assertEqual(result, "Data")
        mock_service.get_practice_by_id.assert_called_once_with(1)

    @patch("app.pages_modules.practices.PracticeService")
    def test_get_consultant_current_practice_none(self, mock_service):
        """Test récupération practice avec practice_id None"""
        from app.pages_modules.practices import _get_consultant_current_practice

        consultant = Mock(practice_id=None)
        result = _get_consultant_current_practice(consultant)

        self.assertEqual(result, "Aucune")
        mock_service.get_practice_by_id.assert_not_called()

    @patch("app.pages_modules.practices.PracticeService")
    def test_get_consultant_current_practice_not_found(self, mock_service):
        """Test récupération practice non trouvée"""
        from app.pages_modules.practices import _get_consultant_current_practice

        mock_service.get_practice_by_id.return_value = None

        consultant = Mock(practice_id=999)
        result = _get_consultant_current_practice(consultant)

        self.assertEqual(result, "Aucune")


class TestGetAvailableConsultants(unittest.TestCase):
    """Tests pour _get_available_consultants"""

    @patch("app.services.consultant_service.ConsultantService")
    def test_get_available_consultants_filtered(self, mock_service):
        """Test filtrage consultants disponibles"""
        from app.pages_modules.practices import _get_available_consultants

        c1 = Mock(id=1, practice_id=None)
        c2 = Mock(id=2, practice_id=1)
        c3 = Mock(id=3, practice_id=2)

        mock_service.get_all_consultants_objects.return_value = [c1, c2, c3]

        practice = Mock(id=1)
        result = _get_available_consultants(practice)

        # c1 (None) et c3 (practice 2) sont disponibles
        self.assertEqual(len(result), 2)
        self.assertIn(c1, result)
        self.assertIn(c3, result)
        self.assertNotIn(c2, result)

    @patch("app.services.consultant_service.ConsultantService")
    def test_get_available_consultants_all_assigned(self, mock_service):
        """Test tous consultants déjà assignés"""
        from app.pages_modules.practices import _get_available_consultants

        c1 = Mock(id=1, practice_id=1)
        c2 = Mock(id=2, practice_id=1)

        mock_service.get_all_consultants_objects.return_value = [c1, c2]

        practice = Mock(id=1)
        result = _get_available_consultants(practice)

        self.assertEqual(len(result), 0)

    @patch("app.services.consultant_service.ConsultantService")
    def test_get_available_consultants_all_available(self, mock_service):
        """Test tous consultants disponibles"""
        from app.pages_modules.practices import _get_available_consultants

        c1 = Mock(id=1, practice_id=None)
        c2 = Mock(id=2, practice_id=None)

        mock_service.get_all_consultants_objects.return_value = [c1, c2]

        practice = Mock(id=1)
        result = _get_available_consultants(practice)

        self.assertEqual(len(result), 2)


class TestPrepareCsvExportData(unittest.TestCase):
    """Tests pour _prepare_csv_export_data"""

    def test_prepare_csv_export_data_full(self):
        """Test préparation export CSV complet"""
        from app.pages_modules.practices import _prepare_csv_export_data

        consultants = [
            Mock(
                id=1,
                nom="Dupont",
                prenom="Jean",
                email="jean@test.com",
                grade="Senior",
                disponibilite=True,
                salaire_actuel=60000,
            )
        ]

        practice = Mock(nom="Data")
        result = _prepare_csv_export_data(consultants, practice)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Practice"], "Data")
        self.assertEqual(result[0]["Salaire"], 60000)

    def test_prepare_csv_export_data_minimal(self):
        """Test préparation export CSV minimal"""
        from app.pages_modules.practices import _prepare_csv_export_data

        consultants = [Mock(id=2, nom="Martin", prenom="Marie", email="marie@test.com", spec=["id", "nom", "prenom", "email"])]

        practice = Mock(nom="Quant")
        result = _prepare_csv_export_data(consultants, practice)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Grade"], "")
        self.assertEqual(result[0]["Disponible"], False)


class TestHandlePracticeCreation(unittest.TestCase):
    """Tests pour _handle_practice_creation et _create_new_practice"""

    @patch("app.pages_modules.practices.st")
    @patch("app.pages_modules.practices.PracticeService")
    def test_create_new_practice_success(self, mock_service, mock_st):
        """Test création practice réussie"""
        from app.pages_modules.practices import _create_new_practice

        mock_service.create_practice.return_value = Mock(id=1, nom="Data")

        _create_new_practice("Data", "Practice Data", "Jean Dupont")

        mock_service.create_practice.assert_called_once_with(nom="Data", description="Practice Data", responsable="Jean Dupont")
        mock_st.success.assert_called_once()

    @patch("app.pages_modules.practices.st")
    @patch("app.pages_modules.practices.PracticeService")
    def test_create_new_practice_failure(self, mock_service, mock_st):
        """Test création practice échouée"""
        from app.pages_modules.practices import _create_new_practice

        mock_service.create_practice.return_value = None

        _create_new_practice("Data", "", "")

        mock_st.error.assert_called()

    @patch("app.pages_modules.practices.st")
    def test_handle_practice_creation_empty_name(self, mock_st):
        """Test création avec nom vide"""
        from app.pages_modules.practices import _handle_practice_creation

        _handle_practice_creation("", "Description", "Responsable")

        mock_st.error.assert_called_once()

    @patch("app.pages_modules.practices.st")
    @patch("app.pages_modules.practices.PracticeService")
    def test_handle_practice_creation_valid_name(self, mock_service, mock_st):
        """Test création avec nom valide"""
        from app.pages_modules.practices import _handle_practice_creation

        mock_service.create_practice.return_value = Mock(id=1)

        _handle_practice_creation("Data", "Description", "Responsable")

        mock_service.create_practice.assert_called_once()


class TestDisplayFunctions(unittest.TestCase):
    """Tests pour les fonctions d'affichage avec Streamlit"""

    @patch("app.pages_modules.practices.st")
    @patch("app.pages_modules.practices.PracticeService")
    def test_show_practice_overview_success(self, mock_service, mock_st):
        """Test affichage vue d'ensemble réussie"""
        from app.pages_modules.practices import show_practice_overview

        mock_service.get_practice_statistics.return_value = {
            "total_practices": 2,
            "total_consultants": 10,
            "active_practices": 2,
        }

        practices = [Mock(nom="Data", description="Practice Data", responsable="Jean", actif=True)]
        mock_service.get_all_practices.return_value = practices

        # Mock st.columns pour éviter ValueError
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        show_practice_overview()

        mock_st.subheader.assert_called()
        self.assertEqual(mock_st.metric.call_count, 3)

    @patch("app.pages_modules.practices.st")
    @patch("app.pages_modules.practices.PracticeService")
    def test_show_practice_overview_error(self, mock_service, mock_st):
        """Test affichage vue d'ensemble avec erreur"""
        from app.pages_modules.practices import show_practice_overview

        mock_service.get_practice_statistics.side_effect = Exception("Database error")

        show_practice_overview()

        mock_st.error.assert_called()

    @patch("app.pages_modules.practices.st")
    def test_display_consultants_simple_list(self, mock_st):
        """Test affichage liste simple consultants"""
        from app.pages_modules.practices import _display_consultants_simple_list

        consultant_data = [
            {"Prénom": "Jean", "Nom": "Dupont", "Grade": "Senior", "Email": "jean@test.com", "Salaire": "50,000€"}
        ]

        _display_consultants_simple_list(consultant_data)

        mock_st.write.assert_called()

    @patch("app.pages_modules.practices.st")
    @patch("app.pages_modules.practices.pd")
    def test_display_consultants_dataframe_with_pandas(self, mock_pd, mock_st):
        """Test affichage dataframe avec pandas"""
        from app.pages_modules.practices import _display_consultants_dataframe

        consultant_data = [{"ID": 1, "Nom": "Dupont"}]
        mock_df = MagicMock()
        mock_pd.DataFrame.return_value = mock_df

        _display_consultants_dataframe(consultant_data)

        mock_pd.DataFrame.assert_called_once()
        mock_st.dataframe.assert_called_once()

    @patch("app.pages_modules.practices.st")
    def test_display_consultants_dataframe_empty(self, mock_st):
        """Test affichage dataframe vide"""
        from app.pages_modules.practices import _display_consultants_dataframe

        _display_consultants_dataframe([])

        # Aucun appel ne devrait être fait pour liste vide
        mock_st.dataframe.assert_not_called()

    @patch("app.pages_modules.practices.st")
    @patch("app.pages_modules.practices.PracticeService")
    def test_display_practice_statistics(self, mock_service, mock_st):
        """Test affichage statistiques practice"""
        from app.pages_modules.practices import _display_practice_statistics

        mock_service.get_practice_statistics.return_value = {
            "practices_detail": [
                {
                    "nom": "Data",
                    "total_consultants": 5,
                    "consultants_actifs": 3,
                    "responsable": "Jean Dupont",
                }
            ]
        }

        practice = Mock(nom="Data")
        _display_practice_statistics(practice)

        mock_st.write.assert_called()
        self.assertEqual(mock_st.metric.call_count, 2)

    @patch("app.pages_modules.practices.st")
    @patch("app.pages_modules.practices.PracticeService")
    def test_display_practice_statistics_error(self, mock_service, mock_st):
        """Test affichage statistiques avec erreur"""
        from app.pages_modules.practices import _display_practice_statistics

        mock_service.get_practice_statistics.side_effect = Exception("Error")

        practice = Mock(nom="Data")
        _display_practice_statistics(practice)

        mock_st.error.assert_called()


class TestGetColumnConfig(unittest.TestCase):
    """Tests pour _get_column_config"""

    @patch("app.pages_modules.practices.st")
    def test_get_column_config_structure(self, mock_st):
        """Test structure configuration colonnes"""
        from app.pages_modules.practices import _get_column_config

        result = _get_column_config()

        self.assertIsInstance(result, dict)
        self.assertIn("ID", result)
        self.assertIn("Nom", result)
        self.assertIn("Prénom", result)
        self.assertIn("Email", result)


if __name__ == "__main__":
    unittest.main()
