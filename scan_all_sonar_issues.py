"""
Script pour scanner TOUS les fichiers de test et identifier les assert True à corriger
"""
import re
from pathlib import Path
from collections import defaultdict

def is_in_except_block(lines, line_idx, lookback=10):
    """Vérifie si la ligne est dans un bloc except"""
    start = max(0, line_idx - lookback)
    context = lines[start:line_idx]
    
    target_indent = len(lines[line_idx]) - len(lines[line_idx].lstrip())
    
    for i in range(len(context) - 1, -1, -1):
        line = context[i]
        stripped = line.strip()
        
        if not stripped or stripped.startswith('#'):
            continue
        
        # Chercher 'except' au début de la ligne (après espaces)
        if stripped.startswith('except') and ':' in stripped:
            except_indent = len(line) - len(line.lstrip())
            if except_indent < target_indent:
                return True
        
        # Si on trouve un 'def' ou 'class', on sort du except potentiel
        if stripped.startswith('def ') or stripped.startswith('class '):
            return False
    
    return False

def scan_file(file_path):
    """Scanne un fichier et retourne les assert True à corriger"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return []
    
    issues = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Patterns à détecter
        if stripped in ['assert True', 'assert False'] or \
           'self.assertTrue(True)' in stripped or \
           'self.assertFalse(False)' in stripped:
            
            # Vérifier si c'est dans un except
            if not is_in_except_block(lines, i):
                issues.append({
                    'line': i + 1,
                    'content': stripped,
                    'indent': len(line) - len(line.lstrip())
                })
    
    return issues

def main():
    print("🔍 Scan COMPLET des assert True/False problématiques")
    print("=" * 80)
    
    # Scanner tous les fichiers de test
    test_dir = Path('tests/unit')
    all_test_files = list(test_dir.rglob('test_*.py'))
    
    print(f"📁 {len(all_test_files)} fichiers de test trouvés\n")
    
    files_with_issues = {}
    total_issues = 0
    
    for test_file in sorted(all_test_files):
        issues = scan_file(test_file)
        if issues:
            rel_path = test_file.relative_to(Path('.'))
            files_with_issues[str(rel_path)] = issues
            total_issues += len(issues)
    
    # Afficher les résultats
    if not files_with_issues:
        print("✅ Aucun assert True/False problématique trouvé!")
        return
    
    print(f"⚠️  {total_issues} issues trouvées dans {len(files_with_issues)} fichiers:\n")
    
    for file_path, issues in sorted(files_with_issues.items()):
        print(f"\n📄 {file_path} ({len(issues)} issues)")
        print("-" * 80)
        for issue in issues[:5]:  # Montrer max 5 par fichier
            print(f"  Ligne {issue['line']:4d}: {issue['content']}")
        if len(issues) > 5:
            print(f"  ... et {len(issues) - 5} autres")
    
    print("\n" + "=" * 80)
    print(f"🎯 TOTAL: {total_issues} issues à corriger dans {len(files_with_issues)} fichiers")
    print("=" * 80)
    
    # Sauvegarder la liste
    with open('sonar_issues_to_fix.txt', 'w', encoding='utf-8') as f:
        f.write("Liste des fichiers avec assert True/False à corriger:\n\n")
        for file_path in sorted(files_with_issues.keys()):
            f.write(f"{file_path}\n")
    
    print("\n💾 Liste sauvegardée dans: sonar_issues_to_fix.txt")

if __name__ == "__main__":
    main()
