#!/usr/bin/env python3
"""
Script pour corriger les tests du practice service avec le bon pattern de mocking
Le service utilise get_session() directement, pas comme context manager
"""

import re

def fix_practice_service_tests():
    """Corrige les tests du practice service pour utiliser le bon pattern de mocking"""
    
    test_file = "tests/unit/test_practice_service_optimized.py"
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 Correction des tests dans {test_file}")
        
        # 1. Corriger l'import pour get_session au lieu de get_database_session
        print("   ✅ Correction du patch path")
        content = re.sub(
            r'@patch\("app\.services\.practice_service\.get_database_session"\)',
            r'@patch("app.services.practice_service.get_session")',
            content
        )
        
        # 2. Remplacer les mocks context manager par des mocks simples
        print("   ✅ Correction des patterns de mock")
        
        # Pattern pour corriger tous les tests success
        old_success_pattern = re.compile(
            r'(def test_\w+_success\(self, mock_st_error, mock_session\):.*?)'
            r'# Mock session avec context manager\s*'
            r'mock_db = Mock\(\)\s*'
            r'mock_session\.return_value\.__enter__\.return_value = mock_db\s*'
            r'mock_session\.return_value\.__exit__\.return_value = None\s*'
            r'mock_db\.query\.return_value\.filter\.return_value\.order_by\.return_value\.all\.return_value = \[(.*?)\]',
            re.DOTALL
        )
        
        def replace_success_pattern(match):
            """Remplace le pattern success avec le bon mocking"""
            test_signature = match.group(1)
            return_value = match.group(2)
            
            return f'''{test_signature}# Mock session simple (pas context manager)
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.close = Mock()
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [{return_value}]'''
        
        content = old_success_pattern.sub(replace_success_pattern, content)
        
        # Pattern pour les tests get_practice_by_id (utilise first() au lieu de all())
        content = re.sub(
            r'mock_db\.query\.return_value\.filter\.return_value\.first\.return_value = (.*?)\n',
            r'mock_db.query.return_value.filter.return_value.first.return_value = \1\n',
            content
        )
        
        # Pattern pour les tests d'erreur
        old_error_pattern = re.compile(
            r'(def test_\w+_error\(self, mock_st_error, mock_session\):.*?)'
            r'# Mock session avec context manager\s*'
            r'mock_db = Mock\(\)\s*'
            r'mock_session\.return_value\.__enter__\.return_value = mock_db\s*'
            r'mock_session\.return_value\.__exit__\.return_value = None\s*'
            r'mock_db\.query\.side_effect = (.*?)\s*',
            re.DOTALL
        )
        
        def replace_error_pattern(match):
            """Remplace le pattern error avec le bon mocking"""
            test_signature = match.group(1)
            exception = match.group(2)
            
            return f'''{test_signature}# Mock session avec erreur
        mock_db = Mock()
        mock_session.return_value = mock_db
        mock_db.close = Mock()
        mock_db.query.side_effect = {exception}
        '''
        
        content = old_error_pattern.sub(replace_error_pattern, content)
        
        # 3. Corriger les tests spécifiques qui utilisent des patterns différents
        
        # Tests create_practice_success
        content = re.sub(
            r'(# Mock session avec context manager\s*'
            r'mock_db = Mock\(\)\s*'
            r'mock_session\.return_value\.__enter__\.return_value = mock_db\s*'
            r'mock_session\.return_value\.__exit__\.return_value = None\s*'
            r'mock_db\.add = Mock\(\)\s*'
            r'mock_db\.commit = Mock\(\))',
            r'# Mock session simple\n        mock_db = Mock()\n        mock_session.return_value = mock_db\n        mock_db.close = Mock()\n        mock_db.add = Mock()\n        mock_db.commit = Mock()',
            content, flags=re.DOTALL
        )
        
        # Tests update_practice
        content = re.sub(
            r'(mock_db\.query\.return_value\.filter\.return_value\.first\.return_value = self\.mock_practice\s*'
            r'mock_db\.commit = Mock\(\))',
            r'\1',
            content
        )
        
        # 4. Ajuster d'autres patterns spécifiques trouvés dans le fichier
        content = re.sub(
            r'mock_db\.query\.return_value\.filter\.return_value\.join\.return_value\.all\.return_value = \[(.*?)\]',
            r'mock_db.query.return_value.filter.return_value.join.return_value.all.return_value = [\1]',
            content
        )
        
        # 5. Nettoyer les références aux context managers restantes
        content = re.sub(
            r'# Mock session avec context manager',
            r'# Mock session simple',
            content
        )
        
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