#!/usr/bin/env python3
"""
SCRIPT D'AMÉLIORATION DE LA COUVERTURE DE CODE
==============================================

Ce script identifie les modules critiques avec faible couverture
et propose des améliorations concrètes.

Usage:
    python improve_coverage.py [--module MODULE] [--target TARGET]

Options:
    --module: Module spécifique à analyser (ex: consultants, main)
    --target: Couverture cible (défaut: 80)
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple

class CoverageAnalyzer:
    """Analyseur de couverture de code pour Consultator"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.reports_dir = self.project_root / "reports"
        self.tests_dir = self.project_root / "tests"

    def run_coverage_analysis(self) -> Dict:
        """Exécute l'analyse de couverture et retourne les résultats"""
        print("🔍 Analyse de la couverture de code en cours...")

        # Exécuter pytest avec couverture
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/unit/",
            "--cov=app",
            "--cov-report=json:reports/coverage.json",
            "--cov-report=term-missing",
            "-q", "--no-header"
        ]

        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            print(f"✅ Analyse terminée (code: {result.returncode})")

            # Charger le rapport JSON
            coverage_file = self.reports_dir / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print("⚠️ Fichier de couverture non trouvé")
                return {}

        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            return {}

    def identify_critical_modules(self, coverage_data: Dict) -> List[Tuple[str, float, int]]:
        """Identifie les modules critiques avec faible couverture"""
        critical_modules = []

        if 'files' not in coverage_data:
            return critical_modules

        for file_path, data in coverage_data['files'].items():
            # Convertir le chemin relatif
            if file_path.startswith('app/'):
                relative_path = file_path
            else:
                continue

            # Calculer la couverture
            statements = data.get('summary', {}).get('num_statements', 0)
            missing = data.get('summary', {}).get('missing_lines', 0)
            covered = statements - missing

            if statements > 0:
                coverage_percent = (covered / statements) * 100
            else:
                coverage_percent = 100.0

            # Identifier les modules critiques
            if (coverage_percent < 50 and statements > 50) or \
               (relative_path in ['app/main.py', 'app/pages_modules/consultants.py']):

                critical_modules.append((
                    relative_path,
                    coverage_percent,
                    statements
                ))

        # Trier par priorité (taille + couverture faible)
        critical_modules.sort(key=lambda x: (x[2] * (100 - x[1])), reverse=True)

        return critical_modules

    def generate_test_plan(self, critical_modules: List[Tuple[str, float, int]]) -> Dict:
        """Génère un plan de test pour améliorer la couverture"""
        test_plan = {
            "modules": [],
            "estimated_tests": 0,
            "estimated_time": 0,
            "priority_order": []
        }

        for module_path, coverage, lines in critical_modules:
            module_name = module_path.split('/')[-1].replace('.py', '')

            # Analyser le fichier pour identifier les fonctions
            functions_to_test = self.analyze_module_functions(module_path)

            module_plan = {
                "name": module_name,
                "path": module_path,
                "current_coverage": coverage,
                "lines": lines,
                "functions_to_test": functions_to_test,
                "estimated_tests": len(functions_to_test),
                "priority": self.calculate_priority(coverage, lines)
            }

            test_plan["modules"].append(module_plan)
            test_plan["estimated_tests"] += len(functions_to_test)
            test_plan["estimated_time"] += len(functions_to_test) * 15  # 15 min par test

        # Trier par priorité
        test_plan["modules"].sort(key=lambda x: x["priority"], reverse=True)
        test_plan["priority_order"] = [m["name"] for m in test_plan["modules"]]

        return test_plan

    def analyze_module_functions(self, module_path: str) -> List[str]:
        """Analyse un module pour identifier les fonctions à tester"""
        functions = []
        full_path = self.project_root / module_path

        if not full_path.exists():
            return functions

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Recherche basique de fonctions (peut être améliorée)
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('def ') and not line.startswith('def _'):
                    # Extraire le nom de la fonction
                    func_name = line.split('def ')[1].split('(')[0].strip()
                    functions.append(func_name)

        except Exception as e:
            print(f"⚠️ Erreur lors de l'analyse de {module_path}: {e}")

        return functions

    def calculate_priority(self, coverage: float, lines: int) -> float:
        """Calcule la priorité d'un module (plus élevé = plus prioritaire)"""
        # Formule: taille * (100 - couverture) / 100
        return (lines * (100 - coverage)) / 100

    def generate_test_template(self, module_plan: Dict) -> str:
        """Génère un template de test pour un module"""
        module_name = module_plan["name"]
        functions = module_plan["functions_to_test"]

        template = f'''"""Tests pour le module {module_name}"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st

# Import du module à tester
from app.pages_modules.{module_name} import *

class Test{module_name.title()}:
    """Tests pour le module {module_name}"""

'''

        for func in functions[:5]:  # Limiter aux 5 premières fonctions
            template += f'''
    def test_{func}_basic(self):
        """Test de base pour {func}"""
        # TODO: Implémenter le test
        # Arrange
        # Act
        # Assert
        pass

    def test_{func}_edge_cases(self):
        """Test des cas limites pour {func}"""
        # TODO: Implémenter les tests de cas limites
        pass
'''

        template += '''
    def test_module_imports(self):
        """Test que les imports du module fonctionnent"""
        # Vérifier que les fonctions principales sont importables
        assert callable(show)  # Fonction principale si elle existe
'''

        return template

    def create_test_file(self, module_plan: Dict):
        """Crée un fichier de test pour un module"""
        module_name = module_plan["name"]
        test_content = self.generate_test_template(module_plan)

        # Créer le répertoire si nécessaire
        test_dir = self.tests_dir / "ui"
        test_dir.mkdir(exist_ok=True)

        # Créer le fichier de test
        test_file = test_dir / f"test_{module_name}.py"

        if not test_file.exists():
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            print(f"✅ Fichier de test créé: {test_file}")
        else:
            print(f"⚠️ Fichier de test existe déjà: {test_file}")

def main():
    """Fonction principale"""
    print("🚀 Script d'amélioration de la couverture de code")
    print("=" * 60)

    # Initialiser l'analyseur
    analyzer = CoverageAnalyzer(".")

    # Analyser la couverture
    coverage_data = analyzer.run_coverage_analysis()

    if not coverage_data:
        print("❌ Impossible d'obtenir les données de couverture")
        return

    # Identifier les modules critiques
    critical_modules = analyzer.identify_critical_modules(coverage_data)

    print(f"\n📊 Modules critiques identifiés: {len(critical_modules)}")
    for module, coverage, lines in critical_modules[:10]:  # Top 10
        print(".1f")

    # Générer le plan de test
    test_plan = analyzer.generate_test_plan(critical_modules)

    print("
📋 Plan d'amélioration:"    print(f"   • Modules à couvrir: {len(test_plan['modules'])}")
    print(f"   • Tests estimés: {test_plan['estimated_tests']}")
    print(f"   • Temps estimé: {test_plan['estimated_time']} minutes")
    print(f"   • Ordre de priorité: {', '.join(test_plan['priority_order'][:5])}")

    # Créer des fichiers de test pour les modules prioritaires
    print("
🔧 Création des fichiers de test..."    for module in test_plan["modules"][:3]:  # Top 3 modules
        analyzer.create_test_file(module)

    print("
✅ Analyse terminée!"    print("📄 Consultez RAPPORT_COUVERTURE_DETAILLE_2025.md pour le rapport complet")

if __name__ == "__main__":
    main()
