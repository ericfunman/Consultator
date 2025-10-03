"""
Script pour vérifier le statut du dernier run CI/CD
"""
import requests
import os

def check_latest_run():
    token = os.getenv('GITHUB_TOKEN', '')
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    } if token else {}
    
    # Récupérer le dernier run
    url = 'https://api.github.com/repos/ericfunman/Consultator/actions/runs'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        runs = response.json().get('workflow_runs', [])
        if runs:
            latest = runs[0]
            print(f"📊 Dernier Run CI/CD")
            print(f"{'='*60}")
            print(f"🔹 Run ID: {latest['id']}")
            print(f"🔹 Run Number: #{latest['run_number']}")
            print(f"🔹 Status: {latest['status']}")
            print(f"🔹 Conclusion: {latest['conclusion']}")
            print(f"🔹 Commit: {latest['head_sha'][:8]}")
            print(f"🔹 Branche: {latest['head_branch']}")
            print(f"🔹 Workflow: {latest['name']}")
            print(f"🔹 Date: {latest['created_at']}")
            print(f"🔹 URL: {latest['html_url']}")
            print(f"{'='*60}")
            
            # Si échec, récupérer les détails des jobs
            if latest['conclusion'] == 'failure':
                print(f"\n❌ Le CI/CD a échoué. Récupération des détails...\n")
                
                jobs_url = latest['jobs_url']
                jobs_response = requests.get(jobs_url, headers=headers)
                
                if jobs_response.status_code == 200:
                    jobs = jobs_response.json().get('jobs', [])
                    print(f"📋 Jobs du workflow ({len(jobs)} total):")
                    print(f"{'-'*60}")
                    
                    for job in jobs:
                        status_emoji = "✅" if job['conclusion'] == 'success' else "❌"
                        print(f"\n{status_emoji} Job: {job['name']}")
                        print(f"   Status: {job['status']}")
                        print(f"   Conclusion: {job['conclusion']}")
                        
                        if job['conclusion'] == 'failure':
                            print(f"\n   🔍 Steps du job échoué:")
                            for step in job['steps']:
                                if step['conclusion'] == 'failure':
                                    print(f"      ❌ {step['name']}")
                                    print(f"         Conclusion: {step['conclusion']}")
                                    print(f"         Numéro: {step['number']}")
                                elif step['conclusion'] == 'success':
                                    print(f"      ✅ {step['name']}")
            
            elif latest['conclusion'] == 'success':
                print(f"\n✅ Le CI/CD a réussi !")
                
            elif latest['status'] == 'in_progress':
                print(f"\n⏳ Le CI/CD est en cours d'exécution...")
                
            elif latest['status'] == 'queued':
                print(f"\n⏸️ Le CI/CD est en attente...")
        else:
            print("Aucun run trouvé")
    else:
        print(f"Erreur API: {response.status_code}")
        print(f"Message: {response.text}")

if __name__ == '__main__':
    check_latest_run()
