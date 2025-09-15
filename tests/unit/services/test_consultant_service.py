"""Tests pour ConsultantService - Version corrigée avec vraies méthodes"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
from app.services.consultant_service import ConsultantService
from app.database.models import Consultant, Practice
from tests.fixtures.base_test import BaseServiceTest, TestDataFactory


class TestConsultantService(BaseServiceTest):
    """Tests pour ConsultantService avec les vraies méthodes disponibles"""

    def test_create_consultant_basic(self):
        """Test de base pour la création d'un consultant"""
        # Test de validation des champs requis
        data_incomplete = {"prenom": "Jean"}
        result = ConsultantService.create_consultant(data_incomplete)
        assert result is False
        
        # Test avec email invalide
        data_invalid_email = {
            "prenom": "Jean",
            "nom": "Dupont", 
            "email": "invalid_email"
        }
        result = ConsultantService.create_consultant(data_invalid_email)
        assert result is False

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_by_id_existing(self, mock_session):
        """Test de récupération d'un consultant existant par ID"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        mock_db.query.return_value.options.return_value.filter.return_value.first.return_value = mock_consultant
        
        # Test
        result = ConsultantService.get_consultant_by_id(1)
        
        # Vérifications
        assert result is not None
        assert result.prenom == "Jean"
        assert result.nom == "Dupont"

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_by_id_not_found(self, mock_session):
        """Test de récupération d'un consultant inexistant"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_db.query.return_value.options.return_value.filter.return_value.first.return_value = None
        
        # Test
        result = ConsultantService.get_consultant_by_id(999)
        
        # Vérifications
        assert result is None

    @patch('app.services.consultant_service.get_database_session')
    def test_create_consultant_valid_data(self, mock_session):
        """Test de création d'un consultant avec données valides"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock pour vérifier que l'email n'existe pas
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Données de test
        data = {
            "prenom": "Marie",
            "nom": "Martin",
            "email": "marie.martin@test.com",
            "telephone": "0123456789",
            "salaire": 55000,
            "practice_id": 1,
            "disponible": True
        }
        
        # Test
        result = ConsultantService.create_consultant(data)
        
        # Vérifications
        assert result is True
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @patch('app.services.consultant_service.get_database_session')
    def test_update_consultant_valid_data(self, mock_session):
        """Test de mise à jour d'un consultant"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock consultant existant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_consultant
        
        # Données de mise à jour
        data = {
            "telephone": "0987654321",
            "salaire": 60000
        }
        
        # Test
        result = ConsultantService.update_consultant(1, data)
        
        # Vérifications
        assert result is True
        mock_db.commit.assert_called_once()

    @patch('app.services.consultant_service.get_database_session')
    def test_delete_consultant_existing(self, mock_session):
        """Test de suppression d'un consultant existant"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_consultant
        
        # Test
        result = ConsultantService.delete_consultant(1)
        
        # Vérifications
        assert result is True
        mock_db.delete.assert_called_once_with(mock_consultant)
        mock_db.commit.assert_called_once()

    @patch('app.services.consultant_service.get_database_session')
    def test_search_consultants(self, mock_session):
        """Test de recherche de consultants"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock consultant trouvé
        mock_consultant = Mock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        
        mock_db.query.return_value.filter.return_value.all.return_value = [mock_consultant]
        
        # Test
        result = ConsultantService.search_consultants("Jean")
        
        # Vérifications
        assert len(result) == 1
        assert result[0].prenom == "Jean"

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultants_count(self, mock_session):
        """Test de comptage des consultants"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        mock_db.query.return_value.count.return_value = 42
        
        # Test
        result = ConsultantService.get_consultants_count()
        
        # Vérifications
        assert result == 42

    @patch('app.services.consultant_service.get_database_session')
    def test_get_all_consultants_objects(self, mock_session):
        """Test de récupération de tous les consultants comme objets"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock consultants
        mock_consultant1 = Mock()
        mock_consultant1.id = 1
        mock_consultant1.prenom = "Jean"
        mock_consultant2 = Mock()
        mock_consultant2.id = 2
        mock_consultant2.prenom = "Marie"

        mock_db.query.return_value.options.return_value.offset.return_value.limit.return_value.all.return_value = [mock_consultant1, mock_consultant2]

        # Test
        result = ConsultantService.get_all_consultants_objects(page=1, per_page=10)

        # Vérifications
        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    @patch('app.services.consultant_service.get_database_session')
    @patch('app.services.consultant_service.ConsultantService.get_all_consultants')
    def test_get_all_consultants(self, mock_get_all_consultants, mock_session):
        """Test de récupération de tous les consultants avec stats"""
        # Mock la fonction pour éviter le cache Streamlit
        mock_get_all_consultants.return_value = [
            {
                'id': 1,
                'prenom': 'Jean',
                'nom': 'Dupont',
                'email': 'jean@test.com',
                'disponibilite': True,
                'salaire_actuel': 50000,
                'date_creation': datetime.now(),
                'societe': 'Quanteam',
                'grade': 'Senior',
                'type_contrat': 'CDI',
                'practice_name': 'Tech',
                'nb_missions': 3,
                'cjm': 1440.0,
                'salaire_formatted': '50,000€',
                'cjm_formatted': '1,440€',
                'statut': '✅ Disponible',
                'experience_annees': 0,
                'experience_formatted': 'N/A'
            }
        ]

        # Test
        result = ConsultantService.get_all_consultants(page=1, per_page=10)

        # Vérifications
        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['prenom'] == "Jean"

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_with_stats(self, mock_session):
        """Test de récupération d'un consultant avec statistiques détaillées"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean@test.com"
        mock_consultant.disponibilite = True
        mock_consultant.telephone = "0123456789"
        mock_consultant.salaire_actuel = 50000
        mock_consultant.notes = "Notes test"
        mock_consultant.date_creation = datetime.now()
        mock_consultant.derniere_maj = datetime.now()

        # Mock les relations
        mock_competence = Mock()
        mock_competence.competence = Mock()
        mock_competence.competence.id = 1
        mock_competence.competence.nom = "Python"
        mock_competence.niveau_maitrise = "expert"
        mock_competence.annees_experience = 5.0

        mock_mission = Mock()
        mock_mission.id = 1
        mock_mission.nom_mission = "Mission Test"
        mock_mission.client = "Client Test"
        mock_mission.description = "Description test"
        mock_mission.date_debut = date.today()
        mock_mission.date_fin = None
        mock_mission.statut = "en_cours"
        mock_mission.revenus_generes = 10000

        mock_consultant.competences = [mock_competence]
        mock_consultant.missions = [mock_mission]

        # Configurer le mock pour simuler la chaîne de méthodes
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_consultant

        # Test
        result = ConsultantService.get_consultant_with_stats(1)

        # Vérifications
        assert result is not None
        assert result['id'] == 1
        assert result['prenom'] == "Jean"
        assert result['competences_count'] == 1
        assert result['missions_count'] == 1
        assert len(result['competences']) == 1
        assert len(result['missions']) == 1

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_by_email(self, mock_session):
        """Test de récupération d'un consultant par email"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.email = "jean@test.com"

        mock_db.query.return_value.filter.return_value.first.return_value = mock_consultant

        # Test
        result = ConsultantService.get_consultant_by_email("jean@test.com")

        # Vérifications
        assert result is not None
        assert result.email == "jean@test.com"

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultants_by_availability(self, mock_session):
        """Test de récupération des consultants par disponibilité"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock consultants disponibles
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.prenom = "Jean"
        mock_consultant.disponibilite = True

        mock_db.query.return_value.filter.return_value.all.return_value = [mock_consultant]

        # Test
        result = ConsultantService.get_consultants_by_availability(available=True)

        # Vérifications
        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['disponibilite'] is True

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_summary_stats(self, mock_session):
        """Test de récupération des statistiques générales"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock les compteurs avec side_effect pour retourner des valeurs différentes
        # Ordre: total_consultants, available_consultants, total_missions, active_missions
        mock_db.query.return_value.count.side_effect = [150, 200, 50]  # total_consultants, total_missions, active_missions
        mock_db.query.return_value.filter.return_value.count.side_effect = [120, 50]  # available_consultants, active_missions

        # Test
        result = ConsultantService.get_consultant_summary_stats()

        # Vérifications
        assert isinstance(result, dict)
        assert 'total_consultants' in result
        assert result['total_consultants'] == 150
        assert result['available_consultants'] == 120
        assert result['total_missions'] == 200
        assert result['active_missions'] == 50
        assert result['busy_consultants'] == 30  # 150 - 120

    @patch('app.services.consultant_service.ConsultantService.get_all_consultants_with_stats')
    def test_get_all_consultants_with_stats(self, mock_get_all_consultants_with_stats):
        """Test de récupération de tous les consultants avec statistiques complètes"""
        # Mock la fonction pour éviter le cache Streamlit
        mock_get_all_consultants_with_stats.return_value = [
            {
                'id': 1,
                'prenom': 'Jean',
                'nom': 'Dupont',
                'disponibilite': True,
                'salaire_actuel': 50000,
                'date_creation': datetime.now(),
                'derniere_maj': datetime.now(),
                'societe': 'Quanteam',
                'grade': 'Senior',
                'type_contrat': 'CDI',
                'practice_name': 'Tech',
                'nb_missions': 3,
                'cjm': 1440.0,
                'salaire_formatted': '50,000€',
                'cjm_formatted': '1,440€',
                'statut': '✅ Disponible',
                'experience_annees': 0,
                'experience_formatted': 'N/A',
                'stats': {
                    'nb_missions': 3,
                    'nb_competences': 5,
                    'experience_moyenne': 2.5
                }
            }
        ]

        # Test
        result = ConsultantService.get_all_consultants_with_stats(page=1, per_page=10)

        # Vérifications
        assert len(result) == 1
        assert result[0]['id'] == 1
        assert 'stats' in result[0]

    @patch('app.services.consultant_service.get_database_session')
    def test_search_consultants_optimized(self, mock_session):
        """Test de recherche optimisée de consultants"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock le résultat de la requête complexe
        mock_result = Mock()
        mock_result.id = 1
        mock_result.prenom = "Jean"
        mock_result.nom = "Dupont"
        mock_result.email = "jean@test.com"
        mock_result.telephone = "0123456789"
        mock_result.salaire_actuel = 50000
        mock_result.disponibilite = True
        mock_result.date_creation = datetime.now()
        mock_result.societe = "Quanteam"
        mock_result.date_entree_societe = None
        mock_result.date_sortie_societe = None
        mock_result.date_premiere_mission = None
        mock_result.grade = "Senior"
        mock_result.type_contrat = "CDI"
        mock_result.practice_name = "Tech"
        mock_result.nb_missions = 3

        # Configurer le mock pour simuler la chaîne de méthodes
        mock_query = Mock()
        mock_db.query.return_value = mock_query
        mock_query.outerjoin.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [mock_result]

        # Test
        result = ConsultantService.search_consultants_optimized("Jean", page=1, per_page=10)

        # Vérifications
        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['prenom'] == "Jean"
        assert result[0]['nb_missions'] == 3

    @patch('app.services.consultant_service.get_database_session')
    def test_save_cv_analysis(self, mock_session):
        """Test de sauvegarde d'analyse CV"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock consultant
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_db.query.return_value.filter.return_value.first.return_value = mock_consultant

        # Données d'analyse
        analysis_data = {
            "competences": ["Python", "SQL"],
            "experience": "5 ans",
            "missions": []
        }

        # Test
        result = ConsultantService.save_cv_analysis(1, analysis_data)

        # Vérifications
        assert result is True
        mock_db.commit.assert_called()

    def test_determine_skill_category(self):
        """Test de détermination de catégorie de compétence"""
        # Test compétences techniques
        result = ConsultantService._determine_skill_category("Python", "technique")
        assert result == "Backend"  # Python est dans backend_keywords

        # Test compétences frontend
        result = ConsultantService._determine_skill_category("React", "technique")
        assert result == "Frontend"

        # Test compétences fonctionnelles
        result = ConsultantService._determine_skill_category("Management", "fonctionnelle")
        assert result == "Management"

        # Test compétence inconnue
        result = ConsultantService._determine_skill_category("Unknown", "technique")
        assert result == "Technique"

    @patch('app.services.consultant_service.get_database_session')
    def test_create_consultant_duplicate_email(self, mock_session):
        """Test de création avec email déjà existant"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock consultant existant avec même email
        mock_existing = Mock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_existing

        # Données de test
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "existing@test.com"
        }

        # Test
        result = ConsultantService.create_consultant(data)

        # Vérifications
        assert result is False

    @patch('app.services.consultant_service.get_database_session')
    def test_update_consultant_not_found(self, mock_session):
        """Test de mise à jour d'un consultant inexistant"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Test
        result = ConsultantService.update_consultant(999, {"prenom": "Test"})

        # Vérifications
        assert result is False

    @patch('app.services.consultant_service.get_database_session')
    def test_delete_consultant_not_found(self, mock_session):
        """Test de suppression d'un consultant inexistant"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Test
        result = ConsultantService.delete_consultant(999)

        # Vérifications
        assert result is False

    @patch('app.services.consultant_service.get_database_session')
    def test_search_consultants_no_results(self, mock_session):
        """Test de recherche sans résultats"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        mock_db.query.return_value.filter.return_value.all.return_value = []

        # Test
        result = ConsultantService.search_consultants("nonexistent")

        # Vérifications
        assert len(result) == 0

    @patch('app.services.consultant_service.get_database_session')
    def test_get_consultant_by_email_not_found(self, mock_session):
        """Test de récupération par email inexistant"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db

        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Test
        result = ConsultantService.get_consultant_by_email("nonexistent@test.com")

        # Vérifications
        assert result is None
