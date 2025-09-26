#!/usr/bin/env python3
"""
Maintenance Quotidienne - Amélioration Continue des Tests
Script à exécuter régulièrement pour maintenir et améliorer la couverture de tests.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Configuration
WORKSPACE = Path(__file__).parent.parent
COVERAGE_TARGET = 80.0  # Objectif de couverture

def daily_maintenance():
    """Routine de maintenance quotidienne"""
    
    print("🔧 MAINTENANCE QUOTIDIENNE DES TESTS")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
    
    # 1. Nettoyage de l'environnement
    print("1️⃣ Nettoyage de l'environnement")
    cleanup_result = run_cleanup()
    
    # 2. Analyse de couverture actuelle
    print("\n2️⃣ Analyse de la couverture")
    coverage_result = analyze_coverage()
    
    # 3. Exécution des tests critiques
    print("\n3️⃣ Tests de régression")
    regression_result = run_regression_tests()
    
    # 4. Identification des opportunités d'amélioration
    print("\n4️⃣ Opportunités d'amélioration")
    opportunities = identify_opportunities()
    
    # 5. Génération de nouveaux tests si nécessaire
    print("\n5️⃣ Génération de tests")
    generation_result = auto_generate_tests()
    
    # 6. Rapport de maintenance
    print("\n6️⃣ Rapport de maintenance")
    generate_maintenance_report({
        'cleanup': cleanup_result,
        'coverage': coverage_result,
        'regression': regression_result,
        'opportunities': opportunities,
        'generation': generation_result
    })
    
    print("\n✅ MAINTENANCE TERMINÉE")

def run_cleanup():
    """Exécute le nettoyage de l'environnement"""
    try:
        result = subprocess.run([
            sys.executable, "scripts/clean_test_environment.py"
        ], cwd=WORKSPACE, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ Environnement nettoyé")
            return "success"
        else:
            print("   ⚠️ Problèmes lors du nettoyage")
            return "warning"
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return "error"

def analyze_coverage():
    """Analyse la couverture actuelle"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/unit/services/test_priority_services.py",
            "tests/unit/pages/test_consultant_pages.py", 
            "tests/regression/test_vsa_import_regression.py",
            "--cov=app",
            "--cov-report=json:reports/coverage_daily.json",
            "--quiet"
        ], cwd=WORKSPACE, capture_output=True, text=True, timeout=120)
        
        # Lire le fichier de couverture
        coverage_file = WORKSPACE / "reports" / "coverage_daily.json"
        if coverage_file.exists():
            import json
            with open(coverage_file) as f:
                data = json.load(f)
            
            coverage_pct = data['totals']['percent_covered']
            print(f"   📊 Couverture actuelle: {coverage_pct:.1f}%")
            
            if coverage_pct >= COVERAGE_TARGET:
                print(f"   🎯 Objectif atteint! ({COVERAGE_TARGET}%)")
            else:
                remaining = COVERAGE_TARGET - coverage_pct
                print(f"   📈 Objectif: {COVERAGE_TARGET}% (reste {remaining:.1f}%)")
            
            return {'percentage': coverage_pct, 'status': 'success'}
        else:
            print("   ⚠️ Fichier de couverture non trouvé")
            return {'percentage': 0, 'status': 'warning'}
            
    except Exception as e:
        print(f"   ❌ Erreur d'analyse: {e}")
        return {'percentage': 0, 'status': 'error'}

def run_regression_tests():
    """Exécute les tests de régression critiques"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/regression/test_vsa_import_regression.py",
            "-v"
        ], cwd=WORKSPACE, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ Tous les tests de régression passent")
            return "success"
        else:
            print("   ❌ Échecs dans les tests de régression!")
            print(f"   Détails: {result.stdout[-200:]}")
            return "failure"
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return "error"

def identify_opportunities():
    """Identifie les opportunités d'amélioration"""
    opportunities = []
    
    # Vérifier les modules sans tests
    app_files = list((WORKSPACE / "app").rglob("*.py"))
    test_files = list((WORKSPACE / "tests").rglob("test_*.py"))
    
    tested_modules = set()
    for test_file in test_files:
        # Extraire le nom du module testé
        content = test_file.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if 'from app.' in line or 'import app.' in line:
                module_path = line.split('from ')[-1].split('import')[0].strip()
                tested_modules.add(module_path)
    
    # Modules principaux à prioriser
    priority_modules = [
        'app.services.consultant_service',
        'app.services.document_service', 
        'app.pages.consultants',
        'app.pages.missions'
    ]
    
    untested_priority = []
    for module in priority_modules:
        if module not in tested_modules:
            untested_priority.append(module)
    
    if untested_priority:
        print("   🎯 Modules prioritaires sans tests:")
        for module in untested_priority:
            print(f"      - {module}")
        opportunities.extend(untested_priority)
    else:
        print("   ✅ Tous les modules prioritaires ont des tests")
    
    # Vérifier les templates générés non complétés
    template_files = list((WORKSPACE / "tests").rglob("*_generated.py"))
    incomplete_templates = []
    
    for template_file in template_files:
        content = template_file.read_text(encoding='utf-8')
        if "# TODO:" in content or "pass  # TODO" in content:
            incomplete_templates.append(template_file.name)
    
    if incomplete_templates:
        print("   🔧 Templates à compléter:")
        for template in incomplete_templates:
            print(f"      - {template}")
        opportunities.extend([f"Complete template: {t}" for t in incomplete_templates])
    
    return opportunities

def auto_generate_tests():
    """Génère automatiquement de nouveaux tests si nécessaire"""
    try:
        # Générer jusqu'à 3 nouveaux modules de tests
        result = subprocess.run([
            sys.executable, "scripts/develop_tests_systematically.py", "3"
        ], cwd=WORKSPACE, capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            if "Templates générés" in result.stdout:
                print("   ✅ Nouveaux templates générés")
                return "generated"
            else:
                print("   📋 Aucun nouveau template nécessaire")
                return "none_needed"
        else:
            print("   ⚠️ Génération partielle")
            return "partial"
            
    except Exception as e:
        print(f"   ❌ Erreur de génération: {e}")
        return "error"

def generate_maintenance_report(results: Dict):
    """Génère un rapport de maintenance"""
    
    report_content = f"""# 🔧 Rapport de Maintenance - {datetime.now().strftime('%d/%m/%Y')}

## Résumé des Opérations

### Statut Global
- **Nettoyage**: {'✅ OK' if results['cleanup'] == 'success' else '⚠️ Problème'}
- **Couverture**: {results['coverage']['percentage']:.1f}% {'✅' if results['coverage']['percentage'] >= COVERAGE_TARGET else '📈'}
- **Régression**: {'✅ OK' if results['regression'] == 'success' else '❌ ÉCHEC'}
- **Génération**: {'✅ OK' if results['generation'] in ['generated', 'none_needed'] else '⚠️ Partielle'}

## Détails

### Couverture de Tests
- **Actuelle**: {results['coverage']['percentage']:.1f}%
- **Objectif**: {COVERAGE_TARGET}%
- **Écart**: {COVERAGE_TARGET - results['coverage']['percentage']:.1f}%

### Opportunités Identifiées ({len(results['opportunities'])})
"""
    
    for i, opp in enumerate(results['opportunities'][:10], 1):
        report_content += f"{i}. {opp}\n"
    
    if len(results['opportunities']) > 10:
        report_content += f"... et {len(results['opportunities']) - 10} autres\n"
    
    report_content += f"""
## Actions Recommandées

### Priorité Immédiate
1. {'Corriger les tests de régression' if results['regression'] != 'success' else 'Maintenir les tests de régression'}
2. {'Améliorer les mocks défaillants' if results['coverage']['percentage'] < 15 else 'Étendre la couverture des services'}
3. {'Compléter les templates générés' if 'template' in str(results['opportunities']) else 'Créer de nouveaux tests'}

### Prochaine Maintenance
- Exécuter ce script quotidiennement
- Compléter progressivement les templates générés
- Ajouter des tests pour les nouvelles fonctionnalités

---
*Rapport généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}*
"""
    
    # Sauvegarder le rapport
    report_file = WORKSPACE / "reports" / f"maintenance_{datetime.now().strftime('%Y%m%d')}.md"
    report_file.write_text(report_content, encoding='utf-8')
    
    print(f"   📋 Rapport sauvegardé: {report_file.name}")

def main():
    """Fonction principale"""
    daily_maintenance()

if __name__ == "__main__":
    main()