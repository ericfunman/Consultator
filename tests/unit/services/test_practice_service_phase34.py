"""
Tests unitaires pour practice_service.py - Phase 34
Coverage: 71% → 85%+ (gain estimé +14%)
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestGetAllPractices(unittest.TestCase):
    """Tests pour get_all_practices"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_all_practices_success(self, mock_st, mock_get_session):
        """Test récupération toutes practices"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        p1 = Mock(id=1, nom="Data", actif=True)
        p2 = Mock(id=2, nom="Quant", actif=True)
        mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [p1, p2]

        result = PracticeService.get_all_practices()

        self.assertEqual(len(result), 2)
        mock_session.close.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_all_practices_error(self, mock_st, mock_get_session):
        """Test erreur SQL"""
        from app.services.practice_service import PracticeService
        from sqlalchemy.exc import SQLAlchemyError

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.side_effect = SQLAlchemyError("DB error")

        result = PracticeService.get_all_practices()

        self.assertEqual(result, [])
        mock_st.error.assert_called_once()


class TestGetPracticeById(unittest.TestCase):
    """Tests pour get_practice_by_id"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_by_id_found(self, mock_st, mock_get_session):
        """Test practice trouvée"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        practice = Mock(id=1, nom="Data")
        mock_session.query.return_value.filter.return_value.first.return_value = practice

        result = PracticeService.get_practice_by_id(1)

        self.assertEqual(result.nom, "Data")

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_by_id_not_found(self, mock_st, mock_get_session):
        """Test practice non trouvée"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = PracticeService.get_practice_by_id(999)

        self.assertIsNone(result)


class TestGetPracticeByName(unittest.TestCase):
    """Tests pour get_practice_by_name"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_by_name_found(self, mock_st, mock_get_session):
        """Test practice trouvée par nom"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        practice = Mock(id=1, nom="Data")
        mock_session.query.return_value.filter.return_value.first.return_value = practice

        result = PracticeService.get_practice_by_name("Data")

        self.assertEqual(result.nom, "Data")


class TestCreatePractice(unittest.TestCase):
    """Tests pour create_practice"""

    @patch("app.services.practice_service.Practice")
    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_create_practice_success(self, mock_st, mock_get_session, mock_practice_class):
        """Test création practice réussie"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        mock_practice = Mock(id=1, nom="NewPractice")
        mock_practice_class.return_value = mock_practice

        result = PracticeService.create_practice("NewPractice", "Description", "Manager")

        self.assertIsNotNone(result)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_st.success.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_create_practice_already_exists(self, mock_st, mock_get_session):
        """Test practice déjà existante"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = Mock()

        result = PracticeService.create_practice("Existing")

        self.assertIsNone(result)
        mock_st.error.assert_called_once()


class TestUpdatePractice(unittest.TestCase):
    """Tests pour update_practice"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_update_practice_success(self, mock_st, mock_get_session):
        """Test mise à jour réussie"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        practice = Mock(id=1, nom="Data", description="Old")
        mock_session.query.return_value.filter.return_value.first.return_value = practice

        result = PracticeService.update_practice(1, nom="Data Updated", description="New")

        self.assertTrue(result)
        self.assertEqual(practice.nom, "Data Updated")
        self.assertEqual(practice.description, "New")
        mock_session.commit.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_update_practice_not_found(self, mock_st, mock_get_session):
        """Test practice non trouvée"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = PracticeService.update_practice(999, nom="Test")

        self.assertFalse(result)
        mock_st.error.assert_called_once()


class TestGetConsultantsByPractice(unittest.TestCase):
    """Tests pour get_consultants_by_practice"""

    @patch("app.services.practice_service.PracticeService._get_consultants_for_specific_practice")
    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_consultants_by_practice_specific(self, mock_st, mock_get_session, mock_get_specific):
        """Test consultants d'une practice spécifique"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_get_specific.return_value = {"Data": [Mock(), Mock()]}

        result = PracticeService.get_consultants_by_practice(practice_id=1)

        self.assertIn("Data", result)
        mock_get_specific.assert_called_once_with(mock_session, 1)

    @patch("app.services.practice_service.PracticeService._get_all_consultants_by_practice")
    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_consultants_by_practice_all(self, mock_st, mock_get_session, mock_get_all):
        """Test tous consultants groupés"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_get_all.return_value = {"Data": [Mock()], "Quant": [Mock()]}

        result = PracticeService.get_consultants_by_practice()

        self.assertEqual(len(result), 2)
        mock_get_all.assert_called_once()


class TestAssignConsultantToPractice(unittest.TestCase):
    """Tests pour assign_consultant_to_practice"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_assign_consultant_success(self, mock_st, mock_get_session):
        """Test assignation réussie"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        consultant = Mock(id=1, practice_id=None)
        mock_session.query.return_value.filter.return_value.first.return_value = consultant

        result = PracticeService.assign_consultant_to_practice(1, 2)

        self.assertTrue(result)
        self.assertEqual(consultant.practice_id, 2)
        mock_session.commit.assert_called_once()

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_assign_consultant_not_found(self, mock_st, mock_get_session):
        """Test consultant non trouvé"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        result = PracticeService.assign_consultant_to_practice(999, 1)

        self.assertFalse(result)


class TestGetPracticeStatistics(unittest.TestCase):
    """Tests pour get_practice_statistics"""

    @patch("app.services.practice_service.get_session")
    @patch("app.services.practice_service.st")
    def test_get_practice_statistics_success(self, mock_st, mock_get_session):
        """Test statistiques practices"""
        from app.services.practice_service import PracticeService

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session
        
        p1 = Mock(id=1, nom="Data")
        p2 = Mock(id=2, nom="Quant")
        mock_session.query.return_value.filter.return_value.all.return_value = [p1, p2]
        
        mock_session.query.return_value.filter.return_value.count.return_value = 5

        result = PracticeService.get_practice_statistics()

        self.assertIn("total_practices", result)
        self.assertIn("practices_detail", result)


if __name__ == "__main__":
    unittest.main()
