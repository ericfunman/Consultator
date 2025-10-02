#!/usr/bin/env python3
"""
Analyseur des logs de workflow GitHub Actions en échec
"""

import requests
import json
import urllib3

# Désactiver les warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GitHubWorkflowLogAnalyzer:
    def __init__(self):
        self.repo_owner = "ericfunman"
        self.repo_name = "Consultator"
        self.base_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Workflow-Log-Analyzer"
        }

    def _make_request(self, endpoint: str) -> dict:
        """Fait une requête à l'API GitHub"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, headers=self.headers, verify=False, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Erreur API GitHub: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Erreur lors de la requête: {e}")
            return {}

    def analyze_failed_workflows(self):
        """Analyse les workflows en échec"""
        print("🔍 Analyse des workflows en échec...")
        print("=" * 80)
        
        # Récupérer les runs récents
        runs_data = self._make_request("/actions/runs?status=failure&per_page=5")
        
        if not runs_data or 'workflow_runs' not in runs_data:
            print("❌ Impossible de récupérer les données des workflows")
            return

        failed_runs = runs_data['workflow_runs']
        
        if not failed_runs:
            print("✅ Aucun workflow en échec récent trouvé")
            return

        print(f"📊 {len(failed_runs)} workflows en échec analysés")
        print("-" * 80)

        for i, run in enumerate(failed_runs[:3]):  # Analyser les 3 derniers échecs
            print(f"\n🔴 ÉCHEC #{i+1}: {run.get('name', 'Unknown')}")
            print(f"   📅 Date: {run.get('created_at', 'N/A')[:19].replace('T', ' ')}")
            print(f"   🌿 Branch: {run.get('head_branch', 'N/A')}")
            print(f"   💾 Commit: {run.get('head_sha', 'N/A')[:8]}")
            print(f"   🔗 URL: {run.get('html_url', 'N/A')}")
            
            # Récupérer les jobs de ce run
            run_id = run.get('id')
            if run_id:
                jobs_data = self._make_request(f"/actions/runs/{run_id}/jobs")
                
                if jobs_data and 'jobs' in jobs_data:
                    print(f"   📋 Jobs ({len(jobs_data['jobs'])}):")
                    
                    for job in jobs_data['jobs']:
                        job_status = job.get('conclusion', job.get('status', 'unknown'))
                        job_icon = '❌' if job_status == 'failure' else '✅' if job_status == 'success' else '🔄'
                        
                        print(f"      {job_icon} {job.get('name', 'Unknown Job')} - {job_status}")
                        
                        # Si le job a échoué, montrer les étapes
                        if job_status == 'failure' and 'steps' in job:
                            failed_steps = [step for step in job['steps'] if step.get('conclusion') == 'failure']
                            
                            if failed_steps:
                                print(f"         💥 Étapes en échec:")
                                for step in failed_steps[:3]:  # Max 3 étapes
                                    print(f"            • {step.get('name', 'Unknown Step')}")

        # Recommandations basées sur l'analyse
        print(f"\n💡 RECOMMANDATIONS")
        print("-" * 80)
        
        # Analyser les patterns d'échec
        workflow_names = [run.get('name', '') for run in failed_runs]
        test_failures = sum(1 for name in workflow_names if 'Test' in name or 'test' in name)
        
        if test_failures > 0:
            print("🧪 PROBLÈMES DE TESTS DÉTECTÉS:")
            print("   • Vérifier les tests qui échouent en local")
            print("   • Contrôler les dépendances dans requirements-test.txt")
            print("   • Vérifier la compatibilité Python 3.9/3.10/3.11")
            print("   • Examiner la configuration de la base de données de test")
            
        print("\n🔧 ACTIONS RECOMMANDÉES:")
        print("   1. Exécuter les tests localement: pytest tests/ -v")
        print("   2. Vérifier les imports manquants")
        print("   3. Corriger les tests qui échouent")
        print("   4. Tester avec différentes versions de Python")
        print("   5. Relancer le workflow après corrections")

if __name__ == "__main__":
    analyzer = GitHubWorkflowLogAnalyzer()
    analyzer.analyze_failed_workflows()