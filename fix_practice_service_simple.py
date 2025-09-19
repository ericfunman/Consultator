#!/usr/bin/env python3
"""
Script pour corriger test_practice_service_optimized.py
Signatures, assertions et valeurs de retour
"""

import re

def fix_practice_service_test_file():
    """Corrige le fichier de test practice service"""
    
    file_path = "tests/unit/test_practice_service_optimized.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Corrections practice service tests...")
    
    # 1. Corriger les signatures de méthodes
    signature_fixes = [
        # update_practice a la signature update_practice(practice_id: int, **kwargs) -> bool
        (r'PracticeService\.update_practice\(1, practice_data\)', 
         'PracticeService.update_practice(1, **practice_data)'),
    ]
    
    for pattern, replacement in signature_fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print(f"✅ Corrigé signature: {pattern}")
    
    # 2. Corriger les assertions invalides
    assertion_fixes = [
        # None is False -> result is None
        (r'assert result is False  # Should return False on error  # Should return None on error', 
         'assert result is None  # Should return None on error'),
         
        (r'assert None is False', 'assert result is False'),
        (r'assert None is True', 'assert result is True'),
    ]
    
    for pattern, replacement in assertion_fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print(f"✅ Corrigé assertion: {pattern}")
    
    # Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fichier corrigé: {file_path}")
    return True

if __name__ == "__main__":
    print("🚀 Correction du fichier test_practice_service_optimized.py")
    fix_practice_service_test_file()
    print("Testons les corrections...")