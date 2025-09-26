"""
Tests de non-régression pour les services

Ce module teste les services métier pour éviter les régressions
dans la logique business.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import date, datetime
import tempfile

from app.services.consultant_service import ConsultantService
from app.database.models import Consultant, Mission, Competence, Practice


class TestConsultantServiceRegression:
    """Tests de non-régression pour ConsultantService"""
    
    def test_get_consultant_by_id_regression(self, db_session):
        """Test de non-régression pour la récupération par ID"""
        # Given - Consultant existant
        consultant = Consultant(
            nom='SERVICE', prenom='Test',
            email='service.test@test.com'
        )
        db_session.add(consultant)
        db_session.commit()
        
        # When - Récupération par ID
        with patch('app.services.consultant_service.get_session') as mock_session:
            mock_session.return_value.__enter__.return_value = db_session
            
            result = ConsultantService.get_consultant_by_id(consultant.id)
        
        # Then - Consultant récupéré correctement
        assert result is not None
        assert result.nom == 'SERVICE'
        assert result.prenom == 'Test'
    
    def test_get_consultant_by_id_not_found(self, db_session):
        """Test de non-régression pour ID inexistant"""
        # When - Récupération d'un ID inexistant
        with patch('app.services.consultant_service.get_session') as mock_session:
            mock_session.return_value.__enter__.return_value = db_session
            
            result = ConsultantService.get_consultant_by_id(99999)
        
        # Then - Doit retourner None
        assert result is None
    
    def test_search_consultants_regression(self, db_session):
        """Test de non-régression pour la recherche"""
        # Given - Plusieurs consultants
        consultants = [
            Consultant(nom='SEARCH1', prenom='Jean', email='jean.search1@test.com'),
            Consultant(nom='SEARCH2', prenom='Marie', email='marie.search2@test.com'),
            Consultant(nom='OTHER', prenom='Paul', email='paul.other@test.com'),
        ]
        
        for consultant in consultants:
            db_session.add(consultant)
        db_session.commit()
        
        # When - Recherche par nom
        with patch('app.services.consultant_service.get_session') as mock_session:
            mock_session.return_value.__enter__.return_value = db_session
            
            results = ConsultantService.search_consultants('SEARCH')
        
        # Then - Seuls les consultants correspondants
        assert len(results) == 2
        assert all('SEARCH' in r.nom for r in results)
    
    def test_create_consultant_regression(self, db_session):
        """Test de non-régression pour la création"""
        # Given - Données valides
        consultant_data = {
            'nom': 'CREATION',
            'prenom': 'Test',
            'email': 'creation.test@test.com',
            'telephone': '0123456789'
        }
        
        # When - Création
        with patch('app.services.consultant_service.get_session') as mock_session:
            mock_session.return_value.__enter__.return_value = db_session
            
            result = ConsultantService.create_consultant(consultant_data)
        
        # Then - Consultant créé
        assert result is not None
        assert result.nom == 'CREATION'
        assert result.email == 'creation.test@test.com'
    
    def test_update_consultant_regression(self, db_session):
        """Test de non-régression pour la mise à jour"""
        # Given - Consultant existant
        consultant = Consultant(
            nom='UPDATE', prenom='Original',
            email='update.original@test.com'
        )
        db_session.add(consultant)
        db_session.commit()
        
        # When - Mise à jour
        update_data = {'prenom': 'Modified', 'telephone': '0987654321'}
        
        with patch('app.services.consultant_service.get_session') as mock_session:
            mock_session.return_value.__enter__.return_value = db_session
            
            result = ConsultantService.update_consultant(consultant.id, update_data)
        
        # Then - Données mises à jour
        assert result is not None
        assert result.prenom == 'Modified'
        assert result.telephone == '0987654321'
        assert result.nom == 'UPDATE'  # Inchangé
    
    def test_get_consultants_with_pagination_regression(self, db_session):
        """Test de non-régression pour la pagination"""
        # Given - Plusieurs consultants
        for i in range(25):
            consultant = Consultant(
                nom=f'PAGE{i:02d}',
                prenom=f'Test{i}',
                email=f'page{i}@test.com'
            )
            db_session.add(consultant)
        db_session.commit()
        
        # When - Récupération avec pagination
        with patch('app.services.consultant_service.get_session') as mock_session:
            mock_session.return_value.__enter__.return_value = db_session
            
            page1 = ConsultantService.get_all_consultants(page=1, per_page=10)
            page2 = ConsultantService.get_all_consultants(page=2, per_page=10)
            page3 = ConsultantService.get_all_consultants(page=3, per_page=10)
        
        # Then - Pagination correcte
        assert len(page1) == 10
        assert len(page2) == 10
        assert len(page3) == 5  # 25 total, donc 5 sur la dernière page
        
        # Pas de doublons entre les pages
        all_ids = [c.id for c in page1] + [c.id for c in page2] + [c.id for c in page3]
        assert len(all_ids) == len(set(all_ids))  # Tous uniques


class TestBusinessLogicRegression:
    """Tests de non-régression pour la logique métier"""
    
    def test_consultant_experience_calculation(self, db_session):
        """Test de calcul de l'expérience"""
        # Given - Consultant avec date d'entrée
        consultant = Consultant(
            nom='EXPERIENCE', prenom='Test',
            email='experience.test@test.com',
            date_entree_societe=date(2020, 1, 1)
        )
        db_session.add(consultant)
        db_session.commit()
        
        # When/Then - Calcul automatique de l'expérience
        assert consultant.experience_annees > 0
        expected_years = (date.today() - date(2020, 1, 1)).days / 365.25
        assert abs(consultant.experience_annees - expected_years) < 0.1
    
    def test_consultant_availability_logic(self, db_session):
        """Test de logique de disponibilité"""
        # Given - Consultant avec missions
        consultant = Consultant(
            nom='AVAILABILITY', prenom='Test',
            email='availability.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # Mission en cours
        current_mission = Mission(
            consultant_id=consultant.id,
            nom_mission='Mission Actuelle',
            client='Client Test',
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 12, 31)
        )
        db_session.add(current_mission)
        db_session.commit()
        
        # When/Then - Date de disponibilité basée sur la mission
        expected_availability = date(2025, 1, 1)  # Jour après la fin de mission
        assert consultant.date_disponibilite == expected_availability
    
    def test_mission_duration_calculation(self, db_session):
        """Test de calcul de durée de mission"""
        # Given - Mission avec dates
        consultant = Consultant(
            nom='DURATION', prenom='Test',
            email='duration.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        mission = Mission(
            consultant_id=consultant.id,
            nom_mission='Mission Durée',
            client='Client Test',
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 3, 31)  # 3 mois
        )
        db_session.add(mission)
        db_session.commit()
        
        # When/Then - Durée calculée automatiquement
        expected_days = (date(2024, 3, 31) - date(2024, 1, 1)).days + 1
        assert mission.duree_jours == expected_days
    
    def test_consultant_status_logic(self, db_session):
        """Test de logique de statut consultant"""
        # Given - Consultant avec statut
        consultant = Consultant(
            nom='STATUS', prenom='Test',
            email='status.test@test.com',
            statut_societe='EN_POSTE',
            date_depart_prevue=None
        )
        db_session.add(consultant)
        db_session.commit()
        
        # When/Then - Propriétés calculées basées sur le statut
        assert consultant.statut_societe == 'EN_POSTE'
        # Add more business logic tests as needed
    
    def test_competence_level_validation(self, db_session):
        """Test de validation des niveaux de compétence"""
        # Given - Consultant et compétence
        consultant = Consultant(
            nom='SKILL', prenom='Test',
            email='skill.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # When - Compétence avec niveau valide
        competence = Competence(
            consultant_id=consultant.id,
            nom='Python',
            niveau=4,  # 1-5 scale
            annees_experience=3
        )
        db_session.add(competence)
        db_session.commit()
        
        # Then - Compétence sauvée correctement
        saved_competence = db_session.query(Competence)\
            .filter_by(consultant_id=consultant.id, nom='Python')\
            .first()
        
        assert saved_competence is not None
        assert saved_competence.niveau == 4
        assert saved_competence.annees_experience == 3


class TestDataConsistencyRegression:
    """Tests de cohérence des données"""
    
    def test_referential_integrity_maintained(self, db_session):
        """Test du maintien de l'intégrité référentielle"""
        # Given - Données liées
        practice = Practice(nom='Test Practice')
        consultant = Consultant(
            nom='INTEGRITY', prenom='Test',
            email='integrity.test@test.com'
        )
        
        db_session.add_all([practice, consultant])
        db_session.flush()
        
        consultant.practice_id = practice.id
        db_session.commit()
        
        # When - Vérification des relations
        consultant_with_practice = db_session.query(Consultant)\
            .filter_by(id=consultant.id)\
            .first()
        
        # Then - Relations maintenues
        assert consultant_with_practice.practice_id == practice.id
    
    def test_cascade_operations_regression(self, db_session):
        """Test des opérations en cascade"""
        # Given - Consultant avec données liées
        consultant = Consultant(
            nom='CASCADE', prenom='Test',
            email='cascade.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # Données liées
        competence = Competence(
            consultant_id=consultant.id,
            nom='Test Skill',
            niveau=3
        )
        mission = Mission(
            consultant_id=consultant.id,
            nom_mission='Test Mission',
            client='Test Client'
        )
        
        db_session.add_all([competence, mission])
        db_session.commit()
        
        # When - Suppression du consultant
        consultant_id = consultant.id
        db_session.delete(consultant)
        db_session.commit()
        
        # Then - Données liées supprimées
        remaining_competences = db_session.query(Competence)\
            .filter_by(consultant_id=consultant_id)\
            .count()
        remaining_missions = db_session.query(Mission)\
            .filter_by(consultant_id=consultant_id)\
            .count()
        
        assert remaining_competences == 0
        assert remaining_missions == 0