"""
Workflow d'amélioration continue de la couverture de tests

Ce script coordonne tous les outils d'amélioration de la couverture
pour un processus d'amélioration continue efficace.
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class ContinuousImprovementWorkflow:
    def __init__(self):
        self.start_time = datetime.now()
        self.project_root = Path.cwd()
        self.reports_dir = self.project_root / 'reports'
        self.target_coverage = 80.0
        self.minimum_improvement = 2.0  # Amélioration minimale par cycle
        
    def log(self, message: str, level: str = "INFO"):
        """Logger simple avec timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        prefix_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "STEP": "🔸"
        }
        prefix = prefix_map.get(level, "📝")
        print(f"[{timestamp}] {prefix} {message}")
        
    def get_current_coverage(self) -> float:
        """Récupère la couverture actuelle"""
        self.log("Analyse de la couverture actuelle...", "STEP")
        
        try:
            # Exécute les tests avec couverture
            result = subprocess.run([
                sys.executable, '-m', 'pytest',
                '--cov=app',
                '--cov-report=json:coverage.json',
                '--cov-report=term-missing',
                '--quiet',
                'tests/'
            ], capture_output=True, text=True, check=False)
            
            # Lit le fichier JSON
            if Path('coverage.json').exists():
                with open('coverage.json', 'r') as f:
                    coverage_data = json.load(f)
                    return coverage_data.get('totals', {}).get('percent_covered', 0.0)
            
            return 0.0
            
        except Exception as e:
            self.log(f"Erreur lors de l'analyse de couverture: {e}", "ERROR")
            return 0.0
    
    def generate_improvement_plan(self) -> bool:
        """Génère le plan d'amélioration"""
        self.log("Génération du plan d'amélioration...", "STEP")
        
        try:
            result = subprocess.run([
                sys.executable, 'scripts/improve_coverage.py'
            ], check=True, capture_output=True, text=True)
            
            self.log("Plan d'amélioration généré", "SUCCESS")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"Erreur génération du plan: {e}", "ERROR")
            return False
    
    def generate_auto_tests(self) -> bool:
        """Génère les tests automatiques"""
        self.log("Génération des tests automatiques...", "STEP")
        
        try:
            result = subprocess.run([
                sys.executable, 'scripts/auto_test_generator.py'
            ], check=True, capture_output=True, text=True)
            
            self.log("Tests automatiques générés", "SUCCESS")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"Erreur génération des tests: {e}", "ERROR")
            return False
    
    def prioritize_test_development(self) -> List[str]:
        """Identifie les fichiers prioritaires pour le développement de tests"""
        self.log("Identification des priorités...", "STEP")
        
        # Fichiers critiques du système
        critical_files = [
            'app/services/consultant_service.py',
            'app/services/mission_service.py', 
            'app/services/competence_service.py',
            'app/database/models.py',
            'import_vsa_missions_complet.py',
            'app/pages_modules/consultant_info.py'
        ]
        
        priorities = []
        
        # Vérifie quels fichiers critiques ont une faible couverture
        try:
            if Path('coverage.json').exists():
                with open('coverage.json', 'r') as f:
                    coverage_data = json.load(f)
                    files = coverage_data.get('files', {})
                
                for file_path in critical_files:
                    normalized_path = file_path.replace('/', '\\')  # Windows
                    alt_path = file_path.replace('\\', '/')  # Unix
                    
                    file_data = files.get(normalized_path) or files.get(alt_path)
                    if file_data:
                        coverage = file_data.get('summary', {}).get('percent_covered', 0)
                        if coverage < 70:  # Priorité haute si < 70%
                            priorities.append({
                                'file': file_path,
                                'coverage': coverage,
                                'priority': 'CRITIQUE' if coverage < 50 else 'HAUTE'
                            })
        
        except Exception as e:
            self.log(f"Erreur analyse des priorités: {e}", "WARNING")
        
        if priorities:
            self.log(f"Identifiés {len(priorities)} fichiers prioritaires", "SUCCESS")
            for p in priorities[:3]:
                self.log(f"  {p['priority']}: {p['file']} ({p['coverage']:.1f}%)")
        else:
            self.log("Aucun fichier critique identifié", "INFO")
        
        return [p['file'] for p in priorities]
    
    def create_focused_test_session(self, priority_files: List[str]):
        """Crée une session de tests ciblée"""
        if not priority_files:
            return
            
        self.log(f"Création de session de tests pour {len(priority_files)} fichiers", "STEP")
        
        # Crée un plan de session
        session_plan = f"""
# 🎯 Session de tests ciblée - {self.start_time.strftime('%Y-%m-%d %H:%M')}

## Objectif
Améliorer la couverture des fichiers les plus critiques du système.

## Fichiers prioritaires
"""
        
        for i, file in enumerate(priority_files[:5], 1):
            session_plan += f"{i}. `{file}`\n"
        
        session_plan += """
## Plan d'action
1. **Réviser les tests existants** pour ces fichiers
2. **Implémenter les tests manquants** selon les templates générés
3. **Valider la couverture** après chaque fichier
4. **Tester l'intégration** entre les composants

## Commandes utiles
```bash
# Tests ciblés pour un fichier
python -m pytest tests/ -k "consultant_service" --cov=app/services/consultant_service.py

# Couverture d'un module spécifique
python -m pytest tests/ --cov=app/services --cov-report=html

# Tests de régression après modifications
python -m pytest tests/regression/ -v
```

## Critères de succès
- [ ] Couverture > 80% pour chaque fichier prioritaire
- [ ] Tous les tests passent
- [ ] Tests de régression OK
- [ ] Documentation des tests mise à jour
"""
        
        # Sauvegarde le plan de session
        session_file = self.reports_dir / f'test_session_{self.start_time.strftime("%Y%m%d_%H%M")}.md'
        self.reports_dir.mkdir(exist_ok=True)
        
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write(session_plan)
        
        self.log(f"Plan de session créé: {session_file}", "SUCCESS")
    
    def run_regression_validation(self) -> bool:
        """Exécute une validation de régression"""
        self.log("Validation de régression...", "STEP")
        
        try:
            # Tests de régression existants
            result = subprocess.run([
                sys.executable, '-m', 'pytest',
                'tests/regression/',
                '-v', '--tb=short'
            ], check=True, capture_output=True, text=True)
            
            self.log("Tests de régression OK", "SUCCESS")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log("Échec des tests de régression", "WARNING")
            self.log("Vérifiez les tests avant de continuer", "WARNING")
            return False
    
    def generate_progress_report(self, initial_coverage: float, final_coverage: float):
        """Génère un rapport de progression"""
        improvement = final_coverage - initial_coverage
        duration = datetime.now() - self.start_time
        
        report = f"""
# 📈 Rapport d'amélioration de couverture

## Résumé
- **Date**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
- **Durée**: {str(duration).split('.')[0]}
- **Couverture initiale**: {initial_coverage:.1f}%
- **Couverture finale**: {final_coverage:.1f}%
- **Amélioration**: {improvement:+.1f}%

## État
"""
        
        if final_coverage >= self.target_coverage:
            report += f"🎯 **OBJECTIF ATTEINT** - Couverture cible de {self.target_coverage}% dépassée !\n"
        elif improvement >= self.minimum_improvement:
            report += f"✅ **PROGRESSION SATISFAISANTE** - Amélioration de {improvement:.1f}%\n"
        else:
            report += f"⚠️ **AMÉLIORATION INSUFFISANTE** - Seulement {improvement:.1f}% d'amélioration\n"
        
        report += f"""
## Prochaines étapes recommandées
"""
        
        if final_coverage < 50:
            report += "1. **Focus sur les tests unitaires** - Priorité aux services et modèles\n"
            report += "2. **Utiliser les templates générés** - Adapter selon la logique métier\n"
        elif final_coverage < 70:
            report += "1. **Tests d'intégration** - Workflows complets\n"
            report += "2. **Tests de pages** - Interfaces utilisateur\n"
        else:
            report += "1. **Optimisation des tests** - Suppression de la redondance\n"
            report += "2. **Tests de performance** - Validation des temps de réponse\n"
        
        report += """
## Commandes de suivi
```bash
# Analyse de couverture détaillée
python scripts/improve_coverage.py

# Génération de nouveaux tests
python scripts/auto_test_generator.py

# Validation complète
python -m pytest tests/ --cov=app --cov-report=html
```
"""
        
        # Sauvegarde le rapport
        report_file = self.reports_dir / f'improvement_report_{self.start_time.strftime("%Y%m%d_%H%M")}.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.log(f"Rapport de progression: {report_file}", "SUCCESS")
    
    def run_complete_workflow(self):
        """Exécute le workflow complet d'amélioration"""
        self.log("🚀 DÉBUT DU WORKFLOW D'AMÉLIORATION CONTINUE", "STEP")
        self.log(f"Objectif: {self.target_coverage}% de couverture", "INFO")
        
        # 1. État initial
        initial_coverage = self.get_current_coverage()
        self.log(f"Couverture initiale: {initial_coverage:.1f}%", "INFO")
        
        if initial_coverage >= self.target_coverage:
            self.log(f"Objectif déjà atteint ! ({initial_coverage:.1f}%)", "SUCCESS")
            return
        
        # 2. Plan d'amélioration
        if not self.generate_improvement_plan():
            self.log("Échec génération du plan", "ERROR")
            return
        
        # 3. Tests automatiques
        if not self.generate_auto_tests():
            self.log("Échec génération des tests", "ERROR")
            return
        
        # 4. Priorités
        priority_files = self.prioritize_test_development()
        self.create_focused_test_session(priority_files)
        
        # 5. Validation
        self.run_regression_validation()
        
        # 6. État final
        final_coverage = self.get_current_coverage()
        self.log(f"Couverture finale: {final_coverage:.1f}%", "INFO")
        
        # 7. Rapport
        self.generate_progress_report(initial_coverage, final_coverage)
        
        # Conclusion
        improvement = final_coverage - initial_coverage
        duration = datetime.now() - self.start_time
        
        self.log("", "INFO")  # Ligne vide
        self.log("="*60, "INFO")
        self.log("✅ WORKFLOW TERMINÉ", "SUCCESS")
        self.log("="*60, "INFO")
        self.log(f"⏱️ Durée: {str(duration).split('.')[0]}", "INFO")
        self.log(f"📈 Amélioration: {improvement:+.1f}% ({initial_coverage:.1f}% → {final_coverage:.1f}%)", "INFO")
        
        if improvement >= self.minimum_improvement:
            self.log("🎉 Objectif d'amélioration atteint !", "SUCCESS")
        else:
            self.log(f"⚠️ Amélioration insuffisante (minimum: {self.minimum_improvement}%)", "WARNING")
            self.log("Consultez le plan de session pour continuer", "INFO")


def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Workflow d\'amélioration continue des tests')
    parser.add_argument('--target', type=float, default=80.0, help='Couverture cible (défaut: 80%%)')
    parser.add_argument('--min-improvement', type=float, default=2.0, help='Amélioration minimale par cycle (défaut: 2%%)')
    parser.add_argument('--quick', action='store_true', help='Mode rapide (analyse seulement)')
    
    args = parser.parse_args()
    
    workflow = ContinuousImprovementWorkflow()
    workflow.target_coverage = args.target
    workflow.minimum_improvement = args.min_improvement
    
    if args.quick:
        # Mode rapide - analyse seulement
        current_coverage = workflow.get_current_coverage()
        workflow.log(f"Couverture actuelle: {current_coverage:.1f}%", "INFO")
        workflow.log(f"Objectif: {args.target}%", "INFO")
        remaining = args.target - current_coverage
        workflow.log(f"Reste à améliorer: {remaining:.1f}%", "INFO")
    else:
        # Workflow complet
        workflow.run_complete_workflow()


if __name__ == '__main__':
    main()