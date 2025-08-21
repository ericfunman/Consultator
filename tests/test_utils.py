"""
Tests pour les utilitaires et configurations
"""
import pytest
import sys
import os

# Ajouter le répertoire app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

def test_skill_categories_import():
    """Test d'import des catégories de compétences"""
    try:
        from utils.skill_categories import SKILL_CATEGORIES
        assert isinstance(SKILL_CATEGORIES, dict)
        assert len(SKILL_CATEGORIES) > 0
    except ImportError:
        pytest.skip("Module skill_categories non disponible")

def test_technologies_referentiel_import():
    """Test d'import du référentiel des technologies"""
    try:
        from utils.technologies_referentiel import TECHNOLOGIES_CATEGORIES
        assert isinstance(TECHNOLOGIES_CATEGORIES, dict)
        assert len(TECHNOLOGIES_CATEGORIES) > 0
    except ImportError:
        pytest.skip("Module technologies_referentiel non disponible")

def test_config_settings():
    """Test de la configuration"""
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))
        
        from settings import DATABASE_PATH
        assert DATABASE_PATH is not None
        assert isinstance(DATABASE_PATH, str)
        
    except ImportError:
        pytest.skip("Module settings non disponible")

def test_file_structure_requirements():
    """Test de la présence des fichiers requis"""
    base_path = os.path.join(os.path.dirname(__file__), '..')
    
    required_files = [
        'requirements.txt',
        'run.py',
        'app/main.py',
        'app/database/models.py',
        'app/services/consultant_service.py'
    ]
    
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        assert os.path.exists(full_path), f"Fichier requis manquant: {file_path}"

def test_quality_pipeline_files():
    """Test de la présence des fichiers de pipeline qualité"""
    base_path = os.path.join(os.path.dirname(__file__), '..')
    
    quality_files = [
        'run_quality_pipeline.py',
        'watch_quality.py',
        '.pylintrc',
        'sonar-project-advanced.properties'
    ]
    
    for file_path in quality_files:
        full_path = os.path.join(base_path, file_path)
        assert os.path.exists(full_path), f"Fichier qualité manquant: {file_path}"
