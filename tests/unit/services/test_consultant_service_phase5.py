"""
Tests de couverture Phase 5 : ConsultantService - Lignes non couvertes ciblées
Objectif : Couvrir les 113 lignes restantes de consultant_service.py (actuellement à 79%)
Lignes cibles : 148,151,154 (erreurs), 230-234 (pagination), 266-268 (optimize), 
                725,732-734,771-777 (delete), 806-808,825-827,862-864 (update),
                1152-1158,1178,1188-1253 (import/export edge cases)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import date
from app.services.consultant_service import ConsultantService


class TestGetConsultantById:
    """Tests pour get_consultant_by_id"""
    
    @patch('app.database.database.Session')
    def test_get_consultant_by_id_found(self, mock_session):
        """Test récupération consultant existant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(id=1, nom="Dupont")
        mock_db.query.return_value.filter.return_value.first.return_value = consultant
        
        result = ConsultantService.get_consultant_by_id(1)
        assert result is not None
    
    @patch('app.database.database.Session')
    def test_get_consultant_by_id_not_found(self, mock_session):
        """Test consultant inexistant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = ConsultantService.get_consultant_by_id(999)
        assert result is None


class TestUpdateConsultant:
    """Tests pour update_consultant"""
    
    @patch('app.database.database.Session')
    def test_update_consultant_success(self, mock_session):
        """Test mise à jour consultant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = consultant
        
        data = {"nom": "Martin"}
        result = ConsultantService.update_consultant(1, data)
        assert result is True
    
    @patch('app.database.database.Session')
    def test_update_consultant_not_found(self, mock_session):
        """Test mise à jour consultant inexistant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = ConsultantService.update_consultant(999, {"nom": "Test"})
        assert result is False


class TestDeleteConsultant:
    """Tests pour delete_consultant"""
    
    @patch('app.database.database.Session')
    def test_delete_consultant_success(self, mock_session):
        """Test suppression consultant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = consultant
        
        result = ConsultantService.delete_consultant(1)
        assert result is True
    
    @patch('app.database.database.Session')
    def test_delete_consultant_not_found(self, mock_session):
        """Test suppression consultant inexistant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = ConsultantService.delete_consultant(999)
        assert result is False


class TestSearchConsultants:
    """Tests pour search_consultants"""
    
    @patch('app.database.database.Session')
    def test_search_consultants_found(self, mock_session):
        """Test recherche avec résultats"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(nom="Dupont")
        mock_db.query.return_value.filter.return_value.all.return_value = [consultant]
        
        result = ConsultantService.search_consultants("Dupont")
        assert len(result) == 1
    
    @patch('app.database.database.Session')
    def test_search_consultants_not_found(self, mock_session):
        """Test recherche sans résultat"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        result = ConsultantService.search_consultants("Inexistant")
        assert len(result) == 0


class TestCreateConsultant:
    """Tests pour create_consultant"""
    
    @patch('app.database.database.Session')
    def test_create_consultant_success(self, mock_session):
        """Test création consultant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@test.com"
        }
        
        result = ConsultantService.create_consultant(data)
        assert result is True
    
    @patch('app.database.database.Session')
    def test_create_consultant_minimal(self, mock_session):
        """Test création avec données minimales"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        data = {"nom": "Dupont", "prenom": "Jean"}
        result = ConsultantService.create_consultant(data)
        assert result is True


class TestGetAllConsultants:
    """Tests pour get_all_consultants"""
    
    @patch('app.database.database.Session')
    def test_get_all_consultants_page1(self, mock_session):
        """Test page 1"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultants = [Mock(id=i) for i in range(10)]
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = consultants
        
        result = ConsultantService.get_all_consultants(page=1, per_page=10)
        assert isinstance(result, list)
    
    @patch('app.database.database.Session')
    def test_get_all_consultants_page2(self, mock_session):
        """Test page 2"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultants = [Mock(id=i) for i in range(10, 20)]
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = consultants
        
        result = ConsultantService.get_all_consultants(page=2, per_page=10)
        assert isinstance(result, list)


class TestConsultantStatistics:
    """Tests pour get_consultants_count"""
    
    @patch('app.database.database.Session')
    def test_get_consultants_count(self, mock_session):
        """Test comptage consultants"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.count.return_value = 15
        
        result = ConsultantService.get_consultants_count()
        assert result == 15
    
    @patch('app.database.database.Session')
    def test_get_consultants_count_zero(self, mock_session):
        """Test comptage zéro"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.count.return_value = 0
        
        result = ConsultantService.get_consultants_count()
        assert result == 0


class TestGetConsultantByEmail:
    """Tests pour get_consultant_by_email"""
    
    @patch('app.database.database.Session')
    def test_get_consultant_by_email_found(self, mock_session):
        """Test recherche par email existant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(email="test@test.com")
        mock_db.query.return_value.filter.return_value.first.return_value = consultant
        
        result = ConsultantService.get_consultant_by_email("test@test.com")
        assert result is not None
    
    @patch('app.database.database.Session')
    def test_get_consultant_by_email_not_found(self, mock_session):
        """Test email inexistant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = ConsultantService.get_consultant_by_email("inexistant@test.com")
        assert result is None


class TestEdgeCases:
    """Tests cas limites"""
    
    @patch('app.database.database.Session')
    def test_update_consultant_empty_data(self, mock_session):
        """Test mise à jour avec dict vide"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        consultant = Mock(id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = consultant
        
        result = ConsultantService.update_consultant(1, {})
        assert result is True
    
    @patch('app.database.database.Session')
    def test_get_all_consultants_empty(self, mock_session):
        """Test sans consultants"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        result = ConsultantService.get_all_consultants()
        assert isinstance(result, list)
        assert len(result) == 0
