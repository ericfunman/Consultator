#!/bin/bash
# Script d'analyse de qualité de code pour Consultator

echo "🔍 Analyse de la qualité du code Consultator"
echo "================================================"

# Installation des outils si nécessaire
echo "📦 Installation des outils d'analyse..."
pip install -r requirements-dev.txt

echo ""
echo "🧹 1. Analyse avec Pylint..."
echo "--------------------------------"
pylint app/ --reports=y --output-format=text > reports/pylint-report.txt
echo "📄 Rapport Pylint généré dans reports/pylint-report.txt"

echo ""
echo "📏 2. Analyse Flake8 (PEP8)..."
echo "--------------------------------"
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics > reports/flake8-report.txt
echo "📄 Rapport Flake8 généré dans reports/flake8-report.txt"

echo ""
echo "🔒 3. Analyse de sécurité avec Bandit..."
echo "--------------------------------"
bandit -r app/ -f json -o reports/bandit-report.json
echo "📄 Rapport Bandit généré dans reports/bandit-report.json"

echo ""
echo "📊 4. Analyse de complexité avec Radon..."
echo "--------------------------------"
radon cc app/ --show-complexity --min=B > reports/radon-complexity.txt
radon mi app/ --show > reports/radon-maintainability.txt
echo "📄 Rapports Radon générés dans reports/"

echo ""
echo "🩺 5. Analyse des types avec MyPy..."
echo "--------------------------------"
mypy app/ --ignore-missing-imports > reports/mypy-report.txt 2>&1
echo "📄 Rapport MyPy généré dans reports/mypy-report.txt"

echo ""
echo "🔍 6. Détection de code mort avec Vulture..."
echo "--------------------------------"
vulture app/ > reports/vulture-report.txt
echo "📄 Rapport Vulture généré dans reports/vulture-report.txt"

echo ""
echo "✅ Analyse terminée ! Consultez le dossier reports/ pour les résultats détaillés."
