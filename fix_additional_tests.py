#!/usr/bin/env python3
"""
Script pour corriger les tests home avec les colonnes Streamlit
"""

import os
import re

def fix_home_tests():
    """Corrige les tests home pour gérer st.columns correctement"""
    
    home_test_files = [
        "tests/unit/pages_modules/test_home_mega_coverage.py",
        "tests/unit/pages_modules/test_home_realistic.py",
        "tests/unit/pages_modules/test_home_targeted.py"
    ]
    
    for file_path in home_test_files:
        if not os.path.exists(file_path):
            continue
            
        print(f"📝 Traitement de {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Add proper columns mocking in setUp
            setup_pattern = r'(def setUp\(self\):.*?)(def test_|class |$)'
            
            def add_columns_mock(match):
                setup_content = match.group(1)
                next_content = match.group(2)
                
                if 'mock_col' not in setup_content:
                    setup_content = setup_content.replace(
                        'def setUp(self):',
                        '''def setUp(self):
        self.mock_col = MagicMock()
        self.mock_col.__enter__ = MagicMock(return_value=self.mock_col)
        self.mock_col.__exit__ = MagicMock(return_value=None)'''
                    )
                
                return setup_content + next_content
            
            content = re.sub(setup_pattern, add_columns_mock, content, flags=re.DOTALL)
            
            # Fix all patches to use app.pages_modules.home.st.*
            patches_to_fix = [
                ('streamlit.columns', 'app.pages_modules.home.st.columns'),
                ('streamlit.title', 'app.pages_modules.home.st.title'),
                ('streamlit.markdown', 'app.pages_modules.home.st.markdown'),
                ('streamlit.write', 'app.pages_modules.home.st.write'),
                ('streamlit.success', 'app.pages_modules.home.st.success'),
                ('streamlit.error', 'app.pages_modules.home.st.error'),
                ('streamlit.warning', 'app.pages_modules.home.st.warning'),
                ('streamlit.info', 'app.pages_modules.home.st.info'),
                ('streamlit.metric', 'app.pages_modules.home.st.metric'),
                ('streamlit.button', 'app.pages_modules.home.st.button'),
                ('streamlit.plotly_chart', 'app.pages_modules.home.st.plotly_chart'),
            ]
            
            for old_patch, new_patch in patches_to_fix:
                content = re.sub(
                    rf"@patch\(['\"]({re.escape(old_patch)})['\"]",
                    f"@patch('{new_patch}'",
                    content
                )
            
            # Fix mock columns return values
            content = re.sub(
                r'mock_columns\.return_value = \[([^\]]+)\]',
                r'mock_columns.return_value = (\1)',
                content
            )
            
            # Add specific return values for different column configurations
            test_methods = re.findall(r'def (test_[^(]+)', content)
            
            for method in test_methods:
                # Find method and add proper mocking
                method_pattern = rf'(def {re.escape(method)}\([^)]*\):.*?)(?=def |\Z)'
                method_match = re.search(method_pattern, content, re.DOTALL)
                
                if method_match:
                    method_content = method_match.group(1)
                    
                    # If method uses st.columns but doesn't have proper mocking
                    if 'st.columns' in method_content and '@patch' in method_content:
                        # Ensure mock_columns returns proper tuples
                        if 'st.columns(3)' in method_content or 'col1, col2, col3' in method_content:
                            if 'mock_columns.return_value' not in method_content:
                                method_content = method_content.replace(
                                    'def ' + method,
                                    'def ' + method + '''
        mock_columns.return_value = (self.mock_col, self.mock_col, self.mock_col)'''
                                )
                        elif 'st.columns(2)' in method_content or '_, col2' in method_content:
                            if 'mock_columns.return_value' not in method_content:
                                method_content = method_content.replace(
                                    'def ' + method,
                                    'def ' + method + '''
        mock_columns.return_value = (self.mock_col, self.mock_col)'''
                                )
                        
                        content = content.replace(method_match.group(1), method_content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Corrigé: {file_path}")
            else:
                print(f"⏭️  Aucune correction nécessaire: {file_path}")
        
        except Exception as e:
            print(f"❌ Erreur lors de la correction de {file_path}: {e}")

def fix_format_string_errors():
    """Corrige les erreurs de format string avec MagicMock"""
    
    test_files = [
        "tests/unit/pages_modules/test_consultants_massive_coverage.py",
        "tests/unit/pages_modules/test_consultants_ultra_coverage.py",
        "tests/test_consultants_simple_coverage.py"
    ]
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            continue
            
        print(f"📝 Correction format strings dans {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Add real values to consultants to avoid format string errors
            setup_pattern = r'(def setUp\(self\):.*?)(def test_|class |$)'
            
            def add_real_values(match):
                setup_content = match.group(1)
                next_content = match.group(2)
                
                if 'self.mock_consultant.salaire_actuel = ' not in setup_content:
                    setup_content = setup_content.replace(
                        'self.mock_consultant = MagicMock()',
                        '''self.mock_consultant = MagicMock()
        self.mock_consultant.salaire_actuel = 50000
        self.mock_consultant.id = 1
        self.mock_consultant.prenom = "Jean"
        self.mock_consultant.nom = "Dupont"'''
                    )
                
                return setup_content + next_content
            
            content = re.sub(setup_pattern, add_real_values, content, flags=re.DOTALL)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Format strings corrigés: {file_path}")
            else:
                print(f"⏭️  Pas de correction de format nécessaire: {file_path}")
        
        except Exception as e:
            print(f"❌ Erreur lors de la correction des formats dans {file_path}: {e}")

def main():
    """Fonction principale"""
    print("🔧 Correction des tests home et format strings...")
    
    fix_home_tests()
    print("\n")
    fix_format_string_errors()
    
    print("\n✅ Corrections terminées!")

if __name__ == "__main__":
    main()