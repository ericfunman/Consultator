"""
Tests unitaires pour consultant_service.py - Phase 29
Coverage target: 82% → 90%+ (gain estimé +8-10%)

Stratégie:
- Fonctions helpers privées (_build_*, _apply_*, _convert_*, _calculate_*)
- Logique de filtrage et recherche optimisée
- Conversion de données et calculs
- Gestion de pagination et grouping

Fonctions clés à tester (~95 lignes manquantes):
- _build_search_query, _apply_search_filters, _finalize_search_query
- _convert_consultant_row_to_dict, _calculate_experience_years
- _build_stats_query, _format_salary_stats
- get_consultants_by_status, get_active_consultants
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import date, timedelta
import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestCalculateExperienceYears(unittest.TestCase):
    """Tests pour _calculate_experience_years"""

    def test_calculate_experience_years_none(self):
        """Test calcul expérience avec date None"""
        from app.services.consultant_service import ConsultantService

        result = ConsultantService._calculate_experience_years(None)
        self.assertEqual(result, 0)

    def test_calculate_experience_years_recent(self):
        """Test calcul expérience récente (<1 an)"""
        from app.services.consultant_service import ConsultantService

        today = date.today()
        date_mission = today - timedelta(days=180)  # 6 mois

        result = ConsultantService._calculate_experience_years(date_mission)
        self.assertGreater(result, 0)
        self.assertLess(result, 1)

    def test_calculate_experience_years_exact(self):
        """Test calcul expérience exacte (1 an)"""
        from app.services.consultant_service import ConsultantService

        today = date.today()
        date_mission = date(today.year - 1, today.month, today.day)

        result = ConsultantService._calculate_experience_years(date_mission)
        self.assertAlmostEqual(result, 1.0, places=1)

    def test_calculate_experience_years_long(self):
        """Test calcul expérience longue (10+ ans)"""
        from app.services.consultant_service import ConsultantService

        today = date.today()
        date_mission = date(today.year - 10, today.month, today.day)

        result = ConsultantService._calculate_experience_years(date_mission)
        self.assertGreater(result, 9.5)
        self.assertLess(result, 10.5)


class TestConvertConsultantRowToDict(unittest.TestCase):
    """Tests pour _convert_consultant_row_to_dict"""

    @patch("app.services.consultant_service.ConsultantService._calculate_experience_years")
    def test_convert_consultant_row_full(self, mock_exp):
        """Test conversion ligne complète"""
        from app.services.consultant_service import ConsultantService

        mock_exp.return_value = 5.2

        row = Mock(
            id=1,
            prenom="Jean",
            nom="Dupont",
            email="jean@test.com",
            telephone="0123456789",
            salaire_actuel=50000,
            disponibilite=True,
            grade="Senior",
            type_contrat="CDI",
            practice_name="Data",
            date_creation=date(2020, 1, 1),
            nb_missions=10,
            societe="Quanteam",
            date_premiere_mission=date(2019, 1, 1),
        )

        result = ConsultantService._convert_consultant_row_to_dict(row)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["nom"], "Dupont")
        self.assertEqual(result["salaire_actuel"], 50000)
        self.assertEqual(result["disponibilite"], True)
        self.assertEqual(result["experience_annees"], 5.2)
        self.assertIn("€", result["salaire_formatted"])
        self.assertEqual(result["statut"], ConsultantService.STATUS_AVAILABLE)

    @patch("app.services.consultant_service.ConsultantService._calculate_experience_years")
    def test_convert_consultant_row_minimal(self, mock_exp):
        """Test conversion ligne minimale (valeurs par défaut)"""
        from app.services.consultant_service import ConsultantService

        mock_exp.return_value = 0

        row = Mock(
            id=2,
            prenom="Marie",
            nom="Martin",
            email="marie@test.com",
            telephone=None,
            salaire_actuel=None,
            disponibilite=False,
            grade=None,
            type_contrat=None,
            practice_name=None,
            date_creation=date(2021, 1, 1),
            nb_missions=0,
            societe=None,
            date_premiere_mission=None,
        )

        result = ConsultantService._convert_consultant_row_to_dict(row)

        self.assertEqual(result["salaire_actuel"], 0)
        self.assertEqual(result["cjm"], 0)
        self.assertEqual(result["grade"], "Junior")
        self.assertEqual(result["type_contrat"], "CDI")
        self.assertEqual(result["practice_name"], "Non affecté")
        self.assertEqual(result["societe"], "Quanteam")
        self.assertEqual(result["experience_annees"], 0)
        self.assertEqual(result["statut"], ConsultantService.STATUS_BUSY)

    @patch("app.services.consultant_service.ConsultantService._calculate_experience_years")
    def test_convert_consultant_row_cjm_calculation(self, mock_exp):
        """Test calcul CJM correct"""
        from app.services.consultant_service import ConsultantService

        mock_exp.return_value = 3.0

        row = Mock(
            id=3,
            prenom="Test",
            nom="User",
            email="test@test.com",
            telephone="",
            salaire_actuel=60000,
            disponibilite=True,
            grade="Senior",
            type_contrat="CDI",
            practice_name="Quant",
            date_creation=date(2020, 1, 1),
            nb_missions=5,
            societe="Quanteam",
            date_premiere_mission=date(2018, 1, 1),
        )

        result = ConsultantService._convert_consultant_row_to_dict(row)

        # CJM = salaire * 1.8 / 216
        expected_cjm = 60000 * 1.8 / 216
        self.assertAlmostEqual(result["cjm"], expected_cjm, places=2)


class TestApplySearchFilters(unittest.TestCase):
    """Tests pour _apply_search_filters"""

    def test_apply_search_filters_practice(self):
        """Test filtre par practice"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        practice_filter = "Data"

        result = ConsultantService._apply_search_filters(mock_query, practice_filter, None, None, None)

        mock_query.filter.assert_called_once()
        self.assertEqual(result, mock_query.filter.return_value)

    def test_apply_search_filters_grade(self):
        """Test filtre par grade"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        grade_filter = "Senior"

        result = ConsultantService._apply_search_filters(mock_query, None, grade_filter, None, None)

        mock_query.filter.assert_called_once()

    def test_apply_search_filters_availability_true(self):
        """Test filtre disponibilité = True"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        availability_filter = True

        result = ConsultantService._apply_search_filters(mock_query, None, None, availability_filter, None)

        mock_query.filter.assert_called_once()

    def test_apply_search_filters_availability_false(self):
        """Test filtre disponibilité = False"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        availability_filter = False

        result = ConsultantService._apply_search_filters(mock_query, None, None, availability_filter, None)

        mock_query.filter.assert_called_once()

    def test_apply_search_filters_search_term(self):
        """Test filtre par terme de recherche"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        search_term = "Dupont"

        result = ConsultantService._apply_search_filters(mock_query, None, None, None, search_term)

        mock_query.filter.assert_called_once()

    def test_apply_search_filters_all_filters(self):
        """Test tous les filtres combinés"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        # Mock pour chaîner les appels filter()
        mock_query.filter.return_value = mock_query

        result = ConsultantService._apply_search_filters(mock_query, "Data", "Senior", True, "Dupont")

        # 4 filtres appliqués
        self.assertEqual(mock_query.filter.call_count, 4)

    def test_apply_search_filters_no_filters(self):
        """Test aucun filtre"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()

        result = ConsultantService._apply_search_filters(mock_query, None, None, None, None)

        mock_query.filter.assert_not_called()
        self.assertEqual(result, mock_query)


class TestFinalizeSearchQuery(unittest.TestCase):
    """Tests pour _finalize_search_query"""

    def test_finalize_search_query_page_1(self):
        """Test pagination page 1"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        mock_query.group_by.return_value = mock_query
        mock_query.offset.return_value = mock_query

        result = ConsultantService._finalize_search_query(mock_query, page=1, per_page=20)

        mock_query.group_by.assert_called_once()
        mock_query.offset.assert_called_once_with(0)  # (1-1)*20 = 0
        mock_query.limit.assert_called_once_with(20)

    def test_finalize_search_query_page_2(self):
        """Test pagination page 2"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        mock_query.group_by.return_value = mock_query
        mock_query.offset.return_value = mock_query

        result = ConsultantService._finalize_search_query(mock_query, page=2, per_page=50)

        mock_query.offset.assert_called_once_with(50)  # (2-1)*50 = 50
        mock_query.limit.assert_called_once_with(50)

    def test_finalize_search_query_page_10(self):
        """Test pagination page élevée"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()
        mock_query.group_by.return_value = mock_query
        mock_query.offset.return_value = mock_query

        result = ConsultantService._finalize_search_query(mock_query, page=10, per_page=100)

        mock_query.offset.assert_called_once_with(900)  # (10-1)*100 = 900
        mock_query.limit.assert_called_once_with(100)


class TestBuildSearchQuery(unittest.TestCase):
    """Tests pour _build_search_query"""

    @patch("app.services.consultant_service.ConsultantService._apply_search_filters")
    def test_build_search_query_structure(self, mock_apply):
        """Test structure de la requête"""
        from app.services.consultant_service import ConsultantService

        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query

        result = ConsultantService._build_search_query(mock_session, None, None, None, None)

        # Vérifie que query() est appelé
        mock_session.query.assert_called_once()
        # Vérifie que outerjoin est appelé (2 fois: Practice et Mission)
        self.assertEqual(mock_query.outerjoin.call_count, 2)
        # Vérifie que _apply_search_filters est appelé
        mock_apply.assert_called_once()

    @patch("app.services.consultant_service.ConsultantService._apply_search_filters")
    def test_build_search_query_with_filters(self, mock_apply):
        """Test requête avec filtres"""
        from app.services.consultant_service import ConsultantService

        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query

        result = ConsultantService._build_search_query(mock_session, "Data", "Senior", True, "Dupont")

        # Vérifie que les filtres sont passés à _apply_search_filters
        mock_apply.assert_called_once_with(mock_query, "Data", "Senior", True, "Dupont")


class TestGetConsultantsCount(unittest.TestCase):
    """Tests pour get_consultants_count"""

    @patch("app.services.consultant_service.get_database_session")
    def test_get_consultants_count_success(self, mock_session):
        """Test comptage réussi"""
        from app.services.consultant_service import ConsultantService

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.count.return_value = 42

        result = ConsultantService.get_consultants_count()

        self.assertEqual(result, 42)

    @patch("app.services.consultant_service.get_database_session")
    def test_get_consultants_count_zero(self, mock_session):
        """Test comptage = 0"""
        from app.services.consultant_service import ConsultantService

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.count.return_value = 0

        result = ConsultantService.get_consultants_count()

        self.assertEqual(result, 0)

    @patch("app.services.consultant_service.get_database_session")
    def test_get_consultants_count_error(self, mock_session):
        """Test erreur comptage (gestion d'exception SQLAlchemy)"""
        from app.services.consultant_service import ConsultantService
        from sqlalchemy.exc import SQLAlchemyError

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        # Lever une SQLAlchemyError au moment de la requête
        mock_db.query.return_value.count.side_effect = SQLAlchemyError("Database error")

        result = ConsultantService.get_consultants_count()

        self.assertEqual(result, 0)


class TestBuildStatsQuery(unittest.TestCase):
    """Tests pour _build_stats_query et _apply_stats_filters"""

    @patch("app.services.consultant_service.ConsultantService._apply_stats_filters")
    def test_build_stats_query_no_filters(self, mock_apply):
        """Test requête stats sans filtres"""
        from app.services.consultant_service import ConsultantService

        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query

        ConsultantService._build_stats_query(mock_session, None, None, None)

        mock_session.query.assert_called_once()
        # 2 outerjoin: Practice et Mission
        self.assertEqual(mock_query.outerjoin.call_count, 2)
        mock_apply.assert_called_once_with(mock_query, None, None, None)

    @patch("app.services.consultant_service.ConsultantService._apply_stats_filters")
    def test_build_stats_query_with_filters(self, mock_apply):
        """Test requête stats avec filtres"""
        from app.services.consultant_service import ConsultantService

        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query

        ConsultantService._build_stats_query(mock_session, "Data", "Senior", True)

        mock_apply.assert_called_once_with(mock_query, "Data", "Senior", True)


class TestApplyStatsFilters(unittest.TestCase):
    """Tests pour _apply_stats_filters"""

    def test_apply_stats_filters_practice(self):
        """Test filtre practice pour stats"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()

        ConsultantService._apply_stats_filters(mock_query, "Data", None, None)

        mock_query.filter.assert_called_once()

    def test_apply_stats_filters_grade(self):
        """Test filtre grade pour stats"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()

        ConsultantService._apply_stats_filters(mock_query, None, "Senior", None)

        mock_query.filter.assert_called_once()

    def test_apply_stats_filters_availability(self):
        """Test filtre disponibilité pour stats"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()

        ConsultantService._apply_stats_filters(mock_query, None, None, True)

        mock_query.filter.assert_called_once()

    def test_apply_stats_filters_no_filters(self):
        """Test aucun filtre pour stats"""
        from app.services.consultant_service import ConsultantService

        mock_query = MagicMock()

        result = ConsultantService._apply_stats_filters(mock_query, None, None, None)

        mock_query.filter.assert_not_called()
        self.assertEqual(result, mock_query)


class TestConstants(unittest.TestCase):
    """Tests pour les constantes de la classe"""

    def test_constants_exist(self):
        """Test existence des constantes"""
        from app.services.consultant_service import ConsultantService

        self.assertTrue(hasattr(ConsultantService, "STATUS_AVAILABLE"))
        self.assertTrue(hasattr(ConsultantService, "STATUS_BUSY"))

    def test_constants_values(self):
        """Test valeurs des constantes"""
        from app.services.consultant_service import ConsultantService

        self.assertIsInstance(ConsultantService.STATUS_AVAILABLE, str)
        self.assertIsInstance(ConsultantService.STATUS_BUSY, str)
        self.assertNotEqual(ConsultantService.STATUS_AVAILABLE, ConsultantService.STATUS_BUSY)


if __name__ == "__main__":
    unittest.main()
