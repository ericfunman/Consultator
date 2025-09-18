"""
Tests de couverture ciblés pour practice_service.py
Tests réalistes basés sur le code existant
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.practice_service import PracticeService


class TestPracticeServiceCoverage:
    """Tests pour améliorer la couverture du PracticeService"""

    def setup_method(self):
        """Setup pour chaque test"""
        self.mock_practice = Mock()
        self.mock_practice.id = 1
        self.mock_practice.nom = "Data Engineering"
        self.mock_practice.description = "Practice Data Engineering"
        self.mock_practice.responsable = "Jean Dupont"
        self.mock_practice.actif = True

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_all_practices_success(self, mock_st_error, mock_session):
        """Test récupération de toutes les practices"""
        # Mock session directe (pas de context manager)
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [self.mock_practice]
        
        # Execution
        result = PracticeService.get_all_practices()
        
        # Vérifications
        assert result == [self.mock_practice]
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_all_practices_error(self, mock_st_error, mock_session):
        """Test récupération practices avec erreur"""
        # Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.side_effect = Exception("DB Error")
        
        # Execution
        result = PracticeService.get_all_practices()
        
        # Vérifications
        assert result == []
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_practice_by_id_found(self, mock_st_error, mock_session):
        """Test récupération practice par ID - trouvée"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice
        
        # Execution
        result = PracticeService.get_practice_by_id(1)
        
        # Vérifications
        assert result == self.mock_practice
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_practice_by_id_error(self, mock_st_error, mock_session):
        """Test récupération practice par ID avec erreur"""
        # Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.side_effect = Exception("DB Error")
        
        # Execution
        result = PracticeService.get_practice_by_id(1)
        
        # Vérifications
        assert result is None
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_practice_by_name_found(self, mock_st_error, mock_session):
        """Test récupération practice par nom - trouvée"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice
        
        # Execution
        result = PracticeService.get_practice_by_name("Data Engineering")
        
        # Vérifications
        assert result == self.mock_practice
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    @patch('streamlit.success')
    def test_create_practice_success(self, mock_st_success, mock_st_error, mock_session):
        """Test création practice réussie"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None  # Pas d'existant
        
        # Mock new practice
        new_practice = Mock()
        
        # Execution
        result = PracticeService.create_practice(
            nom="Test Practice",
            description="Description test",
            responsable="Test Manager"
        )
        
        # Vérifications
        mock_db.add.assert_called()
        mock_db.commit.assert_called()
        mock_st_success.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_create_practice_already_exists(self, mock_st_error, mock_session):
        """Test création practice - déjà existante"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice  # Déjà existant
        
        # Execution
        result = PracticeService.create_practice(
            nom="Test Practice",
            description="Description test"
        )
        
        # Vérifications
        assert result is None
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_create_practice_error(self, mock_st_error, mock_session):
        """Test création practice avec erreur"""
        # Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_db.add.side_effect = Exception("Test error")
        
        # Execution
        result = PracticeService.create_practice(
            nom="Test Practice",
            description="Description test"
        )
        
        # Vérifications
        assert result is None
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    @patch('streamlit.success')
    def test_update_practice_success(self, mock_st_success, mock_st_error, mock_session):
        """Test mise à jour practice réussie"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice
        
        # Execution
        result = PracticeService.update_practice(1, nom="New Name")
        
        # Vérifications
        assert result is True
        mock_db.commit.assert_called()
        mock_st_success.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_update_practice_not_found(self, mock_st_error, mock_session):
        """Test mise à jour practice non trouvée"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Execution
        result = PracticeService.update_practice(999, nom="New Name")
        
        # Vérifications
        assert result is False
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_update_practice_error(self, mock_st_error, mock_session):
        """Test mise à jour practice avec erreur"""
        # Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice
        mock_db.commit.side_effect = Exception("DB Error")
        
        # Execution
        result = PracticeService.update_practice(1, nom="New Name")
        
        # Vérifications
        assert result is False
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_consultants_by_practice_specific(self, mock_st_error, mock_session):
        """Test récupération consultants par practice spécifique"""
        # Mock consultants
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"
        mock_consultant.prenom = "Jean"
        
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.options.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_consultant]
        mock_db.query.return_value.filter.return_value.first.return_value = self.mock_practice
        
        # Execution
        result = PracticeService.get_consultants_by_practice(1)
        
        # Vérifications
        assert isinstance(result, dict)
        assert "Data Engineering" in result
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_consultants_by_practice_all(self, mock_st_error, mock_session):
        """Test récupération tous consultants par practice"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.all.return_value = [self.mock_practice]
        mock_db.query.return_value.options.return_value.filter.return_value.order_by.return_value.all.return_value = []
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
        
        # Execution
        result = PracticeService.get_consultants_by_practice()
        
        # Vérifications
        assert isinstance(result, dict)
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_consultants_by_practice_error(self, mock_st_error, mock_session):
        """Test récupération consultants avec erreur"""
        # Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.side_effect = Exception("DB Error")
        
        # Execution
        result = PracticeService.get_consultants_by_practice(1)
        
        # Vérifications
        assert result == {}
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    @patch('streamlit.success')
    def test_assign_consultant_to_practice_success(self, mock_st_success, mock_st_error, mock_session):
        """Test assignation consultant à practice réussie"""
        # Mock consultant et practice
        mock_consultant = Mock()
        mock_practice = Mock()
        mock_practice.nom = "Data"
        
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        
        # Premier appel pour consultant, deuxième pour practice
        mock_db.query.return_value.filter.return_value.first.side_effect = [mock_consultant, mock_practice]
        
        # Execution
        result = PracticeService.assign_consultant_to_practice(1, 1)
        
        # Vérifications
        assert result is True
        mock_db.commit.assert_called()
        mock_st_success.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_assign_consultant_to_practice_consultant_not_found(self, mock_st_error, mock_session):
        """Test assignation consultant non trouvé"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None  # Consultant not found
        
        # Execution
        result = PracticeService.assign_consultant_to_practice(999, 1)
        
        # Vérifications
        assert result is False
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_assign_consultant_practice_not_found(self, mock_st_error, mock_session):
        """Test assignation practice non trouvée"""
        # Mock consultant trouvé, practice non trouvée
        mock_consultant = Mock()
        
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        
        # Premier appel pour consultant (trouvé), deuxième pour practice (non trouvée)
        mock_db.query.return_value.filter.return_value.first.side_effect = [mock_consultant, None]
        
        # Execution
        result = PracticeService.assign_consultant_to_practice(1, 999)
        
        # Vérifications
        assert result is False
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_practice_statistics_success(self, mock_st_error, mock_session):
        """Test récupération statistiques practices avec succès"""
        # Mock practices
        mock_practices = [self.mock_practice]
        
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.filter.return_value.all.return_value = mock_practices
        mock_db.query.return_value.filter.return_value.count.return_value = 5
        mock_db.query.return_value.count.return_value = 2
        
        # Execution
        result = PracticeService.get_practice_statistics()
        
        # Vérifications
        assert isinstance(result, dict)
        assert "total_practices" in result
        assert "practices_detail" in result
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_get_practice_statistics_error(self, mock_st_error, mock_session):
        """Test récupération statistiques avec erreur"""
        # Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.side_effect = Exception("DB Error")
        
        # Execution
        result = PracticeService.get_practice_statistics()
        
        # Vérifications
        assert result["total_practices"] == 0
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    @patch('streamlit.success')
    def test_init_default_practices_success(self, mock_st_success, mock_st_error, mock_session):
        """Test initialisation practices par défaut"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.all.return_value = []  # Pas de practices existantes
        
        # Execution
        PracticeService.init_default_practices()
        
        # Vérifications
        assert mock_db.add.call_count == 2  # Data + Quant
        mock_db.commit.assert_called()
        mock_st_success.assert_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_init_default_practices_already_exist(self, mock_st_error, mock_session):
        """Test initialisation practices par défaut - déjà existantes"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.all.return_value = [self.mock_practice]  # Practices déjà existantes
        
        # Execution
        PracticeService.init_default_practices()
        
        # Vérifications
        mock_db.add.assert_not_called()
        mock_db.close.assert_called()

    @patch('app.services.practice_service.get_session')
    @patch('streamlit.error')
    def test_init_default_practices_error(self, mock_st_error, mock_session):
        """Test initialisation practices avec erreur"""
        # Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.query.return_value.all.return_value = []
        mock_db.add.side_effect = Exception("DB Error")
        
        # Execution
        PracticeService.init_default_practices()
        
        # Vérifications
        mock_st_error.assert_called()
        mock_db.close.assert_called()

    def test_practice_service_static_methods_exist(self):
        """Test que les méthodes statiques existent et sont appelables"""
        # Test d'existence des méthodes
        assert hasattr(PracticeService, 'get_all_practices')
        assert hasattr(PracticeService, 'get_practice_by_id')
        assert hasattr(PracticeService, 'get_practice_by_name')
        assert hasattr(PracticeService, 'create_practice')
        assert hasattr(PracticeService, 'update_practice')
        assert hasattr(PracticeService, 'get_consultants_by_practice')
        assert hasattr(PracticeService, 'assign_consultant_to_practice')
        assert hasattr(PracticeService, 'get_practice_statistics')
        assert hasattr(PracticeService, 'init_default_practices')
        
        # Test que ce sont des méthodes appelables
        assert callable(PracticeService.get_all_practices)
        assert callable(PracticeService.create_practice)
        assert callable(PracticeService.get_practice_statistics)