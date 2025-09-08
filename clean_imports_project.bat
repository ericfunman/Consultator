@echo off
REM Script de nettoyage des imports du projet - Windows
REM Utilise le script Python spécialisé pour le projet uniquement

echo ========================================
echo 🧹 Nettoyeur d'Imports - Version Projet
echo ========================================
echo.

if "%1"=="--help" goto :help
if "%1"=="-h" goto :help
if "%1"=="help" goto :help

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ et l'ajouter au PATH
    pause
    exit /b 1
)

REM Mode simulation par défaut
if "%1"=="--apply" (
    echo ⚠️  MODE PRODUCTION - Les changements seront appliqués !
    echo.
    python clean_imports_project.py --apply --verbose
) else if "%1"=="--no-backup" (
    echo ⚠️  MODE SANS SAUVEGARDE
    echo.
    python clean_imports_project.py --no-backup --verbose
) else if "%1"=="--apply-no-backup" (
    echo ⚠️  MODE PRODUCTION SANS SAUVEGARDE - ATTENTION !
    echo.
    python clean_imports_project.py --apply --no-backup --verbose
) else (
    echo 🔍 MODE SIMULATION (aucun changement réel)
    echo Utilisez --apply pour appliquer les changements
    echo.
    python clean_imports_project.py --verbose
)

echo.
echo ========================================
echo Terminé !
echo ========================================
pause
exit /b 0

:help
echo.
echo 📖 AIDE - Nettoyeur d'Imports Projet
echo ========================================
echo.
echo USAGE:
echo   clean_imports_project.bat              # Mode simulation
echo   clean_imports_project.bat --apply      # Appliquer les changements
echo   clean_imports_project.bat --no-backup  # Simulation sans sauvegarde
echo   clean_imports_project.bat --apply-no-backup  # Production sans sauvegarde
echo.
echo DESCRIPTION:
echo   Nettoie automatiquement les imports inutilisés dans les fichiers
echo   du projet uniquement (exclut les dépendances externes).
echo.
echo OPTIONS:
echo   --apply              Applique réellement les changements
echo   --no-backup          Désactive la création de sauvegardes
echo   --apply-no-backup    Applique sans sauvegarde (DANGER !)
echo.
echo EXEMPLES:
echo   clean_imports_project.bat                    # Test sécurisé
echo   clean_imports_project.bat --apply           # Nettoyage réel
echo.
echo NOTES:
echo   - Les sauvegardes sont créées dans backups/imports_cleaning_project/
echo   - Utilisez git commit avant d'appliquer les changements
echo   - Vérifiez les tests après le nettoyage
echo.
pause
exit /b 0
