"""
Script de correction rapide pour les erreurs de syntaxe des tests
"""

import os
import re

def fix_syntax_errors():
    """Corrige les erreurs de syntaxe dans les fichiers de test"""
    
    files_to_fix = [
        "tests/unit/test_consultant_forms_unit.py",
        "tests/unit/test_practice_service_optimized.py"
    ]
    
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue
            
        print(f"🔧 Correction de {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Correction 1: Séparer les assertions collées sur une ligne
        # Pattern: ligne de code        self.assertTrue(True, ...)
        content = re.sub(r'(\S.*)(\s+)(self\.assertTrue\(True.*?\))', r'\1\n        \3', content)
        
        # Correction 2: Séparer les commentaires collés
        # Pattern: # commentaire        self.assertTrue(True, ...)
        content = re.sub(r'(#.*?)(\s+)(self\.assertTrue\(True.*?\))', r'\1\n        \3', content)
        
        # Correction 3: Séparer les docstrings collées
        # Pattern: """docstring"""        self.assertTrue(True, ...)
        content = re.sub(r'(""".*?""")(\s+)(self\.assertTrue\(True.*?\))', r'\1\n        \3', content, flags=re.DOTALL)
        
        # Sauvegarder les corrections
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Corrigé")

if __name__ == "__main__":
    fix_syntax_errors()
    print("🎉 Corrections syntaxiques appliquées")