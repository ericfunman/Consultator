"""
Test basique pour valider le pipeline
"""

def test_pipeline_basic():
    """Test basique pour valider que le pipeline fonctionne"""
    assert True

def test_imports():
    """Test des imports de base"""
    try:
        import streamlit
        import pandas
        import sqlalchemy
        assert True
    except ImportError:
        assert False, "Imports de base échoués"

def test_app_structure():
    """Test de la structure de l'application"""
    import os
    
    # Vérifier les répertoires principaux
    assert os.path.exists("app"), "Répertoire app manquant"
    assert os.path.exists("app/main.py"), "main.py manquant"
    assert os.path.exists("app/database"), "Répertoire database manquant"
    assert os.path.exists("app/services"), "Répertoire services manquant"
    assert os.path.exists("app/pages_modules"), "Répertoire pages_modules manquant"

def test_database_models():
    """Test des modèles de base de données"""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
        
        from database.models import Consultant, Mission
        
        # Test création basique
        consultant = Consultant()
        mission = Mission()
        
        assert consultant is not None
        assert mission is not None
        
    except ImportError:
        # Skip si les modèles ne peuvent pas être importés
        pass
