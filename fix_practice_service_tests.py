#!/usr/bin/env python3
"""
Script pour corriger les tests du practice service avec le bon pattern de mocking
"""

import re

def fix_practice_service_tests():
    """Corrige les tests du practice service pour utiliser le bon pattern de mocking"""
    
    test_file = "tests/unit/test_practice_service_optimized.py"
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 Correction des tests dans {test_file}")
        
        # 1. Ajouter l'import contextmanager si manquant
        if 'from contextlib import contextmanager' not in content:
            print("   ✅ Ajout de l'import contextmanager")
            content = content.replace(
                'from unittest.mock import Mock, patch, MagicMock',
                'from unittest.mock import Mock, patch, MagicMock\nfrom contextlib import contextmanager'
            )
        
        # 2. Ajouter la méthode setup_database_mock si manquante
        if 'def setup_database_mock' not in content:
            print("   ✅ Ajout de la méthode setup_database_mock")
            setup_mock_method = '''
    @contextmanager
    def setup_database_mock(self, mock_session, return_value=None, side_effect=None):
        """Mock context manager pour les sessions de base de données"""
        mock_db = Mock()
        
        # Configuration de la chaîne query complète
        if return_value is not None:
            mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = return_value
            mock_db.query.return_value.filter.return_value.first.return_value = return_value
            mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = return_value
        
        if side_effect is not None:
            mock_db.query.side_effect = side_effect
        
        # Mock de la session comme fonction simple (pas context manager)
        mock_session.return_value = mock_db
        mock_db.close = Mock()
        
        try:
            yield mock_db
        finally:
            pass'''
            
            # Insérer après la méthode setup_method
            setup_method_end = content.find('        self.mock_consultant.practice_id = 1')
            if setup_method_end != -1:
                insertion_point = content.find('\n', setup_method_end) + 1
                content = content[:insertion_point] + setup_mock_method + '\n' + content[insertion_point:]
        
        # 3. Corriger tous les tests pour utiliser le bon pattern
        # Pattern de remplacement pour les tests utilisant context manager
        old_pattern = re.compile(
            r'(@patch\("app\.services\.practice_service\.get_database_session"\)\s*'
            r'@patch\("streamlit\.error"\)\s*'
            r'def test_\w+\(self, mock_st_error, mock_session\):\s*'
            r'.*?)'
            r'# Mock session avec context manager\s*'
            r'mock_db = Mock\(\)\s*'
            r'mock_session\.return_value\.__enter__\.return_value = mock_db\s*'
            r'mock_session\.return_value\.__exit__\.return_value = None\s*'
            r'mock_db\.query\.return_value\.filter\.return_value\.order_by\.return_value\.all\.return_value = \[(.*?)\]',
            re.DOTALL
        )
        
        def replace_test_pattern(match):
            """Remplace le pattern de test avec le bon mocking"""
            test_signature = match.group(1)
            return_value = match.group(2)
            
            return f'''{test_signature}# Mock session avec pattern correct
        with self.setup_database_mock(mock_session, return_value=[{return_value}]):'''
        
        content = old_pattern.sub(replace_test_pattern, content)
        
        # 4. Corrections spécifiques pour différents types de tests
        
        # Tests get_all_practices
        content = re.sub(
            r'(@patch\("app\.services\.practice_service\.get_database_session"\)\s*'
            r'@patch\("streamlit\.error"\)\s*'
            r'def test_get_all_practices_\w+\(self, mock_st_error, mock_session\):.*?)'
            r'# Execution\s*'
            r'result = PracticeService\.get_all_practices\(\)',
            r'\1# Execution\n        result = PracticeService.get_all_practices()',
            content, flags=re.DOTALL
        )
        
        # Tests get_practice_by_id
        content = re.sub(
            r'mock_db\.query\.return_value\.filter\.return_value\.first\.return_value = (.*?)\n',
            r'# Mock configuré via setup_database_mock\n',
            content
        )
        
        # Tests avec side_effect pour les erreurs
        content = re.sub(
            r'mock_db\.query\.side_effect = (.*?)\n',
            r'# Exception configurée via setup_database_mock\n',
            content
        )
        
        # 5. Corriger les tests d'erreur pour utiliser side_effect
        error_test_pattern = r'(@patch\("app\.services\.practice_service\.get_database_session"\)\s*@patch\("streamlit\.error"\)\s*def test_.*?error.*?\(self, mock_st_error, mock_session\):.*?)mock_db\.query\.side_effect = (.*?)\s*# Execution'
        
        def fix_error_test(match):
            """Corrige les tests d'erreur"""
            test_part = match.group(1)
            exception = match.group(2)
            return f'''{test_part}with self.setup_database_mock(mock_session, side_effect={exception}):
            # Execution'''
        
        content = re.sub(error_test_pattern, fix_error_test, content, flags=re.DOTALL)
        
        # 6. Corriger l'import pour get_database_session
        content = re.sub(
            r'@patch\("app\.services\.practice_service\.get_database_session"\)',
            r'@patch("app.services.practice_service.get_session")',
            content
        )
        
        # 7. Ajuster les indentations
        content = re.sub(r'\n\s{8}# Execution\s*\n\s{8}result = ', '\n            # Execution\n            result = ', content)
        content = re.sub(r'\n\s{8}# Vérifications\s*\n\s{8}assert ', '\n            # Vérifications\n            assert ', content)
        
        # Sauvegarder le fichier corrigé
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fichier {test_file} corrigé avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {test_file}: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Correction des tests practice service...")
    fix_practice_service_tests()
    print("✅ Correction terminée!")