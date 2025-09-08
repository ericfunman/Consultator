"""
Configuration pour l'intégration continue avec SonarQube
Gestion automatique des analyses de qualité de code
"""

import json
import subprocess
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests


class SonarIntegration:
    """Gestionnaire d'intégration SonarQube pour l'analyse continue"""

    def __init__(
        self, sonar_url="http://localhost:9000", project_key="consultator-app"
    ):
        self.sonar_url = sonar_url
        self.project_key = project_key
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

    def run_quality_analysis(self):
        """Exécute l'analyse complète de qualité de code"""
        print("🔍 Démarrage de l'analyse de qualité complète...")

        # 1. Pylint
        self._run_pylint()

        # 2. Flake8
        self._run_flake8()

        # 3. Bandit (sécurité)
        self._run_bandit()

        # 4. Tests avec coverage
        self._run_tests_with_coverage()

        # 5. SonarQube Scanner
        self._run_sonar_scanner()

        print("✅ Analyse de qualité terminée !")

    def _run_pylint(self):
        """Exécute Pylint et génère le rapport"""
        print("📊 Exécution de Pylint...")
        try:
            result = subprocess.run(
                ["pylint", "app/", "--output-format=parseable", "--score=yes"],
                capture_output=True,
                text=True,
            )

            with open(
                self.reports_dir / "pylint-report.txt", "w", encoding="utf-8"
            ) as f:
                f.write(result.stdout)
                f.write(result.stderr)

            print(f"✅ Rapport Pylint généré : {self.reports_dir}/pylint-report.txt")

        except Exception as e:
            print(f"❌ Erreur Pylint : {e}")

    def _run_flake8(self):
        """Exécute Flake8 et génère le rapport"""
        print("📊 Exécution de Flake8...")
        try:
            result = subprocess.run(
                [
                    "flake8",
                    "app/",
                    "--format=default",
                    "--output-file",
                    str(self.reports_dir / "flake8-report.txt"),
                ],
                capture_output=True,
                text=True,
            )

            print(f"✅ Rapport Flake8 généré : {self.reports_dir}/flake8-report.txt")

        except Exception as e:
            print(f"❌ Erreur Flake8 : {e}")

    def _run_bandit(self):
        """Exécute Bandit (analyse de sécurité)"""
        print("🔒 Exécution de Bandit...")
        try:
            result = subprocess.run(
                [
                    "bandit",
                    "-r",
                    "app/",
                    "-f",
                    "json",
                    "-o",
                    str(self.reports_dir / "bandit-report.json"),
                ],
                capture_output=True,
                text=True,
            )

            print(f"✅ Rapport Bandit généré : {self.reports_dir}/bandit-report.json")

        except Exception as e:
            print(f"❌ Erreur Bandit : {e}")

    def _run_tests_with_coverage(self):
        """Exécute les tests avec coverage"""
        print("🧪 Exécution des tests avec coverage...")
        try:
            # Coverage run
            subprocess.run(
                ["coverage", "run", "--source=app", "-m", "pytest", "tests/", "-v"],
                check=True,
            )

            # Coverage XML pour SonarQube
            subprocess.run(
                ["coverage", "xml", "-o", str(self.reports_dir / "coverage.xml")],
                check=True,
            )

            # Coverage HTML pour visualisation
            subprocess.run(
                ["coverage", "html", "-d", str(self.reports_dir / "htmlcov")],
                check=True,
            )

            print(f"✅ Rapports de coverage générés")

        except Exception as e:
            print(f"❌ Erreur coverage : {e}")

    def _run_sonar_scanner(self):
        """Exécute SonarQube Scanner"""
        print("🔍 Exécution de SonarQube Scanner...")
        try:
            result = subprocess.run(
                [
                    "sonar-scanner",
                    f"-Dsonar.projectKey={self.project_key}",
                    f"-Dsonar.host.url={self.sonar_url}",
                    "-Dsonar.projectBaseDir=.",
                    "-Dsonar.python.coverage.reportPaths=reports/coverage.xml",
                    "-Dsonar.python.pylint.reportPath=reports/pylint-report.txt",
                    "-Dsonar.python.flake8.reportPath=reports/flake8-report.txt",
                    "-Dsonar.python.bandit.reportPath=reports/bandit-report.json",
                ],
                capture_output=True,
                text=True,
            )

            print("✅ Analyse SonarQube terminée")
            return result.returncode == 0

        except Exception as e:
            print(f"❌ Erreur SonarQube Scanner : {e}")
            return False

    def get_quality_gate_status(self):
        """Récupère le statut de la Quality Gate"""
        try:
            response = requests.get(
                f"{self.sonar_url}/api/qualitygates/project_status",
                params={"projectKey": self.project_key},
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("projectStatus", {}).get("status")
            else:
                print(f"❌ Erreur récupération Quality Gate : {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Erreur API SonarQube : {e}")
            return None

    def wait_for_analysis_completion(self, timeout=300):
        """Attend la fin de l'analyse SonarQube"""
        print("⏳ Attente de la fin de l'analyse...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_quality_gate_status()

            if status == "OK":
                print("✅ Quality Gate : PASSED")
                return True
            elif status == "ERROR":
                print("❌ Quality Gate : FAILED")
                return False
            elif status is None:
                print("🔄 Analyse en cours...")
                time.sleep(10)
            else:
                print(f"🔄 Statut : {status}")
                time.sleep(10)

        print("⏰ Timeout atteint")
        return False

    def generate_quality_report(self):
        """Génère un rapport de qualité consolidé"""
        print("📋 Génération du rapport de qualité...")

        report = {
            "timestamp": datetime.now().isoformat(),
            "project": self.project_key,
            "reports": [],
        }

        # Pylint score
        pylint_file = self.reports_dir / "pylint-report.txt"
        if pylint_file.exists():
            with open(pylint_file, "r", encoding="utf-8") as f:
                content = f.read()
                if "Your code has been rated at" in content:
                    score_line = [
                        line
                        for line in content.split("\n")
                        if "Your code has been rated at" in line
                    ]
                    if score_line:
                        score = score_line[0].split("rated at ")[1].split("/10")[0]
                        report["reports"].append(
                            {
                                "tool": "Pylint",
                                "score": float(score),
                                "status": (
                                    "PASSED" if float(score) >= 8.0 else "WARNING"
                                ),
                            }
                        )

        # Coverage
        coverage_file = self.reports_dir / "coverage.xml"
        if coverage_file.exists():
            try:
                tree = ET.parse(coverage_file)
                root = tree.getroot()
                coverage_pct = float(root.attrib.get("line-rate", 0)) * 100
                report["reports"].append(
                    {
                        "tool": "Coverage",
                        "percentage": coverage_pct,
                        "status": "PASSED" if coverage_pct >= 80 else "WARNING",
                    }
                )
            except Exception as e:
                print(f"❌ Erreur lecture coverage : {e}")

        # Quality Gate
        quality_gate = self.get_quality_gate_status()
        if quality_gate:
            report["quality_gate"] = quality_gate

        # Sauvegarde du rapport
        report_file = (
            self.reports_dir
            / f"quality-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"✅ Rapport qualité sauvegardé : {report_file}")
        return report


def main():
    """Point d'entrée principal"""
    sonar = SonarIntegration()

    # Analyse complète
    sonar.run_quality_analysis()

    # Attente et vérification
    success = sonar.wait_for_analysis_completion()

    # Génération du rapport final
    report = sonar.generate_quality_report()

    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE L'ANALYSE DE QUALITÉ")
    print("=" * 50)

    for item in report.get("reports", []):
        tool = item["tool"]
        if "score" in item:
            print(f"{tool}: {item['score']}/10 - {item['status']}")
        elif "percentage" in item:
            print(f"{tool}: {item['percentage']:.1f}% - {item['status']}")

    if "quality_gate" in report:
        print(f"Quality Gate: {report['quality_gate']}")

    return success


if __name__ == "__main__":
    main()
