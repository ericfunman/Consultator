"""
Configuration des hooks de test de régression

Ce script configure automatiquement les hooks Git et les processus
d'amélioration continue de la couverture de tests.
"""

import os
import shutil
import subprocess
from pathlib import Path


def setup_test_environment():
    """Configure l'environnement de tests complet"""
    print("🔧 Configuration de l'environnement de tests...")
    
    # Créer la structure des dossiers de tests
    test_dirs = [
        'tests/auto_generated',
        'tests/auto_generated/services',
        'tests/auto_generated/pages',  
        'tests/auto_generated/models',
        'tests/templates',
        'reports',
        'reports/coverage',
        'reports/regression'
    ]
    
    for test_dir in test_dirs:
        Path(test_dir).mkdir(parents=True, exist_ok=True)
        print(f"  📁 {test_dir}")
    
    # Créer les fichiers __init__.py manquants
    init_files = [
        'tests/__init__.py',
        'tests/auto_generated/__init__.py',
        'tests/auto_generated/services/__init__.py', 
        'tests/auto_generated/pages/__init__.py',
        'tests/auto_generated/models/__init__.py',
        'tests/templates/__init__.py'
    ]
    
    for init_file in init_files:
        init_path = Path(init_file)
        if not init_path.exists():
            init_path.write_text('"""Auto-generated test package"""')
            print(f"  📄 {init_file}")
    
    print("✅ Structure de tests créée")


def create_makefile():
    """Crée un Makefile pour les commandes de test courantes"""
    makefile_content = """# Consultator Test Management Makefile

.PHONY: test test-unit test-integration test-regression coverage coverage-html improve-coverage auto-tests setup-hooks clean-tests

# Tests basiques
test:
	python -m pytest tests/ -v --tb=short

test-unit:
	python -m pytest tests/unit/ -v --tb=short

test-integration:
	python -m pytest tests/integration/ -v --tb=short

test-regression:
	python -m pytest tests/regression/ -v --tb=short

# Couverture
coverage:
	python -m pytest --cov=app --cov-report=term-missing --cov-report=html:reports/htmlcov tests/

coverage-html:
	python -m pytest --cov=app --cov-report=html:reports/htmlcov tests/
	@echo "📊 Rapport HTML généré dans reports/htmlcov/index.html"

# Amélioration de la couverture
improve-coverage:
	python scripts/improve_coverage.py

auto-tests:
	python scripts/auto_test_generator.py

# Configuration
setup-hooks:
	python scripts/test_hooks.py --setup
	@echo "✅ Hooks Git configurés"

# Nettoyage
clean-tests:
	rm -rf tests/auto_generated/*
	rm -rf reports/*
	rm -rf .coverage
	rm -rf coverage.json
	@echo "🧹 Tests automatiques et rapports nettoyés"

# Processus complet d'amélioration
full-improvement:
	python scripts/improve_coverage.py
	python scripts/auto_test_generator.py
	python -m pytest tests/auto_generated/ --tb=short
	@echo "🚀 Processus d'amélioration terminé"

# Validation avant commit
pre-commit:
	python scripts/test_hooks.py --pre-commit

# Validation après merge  
post-merge:
	python scripts/test_hooks.py --post-merge
"""
    
    with open('Makefile', 'w', encoding='utf-8') as f:
        f.write(makefile_content)
    
    print("✅ Makefile créé")


def create_batch_scripts():
    """Crée des scripts batch pour Windows"""
    scripts = {
        'test.bat': '''@echo off
echo 🧪 Exécution des tests...
python -m pytest tests/ -v --tb=short
pause''',
        
        'coverage.bat': '''@echo off
echo 📊 Analyse de couverture...
python -m pytest --cov=app --cov-report=html:reports/htmlcov --cov-report=term-missing tests/
echo.
echo 📈 Rapport HTML généré dans reports/htmlcov/index.html
pause''',
        
        'improve-tests.bat': '''@echo off
echo 🚀 Amélioration de la couverture de tests...
python scripts/improve_coverage.py
python scripts/auto_test_generator.py
echo.
echo ✅ Processus terminé. Consultez les fichiers générés.
pause''',
        
        'setup-hooks.bat': '''@echo off
echo 🔧 Configuration des hooks Git...
python scripts/test_hooks.py --setup
echo.
echo ✅ Hooks configurés avec succès
pause'''
    }
    
    scripts_dir = Path('scripts/batch')
    scripts_dir.mkdir(exist_ok=True)
    
    for script_name, content in scripts.items():
        script_path = scripts_dir / script_name
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📄 {script_path}")
    
    print("✅ Scripts batch créés")


def update_pytest_ini():
    """Met à jour la configuration pytest"""
    pytest_config = """[tool:pytest]
# Configuration pytest pour Consultator

# Dossiers de tests
testpaths = tests

# Patterns de découverte
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Marqueurs personnalisés
markers =
    unit: Tests unitaires rapides
    integration: Tests d'intégration avec DB
    regression: Tests de non-régression
    slow: Tests lents (>5s)
    ui: Tests d'interface utilisateur
    import: Tests d'import de données
    service: Tests de services métier
    critical: Tests critiques à ne pas ignorer

# Options par défaut
addopts = 
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --maxfail=10
    --durations=10
    --cov-report=term-missing
    --cov-fail-under=15

# Filtres d'avertissement
filterwarnings =
    ignore::UserWarning
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
    ignore:.*pandas.*:FutureWarning
    
# Timeout pour les tests lents
timeout = 300
timeout_method = thread

# Coverage
[coverage:run]
source = app
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*
    setup.py
    
[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\\bProtocol\\):
    @(abc\.)?abstractmethod
"""
    
    with open('pytest.ini', 'w', encoding='utf-8') as f:
        f.write(pytest_config)
    
    print("✅ Configuration pytest mise à jour")


def create_github_workflow():
    """Crée un workflow GitHub Actions pour les tests"""
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_content = """name: 🧪 Tests et Couverture

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Create test database
      run: |
        python -c "from app.database.database import init_database; init_database()"
    
    - name: Run tests with coverage
      run: |
        python -m pytest tests/ --cov=app --cov-report=xml --cov-report=html
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      if: matrix.python-version == '3.11'
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false
    
    - name: Generate test report
      if: always()
      run: |
        python -m pytest tests/ --html=reports/pytest_report.html --self-contained-html
    
    - name: Upload test reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-reports-${{ matrix.python-version }}
        path: |
          reports/
          htmlcov/

  regression-tests:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Generate regression tests
      run: |
        python scripts/auto_test_generator.py
    
    - name: Run regression tests
      run: |
        python -m pytest tests/regression/ -v --tb=short
        
    - name: Coverage improvement analysis
      run: |
        python scripts/improve_coverage.py
        
    - name: Upload analysis reports
      uses: actions/upload-artifact@v3
      with:
        name: analysis-reports
        path: |
          TEST_IMPROVEMENT_PLAN.md
          tests/auto_generated/GENERATION_SUMMARY.md
"""
    
    workflow_file = workflow_dir / 'tests.yml'
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    print(f"✅ Workflow GitHub créé : {workflow_file}")


def install_pre_commit():
    """Installe et configure pre-commit"""
    precommit_config = """repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
    -   id: check-merge-conflict
    -   id: debug-statements

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
        language_version: python3

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
        args: ["--profile", "black"]

-   repo: local
    hooks:
    -   id: test-regression
        name: Tests de régression
        entry: python scripts/test_hooks.py --pre-commit
        language: system
        always_run: true
        pass_filenames: false
"""
    
    with open('.pre-commit-config.yaml', 'w', encoding='utf-8') as f:
        f.write(precommit_config)
    
    try:
        subprocess.run(['pre-commit', 'install'], check=True)
        print("✅ Pre-commit installé et configuré")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Pre-commit non installé. Installez avec: pip install pre-commit")


def main():
    """Configuration complète de l'environnement de tests"""
    print("🚀 CONFIGURATION COMPLÈTE DE L'ENVIRONNEMENT DE TESTS")
    print("="*60)
    
    # Configuration de base
    setup_test_environment()
    
    # Scripts et configurations
    create_makefile()
    create_batch_scripts()
    update_pytest_ini()
    
    # CI/CD
    create_github_workflow()
    install_pre_commit()
    
    # Configuration des hooks Git
    try:
        from scripts.test_hooks import setup_git_hooks
        setup_git_hooks()
    except ImportError:
        print("⚠️ Impossible d'importer test_hooks pour configurer les hooks Git")
    
    print("\n" + "="*60)
    print("✅ CONFIGURATION TERMINÉE")
    print("="*60)
    
    print("""
🎯 PROCHAINES ÉTAPES RECOMMANDÉES:

1. 📊 **Analyser la couverture actuelle**:
   python scripts/improve_coverage.py
   
2. 🤖 **Générer des tests automatiques**:
   python scripts/auto_test_generator.py
   
3. 🧪 **Exécuter les tests**:
   python -m pytest tests/ --cov=app --cov-report=html
   
4. 🔧 **Configurer les hooks Git** (optionnel):
   python scripts/test_hooks.py --setup
   
5. 📈 **Surveiller la couverture**:
   make coverage-html  # ou coverage.bat sur Windows

🛠️ COMMANDES DISPONIBLES:
- make test              # Tests basiques
- make coverage          # Couverture avec rapport
- make improve-coverage  # Analyse d'amélioration
- make auto-tests        # Génération automatique
- make full-improvement  # Processus complet

📁 STRUCTURE CRÉÉE:
- tests/auto_generated/  # Tests générés automatiquement
- tests/templates/       # Templates de tests
- reports/              # Rapports de couverture
- scripts/batch/        # Scripts Windows (.bat)
- .github/workflows/    # CI/CD GitHub Actions

💡 La prochaine fois que vous modifiez du code, les tests de régression
   seront automatiquement générés et exécutés !
""")


if __name__ == '__main__':
    main()