"""
Hooks pour l'exécution automatique des tests de non-régression

Ce module contient des hooks Git pour exécuter automatiquement
les tests de non-régression lors des commits/push.
"""

import subprocess
import sys
import os
from pathlib import Path


def get_venv_python():
    """Retourne le chemin vers le Python du venv .venv_clean"""
    venv_python = Path(__file__).parent.parent / ".venv_clean" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    # Fallback sur sys.executable si venv non trouvé
    return sys.executable


def run_regression_tests_on_changed_files():
    """
    Exécute les tests de non-régression sur les fichiers modifiés
    """
    try:
        # Récupère les fichiers modifiés
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True, text=True, check=True
        )
        
        changed_files = result.stdout.strip().split('\n')
        python_files = [f for f in changed_files if f.endswith('.py') and 'test' not in f]
        
        if not python_files:
            print("✅ Aucun fichier Python modifié, pas de tests de régression nécessaires")
            return True
        
        print(f"📊 Fichiers Python modifiés : {len(python_files)}")
        for file in python_files:
            print(f"  - {file}")
        
        # Génère les tests de régression
        print("\n🔧 Génération des tests de régression...")
        python_exe = get_venv_python()
        subprocess.run([
            python_exe, 'scripts/generate_regression_tests.py',
            '--files'] + python_files,
            check=True
        )
        
        # Exécute les tests de régression
        print("\n🧪 Exécution des tests de régression...")
        test_result = subprocess.run([
            python_exe, '-m', 'pytest',
            'tests/regression/',
            '-v', '--tb=short',
            '--cov=app',
            '--cov-report=term-missing'
        ], check=False)
        
        if test_result.returncode != 0:
            print("❌ Tests de régression échoués")
            return False
        
        print("✅ Tests de régression réussis")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return False


def pre_commit_hook():
    """Hook de pré-commit pour les tests de régression"""
    print("🔍 Exécution du hook de pré-commit...")
    
    # Vérifie si les tests passent
    if not run_regression_tests_on_changed_files():
        print("\n❌ COMMIT BLOQUÉ : Les tests de régression ont échoué")
        print("Corrigez les erreurs avant de commiter")
        sys.exit(1)
    
    print("\n✅ Hook de pré-commit réussi")


def post_merge_hook():
    """Hook post-merge pour vérifier l'intégrité après un merge"""
    print("🔄 Exécution du hook post-merge...")
    
    # Exécute tous les tests de régression
    python_exe = get_venv_python()
    test_result = subprocess.run([
        python_exe, '-m', 'pytest',
        'tests/regression/',
        '-v',
        '--cov=app',
        '--cov-report=html:reports/htmlcov',
        '--html=reports/regression_report.html'
    ], check=False)
    
    if test_result.returncode != 0:
        print("⚠️  Attention : Certains tests de régression ont échoué après le merge")
        print("Vérifiez les rapports dans le dossier 'reports/'")
    else:
        print("✅ Tous les tests de régression passent après le merge")


def setup_git_hooks():
    """Configure les hooks Git pour le projet"""
    hooks_dir = Path('.git/hooks')
    
    # Hook pré-commit
    pre_commit_path = hooks_dir / 'pre-commit'
    pre_commit_content = '''#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from scripts.test_hooks import pre_commit_hook
pre_commit_hook()
'''
    
    with open(pre_commit_path, 'w') as f:
        f.write(pre_commit_content)
    pre_commit_path.chmod(0o755)
    
    # Hook post-merge  
    post_merge_path = hooks_dir / 'post-merge'
    post_merge_content = '''#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from scripts.test_hooks import post_merge_hook
post_merge_hook()
'''
    
    with open(post_merge_path, 'w') as f:
        f.write(post_merge_content)
    post_merge_path.chmod(0o755)
    
    print("✅ Hooks Git configurés:")
    print(f"  - {pre_commit_path}")
    print(f"  - {post_merge_path}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Hooks de tests de régression')
    parser.add_argument('--setup', action='store_true', help='Configure les hooks Git')
    parser.add_argument('--pre-commit', action='store_true', help='Exécute le hook pré-commit')
    parser.add_argument('--post-merge', action='store_true', help='Exécute le hook post-merge')
    parser.add_argument('--check', action='store_true', help='Vérifie les fichiers modifiés')
    
    args = parser.parse_args()
    
    if args.setup:
        setup_git_hooks()
    elif args.pre_commit:
        pre_commit_hook()
    elif args.post_merge:
        post_merge_hook()
    elif args.check:
        run_regression_tests_on_changed_files()
    else:
        parser.print_help()