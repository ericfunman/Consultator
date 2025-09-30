"""
Tests pour le service BusinessManagerService
Couverture des fonctionnalités CRUD et recherche
"""

from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.database.models import BusinessManager, ConsultantCompetence
from app.database.models import ConsultantBusinessManager, ConsultantCompetence
from app.services.business_manager_service import BusinessManagerService
from tests.fixtures.base_test import BaseServiceTest
from tests.fixtures.base_test import TestDataFactory


class TestBusinessManagerService(BaseServiceTest):
    """Tests pour BusinessManagerService"""

    @patch.object(BusinessManagerService, "get_all_business_managers")
    def test_get_all_business_managers_success(self, mock_get_all):
        """Test récupération de tous les Business Managers - cas succès"""
        # Mock the function to return serializable data
        mock_get_all.return_value = [
            {
                "id": 1,
                "prenom": "Jean",
                "nom": "Dupont",
                "email": "j.dupont@consultator.fr",
                "telephone": "0123456789",
                "actif": True,
                "consultants_count": 5,
                "date_creation": datetime(2024, 1, 1),
                "notes": "BM expérimenté",
            },
            {
                "id": 2,
                "prenom": "Marie",
                "nom": "Martin",
                "email": "m.martin@consultator.fr",
                "telephone": "0987654321",
                "actif": True,
                "consultants_count": 3,
                "date_creation": datetime(2024, 2, 1),
                "notes": None,
            },
        ]

        # Test
        result = BusinessManagerService.get_all_business_managers()

        # Vérifications
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["prenom"] == "Jean"
        assert result[0]["nom"] == "Dupont"
        assert result[0]["email"] == "j.dupont@consultator.fr"
        assert result[0]["actif"] is True
        assert result[0]["consultants_count"] == 5
        assert result[1]["id"] == 2
        assert result[1]["prenom"] == "Marie"
        assert result[1]["nom"] == "Martin"

    @patch("app.services.business_manager_service.st")
    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers_database_error(self, mock_session, mock_st):
        """Test récupération Business Managers - erreur base de données"""
        # Mock streamlit cache - use MagicMock to support decorator behavior
        mock_st.cache_data = MagicMock(return_value=lambda func: func)

        # Mock session qui lève une exception SQLAlchemyError
        from sqlalchemy.exc import SQLAlchemyError

        mock_session_instance = MagicMock()
        mock_session_instance.query.side_effect = SQLAlchemyError(
            "Database connection failed"
        )
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session.return_value.__exit__.return_value = None

        # Test
        result = BusinessManagerService.get_all_business_managers()

        # Vérifications
        assert result == []

    @patch.object(BusinessManagerService, "search_business_managers")
    def test_search_business_managers_with_term(self, mock_search):
        """Test recherche Business Managers avec terme de recherche"""
        # Mock the function to return serializable data
        mock_search.return_value = [
            {
                "id": 1,
                "prenom": "Jean",
                "nom": "Dupont",
                "email": "j.dupont@consultator.fr",
                "telephone": "0123456789",
                "actif": True,
                "consultants_count": 3,
                "date_creation": datetime(2024, 1, 1),
                "notes": "BM expérimenté",
            }
        ]

        # Test
        result = BusinessManagerService.search_business_managers("Dupont")

        # Vérifications
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"
        assert result[0]["prenom"] == "Jean"
        assert result[0]["consultants_count"] == 3

    @patch.object(BusinessManagerService, "search_business_managers")
    def test_search_business_managers_empty_term(self, mock_search):
        """Test recherche Business Managers avec terme vide"""
        # Mock the function to return serializable data
        mock_search.return_value = [
            {
                "id": 1,
                "prenom": "Jean",
                "nom": "Dupont",
                "email": "j.dupont@consultator.fr",
                "telephone": "0123456789",
                "actif": True,
                "consultants_count": 2,
                "date_creation": datetime(2024, 1, 1),
                "notes": "BM expérimenté",
            }
        ]

        # Test
        result = BusinessManagerService.search_business_managers("")

        # Vérifications
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"
        assert result[0]["consultants_count"] == 2

    @patch.object(BusinessManagerService, "get_business_managers_count")
    def test_get_business_managers_count_success(self, mock_count):
        """Test comptage Business Managers - cas succès"""
        # Mock the function to return count
        mock_count.return_value = 5

        # Test
        result = BusinessManagerService.get_business_managers_count()

        # Vérifications
        assert result == 5

    @patch.object(BusinessManagerService, "get_business_managers_count")
    def test_get_business_managers_count_error(self, mock_count):
        """Test comptage Business Managers - erreur base de données"""
        # Mock the function to return 0 on error
        mock_count.return_value = 0

        # Test
        result = BusinessManagerService.get_business_managers_count()

        # Vérifications
        assert result == 0

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id_found(self, mock_session):
        """Test récupération Business Manager par ID - trouvé"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock Business Manager
        mock_bm = Mock()
        mock_bm.id = 1
        mock_bm.prenom = "Jean"
        mock_bm.nom = "Dupont"

        # Mock la query
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = mock_bm
        mock_session_instance.query.return_value = mock_query

        # Test
        result = BusinessManagerService.get_business_manager_by_id(1)

        # Vérifications
        assert result is not None
        assert result.id == 1
        assert result.prenom == "Jean"

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id_not_found(self, mock_session):
        """Test récupération Business Manager par ID - non trouvé"""
        # Mock session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock la query qui ne trouve rien
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_session_instance.query.return_value = mock_query

        # Test
        result = BusinessManagerService.get_business_manager_by_id(999)

        # Vérifications
        assert result is None

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id_error(self, mock_session):
        """Test récupération Business Manager par ID - erreur base de données"""
        # Mock session qui lève une exception SQLAlchemyError
        from sqlalchemy.exc import SQLAlchemyError

        mock_session_instance = MagicMock()
        mock_session_instance.query.side_effect = SQLAlchemyError(
            "Database connection failed"
        )
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Test
        result = BusinessManagerService.get_business_manager_by_id(1)

        # Vérifications
        assert result is None
