#!/usr/bin/env python3
"""
Script pour corriger systématiquement les tests défaillants des consultants
"""

import os
import re
from pathlib import Path

def fix_streamlit_patches_in_file(file_path):
    """Corrige les patches Streamlit dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Correction des patches Streamlit
        patches_to_fix = [
            ('streamlit.columns', 'app.pages_modules.consultants.st.columns'),
            ('streamlit.date_input', 'app.pages_modules.consultants.st.date_input'),
            ('streamlit.selectbox', 'app.pages_modules.consultants.st.selectbox'),
            ('streamlit.tabs', 'app.pages_modules.consultants.st.tabs'),
            ('streamlit.metric', 'app.pages_modules.consultants.st.metric'),
            ('streamlit.title', 'app.pages_modules.consultants.st.title'),
            ('streamlit.markdown', 'app.pages_modules.consultants.st.markdown'),
            ('streamlit.write', 'app.pages_modules.consultants.st.write'),
            ('streamlit.success', 'app.pages_modules.consultants.st.success'),
            ('streamlit.error', 'app.pages_modules.consultants.st.error'),
            ('streamlit.warning', 'app.pages_modules.consultants.st.warning'),
            ('streamlit.info', 'app.pages_modules.consultants.st.info'),
            ('streamlit.expander', 'app.pages_modules.consultants.st.expander'),
            ('streamlit.form', 'app.pages_modules.consultants.st.form'),
            ('streamlit.form_submit_button', 'app.pages_modules.consultants.st.form_submit_button'),
            ('streamlit.checkbox', 'app.pages_modules.consultants.st.checkbox'),
            ('streamlit.button', 'app.pages_modules.consultants.st.button'),
            ('streamlit.text_input', 'app.pages_modules.consultants.st.text_input'),
            ('streamlit.text_area', 'app.pages_modules.consultants.st.text_area'),
            ('streamlit.number_input', 'app.pages_modules.consultants.st.number_input'),
            ('streamlit.spinner', 'app.pages_modules.consultants.st.spinner'),
            ('streamlit.rerun', 'app.pages_modules.consultants.st.rerun'),
        ]
        
        for old_patch, new_patch in patches_to_fix:
            # Correction des @patch decorators
            content = re.sub(
                rf"@patch\(['\"]({re.escape(old_patch)})['\"]", 
                f"@patch('{new_patch}'", 
                content
            )
        
        # Fix mock columns return value - use tuple instead of list
        content = re.sub(
            r'mock_columns\.return_value = \[([^\]]+)\]',
            r'mock_columns.return_value = (\1)',
            content
        )
        
        # Fix session_state mocking
        content = re.sub(
            r"st\.session_state\.([a-zA-Z_][a-zA-Z0-9_]*)",
            r"st.session_state.get('\1')",
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Corrigé: {file_path}")
            return True
        else:
            print(f"⏭️  Aucune correction nécessaire: {file_path}")
            return False
    
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {file_path}: {e}")
        return False

def add_date_mocking_to_tests(file_path):
    """Ajoute des dates réelles aux tests qui utilisent des MagicMock"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add imports if missing
        if 'from datetime import date' not in content:
            if 'import unittest' in content:
                content = content.replace(
                    'import unittest',
                    'import unittest\nfrom datetime import date'
                )
            elif 'from unittest.mock import' in content:
                content = content.replace(
                    'from unittest.mock import',
                    'from datetime import date\nfrom unittest.mock import'
                )
        
        # Add real dates to consultant mocks in setUp methods
        setup_pattern = r'(def setUp\(self\):.*?)(def test_|class |$)'
        
        def add_date_attributes(match):
            setup_content = match.group(1)
            next_content = match.group(2)
            
            if 'self.mock_consultant.date_entree' not in setup_content:
                setup_content = setup_content.replace(
                    'self.mock_consultant = MagicMock()',
                    '''self.mock_consultant = MagicMock()
        self.mock_consultant.date_entree = date(2022, 1, 1)
        self.mock_consultant.date_sortie = date(2023, 12, 31)
        self.mock_consultant.date_premiere_mission = date(2022, 1, 15)'''
                )
            
            return setup_content + next_content
        
        content = re.sub(setup_pattern, add_date_attributes, content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Dates ajoutées: {file_path}")
            return True
        else:
            print(f"⏭️  Dates déjà présentes: {file_path}")
            return False
    
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de dates dans {file_path}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 Correction systématique des tests de consultants...")
    
    # Fichiers de test à corriger
    test_files = [
        "tests/unit/pages_modules/test_consultants_fixed_coverage.py",
        "tests/unit/pages_modules/test_consultants_massive_coverage.py",
        "tests/unit/pages_modules/test_consultants_optimized_coverage.py",
        "tests/unit/pages_modules/test_consultants_ultra_coverage.py",
        "tests/unit/pages_modules/test_consultants_advanced_coverage.py",
        "tests/unit/pages_modules/test_consultants_coverage_optimized.py",
        "tests/unit/pages_modules/test_consultants_final_coverage.py",
    ]
    
    fixed_count = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📝 Traitement de {test_file}...")
            
            # Correction des patches Streamlit
            if fix_streamlit_patches_in_file(test_file):
                fixed_count += 1
            
            # Ajout des dates réelles
            if add_date_mocking_to_tests(test_file):
                fixed_count += 1
        else:
            print(f"⚠️  Fichier non trouvé: {test_file}")
    
    print(f"\n✅ Correction terminée! {fixed_count} fichiers modifiés.")
    print("\n📊 Lancez maintenant: pytest tests/test_consultants_simple_coverage.py pour vérifier")

if __name__ == "__main__":
    main()