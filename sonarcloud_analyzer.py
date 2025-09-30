#!/usr/bin/env python3
"""
Script pour analyser les résultats SonarCloud du projet Consultator
Récupère les issues et les métriques de couverture de code
"""

import json
import sys
from typing import Dict, List, Any
import requests
from datetime import datetime

# Configuration SonarCloud
SONAR_TOKEN = "dc9f7acde5993776f1823d2084864bd610bc9e2b"  # ⚠️ À remplacer par votre token réel
PROJECT_KEY = "ericfunman_Consultator"
SONAR_URL = "https://sonarcloud.io/api"

class SonarCloudAnalyzer:
    """Analyseur des résultats SonarCloud"""

    def __init__(self, token: str, project_key: str):
        self.token = token
        self.project_key = project_key
        self.base_url = "https://sonarcloud.io/api"
        self.session = requests.Session()
        self.session.auth = (token, '')  # Token comme username, password vide

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict:
        """Fait une requête à l'API SonarCloud"""
        url = f"{self.base_url}/{endpoint}"
        try:
            # ⚠️ Désactivation temporaire de la vérification SSL pour contourner les problèmes de certificats
            # À utiliser avec précaution - ne pas faire en production
            response = self.session.get(url, params=params, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors de la requête {endpoint}: {e}")
            return {}

    def get_project_issues(self, limit: int = 100) -> List[Dict]:
        """Récupère les issues du projet"""
        print("🔍 Récupération des issues...")

        params = {
            'projectKeys': self.project_key,
            'ps': limit,  # Page size
            'p': 1,  # Page number
            'statuses': 'OPEN,CONFIRMED,REOPENED',
            'types': 'BUG,VULNERABILITY,CODE_SMELL',
            'severities': 'BLOCKER,CRITICAL,MAJOR,MINOR,INFO'
        }

        response = self._make_request('issues/search', params)

        issues = response.get('issues', [])
        total = response.get('total', 0)

        print(f"📊 {len(issues)} issues trouvées sur {total} total")

        return issues

    def get_coverage_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques de couverture"""
        print("📈 Récupération des métriques de couverture...")

        # Essayer d'abord avec l'endpoint measures/component
        params = {
            'component': self.project_key,
            'metricKeys': 'coverage,line_coverage,branch_coverage,duplicated_lines_density,ncloc'
        }

        response = self._make_request('measures/component', params)

        metrics = {}
        if 'component' in response and 'measures' in response['component']:
            for measure in response['component']['measures']:
                key = measure['metric']
                value = measure.get('value', 'N/A')
                metrics[key] = value

        # Si ça n'a pas marché, essayer avec measures/search
        if not metrics:
            params = {
                'projectKeys': self.project_key,
                'metricKeys': 'coverage,line_coverage,branch_coverage,duplicated_lines_density,ncloc'
            }
            response = self._make_request('measures/search', params)

            if 'measures' in response:
                for measure in response['measures']:
                    key = measure['metric']
                    value = measure.get('value', 'N/A')
                    metrics[key] = value

        return metrics

    def analyze_issues_by_type(self, issues: List[Dict]) -> Dict[str, int]:
        """Analyse les issues par type"""
        types_count = {}
        for issue in issues:
            issue_type = issue.get('type', 'UNKNOWN')
            types_count[issue_type] = types_count.get(issue_type, 0) + 1

        return types_count

    def analyze_issues_by_severity(self, issues: List[Dict]) -> Dict[str, int]:
        """Analyse les issues par sévérité"""
        severity_count = {}
        for issue in issues:
            severity = issue.get('severity', 'UNKNOWN')
            severity_count[severity] = severity_count.get(severity, 0) + 1

        return severity_count

    def get_top_issues(self, issues: List[Dict], limit: int = 10) -> List[Dict]:
        """Retourne les issues les plus importantes"""
        # Trier par sévérité (BLOCKER > CRITICAL > MAJOR > MINOR > INFO)
        severity_order = {'BLOCKER': 5, 'CRITICAL': 4, 'MAJOR': 3, 'MINOR': 2, 'INFO': 1}

        sorted_issues = sorted(
            issues,
            key=lambda x: severity_order.get(x.get('severity', 'UNKNOWN'), 0),
            reverse=True
        )

        return sorted_issues[:limit]

    def display_results(self):
        """Affiche tous les résultats"""
        print("\n" + "="*80)
        print("🎯 ANALYSE SONARCLOUD - PROJET CONSULTATOR")
        print("="*80)

        # Récupération des données
        issues = self.get_project_issues()
        metrics = self.get_coverage_metrics()

        # Métriques de couverture
        print(f"\n📊 MÉTRIQUES DE COUVERTURE")
        print("-" * 40)

        coverage = metrics.get('coverage', 'N/A')
        line_coverage = metrics.get('line_coverage', 'N/A')
        branch_coverage = metrics.get('branch_coverage', 'N/A')
        duplicated_lines = metrics.get('duplicated_lines_density', 'N/A')
        ncloc = metrics.get('ncloc', 'N/A')

        print(f"🔹 Couverture globale    : {coverage}%")
        print(f"🔹 Couverture de lignes  : {line_coverage}%")
        print(f"🔹 Couverture de branches: {branch_coverage}%")
        print(f"🔹 Lignes dupliquées    : {duplicated_lines}%")
        print(f"🔹 Lignes de code       : {ncloc}")

        # Analyse des issues
        if issues:
            print(f"\n🐛 ANALYSE DES ISSUES ({len(issues)})")
            print("-" * 40)

            # Par type
            types_count = self.analyze_issues_by_type(issues)
            print("📋 Répartition par type :")
            for issue_type, count in types_count.items():
                print(f"   • {issue_type}: {count}")

            # Par sévérité
            severity_count = self.analyze_issues_by_severity(issues)
            print("\n🚨 Répartition par sévérité :")
            for severity, count in severity_count.items():
                emoji = {'BLOCKER': '🔴', 'CRITICAL': '🟠', 'MAJOR': '🟡', 'MINOR': '🔵', 'INFO': '⚪'}.get(severity, '⚫')
                print(f"   {emoji} {severity}: {count}")

            # Top 10 issues
            print(f"\n🔥 TOP 10 ISSUES LES PLUS CRITIQUES")
            print("-" * 40)

            top_issues = self.get_top_issues(issues, 10)
            for i, issue in enumerate(top_issues, 1):
                severity = issue.get('severity', 'UNKNOWN')
                issue_type = issue.get('type', 'UNKNOWN')
                message = issue.get('message', 'No message')
                file_path = issue.get('component', 'Unknown file')
                line = issue.get('line', 'N/A')

                emoji = {'BLOCKER': '🔴', 'CRITICAL': '🟠', 'MAJOR': '🟡', 'MINOR': '🔵', 'INFO': '⚪'}.get(severity, '⚫')

                print(f"{i}. {emoji} [{severity}] {issue_type}")
                print(f"   📁 {file_path}:{line}")
                print(f"   💬 {message[:100]}{'...' if len(message) > 100 else ''}")
                print()

        else:
            print("\n✅ AUCUNE ISSUE TROUVÉE")
            print("🎉 Félicitations ! Votre code est propre selon SonarCloud.")

        print("\n" + "="*80)
        print(f"📅 Analyse effectuée le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
        print("="*80)


def main():
    """Fonction principale"""
    print("🚀 Démarrage de l'analyse SonarCloud...")

    # Vérification du token
    if not SONAR_TOKEN or SONAR_TOKEN == "YOUR_TOKEN_HERE":
        print("❌ Erreur: Token SonarCloud non configuré!")
        print("Modifiez la variable SONAR_TOKEN dans le script.")
        sys.exit(1)

    # Création de l'analyseur
    analyzer = SonarCloudAnalyzer(SONAR_TOKEN, PROJECT_KEY)

    # Affichage des résultats
    analyzer.display_results()


if __name__ == "__main__":
    main()