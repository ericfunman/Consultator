#!/usr/bin/env python3
"""
Analyseur des workflows GitHub Actions pour le projet Consultator
Récupère et analyse les résultats des dernières exécutions des workflows
"""

import requests
import json
from datetime import datetime
import urllib3

# Désactiver les warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GitHubWorkflowAnalyzer:
    def __init__(self):
        self.repo_owner = "ericfunman"
        self.repo_name = "Consultator"
        self.base_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        
        # Headers pour l'API GitHub
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Workflow-Analyzer"
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

    def get_workflow_runs(self) -> dict:
        """Récupère les dernières exécutions de workflows"""
        print("🔍 Récupération des workflows...")
        return self._make_request("/actions/runs?per_page=20")

    def get_workflow_details(self, workflow_id: int) -> dict:
        """Récupère les détails d'un workflow spécifique"""
        return self._make_request(f"/actions/workflows/{workflow_id}")

    def format_duration(self, start_time: str, end_time: str = None) -> str:
        """Formate la durée d'exécution"""
        try:
            start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            if end_time:
                end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                duration = end - start
                return f"{duration.total_seconds():.0f}s"
            return "En cours..."
        except:
            return "N/A"

    def analyze_workflows(self):
        """Analyse principale des workflows"""
        print("🚀 Analyse des workflows GitHub Actions...")
        print("=" * 80)
        
        runs_data = self.get_workflow_runs()
        
        if not runs_data or 'workflow_runs' not in runs_data:
            print("❌ Impossible de récupérer les données des workflows")
            return

        workflow_runs = runs_data['workflow_runs']
        
        if not workflow_runs:
            print("ℹ️ Aucun workflow trouvé")
            return

        print(f"📊 RÉSULTATS DES WORKFLOWS ({len(workflow_runs)} exécutions récentes)")
        print("-" * 80)

        # Grouper par workflow
        workflows_summary = {}
        
        for run in workflow_runs:
            workflow_name = run.get('name', 'Unknown')
            
            if workflow_name not in workflows_summary:
                workflows_summary[workflow_name] = {
                    'total_runs': 0,
                    'success': 0,
                    'failure': 0,
                    'in_progress': 0,
                    'latest_run': None
                }
            
            workflows_summary[workflow_name]['total_runs'] += 1
            
            status = run.get('status', 'unknown')
            conclusion = run.get('conclusion')
            
            if status == 'completed':
                if conclusion == 'success':
                    workflows_summary[workflow_name]['success'] += 1
                elif conclusion in ['failure', 'cancelled']:
                    workflows_summary[workflow_name]['failure'] += 1
            else:
                workflows_summary[workflow_name]['in_progress'] += 1
            
            # Garder la dernière exécution
            if not workflows_summary[workflow_name]['latest_run']:
                workflows_summary[workflow_name]['latest_run'] = run

        # Afficher le résumé par workflow
        for workflow_name, summary in workflows_summary.items():
            latest = summary['latest_run']
            
            print(f"\n🔧 {workflow_name}")
            print(f"   📈 Exécutions totales: {summary['total_runs']}")
            print(f"   ✅ Succès: {summary['success']}")
            print(f"   ❌ Échecs: {summary['failure']}")
            print(f"   🔄 En cours: {summary['in_progress']}")
            
            if latest:
                status_icon = {
                    'success': '✅',
                    'failure': '❌', 
                    'cancelled': '🚫',
                    'in_progress': '🔄'
                }.get(latest.get('conclusion', latest.get('status', 'unknown')), '❓')
                
                duration = self.format_duration(
                    latest.get('created_at', ''),
                    latest.get('updated_at', '')
                )
                
                print(f"   🕐 Dernière exécution: {status_icon} {latest.get('conclusion', latest.get('status', 'unknown'))} ({duration})")
                print(f"   🌿 Branch: {latest.get('head_branch', 'N/A')}")
                print(f"   💾 Commit: {latest.get('head_sha', 'N/A')[:8]}")
                print(f"   📅 Date: {latest.get('created_at', 'N/A')[:19].replace('T', ' ')}")

        # Détails des 5 dernières exécutions
        print(f"\n🔍 DÉTAILS DES 5 DERNIÈRES EXÉCUTIONS")
        print("-" * 80)
        
        for i, run in enumerate(workflow_runs[:5]):
            status_icon = {
                'success': '✅',
                'failure': '❌',
                'cancelled': '🚫',
                'in_progress': '🔄'
            }.get(run.get('conclusion', run.get('status', 'unknown')), '❓')
            
            duration = self.format_duration(
                run.get('created_at', ''),
                run.get('updated_at', '')
            )
            
            print(f"{i+1}. {status_icon} {run.get('name', 'Unknown')} - {run.get('conclusion', run.get('status', 'unknown'))}")
            print(f"   📅 {run.get('created_at', 'N/A')[:19].replace('T', ' ')} ({duration})")
            print(f"   🌿 {run.get('head_branch', 'N/A')} - {run.get('head_sha', 'N/A')[:8]}")
            
            if run.get('conclusion') == 'failure':
                print(f"   🔗 Logs: {run.get('html_url', 'N/A')}")
            print()

        print("=" * 80)
        print(f"📅 Analyse effectuée le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")

if __name__ == "__main__":
    analyzer = GitHubWorkflowAnalyzer()
    analyzer.analyze_workflows()