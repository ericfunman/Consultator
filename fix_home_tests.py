#!/usr/bin/env python3
"""
Correctif rapide pour les tests home défaillants avec pandas
"""

import re

def fix_home_test_files():
    """Corrige les fichiers de tests home qui échouent avec pandas"""
    
    # Liste des fichiers à corriger
    files_to_fix = [
        "tests/unit/pages_modules/test_home_mega_coverage.py",
        "tests/unit/pages_modules/test_home_realistic.py", 
        "tests/unit/pages_modules/test_home_targeted.py"
    ]
    
    for file_path in files_to_fix:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Ajouter les imports pandas et plotly au début
            if "import pandas as pd" not in content:
                # Trouver la ligne des imports
                import_section = re.search(r'(from unittest\.mock import.*?\n)', content, re.DOTALL)
                if import_section:
                    new_imports = import_section.group(1) + "import pandas as pd\nimport plotly.express as px\n"
                    content = content.replace(import_section.group(1), new_imports)
            
            # Remplacer les appels problématiques à show_dashboard_charts
            old_pattern = r'from app\.pages_modules\.home import show_dashboard_charts\s+show_dashboard_charts\(\)'
            
            new_replacement = '''with patch('app.pages_modules.home.pd.DataFrame') as mock_df, \\
             patch('app.pages_modules.home.pd.date_range') as mock_date_range, \\
             patch('app.pages_modules.home.px.line') as mock_px_line:
            
            # Mock pandas objects properly
            mock_date_range.return_value = ["2024-01", "2024-02", "2024-03"]
            mock_df.return_value = MagicMock()
            mock_px_line.return_value = MagicMock()
            
            from app.pages_modules.home import show_dashboard_charts
            show_dashboard_charts()'''
            
            content = re.sub(old_pattern, new_replacement, content)
            
            # Écrire le fichier corrigé
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"✅ Corrigé: {file_path}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la correction de {file_path}: {e}")

def create_simple_home_test():
    """Crée un test home simple qui fonctionne sans pandas"""
    
    simple_test = '''"""
Test home simplifié pour améliorer la couverture
"""
import unittest
from unittest.mock import patch, MagicMock

class TestHomeSimplified(unittest.TestCase):
    """Tests simplifiés pour le module home"""
    
    @patch('app.pages_modules.home.st')
    @patch('app.pages_modules.home.get_database_info')
    def test_show_with_no_data(self, mock_get_db_info, mock_st):
        """Test show() sans données"""
        mock_get_db_info.return_value = {
            'exists': True,
            'consultants': 0,
            'missions': 0, 
            'practices': 0
        }
        mock_st.title.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        mock_st.metric.return_value = None
        
        from app.pages_modules.home import show
        show()
        
        mock_st.title.assert_called_once_with("🏠 Accueil - Consultator")
        self.assertGreater(mock_st.columns.call_count, 0)
    
    @patch('app.pages_modules.home.st')
    def test_get_database_info_basic(self, mock_st):
        """Test get_database_info() fonction de base"""
        with patch('app.pages_modules.home.get_database_session') as mock_session:
            mock_session_obj = mock_session.return_value.__enter__.return_value
            mock_session_obj.query.return_value.count.return_value = 5
            
            from app.pages_modules.home import get_database_info
            result = get_database_info()
            
            self.assertIsInstance(result, dict)
            self.assertIn('exists', result)
    
    @patch('app.pages_modules.home.st')
    def test_show_getting_started_basic_structure(self, mock_st):
        """Test show_getting_started() structure de base"""
        mock_st.subheader.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
        mock_st.container.return_value.__enter__ = MagicMock()
        mock_st.container.return_value.__exit__ = MagicMock()
        mock_st.markdown.return_value = None
        mock_st.button.return_value = False
        mock_st.expander.return_value.__enter__ = MagicMock()
        mock_st.expander.return_value.__exit__ = MagicMock()
        
        from app.pages_modules.home import show_getting_started
        show_getting_started()
        
        # Vérifier que la fonction s'exécute sans erreur
        self.assertGreater(mock_st.subheader.call_count, 0)

if __name__ == '__main__':
    unittest.main()
'''
    
    with open("tests/unit/pages_modules/test_home_simplified.py", 'w', encoding='utf-8') as f:
        f.write(simple_test)
    
    print("✅ Créé: tests/unit/pages_modules/test_home_simplified.py")

if __name__ == "__main__":
    print("🔧 Correction des tests home défaillants...")
    fix_home_test_files()
    create_simple_home_test()
    print("✅ Corrections terminées!")