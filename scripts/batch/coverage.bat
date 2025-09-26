@echo off
echo 📊 Analyse de couverture...
python -m pytest --cov=app --cov-report=html:reports/htmlcov --cov-report=term-missing tests/
echo.
echo 📈 Rapport HTML généré dans reports/htmlcov/index.html
pause