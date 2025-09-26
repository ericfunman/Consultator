@echo off
echo 🧪 Exécution des tests...
python -m pytest tests/ -v --tb=short
pause