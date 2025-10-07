"""Script pour récupérer toutes les issues S5914 de SonarCloud."""
import requests
import os

SONAR_TOKEN = os.getenv("SONAR_TOKEN", "sqp_ba1f35dcda47d2a5f8f4ec34c8dda8dff4d53b5b")
PROJECT_KEY = "ericfunman_Consultator"
SONAR_URL = "https://sonarcloud.io"

def get_s5914_issues():
    """Récupère toutes les issues S5914."""
    url = f"{SONAR_URL}/api/issues/search"
    
    all_issues = []
    page = 1
    
    while True:
        params = {
            "componentKeys": PROJECT_KEY,
            "rules": "python:S5914",
            "statuses": "OPEN,CONFIRMED,REOPENED",
            "ps": 100,  # 100 issues par page
            "p": page
        }
        
        headers = {
            "Authorization": f"Bearer {SONAR_TOKEN}"
        }
        
        response = requests.get(url, params=params, headers=headers, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            issues = data.get("issues", [])
            all_issues.extend(issues)
            
            total = data.get("total", 0)
            print(f"Page {page}: {len(issues)} issues récupérées (total: {len(all_issues)}/{total})")
            
            # Si on a tout récupéré, on arrête
            if len(all_issues) >= total:
                break
                
            page += 1
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            break
    
    return all_issues

def analyze_issues(issues):
    """Analyse les issues S5914."""
    print("\n" + "="*80)
    print(f"ANALYSE DES {len(issues)} ISSUES S5914")
    print("="*80)
    
    # Grouper par fichier
    by_file = {}
    for issue in issues:
        component = issue.get("component", "")
        file_path = component.replace(f"{PROJECT_KEY}:", "")
        
        if file_path not in by_file:
            by_file[file_path] = []
        
        by_file[file_path].append({
            "line": issue.get("line", "?"),
            "message": issue.get("message", ""),
            "code": issue.get("textRange", {})
        })
    
    # Afficher par fichier
    for file_path in sorted(by_file.keys()):
        print(f"\n📄 {file_path} ({len(by_file[file_path])} issues)")
        print("-" * 80)
        for idx, issue in enumerate(by_file[file_path], 1):
            print(f"  {idx}. Line {issue['line']}: {issue['message']}")
    
    print("\n" + "="*80)
    print(f"TOTAL: {len(issues)} issues S5914 dans {len(by_file)} fichiers")
    print("="*80)
    
    return by_file

if __name__ == "__main__":
    print("🔍 Récupération des issues S5914...")
    issues = get_s5914_issues()
    
    if issues:
        by_file = analyze_issues(issues)
        
        # Sauvegarder dans un fichier
        with open("s5914_issues_details.txt", "w", encoding="utf-8") as f:
            f.write(f"ISSUES S5914 - {len(issues)} au total\n")
            f.write("="*80 + "\n\n")
            
            for file_path in sorted(by_file.keys()):
                f.write(f"\n{file_path} ({len(by_file[file_path])} issues)\n")
                f.write("-" * 80 + "\n")
                for idx, issue in enumerate(by_file[file_path], 1):
                    f.write(f"  Line {issue['line']}: {issue['message']}\n")
        
        print(f"\n✅ Détails sauvegardés dans s5914_issues_details.txt")
    else:
        print("❌ Aucune issue récupérée")
