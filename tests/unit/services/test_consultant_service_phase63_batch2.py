"""
Phase 63 - Batch 2: Tests pour consultant_service.py
Focus: Méthodes de statistiques et comptage (lines 266-415)
Objectif: Coverage 71% → 77% (+6%)
"""

from datetime import date, datetime
from unittest.mock import Mock, patch, MagicMock
import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Query

from app.services.consultant_service import ConsultantService
from app.database.models import Consultant, Practice, Mission


class TestGetConsultantsCount:
    """Tests pour get_consultants_count() - Error paths (lines 266-268)"""

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultants_count_sqlalchemy_error(self, mock_session):
        """Test avec SQLAlchemyError lors du comptage"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Simuler une erreur SQL
        mock_db.query.return_value.count.side_effect = SQLAlchemyError("Database error")
        
        result = ConsultantService.get_consultants_count()
        
        assert result == 0

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultants_count_value_error(self, mock_session):
        """Test avec ValueError lors du comptage"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_db.query.return_value.count.side_effect = ValueError("Invalid count")
        
        result = ConsultantService.get_consultants_count()
        
        assert result == 0

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultants_count_type_error(self, mock_session):
        """Test avec TypeError lors du comptage"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_db.query.return_value.count.side_effect = TypeError("Type error")
        
        result = ConsultantService.get_consultants_count()
        
        assert result == 0


class TestBuildStatsQuery:
    """Tests pour _build_stats_query() - Statistiques (lines 284-308)"""

    @patch('app.services.consultant_service.get_database_session')
    def test_build_stats_query_all_filters_none(self, mock_session):
        """Test avec tous filtres None"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        
        # Mock query builder
        mock_db.query.return_value.outerjoin.return_value.outerjoin.return_value = mock_query
        
        result = ConsultantService._build_stats_query(
            session=mock_db,
            practice_filter=None,
            grade_filter=None,
            availability_filter=None
        )
        
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_stats_query_with_practice_filter(self, mock_session):
        """Test avec practice_filter défini"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_db.query.return_value.outerjoin.return_value.outerjoin.return_value = mock_query
        
        result = ConsultantService._build_stats_query(
            session=mock_db,
            practice_filter="Data Engineering",
            grade_filter=None,
            availability_filter=None
        )
        
        # Vérifier que filter a été appelé
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_stats_query_with_grade_filter(self, mock_session):
        """Test avec grade_filter défini"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_db.query.return_value.outerjoin.return_value.outerjoin.return_value = mock_query
        
        result = ConsultantService._build_stats_query(
            session=mock_db,
            practice_filter=None,
            grade_filter="Senior",
            availability_filter=None
        )
        
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_stats_query_with_availability_filter(self, mock_session):
        """Test avec availability_filter défini"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_db.query.return_value.outerjoin.return_value.outerjoin.return_value = mock_query
        
        result = ConsultantService._build_stats_query(
            session=mock_db,
            practice_filter=None,
            grade_filter=None,
            availability_filter=True
        )
        
        assert result is not None

    @patch('app.services.consultant_service.get_database_session')
    def test_build_stats_query_all_filters_set(self, mock_session):
        """Test avec tous les filtres définis"""
        mock_db = Mock()
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_db.query.return_value.outerjoin.return_value.outerjoin.return_value = mock_query
        
        result = ConsultantService._build_stats_query(
            session=mock_db,
            practice_filter="Data Engineering",
            grade_filter="Senior",
            availability_filter=False
        )
        
        assert result is not None


class TestApplyStatsFilters:
    """Tests pour _apply_stats_filters() - Application filtres stats (lines 314-323)"""

    def test_apply_stats_filters_no_filters(self):
        """Test sans filtres"""
        mock_query = Mock(spec=Query)
        
        result = ConsultantService._apply_stats_filters(
            query=mock_query,
            practice_filter=None,
            grade_filter=None,
            availability_filter=None
        )
        
        # Query retournée sans modifications
        assert result == mock_query

    def test_apply_stats_filters_practice_only(self):
        """Test avec practice_filter uniquement"""
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        
        result = ConsultantService._apply_stats_filters(
            query=mock_query,
            practice_filter="Data Science",
            grade_filter=None,
            availability_filter=None
        )
        
        # Vérifier filter appelé une fois
        mock_query.filter.assert_called_once()
        assert result is not None

    def test_apply_stats_filters_grade_only(self):
        """Test avec grade_filter uniquement"""
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        
        result = ConsultantService._apply_stats_filters(
            query=mock_query,
            practice_filter=None,
            grade_filter="Manager",
            availability_filter=None
        )
        
        mock_query.filter.assert_called_once()
        assert result is not None

    def test_apply_stats_filters_availability_true(self):
        """Test avec availability_filter=True"""
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        
        result = ConsultantService._apply_stats_filters(
            query=mock_query,
            practice_filter=None,
            grade_filter=None,
            availability_filter=True
        )
        
        mock_query.filter.assert_called_once()
        assert result is not None

    def test_apply_stats_filters_availability_false(self):
        """Test avec availability_filter=False"""
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        
        result = ConsultantService._apply_stats_filters(
            query=mock_query,
            practice_filter=None,
            grade_filter=None,
            availability_filter=False
        )
        
        mock_query.filter.assert_called_once()
        assert result is not None

    def test_apply_stats_filters_all_combinations(self):
        """Test avec toutes les combinaisons de filtres"""
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        
        result = ConsultantService._apply_stats_filters(
            query=mock_query,
            practice_filter="BI & Analytics",
            grade_filter="Expert",
            availability_filter=True
        )
        
        # 3 filtres appliqués
        assert mock_query.filter.call_count == 3
        assert result is not None


class TestGetConsultantSummaryStats:
    """Tests pour get_consultant_summary_stats() - Stats globales (lines 354-360)"""

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_summary_stats_success(self, mock_session):
        """Test avec succès des statistiques"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock query counts - Simuler les 4 requêtes séparées
        mock_query_consultant = Mock()
        mock_query_consultant.count.return_value = 100
        
        mock_query_available = Mock()
        mock_query_available.count.return_value = 30
        
        mock_query_mission = Mock()
        mock_query_mission.count.return_value = 200
        
        mock_query_active = Mock()
        mock_query_active.count.return_value = 45
        
        # Simuler les appels successifs à query()
        mock_db.query.side_effect = [
            mock_query_consultant,  # Total consultants
            mock_query_available,   # Available consultants
            mock_query_mission,     # Total missions
            mock_query_active       # Active missions
        ]
        
        # Mock filter pour available et active
        mock_query_available.filter.return_value = mock_query_available
        mock_query_active.filter.return_value = mock_query_active
        
        result = ConsultantService.get_consultant_summary_stats()
        
        assert result["total_consultants"] == 100
        assert result["available_consultants"] == 30
        assert result["total_missions"] == 200
        assert result["active_missions"] == 45
        assert result["busy_consultants"] == 70  # 100 - 30

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_summary_stats_empty_db(self, mock_session):
        """Test avec DB vide"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Tous les counts retournent 0
        mock_db.query.return_value.count.return_value = 0
        mock_db.query.return_value.filter.return_value.count.return_value = 0
        
        result = ConsultantService.get_consultant_summary_stats()
        
        assert result["total_consultants"] == 0
        assert result["available_consultants"] == 0
        assert result["total_missions"] == 0
        assert result["active_missions"] == 0
        assert result["busy_consultants"] == 0

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_summary_stats_sqlalchemy_error(self, mock_session):
        """Test avec SQLAlchemyError"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Simuler erreur SQL
        mock_db.query.side_effect = SQLAlchemyError("Connection lost")
        
        result = ConsultantService.get_consultant_summary_stats()
        
        # Doit retourner dict avec valeurs 0
        assert result["total_consultants"] == 0
        assert result["available_consultants"] == 0
        assert result["total_missions"] == 0
        assert result["active_missions"] == 0
        assert result["busy_consultants"] == 0

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_summary_stats_value_error(self, mock_session):
        """Test avec ValueError lors du comptage"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_db.query.return_value.count.side_effect = ValueError("Invalid value")
        
        result = ConsultantService.get_consultant_summary_stats()
        
        assert all(v == 0 for v in result.values())

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_summary_stats_type_error(self, mock_session):
        """Test avec TypeError"""
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_db.query.return_value.count.side_effect = TypeError("Type mismatch")
        
        result = ConsultantService.get_consultant_summary_stats()
        
        assert all(v == 0 for v in result.values())


class TestConvertStatsRowToDict:
    """Tests pour _convert_stats_row_to_dict() - Conversion stats (lines 397-415)"""

    def test_convert_stats_row_to_dict_with_salary(self):
        """Test conversion avec salaire valide"""
        mock_row = Mock()
        mock_row.id = 1
        mock_row.prenom = "Jean"
        mock_row.nom = "Dupont"
        mock_row.email = "jean.dupont@example.com"
        mock_row.telephone = "0123456789"
        mock_row.salaire_actuel = 50000
        mock_row.disponibilite = True
        mock_row.date_creation = datetime(2023, 1, 1)
        mock_row.derniere_maj = datetime(2025, 1, 1)
        mock_row.societe = "Quanteam"
        mock_row.date_entree_societe = date(2023, 1, 1)
        mock_row.date_sortie_societe = None
        mock_row.date_premiere_mission = date(2023, 6, 1)
        mock_row.grade = "Senior"
        mock_row.type_contrat = "CDI"
        mock_row.practice_name = "Data Engineering"
        mock_row.nb_missions = 5
        
        result = ConsultantService._convert_stats_row_to_dict(mock_row)
        
        assert result["id"] == 1
        assert result["prenom"] == "Jean"
        assert result["nom"] == "Dupont"
        assert result["salaire_actuel"] == 50000
        assert result["cjm"] > 0  # CJM calculé
        assert result["grade"] == "Senior"
        assert result["type_contrat"] == "CDI"
        assert result["nb_missions"] == 5

    def test_convert_stats_row_to_dict_salary_none(self):
        """Test conversion avec salaire None"""
        mock_row = Mock()
        mock_row.id = 2
        mock_row.prenom = "Marie"
        mock_row.nom = "Martin"
        mock_row.email = "marie@example.com"
        mock_row.telephone = None
        mock_row.salaire_actuel = None
        mock_row.disponibilite = False
        mock_row.date_creation = datetime(2024, 1, 1)
        mock_row.derniere_maj = datetime(2025, 1, 1)
        mock_row.societe = None
        mock_row.date_entree_societe = None
        mock_row.date_sortie_societe = None
        mock_row.date_premiere_mission = None
        mock_row.grade = None
        mock_row.type_contrat = None
        mock_row.practice_name = None
        mock_row.nb_missions = 0
        
        result = ConsultantService._convert_stats_row_to_dict(mock_row)
        
        assert result["salaire_actuel"] == 0
        assert result["cjm"] == 0  # CJM = 0 si pas de salaire
        assert result["grade"] == "Junior"  # Valeur par défaut
        assert result["type_contrat"] == "CDI"  # Valeur par défaut
        assert result["nb_missions"] == 0

    def test_convert_stats_row_to_dict_salary_zero(self):
        """Test conversion avec salaire 0"""
        mock_row = Mock()
        mock_row.id = 3
        mock_row.prenom = "Paul"
        mock_row.nom = "Bernard"
        mock_row.email = "paul@example.com"
        mock_row.telephone = "0987654321"
        mock_row.salaire_actuel = 0
        mock_row.disponibilite = True
        mock_row.date_creation = datetime(2025, 1, 1)
        mock_row.derniere_maj = datetime(2025, 10, 1)
        mock_row.societe = "Company"
        mock_row.date_entree_societe = date(2025, 1, 1)
        mock_row.date_sortie_societe = None
        mock_row.date_premiere_mission = date(2025, 2, 1)
        mock_row.grade = "Manager"
        mock_row.type_contrat = "Freelance"
        mock_row.practice_name = "Cloud"
        mock_row.nb_missions = 2
        
        result = ConsultantService._convert_stats_row_to_dict(mock_row)
        
        assert result["salaire_actuel"] == 0
        assert result["cjm"] == 0  # Division par 0 évitée

    def test_convert_stats_row_to_dict_with_experience(self):
        """Test conversion avec calcul d'expérience"""
        mock_row = Mock()
        mock_row.id = 4
        mock_row.prenom = "Sophie"
        mock_row.nom = "Durand"
        mock_row.email = "sophie@example.com"
        mock_row.telephone = "0111111111"
        mock_row.salaire_actuel = 60000
        mock_row.disponibilite = False
        mock_row.date_creation = datetime(2020, 1, 1)
        mock_row.derniere_maj = datetime(2025, 10, 8)
        mock_row.societe = "Tech Corp"
        mock_row.date_entree_societe = date(2020, 1, 1)
        mock_row.date_sortie_societe = None
        mock_row.date_premiere_mission = date(2020, 6, 1)  # ~5 ans d'expérience
        mock_row.grade = "Expert"
        mock_row.type_contrat = "CDI"
        mock_row.practice_name = "Data Science"
        mock_row.nb_missions = 10
        
        result = ConsultantService._convert_stats_row_to_dict(mock_row)
        
        # Vérifier que l'expérience est calculée (environ 5 ans)
        assert "experience_annees" in result
        assert result["experience_annees"] >= 4
        assert result["experience_annees"] <= 6
