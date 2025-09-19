#!/usr/bin/env python3
"""
Script pour corriger les imports défaillants dans les tests pages_modules
Remplace les imports via __init__.py par des imports directs
"""

import re
import os
import glob


def fix_pages_modules_imports():
    """Corrige les imports dans tous les tests pages_modules"""
    
    # Trouver tous les fichiers de test pages_modules
    test_files = glob.glob("tests/unit/pages_modules/test_*.py")
    
    fixed_files = []
    
    for file_path in test_files:
        print(f"🔧 Analyse de {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Corriger l'import du module consultants
        old_import = "from app.pages_modules import consultants"
        new_import = "import app.pages_modules.consultants as consultants"
        content = content.replace(old_import, new_import)
        
        # 2. Corriger d'autres imports similaires
        patterns_to_fix = [
            ("from app.pages_modules import home", "import app.pages_modules.home as home"),
            ("from app.pages_modules import practices", "import app.pages_modules.practices as practices"),
            ("from app.pages_modules import business_managers", "import app.pages_modules.business_managers as business_managers"),
            ("from app.pages_modules import technologies", "import app.pages_modules.technologies as technologies"),
            ("from app.pages_modules import documents_functions", "import app.pages_modules.documents_functions as documents_functions"),
        ]
        
        for old_pattern, new_pattern in patterns_to_fix:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                print(f"  ✅ Corrigé: {old_pattern} → {new_pattern}")
        
        # 3. Ajouter un handler pour les imports qui échouent
        if "try:" not in content and "import app.pages_modules" in content:
            # Ajouter une gestion d'erreur pour les imports
            import_section = """
# Configuration des imports pour les tests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
"""
            # Insérer après les premiers imports
            import_index = content.find("import os")
            if import_index > 0:
                content = content[:import_index] + import_section + content[import_index:]
        
        # Sauvegarder si modifié
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Fichier mis à jour: {file_path}")
            fixed_files.append(file_path)
        else:
            print(f"  ⚪ Aucun changement: {file_path}")
    
    return fixed_files


def fix_consultants_test_specifically():
    """Correction spécifique pour le test consultants qui pose le plus de problèmes"""
    
    file_path = "tests/unit/pages_modules/test_unit_consultants_coverage.py"
    
    print(f"🔧 Correction spécifique de {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer complètement la section d'import
    old_import_section = '''# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

try:
    from app.pages_modules import consultants
except ImportError:
    consultants = None'''
    
    new_import_section = '''# Ajouter le chemin du module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

consultants = None
try:
    import app.pages_modules.consultants as consultants
except ImportError as e:
    print(f"Import failed: {e}")
    consultants = None
except Exception as e:
    print(f"Other error: {e}")
    consultants = None'''
    
    if old_import_section in content:
        content = content.replace(old_import_section, new_import_section)
        print("  ✅ Section d'import remplacée")
    
    # Ajouter des vérifications pour éviter les erreurs NoneType
    content = content.replace(
        "assert hasattr(consultants, \"imports_ok\")",
        "assert consultants is not None and hasattr(consultants, \"imports_ok\")"
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Corrections spécifiques appliquées")


if __name__ == "__main__":
    print("🚀 Correction des imports pages_modules...")
    
    fixed_files = fix_pages_modules_imports()
    fix_consultants_test_specifically()
    
    print(f"\n✅ {len(fixed_files)} fichiers corrigés")
    print("🧪 Test: python -m pytest tests/unit/pages_modules/test_unit_consultants_coverage.py::TestConsultantsImports::test_imports_available -v")