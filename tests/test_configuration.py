"""
Tests pour les fonctionnalités de configuration et qualité
"""
import pytest
import os
import json
from pathlib import Path

def test_pylint_configuration():
    """Test de la configuration Pylint"""
    pylintrc_path = os.path.join(os.path.dirname(__file__), '..', '.pylintrc')
    assert os.path.exists(pylintrc_path), "Fichier .pylintrc manquant"
    
    with open(pylintrc_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '[MASTER]' in content
        assert '[MESSAGES CONTROL]' in content

def test_sonar_configuration():
    """Test de la configuration SonarQube"""
    sonar_path = os.path.join(os.path.dirname(__file__), '..', 'sonar-project-advanced.properties')
    assert os.path.exists(sonar_path), "Fichier sonar-project-advanced.properties manquant"
    
    with open(sonar_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'sonar.projectKey=' in content
        assert 'sonar.sources=' in content

def test_github_workflows():
    """Test de la présence des workflows GitHub Actions"""
    workflows_dir = os.path.join(os.path.dirname(__file__), '..', '.github', 'workflows')
    
    if os.path.exists(workflows_dir):
        workflow_files = os.listdir(workflows_dir)
        assert len(workflow_files) > 0, "Aucun workflow GitHub Actions trouvé"
        
        # Vérifier qu'au moins un workflow contient des tests
        has_test_workflow = False
        for file in workflow_files:
            if file.endswith('.yml') or file.endswith('.yaml'):
                file_path = os.path.join(workflows_dir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'pytest' in content or 'test' in content.lower():
                        has_test_workflow = True
                        break
        
        assert has_test_workflow, "Aucun workflow de test trouvé"

def test_requirements_files():
    """Test de la validité des fichiers requirements"""
    base_path = os.path.join(os.path.dirname(__file__), '..')
    
    requirements_files = [
        'requirements.txt',
        'requirements-dev.txt',
        'requirements-test.txt'
    ]
    
    for req_file in requirements_files:
        req_path = os.path.join(base_path, req_file)
        if os.path.exists(req_path):
            with open(req_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                assert len(lines) > 0, f"Fichier {req_file} vide"

def test_quality_pipeline_executable():
    """Test que le pipeline de qualité est exécutable"""
    pipeline_path = os.path.join(os.path.dirname(__file__), '..', 'run_quality_pipeline.py')
    assert os.path.exists(pipeline_path), "Script run_quality_pipeline.py manquant"
    
    # Vérifier que le fichier contient les éléments essentiels
    with open(pipeline_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'def main(' in content or 'if __name__ == "__main__"' in content
        assert 'pylint' in content.lower() or 'quality' in content.lower()

def test_watch_quality_executable():
    """Test que le système de surveillance est exécutable"""
    watch_path = os.path.join(os.path.dirname(__file__), '..', 'watch_quality.py')
    assert os.path.exists(watch_path), "Script watch_quality.py manquant"
    
    # Vérifier que le fichier contient les éléments essentiels
    with open(watch_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'watchdog' in content.lower() or 'FileSystemEventHandler' in content
        assert 'def main(' in content or 'if __name__ == "__main__"' in content
