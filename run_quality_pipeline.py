"""
Script principal d'automatisation des tests et de l'analyse de qualité
Exécution automatique après chaque modification pour validation de non-régression
"""

import subprocess
import sys
import time
import json
from pathlib import Path
from datetime import datetime
import argparse

class AutomatedQualityPipeline:
    """Pipeline automatisé de qualité et tests"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        self.test_results = {}
        
    def install_dependencies(self):
        """Installe les dépendances de test si nécessaire"""
        print("🔧 Vérification des dépendances de test...")
        
        try:
            # Installer les dépendances de test
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"
            ], check=True, capture_output=True)
            
            print("✅ Dépendances de test installées")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur installation dépendances : {e}")
            return False
            
    def run_unit_tests(self):
        """Exécute les tests unitaires avec coverage"""
        print("🧪 Exécution des tests unitaires...")
        
        try:
            # Lancer pytest avec coverage
            result = subprocess.run([
                "python", "-m", "pytest", 
                "tests/",
                "-v",
                "--cov=app",
                "--cov-report=xml:reports/coverage.xml",
                "--cov-report=html:reports/htmlcov",
                "--cov-report=term-missing",
                "--junitxml=reports/test-results.xml",
                "--html=reports/test-report.html",
                "--tb=short"
            ], capture_output=True, text=True, timeout=300)
            
            # Sauvegarder les résultats
            with open(self.reports_dir / "pytest-output.txt", "w", encoding="utf-8") as f:
                f.write(result.stdout)
                f.write(result.stderr)
            
            # Analyser les résultats
            success = result.returncode == 0
            self.test_results['unit_tests'] = {
                'success': success,
                'exit_code': result.returncode,
                'duration': 'completed'
            }
            
            if success:
                print("✅ Tests unitaires réussis")
            else:
                print("❌ Échec des tests unitaires")
                print(f"Code de sortie : {result.returncode}")
                
            return success
            
        except subprocess.TimeoutExpired:
            print("⏰ Timeout des tests unitaires (5 min)")
            self.test_results['unit_tests'] = {'success': False, 'error': 'timeout'}
            return False
        except Exception as e:
            print(f"❌ Erreur tests unitaires : {e}")
            self.test_results['unit_tests'] = {'success': False, 'error': str(e)}
            return False
            
    def run_smoke_tests(self):
        """Exécute les tests de fumée (smoke tests)"""
        print("💨 Exécution des tests de fumée...")
        
        try:
            # Tests de fumée basiques
            result = subprocess.run([
                "python", "-m", "pytest", 
                "tests/",
                "-m", "smoke",
                "-v",
                "--tb=short"
            ], capture_output=True, text=True, timeout=120)
            
            success = result.returncode == 0
            self.test_results['smoke_tests'] = {
                'success': success,
                'exit_code': result.returncode
            }
            
            if success:
                print("✅ Tests de fumée réussis")
            else:
                print("❌ Échec des tests de fumée")
                
            return success
            
        except Exception as e:
            print(f"❌ Erreur tests de fumée : {e}")
            self.test_results['smoke_tests'] = {'success': False, 'error': str(e)}
            return False
            
    def run_regression_tests(self):
        """Exécute les tests de non-régression"""
        print("🔄 Exécution des tests de régression...")
        
        try:
            result = subprocess.run([
                "python", "-m", "pytest", 
                "tests/",
                "-m", "regression",
                "-v",
                "--tb=short"
            ], capture_output=True, text=True, timeout=180)
            
            success = result.returncode == 0
            self.test_results['regression_tests'] = {
                'success': success,
                'exit_code': result.returncode
            }
            
            if success:
                print("✅ Tests de régression réussis")
            else:
                print("⚠️ Attention : Détection de régression possible")
                
            return success
            
        except Exception as e:
            print(f"❌ Erreur tests de régression : {e}")
            self.test_results['regression_tests'] = {'success': False, 'error': str(e)}
            return False
            
    def run_linting(self):
        """Exécute l'analyse de code (linting)"""
        print("📊 Analyse de code en cours...")
        
        lint_results = {}
        
        # Pylint
        try:
            result = subprocess.run([
                "pylint", "app/", 
                "--output-format=text",
                "--score=yes"
            ], capture_output=True, text=True)
            
            with open(self.reports_dir / "pylint-report.txt", "w", encoding="utf-8") as f:
                f.write(result.stdout)
                f.write(result.stderr)
                
            # Extraire le score
            score = self._extract_pylint_score(result.stdout)
            lint_results['pylint'] = {'score': score, 'success': score >= 8.0}
            
            print(f"📊 Pylint Score : {score}/10")
            
        except Exception as e:
            print(f"❌ Erreur Pylint : {e}")
            lint_results['pylint'] = {'success': False, 'error': str(e)}
            
        # Flake8
        try:
            result = subprocess.run([
                "flake8", "app/",
                "--format=default",
                "--output-file", str(self.reports_dir / "flake8-report.txt")
            ], capture_output=True, text=True)
            
            issues_count = self._count_flake8_issues()
            lint_results['flake8'] = {
                'issues': issues_count, 
                'success': issues_count < 50
            }
            
            print(f"📊 Flake8 : {issues_count} problèmes détectés")
            
        except Exception as e:
            print(f"❌ Erreur Flake8 : {e}")
            lint_results['flake8'] = {'success': False, 'error': str(e)}
            
        # Bandit (sécurité)
        try:
            result = subprocess.run([
                "bandit", "-r", "app/",
                "-f", "json",
                "-o", str(self.reports_dir / "bandit-report.json")
            ], capture_output=True, text=True)
            
            security_issues = self._count_bandit_issues()
            lint_results['bandit'] = {
                'security_issues': security_issues,
                'success': security_issues == 0
            }
            
            print(f"🔒 Bandit : {security_issues} problèmes de sécurité")
            
        except Exception as e:
            print(f"❌ Erreur Bandit : {e}")
            lint_results['bandit'] = {'success': False, 'error': str(e)}
            
        self.test_results['linting'] = lint_results
        
        # Retourner True si tous les outils passent leurs seuils
        return all(tool.get('success', False) for tool in lint_results.values())
        
    def run_app_startup_test(self):
        """Test de démarrage de l'application"""
        print("🚀 Test de démarrage de l'application...")
        
        try:
            # Test de démarrage rapide (timeout 30s)
            result = subprocess.run([
                "python", "-c", 
                "import streamlit; print('Streamlit OK'); "
                "import app.main; print('App import OK')"
            ], capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0
            self.test_results['startup_test'] = {
                'success': success,
                'output': result.stdout
            }
            
            if success:
                print("✅ Démarrage de l'application : OK")
            else:
                print("❌ Échec du démarrage de l'application")
                print(result.stderr)
                
            return success
            
        except subprocess.TimeoutExpired:
            print("⏰ Timeout du test de démarrage")
            self.test_results['startup_test'] = {'success': False, 'error': 'timeout'}
            return False
        except Exception as e:
            print(f"❌ Erreur test démarrage : {e}")
            self.test_results['startup_test'] = {'success': False, 'error': str(e)}
            return False
            
    def run_database_tests(self):
        """Test de l'intégrité de la base de données"""
        print("🗃️ Test de la base de données...")
        
        try:
            # Test basique de la base de données
            result = subprocess.run([
                "python", "-c",
                "from app.database.database import init_database, get_database_session; "
                "init_database(); "
                "with get_database_session() as session: print('DB OK')"
            ], capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0
            self.test_results['database_test'] = {
                'success': success,
                'output': result.stdout
            }
            
            if success:
                print("✅ Base de données : OK")
            else:
                print("❌ Échec test base de données")
                print(result.stderr)
                
            return success
            
        except Exception as e:
            print(f"❌ Erreur test DB : {e}")
            self.test_results['database_test'] = {'success': False, 'error': str(e)}
            return False
            
    def generate_summary_report(self):
        """Génère un rapport de synthèse"""
        print("📋 Génération du rapport de synthèse...")
        
        timestamp = datetime.now().isoformat()
        
        summary = {
            'timestamp': timestamp,
            'project': 'Consultator',
            'pipeline_results': self.test_results,
            'overall_success': self._calculate_overall_success(),
            'recommendations': self._generate_recommendations()
        }
        
        # Sauvegarde JSON
        report_file = self.reports_dir / f"pipeline-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        # Rapport texte
        self._generate_text_report(summary)
        
        print(f"✅ Rapport sauvegardé : {report_file}")
        return summary
        
    def _extract_pylint_score(self, output):
        """Extrait le score Pylint du output"""
        try:
            for line in output.split('\n'):
                if "Your code has been rated at" in line:
                    return float(line.split("rated at ")[1].split("/10")[0])
            return 0.0
        except:
            return 0.0
            
    def _count_flake8_issues(self):
        """Compte les problèmes Flake8"""
        try:
            flake8_file = self.reports_dir / "flake8-report.txt"
            if flake8_file.exists():
                with open(flake8_file, "r", encoding="utf-8") as f:
                    return len(f.readlines())
            return 0
        except:
            return 999
            
    def _count_bandit_issues(self):
        """Compte les problèmes de sécurité Bandit"""
        try:
            bandit_file = self.reports_dir / "bandit-report.json"
            if bandit_file.exists():
                with open(bandit_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return len(data.get("results", []))
            return 0
        except:
            return 999
            
    def _calculate_overall_success(self):
        """Calcule le succès global du pipeline"""
        critical_tests = ['unit_tests', 'startup_test', 'database_test']
        
        # Tests critiques doivent tous passer
        for test_name in critical_tests:
            if not self.test_results.get(test_name, {}).get('success', False):
                return False
                
        # Linting doit avoir un score acceptable
        lint_results = self.test_results.get('linting', {})
        pylint_success = lint_results.get('pylint', {}).get('success', False)
        
        return pylint_success
        
    def _generate_recommendations(self):
        """Génère des recommandations basées sur les résultats"""
        recommendations = []
        
        # Recommandations basées sur les résultats
        if not self.test_results.get('unit_tests', {}).get('success', False):
            recommendations.append("❌ Corriger les tests unitaires qui échouent")
            
        if not self.test_results.get('regression_tests', {}).get('success', False):
            recommendations.append("⚠️ Vérifier les régressions détectées")
            
        lint_results = self.test_results.get('linting', {})
        pylint_score = lint_results.get('pylint', {}).get('score', 0)
        
        if pylint_score < 8.0:
            recommendations.append(f"📊 Améliorer le score Pylint (actuel: {pylint_score}/10)")
            
        flake8_issues = lint_results.get('flake8', {}).get('issues', 0)
        if flake8_issues > 50:
            recommendations.append(f"🔧 Corriger les {flake8_issues} problèmes Flake8")
            
        security_issues = lint_results.get('bandit', {}).get('security_issues', 0)
        if security_issues > 0:
            recommendations.append(f"🔒 Corriger les {security_issues} problèmes de sécurité")
            
        if not recommendations:
            recommendations.append("✅ Tous les tests passent ! Code de qualité excellent.")
            
        return recommendations
        
    def _generate_text_report(self, summary):
        """Génère un rapport texte lisible"""
        report_lines = [
            "="*60,
            "📊 RAPPORT DE QUALITÉ - CONSULTATOR",
            "="*60,
            f"⏰ Timestamp: {summary['timestamp']}",
            f"🎯 Succès global: {'✅ OUI' if summary['overall_success'] else '❌ NON'}",
            "",
            "📋 RÉSULTATS DES TESTS:",
            "-"*30
        ]
        
        for test_name, results in summary['pipeline_results'].items():
            if isinstance(results, dict):
                success = results.get('success', False)
                status = "✅ PASS" if success else "❌ FAIL"
                report_lines.append(f"{test_name}: {status}")
                
                if test_name == 'linting' and isinstance(results, dict):
                    for tool, tool_results in results.items():
                        if isinstance(tool_results, dict):
                            tool_success = tool_results.get('success', False)
                            tool_status = "✅" if tool_success else "❌"
                            score = tool_results.get('score', '')
                            issues = tool_results.get('issues', '')
                            detail = f" (Score: {score})" if score else f" ({issues} issues)" if issues else ""
                            report_lines.append(f"  └─ {tool}: {tool_status}{detail}")
        
        report_lines.extend([
            "",
            "💡 RECOMMANDATIONS:",
            "-"*20
        ])
        
        for i, rec in enumerate(summary['recommendations'], 1):
            report_lines.append(f"{i}. {rec}")
        
        report_lines.append("="*60)
        
        # Sauvegarder le rapport texte
        text_report_file = self.reports_dir / f"quality-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(text_report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
            
        # Afficher le rapport
        print("\n".join(report_lines))


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="Pipeline automatisé de qualité")
    parser.add_argument("--skip-install", action="store_true", help="Ignorer l'installation des dépendances")
    parser.add_argument("--quick", action="store_true", help="Exécution rapide (tests essentiels seulement)")
    parser.add_argument("--regression-only", action="store_true", help="Tests de régression seulement")
    
    args = parser.parse_args()
    
    pipeline = AutomatedQualityPipeline()
    
    start_time = time.time()
    print("🚀 DÉMARRAGE DU PIPELINE DE QUALITÉ")
    print("="*50)
    
    success_count = 0
    total_tests = 0
    
    # Installation des dépendances
    if not args.skip_install:
        if pipeline.install_dependencies():
            success_count += 1
        total_tests += 1
    
    # Tests essentiels
    essential_tests = [
        ('startup_test', pipeline.run_app_startup_test),
        ('database_test', pipeline.run_database_tests)
    ]
    
    for test_name, test_func in essential_tests:
        total_tests += 1
        if test_func():
            success_count += 1
        else:
            print(f"⚠️ Test essentiel {test_name} échoué")
            
    # Tests rapides ou complets
    if args.quick:
        test_suite = [
            ('smoke_tests', pipeline.run_smoke_tests),
            ('linting', pipeline.run_linting)
        ]
    elif args.regression_only:
        test_suite = [
            ('regression_tests', pipeline.run_regression_tests)
        ]
    else:
        test_suite = [
            ('unit_tests', pipeline.run_unit_tests),
            ('smoke_tests', pipeline.run_smoke_tests),
            ('regression_tests', pipeline.run_regression_tests),
            ('linting', pipeline.run_linting)
        ]
    
    # Exécution des tests
    for test_name, test_func in test_suite:
        total_tests += 1
        if test_func():
            success_count += 1
            
    # Rapport final
    summary = pipeline.generate_summary_report()
    
    execution_time = time.time() - start_time
    
    print(f"\n⏱️ Temps d'exécution: {execution_time:.1f}s")
    print(f"📊 Tests réussis: {success_count}/{total_tests}")
    
    if summary['overall_success']:
        print("🎉 PIPELINE RÉUSSI - Code prêt pour production !")
        return 0
    else:
        print("❌ PIPELINE ÉCHOUÉ - Corrections nécessaires")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
