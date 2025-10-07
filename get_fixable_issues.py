"""
Script pour récupérer les détails des 10 issues non-S5914
"""
import requests
import json

SONAR_TOKEN = "dc9f7acde5993776f1823d2084864bd610bc9e2b"
PROJECT_KEY = "ericfunman_Consultator"
BASE_URL = "https://sonarcloud.io/api"

def get_non_s5914_issues():
    """Récupère les issues qui ne sont pas S5914 (assert True)"""
    url = f"{BASE_URL}/issues/search"
    params = {
        "componentKeys": PROJECT_KEY,
        "ps": 500,
        "resolved": "false"
    }
    
    headers = {"Authorization": f"Bearer {SONAR_TOKEN}"}
    
    try:
        response = requests.get(url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        
        issues = data.get('issues', [])
        
        # Filtrer les non-S5914
        non_s5914 = [i for i in issues if i.get('rule', '') != 'python:S5914']
        
        print(f"Issues non-S5914: {len(non_s5914)}\n")
        
        for issue in non_s5914:
            rule = issue.get('rule', '')
            component = issue.get('component', '').replace(f'{PROJECT_KEY}:', '')
            line = issue.get('line', '?')
            message = issue.get('message', '')
            
            print(f"Rule: {rule}")
            print(f"File: {component}:{line}")
            print(f"Message: {message}")
            print("-" * 80)
        
        return non_s5914
    except Exception as e:
        print(f"Erreur: {e}")
        return []

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("Issues SonarCloud à corriger (hors S5914)\n" + "=" * 80)
    issues = get_non_s5914_issues()
    print(f"\nTOTAL: {len(issues)} issues à corriger")
