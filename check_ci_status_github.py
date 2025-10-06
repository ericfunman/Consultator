#!/usr/bin/env python3
"""
Script pour vérifier l'état du CI/CD GitHub Actions
"""
import json
import requests
from datetime import datetime

def check_github_actions():
    """Vérifie l'état des dernières exécutions GitHub Actions"""
    repo = "ericfunman/Consultator"
    url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=3"
    
    try:
        print(f"🔍 Vérification du CI/CD pour {repo}...")
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        runs = data.get("workflow_runs", [])
        
        if not runs:
            print("❌ Aucune exécution trouvée")
            return
        
        print(f"\n📊 {len(runs)} dernières exécutions:\n")
        
        for i, run in enumerate(runs, 1):
            name = run.get("name", "Unknown")
            status = run.get("status", "unknown")
            conclusion = run.get("conclusion", "N/A")
            created = run.get("created_at", "")
            branch = run.get("head_branch", "unknown")
            commit = run.get("head_sha", "")[:7]
            run_number = run.get("run_number", 0)
            html_url = run.get("html_url", "")
            
            # Emoji pour le statut
            status_emoji = {
                "completed": "✅" if conclusion == "success" else "❌",
                "in_progress": "⏳",
                "queued": "⏱️",
                "waiting": "⏸️"
            }.get(status, "❓")
            
            conclusion_emoji = {
                "success": "✅",
                "failure": "❌",
                "cancelled": "🚫",
                "skipped": "⏭️",
                "timed_out": "⏱️"
            }.get(conclusion, "")
            
            print(f"{status_emoji} Run #{run_number} - {name}")
            print(f"   Status: {status} | Conclusion: {conclusion} {conclusion_emoji}")
            print(f"   Branch: {branch} | Commit: {commit}")
            print(f"   Créé: {created}")
            print(f"   URL: {html_url}")
            
            # Si échec, récupérer les détails
            if conclusion == "failure":
                print(f"\n   🔍 Récupération des détails de l'échec...")
                jobs_url = run.get("jobs_url", "")
                if jobs_url:
                    jobs_response = requests.get(jobs_url)
                    if jobs_response.status_code == 200:
                        jobs_data = jobs_response.json()
                        failed_jobs = [j for j in jobs_data.get("jobs", []) if j.get("conclusion") == "failure"]
                        
                        for job in failed_jobs:
                            job_name = job.get("name", "Unknown")
                            print(f"      ❌ Job échoué: {job_name}")
                            
                            # Récupérer les steps échoués
                            steps = job.get("steps", [])
                            for step in steps:
                                if step.get("conclusion") == "failure":
                                    step_name = step.get("name", "Unknown")
                                    print(f"         💥 Step: {step_name}")
            
            print()
        
    except requests.RequestException as e:
        print(f"❌ Erreur lors de la récupération: {e}")

if __name__ == "__main__":
    check_github_actions()
