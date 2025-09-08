"""
Surveillance continue de la qualité du code
Exécution automatique après chaque modification de fichier
"""

import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class CodeQualityWatcher(FileSystemEventHandler):
    """Surveillance des modifications de fichiers pour déclencher les tests"""

    def __init__(self):
        self.last_run = 0
        self.debounce_time = 5  # 5 secondes entre les exécutions
        self.project_root = Path.cwd()

    def on_modified(self, event):
        """Déclenché quand un fichier est modifié"""
        if event.is_directory:
            return

        # Filtrer les types de fichiers
        if not self._should_trigger(event.src_path):
            return

        current_time = time.time()
        if current_time - self.last_run < self.debounce_time:
            return

        self.last_run = current_time

        print(f"\n🔍 Modification détectée : {event.src_path}")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")

        self._run_quality_checks(event.src_path)

    def _should_trigger(self, file_path):
        """Détermine si une modification doit déclencher les tests"""
        file_path = Path(file_path)

        # Extensions à surveiller
        python_extensions = {".py"}
        config_extensions = {".yml", ".yaml", ".json", ".cfg", ".ini"}

        if file_path.suffix in python_extensions:
            return True

        if file_path.suffix in config_extensions:
            return True

        # Ignorer certains répertoires/fichiers
        ignore_patterns = {
            "__pycache__",
            ".pytest_cache",
            "reports",
            ".git",
            "backup",
            ".coverage",
        }

        for pattern in ignore_patterns:
            if pattern in str(file_path):
                return False

        return False

    def _run_quality_checks(self, modified_file):
        """Exécute les vérifications de qualité appropriées"""
        file_path = Path(modified_file)

        print("🏃‍♂️ Exécution des vérifications...")

        if file_path.suffix == ".py":
            # Tests spécifiques au fichier Python modifié
            self._run_python_checks(file_path)
        else:
            # Tests généraux
            self._run_general_checks()

    def _run_python_checks(self, file_path):
        """Tests spécifiques pour les fichiers Python"""
        print(f"🐍 Vérification Python : {file_path.name}")

        # 1. Syntax check
        if self._check_syntax(file_path):
            print("✅ Syntaxe valide")
        else:
            print("❌ Erreur de syntaxe")
            return

        # 2. Pylint sur le fichier spécifique
        self._run_pylint_file(file_path)

        # 3. Tests associés
        self._run_related_tests(file_path)

    def _check_syntax(self, file_path):
        """Vérification de la syntaxe Python"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                compile(f.read(), file_path, "exec")
            return True
        except SyntaxError as e:
            print(f"❌ Erreur syntaxe ligne {e.lineno}: {e.msg}")
            return False
        except Exception as e:
            print(f"❌ Erreur lecture fichier: {e}")
            return False

    def _run_pylint_file(self, file_path):
        """Pylint sur un fichier spécifique"""
        try:
            result = subprocess.run(
                ["pylint", str(file_path), "--score=yes", "--reports=no"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if "Your code has been rated at" in result.stdout:
                score_line = [
                    line
                    for line in result.stdout.split("\n")
                    if "Your code has been rated at" in line
                ][0]
                score = score_line.split("rated at ")[1].split("/10")[0]
                print(f"📊 Pylint : {score}/10")

                if float(score) >= 8.0:
                    print("✅ Score Pylint acceptable")
                else:
                    print("⚠️ Score Pylint à améliorer")
            else:
                print("❌ Erreur Pylint")

        except subprocess.TimeoutExpired:
            print("⏰ Timeout Pylint")
        except Exception as e:
            print(f"❌ Erreur Pylint : {e}")

    def _run_related_tests(self, file_path):
        """Exécute les tests liés au fichier modifié"""
        # Rechercher les tests correspondants
        test_patterns = [
            f"test_{file_path.stem}.py",
            f"test_{file_path.stem}_*.py",
            f"*_test_{file_path.stem}.py",
        ]

        test_files = []
        tests_dir = self.project_root / "tests"

        if tests_dir.exists():
            for pattern in test_patterns:
                test_files.extend(tests_dir.glob(pattern))

        if test_files:
            print(f"🧪 Tests trouvés : {[f.name for f in test_files]}")

            for test_file in test_files:
                self._run_specific_test(test_file)
        else:
            print("🔍 Aucun test spécifique trouvé")

    def _run_specific_test(self, test_file):
        """Exécute un fichier de test spécifique"""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", str(test_file), "-v"],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                print(f"✅ Tests {test_file.name} : OK")
            else:
                print(f"❌ Tests {test_file.name} : ÉCHEC")
                # Afficher les premières lignes d'erreur
                error_lines = result.stdout.split("\n")[-10:]
                for line in error_lines:
                    if line.strip() and not line.startswith("="):
                        print(f"   {line}")

        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout test {test_file.name}")
        except Exception as e:
            print(f"❌ Erreur test {test_file.name}: {e}")

    def _run_general_checks(self):
        """Tests généraux (fichiers de config, etc.)"""
        print("🔧 Vérifications générales...")

        # Test de démarrage rapide
        try:
            result = subprocess.run(
                ["python", "-c", "import app.main; print('Import OK')"],
                capture_output=True,
                text=True,
                timeout=15,
            )

            if result.returncode == 0:
                print("✅ Import application : OK")
            else:
                print("❌ Erreur import application")

        except subprocess.TimeoutExpired:
            print("⏰ Timeout import application")
        except Exception as e:
            print(f"❌ Erreur import : {e}")


class ContinuousQualityMonitor:
    """Moniteur de qualité continue"""

    def __init__(self):
        self.observer = Observer()
        self.handler = CodeQualityWatcher()
        self.project_root = Path.cwd()

    def start_monitoring(self):
        """Démarre la surveillance"""
        print("🎯 SURVEILLANCE CONTINUE DE LA QUALITÉ")
        print("=" * 50)
        print(f"📁 Répertoire surveillé : {self.project_root}")
        print("🔍 Types de fichiers : .py, .yml, .json, .cfg")
        print("⚡ Délai de debounce : 5 secondes")
        print("🛑 Arrêt avec Ctrl+C")
        print("=" * 50)

        # Surveiller le répertoire app/
        app_path = self.project_root / "app"
        if app_path.exists():
            self.observer.schedule(self.handler, str(app_path), recursive=True)
            print(f"👀 Surveillance : {app_path}")

        # Surveiller le répertoire tests/
        tests_path = self.project_root / "tests"
        if tests_path.exists():
            self.observer.schedule(self.handler, str(tests_path), recursive=True)
            print(f"👀 Surveillance : {tests_path}")

        # Surveiller les fichiers de config
        config_files = ["setup.cfg", "pyproject.toml", "requirements.txt"]
        for config_file in config_files:
            if (self.project_root / config_file).exists():
                self.observer.schedule(
                    self.handler, str(self.project_root), recursive=False
                )
                break

        self.observer.start()
        print("\n✅ Surveillance démarrée !")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt de la surveillance...")
            self.observer.stop()

        self.observer.join()
        print("👋 Surveillance terminée")

    def run_initial_check(self):
        """Exécute une vérification initiale"""
        print("🏁 Vérification initiale...")

        try:
            result = subprocess.run(
                ["python", "run_quality_pipeline.py", "--quick"], timeout=120
            )

            if result.returncode == 0:
                print("✅ Vérification initiale : OK")
            else:
                print("⚠️ Vérification initiale : Améliorations nécessaires")

        except subprocess.TimeoutExpired:
            print("⏰ Timeout vérification initiale")
        except Exception as e:
            print(f"❌ Erreur vérification initiale : {e}")


def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Surveillance continue de la qualité")
    parser.add_argument(
        "--no-initial", action="store_true", help="Ignorer la vérification initiale"
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Installer les dépendances de surveillance",
    )

    args = parser.parse_args()

    # Installation des dépendances si demandé
    if args.install_deps:
        print("📦 Installation des dépendances de surveillance...")
        subprocess.run([sys.executable, "-m", "pip", "install", "watchdog"])

    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        print("❌ Module 'watchdog' manquant")
        print("📦 Installation : pip install watchdog")
        print("🔄 Ou utilisez : python watch_quality.py --install-deps")
        return 1

    monitor = ContinuousQualityMonitor()

    # Vérification initiale
    if not args.no_initial:
        monitor.run_initial_check()
        print()

    # Démarrage de la surveillance
    monitor.start_monitoring()

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
