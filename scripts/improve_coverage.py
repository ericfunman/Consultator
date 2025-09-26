"""
Strategy d'amélioration systématique de la couverture de tests

Ce script analyse la couverture de tests actuelle et propose un plan
d'amélioration ciblé avec priorités.
"""

import subprocess
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class CoverageAnalyzer:
    def __init__(self):
        self.coverage_data = {}
        self.uncovered_files = []
        self.critical_files = [
            'app/services/consultant_service.py',
            'app/services/mission_service.py',
            'app/services/competence_service.py',
            'app/database/models.py',
            'app/pages/gestion_consultants.py',
            'app/pages/gestion_missions.py',
            'import_vsa_missions_complet.py'
        ]

    def run_coverage_analysis(self) -> Dict:
        """Exécute une analyse complète de couverture"""
        print("🔍 Analyse de couverture en cours...")
        
        try:
            # Génère le rapport de couverture JSON
            result = subprocess.run([
                sys.executable, '-m', 'pytest',
                '--cov=app',
                '--cov-report=json:coverage.json',
                '--cov-report=term-missing',
                '--cov-fail-under=0',  # Ne pas échouer sur la couverture faible
                'tests/'
            ], capture_output=True, text=True, check=False)
            
            # Lit les données de couverture
            if Path('coverage.json').exists():
                with open('coverage.json', 'r') as f:
                    self.coverage_data = json.load(f)
            
            return self.analyze_coverage_gaps()
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse : {e}")
            return {}

    def analyze_coverage_gaps(self) -> Dict:
        """Analyse les lacunes de couverture par priorité"""
        analysis = {
            'summary': {
                'total_coverage': 0,
                'files_analyzed': 0,
                'critical_files_coverage': 0
            },
            'priorities': {
                'critical': [],
                'high': [],
                'medium': [],
                'low': []
            },
            'recommendations': []
        }
        
        if not self.coverage_data:
            return analysis
        
        files = self.coverage_data.get('files', {})
        analysis['summary']['total_coverage'] = self.coverage_data.get('totals', {}).get('percent_covered', 0)
        analysis['summary']['files_analyzed'] = len(files)
        
        # Analyse par fichier
        for file_path, file_data in files.items():
            coverage = file_data.get('summary', {}).get('percent_covered', 0)
            missing_lines = file_data.get('missing_lines', [])
            
            file_info = {
                'file': file_path,
                'coverage': coverage,
                'missing_lines': len(missing_lines),
                'missing_line_numbers': missing_lines[:10]  # Limite à 10 lignes
            }
            
            # Catégorisation par priorité
            if file_path in self.critical_files:
                if coverage < 70:
                    analysis['priorities']['critical'].append(file_info)
                elif coverage < 90:
                    analysis['priorities']['high'].append(file_info)
            elif 'service' in file_path.lower():
                if coverage < 80:
                    analysis['priorities']['high'].append(file_info)
                else:
                    analysis['priorities']['medium'].append(file_info)
            elif 'pages' in file_path.lower():
                if coverage < 60:
                    analysis['priorities']['medium'].append(file_info)
                else:
                    analysis['priorities']['low'].append(file_info)
            else:
                if coverage < 50:
                    analysis['priorities']['medium'].append(file_info)
                else:
                    analysis['priorities']['low'].append(file_info)
        
        # Calcul de la couverture des fichiers critiques
        critical_coverages = [
            files.get(f, {}).get('summary', {}).get('percent_covered', 0)
            for f in self.critical_files if f in files
        ]
        if critical_coverages:
            analysis['summary']['critical_files_coverage'] = sum(critical_coverages) / len(critical_coverages)
        
        # Génération de recommandations
        analysis['recommendations'] = self.generate_recommendations(analysis)
        
        return analysis

    def generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Génère des recommandations d'amélioration"""
        recommendations = []
        
        # Recommandations critiques
        if analysis['priorities']['critical']:
            recommendations.append({
                'priority': 'CRITIQUE',
                'title': 'Fichiers critiques sous-testés',
                'description': f"{len(analysis['priorities']['critical'])} fichiers critiques ont moins de 70% de couverture",
                'action': 'Créer des tests complets pour ces fichiers immédiatement',
                'files': [f['file'] for f in analysis['priorities']['critical'][:5]]
            })
        
        # Recommandations services
        high_priority_services = [
            f for f in analysis['priorities']['high'] 
            if 'service' in f['file'].lower()
        ]
        if high_priority_services:
            recommendations.append({
                'priority': 'HAUTE',
                'title': 'Services métier insuffisamment testés',
                'description': f"{len(high_priority_services)} services ont moins de 80% de couverture",
                'action': 'Implémenter des tests unitaires et d\'intégration',
                'files': [f['file'] for f in high_priority_services[:3]]
            })
        
        # Recommandations pages
        medium_priority_pages = [
            f for f in analysis['priorities']['medium'] 
            if 'pages' in f['file'].lower()
        ]
        if medium_priority_pages:
            recommendations.append({
                'priority': 'MOYENNE',
                'title': 'Interfaces utilisateur partiellement testées',
                'description': f"{len(medium_priority_pages)} pages ont moins de 60% de couverture",
                'action': 'Développer des tests UI et de workflow',
                'files': [f['file'] for f in medium_priority_pages[:3]]
            })
        
        # Recommandation générale
        if analysis['summary']['total_coverage'] < 50:
            recommendations.append({
                'priority': 'GÉNÉRALE',
                'title': 'Couverture globale insuffisante',
                'description': f"Couverture globale de {analysis['summary']['total_coverage']:.1f}% (objectif: 80%)",
                'action': 'Plan d\'amélioration progressive sur 4 sprints',
                'files': []
            })
        
        return recommendations

    def generate_test_plan(self, analysis: Dict) -> str:
        """Génère un plan de tests structuré"""
        plan = """
# 📋 Plan d'amélioration de la couverture de tests

## 📊 État actuel
- **Couverture globale**: {total_coverage:.1f}%
- **Fichiers analysés**: {files_analyzed}
- **Couverture fichiers critiques**: {critical_coverage:.1f}%

## 🎯 Objectifs
- **Sprint 1**: Atteindre 50% de couverture globale
- **Sprint 2**: Atteindre 65% de couverture globale  
- **Sprint 3**: Atteindre 80% de couverture globale
- **Sprint 4**: Optimisation et stabilisation

## ⚡ Actions prioritaires

### 🔴 Critique (À faire immédiatement)
""".format(
            total_coverage=analysis['summary']['total_coverage'],
            files_analyzed=analysis['summary']['files_analyzed'],
            critical_coverage=analysis['summary']['critical_files_coverage']
        )
        
        for item in analysis['priorities']['critical'][:3]:
            plan += f"- **{item['file']}** ({item['coverage']:.1f}% couverture)\n"
            plan += f"  - {item['missing_lines']} lignes non testées\n"
            plan += f"  - Lignes: {item['missing_line_numbers']}\n\n"
        
        plan += """
### 🟡 Haute priorité (Sprint 1-2)
"""
        for item in analysis['priorities']['high'][:3]:
            plan += f"- **{item['file']}** ({item['coverage']:.1f}% couverture)\n"
        
        plan += """
### 🟢 Priorité moyenne (Sprint 2-3)
"""
        for item in analysis['priorities']['medium'][:3]:
            plan += f"- **{item['file']}** ({item['coverage']:.1f}% couverture)\n"
        
        plan += """
## 🛠️ Stratégies de tests recommandées

### Pour les services (app/services/)
```python
# Tests unitaires avec mocking
def test_service_method_success():
    # Given
    mock_data = create_mock_data()
    
    # When  
    result = service.method(mock_data)
    
    # Then
    assert result.is_success
    assert len(result.data) > 0

# Tests d'intégration avec base de données
def test_service_integration():
    # Given
    db_session = create_test_session()
    
    # When
    result = service.create_entity(valid_data)
    
    # Then
    assert result.id is not None
    db_session.rollback()
```

### Pour les pages (app/pages/)
```python
# Tests de workflow utilisateur
def test_page_workflow():
    # Simulate user input
    with patch('streamlit.form_submit_button', return_value=True):
        result = page.process_form(test_data)
        assert result.success

# Tests des composants UI
def test_ui_components():
    with patch('streamlit.columns') as mock_columns:
        page.show_data_table(test_data)
        mock_columns.assert_called()
```

## 📈 Métriques de suivi
- Couverture par catégorie de fichiers
- Nombre de tests par module  
- Temps d'exécution des tests
- Ratio tests/code de production

## 🔄 Processus d'amélioration continue
1. **Analyse hebdomadaire** de la couverture
2. **Tests de régression** automatiques à chaque commit
3. **Revue de code** incluant la validation des tests
4. **Refactoring** des tests obsolètes ou redondants
"""
        
        return plan

    def create_test_templates(self, analysis: Dict):
        """Crée des templates de tests pour les fichiers prioritaires"""
        templates_dir = Path('tests/templates')
        templates_dir.mkdir(exist_ok=True)
        
        # Template pour services
        service_template = '''"""
Tests pour {filename}
Généré automatiquement - À adapter selon les besoins
"""

import pytest
from unittest.mock import Mock, patch
from {import_path} import {class_name}


class Test{class_name}:
    """Tests unitaires pour {class_name}"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.service = {class_name}()
        
    def test_init(self):
        """Test d'initialisation"""
        assert self.service is not None
        
    # TODO: Ajouter les tests spécifiques aux méthodes
    
    @pytest.mark.parametrize("input_data,expected", [
        ({"valid": True}, True),
        ({"valid": False}, False),
    ])
    def test_validation(self, input_data, expected):
        """Tests paramétrés de validation"""
        # TODO: Implémenter selon la logique métier
        pass
        
    def test_error_handling(self):
        """Test de gestion d'erreurs"""  
        # TODO: Tester les cas d'erreur
        pass

    @patch('app.database.get_session')
    def test_database_interaction(self, mock_session):
        """Test d'interaction avec la base de données"""
        # TODO: Tester les opérations DB
        pass
'''

        # Génère des templates pour les fichiers critiques
        for item in analysis['priorities']['critical'][:3]:
            file_path = item['file']
            if 'service' in file_path.lower():
                # Extrait le nom de classe du fichier
                filename = Path(file_path).stem
                class_name = ''.join(word.capitalize() for word in filename.split('_'))
                import_path = file_path.replace('/', '.').replace('.py', '')
                
                template_content = service_template.format(
                    filename=filename,
                    class_name=class_name,
                    import_path=import_path
                )
                
                template_file = templates_dir / f'test_{filename}_template.py'
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                
                print(f"📝 Template créé : {template_file}")

    def print_analysis_report(self, analysis: Dict):
        """Affiche un rapport d'analyse détaillé"""
        print("\n" + "="*60)
        print("📊 RAPPORT D'ANALYSE DE COUVERTURE")
        print("="*60)
        
        # Résumé
        summary = analysis['summary']
        print(f"\n📈 RÉSUMÉ:")
        print(f"  Couverture globale: {summary['total_coverage']:.1f}%")
        print(f"  Fichiers analysés: {summary['files_analyzed']}")
        print(f"  Couverture fichiers critiques: {summary['critical_files_coverage']:.1f}%")
        
        # Priorités
        priorities = analysis['priorities']
        print(f"\n⚡ PRIORITÉS:")
        print(f"  🔴 Critique: {len(priorities['critical'])} fichiers")
        print(f"  🟡 Haute: {len(priorities['high'])} fichiers") 
        print(f"  🟢 Moyenne: {len(priorities['medium'])} fichiers")
        print(f"  🔵 Faible: {len(priorities['low'])} fichiers")
        
        # Top 5 des fichiers critiques
        if priorities['critical']:
            print(f"\n🚨 TOP 5 FICHIERS CRITIQUES:")
            for i, item in enumerate(priorities['critical'][:5], 1):
                print(f"  {i}. {item['file']} - {item['coverage']:.1f}% ({item['missing_lines']} lignes)")
        
        # Recommandations
        if analysis['recommendations']:
            print(f"\n💡 RECOMMANDATIONS:")
            for i, rec in enumerate(analysis['recommendations'], 1):
                print(f"  {i}. [{rec['priority']}] {rec['title']}")
                print(f"     {rec['description']}")
                if rec['files']:
                    print(f"     Fichiers: {', '.join(rec['files'][:2])}...")
                print()


def main():
    """Fonction principale d'amélioration de couverture"""
    print("🚀 SYSTÈME D'AMÉLIORATION DE COUVERTURE DE TESTS")
    print("="*50)
    
    analyzer = CoverageAnalyzer()
    
    # Analyse la couverture
    analysis = analyzer.run_coverage_analysis()
    
    if not analysis:
        print("❌ Impossible d'analyser la couverture")
        return
    
    # Affiche le rapport
    analyzer.print_analysis_report(analysis)
    
    # Génère le plan d'amélioration
    test_plan = analyzer.generate_test_plan(analysis)
    
    # Sauvegarde le plan
    plan_file = Path('TEST_IMPROVEMENT_PLAN.md')
    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write(test_plan)
    
    print(f"📋 Plan d'amélioration sauvegardé : {plan_file}")
    
    # Crée les templates de tests
    analyzer.create_test_templates(analysis)
    
    print("\n✅ Analyse terminée. Consultez TEST_IMPROVEMENT_PLAN.md pour les prochaines étapes.")


if __name__ == '__main__':
    main()