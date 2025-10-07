"""
Script simple pour récupérer le compte exact d'issues SonarCloud
"""
import requests
import json

# Configuration
SONAR_TOKEN = "dc9f7acde5993776f1823d2084864bd610bc9e2b"
PROJECT_KEY = "ericfunman_Consultator"
BASE_URL = "https://sonarcloud.io/api"

def get_issues_count():
    """Récupère le nombre total d'issues"""
    url = f"{BASE_URL}/issues/search"
    params = {
        "componentKeys": PROJECT_KEY,
        "ps": 1,  # Une seule issue pour avoir le total
        "resolved": "false"
    }
    
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        
        total = data.get('total', 0)
        paging = data.get('paging', {})
        
        print("Issues SonarCloud:")
        print(f"  Total: {total}")
        print(f"  Page size: {paging.get('pageSize', 0)}")
        print(f"  Page index: {paging.get('pageIndex', 0)}")
        
        return total
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def get_issues_by_type():
    """Récupère la répartition des issues par type"""
    url = f"{BASE_URL}/issues/search"
    params = {
        "componentKeys": PROJECT_KEY,
        "ps": 500,  # Maximum
        "resolved": "false"
    }
    
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        
        issues = data.get('issues', [])
        
        # Compter par rule
        rules = {}
        for issue in issues:
            rule = issue.get('rule', 'Unknown')
            message = issue.get('message', '')
            if rule not in rules:
                rules[rule] = {'count': 0, 'example': message}
            rules[rule]['count'] += 1
        
        print(f"\nRepartition par rule ({len(issues)} issues):")
        for rule, info in sorted(rules.items(), key=lambda x: x[1]['count'], reverse=True):
            print(f"  {rule}: {info['count']} issues")
            print(f"    Exemple: {info['example'][:80]}...")
        
        return rules
    except Exception as e:
        print(f"Erreur: {e}")
        return None

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("Analyse SonarCloud\n" + "=" * 60)
    
    total = get_issues_count()
    print("\n" + "-" * 60)
    rules = get_issues_by_type()
    
    print("\n" + "=" * 60)
    if total:
        print(f"TOTAL: {total} issues restantes")
