"""
Tests unitaires pour app/services/business_manager_service.py - Phase 49
Tests complets du service de gestion des Business Managers
"""

from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError


# Patch le cache Streamlit pour éviter les interférences entre tests
@pytest.fixture(autouse=True)
def mock_streamlit_cache():
    """Mock Streamlit cache decorator"""
    with patch("streamlit.cache_data", lambda **kwargs: lambda func: func):
        yield


# Import after patching
from app.services.business_manager_service import BusinessManagerService


# ============================================================================
# Tests get_all_business_managers
# ============================================================================


class TestGetAllBusinessManagers:
    """Tests pour get_all_business_managers"""

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers_success(self, mock_session):
        """Test récupération réussie de tous les BM"""
        # Créer un mock BM
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        mock_bm.email = "jean.dupont@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime(2024, 1, 1)
        mock_bm.notes = "Test notes"

        # Mock session et query
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 3

        # Exécuter
        result = BusinessManagerService.get_all_business_managers()

        # Vérifier
        assert isinstance(result, list)
        assert len(result) == 1
        
        bm_dict = result[0]
        assert bm_dict["id"] == 1
        assert bm_dict["prenom"] == "Jean"
        assert bm_dict["nom"] == "Dupont"
        assert bm_dict["email"] == "jean.dupont@test.com"
        assert bm_dict["telephone"] == "0612345678"
        assert bm_dict["actif"] is True
        assert bm_dict["consultants_count"] == 3
        assert bm_dict["notes"] == "Test notes"

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers_empty(self, mock_session):
        """Test quand aucun BM n'existe"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.all.return_value = []

        result = BusinessManagerService.get_all_business_managers()

        assert isinstance(result, list)
        assert len(result) == 0

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers_multiple(self, mock_session):
        """Test avec plusieurs BM"""
        mock_bm1 = Mock()
        mock_bm1.id = 1
        mock_bm1.prenom = "Jean"
        mock_bm1.nom = "Dupont"
        mock_bm1.email = "jean@test.com"
        mock_bm1.telephone = "0612345678"
        mock_bm1.actif = True
        mock_bm1.date_creation = datetime.now()
        mock_bm1.notes = ""

        mock_bm2 = Mock()
        mock_bm2.id = 2
        mock_bm2.prenom = "Marie"
        mock_bm2.nom = "Martin"
        mock_bm2.email = "marie@test.com"
        mock_bm2.telephone = "0698765432"
        mock_bm2.actif = False
        mock_bm2.date_creation = datetime.now()
        mock_bm2.notes = "Inactif"

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.all.return_value = [mock_bm1, mock_bm2]
        mock_db.query.return_value.filter.return_value.count.return_value = 5

        result = BusinessManagerService.get_all_business_managers()

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2
        assert result[0]["actif"] is True
        assert result[1]["actif"] is False

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers_error(self, mock_session):
        """Test gestion d'erreur SQL"""
        mock_session.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")

        result = BusinessManagerService.get_all_business_managers()

        assert isinstance(result, list)
        assert len(result) == 0

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers_consultants_count_zero(self, mock_session):
        """Test BM sans consultants assignés"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Test"
        mock_bm.nom = "BM"
        mock_bm.email = "test@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 0

        result = BusinessManagerService.get_all_business_managers()

        assert result[0]["consultants_count"] == 0

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers_id_type(self, mock_session):
        """Test que l'ID est bien converti en entier"""
        mock_bm = Mock()
        mock_bm.id = "1"  # String au lieu d'int
        mock_bm.prenom = "Test"
        mock_bm.nom = "BM"
        mock_bm.email = "test@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 0

        result = BusinessManagerService.get_all_business_managers()

        assert isinstance(result[0]["id"], int)


# ============================================================================
# Tests search_business_managers
# ============================================================================


class TestSearchBusinessManagers:
    """Tests pour search_business_managers"""

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_by_nom(self, mock_session):
        """Test recherche par nom"""
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
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 2

        result = BusinessManagerService.search_business_managers("Dupont")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_by_prenom(self, mock_session):
        """Test recherche par prénom"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Marie"
        mock_bm.nom = "Martin"
        mock_bm.email = "marie@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 1

        result = BusinessManagerService.search_business_managers("Marie")

        assert len(result) == 1
        assert result[0]["prenom"] == "Marie"

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_by_email(self, mock_session):
        """Test recherche par email"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Pierre"
        mock_bm.nom = "Durand"
        mock_bm.email = "pierre.durand@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 0

        result = BusinessManagerService.search_business_managers("pierre")

        assert len(result) == 1
        assert "pierre" in result[0]["email"].lower()

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_empty_term(self, mock_session):
        """Test recherche avec terme vide"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Test"
        mock_bm.nom = "BM"
        mock_bm.email = "test@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 0

        result = BusinessManagerService.search_business_managers("")

        # Avec terme vide, devrait retourner tous les BM (pas de filtre)
        assert isinstance(result, list)
        assert len(result) == 1

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_no_results(self, mock_session):
        """Test recherche sans résultats"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = []

        result = BusinessManagerService.search_business_managers("NonExistant")

        assert isinstance(result, list)
        assert len(result) == 0

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_case_insensitive(self, mock_session):
        """Test recherche insensible à la casse"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Sophie"
        mock_bm.nom = "Bernard"
        mock_bm.email = "sophie@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 0

        # Recherche en majuscules
        result = BusinessManagerService.search_business_managers("BERNARD")

        assert len(result) == 1

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_partial_match(self, mock_session):
        """Test recherche partielle"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Alexandre"
        mock_bm.nom = "Dubois"
        mock_bm.email = "alexandre@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 1

        # Recherche partielle
        result = BusinessManagerService.search_business_managers("Alex")

        assert len(result) == 1

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_error(self, mock_session):
        """Test gestion d'erreur lors de la recherche"""
        mock_session.return_value.__enter__.side_effect = SQLAlchemyError("Search error")

        result = BusinessManagerService.search_business_managers("Test")

        assert isinstance(result, list)
        assert len(result) == 0

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_multiple_results(self, mock_session):
        """Test recherche avec plusieurs résultats"""
        mock_bm1 = Mock()
        mock_bm1.id = 1
        mock_bm1.prenom = "Jean"
        mock_bm1.nom = "Dupont"
        mock_bm1.email = "jean@test.com"
        mock_bm1.telephone = "0612345678"
        mock_bm1.actif = True
        mock_bm1.date_creation = datetime.now()
        mock_bm1.notes = ""

        mock_bm2 = Mock()
        mock_bm2.id = 2
        mock_bm2.prenom = "Jeanne"
        mock_bm2.nom = "Martin"
        mock_bm2.email = "jeanne@test.com"
        mock_bm2.telephone = "0698765432"
        mock_bm2.actif = True
        mock_bm2.date_creation = datetime.now()
        mock_bm2.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm1, mock_bm2]
        mock_db.query.return_value.filter.return_value.count.return_value = 0

        result = BusinessManagerService.search_business_managers("Jean")

        assert len(result) == 2


# ============================================================================
# Tests get_business_managers_count
# ============================================================================


class TestGetBusinessManagersCount:
    """Tests pour get_business_managers_count"""

    @patch("app.services.business_manager_service.get_database_session")
    def test_count_success(self, mock_session):
        """Test comptage réussi"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.count.return_value = 15

        result = BusinessManagerService.get_business_managers_count()

        assert result == 15

    @patch("app.services.business_manager_service.get_database_session")
    def test_count_zero(self, mock_session):
        """Test comptage quand aucun BM"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.count.return_value = 0

        result = BusinessManagerService.get_business_managers_count()

        assert result == 0

    @patch("app.services.business_manager_service.get_database_session")
    def test_count_error(self, mock_session):
        """Test gestion d'erreur lors du comptage"""
        mock_session.return_value.__enter__.side_effect = SQLAlchemyError("Count error")

        result = BusinessManagerService.get_business_managers_count()

        assert result == 0

    @patch("app.services.business_manager_service.get_database_session")
    def test_count_large_number(self, mock_session):
        """Test avec grand nombre"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.count.return_value = 1000

        result = BusinessManagerService.get_business_managers_count()

        assert result == 1000


# ============================================================================
# Tests get_business_manager_by_id
# ============================================================================


class TestGetBusinessManagerById:
    """Tests pour get_business_manager_by_id"""

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_by_id_found(self, mock_session):
        """Test récupération par ID existant"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"
        mock_bm.email = "jean@test.com"

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = mock_bm

        result = BusinessManagerService.get_business_manager_by_id(1)

        assert result is not None
        assert result.id == 1
        assert result.prenom == "Jean"

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_by_id_not_found(self, mock_session):
        """Test récupération par ID inexistant"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = BusinessManagerService.get_business_manager_by_id(999)

        assert result is None

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_by_id_error(self, mock_session):
        """Test gestion d'erreur lors de la récupération"""
        mock_session.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")

        result = BusinessManagerService.get_business_manager_by_id(1)

        assert result is None

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_by_id_zero(self, mock_session):
        """Test avec ID 0"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = BusinessManagerService.get_business_manager_by_id(0)

        assert result is None

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_by_id_negative(self, mock_session):
        """Test avec ID négatif"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = BusinessManagerService.get_business_manager_by_id(-1)

        assert result is None


# ============================================================================
# Tests d'intégration
# ============================================================================


class TestIntegration:
    """Tests d'intégration entre les méthodes"""

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_then_get_by_id(self, mock_session):
        """Test récupération de tous puis par ID"""
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
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Pour get_all
        mock_db.query.return_value.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 0
        
        all_bms = BusinessManagerService.get_all_business_managers()
        
        # Pour get_by_id
        mock_db.query.return_value.filter.return_value.first.return_value = mock_bm
        
        first_bm_id = all_bms[0]["id"]
        specific_bm = BusinessManagerService.get_business_manager_by_id(first_bm_id)

        assert specific_bm is not None
        assert specific_bm.id == first_bm_id

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_then_count(self, mock_session):
        """Test recherche puis comptage"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Test"
        mock_bm.nom = "BM"
        mock_bm.email = "test@test.com"
        mock_bm.telephone = "0612345678"
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = ""

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Pour search
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = [mock_bm]
        
        search_results = BusinessManagerService.search_business_managers("Test")
        
        # Pour count
        mock_db.query.return_value.count.return_value = 1
        
        total_count = BusinessManagerService.get_business_managers_count()

        assert len(search_results) <= total_count


# ============================================================================
# Tests de cas limites
# ============================================================================


class TestEdgeCases:
    """Tests des cas limites"""

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_with_special_characters(self, mock_session):
        """Test recherche avec caractères spéciaux"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = []

        # Ne devrait pas crasher avec caractères spéciaux
        result = BusinessManagerService.search_business_managers("O'Brien")

        assert isinstance(result, list)

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_with_sql_injection_attempt(self, mock_session):
        """Test recherche avec tentative d'injection SQL"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = []

        # Ne devrait pas crasher
        result = BusinessManagerService.search_business_managers("'; DROP TABLE --")

        assert isinstance(result, list)

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_with_none_fields(self, mock_session):
        """Test BM avec champs None"""
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Test"
        mock_bm.nom = "BM"
        mock_bm.email = None  # Email None
        mock_bm.telephone = None  # Téléphone None
        mock_bm.actif = True
        mock_bm.date_creation = datetime.now()
        mock_bm.notes = None  # Notes None

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.all.return_value = [mock_bm]
        mock_db.query.return_value.filter.return_value.count.return_value = 0

        result = BusinessManagerService.get_all_business_managers()

        assert len(result) == 1
        assert result[0]["email"] is None
        assert result[0]["telephone"] is None

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_very_long_term(self, mock_session):
        """Test recherche avec terme très long"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_query = mock_db.query.return_value
        mock_filtered = mock_query.filter.return_value
        mock_filtered.all.return_value = []

        long_term = "a" * 1000
        result = BusinessManagerService.search_business_managers(long_term)

        assert isinstance(result, list)
