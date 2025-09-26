@echo off
echo 🚀 Amélioration de la couverture de tests...
python scripts/improve_coverage.py
python scripts/auto_test_generator.py
echo.
echo ✅ Processus terminé. Consultez les fichiers générés.
pause