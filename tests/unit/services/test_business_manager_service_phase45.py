"""Tests Phase 45: business_manager_service.py (48% → 50%)"""
import unittest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestGetBusinessManagerById(unittest.TestCase):
    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id_found(self, mock_session):
        from app.services.business_manager_service import BusinessManagerService
        from app.database.models import BusinessManager
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        bm = BusinessManager(id=1, prenom="Jean", nom="Dupont")
        mock_db.query.return_value.filter.return_value.first.return_value = bm
        
        result = BusinessManagerService.get_business_manager_by_id(1)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.prenom, "Jean")

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id_not_found(self, mock_session):
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = BusinessManagerService.get_business_manager_by_id(999)
        
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
