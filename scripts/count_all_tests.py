#!/usr/bin/env python3
"""
Analyse exhaustive du nombre de tests dans Consultator
"""

import os
from pathlib import Path

def count_all_tests():
    workspace = Path('.')
    test_count = {
        'functional': 0, 
        'problematic': 0, 
        'auto_generated': 0, 
        'backup': 0,
        'total_files': 0
    }

    print("🔍 ANALYSE EXHAUSTIVE DES TESTS CONSULTATOR")
    print("=" * 50)
    
    # Tests fonctionnels
    print("\n📊 Tests fonctionnels:")
    functional_dirs = [
        'tests/unit/services',
        'tests/unit/pages', 
        'tests/unit/pages_modules',
        'tests/regression'
    ]

    for dir_path in functional_dirs:
        dir_full = workspace / dir_path
        if dir_full.exists():
            print(f"   📁 {dir_path}:")
            for test_file in dir_full.glob('test_*.py'):
                try:
                    with open(test_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        test_methods = content.count('def test_')
                        test_count['functional'] += test_methods
                        test_count['total_files'] += 1
                        print(f"      📄 {test_file.name}: {test_methods} tests")
                except Exception as e:
                    print(f"      ❌ {test_file.name}: erreur de lecture")

    # Tests auto-générés
    print("\n🤖 Tests auto-générés:")
    auto_dir = workspace / 'tests/auto_generated'
    if auto_dir.exists():
        for test_file in auto_dir.rglob('test_*.py'):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    test_methods = content.count('def test_')
                    test_count['auto_generated'] += test_methods
                    test_count['total_files'] += 1
                    if test_methods > 0:
                        print(f"   📄 {test_file.name}: {test_methods} tests")
            except Exception as e:
                pass

    # Tests problématiques
    print("\n⚠️ Tests problématiques:")
    prob_dir = workspace / 'tests/problematic_tests'
    if prob_dir.exists():
        for test_file in prob_dir.rglob('test_*.py'):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    test_methods = content.count('def test_')
                    test_count['problematic'] += test_methods
                    test_count['total_files'] += 1
                    if test_methods > 0:
                        print(f"   📄 {test_file.name}: {test_methods} tests")
            except Exception as e:
                pass

    # Tests en backup
    print("\n💾 Tests en backup:")
    backup_dir = workspace / 'tests_backup'
    if backup_dir.exists():
        for test_file in backup_dir.rglob('test_*.py'):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    test_methods = content.count('def test_')
                    test_count['backup'] += test_methods
                    if test_methods > 0:
                        print(f"   📄 {test_file.name}: {test_methods} tests")
            except:
                pass

    # Autres tests (racine)
    root_tests = 0
    for test_file in workspace.glob('test_*.py'):
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                test_methods = content.count('def test_')
                root_tests += test_methods
                if test_methods > 0:
                    print(f"   📄 {test_file.name}: {test_methods} tests (racine)")
        except:
            pass

    total_tests = (test_count['functional'] + test_count['auto_generated'] + 
                   test_count['problematic'] + test_count['backup'] + root_tests)

    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ COMPLET:")
    print("=" * 50)
    print(f"   🧪 Tests fonctionnels opérationnels: {test_count['functional']}")
    print(f"   🤖 Tests auto-générés (templates): {test_count['auto_generated']}")
    print(f"   ⚠️  Tests problématiques (isolés): {test_count['problematic']}")
    print(f"   💾 Tests en backup: {test_count['backup']}")
    print(f"   📁 Tests racine: {root_tests}")
    print(f"   📋 Fichiers analysés: {test_count['total_files']}")
    print("-" * 50)
    print(f"   🎯 TOTAL TESTS: {total_tests}")
    print("=" * 50)

    # Évaluation par rapport à l'objectif 2000
    print("\n🎯 ÉVALUATION OBJECTIF 2000 TESTS:")
    if total_tests >= 2000:
        print(f"   ✅ OBJECTIF ATTEINT: {total_tests} tests (>{2000})")
        print(f"   📈 Dépassement: +{total_tests - 2000} tests")
    else:
        print(f"   ❌ OBJECTIF PAS ATTEINT: {total_tests} tests (<2000)")
        print(f"   📈 Il manque: {2000 - total_tests} tests")
        print(f"   📊 Progression: {(total_tests/2000)*100:.1f}%")

    # Évaluation de la qualité
    print("\n💡 ANALYSE QUALITATIVE:")
    operational_tests = test_count['functional']
    total_potential = total_tests - test_count['backup']  # Exclure les backups
    
    print(f"   🟢 Tests opérationnels: {operational_tests} ({(operational_tests/total_potential)*100:.1f}%)")
    print(f"   🟡 Tests à corriger/compléter: {test_count['auto_generated'] + test_count['problematic']} ({((test_count['auto_generated'] + test_count['problematic'])/total_potential)*100:.1f}%)")
    print(f"   🔴 Tests en backup: {test_count['backup']} (non comptabilisés)")

    return total_tests, test_count

if __name__ == "__main__":
    total, details = count_all_tests()