#!/usr/bin/env python3
"""
Script pour identifier les tests qui échouent réellement et de manière consistante
"""

import subprocess
import sys
import re

def run_pytest_and_extract_failures():
    """Lance pytest et extrait la liste des tests en échec"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", 
            "--tb=no", "-q", "--maxfail=100"
        ], capture_output=True, text=True, timeout=300)
        
        output = result.stdout
        
        # Extraire les lignes FAILED
        failed_lines = []
        for line in output.split('\n'):
            if line.strip().startswith('FAILED'):
                failed_lines.append(line.strip())
        
        return failed_lines
        
    except subprocess.TimeoutExpired:
        print("Timeout lors de l'exécution des tests")
        return []
    except Exception as e:
        print(f"Erreur lors de l'exécution des tests: {e}")
        return []

def analyze_failure_patterns(failed_tests):
    """Analyse les patterns d'échec"""
    if not failed_tests:
        print("✅ Aucun test en échec détecté!")
        return
    
    print(f"❌ {len(failed_tests)} tests en échec détectés:")
    print("=" * 80)
    
    # Grouper par type d'erreur principal
    error_patterns = {}
    
    for test in failed_tests:
        # Extraire le message d'erreur
        if " - " in test:
            test_name, error_msg = test.split(" - ", 1)
            
            # Classifier l'erreur
            if "ValueError" in error_msg:
                error_type = "ValueError"
            elif "AssertionError" in error_msg:
                error_type = "AssertionError"
            elif "AttributeError" in error_msg:
                error_type = "AttributeError"
            elif "TypeError" in error_msg:
                error_type = "TypeError"
            elif "NameError" in error_msg:
                error_type = "NameError"
            elif "IndexError" in error_msg:
                error_type = "IndexError"
            elif "UnboundLocalError" in error_msg:
                error_type = "UnboundLocalError"
            else:
                error_type = "Other"
            
            if error_type not in error_patterns:
                error_patterns[error_type] = []
            error_patterns[error_type].append((test_name, error_msg))
        else:
            print(f"Format inattendu: {test}")
    
    # Afficher les résultats groupés
    for error_type, tests in error_patterns.items():
        print(f"\n🔸 {error_type} ({len(tests)} tests):")
        for test_name, error_msg in tests[:5]:  # Limiter à 5 exemples
            print(f"  - {test_name}")
            print(f"    → {error_msg[:100]}...")
        if len(tests) > 5:
            print(f"  ... et {len(tests) - 5} autres tests")
    
    return error_patterns

def generate_fix_priority(error_patterns):
    """Génère les priorités de correction"""
    if not error_patterns:
        return
    
    print("\n" + "=" * 80)
    print("📋 PRIORITÉS DE CORRECTION:")
    print("=" * 80)
    
    # Ordre de priorité des corrections
    priority_order = [
        "ValueError", "TypeError", "NameError", "UnboundLocalError",
        "AttributeError", "AssertionError", "IndexError", "Other"
    ]
    
    for i, error_type in enumerate(priority_order, 1):
        if error_type in error_patterns:
            tests = error_patterns[error_type]
            print(f"\n{i}. {error_type} ({len(tests)} tests) - Priorité {'HAUTE' if i <= 2 else 'MOYENNE' if i <= 4 else 'BASSE'}")
            
            # Suggestion de correction
            if error_type == "ValueError":
                print("   💡 Suggestions: Vérifier formats de données, conversions de types, unpacking")
            elif error_type == "TypeError":
                print("   💡 Suggestions: Vérifier types d'arguments, opérateurs, comparaisons")
            elif error_type == "NameError":
                print("   💡 Suggestions: Ajouter imports manquants, définir variables")
            elif error_type == "UnboundLocalError":
                print("   💡 Suggestions: Corriger scope des variables locales")
            elif error_type == "AttributeError":
                print("   💡 Suggestions: Vérifier attributs mockés, méthodes disponibles")
            elif error_type == "AssertionError":
                print("   💡 Suggestions: Ajuster expectations des mocks, valeurs attendues")

if __name__ == "__main__":
    print("🔍 Analyse des tests en échec...")
    print("=" * 80)
    
    failed_tests = run_pytest_and_extract_failures()
    error_patterns = analyze_failure_patterns(failed_tests)
    generate_fix_priority(error_patterns)
    
    print(f"\n✅ Analyse terminée. {len(failed_tests) if failed_tests else 0} tests analysés.")