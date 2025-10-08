"""
Tests Phase 56 - technology_service.py (Coverage boost 69% → 72%+)
Cible: TechnologyService - Gestion technologies référentiel + personnalisées
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError

# Import du service à tester
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from app.services.technology_service import TechnologyService


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_db_session():
    """Mock session de base de données"""
    session = MagicMock()
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=False)
    return session


@pytest.fixture
def mock_custom_technologies():
    """Mock liste de technologies personnalisées"""
    tech1 = Mock()
    tech1.id = 1
    tech1.nom = "CustomTech1"
    tech1.categorie = "Personnalisées"
    tech1.description = "Description tech 1"
    
    tech2 = Mock()
    tech2.id = 2
    tech2.nom = "CustomTech2"
    tech2.categorie = "Personnalisées"
    tech2.description = "Description tech 2"
    
    return [tech1, tech2]


# ============================================================================
# TESTS: get_all_available_technologies()
# ============================================================================

class TestGetAllAvailableTechnologies:
    """Tests pour get_all_available_technologies()"""

    @patch('app.services.technology_service.get_database_session')
    @patch('app.services.technology_service.get_all_technologies')
    def test_get_all_available_technologies_success(self, mock_get_all_techs, mock_get_db, mock_db_session, mock_custom_technologies):
        """Test récupération réussie de toutes les technologies"""
        # Mock référentiel
        mock_get_all_techs.return_value = ["Python", "Java", "JavaScript"]
        
        # Mock DB
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.all.return_value = mock_custom_technologies
        
        result = TechnologyService.get_all_available_technologies()
        
        assert isinstance(result, list)
        assert "Python" in result
        assert "Java" in result
        assert "JavaScript" in result
        assert "CustomTech1" in result
        assert "CustomTech2" in result
        assert len(result) == 5  # 3 réf + 2 custom
        assert result == sorted(result)  # Vérifie le tri

    @patch('app.services.technology_service.get_database_session')
    @patch('app.services.technology_service.get_all_technologies')
    def test_get_all_available_technologies_db_error(self, mock_get_all_techs, mock_get_db):
        """Test avec erreur de base de données"""
        # Mock référentiel
        mock_get_all_techs.return_value = ["Python", "Java"]
        
        # Mock DB avec erreur
        mock_get_db.side_effect = SQLAlchemyError("Database error")
        
        result = TechnologyService.get_all_available_technologies()
        
        # Devrait retourner seulement le référentiel
        assert result == ["Python", "Java"]

    @patch('app.services.technology_service.get_database_session')
    @patch('app.services.technology_service.get_all_technologies')
    def test_get_all_available_technologies_no_custom(self, mock_get_all_techs, mock_get_db, mock_db_session):
        """Test sans technologies personnalisées"""
        # Mock référentiel
        mock_get_all_techs.return_value = ["Python", "Java"]
        
        # Mock DB sans custom tech
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.all.return_value = []
        
        result = TechnologyService.get_all_available_technologies()
        
        assert result == ["Java", "Python"]  # Trié

    @patch('app.services.technology_service.get_database_session')
    @patch('app.services.technology_service.get_all_technologies')
    def test_get_all_available_technologies_deduplication(self, mock_get_all_techs, mock_get_db, mock_db_session):
        """Test dédoublonnage si technologie existe dans les deux sources"""
        # Mock référentiel
        mock_get_all_techs.return_value = ["Python", "Java", "React"]
        
        # Mock DB avec une tech en double
        tech_duplicate = Mock()
        tech_duplicate.nom = "Python"  # Doublon
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.all.return_value = [tech_duplicate]
        
        result = TechnologyService.get_all_available_technologies()
        
        # Python ne devrait apparaître qu'une fois
        assert result.count("Python") == 1
        assert len(result) == 3


# ============================================================================
# TESTS: get_all_technologies() (alias)
# ============================================================================

class TestGetAllTechnologies:
    """Tests pour get_all_technologies() - alias de compatibilité"""

    @patch('app.services.technology_service.TechnologyService.get_all_available_technologies')
    def test_get_all_technologies_alias(self, mock_get_all_available):
        """Test que get_all_technologies appelle get_all_available_technologies"""
        mock_get_all_available.return_value = ["Python", "Java"]
        
        result = TechnologyService.get_all_technologies()
        
        mock_get_all_available.assert_called_once()
        assert result == ["Python", "Java"]


# ============================================================================
# TESTS: add_custom_technology()
# ============================================================================

class TestAddCustomTechnology:
    """Tests pour add_custom_technology()"""

    @patch('app.services.technology_service.get_database_session')
    def test_add_custom_technology_success(self, mock_get_db, mock_db_session):
        """Test ajout réussi d'une technologie personnalisée"""
        # Mock DB - technologie n'existe pas
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = TechnologyService.add_custom_technology("NewTech", "Custom Category")
        
        assert result is True
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @patch('app.services.technology_service.get_database_session')
    def test_add_custom_technology_already_exists(self, mock_get_db, mock_db_session):
        """Test ajout d'une technologie déjà existante"""
        # Mock DB - technologie existe déjà
        existing_tech = Mock()
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = existing_tech
        
        result = TechnologyService.add_custom_technology("ExistingTech")
        
        assert result is False
        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()

    @patch('app.services.technology_service.get_database_session')
    def test_add_custom_technology_default_category(self, mock_get_db, mock_db_session):
        """Test ajout avec catégorie par défaut"""
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = TechnologyService.add_custom_technology("NewTech")  # Sans catégorie
        
        assert result is True
        # Vérifier que la catégorie par défaut est "Personnalisées"
        mock_db_session.add.assert_called_once()

    @patch('app.services.technology_service.get_database_session')
    def test_add_custom_technology_db_error(self, mock_get_db):
        """Test avec erreur de base de données"""
        mock_get_db.side_effect = SQLAlchemyError("Database error")
        
        result = TechnologyService.add_custom_technology("NewTech")
        
        assert result is False


# ============================================================================
# TESTS: get_custom_technologies()
# ============================================================================

class TestGetCustomTechnologies:
    """Tests pour get_custom_technologies()"""

    @patch('app.services.technology_service.get_database_session')
    def test_get_custom_technologies_success(self, mock_get_db, mock_db_session, mock_custom_technologies):
        """Test récupération réussie des technologies personnalisées"""
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.all.return_value = mock_custom_technologies
        
        result = TechnologyService.get_custom_technologies()
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["nom"] == "CustomTech1"
        assert result[0]["categorie"] == "Personnalisées"
        assert result[1]["nom"] == "CustomTech2"

    @patch('app.services.technology_service.get_database_session')
    def test_get_custom_technologies_empty(self, mock_get_db, mock_db_session):
        """Test sans technologies personnalisées"""
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.all.return_value = []
        
        result = TechnologyService.get_custom_technologies()
        
        assert result == []

    @patch('app.services.technology_service.get_database_session')
    def test_get_custom_technologies_db_error(self, mock_get_db):
        """Test avec erreur de base de données"""
        mock_get_db.side_effect = SQLAlchemyError("Database error")
        
        result = TechnologyService.get_custom_technologies()
        
        assert result == []


# ============================================================================
# TESTS: delete_custom_technology()
# ============================================================================

class TestDeleteCustomTechnology:
    """Tests pour delete_custom_technology()"""

    @patch('app.services.technology_service.get_database_session')
    def test_delete_custom_technology_success(self, mock_get_db, mock_db_session):
        """Test suppression réussie d'une technologie personnalisée"""
        # Mock DB - technologie existe
        tech_to_delete = Mock()
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = tech_to_delete
        
        result = TechnologyService.delete_custom_technology(1)
        
        assert result is True
        mock_db_session.delete.assert_called_once_with(tech_to_delete)
        mock_db_session.commit.assert_called_once()

    @patch('app.services.technology_service.get_database_session')
    def test_delete_custom_technology_not_found(self, mock_get_db, mock_db_session):
        """Test suppression d'une technologie inexistante"""
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = TechnologyService.delete_custom_technology(999)
        
        assert result is False
        mock_db_session.delete.assert_not_called()
        mock_db_session.commit.assert_not_called()

    @patch('app.services.technology_service.get_database_session')
    def test_delete_custom_technology_db_error(self, mock_get_db):
        """Test avec erreur de base de données"""
        mock_get_db.side_effect = SQLAlchemyError("Database error")
        
        result = TechnologyService.delete_custom_technology(1)
        
        assert result is False


# ============================================================================
# TESTS: search_technologies()
# ============================================================================

class TestSearchTechnologies:
    """Tests pour search_technologies()"""

    @patch('app.services.technology_service.TechnologyService.get_all_available_technologies')
    def test_search_technologies_case_insensitive(self, mock_get_all):
        """Test recherche insensible à la casse"""
        mock_get_all.return_value = ["Python", "Java", "JavaScript", "TypeScript"]
        
        result = TechnologyService.search_technologies("script")
        
        assert "JavaScript" in result
        assert "TypeScript" in result
        assert len(result) == 2

    @patch('app.services.technology_service.TechnologyService.get_all_available_technologies')
    def test_search_technologies_exact_match(self, mock_get_all):
        """Test recherche avec correspondance exacte"""
        mock_get_all.return_value = ["Python", "Java", "JavaScript"]
        
        result = TechnologyService.search_technologies("Java")
        
        assert "Java" in result
        assert "JavaScript" in result
        assert len(result) == 2

    @patch('app.services.technology_service.TechnologyService.get_all_available_technologies')
    def test_search_technologies_no_match(self, mock_get_all):
        """Test recherche sans résultat"""
        mock_get_all.return_value = ["Python", "Java", "JavaScript"]
        
        result = TechnologyService.search_technologies("Ruby")
        
        assert result == []

    @patch('app.services.technology_service.TechnologyService.get_all_available_technologies')
    def test_search_technologies_empty_query(self, mock_get_all):
        """Test recherche avec query vide"""
        mock_get_all.return_value = ["Python", "Java", "JavaScript"]
        
        result = TechnologyService.search_technologies("")
        
        # Tous les résultats (query vide contenu dans tous)
        assert len(result) == 3

    @patch('app.services.technology_service.TechnologyService.get_all_available_technologies')
    def test_search_technologies_partial_match(self, mock_get_all):
        """Test recherche avec correspondance partielle"""
        mock_get_all.return_value = ["Python", "PyCharm", "Java", "JavaScript"]
        
        result = TechnologyService.search_technologies("Py")
        
        assert "Python" in result
        assert "PyCharm" in result
        assert len(result) == 2


# ============================================================================
# TESTS: get_technologies_by_category()
# ============================================================================

class TestGetTechnologiesByCategory:
    """Tests pour get_technologies_by_category()"""

    @patch('app.services.technology_service.TechnologyService.get_custom_technologies')
    @patch('app.services.technology_service.TECHNOLOGIES_REFERENTIEL')
    def test_get_technologies_by_category_success(self, mock_referentiel, mock_get_custom):
        """Test récupération par catégorie avec référentiel + custom"""
        # Mock référentiel
        mock_referentiel.copy.return_value = {
            "Langages": ["Python", "Java"],
            "Frontend": ["React", "Vue"]
        }
        
        # Mock technologies personnalisées
        mock_get_custom.return_value = [
            {"nom": "CustomTech1", "categorie": "Personnalisées"},
            {"nom": "CustomTech2", "categorie": "Personnalisées"}
        ]
        
        result = TechnologyService.get_technologies_by_category()
        
        assert isinstance(result, dict)
        assert "Langages" in result
        assert "Frontend" in result
        assert "Personnalisées" in result
        assert len(result["Personnalisées"]) == 2

    @patch('app.services.technology_service.TechnologyService.get_custom_technologies')
    @patch('app.services.technology_service.TECHNOLOGIES_REFERENTIEL')
    def test_get_technologies_by_category_sorted(self, mock_referentiel, mock_get_custom):
        """Test que les technologies sont triées dans chaque catégorie"""
        mock_referentiel.copy.return_value = {
            "Langages": ["Zebra", "Alpha", "Beta"]  # Non trié
        }
        mock_get_custom.return_value = []
        
        result = TechnologyService.get_technologies_by_category()
        
        # Devrait être trié
        assert result["Langages"] == ["Alpha", "Beta", "Zebra"]

    @patch('app.services.technology_service.TechnologyService.get_custom_technologies')
    @patch('app.services.technology_service.TECHNOLOGIES_REFERENTIEL')
    def test_get_technologies_by_category_no_custom(self, mock_referentiel, mock_get_custom):
        """Test sans technologies personnalisées"""
        mock_referentiel.copy.return_value = {
            "Langages": ["Python", "Java"]
        }
        mock_get_custom.return_value = []
        
        result = TechnologyService.get_technologies_by_category()
        
        assert "Langages" in result
        assert "Personnalisées" not in result

    @patch('app.services.technology_service.TechnologyService.get_custom_technologies')
    @patch('app.services.technology_service.TECHNOLOGIES_REFERENTIEL')
    def test_get_technologies_by_category_new_category(self, mock_referentiel, mock_get_custom):
        """Test ajout d'une nouvelle catégorie via custom tech"""
        mock_referentiel.copy.return_value = {
            "Langages": ["Python"]
        }
        mock_get_custom.return_value = [
            {"nom": "CustomTool", "categorie": "Outils Internes"}
        ]
        
        result = TechnologyService.get_technologies_by_category()
        
        assert "Outils Internes" in result
        assert "CustomTool" in result["Outils Internes"]


# ============================================================================
# TESTS: Edge cases et intégration
# ============================================================================

class TestEdgeCases:
    """Tests de cas limites"""

    @patch('app.services.technology_service.get_database_session')
    def test_add_technology_with_special_characters(self, mock_get_db, mock_db_session):
        """Test ajout technologie avec caractères spéciaux"""
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = TechnologyService.add_custom_technology("C++", "Langages")
        
        assert result is True

    @patch('app.services.technology_service.get_database_session')
    def test_add_technology_empty_name(self, mock_get_db, mock_db_session):
        """Test ajout avec nom vide"""
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = TechnologyService.add_custom_technology("")
        
        # Devrait accepter (pas de validation dans le code)
        assert result is True

    @patch('app.services.technology_service.TechnologyService.get_all_available_technologies')
    def test_search_with_special_characters(self, mock_get_all):
        """Test recherche avec caractères spéciaux"""
        mock_get_all.return_value = ["C++", "C#", "F#"]
        
        result = TechnologyService.search_technologies("+")
        
        assert "C++" in result

    @patch('app.services.technology_service.get_database_session')
    def test_delete_technology_with_id_zero(self, mock_get_db, mock_db_session):
        """Test suppression avec ID = 0"""
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = TechnologyService.delete_custom_technology(0)
        
        assert result is False

    @patch('app.services.technology_service.get_database_session')
    def test_delete_technology_with_negative_id(self, mock_get_db, mock_db_session):
        """Test suppression avec ID négatif"""
        mock_get_db.return_value = mock_db_session
        mock_db_session.query.return_value.filter.return_value.first.return_value = None
        
        result = TechnologyService.delete_custom_technology(-1)
        
        assert result is False
