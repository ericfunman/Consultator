#!/usr/bin/env python3
"""
Script pour corriger les patches du practice service
"""

import re

def fix_practice_service_patches():
    """Corrige les patches du practice service"""
    
    file_path = "tests/unit/test_practice_service_coverage.py"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer get_database_session par get_session
    content = content.replace(
        '@patch("app.services.practice_service.get_database_session")',
        '@patch("app.services.practice_service.get_session")'
    )
    
    # Supprimer les context manager patterns incorrects
    # Pattern: mock_session.return_value.__enter__.return_value = mock_db
    content = re.sub(
        r'\s+mock_session\.return_value\.__enter__\.return_value = mock_db\n\s+mock_session\.return_value\.__exit__\.return_value = None\n',
        '\n        mock_session.return_value = mock_db\n',
        content
    )
    
    # Ajouter mock_db.close = Mock() où nécessaire
    content = re.sub(
        r'(mock_session\.return_value = mock_db\n)',
        r'\1        mock_db.close = Mock()\n',
        content
    )
    
    # Supprimer les assertions sur __enter__/__exit__
    content = re.sub(r'\s+mock_session\.return_value\.__enter__\.assert_called\(\)\n', '', content)
    content = re.sub(r'\s+mock_session\.return_value\.__exit__\.assert_called\(\)\n', '', content)
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Practice service patches corrigés dans {file_path}")

if __name__ == "__main__":
    fix_practice_service_patches()