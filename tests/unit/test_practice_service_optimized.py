"""
Tests de couverture optimisés pour practice_service.py - Version corrigée
Tests robustes avec bon mocking pour atteindre 95% de couverture
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.practice_service import PracticeService


class TestPracticeServiceOptimized:
    """Tests optimisés pour PracticeService avec mocking corrigé"""

    def setup_method(self):
        """Setup pour chaque test"""
        self.mock_practice = Mock()
        self.mock_practice.id = 1
        self.mock_practice.nom = "Data Engineering"
        self.mock_practice.description = "Practice Data Engineering"
        self.mock_practice.responsable = "Jean Dupont"
        self.mock_practice.actif = True

        self.mock_consultant = Mock()
        self.mock_consultant.id = 1
        self.mock_consultant.nom = "Dupont"
        self.mock_consultant.prenom = "Jean"
        self.mock_consultant.email = "jean.dupont@example.com"
        self.mock_consultant.salaire_actuel = 50000
        self.mock_consultant.practice_id = 1

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_all_practices_success(self, mock_st_error, mock_session):
        """Test récupération de toutes les practices avec succès"""
        # Mock session avec context manager
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [self.mock_practice]
        
        # Execution
        result = PracticeService.get_all_practices()
        
        # Vérifications
        assert result == [self.mock_practice]
        mock_st_error.assert_not_called()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_all_practices_error(self, mock_st_error, mock_session):
        """Test récupération practices avec erreur DB"""
        # Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.side_effect = Exception("DB Error")
        
        # Execution
        result = PracticeService.get_all_practices()
        
        # Vérifications
        assert result == []
        mock_st_error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_practice_by_id_success(self, mock_st_error, mock_session):
        """Test récupération practice par ID avec succès"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice
        
        result = PracticeService.get_practice_by_id(1)
        
        assert result == self.mock_practice
        mock_st_error.assert_not_called()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_practice_by_id_not_found(self, mock_st_error, mock_session):
        """Test récupération practice par ID non trouvé"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = PracticeService.get_practice_by_id(999)
        
        assert result is None
        mock_st_error.assert_not_called()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_practice_by_id_error(self, mock_st_error, mock_session):
        """Test récupération practice par ID avec erreur"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.side_effect = Exception("DB Error")
        
        result = PracticeService.get_practice_by_id(1)
        
        assert result is None
        mock_st_error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_create_practice_success(self, mock_st_error, mock_st_success, mock_session):
        """Test création practice avec succès"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        
        # Mock de la nouvelle practice créée
        from database.models import Practice
        with patch('app.services.practice_service.Practice') as mock_practice_class:
            mock_new_practice = Mock()
            mock_practice_class.return_value = mock_new_practice
            
            data = {
                "nom": "New Practice",
                "description": "Description",
                "responsable": "Manager"
            }
            
            result = PracticeService.create_practice(data)
            
            assert result is True
            mock_db.add.assert_called_once_with(mock_new_practice)
            mock_db.commit.assert_called_once()
            mock_st_success.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_create_practice_error(self, mock_st_error, mock_st_success, mock_session):
        """Test création practice avec erreur"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.add.side_effect = Exception("Test error")
        
        from database.models import Practice
        with patch('app.services.practice_service.Practice'):
            data = {"nom": "Practice", "description": "Desc", "responsable": "Manager"}
            
            result = PracticeService.create_practice(data)
            
            assert result is False
            mock_db.rollback.assert_called_once()
            mock_st_error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_update_practice_success(self, mock_st_error, mock_st_success, mock_session):
        """Test mise à jour practice avec succès"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice
        
        data = {"nom": "Updated Name", "description": "Updated Desc"}
        
        result = PracticeService.update_practice(1, data)
        
        assert result is True
        assert self.mock_practice.nom == "Updated Name"
        assert self.mock_practice.description == "Updated Desc"
        mock_db.commit.assert_called_once()
        mock_st_success.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_update_practice_not_found(self, mock_st_error, mock_st_success, mock_session):
        """Test mise à jour practice non trouvée"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        data = {"nom": "Updated Name"}
        
        result = PracticeService.update_practice(999, data)
        
        assert result is False
        mock_st_error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_update_practice_error(self, mock_st_error, mock_st_success, mock_session):
        """Test mise à jour practice avec erreur DB"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice
        mock_db.commit.side_effect = Exception("DB Error")
        
        data = {"nom": "Updated Name"}
        
        result = PracticeService.update_practice(1, data)
        
        assert result is False
        mock_db.rollback.assert_called_once()
        mock_st_error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_consultants_by_practice_success(self, mock_st_error, mock_session):
        """Test récupération consultants par practice avec succès"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.filter.return_value.all.return_value = [self.mock_consultant]
        
        result = PracticeService.get_consultants_by_practice(1)
        
        assert result == [self.mock_consultant]
        mock_st_error.assert_not_called()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_consultants_by_practice_empty(self, mock_st_error, mock_session):
        """Test récupération consultants practice vide"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        result = PracticeService.get_consultants_by_practice(1)
        
        assert result == []
        mock_st_error.assert_not_called()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_consultants_by_practice_error(self, mock_st_error, mock_session):
        """Test récupération consultants avec erreur DB"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.side_effect = Exception("DB Error")
        
        result = PracticeService.get_consultants_by_practice(1)
        
        assert result == []
        mock_st_error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_practice_statistics_success(self, mock_st_error, mock_session):
        """Test récupération statistiques practice avec succès"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        
        # Mock consultants count
        mock_db.query.return_value.filter.return_value.count.return_value = 5
        # Mock avg salary
        mock_db.query.return_value.filter.return_value.scalar.return_value = 55000
        
        result = PracticeService.get_practice_statistics(1)
        
        assert result["total_consultants"] == 5
        assert result["salaire_moyen"] == 55000
        mock_st_error.assert_not_called()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_practice_statistics_no_consultants(self, mock_st_error, mock_session):
        """Test statistiques practice sans consultants"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        
        # Mock zero consultants
        mock_db.query.return_value.filter.return_value.count.return_value = 0
        mock_db.query.return_value.filter.return_value.scalar.return_value = None
        
        result = PracticeService.get_practice_statistics(1)
        
        assert result["total_consultants"] == 0
        assert result["salaire_moyen"] == 0
        mock_st_error.assert_not_called()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_get_practice_statistics_error(self, mock_st_error, mock_session):
        """Test statistiques practice avec erreur DB"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.side_effect = Exception("DB Error")
        
        result = PracticeService.get_practice_statistics(1)
        
        assert result["total_consultants"] == 0
        assert result["salaire_moyen"] == 0
        mock_st_error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_init_default_practices_success(self, mock_st_error, mock_st_success, mock_session):
        """Test initialisation practices par défaut avec succès"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        
        # Mock count = 0 (pas de practices existantes)
        mock_db.query.return_value.count.return_value = 0
        
        from database.models import Practice
        with patch('app.services.practice_service.Practice') as mock_practice_class:
            mock_new_practices = [Mock(), Mock(), Mock()]
            mock_practice_class.side_effect = mock_new_practices
            
            result = PracticeService.init_default_practices()
            
            assert result is True
            # Vérifier que 3 practices ont été ajoutées
            assert mock_db.add.call_count == 3
            mock_db.commit.assert_called_once()
            mock_st_success.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_init_default_practices_already_exist(self, mock_st_error, mock_st_success, mock_session):
        """Test initialisation practices déjà existantes"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        
        # Mock count > 0 (practices déjà existantes)
        mock_db.query.return_value.count.return_value = 5
        
        result = PracticeService.init_default_practices()
        
        assert result is True
        mock_db.add.assert_not_called()
        mock_st_success.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_init_default_practices_error(self, mock_st_error, mock_st_success, mock_session):
        """Test initialisation practices avec erreur DB"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        mock_db.query.return_value.count.return_value = 0
        mock_db.add.side_effect = Exception("DB Error")
        
        from database.models import Practice
        with patch('app.services.practice_service.Practice'):
            result = PracticeService.init_default_practices()
            
            assert result is False
            mock_db.rollback.assert_called_once()
            mock_st_error.assert_called_once()

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_practice_service_edge_cases(self, mock_st_error, mock_session):
        """Test cas limites et branches supplémentaires"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        
        # Test get_practice_by_id avec ID None
        result = PracticeService.get_practice_by_id(None)
        assert result is None
        
        # Test get_consultants_by_practice avec ID None
        result = PracticeService.get_consultants_by_practice(None)
        assert result == []

    @patch('app.services.practice_service.get_database_session')
    def test_practice_service_context_manager_error(self, mock_session):
        """Test erreur dans context manager"""
        # Mock erreur dans l'ouverture de session
        mock_session.side_effect = Exception("Connection error")
        
        result = PracticeService.get_all_practices()
        assert result == []

    def test_practice_service_constants(self):
        """Test des constantes et attributs de classe"""
        # Vérifier que la classe existe et a les bonnes méthodes
        assert hasattr(PracticeService, 'get_all_practices')
        assert hasattr(PracticeService, 'get_practice_by_id')
        assert hasattr(PracticeService, 'create_practice')
        assert hasattr(PracticeService, 'update_practice')
        assert hasattr(PracticeService, 'get_consultants_by_practice')
        assert hasattr(PracticeService, 'get_practice_statistics')
        assert hasattr(PracticeService, 'init_default_practices')

    @patch('app.services.practice_service.get_database_session')
    @patch('streamlit.error')
    def test_complex_query_scenarios(self, mock_st_error, mock_session):
        """Test scénarios de requêtes complexes"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_session.return_value.__exit__.return_value = None
        
        # Test avec multiples practices
        mock_practices = [Mock() for _ in range(10)]
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = mock_practices
        
        result = PracticeService.get_all_practices()
        assert len(result) == 10
        
        # Test avec filtres sur consultants
        mock_consultants = [Mock() for _ in range(3)]
        for i, consultant in enumerate(mock_consultants):
            consultant.id = i + 1
            consultant.practice_id = 1
            
        mock_db.query.return_value.filter.return_value.all.return_value = mock_consultants
        
        result = PracticeService.get_consultants_by_practice(1)
        assert len(result) == 3