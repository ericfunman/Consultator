import subprocess
import sys

def run_git_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=r'c:\Users\b302gja\Documents\Consultator en cours\Consultator')
        print(f'Command: {" ".join(cmd)}')
        print(f'Exit code: {result.returncode}')
        if result.stdout:
            print(f'STDOUT: {result.stdout}')
        if result.stderr:
            print(f'STDERR: {result.stderr}')
        print('---')
        return result.returncode == 0
    except Exception as e:
        print(f'Error running command: {e}')
        return False

# Check git status
print("=== Checking git status ===")
run_git_command(['git', 'status', '--porcelain'])

# Add all changes
print("=== Adding changes ===")
run_git_command(['git', 'add', '.'])

# Check status after add
print("=== Status after add ===")
run_git_command(['git', 'status', '--porcelain'])

# Commit
print("=== Committing changes ===")
commit_message = '''feat: Amélioration significative de la couverture de tests pour conformité SonarQube

- Expansion majeure des tests unitaires pour ChatbotService (36+ tests)
- Création complète de tests pour DocumentAnalyzer (15 tests)
- Tests exhaustifs pour SimpleDocumentAnalyzer (extraction fichiers)
- Tests complets pour TechnologyService avec gestion d'erreurs
- Tests UI pour TechnologyWidget avec mocking Streamlit
- Correction des erreurs SQLAlchemy dans les tests
- Amélioration du mocking pour les interactions DB et UI
- Couverture de tests dépassant 80% pour tous les services critiques
- Préparation pour analyse SonarQube et validation qualité code'''

commit_success = run_git_command(['git', 'commit', '-m', commit_message])

if commit_success:
    print("=== Pushing to master ===")
    # Push
    run_git_command(['git', 'push', 'origin', 'master'])
else:
    print('Commit failed, not pushing')
