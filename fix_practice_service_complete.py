#!/usr/bin/env python3
"""
Script pour corriger TOUS les patterns de mocking dans test_practice_service_optimized.py
"""

import re

def fix_practice_service_tests_complete():
    """Corrige complètement tous les tests du practice service"""
    
    test_file = "tests/unit/test_practice_service_optimized.py"
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📄 Correction complète des tests dans {test_file}")
        
        # 1. Supprimer TOUTES les références aux context managers
        print("   ✅ Suppression des context managers")
        content = re.sub(
            r'mock_session\.return_value\.__enter__\.return_value = mock_db\s*',
            '',
            content
        )
        content = re.sub(
            r'mock_session\.return_value\.__exit__\.return_value = None\s*',
            '',
            content
        )
        
        # 2. Remplacer par des sessions directes
        print("   ✅ Correction des sessions directes")
        content = re.sub(
            r'mock_db = Mock\(\)\s*',
            'mock_db = Mock()\n        mock_session.return_value = mock_db\n        mock_db.close = Mock()\n        ',
            content
        )
        
        # 3. Nettoyer les lignes vides multiples
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 4. Corriger les patterns spécifiques qui restent incorrects
        
        # Pattern pour les tests avec all()
        content = re.sub(
            r'mock_db\.query\.return_value\.filter\.return_value\.order_by\.return_value\.all\.return_value = \[(.*?)\]',
            r'mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [\1]',
            content
        )
        
        # Pattern pour les tests avec first()
        content = re.sub(
            r'mock_db\.query\.return_value\.filter\.return_value\.first\.return_value = \((.*?)\)',
            r'mock_db.query.return_value.filter.return_value.first.return_value = \1',
            content
        )
        
        # Pattern pour les tests avec None
        content = re.sub(
            r'mock_db\.query\.return_value\.filter\.return_value\.first\.return_value = None',
            r'mock_db.query.return_value.filter.return_value.first.return_value = None',
            content
        )
        
        # 5. Supprimer les doublons de configuration de session
        content = re.sub(
            r'(mock_session\.return_value = mock_db\s*mock_db\.close = Mock\(\)\s*){2,}',
            r'mock_session.return_value = mock_db\n        mock_db.close = Mock()\n        ',
            content, flags=re.MULTILINE
        )
        
        # 6. Corriger les indentations
        content = re.sub(r'\n\s{8}mock_session\.return_value = mock_db', '\n        mock_session.return_value = mock_db', content)
        content = re.sub(r'\n\s{8}mock_db\.close = Mock\(\)', '\n        mock_db.close = Mock()', content)
        
        # 7. Corriger les patterns avec join pour get_consultants_by_practice
        content = re.sub(
            r'mock_db\.query\.return_value\.filter\.return_value\.join\.return_value\.all\.return_value = \[(.*?)\]',
            r'mock_db.query.return_value.filter.return_value.join.return_value.all.return_value = [\1]',
            content
        )
        
        # 8. Nettoyer les lignes avec des espaces en trop
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Supprimer les lignes qui ne contiennent que des espaces
            if line.strip() == '':
                cleaned_lines.append('')
            else:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # 9. Corriger la structure des tests pour qu'ils soient cohérents
        # Rechercher tous les tests et s'assurer qu'ils ont la bonne structure
        
        test_pattern = re.compile(
            r'(def test_\w+\(self, mock_st_error, mock_session\):.*?)(\n\s{8}# Execution|\n\s{8}result =)',
            re.DOTALL
        )
        
        def fix_test_structure(match):
            """Corrige la structure d'un test individuel"""
            test_content = match.group(1)
            execution_start = match.group(2)
            
            # S'assurer que chaque test a la structure de base correcte
            if 'mock_session.return_value = mock_db' not in test_content:
                # Ajouter la configuration de base si elle manque
                test_content += '\n        mock_db = Mock()\n        mock_session.return_value = mock_db\n        mock_db.close = Mock()'
            
            return test_content + execution_start
        
        content = test_pattern.sub(fix_test_structure, content)
        
        # Sauvegarder le fichier corrigé
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fichier {test_file} corrigé complètement!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {test_file}: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Correction complète des tests practice service...")
    fix_practice_service_tests_complete()
    print("✅ Correction terminée!")