"""
Tests de non-régression pour les fonctionnalités critiques

Ce module teste les fonctionnalités essentielles de Consultator pour s'assurer
qu'aucune régression n'est introduite lors des développements.
"""
import pytest
from unittest.mock import Mock, patch
import tempfile
import os
from datetime import datetime, date

from app.database.models import (
    Consultant, Mission, Competence, Practice, 
    VSA_Mission, BusinessManager, CV
)
from app.services.consultant_service import ConsultantService
from app.database.database import get_session


class TestCoreFeatures:
    """Tests de non-régression pour les fonctionnalités critiques"""
    
    def test_consultant_creation_complete_workflow(self, db_session):
        """Test du workflow complet de création d'un consultant"""
        # Given - Données de test complètes
        consultant_data = {
            'nom': 'DUPONT',
            'prenom': 'Jean',
            'email': 'jean.dupont@test.com',
            'telephone': '0123456789',
            'ville': 'Paris',
            'date_naissance': date(1985, 1, 1),
            'date_entree_societe': date(2020, 1, 1),
            'salaire_actuel': 50000,
            'tjm_actuel': 500,
            'niveau_etude': 'BAC+5',
            'ecole': 'SUPINFO',
            'statut_societe': 'EN_POSTE'
        }
        
        # When - Création du consultant
        consultant = Consultant(**consultant_data)
        db_session.add(consultant)
        db_session.commit()
        
        # Then - Vérifications complètes
        assert consultant.id is not None
        assert consultant.nom_complet == 'DUPONT Jean'
        assert consultant.experience_annees > 0  # Calculé automatiquement
        assert consultant.date_disponibilite is not None
        
        # Vérification que le consultant peut être récupéré
        retrieved = db_session.query(Consultant).filter_by(email='jean.dupont@test.com').first()
        assert retrieved is not None
        assert retrieved.nom == 'DUPONT'
    
    def test_mission_assignment_workflow(self, db_session):
        """Test du workflow complet d'affectation de mission"""
        # Given - Consultant existant
        consultant = Consultant(
            nom='MARTIN', prenom='Marie',
            email='marie.martin@test.com',
            statut_societe='EN_POSTE'
        )
        db_session.add(consultant)
        db_session.flush()  # Pour obtenir l'ID
        
        # When - Création d'une mission
        mission = Mission(
            consultant_id=consultant.id,
            nom_mission='Mission Test',
            client='Client Test',
            date_debut=date.today(),
            taux_journalier=600,
            description='Test mission assignment'
        )
        db_session.add(mission)
        db_session.commit()
        
        # Then - Vérifications
        assert mission.id is not None
        assert mission.consultant_id == consultant.id
        assert mission.duree_jours is not None  # Calculé automatiquement
        
        # Vérification de la relation
        consultant_missions = db_session.query(Mission).filter_by(consultant_id=consultant.id).all()
        assert len(consultant_missions) == 1
        assert consultant_missions[0].nom_mission == 'Mission Test'
    
    def test_competence_management_workflow(self, db_session):
        """Test du workflow de gestion des compétences"""
        # Given - Consultant existant
        consultant = Consultant(
            nom='BERNARD', prenom='Paul',
            email='paul.bernard@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        # When - Ajout de compétences
        competences = [
            Competence(consultant_id=consultant.id, nom='Python', niveau=4, annees_experience=3),
            Competence(consultant_id=consultant.id, nom='Django', niveau=3, annees_experience=2),
            Competence(consultant_id=consultant.id, nom='PostgreSQL', niveau=3, annees_experience=2)
        ]
        
        for comp in competences:
            db_session.add(comp)
        db_session.commit()
        
        # Then - Vérifications
        consultant_competences = db_session.query(Competence).filter_by(consultant_id=consultant.id).all()
        assert len(consultant_competences) == 3
        
        # Vérification des niveaux et expérience
        python_comp = next((c for c in consultant_competences if c.nom == 'Python'), None)
        assert python_comp is not None
        assert python_comp.niveau == 4
        assert python_comp.annees_experience == 3
    
    def test_business_manager_assignment(self, db_session):
        """Test de l'affectation d'un business manager"""
        # Given - BM et consultant
        bm = BusinessManager(
            nom='DURAND', prenom='Sophie',
            email='sophie.durand@test.com'
        )
        consultant = Consultant(
            nom='LEFEBVRE', prenom='Thomas',
            email='thomas.lefebvre@test.com'
        )
        
        db_session.add_all([bm, consultant])
        db_session.flush()
        
        # When - Attribution du BM
        consultant.business_manager_id = bm.id
        db_session.commit()
        
        # Then - Vérifications
        assert consultant.business_manager_id == bm.id
        
        # Test de la relation inverse
        bm_consultants = db_session.query(Consultant).filter_by(business_manager_id=bm.id).all()
        assert len(bm_consultants) == 1
        assert bm_consultants[0].nom == 'LEFEBVRE'
    
    def test_practice_consultant_relationship(self, db_session):
        """Test de la relation consultant-practice"""
        # Given - Practice et consultant
        practice = Practice(nom='Data Science', description='Practice Data Science')
        consultant = Consultant(
            nom='MOREAU', prenom='Julie',
            email='julie.moreau@test.com'
        )
        
        db_session.add_all([practice, consultant])
        db_session.flush()
        
        # When - Attribution de la practice
        consultant.practice_id = practice.id
        db_session.commit()
        
        # Then - Vérifications
        assert consultant.practice_id == practice.id
        
        # Test du calcul du nombre de consultants
        practice_consultants = db_session.query(Consultant).filter_by(practice_id=practice.id).all()
        assert len(practice_consultants) == 1


class TestDataIntegrity:
    """Tests de non-régression pour l'intégrité des données"""
    
    def test_unique_constraints_respected(self, db_session):
        """Test que les contraintes d'unicité sont respectées"""
        # Given - Premier consultant
        consultant1 = Consultant(
            nom='TEST', prenom='User1',
            email='test.unique@test.com'
        )
        db_session.add(consultant1)
        db_session.commit()
        
        # When/Then - Tentative de création d'un doublon
        consultant2 = Consultant(
            nom='TEST', prenom='User2',
            email='test.unique@test.com'  # Email identique
        )
        db_session.add(consultant2)
        
        with pytest.raises(Exception):  # Violation de contrainte d'unicité
            db_session.commit()
    
    def test_foreign_key_constraints(self, db_session):
        """Test des contraintes de clés étrangères"""
        # When/Then - Tentative de création avec FK invalide
        mission = Mission(
            consultant_id=99999,  # ID inexistant
            nom_mission='Mission Invalide',
            client='Client Test'
        )
        db_session.add(mission)
        
        with pytest.raises(Exception):  # Violation de contrainte FK
            db_session.commit()
    
    def test_cascade_deletions(self, db_session):
        """Test des suppressions en cascade"""
        # Given - Consultant avec missions et compétences
        consultant = Consultant(
            nom='CASCADE', prenom='Test',
            email='cascade.test@test.com'
        )
        db_session.add(consultant)
        db_session.flush()
        
        mission = Mission(
            consultant_id=consultant.id,
            nom_mission='Mission à supprimer',
            client='Client Test'
        )
        competence = Competence(
            consultant_id=consultant.id,
            nom='Compétence à supprimer',
            niveau=3
        )
        
        db_session.add_all([mission, competence])
        db_session.commit()
        
        # When - Suppression du consultant
        db_session.delete(consultant)
        db_session.commit()
        
        # Then - Vérification que les relations sont supprimées
        remaining_missions = db_session.query(Mission).filter_by(consultant_id=consultant.id).all()
        remaining_competences = db_session.query(Competence).filter_by(consultant_id=consultant.id).all()
        
        assert len(remaining_missions) == 0
        assert len(remaining_competences) == 0


class TestPerformanceRegression:
    """Tests de non-régression des performances"""
    
    def test_bulk_consultant_creation_performance(self, db_session):
        """Test que la création en masse reste performante"""
        import time
        
        # Given - Données pour création en masse
        consultants_data = []
        for i in range(100):
            consultants_data.append(Consultant(
                nom=f'PERF{i:03d}',
                prenom=f'Test{i}',
                email=f'perf.test{i}@test.com'
            ))
        
        # When - Mesure du temps de création
        start_time = time.time()
        db_session.add_all(consultants_data)
        db_session.commit()
        end_time = time.time()
        
        # Then - Vérification du temps (doit rester sous 5 secondes)
        creation_time = end_time - start_time
        assert creation_time < 5.0, f"Création trop lente: {creation_time:.2f}s"
        
        # Vérification que tous les consultants sont créés
        created_count = db_session.query(Consultant).filter(Consultant.nom.like('PERF%')).count()
        assert created_count == 100
    
    def test_complex_query_performance(self, db_session):
        """Test des performances des requêtes complexes"""
        import time
        
        # Given - Données de test avec relations
        practice = Practice(nom='Performance Test Practice')
        db_session.add(practice)
        db_session.flush()
        
        for i in range(50):
            consultant = Consultant(
                nom=f'QUERY{i:02d}',
                prenom=f'Test{i}',
                email=f'query.test{i}@test.com',
                practice_id=practice.id
            )
            db_session.add(consultant)
        
        db_session.commit()
        
        # When - Requête complexe avec jointures
        start_time = time.time()
        
        results = db_session.query(Consultant)\
            .join(Practice)\
            .filter(Practice.nom == 'Performance Test Practice')\
            .filter(Consultant.nom.like('QUERY%'))\
            .order_by(Consultant.nom)\
            .all()
        
        end_time = time.time()
        
        # Then - Vérification du temps et des résultats
        query_time = end_time - start_time
        assert query_time < 2.0, f"Requête trop lente: {query_time:.2f}s"
        assert len(results) == 50