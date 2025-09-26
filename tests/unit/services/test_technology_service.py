"""
Tests unitaires pour le service TechnologyService
Couvre toutes les méthodes statiques de gestion des technologies
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.services.technology_service import TechnologyService


class TestTechnologyService:
    """Tests pour la classe TechnologyService"""

    @patch("app.services.technology_service.get_database_session")
    @patch("app.services.technology_service.get_all_technologies")
    def test_get_all_available_technologies_success(
        self, mock_get_all, mock_get_session
    ):
        """Test récupération de toutes les technologies disponibles"""
        # Mock données
        mock_get_all.return_value = ["Python", "Java", "SQL"]

        mock_custom_tech = MagicMock()
        mock_custom_tech.nom = "React"
        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_custom_tech]
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.get_all_available_technologies()

        # Vérifications
        assert "Python" in result
        assert "Java" in result
        assert "SQL" in result
        assert "React" in result
        assert len(result) == 4  # Toutes les technos sans doublons
        assert result == sorted(result)  # Trié

    @patch("app.services.technology_service.get_database_session")
    @patch("app.services.technology_service.get_all_technologies")
    def test_get_all_available_technologies_db_error(
        self, mock_get_all, mock_get_session
    ):
        """Test récupération avec erreur DB - retourne seulement référentiel"""
        mock_get_all.return_value = ["Python", "Java"]

        mock_session = MagicMock()
        mock_session.query.side_effect = SQLAlchemyError("DB Error")
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.get_all_available_technologies()

        # Retourne seulement les technos du référentiel
        assert result == ["Python", "Java"]

    @patch("app.services.technology_service.get_database_session")
    def test_add_custom_technology_success(self, mock_get_session):
        """Test ajout d'une technologie personnalisée"""
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            None  # N'existe pas
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.add_custom_technology("NewTech", "Frameworks")

        assert result is True
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch("app.services.technology_service.get_database_session")
    def test_add_custom_technology_already_exists(self, mock_get_session):
        """Test ajout d'une technologie qui existe déjà"""
        mock_existing = MagicMock()
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_existing
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.add_custom_technology("ExistingTech")

        assert result is False
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @patch("app.services.technology_service.get_database_session")
    def test_add_custom_technology_db_error(self, mock_get_session):
        """Test ajout avec erreur DB"""
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.side_effect = (
            SQLAlchemyError("DB Error")
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.add_custom_technology("NewTech")

        assert result is False

    @patch("app.services.technology_service.get_database_session")
    def test_get_custom_technologies_success(self, mock_get_session):
        """Test récupération des technologies personnalisées"""
        mock_tech = MagicMock()
        mock_tech.id = 1
        mock_tech.nom = "CustomTech"
        mock_tech.categorie = "Personnalisées"
        mock_tech.description = "Description"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [mock_tech]
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.get_custom_technologies()

        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["nom"] == "CustomTech"
        assert result[0]["categorie"] == "Personnalisées"

    @patch("app.services.technology_service.get_database_session")
    def test_get_custom_technologies_db_error(self, mock_get_session):
        """Test récupération avec erreur DB"""
        mock_session = MagicMock()
        mock_session.query.side_effect = SQLAlchemyError("DB Error")
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.get_custom_technologies()

        assert result == []

    @patch("app.services.technology_service.get_database_session")
    def test_delete_custom_technology_success(self, mock_get_session):
        """Test suppression d'une technologie personnalisée"""
        mock_tech = MagicMock()
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_tech
        )
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.delete_custom_technology(1)

        assert result is True
        mock_session.delete.assert_called_once_with(mock_tech)
        mock_session.commit.assert_called_once()

    @patch("app.services.technology_service.get_database_session")
    def test_delete_custom_technology_not_found(self, mock_get_session):
        """Test suppression d'une technologie inexistante"""
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.delete_custom_technology(999)

        assert result is False
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()

    @patch("app.services.technology_service.get_database_session")
    def test_delete_custom_technology_db_error(self, mock_get_session):
        """Test suppression avec erreur DB"""
        mock_session = MagicMock()
        mock_session.query.side_effect = SQLAlchemyError("DB Error")
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = TechnologyService.delete_custom_technology(1)

        assert result is False

    @patch(
        "app.services.technology_service.TechnologyService.get_all_available_technologies"
    )
    def test_search_technologies(self, mock_get_all):
        """Test recherche de technologies"""
        mock_get_all.return_value = ["Python", "Java", "JavaScript", "SQL", "React"]

        # Recherche partielle
        result = TechnologyService.search_technologies("Java")
        assert "Java" in result
        assert "JavaScript" in result
        assert "Python" not in result

        # Recherche insensible à la casse
        result = TechnologyService.search_technologies("python")
        assert "Python" in result

        # Recherche sans résultat
        result = TechnologyService.search_technologies("xyz")
        assert result == []

    @patch("app.services.technology_service.TECHNOLOGIES_REFERENTIEL")
    @patch("app.services.technology_service.TechnologyService.get_custom_technologies")
    def test_get_technologies_by_category(self, mock_get_custom, mock_referentiel):
        """Test organisation des technologies par catégorie"""
        # Mock référentiel
        mock_referentiel.copy.return_value = {
            "Langages": ["Python", "Java"],
            "Frameworks": ["React", "Angular"],
        }

        # Mock technologies personnalisées
        mock_get_custom.return_value = [
            {"nom": "CustomLang", "categorie": "Langages"},
            {"nom": "CustomFramework", "categorie": "Frameworks"},
            {"nom": "NewCategoryTech", "categorie": "Nouvelles"},
        ]

        result = TechnologyService.get_technologies_by_category()

        # Vérifications
        assert "Langages" in result
        assert "Python" in result["Langages"]
        assert "Java" in result["Langages"]
        assert "CustomLang" in result["Langages"]

        assert "Frameworks" in result
        assert "React" in result["Frameworks"]
        assert "CustomFramework" in result["Frameworks"]

        assert "Nouvelles" in result
        assert "NewCategoryTech" in result["Nouvelles"]

        # Vérifier que chaque catégorie est triée
        for category in result:
            assert result[category] == sorted(result[category])
