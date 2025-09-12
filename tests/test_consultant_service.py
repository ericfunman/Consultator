"""Tests pour ConsultantService - Version corrigée avec vraies méthodes"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
from app.services.consultant_service import ConsultantService
from app.database.models import Consultant, Practice


class TestConsultantService:
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
    def test_get_available_consultants(self, mock_session):
        """Test de récupération des consultants disponibles"""
        # Mock session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock consultants disponibles
        mock_consultant1 = Mock()
        mock_consultant1.disponibilite = True
        mock_consultant2 = Mock()
        mock_consultant2.disponibilite = True
        
        mock_db.query.return_value.filter.return_value.all.return_value = [mock_consultant1, mock_consultant2]
        
        # Test
        result = ConsultantService.get_available_consultants()
        
        # Vérifications
        assert len(result) == 2
        assert all(c.disponibilite for c in result)
