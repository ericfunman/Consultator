@echo off
echo 🔧 Configuration des hooks Git...
python scripts/test_hooks.py --setup
echo.
echo ✅ Hooks configurés avec succès
pause