@echo off
REM Script de nettoyage automatique des imports Python
REM Utilise le script Python clean_imports.py

echo ========================================
echo 🧹 NETTOYEUR D'IMPORTS PYTHON
echo ========================================
echo.

set "PROJECT_ROOT=%~dp0"
set "SCRIPT_PATH=%PROJECT_ROOT%clean_imports.py"

REM Vérifier si Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.6+ et réessayer
    pause
    exit /b 1
)

REM Vérifier si le script existe
if not exist "%SCRIPT_PATH%" (
    echo ❌ Le script clean_imports.py n'existe pas
    echo Chemin: %SCRIPT_PATH%
    pause
    exit /b 1
)

echo 📁 Projet: %PROJECT_ROOT%
echo 🐍 Script: %SCRIPT_PATH%
echo.

:menu
echo Choisissez une option:
echo [1] Analyse seulement (recommandé)
echo [2] Nettoyage automatique (avec sauvegardes)
echo [3] Nettoyage sans sauvegardes (risqué)
echo [4] Quitter
echo.
set /p choice="Votre choix (1-4): "

if "%choice%"=="1" goto analyze
if "%choice%"=="2" goto clean_backup
if "%choice%"=="3" goto clean_no_backup
if "%choice%"=="4" goto exit
goto menu

:analyze
echo.
echo 🔍 MODE ANALYSE (simulation)
echo ================================
python "%SCRIPT_PATH%" --dry-run --verbose
goto end

:clean_backup
echo.
echo 🧹 NETTOYAGE AVEC SAUVEGARDES
echo ================================
echo ⚠️  ATTENTION: Les modifications seront appliquées !
echo 💾 Des sauvegardes seront créées automatiquement
echo.
set /p confirm="Confirmer ? (o/N): "
if /i "%confirm%"=="o" (
    python "%SCRIPT_PATH%" --dry-run=false --verbose
) else (
    echo Opération annulée
)
goto end

:clean_no_backup
echo.
echo 🧹 NETTOYAGE SANS SAUVEGARDES ⚠️
echo ================================
echo ❌ ATTENTION: AUCUNE SAUVEGARDE ne sera créée !
echo 💀 Cette action est IRRÉVERSIBLE !
echo.
set /p confirm="Êtes-vous SÛR ? Tapez 'OUI' pour confirmer: "
if "%confirm%"=="OUI" (
    python "%SCRIPT_PATH%" --dry-run=false --no-backup --verbose
) else (
    echo Opération annulée
)
goto end

:exit
echo.
echo Au revoir !
goto end

:end
echo.
echo ========================================
echo 📊 Opération terminée
echo ========================================
pause
