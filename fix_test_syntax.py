#!/usr/bin/env python3
"""
Script pour corriger les erreurs de syntaxe dans les fichiers de tests
"""

import os
import re
from pathlib import Path


def fix_indentation_errors():
    """Corrige les erreurs d'indentation dans les fichiers de tests"""
    
    tests_dir = Path("tests")
    files_fixed = []
    
    print("🔧 Correction des erreurs d'indentation dans les tests...")
    
    for test_file in tests_dir.glob("test_*.py"):
        print(f"📝 Vérification de {test_file}")
        
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = 0
            
            # Corriger les lignes avec indentation inattendue au début du fichier
            lines = content.split('\n')
            fixed_lines = []
            
            for i, line in enumerate(lines):
                # Si on trouve une ligne indentée de manière inattendue au début
                if i < 50 and line.startswith('    ') and not any(x in line for x in ['def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except', 'with ', 'return ', '#']):
                    if lines[i-1].strip() and not lines[i-1].endswith(':') and not lines[i-1].endswith('\\'):
                        # Supprimer l'indentation excessive
                        fixed_line = line.lstrip()
                        fixed_lines.append(fixed_line)
                        changes_made += 1
                        continue
                
                fixed_lines.append(line)
            
            if changes_made > 0:
                new_content = '\n'.join(fixed_lines)
                
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_fixed.append(str(test_file))
                print(f"✅ {test_file}: {changes_made} corrections d'indentation")
            
        except Exception as e:
            print(f"❌ Erreur avec {test_file}: {e}")
    
    return files_fixed


def fix_specific_syntax_errors():
    """Corrige des erreurs de syntaxe spécifiques connues"""
    
    fixes = {
        "tests/test_business_managers_simple.py": {
            "from app.pages_modules.business_managers import (": "from app.pages_modules.business_managers import show_business_managers"
        },
        "tests/test_competences_filtering.py": {
            "    chatbot = ChatbotService()": "chatbot = ChatbotService()"
        },
        "tests/test_competences_fonctionnelles.py": {
            "    session = session_local()": "session = session_local()"
        }
    }
    
    for file_path, file_fixes in fixes.items():
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for old_text, new_text in file_fixes.items():
                    content = content.replace(old_text, new_text)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Corrections spécifiques appliquées à {file_path}")
                
            except Exception as e:
                print(f"❌ Erreur avec {file_path}: {e}")


def main():
    """Fonction principale"""
    
    print("🚀 Début de la correction des erreurs de syntaxe des tests")
    
    # Corriger les erreurs d'indentation
    files_fixed = fix_indentation_errors()
    
    # Corriger des erreurs spécifiques
    fix_specific_syntax_errors()
    
    print(f"\n✅ Correction terminée!")
    print(f"📊 Fichiers corrigés: {len(files_fixed)}")
    
    if files_fixed:
        print("📝 Fichiers modifiés:")
        for file in files_fixed:
            print(f"  - {file}")
    
    print("\n🔍 Test de compilation des fichiers corrigés...")
    
    # Tester la compilation
    import subprocess
    import sys
    
    tests_dir = Path("tests")
    errors = []
    
    for test_file in tests_dir.glob("test_*.py"):
        try:
            result = subprocess.run([sys.executable, '-m', 'py_compile', str(test_file)], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                errors.append(f"{test_file}: {result.stderr.strip()}")
                
        except Exception as e:
            errors.append(f"{test_file}: {e}")
    
    if errors:
        print(f"❌ {len(errors)} fichiers ont encore des erreurs:")
        for error in errors[:10]:  # Afficher seulement les 10 premiers
            print(f"  {error}")
    else:
        print("✅ Tous les fichiers de tests compilent correctement!")


if __name__ == "__main__":
    main()
