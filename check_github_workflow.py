"""
Script pour récupérer les logs du dernier workflow GitHub Actions
"""

import requests
import os
from datetime import datetime

# Configuration
GITHUB_OWNER = "ericfunman"
GITHUB_REPO = "Consultator"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

def get_latest_workflow_run():
    """Récupère la dernière exécution du workflow"""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs"
    
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("workflow_runs"):
            print("❌ Aucun workflow trouvé")
            return None
        
        # Trier par date de création (plus récent en premier)
        runs = sorted(data["workflow_runs"], key=lambda x: x["created_at"], reverse=True)
        
        print("=" * 80)
        print("📋 DERNIÈRES EXÉCUTIONS DE WORKFLOWS")
        print("=" * 80)
        
        for i, run in enumerate(runs[:5], 1):
            created = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            status_emoji = {
                "completed": "✅" if run["conclusion"] == "success" else "❌",
                "in_progress": "🔄",
                "queued": "⏳"
            }.get(run["status"], "❓")
            
            print(f"\n{i}. {status_emoji} {run['name']}")
            print(f"   Status: {run['status']}")
            print(f"   Conclusion: {run.get('conclusion', 'N/A')}")
            print(f"   Commit: {run['head_sha'][:8]}")
            print(f"   Branch: {run['head_branch']}")
            print(f"   Date: {created.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   URL: {run['html_url']}")
        
        return runs[0]
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des workflows: {e}")
        return None

def get_workflow_jobs(run_id):
    """Récupère les jobs d'une exécution de workflow"""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs/{run_id}/jobs"
    
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        print("\n" + "=" * 80)
        print("🔧 JOBS DU WORKFLOW")
        print("=" * 80)
        
        for job in data.get("jobs", []):
            status_emoji = {
                "completed": "✅" if job["conclusion"] == "success" else "❌",
                "in_progress": "🔄",
                "queued": "⏳"
            }.get(job["status"], "❓")
            
            print(f"\n{status_emoji} Job: {job['name']}")
            print(f"   Status: {job['status']}")
            print(f"   Conclusion: {job.get('conclusion', 'N/A')}")
            
            # Afficher les steps en erreur
            if job.get("steps"):
                for step in job["steps"]:
                    if step.get("conclusion") == "failure":
                        print(f"   ❌ Step échoué: {step['name']}")
                        print(f"      Durée: {step.get('completed_at', 'N/A')}")
        
        return data.get("jobs", [])
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des jobs: {e}")
        return []

def get_job_logs(job_id):
    """Récupère les logs d'un job spécifique"""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/jobs/{job_id}/logs"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            return response.text
        else:
            return f"Erreur {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Erreur lors de la récupération des logs: {e}"

def main():
    print("🔍 ANALYSE DES WORKFLOWS GITHUB ACTIONS - CONSULTATOR")
    print("=" * 80)
    
    # Récupérer le dernier workflow
    latest_run = get_latest_workflow_run()
    
    if not latest_run:
        return
    
    # Récupérer les jobs
    jobs = get_workflow_jobs(latest_run["id"])
    
    # Trouver les jobs en erreur et afficher leurs logs
    failed_jobs = [job for job in jobs if job.get("conclusion") == "failure"]
    
    if failed_jobs:
        print("\n" + "=" * 80)
        print("📝 LOGS DES JOBS EN ERREUR")
        print("=" * 80)
        
        for job in failed_jobs:
            print(f"\n{'=' * 80}")
            print(f"Job: {job['name']}")
            print(f"{'=' * 80}")
            
            logs = get_job_logs(job["id"])
            
            # Extraire les parties pertinentes (erreurs)
            lines = logs.split('\n')
            error_lines = []
            capture = False
            
            for i, line in enumerate(lines):
                # Capturer autour des erreurs
                if any(keyword in line.lower() for keyword in ['error', 'failed', 'exception', 'traceback']):
                    capture = True
                    # Prendre 5 lignes avant et après
                    start = max(0, i - 5)
                    end = min(len(lines), i + 10)
                    error_lines.extend(lines[start:end])
                    error_lines.append("..." + "-" * 40)
            
            if error_lines:
                print("\n🔴 Extraits des erreurs:")
                for line in error_lines[:100]:  # Limiter à 100 lignes
                    print(line)
            else:
                print("\n📄 Logs complets (dernières 50 lignes):")
                for line in lines[-50:]:
                    print(line)
    
    print("\n" + "=" * 80)
    print("✅ Analyse terminée")
    print("=" * 80)

if __name__ == "__main__":
    main()
