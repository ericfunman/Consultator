"""
Tests Phase 60: BusinessManagerService - CORRECTION POUR OPTION A
Objectif: Passer de 48.4% à 75%+ de coverage
Ciblage: 32 lignes manquantes dans business_manager_service.py
Fix: Clear cache Streamlit + Mocks corrects
"""
import unittest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
import pytest

# Import du service
from app.services.business_manager_service import BusinessManagerService
from app.database.models import BusinessManager, ConsultantBusinessManager
from sqlalchemy.exc import SQLAlchemyError


class TestBusinessManagerServicePhase60(unittest.TestCase):
    """Tests corrigés pour BusinessManagerService"""

    def setUp(self):
        """Setup avant chaque test - Clear cache Streamlit"""
        # Clear tous les caches Streamlit pour éviter interférences
        try:
            BusinessManagerService.get_all_business_managers.clear()
            BusinessManagerService.search_business_managers.clear()
            BusinessManagerService.get_business_managers_count.clear()
        except AttributeError:
            pass  # Si pas de cache, pas grave

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_all_business_managers_with_multiple_bm(self, mock_session):
        """Test récupération de tous les BM avec plusieurs résultats"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock 2 Business Managers
        mock_bm1 = Mock(spec=BusinessManager)
        mock_bm1.id = 1
        mock_bm1.prenom = "Jean"
        mock_bm1.nom = "Dupont"
        mock_bm1.email = "jean.dupont@test.com"
        mock_bm1.telephone = "0601020304"
        mock_bm1.actif = True
        mock_bm1.date_creation = datetime(2024, 1, 1)
        mock_bm1.notes = "Test notes 1"
        
        mock_bm2 = Mock(spec=BusinessManager)
        mock_bm2.id = 2
        mock_bm2.prenom = "Marie"
        mock_bm2.nom = "Martin"
        mock_bm2.email = "marie.martin@test.com"
        mock_bm2.telephone = "0602030405"
        mock_bm2.actif = True
        mock_bm2.date_creation = datetime(2024, 2, 1)
        mock_bm2.notes = None
        
        # Mock query pour BusinessManager.query().all()
        mock_bm_query = MagicMock()
        mock_bm_query.all.return_value = [mock_bm1, mock_bm2]
        
        # Mock query pour ConsultantBusinessManager count
        mock_count_query = MagicMock()
        mock_count_query.filter.return_value.count.return_value = 5
        
        # Configuration du mock session.query() avec 2 appels différents
        mock_db.query.side_effect = lambda model: (
            mock_bm_query if model == BusinessManager else mock_count_query
        )
        
        # Act
        result = BusinessManagerService.get_all_business_managers()
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        
        # Vérifier structure du premier BM
        bm1 = result[0]
        assert bm1["id"] == 1
        assert bm1["prenom"] == "Jean"
        assert bm1["nom"] == "Dupont"
        assert bm1["email"] == "jean.dupont@test.com"
        assert bm1["telephone"] == "0601020304"
        assert bm1["actif"] is True
        assert "consultants_count" in bm1
        assert bm1["consultants_count"] == 5
        assert bm1["date_creation"] == datetime(2024, 1, 1)
        assert bm1["notes"] == "Test notes 1"
        
        # Vérifier que query() a été appelé
        assert mock_db.query.call_count >= 2  # Au moins 2 fois (BM + count pour chaque)

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_all_business_managers_empty(self, mock_session):
        """Test récupération BM avec liste vide"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = MagicMock()
        mock_query.all.return_value = []
        mock_db.query.return_value = mock_query
        
        # Act
        result = BusinessManagerService.get_all_business_managers()
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_all_business_managers_sql_error(self, mock_session):
        """Test récupération BM avec erreur SQLAlchemy"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = SQLAlchemyError("Database connection failed")
        
        # Act
        result = BusinessManagerService.get_all_business_managers()
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.services.business_manager_service.get_database_session')
    def test_search_business_managers_by_nom(self, mock_session):
        """Test recherche BM par nom"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock(spec=BusinessManager)
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        mock_bm.email = "jean@test.com"
        mock_bm.telephone = "0601020304"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""
        
        # Mock query chain
        mock_bm_query = MagicMock()
        mock_bm_query.filter.return_value.all.return_value = [mock_bm]
        
        mock_count_query = MagicMock()
        mock_count_query.filter.return_value.count.return_value = 3
        
        mock_db.query.side_effect = lambda model: (
            mock_bm_query if model == BusinessManager else mock_count_query
        )
        
        # Act
        result = BusinessManagerService.search_business_managers("Dupont")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"
        assert result[0]["consultants_count"] == 3

    @patch('app.services.business_manager_service.get_database_session')
    def test_search_business_managers_by_prenom(self, mock_session):
        """Test recherche BM par prénom"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock(spec=BusinessManager)
        mock_bm.id = 2
        mock_bm.prenom = "Sophie"
        mock_bm.nom = "Bernard"
        mock_bm.email = "sophie@test.com"
        mock_bm.telephone = "0602"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = None
        
        mock_bm_query = MagicMock()
        mock_bm_query.filter.return_value.all.return_value = [mock_bm]
        
        mock_count_query = MagicMock()
        mock_count_query.filter.return_value.count.return_value = 7
        
        mock_db.query.side_effect = lambda model: (
            mock_bm_query if model == BusinessManager else mock_count_query
        )
        
        # Act
        result = BusinessManagerService.search_business_managers("Sophie")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["prenom"] == "Sophie"

    @patch('app.services.business_manager_service.get_database_session')
    def test_search_business_managers_by_email(self, mock_session):
        """Test recherche BM par email"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock(spec=BusinessManager)
        mock_bm.id = 3
        mock_bm.prenom = "Paul"
        mock_bm.nom = "Durand"
        mock_bm.email = "paul.durand@example.com"
        mock_bm.telephone = "0603"
        mock_bm.actif = False
        mock_bm.date_creation = datetime(2023, 5, 10)
        mock_bm.notes = "Important"
        
        mock_bm_query = MagicMock()
        mock_bm_query.filter.return_value.all.return_value = [mock_bm]
        
        mock_count_query = MagicMock()
        mock_count_query.filter.return_value.count.return_value = 2
        
        mock_db.query.side_effect = lambda model: (
            mock_bm_query if model == BusinessManager else mock_count_query
        )
        
        # Act
        result = BusinessManagerService.search_business_managers("paul.durand")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["email"] == "paul.durand@example.com"
        assert result[0]["actif"] is False

    @patch('app.services.business_manager_service.get_database_session')
    def test_search_business_managers_empty_term(self, mock_session):
        """Test recherche BM avec terme vide (retourne tous)"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm_query = MagicMock()
        mock_bm_query.all.return_value = []
        mock_db.query.return_value = mock_bm_query
        
        # Act
        result = BusinessManagerService.search_business_managers("")
        
        # Assert
        assert isinstance(result, list)
        # Avec terme vide, le filtre n'est pas appliqué, donc query.all() est appelé
        mock_bm_query.all.assert_called_once()

    @patch('app.services.business_manager_service.get_database_session')
    def test_search_business_managers_no_results(self, mock_session):
        """Test recherche BM sans résultats"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm_query = MagicMock()
        mock_bm_query.filter.return_value.all.return_value = []
        mock_db.query.return_value = mock_bm_query
        
        # Act
        result = BusinessManagerService.search_business_managers("NonExistant12345")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.services.business_manager_service.get_database_session')
    def test_search_business_managers_sql_error(self, mock_session):
        """Test recherche BM avec erreur SQL"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = SQLAlchemyError("Search failed")
        
        # Act
        result = BusinessManagerService.search_business_managers("Test")
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_business_managers_count_positive(self, mock_session):
        """Test comptage BM avec résultat positif"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = MagicMock()
        mock_query.count.return_value = 42
        mock_db.query.return_value = mock_query
        
        # Act
        result = BusinessManagerService.get_business_managers_count()
        
        # Assert
        assert isinstance(result, int)
        assert result == 42

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_business_managers_count_zero(self, mock_session):
        """Test comptage BM avec zéro résultats"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = MagicMock()
        mock_query.count.return_value = 0
        mock_db.query.return_value = mock_query
        
        # Act
        result = BusinessManagerService.get_business_managers_count()
        
        # Assert
        assert result == 0

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_business_managers_count_sql_error(self, mock_session):
        """Test comptage BM avec erreur SQL"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = SQLAlchemyError("Count failed")
        
        # Act
        result = BusinessManagerService.get_business_managers_count()
        
        # Assert
        assert result == 0

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_business_manager_by_id_found(self, mock_session):
        """Test récupération BM par ID existant"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock(spec=BusinessManager)
        mock_bm.id = 10
        mock_bm.nom = "Dupont"
        mock_bm.prenom = "Jean"
        mock_bm.email = "jean.dupont@test.com"
        
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = mock_bm
        mock_db.query.return_value = mock_query
        
        # Act
        result = BusinessManagerService.get_business_manager_by_id(10)
        
        # Assert
        assert result is not None
        assert result.id == 10
        assert result.nom == "Dupont"

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_business_manager_by_id_not_found(self, mock_session):
        """Test récupération BM par ID inexistant"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_db.query.return_value = mock_query
        
        # Act
        result = BusinessManagerService.get_business_manager_by_id(99999)
        
        # Assert
        assert result is None

    @patch('app.services.business_manager_service.get_database_session')
    def test_get_business_manager_by_id_sql_error(self, mock_session):
        """Test récupération BM par ID avec erreur SQL"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.side_effect = SQLAlchemyError("Get by ID failed")
        
        # Act
        result = BusinessManagerService.get_business_manager_by_id(1)
        
        # Assert
        assert result is None

    @patch('app.services.business_manager_service.get_database_session')
    def test_consultants_count_with_date_fin_none_filter(self, mock_session):
        """Test que le comptage consultants filtre bien date_fin IS NULL (actifs)"""
        # Arrange
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_bm = Mock(spec=BusinessManager)
        mock_bm.id = 1
        mock_bm.prenom = "Test"
        mock_bm.nom = "User"
        mock_bm.email = "test@test.com"
        mock_bm.telephone = "0601"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""
        
        mock_bm_query = MagicMock()
        mock_bm_query.all.return_value = [mock_bm]
        
        # Mock count avec tracking du filtre
        mock_count_query = MagicMock()
        mock_filter_chain = MagicMock()
        mock_filter_chain.count.return_value = 8
        mock_count_query.filter.return_value = mock_filter_chain
        
        mock_db.query.side_effect = lambda model: (
            mock_bm_query if model == BusinessManager else mock_count_query
        )
        
        # Act
        result = BusinessManagerService.get_all_business_managers()
        
        # Assert
        assert len(result) == 1
        assert result[0]["consultants_count"] == 8
        # Vérifier que filter a été appelé (pour date_fin.is_(None))
        mock_count_query.filter.assert_called()


if __name__ == "__main__":
    unittest.main()
