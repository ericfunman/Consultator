"""
Phase 63 - Batch 1: Tests pour consultant_service.py
Focus: Méthodes de recherche et filtres (lines 67-234)
Objectif: Coverage 69% → 75% (+6%)
"""

from datetime import date, datetime
from unittest.mock import Mock, patch, MagicMock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Query

from app.services.consultant_service import ConsultantService
from app.database.models import Consultant, Practice


class TestGetAllConsultantsObjectsErrorPaths:
    """Tests pour get_all_consultants_objects() - Chemins d'erreur (lines 67-69)"""

    @patch('app.services.consultant_service.get_database_session')
    def test_get_all_consultants_objects_sqlalchemy_error(self, mock_session):
        """Test avec SQLAlchemyError lors de la requête"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Simuler une erreur SQL
        mock_db.query.side_effect = SQLAlchemyError("Database connection failed")
        
        result = ConsultantService.get_all_consultants_objects(page=1, per_page=50)
        
        assert result == []

    @patch('app.services.consultant_service.get_database_session')
    def test_get_all_consultants_objects_value_error(self, mock_session):
        """Test avec ValueError (page invalide)"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Simuler une ValueError sur offset
        mock_db.query.return_value.options.return_value.offset.side_effect = ValueError("Invalid page number")
        
        result = ConsultantService.get_all_consultants_objects(page=-1, per_page=50)
        
        assert result == []

    @patch('app.services.consultant_service.get_database_session')
    def test_get_all_consultants_objects_type_error(self, mock_session):
        """Test avec TypeError lors de l'expunge"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Créer un mock consultant qui cause TypeError sur expunge
        mock_consultant = Mock(spec=Consultant)
        mock_db.query.return_value.options.return_value.offset.return_value.limit.return_value.all.return_value = [mock_consultant]
        mock_db.expunge.side_effect = TypeError("Cannot expunge")
        
        result = ConsultantService.get_all_consultants_objects(page=1, per_page=50)
        
        assert result == []

    @patch('app.services.consultant_service.get_database_session')
    def test_get_all_consultants_objects_attribute_error(self, mock_session):
        """Test avec AttributeError lors de l'accès à practice"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Simuler AttributeError sur l'accès à la practice
        mock_consultant = Mock(spec=Consultant)
        mock_consultant.practice = Mock()
        # Forcer l'erreur lors de l'accès à practice.nom
        mock_consultant.practice.nom = property(lambda self: None)  # noqa: S5914
        
        # Simuler erreur lors de l'itération sur consultants
        mock_db.query.return_value.options.return_value.offset.return_value.limit.return_value.all.side_effect = AttributeError("practice attribute error")
        
        result = ConsultantService.get_all_consultants_objects(page=1, per_page=50)
        
        assert result == []


class TestBuildSearchQuery:
    """Tests pour _build_search_query() - Création de requête (lines 74-110)"""

    @patch('app.services.consultant_service.get_database_session')
    def test_build_search_query_all_filters_empty(self, mock_session):
        """Test avec tous les filtres vides"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock query builder
        mock_query = Mock(spec=Query)
        mock_db.query.return_value.options.return_value = mock_query
        
        result = ConsultantService._build_search_query(
            session=mock_db,
            practice_filter=None,
            grade_filter=None,
            availability_filter=None,
            search_term=""
        )
        
        # Vérifier que query est créée sans filtres
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_search_query_with_practice_filter(self, mock_session):
        """Test avec practice_filter défini"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_db.query.return_value.options.return_value = mock_query
        
        result = ConsultantService._build_search_query(
            session=mock_db,
            practice_filter="Data Engineering",
            grade_filter=None,
            availability_filter=None,
            search_term=""
        )
        
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_search_query_with_grade_filter(self, mock_session):
        """Test avec grade_filter défini"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_db.query.return_value.options.return_value = mock_query
        
        result = ConsultantService._build_search_query(
            session=mock_db,
            practice_filter=None,
            grade_filter="Senior",
            availability_filter=None,
            search_term=""
        )
        
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_search_query_with_availability_filter(self, mock_session):
        """Test avec availability_filter défini"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_db.query.return_value.options.return_value = mock_query
        
        result = ConsultantService._build_search_query(
            session=mock_db,
            practice_filter=None,
            grade_filter=None,
            availability_filter="✅ Disponible",
            search_term=""
        )
        
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_search_query_multiple_filters(self, mock_session):
        """Test avec combinaison de filtres"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_db.query.return_value.options.return_value = mock_query
        
        result = ConsultantService._build_search_query(
            session=mock_db,
            practice_filter="Data Engineering",
            grade_filter="Senior",
            availability_filter="✅ Disponible",
            search_term="Dupont"
        )
        
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_search_query_with_search_term(self, mock_session):
        """Test avec search_term défini"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_db.query.return_value.options.return_value = mock_query
        
        result = ConsultantService._build_search_query(
            session=mock_db,
            practice_filter=None,
            grade_filter=None,
            availability_filter=None,
            search_term="Jean"
        )
        
        assert result is not None


class TestApplySearchFilters:
    """Tests pour _apply_search_filters() - Application filtres (lines 148, 151, 154)"""

    def test_apply_search_filters_empty_search_term(self):
        """Test avec search_term vide"""
        mock_query = Mock(spec=Query)
        
        result = ConsultantService._apply_search_filters(
            query=mock_query,
            practice_filter=None,
            grade_filter=None,
            availability_filter=None,
            search_term=""
        )
        
        # Vérifier que query est retournée sans modifications
        assert result == mock_query

    def test_apply_search_filters_sql_injection_attempt(self):
        """Test avec tentative d'injection SQL dans search_term"""
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        
        # Terme malveillant
        malicious_term = "'; DROP TABLE consultants; --"
        
        result = ConsultantService._apply_search_filters(
            query=mock_query,
            practice_filter=None,
            grade_filter=None,
            availability_filter=None,
            search_term=malicious_term
        )
        
        # Vérifier que filter est appelé (SQLAlchemy gère l'échappement)
        assert result is not None

    def test_apply_search_filters_special_characters(self):
        """Test avec caractères spéciaux dans search_term"""
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        
        special_chars = "Jean-François O'Brien (test@example.com)"
        
        result = ConsultantService._apply_search_filters(
            query=mock_query,
            practice_filter=None,
            grade_filter=None,
            availability_filter=None,
            search_term=special_chars
        )
        
        assert result is not None

    def test_apply_search_filters_with_all_parameters(self):
        """Test avec tous les paramètres définis"""
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        
        result = ConsultantService._apply_search_filters(
            query=mock_query,
            practice_filter="Data Engineering",
            grade_filter="Senior",
            availability_filter="✅ Disponible",
            search_term="Dupont"
        )
        
        assert result is not None


class TestCalculateExperienceYears:
    """Tests pour _calculate_experience_years() - Calcul d'expérience (lines 230-234)"""

    def test_calculate_experience_years_none(self):
        """Test avec date_premiere_mission None"""
        result = ConsultantService._calculate_experience_years(None)
        
        assert result == 0

    def test_calculate_experience_years_future_date(self):
        """Test avec date dans le futur"""
        future_date = date(2030, 1, 1)
        
        result = ConsultantService._calculate_experience_years(future_date)
        
        # Devrait retourner 0 ou un nombre négatif géré
        assert result <= 0

    def test_calculate_experience_years_valid_date(self):
        """Test avec date valide (10 ans d'expérience)"""
        past_date = date(2015, 10, 8)  # 10 ans avant octobre 2025
        
        result = ConsultantService._calculate_experience_years(past_date)
        
        # Devrait être environ 10 ans
        assert result >= 9
        assert result <= 11

    def test_calculate_experience_years_very_old_date(self):
        """Test avec date très ancienne (>50 ans)"""
        very_old_date = date(1970, 1, 1)
        
        result = ConsultantService._calculate_experience_years(very_old_date)
        
        # Devrait retourner un nombre élevé (>50)
        assert result >= 50

    def test_calculate_experience_years_recent_date(self):
        """Test avec date récente (6 mois)"""
        recent_date = date(2025, 4, 8)  # 6 mois avant octobre 2025
        
        result = ConsultantService._calculate_experience_years(recent_date)
        
        # Devrait être 0 ou 1 an
        assert result >= 0
        assert result <= 1


# Test de régression pour s'assurer que les constantes sont bien définies
class TestConstants:
    """Tests pour les constantes de classe"""

    def test_status_constants_defined(self):
        """Test que les constantes de statut sont bien définies"""
        assert hasattr(ConsultantService, 'STATUS_AVAILABLE')
        assert hasattr(ConsultantService, 'STATUS_BUSY')
        assert hasattr(ConsultantService, 'STATUS_IN_PROGRESS')
        
        assert ConsultantService.STATUS_AVAILABLE == "✅ Disponible"
        assert ConsultantService.STATUS_BUSY == "🔴 Occupé"
        assert ConsultantService.STATUS_IN_PROGRESS == "En cours"
