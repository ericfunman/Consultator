#!/usr/bin/env python3
"""
Script pour supprimer les assertions streamlit incorrectes des tests
"""

import re

def fix_streamlit_assertions():
    """Supprime les assertions streamlit incorrectes"""
    
    file_path = "tests/unit/test_consultant_service_coverage.py"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Supprimer les assertions sur mock_st_success et mock_st_error
    patterns_to_remove = [
        r'\s+mock_st_success\.assert_called\(\)\n',
        r'\s+mock_st_error\.assert_called\(\)\n',
        r'\s+mock_st_success\.assert_called_once\(\)\n',
        r'\s+mock_st_error\.assert_called_once\(\)\n',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content)
    
    # Ajouter des commentaires pour expliquer
    content = content.replace(
        'mock_db.commit.assert_called()',
        'mock_db.commit.assert_called()\n        # Note: Les fonctions utilisent maintenant print() au lieu de streamlit'
    )
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Assertions streamlit supprimées de {file_path}")

if __name__ == "__main__":
    fix_streamlit_assertions()