"""
Script pour vérifier la couverture SonarCloud et diagnostiquer le problème
"""
import requests
import json
from datetime import datetime
import urllib3

# Désactiver les warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
SONAR_TOKEN = "dc9f7acde5993776f1823d2084864bd610bc9e2b"
PROJECT_KEY = "ericfunman_Consultator"
BASE_URL = "https://sonarcloud.io/api"

def get_project_measures():
    """Récupère les métriques du projet incluant la couverture"""
    url = f"{BASE_URL}/measures/component"
    params = {
        "component": PROJECT_KEY,
        "metricKeys": "coverage,line_coverage,branch_coverage,lines_to_cover,uncovered_lines,tests,test_success_density,test_execution_time"
    }
    
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        
        component = data.get('component', {})
        measures = component.get('measures', [])
        
        print("📊 MÉTRIQUES SONARCLOUD")
        print("=" * 70)
        
        metrics = {}
        for measure in measures:
            metric_key = measure.get('metric')
            value = measure.get('value', 'N/A')
            metrics[metric_key] = value
            
            # Affichage formaté
            if metric_key == 'coverage':
                print(f"🎯 Couverture totale: {value}%")
            elif metric_key == 'line_coverage':
                print(f"📝 Couverture des lignes: {value}%")
            elif metric_key == 'branch_coverage':
                print(f"🔀 Couverture des branches: {value}%")
            elif metric_key == 'lines_to_cover':
                print(f"📏 Lignes à couvrir: {value}")
            elif metric_key == 'uncovered_lines':
                print(f"❌ Lignes non couvertes: {value}")
            elif metric_key == 'tests':
                print(f"🧪 Nombre de tests: {value}")
            elif metric_key == 'test_success_density':
                print(f"✅ Taux de réussite des tests: {value}%")
        
        return metrics
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des métriques: {e}")
        return None

def get_project_analyses():
    """Récupère l'historique des analyses"""
    url = f"{BASE_URL}/project_analyses/search"
    params = {
        "project": PROJECT_KEY,
        "ps": 10  # Dernières 10 analyses
    }
    
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        
        analyses = data.get('analyses', [])
        
        print("\n📅 HISTORIQUE DES ANALYSES (10 dernières)")
        print("=" * 70)
        
        for i, analysis in enumerate(analyses[:5], 1):
            date = analysis.get('date', 'N/A')
            revision = analysis.get('revision', 'N/A')[:8]  # 8 premiers caractères du commit
            events = analysis.get('events', [])
            
            # Convertir la date
            try:
                dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_formatted = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_formatted = date
            
            print(f"\n{i}. Analyse du {date_formatted}")
            print(f"   Commit: {revision}")
            
            if events:
                print(f"   Événements:")
                for event in events:
                    print(f"   - {event.get('category', 'N/A')}: {event.get('name', 'N/A')}")
        
        return analyses
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des analyses: {e}")
        return None

def get_coverage_history():
    """Récupère l'historique de la couverture"""
    url = f"{BASE_URL}/measures/search_history"
    params = {
        "component": PROJECT_KEY,
        "metrics": "coverage,lines_to_cover,uncovered_lines",
        "ps": 10
    }
    
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        
        measures = data.get('measures', [])
        
        print("\n📈 ÉVOLUTION DE LA COUVERTURE")
        print("=" * 70)
        
        for measure in measures:
            metric = measure.get('metric')
            history = measure.get('history', [])
            
            if metric == 'coverage' and history:
                print(f"\n{metric.upper()}:")
                for entry in history[-5:]:  # 5 dernières valeurs
                    date = entry.get('date', 'N/A')
                    value = entry.get('value', 'N/A')
                    
                    try:
                        dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
                        date_formatted = dt.strftime('%Y-%m-%d %H:%M')
                    except:
                        date_formatted = date
                    
                    print(f"  {date_formatted}: {value}%")
        
        return measures
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de l'historique: {e}")
        return None

def diagnose_coverage_issue():
    """Diagnostic complet du problème de couverture"""
    print("\n" + "=" * 70)
    print("🔍 DIAGNOSTIC DU PROBLÈME DE COUVERTURE")
    print("=" * 70)
    
    # 1. Métriques actuelles
    metrics = get_project_measures()
    
    if not metrics:
        print("\n❌ Impossible de récupérer les métriques")
        return
    
    # 2. Analyses récentes
    analyses = get_project_analyses()
    
    # 3. Historique de couverture
    history = get_coverage_history()
    
    # 4. Diagnostic
    print("\n" + "=" * 70)
    print("💡 DIAGNOSTIC")
    print("=" * 70)
    
    current_coverage = float(metrics.get('coverage', 0))
    expected_coverage = 80.0
    
    print(f"\n📊 Couverture actuelle: {current_coverage}%")
    print(f"🎯 Couverture attendue: {expected_coverage}%")
    print(f"📉 Écart: {expected_coverage - current_coverage:.1f} points")
    
    if current_coverage < 70:
        print("\n⚠️  PROBLÈME IDENTIFIÉ:")
        print("   La couverture est toujours à l'ancien niveau (~67.7%)")
        print("\n🔍 Causes possibles:")
        print("   1. ❌ Le workflow GitHub Actions n'a pas encore tourné")
        print("   2. ❌ Le workflow est en cours d'exécution")
        print("   3. ❌ Les tests échouent dans le CI (Python 3.13 non disponible)")
        print("   4. ❌ Le coverage.xml n'a pas été généré correctement")
        print("   5. ❌ Le coverage.xml n'a pas été envoyé à SonarCloud")
        
        print("\n✅ Actions recommandées:")
        print("   1. Vérifier GitHub Actions:")
        print("      https://github.com/ericfunman/Consultator/actions")
        print("   2. Chercher le workflow avec commit 1e8ff2a")
        print("   3. Vérifier les logs du step 'Run tests with coverage'")
        print("   4. Vérifier que Python 3.13 est bien utilisé")
        
        if analyses and len(analyses) > 0:
            last_analysis = analyses[0]
            last_commit = last_analysis.get('revision', 'N/A')[:8]
            print(f"\n   Dernier commit analysé: {last_commit}")
            print(f"   Commit attendu: 1e8ff2a")
            
            if last_commit != "1e8ff2a":
                print(f"\n   ⚠️  Le commit 1e8ff2a n'a pas encore été analysé par SonarCloud!")
    
    elif current_coverage >= 78:
        print("\n✅ SUCCÈS: La couverture a été mise à jour!")
        print("   Le workflow GitHub Actions a fonctionné correctement.")
    
    else:
        print("\n⚠️  COUVERTURE PARTIELLE:")
        print("   La couverture a augmenté mais n'atteint pas encore 80%")
        print("   Certains tests peuvent encore échouer dans le CI")

if __name__ == "__main__":
    print("🔍 ANALYSE SONARCLOUD - CONSULTATOR")
    print("=" * 70)
    print(f"Projet: {PROJECT_KEY}")
    print(f"URL: https://sonarcloud.io/project/overview?id={PROJECT_KEY}")
    print("=" * 70)
    
    diagnose_coverage_issue()
    
    print("\n" + "=" * 70)
    print("✅ Analyse terminée")
    print("=" * 70)
