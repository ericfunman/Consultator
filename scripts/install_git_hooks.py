#!/usr/bin/env python3
"""
Installation et Configuration des Hooks Git pour Consultator
Configure automatiquement les hooks pre-commit pour les tests de régression.
"""

import os
import shutil
import stat
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent

def install_git_hooks():
    """Installe les hooks Git pour les tests automatiques"""
    
    print("🔧 Installation des Hooks Git - Consultator")
    print("=" * 50)
    
    # Vérifier que nous sommes dans un repo Git
    git_dir = WORKSPACE / ".git"
    if not git_dir.exists():
        print("❌ Erreur: Ce n'est pas un dépôt Git")
        print("   Initialisez Git d'abord: git init")
        return False
    
    # Créer le dossier hooks s'il n'existe pas
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    
    # Source et destination des hooks
    source_hooks_dir = WORKSPACE / ".githooks"
    
    if not source_hooks_dir.exists():
        print("❌ Erreur: Dossier .githooks manquant")
        return False
    
    # Installation des hooks
    hooks_installed = []
    
    # Hook pre-commit (Unix/Linux/Mac)
    pre_commit_source = source_hooks_dir / "pre-commit"
    pre_commit_dest = hooks_dir / "pre-commit"
    
    if pre_commit_source.exists():
        shutil.copy2(pre_commit_source, pre_commit_dest)
        
        # Rendre exécutable sur Unix
        if os.name != 'nt':  # Pas Windows
            st = os.stat(pre_commit_dest)
            os.chmod(pre_commit_dest, st.st_mode | stat.S_IEXEC)
        
        hooks_installed.append("pre-commit (Unix/Linux/Mac)")
        print("✅ Hook pre-commit installé")
    
    # Hook pre-commit PowerShell (Windows)
    pre_commit_ps_source = source_hooks_dir / "pre-commit.ps1"
    pre_commit_ps_dest = hooks_dir / "pre-commit.ps1"
    
    if pre_commit_ps_source.exists():
        shutil.copy2(pre_commit_ps_source, pre_commit_ps_dest)
        hooks_installed.append("pre-commit.ps1 (Windows)")
        print("✅ Hook pre-commit PowerShell installé")
    
    # Configuration Git pour utiliser le bon hook selon l'OS
    configure_git_hooks()
    
    # Créer un script d'activation pour Windows
    create_windows_activation_script()
    
    # Résumé
    print(f"\n📋 Résumé:")
    print(f"   Hooks installés: {len(hooks_installed)}")
    for hook in hooks_installed:
        print(f"   ├── {hook}")
    
    print(f"\n💡 Usage:")
    print(f"   Les tests de régression s'exécuteront automatiquement avant chaque commit")
    print(f"   Si les tests échouent, le commit sera bloqué")
    print(f"   Pas besoin d'action manuelle !")
    
    print(f"\n🔧 Commandes utiles:")
    print(f"   # Tester le hook manuellement")
    if os.name == 'nt':  # Windows
        print(f"   powershell .git\\hooks\\pre-commit.ps1")
    else:
        print(f"   .git/hooks/pre-commit")
    
    print(f"   # Désactiver temporairement")
    print(f"   git commit --no-verify")
    
    print(f"   # Maintenance quotidienne")
    print(f"   python scripts\\daily_maintenance.py")
    
    return True

def configure_git_hooks():
    """Configure Git pour utiliser nos hooks"""
    
    # Configuration pour utiliser notre dossier de hooks
    os.system("git config core.hooksPath .git/hooks")
    print("✅ Configuration Git mise à jour")

def create_windows_activation_script():
    """Crée un script d'activation spécial pour Windows"""
    
    if os.name != 'nt':  # Pas Windows
        return
    
    activation_script = WORKSPACE / "activate_git_hooks.bat"
    
    script_content = f"""@echo off
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
powershell -ExecutionPolicy Bypass -File .git\\hooks\\pre-commit.ps1

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
"""
    
    with open(activation_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script d'activation Windows créé: activate_git_hooks.bat")

def main():
    """Fonction principale"""
    
    try:
        success = install_git_hooks()
        
        if success:
            print(f"\n🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !")
            print(f"   Les hooks Git sont maintenant actifs")
            
            if os.name == 'nt':  # Windows
                print(f"   Exécutez 'activate_git_hooks.bat' si nécessaire")
        else:
            print(f"\n❌ INSTALLATION ÉCHOUÉE")
            print(f"   Vérifiez les erreurs ci-dessus")
            
    except Exception as e:
        print(f"\n❌ ERREUR INATTENDUE: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())