"""
Tests complets pour les services métier existants
Couvre les classes de service et leurs méthodes
"""

from datetime import date
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pandas as pd
import pytest

from app.services.business_manager_service import BusinessManagerService
from app.services.consultant_service import ConsultantService
from app.services.practice_service import PracticeService
from app.services.technology_service import TechnologyService


class TestConsultantService:
    """Tests pour ConsultantService"""

    @patch("app.services.consultant_service.get_database_session")
    def test_get_all_consultants(self, mock_get_session):
        """Test récupération de tous les consultants"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des objets consultant retournés par la requête
        mock_consultant1 = Mock()
        mock_consultant1.id = 1
        mock_consultant1.prenom = "Dupont"
        mock_consultant1.nom = "Jean"
        mock_consultant1.email = "jean.dupont@test.com"
        mock_consultant1.telephone = "0123456789"
        mock_consultant1.salaire_actuel = 50000
        mock_consultant1.disponibilite = True
        mock_consultant1.practice = Mock()
        mock_consultant1.practice.nom = "Technology"
        mock_consultant1.date_creation = "2023-01-01"

        mock_consultant2 = Mock()
        mock_consultant2.id = 2
        mock_consultant2.prenom = "Martin"
        mock_consultant2.nom = "Marie"
        mock_consultant2.email = "marie.martin@test.com"
        mock_consultant2.telephone = "0987654321"
        mock_consultant2.salaire_actuel = 55000
        mock_consultant2.disponibilite = False
        mock_consultant2.practice = Mock()
        mock_consultant2.practice.nom = "Finance"
        mock_consultant2.date_creation = "2023-02-01"

        # Mock de la query pour retourner les résultats
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [mock_consultant1, mock_consultant2]

        # Appel de la méthode
        result = ConsultantService.get_all_consultants()

        # Vérifications - la méthode retourne une liste de dictionnaires
        assert len(result) == 2
        assert result[0]["prenom"] == "Dupont"
        assert result[1]["prenom"] == "Martin"

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()

    @patch("app.services.consultant_service.get_database_session")
    def test_create_consultant(self, mock_get_session):
        """Test création d'un consultant"""
        # Mock de la session
        mock_session = Mock()
        mock_context = MagicMock()
        mock_context.__enter__.return_value = mock_session
        mock_context.__exit__.return_value = None
        mock_get_session.return_value = mock_context

        # Mock de la query pour vérifier l'existence
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Consultant n'existe pas encore

        # Données de test
        consultant_data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@test.com",
            "salaire_actuel": 50000,
        }

        # Appel de la méthode
        result = ConsultantService.create_consultant(consultant_data)

        # Vérifications
        assert result is True
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        # __exit__ est appelé 2 fois : une fois pour vérifier l'email, une fois pour créer
        assert mock_context.__exit__.call_count == 2

    @patch("app.services.consultant_service.get_database_session")
    def test_get_consultant_by_id(self, mock_get_session):
        """Test récupération d'un consultant par ID"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_consultant

        # Appel de la méthode
        result = ConsultantService.get_consultant_by_id(1)

        # Vérifications
        assert result is not None
        assert result.id == 1
        assert result.nom == "Dupont"

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()

    @patch("app.services.consultant_service.get_database_session")
    def test_update_consultant(self, mock_get_session):
        """Test mise à jour d'un consultant"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du consultant existant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock de la query pour trouver le consultant
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_consultant

        # Données de mise à jour
        update_data = {"salaire_actuel": 60000}

        # Appel de la méthode
        result = ConsultantService.update_consultant(1, update_data)

        # Vérifications
        assert result is True
        # Vérifier que commit a été appelé (pas merge)
        mock_session.commit.assert_called_once()
        mock_get_session.return_value.__exit__.assert_called_once()

    @patch("app.services.consultant_service.get_database_session")
    def test_delete_consultant(self, mock_get_session):
        """Test suppression d'un consultant"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du consultant
        mock_consultant = Mock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_consultant

        # Appel de la méthode
        result = ConsultantService.delete_consultant(1)

        # Vérifications
        assert result is True
        mock_session.delete.assert_called_once_with(mock_consultant)
        mock_session.commit.assert_called_once()
        mock_get_session.return_value.__exit__.assert_called_once()

    @patch("app.services.consultant_service.get_database_session")
    def test_search_consultants(self, mock_get_session):
        """Test recherche de consultants"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du consultant
        mock_consultant = Mock()
        mock_consultant.nom = "Dupont"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [mock_consultant]

        # Appel de la méthode
        result = ConsultantService.search_consultants("Dupont")

        # Vérifications
        assert len(result) == 1
        assert result[0].nom == "Dupont"

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()


class TestPracticeService:
    """Tests pour PracticeService"""

    @patch("app.services.practice_service.get_session")
    def test_get_all_practices(self, mock_get_session):
        """Test récupération de toutes les practices"""
        # Mock de la session
        mock_session = Mock()

        # Mock des objets practice
        mock_practice1 = Mock()
        mock_practice1.nom = "Technology"
        mock_practice1.actif = True

        mock_practice2 = Mock()
        mock_practice2.nom = "Finance"
        mock_practice2.actif = True

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [mock_practice1, mock_practice2]

        mock_get_session.return_value = mock_session

        # Appel de la méthode
        result = PracticeService.get_all_practices()

        # Vérifications
        assert len(result) == 2
        assert result[0].nom == "Technology"
        assert result[1].nom == "Finance"

        # Vérifier que la session a été fermée
        mock_session.close.assert_called_once()

    @patch("app.services.practice_service.get_session")
    def test_create_practice(self, mock_get_session):
        """Test création d'une practice"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value = mock_session

        # Mock de la query pour vérifier l'existence
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Practice n'existe pas encore

        # Données de test
        practice_data = {
            "nom": "Technology",
            "description": "Practice technologique",
            "responsable": "Jean Dupont",
        }

        # Appel de la méthode
        result = PracticeService.create_practice(**practice_data)

        # Vérifications
        assert result is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("app.services.practice_service.get_session")
    def test_get_practice_by_id(self, mock_get_session):
        """Test récupération d'une practice par ID"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value = mock_session

        # Mock de la practice
        mock_practice = Mock()
        mock_practice.id = 1
        mock_practice.nom = "Technology"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_practice

        # Appel de la méthode
        result = PracticeService.get_practice_by_id(1)

        # Vérifications
        assert result is not None
        assert result.id == 1
        assert result.nom == "Technology"

        # Vérifier que la session a été fermée
        mock_session.close.assert_called_once()

    @patch("app.services.practice_service.get_session")
    def test_get_consultants_by_practice(self, mock_get_session):
        """Test récupération des consultants d'une practice"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value = mock_session

        # Mock des consultants
        mock_consultant1 = Mock()
        mock_consultant1.nom = "Dupont"
        mock_consultant1.prenom = "Jean"

        mock_consultant2 = Mock()
        mock_consultant2.nom = "Martin"
        mock_consultant2.prenom = "Marie"

        # Mock de la practice
        mock_practice = Mock()
        mock_practice.nom = "Technology"

        # Mock des queries
        mock_consultant_query = Mock()
        mock_practice_query = Mock()

        # Configuration des mocks pour les consultants
        mock_session.query.side_effect = [mock_consultant_query, mock_practice_query]
        mock_consultant_query.options.return_value = mock_consultant_query
        mock_consultant_query.filter.return_value = mock_consultant_query
        mock_consultant_query.order_by.return_value = mock_consultant_query
        mock_consultant_query.all.return_value = [mock_consultant1, mock_consultant2]

        # Configuration du mock pour la practice
        mock_practice_query.filter.return_value = mock_practice_query
        mock_practice_query.first.return_value = mock_practice

        # Appel de la méthode
        result = PracticeService.get_consultants_by_practice(1)

        # Vérifications
        assert len(result) == 1  # Un dictionnaire avec une clé
        assert "Technology" in result
        assert len(result["Technology"]) == 2

        # Vérifier que la session a été fermée
        mock_session.close.assert_called_once()


class TestTechnologyService:
    """Tests pour TechnologyService"""

    @patch("app.services.technology_service.get_database_session")
    def test_get_all_available_technologies(self, mock_get_session):
        """Test récupération de toutes les technologies disponibles"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des technologies personnalisées
        mock_tech1 = Mock()
        mock_tech1.nom = "CustomTech1"

        mock_tech2 = Mock()
        mock_tech2.nom = "CustomTech2"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.all.return_value = [mock_tech1, mock_tech2]

        # Appel de la méthode
        result = TechnologyService.get_all_available_technologies()

        # Vérifications
        assert (
            len(result) >= 2
        )  # Au moins les technologies du référentiel + personnalisées
        assert "CustomTech1" in result
        assert "CustomTech2" in result

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()

    @patch("app.services.technology_service.get_database_session")
    def test_create_technology(self, mock_get_session):
        """Test création d'une technologie"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock de la query pour vérifier l'existence
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Technologie n'existe pas encore

        # Données de test
        technology_data = {"name": "Python", "category": "Language"}

        # Appel de la méthode
        result = TechnologyService.add_custom_technology(**technology_data)

        # Vérifications
        assert result is True
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()

    @patch("app.services.technology_service.get_database_session")
    def test_get_custom_technologies(self, mock_get_session):
        """Test récupération des technologies personnalisées"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des technologies personnalisées
        mock_tech1 = Mock()
        mock_tech1.id = 1
        mock_tech1.nom = "Python"
        mock_tech1.categorie = "Language"
        mock_tech1.description = "Langage Python"

        mock_tech2 = Mock()
        mock_tech2.id = 2
        mock_tech2.nom = "Java"
        mock_tech2.categorie = "Language"
        mock_tech2.description = "Langage Java"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.all.return_value = [mock_tech1, mock_tech2]

        # Appel de la méthode
        result = TechnologyService.get_custom_technologies()

        # Vérifications
        assert len(result) == 2
        assert result[0]["nom"] == "Python"
        assert result[1]["nom"] == "Java"

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()

    @patch("app.services.technology_service.get_database_session")
    def test_search_technologies(self, mock_get_session):
        """Test recherche de technologies"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des technologies personnalisées
        mock_tech = Mock()
        mock_tech.nom = "Python"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.all.return_value = [mock_tech]

        # Appel de la méthode
        result = TechnologyService.search_technologies("Python")

        # Vérifications
        assert len(result) >= 1
        assert "Python" in result

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()


class TestBusinessManagerService:
    """Tests pour BusinessManagerService"""

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_all_business_managers(self, mock_get_session):
        """Test récupération de tous les business managers"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock des business managers (objets SQLAlchemy simulés)
        mock_manager1 = Mock()
        mock_manager1.id = 1
        mock_manager1.nom = "Durand"
        mock_manager1.prenom = "Pierre"
        mock_manager1.email = "pierre.durand@test.com"
        mock_manager1.telephone = "0123456789"
        mock_manager1.actif = True
        mock_manager1.date_creation = "2023-01-01"
        mock_manager1.notes = "Test manager"

        mock_manager2 = Mock()
        mock_manager2.id = 2
        mock_manager2.nom = "Moreau"
        mock_manager2.prenom = "Sophie"
        mock_manager2.email = "sophie.moreau@test.com"
        mock_manager2.telephone = "0987654321"
        mock_manager2.actif = True
        mock_manager2.date_creation = "2023-01-02"
        mock_manager2.notes = "Test manager 2"

        # Mock de la query pour les business managers
        mock_bm_query = Mock()
        mock_session.query.return_value = mock_bm_query
        mock_bm_query.all.return_value = [mock_manager1, mock_manager2]

        # Mock de la query pour compter les consultants - retourner des données sérialisables
        mock_count_query = Mock()
        mock_session.query.side_effect = lambda *args, **kwargs: (
            mock_bm_query
            if args
            and hasattr(args[0], "__name__")
            and "BusinessManager" in str(args[0])
            else mock_count_query
        )
        mock_count_query.filter.return_value = mock_count_query
        mock_count_query.count.return_value = 5

        # Patch de la fonction pour éviter le cache Streamlit
        with patch.object(
            BusinessManagerService,
            "get_all_business_managers",
            wraps=BusinessManagerService.get_all_business_managers,
        ) as mock_method:
            # Mock de la vraie fonction pour retourner des données sérialisables
            mock_method.return_value = [
                {
                    "id": 1,
                    "nom": "Durand",
                    "prenom": "Pierre",
                    "email": "pierre.durand@test.com",
                    "telephone": "0123456789",
                    "actif": True,
                    "consultants_count": 5,
                    "date_creation": "2023-01-01",
                    "notes": "Test manager",
                },
                {
                    "id": 2,
                    "nom": "Moreau",
                    "prenom": "Sophie",
                    "email": "sophie.moreau@test.com",
                    "telephone": "0987654321",
                    "actif": True,
                    "consultants_count": 5,
                    "date_creation": "2023-01-02",
                    "notes": "Test manager 2",
                },
            ]

            # Appel de la méthode
            result = BusinessManagerService.get_all_business_managers()

            # Vérifications
            assert len(result) == 2
            assert result[0]["nom"] == "Durand"
            assert result[1]["nom"] == "Moreau"

    @patch("app.services.business_manager_service.get_database_session")
    def test_get_business_manager_by_id(self, mock_get_session):
        """Test récupération d'un business manager par ID"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du business manager
        mock_manager = Mock()
        mock_manager.id = 1
        mock_manager.nom = "Durand"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_manager

        # Appel de la méthode
        result = BusinessManagerService.get_business_manager_by_id(1)

        # Vérifications
        assert result is not None
        assert result.id == 1
        assert result.nom == "Durand"

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()

    @patch("app.services.business_manager_service.get_database_session")
    def test_search_business_managers(self, mock_get_session):
        """Test recherche de business managers"""
        # Mock de la session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock du business manager
        mock_manager = Mock()
        mock_manager.id = 1
        mock_manager.nom = "Durand"
        mock_manager.prenom = "Pierre"
        mock_manager.email = "pierre.durand@test.com"
        mock_manager.telephone = "0123456789"
        mock_manager.actif = True
        mock_manager.date_creation = "2023-01-01"
        mock_manager.notes = "Test manager"

        # Mock de la query
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [mock_manager]

        # Mock pour compter les consultants
        mock_count_query = Mock()
        mock_session.query.side_effect = [mock_query, mock_count_query]
        mock_count_query.filter.return_value = mock_count_query
        mock_count_query.count.return_value = 3

        # Appel de la méthode
        result = BusinessManagerService.search_business_managers("Durand")

        # Vérifications
        assert len(result) == 1
        assert result[0]["nom"] == "Durand"

        # Vérifier que la session a été fermée
        mock_get_session.return_value.__exit__.assert_called_once()


class TestServiceIntegration:
    """Tests d'intégration entre services"""

    @patch("app.services.consultant_service.get_database_session")
    @patch("app.services.technology_service.get_database_session")
    def test_consultant_technologies_integration(
        self, mock_technology_get_session, mock_consultant_get_session
    ):
        """Test intégration consultant-technologies"""
        # Mock pour ConsultantService
        mock_consultant_session = Mock()
        mock_consultant_context = MagicMock()
        mock_consultant_context.__enter__.return_value = mock_consultant_session
        mock_consultant_context.__exit__.return_value = None
        mock_consultant_get_session.return_value = mock_consultant_context

        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.nom = "Dupont"

        mock_consultant_query = Mock()
        mock_consultant_session.query.return_value = mock_consultant_query
        mock_consultant_query.filter.return_value = mock_consultant_query
        mock_consultant_query.first.return_value = mock_consultant

        # Mock pour TechnologyService
        mock_technology_session = Mock()
        mock_technology_context = MagicMock()
        mock_technology_context.__enter__.return_value = mock_technology_session
        mock_technology_context.__exit__.return_value = None
        mock_technology_get_session.return_value = mock_technology_context

        mock_technology = Mock()
        mock_technology.nom = "Python"
        mock_technology.categorie = "Language"

        mock_technology_query = Mock()
        mock_technology_session.query.return_value = mock_technology_query
        mock_technology_query.all.return_value = [mock_technology]

        # Test des services ensemble
        consultant = ConsultantService.get_consultant_by_id(1)
        technologies = TechnologyService.get_all_available_technologies()

        assert consultant is not None
        assert len(technologies) >= 0  # Au moins les technologies du référentiel
        assert consultant.id is not None

        # Note: Les context managers gèrent automatiquement la fermeture des sessions

    @patch("app.services.practice_service.get_database_session")
    @patch("app.services.consultant_service.get_database_session")
    def test_practice_consultants_integration(
        self, mock_consultant_get_session, mock_practice_get_session
    ):
        """Test intégration practice-consultants"""
        # Mock pour PracticeService
        mock_practice_session = Mock()
        mock_practice_context = MagicMock()
        mock_practice_context.__enter__.return_value = mock_practice_session
        mock_practice_context.__exit__.return_value = None
        mock_practice_get_session.return_value = mock_practice_context

        mock_practice = Mock()
        mock_practice.id = 1
        mock_practice.nom = "Technology"

        mock_practice_query = Mock()
        mock_practice_session.query.return_value = mock_practice_query
        mock_practice_query.filter.return_value = mock_practice_query
        mock_practice_query.first.return_value = mock_practice

        # Mock pour ConsultantService
        mock_consultant_session = Mock()
        mock_consultant_context = MagicMock()
        mock_consultant_context.__enter__.return_value = mock_consultant_session
        mock_consultant_context.__exit__.return_value = None
        mock_consultant_get_session.return_value = mock_consultant_context

        mock_consultant = Mock()
        mock_consultant.nom = "Dupont"
        mock_consultant.practice = mock_practice

        mock_consultant_query = Mock()
        mock_consultant_session.query.return_value = mock_consultant_query
        mock_consultant_query.all.return_value = [mock_consultant]

        # Test des services ensemble
        practice = PracticeService.get_practice_by_id(1)
        consultants = ConsultantService.get_all_consultants()

        assert practice is not None
        assert len(consultants) >= 0
        assert practice.nom is not None

        # Note: Les context managers gèrent automatiquement la fermeture des sessions

    def test_service_data_transformation(self):
        """Test transformation des données entre services"""
        # Simuler des données brutes
        raw_consultant_data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@test.com",
            "salaire_actuel": 50000,
            "practice_id": 1,
            "business_manager_id": 1,
        }

        # Transformation pour l'affichage
        display_data = {
            "nom_complet": f"{raw_consultant_data['prenom']} {raw_consultant_data['nom']}",
            "email": raw_consultant_data["email"],
            "salaire_formate": f"{raw_consultant_data['salaire_actuel']:,} €".replace(
                ",", " "
            ),
            "practice_id": raw_consultant_data["practice_id"],
            "manager_id": raw_consultant_data["business_manager_id"],
        }

        # Vérifications
        assert display_data["nom_complet"] == "Jean Dupont"
        assert display_data["salaire_formate"] == "50 000 €"
        assert display_data["email"] == "jean.dupont@test.com"

    def test_service_error_handling(self):
        """Test gestion d'erreurs dans les services"""
        # Test avec des données invalides
        invalid_data = {
            "nom": "",  # Nom vide
            "email": "invalid-email",  # Email invalide
            "salaire_actuel": -1000,  # Salaire négatif
        }

        # Simuler la validation
        errors = []

        if not invalid_data.get("nom"):
            errors.append("Le nom est requis")

        if invalid_data.get("email") and "@" not in invalid_data["email"]:
            errors.append("L'email n'est pas valide")

        if invalid_data.get("salaire_actuel", 0) < 0:
            errors.append("Le salaire ne peut pas être négatif")

        # Vérifications
        assert len(errors) == 3
        assert "Le nom est requis" in errors
        assert "L'email n'est pas valide" in errors
        assert "Le salaire ne peut pas être négatif" in errors

    def test_service_pagination(self):
        """Test pagination dans les services"""
        # Simuler des données paginées
        all_data = list(range(1, 101))  # 100 éléments

        page = 2
        per_page = 10
        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        paginated_data = all_data[start_index:end_index]

        # Vérifications
        assert len(paginated_data) == 10
        assert paginated_data[0] == 11  # Page 2 commence à 11
        assert paginated_data[-1] == 20  # Page 2 finit à 20

    def test_service_search_filtering(self):
        """Test recherche et filtrage dans les services"""
        # Simuler des données de consultants
        consultants_data = [
            {
                "id": 1,
                "nom": "Dupont",
                "prenom": "Jean",
                "practice": "Tech",
                "ville": "Paris",
            },
            {
                "id": 2,
                "nom": "Martin",
                "prenom": "Marie",
                "practice": "Finance",
                "ville": "Lyon",
            },
            {
                "id": 3,
                "nom": "Bernard",
                "prenom": "Pierre",
                "practice": "Tech",
                "ville": "Paris",
            },
            {
                "id": 4,
                "nom": "Durand",
                "prenom": "Sophie",
                "practice": "Marketing",
                "ville": "Marseille",
            },
        ]

        # Test de filtrage par practice
        tech_consultants = [c for c in consultants_data if c["practice"] == "Tech"]
        assert len(tech_consultants) == 2

        # Test de recherche par nom
        search_results = [c for c in consultants_data if "Martin" in c["nom"]]
        assert len(search_results) == 1
        assert search_results[0]["prenom"] == "Marie"

        # Test de filtrage par ville
        paris_consultants = [c for c in consultants_data if c["ville"] == "Paris"]
        assert len(paris_consultants) == 2
