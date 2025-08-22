#!/bin/bash
# Script de nettoyage automatique du code Consultator

echo "🧹 Démarrage du nettoyage automatique du code..."
echo "================================================"

# 1. Installer les outils de formatage
echo "📦 Installation des outils de formatage..."
pip install black isort autoflake

# 2. Supprimer les imports inutilisés
echo "🗑️ Suppression des imports inutilisés..."
autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive app/

# 3. Tri et formatage des imports
echo "📋 Tri des imports..."
isort app/ --profile black

# 4. Formatage automatique du code
echo "🎨 Formatage automatique avec Black..."
black app/ --line-length 79

# 5. Verification finale
echo "✅ Vérification finale..."
flake8 app/ --select=E9,F63,F7,F82 --show-source --statistics

echo ""
echo "✨ Nettoyage terminé !"
echo "📊 Exécutez 'pylint app/' pour voir l'amélioration du score."
