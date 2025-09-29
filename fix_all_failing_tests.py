#!/usr/bin/env python3
"""
Script pour corriger MASSIVEMENT tous les tests en échec
"""

import os
import re
import subprocess
from pathlib import Path

def run_failing_tests():
    """Exécute tous les tests et identifie ceux en échec"""
    print("🔍 Identification des tests en échec...")
    
    cmd = ["python", "-m", "pytest", "tests/", "--tb=no", "-v", "--co", "-q"]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode != 0:
        print("⚠️ Certains tests ont des erreurs de collection")
        print(result.stdout)
        print(result.stderr)
    
    # Maintenant lancer les tests pour voir les échecs
    print("🧪 Exécution des tests pour identifier les échecs...")
    cmd = ["python", "-m", "pytest", "tests/", "--tb=no", "-x", "--maxfail=20"]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    return result.stdout, result.stderr

def fix_common_issues():
    """Corrige les problèmes communs dans tous les fichiers de tests"""
    
    # Répertoires à corriger
    test_dirs = [
        "tests/regression_backup/",
        "tests/problematic_tests/",
        "tests/ui/",
        "tests/unit/"
    ]
    
    fixes_applied = 0
    
    for test_dir in test_dirs:
        if not os.path.exists(test_dir):
            print(f"⏭️ Répertoire {test_dir} n'existe pas, passage au suivant")
            continue
            
        print(f"🔧 Correction du répertoire {test_dir}...")
        
        for file_path in Path(test_dir).rglob("*.py"):
            if file_path.name.startswith("test_"):
                fixes_applied += fix_single_file(file_path)
    
    print(f"✅ {fixes_applied} corrections appliquées")

def fix_single_file(file_path):
    """Corrige un fichier de test spécifique"""
    fixes = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture {file_path}: {e}")
        return 0
    
    original_content = content
    
    # 1. Corriger les imports manquants
    if 'from app.database.models import' in content and 'ConsultantCompetence' not in content:
        content = re.sub(
            r'(from app\.database\.models import [^\n]+)',
            r'\1, ConsultantCompetence',
            content
        )
        fixes += 1
    
    # 2. Corriger la création de Competence avec consultant_id
    patterns = [
        # Competence avec consultant_id et niveau
        (
            r'(\s+)competence = Competence\(\s*consultant_id=([^,]+),\s*nom=[\'"]([^\'\"]+)[\'"],\s*niveau=(\d+)\s*\)',
            r'''\1competence = Competence(
\1    nom="\3",
\1    categorie="technique"
\1)
\1db_session.add(competence)
\1db_session.flush()
\1
\1consultant_competence = ConsultantCompetence(
\1    consultant_id=\2,
\1    competence_id=competence.id,
\1    niveau_maitrise="intermediaire",
\1    annees_experience=float(\4)
\1)'''
        ),
        
        # Mission sans date_debut
        (
            r'(\s+)mission = Mission\(\s*consultant_id=([^,]+),\s*nom_mission=[\'"]([^\'\"]+)[\'"],\s*client=[\'"]([^\'\"]+)[\'"]\s*\)',
            r'''\1mission = Mission(
\1    consultant_id=\2,
\1    nom_mission="\3",
\1    client="\4",
\1    date_debut=date(2023, 1, 1)
\1)'''
        ),
        
        # Ajouter l'import date si besoin
        (
            r'^(from datetime import [^\n]*)',
            r'\1'  # Laisse tel quel si déjà présent
        ),
        
        # Corriger les requêtes Competence.filter_by(consultant_id=)
        (
            r'\.query\(Competence\)\s*\\?\s*\.filter_by\(consultant_id=([^)]+)\)',
            r'.query(ConsultantCompetence)\\n            .filter_by(consultant_id=\1)'
        ),
        
        # Corriger les assertions sur les competences
        (
            r'remaining_competences = ([^\n]+ConsultantCompetence[^\n]+)',
            r'remaining_consultant_competences = \1'
        ),
        
        (
            r'assert remaining_competences == 0',
            r'assert remaining_consultant_competences == 0'
        ),
        
        # Corriger add_all avec competence et consultant_competence
        (
            r'db_session\.add_all\(\[competence, ([^\]]+)\]\)',
            r'db_session.add_all([competence, consultant_competence, \1])'
        )
    ]
    
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if new_content != content:
            content = new_content
            fixes += 1
    
    # Ajouter l'import date si nécessaire et pas déjà présent
    if 'date(' in content and 'from datetime import date' not in content and 'from datetime import' in content:
        content = re.sub(
            r'from datetime import ([^\n]+)',
            r'from datetime import \1, date' if 'date' not in content else r'from datetime import \1',
            content
        )
        fixes += 1
    elif 'date(' in content and 'from datetime import' not in content:
        # Ajouter l'import complet
        if 'import pytest' in content:
            content = re.sub(
                r'(import pytest\n)',
                r'\1from datetime import date\n',
                content
            )
            fixes += 1
    
    # Sauvegarder si des changements ont été faits
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {file_path}: {fixes} corrections appliquées")
        except Exception as e:
            print(f"❌ Erreur écriture {file_path}: {e}")
            return 0
    
    return fixes

def check_syntax_errors():
    """Vérifie les erreurs de syntaxe dans les fichiers corrigés"""
    print("🔍 Vérification des erreurs de syntaxe...")
    
    test_files = list(Path("tests/").rglob("test_*.py"))
    
    syntax_errors = []
    
    for file_path in test_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            compile(content, str(file_path), 'exec')
            
        except SyntaxError as e:
            syntax_errors.append((file_path, e))
            print(f"❌ Erreur syntaxe {file_path}:{e.lineno}: {e.msg}")
        except Exception as e:
            syntax_errors.append((file_path, e))
            print(f"❌ Erreur {file_path}: {e}")
    
    return syntax_errors

if __name__ == "__main__":
    print("🚀 Correction massive des tests en échec...")
    
    # 1. Corriger les problèmes communs
    fix_common_issues()
    
    # 2. Vérifier les erreurs de syntaxe
    syntax_errors = check_syntax_errors()
    
    if syntax_errors:
        print(f"⚠️ {len(syntax_errors)} fichiers ont des erreurs de syntaxe")
        for file_path, error in syntax_errors[:5]:  # Afficher seulement les 5 premières
            print(f"  - {file_path}: {error}")
    else:
        print("✅ Aucune erreur de syntaxe détectée")
    
    print("\n📊 Test d'un échantillon après correction...")
    
    # Tester quelques fichiers pour voir si ça fonctionne
    test_samples = [
        "tests/regression_backup/test_service_regression.py::TestDataConsistencyRegression::test_cascade_operations_regression"
    ]
    
    for test in test_samples:
        print(f"🧪 Test: {test}")
        result = subprocess.run(
            ["python", "-m", "pytest", test, "-v"], 
            capture_output=True, text=True, shell=True
        )
        
        if result.returncode == 0:
            print("  ✅ PASSE")
        else:
            print("  ❌ ÉCHEC")
            # Afficher les premières lignes d'erreur
            lines = result.stdout.split('\n')
            for line in lines[-10:]:
                if line.strip():
                    print(f"    {line}")
    
    print("\n✅ Correction massive terminée !")