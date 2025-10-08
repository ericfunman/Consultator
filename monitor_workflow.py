"""
Script de monitoring du workflow GitHub Actions et SonarCloud
"""

import requests
import time
from datetime import datetime

GITHUB_OWNER = "ericfunman"
GITHUB_REPO = "Consultator"
EXPECTED_COMMIT = "22cfcd1"

def check_workflow_status():
    """Vérifie le statut du workflow GitHub Actions"""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        runs = sorted(data["workflow_runs"], key=lambda x: x["created_at"], reverse=True)
        
        print("=" * 80)
        print(f"🔍 MONITORING WORKFLOW - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 80)
        
        latest_run = runs[0] if runs else None
        
        if latest_run:
            commit_sha = latest_run['head_sha'][:7]
            status = latest_run['status']
            conclusion = latest_run.get('conclusion', 'N/A')
            
            status_emoji = {
                "completed": "✅" if conclusion == "success" else "❌",
                "in_progress": "🔄",
                "queued": "⏳"
            }.get(status, "❓")
            
            print(f"\n{status_emoji} Dernier workflow:")
            print(f"   Commit: {commit_sha}")
            print(f"   Status: {status}")
            print(f"   Conclusion: {conclusion}")
            print(f"   URL: {latest_run['html_url']}")
            
            if commit_sha == EXPECTED_COMMIT:
                print(f"\n✅ Le commit {EXPECTED_COMMIT} est en cours d'exécution !")
                return status, conclusion
            else:
                print(f"\n⏳ En attente du commit {EXPECTED_COMMIT}")
                print(f"   Dernier commit traité: {commit_sha}")
                return "waiting", None
        
        return "unknown", None
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return "error", None

def check_sonarcloud_coverage():
    """Vérifie la couverture sur SonarCloud"""
    url = f"https://sonarcloud.io/api/measures/component"
    params = {
        "component": f"{GITHUB_OWNER}_{GITHUB_REPO}",
        "metricKeys": "coverage,lines_to_cover,uncovered_lines"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        measures = data.get("component", {}).get("measures", [])
        
        coverage_data = {}
        for measure in measures:
            coverage_data[measure["metric"]] = measure.get("value", "N/A")
        
        print("\n" + "=" * 80)
        print("📊 COUVERTURE SONARCLOUD")
        print("=" * 80)
        
        coverage = float(coverage_data.get("coverage", "0"))
        print(f"🎯 Couverture: {coverage}%")
        print(f"📏 Lignes à couvrir: {coverage_data.get('lines_to_cover', 'N/A')}")
        print(f"❌ Lignes non couvertes: {coverage_data.get('uncovered_lines', 'N/A')}")
        
        if coverage >= 80:
            print("\n🎉 OBJECTIF ATTEINT ! Couverture ≥ 80%")
        else:
            print(f"\n⏳ Objectif: 80% (manque {80 - coverage:.1f} points)")
        
        return coverage
        
    except Exception as e:
        print(f"❌ Erreur SonarCloud: {e}")
        return None

def main():
    """Monitoring principal"""
    print("🚀 DÉMARRAGE DU MONITORING")
    print("=" * 80)
    print(f"Commit attendu: {EXPECTED_COMMIT}")
    print(f"Objectif: Couverture ≥ 80% sur SonarCloud")
    print("=" * 80)
    
    max_iterations = 20
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # Vérifier le workflow
        status, conclusion = check_workflow_status()
        
        # Si le workflow est terminé avec succès
        if status == "completed" and conclusion == "success":
            print("\n✅ Workflow terminé avec succès !")
            
            # Attendre un peu pour laisser SonarCloud traiter
            print("\n⏳ Attente de 30 secondes pour l'analyse SonarCloud...")
            time.sleep(30)
            
            # Vérifier la couverture
            coverage = check_sonarcloud_coverage()
            
            if coverage and coverage >= 80:
                print("\n" + "=" * 80)
                print("🎉 SUCCÈS ! OBJECTIF ATTEINT !")
                print("=" * 80)
                break
            else:
                print("\n⚠️ La couverture n'a pas encore été mise à jour")
                print("   Nouvelle tentative dans 30 secondes...")
        
        # Si le workflow a échoué
        elif status == "completed" and conclusion != "success":
            print("\n❌ Le workflow a échoué !")
            print("   Vérifiez les logs sur GitHub Actions")
            break
        
        # Si le workflow est en cours
        elif status == "in_progress":
            print(f"\n🔄 Workflow en cours... (tentative {iteration}/{max_iterations})")
        
        # Attendre avant la prochaine vérification
        if iteration < max_iterations:
            print(f"\n⏳ Prochaine vérification dans 30 secondes...")
            time.sleep(30)
    
    print("\n" + "=" * 80)
    print("✅ Monitoring terminé")
    print("=" * 80)

if __name__ == "__main__":
    main()
