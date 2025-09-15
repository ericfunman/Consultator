#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuration du pipeline CI/CD pour Consultator
Installe et configure pre-commit, les dépendances de développement
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        print(f"✅ {description} - Terminé")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description}: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False


def install_dev_dependencies():
    """Installe les dépendances de développement"""
    print("📦 Installation des dépendances de développement...")

    dev_packages = [
        "pre-commit",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "pylint",
        "black",
        "flake8",
        "isort",
        "bandit",
        "radon",
        "mypy"
    ]

    for package in dev_packages:
        if not run_command(f"pip install {package}", f"Installation de {package}"):
            return False

    return True


def setup_pre_commit():
    """Configure pre-commit"""
    print("🔗 Configuration de pre-commit...")

    # Installer pre-commit
    if not run_command("pre-commit install", "Installation des hooks pre-commit"):
        return False

    # Installer les hooks dans le repo
    if not run_command("pre-commit install --install-hooks", "Installation des hooks dans le repo"):
        return False

    return True


def run_initial_checks():
    """Exécute les vérifications initiales"""
    print("🔍 Exécution des vérifications initiales...")

    checks = [
        ("black --check app/", "Vérification du formatage Black"),
        ("isort --check-only app/", "Vérification du tri des imports"),
        ("flake8 app/", "Vérification Flake8"),
        ("python -m pytest tests/ --tb=short -q", "Exécution des tests"),
    ]

    all_passed = True
    for command, description in checks:
        if not run_command(command, description):
            all_passed = False

    return all_passed


def create_gitignore_entries():
    """Ajoute les entrées nécessaires au .gitignore"""
    gitignore_path = Path(".gitignore")

    entries_to_add = [
        "",
        "# CI/CD et couverture",
        "coverage.xml",
        "htmlcov/",
        ".coverage",
        ".coverage.*",
        "coverage-*.xml",
        "",
        "# Rapports de qualité",
        "bandit-report.json",
        "complexity_report.txt",
        "pylint-report.json",
        "",
        "# Environnements virtuels",
        ".venv/",
        "venv/",
        "ENV/",
        "env/",
    ]

    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = ""

    for entry in entries_to_add:
        if entry and entry not in content:
            content += entry + "\n"

    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ .gitignore mis à jour")
    return True


def main():
    """Fonction principale"""
    print("🚀 Configuration du pipeline CI/CD pour Consultator")
    print("=" * 60)

    # Vérifier que nous sommes dans le bon répertoire
    if not Path("app").exists() or not Path("requirements.txt").exists():
        print("❌ Ce script doit être exécuté depuis la racine du projet Consultator")
        sys.exit(1)

    steps = [
        ("Installation des dépendances de développement", install_dev_dependencies),
        ("Configuration de pre-commit", setup_pre_commit),
        ("Mise à jour du .gitignore", create_gitignore_entries),
        ("Vérifications initiales", run_initial_checks),
    ]

    success_count = 0

    for description, func in steps:
        print(f"\n📋 Étape: {description}")
        if func():
            success_count += 1
        else:
            print(f"⚠️  Échec de l'étape: {description}")

    print("\n" + "=" * 60)
    print(f"📊 Résumé: {success_count}/{len(steps)} étapes réussies")

    if success_count == len(steps):
        print("🎉 Configuration CI/CD terminée avec succès !")
        print("\n📝 Prochaines étapes :")
        print("1. Commitez les changements : git add . && git commit -m 'feat: setup CI/CD pipeline'")
        print("2. Poussez vers GitHub : git push origin master")
        print("3. Vérifiez le statut du workflow dans l'onglet Actions de GitHub")
        print("\n🔧 Commandes utiles :")
        print("- pre-commit run --all-files  # Exécuter tous les hooks")
        print("- pre-commit run black        # Exécuter seulement Black")
        print("- python -m pytest tests/      # Exécuter les tests")
    else:
        print("⚠️  Certaines étapes ont échoué. Vérifiez les messages d'erreur ci-dessus.")
        sys.exit(1)


if __name__ == "__main__":
    main()
