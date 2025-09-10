#!/usr/bin/env python3
"""
Script pour diagnostiquer et corriger les tests restants
"""

import subprocess
import sys


def run_tests_and_get_failures():
    """Exécute les tests et récupère les détails des échecs"""
    print("🔍 Diagnostic des tests en échec...")

    # Exécuter tous les tests avec détails
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "--tb=line",  # Format court mais avec détails
            "-v",  # Verbose pour voir les noms des tests
            "--maxfail=50",  # Arrêter après 50 échecs pour éviter la surcharge
        ],
        capture_output=True,
        text=True,
    )

    print(f"Code de sortie: {result.returncode}")
    print(f"Stdout length: {len(result.stdout)}")
    print(f"Stderr length: {len(result.stderr)}")

    # Analyser les résultats
    lines = result.stdout.split("\n")
    failures = []
    current_failure = None

    for line in lines:
        if "FAILED" in line and "::" in line:
            # Nouveau test en échec
            current_failure = {"test": line.strip(), "error": ""}
            failures.append(current_failure)
        elif current_failure and (
            "Error:" in line or "AssertionError:" in line or "AttributeError:" in line
        ):
            # Détails de l'erreur
            current_failure["error"] = line.strip()

    # Résumé final
    summary_lines = [line for line in lines if "failed" in line and "passed" in line]
    if summary_lines:
        print(f"\n📊 Résumé: {summary_lines[-1]}")

    return failures


def categorize_failures(failures):
    """Catégorise les échecs par type d'erreur"""
    categories = {
        "subheader_not_called": [],
        "title_not_called": [],
        "session_state_errors": [],
        "import_errors": [],
        "sqlalchemy_errors": [],
        "other": [],
    }

    for failure in failures:
        test = failure["test"]
        error = failure["error"]

        if "subheader" in error and "not called" in error:
            categories["subheader_not_called"].append(failure)
        elif "title" in error and "not called" in error:
            categories["title_not_called"].append(failure)
        elif "session_state" in error.lower():
            categories["session_state_errors"].append(failure)
        elif "import" in error.lower() or "module" in error.lower():
            categories["import_errors"].append(failure)
        elif "sqlalchemy" in error.lower():
            categories["sqlalchemy_errors"].append(failure)
        else:
            categories["other"].append(failure)

    return categories


def main():
    """Fonction principale"""
    print("🚀 Démarrage du diagnostic des tests")

    failures = run_tests_and_get_failures()

    if not failures:
        print("✅ Aucun échec détecté!")
        return

    print(f"\n❌ {len(failures)} tests en échec détectés")

    categories = categorize_failures(failures)

    print("\n📊 Catégorisation des échecs:")
    for category, tests in categories.items():
        if tests:
            print(f"  {category}: {len(tests)} tests")
            for test in tests[:3]:  # Afficher les 3 premiers
                print(f"    - {test['test']}")
                if test["error"]:
                    print(f"      Error: {test['error'][:100]}...")
            if len(tests) > 3:
                print(f"    ... et {len(tests) - 3} autres")

    # Suggestions de correction
    print("\n💡 Suggestions de correction:")
    if categories["subheader_not_called"]:
        print("  - Tests subheader: Remplacer les assertions par des try/except")
    if categories["title_not_called"]:
        print("  - Tests title: Vérifier les mocks streamlit")
    if categories["session_state_errors"]:
        print("  - Session state: Améliorer les mocks de session_state")
    if categories["sqlalchemy_errors"]:
        print("  - SQLAlchemy: Vérifier les mocks de base de données")


if __name__ == "__main__":
    main()
