#!/bin/bash
# Script d'installation des hooks pre-commit pour Consultator
# Ce script installe et configure automatiquement les hooks de pre-commit

echo "========================================"
echo "🔧 Installation des Hooks Pre-commit"
echo "========================================"
echo

# Vérifier si Python est installé
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python n'est pas installé ou n'est pas dans le PATH"
    echo "Veuillez installer Python 3.8+ et l'ajouter au PATH"
    exit 1
fi

# Utiliser python3 si disponible, sinon python
PYTHON_CMD="python"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

# Vérifier si pip est installé
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip n'est pas installé"
    echo "Veuillez installer pip"
    exit 1
fi

# Utiliser pip3 si disponible, sinon pip
PIP_CMD="pip"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
fi

echo "📦 Installation de pre-commit..."
$PIP_CMD install pre-commit

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation de pre-commit"
    exit 1
fi

echo "✅ Pre-commit installé avec succès"
echo

echo "🔧 Installation des hooks..."
pre-commit install

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation des hooks"
    exit 1
fi

echo "✅ Hooks installés avec succès"
echo

echo "🧪 Test des hooks sur tous les fichiers..."
pre-commit run --all-files

if [ $? -ne 0 ]; then
    echo "⚠️  Certains hooks ont échoué lors du test"
    echo "Vous pouvez corriger les erreurs ou ajuster la configuration"
    echo
else
    echo "✅ Tous les hooks passent avec succès !"
    echo
fi

echo "========================================"
echo "📋 Instructions d'utilisation :"
echo "========================================"
echo
echo "• Les hooks s'exécutent automatiquement avant chaque commit"
echo "• Pour exécuter manuellement : pre-commit run --all-files"
echo "• Pour un fichier spécifique : pre-commit run --files fichier.py"
echo "• Pour désactiver temporairement : git commit --no-verify"
echo
echo "• Hooks configurés :"
echo "  ✓ Suppression espaces fin de ligne"
echo "  ✓ Formatage automatique (Black)"
echo "  ✓ Tri des imports (isort)"
echo "  ✓ Analyse flake8"
echo "  ✓ Analyse pylint"
echo "  ✓ Vérification types (mypy)"
echo "  ✓ Analyse sécurité (bandit)"
echo "  ✓ Vérification documentation"
echo
echo "• Fichiers exclus : venv, cache, backups, tests"
echo
