#!/usr/bin/env python3
"""
Script pour corriger les décorateurs cassés dans les tests
"""

import re

def fix_broken_decorators():
    """Corrige les décorateurs cassés collés aux assert"""
    
    file_path = "tests/unit/test_consultant_service_coverage.py"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour corriger les décorateurs cassés
    # Chercher : assert ... @patch(...)
    # Remplacer par : assert ...\n\n    @patch(...)
    
    pattern = r'(assert [^@]+)(@patch\()'
    replacement = r'\1\n\n    \2'
    
    content = re.sub(pattern, replacement, content)
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Décorateurs corrigés dans {file_path}")

if __name__ == "__main__":
    fix_broken_decorators()