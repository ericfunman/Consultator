@echo off
REM Script d'installation des hooks pre-commit pour Consultator
REM Ce script installe et configure automatiquement les hooks de pre-commit

echo ========================================
echo 🔧 Installation des Hooks Pre-commit
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ et l'ajouter au PATH
    pause
    exit /b 1
)

REM Vérifier si pip est installé
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip n'est pas installé
    echo Veuillez installer pip
    pause
    exit /b 1
)

echo 📦 Installation de pre-commit...
pip install pre-commit

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation de pre-commit
    pause
    exit /b 1
)

echo ✅ Pre-commit installé avec succès
echo.

echo 🔧 Installation des hooks...
pre-commit install

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des hooks
    pause
    exit /b 1
)

echo ✅ Hooks installés avec succès
echo.

echo 🧪 Test des hooks sur tous les fichiers...
pre-commit run --all-files

if errorlevel 1 (
    echo ⚠️  Certains hooks ont échoué lors du test
    echo Vous pouvez corriger les erreurs ou ajuster la configuration
    echo.
) else (
    echo ✅ Tous les hooks passent avec succès !
    echo.
)

echo ========================================
echo 📋 Instructions d'utilisation :
echo ========================================
echo.
echo • Les hooks s'exécutent automatiquement avant chaque commit
echo • Pour exécuter manuellement : pre-commit run --all-files
echo • Pour un fichier spécifique : pre-commit run --files fichier.py
echo • Pour désactiver temporairement : git commit --no-verify
echo.
echo • Hooks configurés :
echo   ✓ Suppression espaces fin de ligne
echo   ✓ Formatage automatique (Black)
echo   ✓ Tri des imports (isort)
echo   ✓ Analyse flake8
echo   ✓ Analyse pylint
echo   ✓ Vérification types (mypy)
echo   ✓ Analyse sécurité (bandit)
echo   ✓ Vérification documentation
echo.
echo • Fichiers exclus : venv, cache, backups, tests
echo.

pause
