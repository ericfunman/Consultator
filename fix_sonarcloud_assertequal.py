#!/usr/bin/env python3
"""
Script pour corriger les issues SonarCloud MINOR "Consider using assertEqual instead"
Remplace assertTrue/assertFalse par assertEquals plus spécifiques
"""

import os
import re
import glob
from typing import List, Tuple

class SonarCloudAssertEqualFixer:
    def __init__(self):
        self.patterns = [
            # assertTrue avec expressions d'égalité
            (r'assertTrue\(([^()]+)\s*==\s*([^()]+)\)', r'assertEqual(\1, \2)'),
            (r'assertTrue\(([^()]+)\s*is\s*([^()]+)\)', r'assertIs(\1, \2)'),
            (r'assertTrue\(([^()]+)\s*in\s*([^()]+)\)', r'assertIn(\1, \2)'),
            
            # assertFalse avec expressions d'inégalité
            (r'assertFalse\(([^()]+)\s*==\s*([^()]+)\)', r'assertNotEqual(\1, \2)'),
            (r'assertFalse\(([^()]+)\s*is\s*([^()]+)\)', r'assertIsNot(\1, \2)'),
            (r'assertFalse\(([^()]+)\s*in\s*([^()]+)\)', r'assertNotIn(\1, \2)'),
            
            # assertTrue avec len()
            (r'assertTrue\(len\(([^()]+)\)\s*==\s*0\)', r'assertEqual(len(\1), 0)'),
            (r'assertTrue\(len\(([^()]+)\)\s*>\s*0\)', r'assertGreater(len(\1), 0)'),
            (r'assertTrue\(len\(([^()]+)\)\)', r'assertGreater(len(\1), 0)'),
            
            # assertFalse avec len()
            (r'assertFalse\(len\(([^()]+)\)\s*==\s*0\)', r'assertNotEqual(len(\1), 0)'),
            (r'assertFalse\(len\(([^()]+)\)\)', r'assertEqual(len(\1), 0)'),
            
            # Cas simples basiques
            (r'assertTrue\(([^()]+)\s*!=\s*([^()]+)\)', r'assertNotEqual(\1, \2)'),
            (r'assertFalse\(([^()]+)\s*!=\s*([^()]+)\)', r'assertEqual(\1, \2)'),
        ]
        
        self.corrections_applied = 0
        self.files_processed = 0

    def fix_assertions_in_file(self, file_path: str) -> bool:
        """Corrige les assertions dans un fichier"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_corrections = 0
            
            for pattern, replacement in self.patterns:
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, replacement, content)
                    file_corrections += len(matches)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {file_path}: {file_corrections} corrections appliquées")
                self.corrections_applied += file_corrections
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erreur dans {file_path}: {e}")
            return False

    def process_test_files(self) -> None:
        """Traite tous les fichiers de test Python"""
        test_patterns = [
            "tests/**/*.py",
            "tests/unit/**/*.py",
            "tests/unit/**/test_*.py"
        ]
        
        processed_files = set()
        
        for pattern in test_patterns:
            for file_path in glob.glob(pattern, recursive=True):
                if file_path not in processed_files:
                    processed_files.add(file_path)
                    self.files_processed += 1
                    self.fix_assertions_in_file(file_path)

    def run(self):
        """Lance la correction des assertions"""
        print("🔧 Correction des assertions SonarCloud...")
        print("📁 Recherche des fichiers de test...")
        
        self.process_test_files()
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"   📁 Fichiers traités: {self.files_processed}")
        print(f"   ✅ Corrections appliquées: {self.corrections_applied}")
        print(f"\n🎯 Les assertions ont été optimisées pour SonarCloud!")

if __name__ == "__main__":
    fixer = SonarCloudAssertEqualFixer()
    fixer.run()