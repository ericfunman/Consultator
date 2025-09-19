#!/usr/bin/env python3
"""
Script pour corriger automatiquement les tests du ConsultantService
qui ont des problèmes de context manager
"""

import re

def fix_consultant_service_tests():
    """Corrige les tests du ConsultantService"""
    
    file_path = "tests/unit/test_consultant_service_coverage.py"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour trouver les tests avec des mocks de session incorrects
    # Chercher les patterns comme:
    # mock_db = Mock()
    # mock_session.return_value = mock_db
    
    old_pattern = r'(\s+# Mock session\n\s+mock_db = Mock\(\)\n\s+mock_session\.return_value = mock_db)'
    new_replacement = r'\1\n        # Setup context manager\n        mock_session.return_value.__enter__ = Mock(return_value=mock_db)\n        mock_session.return_value.__exit__ = Mock(return_value=None)\n        mock_db.expunge = Mock()'
    
    # Autre pattern plus spécifique
    pattern1 = r'(\s+mock_db = Mock\(\)\n\s+mock_session\.return_value = mock_db\n)'
    replacement1 = r'\1        # Setup context manager\n        mock_session.return_value.__enter__ = Mock(return_value=mock_db)\n        mock_session.return_value.__exit__ = Mock(return_value=None)\n        mock_db.expunge = Mock()\n'
    
    # Appliquer les corrections
    content = re.sub(pattern1, replacement1, content)
    
    # Pattern pour supprimer les assertions sur mock_db.close
    content = re.sub(r'\s+mock_db\.close\.assert_called\(\)\n', '', content)
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Corrections appliquées à {file_path}")

if __name__ == "__main__":
    fix_consultant_service_tests()