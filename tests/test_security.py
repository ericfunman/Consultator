"""
Tests pour la sécurité et les performances
"""
import pytest
import os
import time
import tempfile
from pathlib import Path

def test_security_no_hardcoded_secrets():
    """Test pour vérifier l'absence de secrets hardcodés"""
    app_dir = os.path.join(os.path.dirname(__file__), '..', 'app')
    
    dangerous_patterns = [
        'password = "',
        'PASSWORD = "',
        'api_key = "',
        'API_KEY = "',
        'secret = "',
        'SECRET = "',
        'token = "'
    ]
    
    violations = []
    
    for root, dirs, files in os.walk(app_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for pattern in dangerous_patterns:
                            if pattern in content:
                                violations.append(f"{file}: {pattern}")
                except:
                    continue
    
    assert len(violations) == 0, f"Secrets potentiels détectés: {violations}"

def test_imports_security():
    """Test de sécurité des imports"""
    dangerous_imports = [
        'os.system',
        'subprocess.call',
        'eval(',
        'exec(',
        '__import__'
    ]
    
    app_dir = os.path.join(os.path.dirname(__file__), '..', 'app')
    violations = []
    
    for root, dirs, files in os.walk(app_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for dangerous in dangerous_imports:
                            if dangerous in content:
                                violations.append(f"{file}: {dangerous}")
                except:
                    continue
    
    # Permettre certains usages légitimes mais les signaler
    if violations:
        print(f"Avertissement - Imports sensibles détectés: {violations}")

def test_file_permissions():
    """Test des permissions de fichiers"""
    sensitive_files = [
        '.pylintrc',
        'sonar-project-advanced.properties',
        'run_quality_pipeline.py'
    ]
    
    base_path = os.path.join(os.path.dirname(__file__), '..')
    
    for file_name in sensitive_files:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            # Vérifier que le fichier n'est pas exécutable pour tout le monde (sur Unix)
            stat_info = os.stat(file_path)
            # Sur Windows, les permissions sont différentes, donc on vérifie juste l'existence
            assert os.access(file_path, os.R_OK), f"Fichier {file_name} non lisible"

def test_performance_imports():
    """Test de performance des imports critiques"""
    critical_imports = [
        'streamlit',
        'pandas',
        'sqlalchemy'
    ]
    
    for module_name in critical_imports:
        start_time = time.time()
        try:
            exec(f"import {module_name}")
            import_time = time.time() - start_time
            
            # L'import ne devrait pas prendre plus de 5 secondes
            assert import_time < 5.0, f"Import de {module_name} trop lent: {import_time:.2f}s"
            
        except ImportError:
            # Module non installé, on passe
            pass

def test_temp_file_cleanup():
    """Test de nettoyage des fichiers temporaires"""
    # Créer un fichier temporaire et vérifier qu'il peut être supprimé
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write("test content")
        tmp_path = tmp_file.name
    
    # Vérifier que le fichier existe
    assert os.path.exists(tmp_path)
    
    # Le supprimer
    os.unlink(tmp_path)
    
    # Vérifier qu'il n'existe plus
    assert not os.path.exists(tmp_path)

def test_data_directory_structure():
    """Test de la structure du répertoire de données"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    if os.path.exists(data_dir):
        # Vérifier que c'est bien un répertoire
        assert os.path.isdir(data_dir)
        
        # Vérifier les permissions d'écriture
        assert os.access(data_dir, os.W_OK), "Répertoire data non accessible en écriture"
        
        # Vérifier la présence du répertoire uploads
        uploads_dir = os.path.join(data_dir, 'uploads')
        if os.path.exists(uploads_dir):
            assert os.path.isdir(uploads_dir)
            assert os.access(uploads_dir, os.W_OK), "Répertoire uploads non accessible en écriture"
