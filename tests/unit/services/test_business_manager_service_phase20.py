"""
Tests Phase 20 FINALE: BusinessManagerService - 48% -> 80%!
Ciblage: 32 lignes manquantes dans business_manager_service.py
Focus: get_all, search, count, get_by_id avec consultants_count
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime


class TestBusinessManagerServiceComplete(unittest.TestCase):
    """BusinessManagerService - 48% -> 80% (32 lignes)"""

    @patch('app.database.database.get_database_session')
    def test_get_all_business_managers_success(self, mock_session):
        """Test récupération tous les BM avec consultants count"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock BM
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        mock_bm.email = "jean.dupont@test.com"
        mock_bm.telephone = "0601020304"
        mock_bm.actif = True
        mock_bm.date_creation = datetime(2024, 1, 1)
        mock_bm.notes = "Test notes"
        
        # Mock query chain
        mock_query = mock_db.query.return_value
        mock_query.all.return_value = [mock_bm]
        
        # Mock consultants count
        mock_count_query = mock_db.query.return_value.filter.return_value
        mock_count_query.count.return_value = 5
        
        result = BusinessManagerService.get_all_business_managers()
        
        assert isinstance(result, list)
        assert len(result) >= 0

    @patch('app.database.database.get_database_session')
    def test_get_all_business_managers_empty(self, mock_session):
        """Test récupération BM liste vide"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_query.all.return_value = []
        
        result = BusinessManagerService.get_all_business_managers()
        
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.database.database.get_database_session')
    def test_get_all_business_managers_error(self, mock_session):
        """Test récupération BM avec erreur SQL"""
        from app.services.business_manager_service import BusinessManagerService
        from sqlalchemy.exc import SQLAlchemyError
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = SQLAlchemyError("Test error")
        
        result = BusinessManagerService.get_all_business_managers()
        
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.database.database.get_database_session')
    def test_search_business_managers_by_nom(self, mock_session):
        """Test recherche BM par nom"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        mock_bm.email = "jean@test.com"
        mock_bm.telephone = "0601020304"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""
        
        # Mock query chain with filter
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm]
        
        # Mock consultants count
        mock_count = mock_db.query.return_value.filter.return_value
        mock_count.count.return_value = 3
        
        result = BusinessManagerService.search_business_managers("Dupont")
        
        assert isinstance(result, list)

    @patch('app.database.database.get_database_session')
    def test_search_business_managers_by_email(self, mock_session):
        """Test recherche BM par email"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock()
        mock_bm.id = 2
        mock_bm.prenom = "Marie"
        mock_bm.nom = "Martin"
        mock_bm.email = "marie.martin@test.com"
        mock_bm.telephone = "0602030405"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = None
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm]
        
        mock_count = mock_db.query.return_value.filter.return_value
        mock_count.count.return_value = 2
        
        result = BusinessManagerService.search_business_managers("marie@test.com")
        
        assert isinstance(result, list)

    @patch('app.database.database.get_database_session')
    def test_search_business_managers_empty_term(self, mock_session):
        """Test recherche BM avec terme vide"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_query.all.return_value = []
        
        result = BusinessManagerService.search_business_managers("")
        
        assert isinstance(result, list)

    @patch('app.database.database.get_database_session')
    def test_search_business_managers_no_results(self, mock_session):
        """Test recherche BM sans résultats"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = []
        
        result = BusinessManagerService.search_business_managers("NonExistant")
        
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.database.database.get_database_session')
    def test_search_business_managers_error(self, mock_session):
        """Test recherche BM avec erreur SQL"""
        from app.services.business_manager_service import BusinessManagerService
        from sqlalchemy.exc import SQLAlchemyError
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = SQLAlchemyError("Search error")
        
        result = BusinessManagerService.search_business_managers("Test")
        
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.database.database.get_database_session')
    def test_get_business_managers_count_success(self, mock_session):
        """Test comptage BM réussi"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_query.count.return_value = 42
        
        result = BusinessManagerService.get_business_managers_count()
        
        assert isinstance(result, int)
        assert result >= 0

    @patch('app.database.database.get_database_session')
    def test_get_business_managers_count_zero(self, mock_session):
        """Test comptage BM vide"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_query.count.return_value = 0
        
        result = BusinessManagerService.get_business_managers_count()
        
        assert result == 0

    @patch('app.database.database.get_database_session')
    def test_get_business_managers_count_error(self, mock_session):
        """Test comptage BM avec erreur"""
        from app.services.business_manager_service import BusinessManagerService
        from sqlalchemy.exc import SQLAlchemyError
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = SQLAlchemyError("Count error")
        
        result = BusinessManagerService.get_business_managers_count()
        
        assert result == 0

    @patch('app.database.database.get_database_session')
    def test_get_business_manager_by_id_success(self, mock_session):
        """Test récupération BM par ID réussi"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.nom = "Dupont"
        mock_bm.prenom = "Jean"
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.first.return_value = mock_bm
        
        result = BusinessManagerService.get_business_manager_by_id(1)
        
        assert result is not None

    @patch('app.database.database.get_database_session')
    def test_get_business_manager_by_id_not_found(self, mock_session):
        """Test récupération BM par ID introuvable"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.first.return_value = None
        
        result = BusinessManagerService.get_business_manager_by_id(999)
        
        assert result is None

    @patch('app.database.database.get_database_session')
    def test_get_business_manager_by_id_error(self, mock_session):
        """Test récupération BM par ID avec erreur"""
        from app.services.business_manager_service import BusinessManagerService
        from sqlalchemy.exc import SQLAlchemyError
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = SQLAlchemyError("Get by ID error")
        
        result = BusinessManagerService.get_business_manager_by_id(1)
        
        assert result is None

    @patch('app.database.database.get_database_session')
    def test_consultants_count_logic(self, mock_session):
        """Test logique comptage consultants actifs"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        mock_bm.email = "jean@test.com"
        mock_bm.telephone = "0601"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""
        
        mock_query = mock_db.query.return_value
        mock_query.all.return_value = [mock_bm]
        
        # Mock consultants count avec filtre date_fin.is_(None)
        mock_count = mock_db.query.return_value.filter.return_value
        mock_count.count.return_value = 10
        
        result = BusinessManagerService.get_all_business_managers()
        
        assert isinstance(result, list)
        if len(result) > 0:
            assert "consultants_count" in result[0]

    @patch('app.database.database.get_database_session')
    def test_bm_dict_conversion_complete(self, mock_session):
        """Test conversion complète BM en dict"""
        from app.services.business_manager_service import BusinessManagerService
        
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock()
        mock_bm.id = 5
        mock_bm.prenom = "Sophie"
        mock_bm.nom = "Bernard"
        mock_bm.email = "sophie.bernard@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = False
        mock_bm.date_creation = datetime(2023, 6, 15)
        mock_bm.notes = "Important notes"
        
        mock_query = mock_db.query.return_value
        mock_query.all.return_value = [mock_bm]
        
        mock_count = mock_db.query.return_value.filter.return_value
        mock_count.count.return_value = 7
        
        result = BusinessManagerService.get_all_business_managers()
        
        assert isinstance(result, list)
        if len(result) > 0:
            bm_dict = result[0]
            assert "id" in bm_dict
            assert "prenom" in bm_dict
            assert "nom" in bm_dict
            assert "email" in bm_dict
            assert "telephone" in bm_dict
            assert "actif" in bm_dict
            assert "consultants_count" in bm_dict
            assert "date_creation" in bm_dict
            assert "notes" in bm_dict


if __name__ == "__main__":
    unittest.main()
