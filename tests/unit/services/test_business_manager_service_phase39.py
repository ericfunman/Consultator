"""Tests Phase 39: business_manager_service.py (48% → 65%+)"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestGetAllBusinessManagers(unittest.TestCase):
    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers_success(self, mock_session):
        from app.services.business_manager_service import BusinessManagerService
        
        # Mock BM
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        mock_bm.email = "jean@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = "Test"
        
        # Mock session
        mock_db = MagicMock()
        mock_db.query.return_value.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 5
        mock_session.return_value.__enter__.return_value = mock_db
        
        result = BusinessManagerService.get_all_business_managers()
        
        self.assertIsInstance(result, list)
        if result:
            self.assertIn("id", result[0])

class TestSearchBusinessManagers(unittest.TestCase):
    @patch("app.services.business_manager_service.get_database_session")
    def test_search_business_managers_found(self, mock_session):
        from app.services.business_manager_service import BusinessManagerService
        
        # Mock BM matching search
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        mock_bm.email = "jean@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""
        
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.filter.return_value.count.return_value = 0
        mock_session.return_value.__enter__.return_value = mock_db
        
        result = BusinessManagerService.search_business_managers("Jean")
        
        self.assertIsInstance(result, list)

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_business_managers_empty(self, mock_session):
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.all.return_value = []
        mock_session.return_value.__enter__.return_value = mock_db
        
        result = BusinessManagerService.search_business_managers("Inconnu")
        
        self.assertEqual(result, [])

class TestGetBusinessManagerById(unittest.TestCase):
    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id_found(self, mock_session):
        from app.services.business_manager_service import BusinessManagerService
        
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_bm
        mock_session.return_value.__enter__.return_value = mock_db
        
        result = BusinessManagerService.get_business_manager_by_id(1)
        
        self.assertIsNotNone(result)

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id_not_found(self, mock_session):
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_session.return_value.__enter__.return_value = mock_db
        
        result = BusinessManagerService.get_business_manager_by_id(999)
        
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
