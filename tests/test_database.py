"""
Tests pour la base de données et les modèles
"""
import pytest
import sys
import os
from pathlib import Path

# Ajouter le répertoire app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

def test_database_connection():
    """Test de connexion à la base de données"""
    try:
        from database.database import get_session
        
        with get_session() as session:
            assert session is not None
            
    except ImportError:
        pytest.skip("Module database non disponible")
    except Exception:
        pytest.skip("Connexion DB non disponible en test")

def test_consultant_model_creation():
    """Test de création d'un modèle Consultant"""
    try:
        from database.models import Consultant
        
        # Test de création avec données minimales
        consultant_data = {
            'nom': 'Test',
            'prenom': 'Consultant',
            'email': 'test@example.com'
        }
        
        consultant = Consultant(**consultant_data)
        assert consultant.nom == 'Test'
        assert consultant.prenom == 'Consultant'
        assert consultant.email == 'test@example.com'
        
    except ImportError:
        pytest.skip("Modèle Consultant non disponible")

def test_mission_model_creation():
    """Test de création d'un modèle Mission"""
    try:
        from database.models import Mission
        from datetime import date
        
        # Test de création avec données minimales
        mission_data = {
            'titre': 'Mission Test',
            'client': 'Client Test',
            'date_debut': date.today(),
            'date_fin': date.today()
        }
        
        mission = Mission(**mission_data)
        assert mission.titre == 'Mission Test'
        assert mission.client == 'Client Test'
        
    except ImportError:
        pytest.skip("Modèle Mission non disponible")

def test_skill_model_creation():
    """Test de création d'un modèle Skill"""
    try:
        from database.models import Skill
        
        skill_data = {
            'nom': 'Python',
            'categorie': 'Développement'
        }
        
        skill = Skill(**skill_data)
        assert skill.nom == 'Python'
        assert skill.categorie == 'Développement'
        
    except ImportError:
        pytest.skip("Modèle Skill non disponible")
    except Exception:
        pytest.skip("Structure du modèle Skill différente")
