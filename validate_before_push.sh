#!/bin/bash
# Script de validation avant push - Consultator
# Lance toutes les vérifications du CI/CD en local

set -e  # Arrêter en cas d'erreur

echo "🔍 =================================="
echo "   VALIDATION PRE-PUSH CONSULTATOR"
echo "=================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de succès
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Fonction d'erreur
error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Fonction d'avertissement
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "📋 Étape 1/5: Vérification Black (formatage code)"
echo "---------------------------------------------------"
if python -m black --check --diff --line-length 120 app/ tests/; then
    success "Black: Code correctement formaté"
else
    error "Black: Code mal formaté. Lancez: python -m black app/ tests/ --line-length 120"
fi
echo ""

echo "📋 Étape 2/5: Vérification isort (ordre imports)"
echo "---------------------------------------------------"
if python -m isort --check-only --diff app/ tests/; then
    success "isort: Imports correctement ordonnés"
else
    warning "isort: Imports mal ordonnés (non-bloquant en CI/CD)"
    echo "Pour corriger: python -m isort app/ tests/"
fi
echo ""

echo "📋 Étape 3/5: Vérification Flake8 (linting)"
echo "---------------------------------------------------"
if python -m flake8 app/ --max-line-length=150 --extend-ignore=E203,W503,F401,F841,W291,W293,E501,C901,E722,F541 --max-complexity=20; then
    success "Flake8: Pas d'erreurs de linting"
else
    warning "Flake8: Avertissements détectés (non-bloquants)"
fi
echo ""

echo "📋 Étape 4/5: Tests de régression"
echo "---------------------------------------------------"
if python -m pytest tests/regression/ -v --tb=short; then
    success "Tests de régression: OK"
else
    error "Tests de régression: ÉCHEC"
fi
echo ""

echo "📋 Étape 5/5: Vérification base de données"
echo "---------------------------------------------------"
if python -c "from app.database.database import init_database; init_database(); print('✅ DB OK')"; then
    success "Base de données: Initialisable"
else
    error "Base de données: Erreur d'initialisation"
fi
echo ""

echo "=================================="
echo -e "${GREEN}✅ TOUTES LES VALIDATIONS PASSÉES !${NC}"
echo "=================================="
echo ""
echo "🚀 Vous pouvez pousser en toute sécurité:"
echo "   git push origin master"
echo ""
