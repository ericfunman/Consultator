"""
Tests ciblés pour business_manager_service - Amélioration couverture 48% -> 70%+
"""

import unittest
from unittest.mock import patch, MagicMock
from app.services.business_manager_service import BusinessManagerService


class TestBusinessManagerServiceCoverage(unittest.TestCase):
    """Tests pour améliorer la couverture de business_manager_service"""

    def setUp(self):
        self.service = BusinessManagerService()

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers(self, mock_session):
        """Test get_all_business_managers()"""
        mock_session.return_value.__enter__.return_value.query.return_value.all.return_value = []
        result = self.service.get_all_business_managers()
        self.assertEqual(result, [])

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id(self, mock_session):
        """Test get_business_manager_by_id()"""
        mock_bm = MagicMock()
        mock_session.return_value.__enter__.return_value.query.return_value.filter.return_value.first.return_value = (
            mock_bm
        )
        result = self.service.get_business_manager_by_id(1)
        self.assertEqual(result, mock_bm)

    @patch("app.services.business_manager_service.get_database_session")
    def test_create_business_manager(self, mock_session):
        """Test create_business_manager()"""
        mock_session_obj = mock_session.return_value.__enter__.return_value
        data = {"nom_complet": "Test Manager", "email": "test@test.com"}

        result = self.service.create_business_manager(data)

        mock_session_obj.add.assert_called_once()
        mock_session_obj.commit.assert_called_once()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
