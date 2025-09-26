@echo off
REM Script de maintenance quotidienne des tests - Consultator
REM Utilisation: maintenance.bat

echo ========================================
echo   CONSULTATOR - MAINTENANCE DES TESTS
echo ========================================
echo.

REM Vérification que nous sommes dans le bon répertoire
if not exist "run.py" (
    echo ❌ Erreur: Ce script doit être exécuté depuis le répertoire racine de Consultator
    echo    Répertoire actuel: %CD%
    echo    Cherche le fichier: run.py
    pause
    exit /b 1
)

echo 🔧 Démarrage de la maintenance quotidienne...
echo.

REM Exécution de la maintenance
python scripts\daily_maintenance.py

REM Vérification du code de retour
if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ Maintenance terminée avec succès !
    echo.
    echo 📋 Rapports disponibles dans le dossier reports\
    echo 🧪 Tests fonctionnels: tests\unit\ et tests\regression\
    echo 🛠️  Scripts d'aide: scripts\
    echo.
) else (
    echo.
    echo ❌ La maintenance a rencontré des problèmes.
    echo    Code d'erreur: %ERRORLEVEL%
    echo.
    echo 💡 Actions recommandées:
    echo    1. Vérifiez que Python est installé et accessible
    echo    2. Installez les dépendances: pip install -r requirements.txt
    echo    3. Exécutez manuellement: python scripts\daily_maintenance.py
    echo.
)

echo Appuyez sur une touche pour continuer...
pause > nul