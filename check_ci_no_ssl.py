"""
Script pour vérifier le statut CI/CD sans vérification SSL
⚠️ ATTENTION: Désactive la vérification SSL - À utiliser uniquement pour diagnostic
"""

import requests
import urllib3
from datetime import datetime

# Désactiver les warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_ci_status():
    """Récupère le statut du dernier workflow CI/CD sans vérifier SSL"""
    
    # Configuration GitHub
    owner = "ericfunman"
    repo = "Consultator"
    workflow_name = "tests-simplified.yml"
    
    # URL de l'API GitHub
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_name}/runs"
    
    try:
        print("🔍 Récupération du statut CI/CD (SSL verification disabled)...")
        print(f"URL: {url}\n")
        
        # Requête sans vérification SSL
        response = requests.get(url, verify=False, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('workflow_runs'):
            print("❌ Aucune exécution trouvée")
            return
        
        # Dernière exécution
        latest_run = data['workflow_runs'][0]
        
        print("=" * 80)
        print("📊 DERNIER RUN CI/CD")
        print("=" * 80)
        print(f"Run ID:        {latest_run['id']}")
        print(f"Run Number:    #{latest_run['run_number']}")
        print(f"Status:        {latest_run['status']}")
        print(f"Conclusion:    {latest_run['conclusion']}")
        print(f"Commit:        {latest_run['head_sha'][:8]}")
        print(f"Branch:        {latest_run['head_branch']}")
        print(f"Message:       {latest_run['head_commit']['message'][:100]}")
        print(f"Created:       {latest_run['created_at']}")
        print(f"Updated:       {latest_run['updated_at']}")
        print(f"URL:           {latest_run['html_url']}")
        print("=" * 80)
        
        # Si échec, récupérer les détails des jobs
        if latest_run['conclusion'] == 'failure':
            print("\n❌ DÉTECTION D'UN ÉCHEC - Récupération des détails...\n")
            
            jobs_url = latest_run['jobs_url']
            jobs_response = requests.get(jobs_url, verify=False, timeout=10)
            jobs_response.raise_for_status()
            
            jobs_data = jobs_response.json()
            
            for job in jobs_data.get('jobs', []):
                print(f"\n📋 Job: {job['name']}")
                print(f"   Status:     {job['status']}")
                print(f"   Conclusion: {job['conclusion']}")
                print(f"   Started:    {job.get('started_at', 'N/A')}")
                print(f"   Completed:  {job.get('completed_at', 'N/A')}")
                
                # Afficher les étapes échouées
                if job['conclusion'] == 'failure':
                    print("\n   ❌ ÉTAPES ÉCHOUÉES:")
                    for step in job.get('steps', []):
                        if step.get('conclusion') == 'failure':
                            print(f"      • {step['name']}")
                            print(f"        Conclusion: {step['conclusion']}")
                            print(f"        Numéro: {step['number']}")
                
                print("   " + "-" * 76)
        
        elif latest_run['conclusion'] == 'success':
            print("\n✅ Le dernier run a réussi!")
        
        # Afficher les 5 dernières exécutions
        print("\n" + "=" * 80)
        print("📜 HISTORIQUE DES 5 DERNIERS RUNS")
        print("=" * 80)
        
        for i, run in enumerate(data['workflow_runs'][:5], 1):
            status_icon = "✅" if run['conclusion'] == 'success' else "❌"
            print(f"{i}. {status_icon} Run #{run['run_number']} - {run['conclusion']} - {run['head_sha'][:8]} - {run['created_at']}")
        
        print("=" * 80)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("⚠️  ATTENTION: Ce script désactive la vérification SSL")
    print("⚠️  À utiliser uniquement pour diagnostic sur réseau d'entreprise")
    print("=" * 80 + "\n")
    check_ci_status()
