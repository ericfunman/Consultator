@echo off
REM Script d'activation des hooks Git pour Windows - Consultator

echo ========================================
echo   ACTIVATION DES HOOKS GIT - CONSULTATOR  
echo ========================================
echo.

REM Configuration Git pour utiliser PowerShell pour les hooks
git config core.hooksPath .git/hooks
git config --global core.autocrlf true

REM Test du hook pre-commit
echo 🧪 Test du hook pre-commit...
powershell -ExecutionPolicy Bypass -File .git\hooks\pre-commit.ps1

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ Hooks Git activés avec succès !
    echo.
    echo 💡 À partir de maintenant:
    echo    - Les tests de régression s'exécuteront avant chaque commit
    echo    - Si les tests échouent, le commit sera bloqué
    echo    - Utilisez 'git commit --no-verify' pour ignorer temporairement
    echo.
) else (
    echo.
    echo ❌ Problème avec les hooks Git
    echo    Vérifiez que Python est installé et accessible
    echo.
)

pause
