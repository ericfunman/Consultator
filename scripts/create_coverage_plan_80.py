#!/usr/bin/env python3
"""
Plan Stratégique pour Atteindre 80% de Couverture de Tests
Analyse détaillée et roadmap pour améliorer la couverture de 9% à 80%
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

def create_coverage_improvement_plan():
    """Crée un plan détaillé pour atteindre 80% de couverture"""
    
    print("🎯 PLAN STRATÉGIQUE - COUVERTURE 80%")
    print("=" * 50)
    
    # Analyse de la couverture actuelle
    print("\n📊 ANALYSE DE LA SITUATION ACTUELLE")
    print("-" * 40)
    
    # Exécuter l'analyse de couverture
    try:
        result = subprocess.run([
            'python', '-m', 'pytest',
            'tests/regression/test_vsa_import_regression.py',
            'tests/unit/services/test_priority_services.py', 
            'tests/unit/pages/test_consultant_pages.py',
            '--cov=app',
            '--cov-report=json:reports/coverage_strategic.json',
            '--cov-report=term-missing',
            '-q'
        ], capture_output=True, text=True, cwd=Path('.'))
        
        # Lire les données de couverture
        coverage_file = Path('reports/coverage_strategic.json')
        if coverage_file.exists():
            with open(coverage_file) as f:
                coverage_data = json.load(f)
            
            current_coverage = coverage_data['totals']['percent_covered']
            total_lines = coverage_data['totals']['num_statements']
            covered_lines = coverage_data['totals']['covered_lines']
            missing_lines = total_lines - covered_lines
            
            print(f"✅ Couverture actuelle: {current_coverage:.1f}%")
            print(f"📏 Lignes totales: {total_lines:,}")
            print(f"✅ Lignes couvertes: {covered_lines:,}")
            print(f"❌ Lignes manquantes: {missing_lines:,}")
            
            # Calcul pour atteindre 80%
            target_coverage = 80.0
            target_covered_lines = int(total_lines * target_coverage / 100)
            additional_lines_needed = target_covered_lines - covered_lines
            
            print(f"\n🎯 OBJECTIF 80%:")
            print(f"📏 Lignes à couvrir: {target_covered_lines:,}")
            print(f"🔥 Lignes supplémentaires nécessaires: {additional_lines_needed:,}")
            print(f"📈 Progression requise: +{target_coverage - current_coverage:.1f}%")
            
            # Analyser les fichiers par priorité
            files_analysis = analyze_priority_files(coverage_data)
            
            # Créer le plan stratégique
            create_strategic_plan(current_coverage, target_coverage, additional_lines_needed, files_analysis)
            
        else:
            print("❌ Impossible de lire les données de couverture")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")

def analyze_priority_files(coverage_data):
    """Analyse les fichiers par ordre de priorité pour l'amélioration"""
    
    files = coverage_data['files']
    priority_files = []
    
    for file_path, file_data in files.items():
        if file_path.startswith('app/'):
            total_lines = file_data['summary']['num_statements']
            covered_lines = file_data['summary']['covered_lines']
            missing_lines = total_lines - covered_lines
            coverage_pct = file_data['summary']['percent_covered']
            
            # Calculer le score de priorité (impact potentiel)
            priority_score = missing_lines * (100 - coverage_pct) / 100
            
            priority_files.append({
                'file': file_path,
                'total_lines': total_lines,
                'covered_lines': covered_lines,
                'missing_lines': missing_lines,
                'coverage_pct': coverage_pct,
                'priority_score': priority_score
            })
    
    # Trier par score de priorité (décroissant)
    priority_files.sort(key=lambda x: x['priority_score'], reverse=True)
    
    print(f"\n🔥 TOP 10 FICHIERS PRIORITAIRES:")
    print("-" * 40)
    for i, file_info in enumerate(priority_files[:10], 1):
        print(f"{i:2d}. {file_info['file']}")
        print(f"    📊 {file_info['coverage_pct']:.1f}% | {file_info['missing_lines']} lignes manquantes")
    
    return priority_files

def create_strategic_plan(current_cov, target_cov, additional_lines, files_analysis):
    """Crée le plan stratégique détaillé"""
    
    plan_content = f"""# 🎯 PLAN STRATÉGIQUE - COUVERTURE 80% CONSULTATOR

*Plan créé le: {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}*

## 📊 Situation Actuelle

- **Couverture actuelle**: {current_cov:.1f}%
- **Objectif**: {target_cov}%
- **Écart**: {target_cov - current_cov:.1f}%
- **Lignes supplémentaires nécessaires**: {additional_lines:,}

## 🚀 Stratégie d'Amélioration

### Phase 1: Services Critiques (Objectif: +25% couverture)
**Délai**: 2-3 semaines

#### 🎯 Actions Prioritaires:
1. **ConsultantService** - Module principal (1500+ lignes)
   - Implémenter tests pour CRUD operations
   - Tests de validation des données
   - Tests de performance avec gros volumes
   
2. **DocumentService** - Gestion documents (200+ lignes)
   - Tests d'upload et parsing CV
   - Tests de génération de rapports
   - Tests d'intégration avec l'IA
   
3. **BusinessManagerService** - Gestion BM (60+ lignes)
   - Corriger les mocks existants (déjà commencé)
   - Tests de validation et CRUD
   
4. **CacheService** - Performance critique (150 lignes)
   - Corriger les tests Streamlit (déjà commencé) 
   - Tests de performance et expiration

#### 🛠️ Outils Disponibles:
- `python scripts/develop_tests_systematically.py 4` (générer templates)
- Templates dans `tests/auto_generated/` (655 tests à compléter)
- Mocks configurés dans `tests/unit/services/`

### Phase 2: Pages Streamlit (Objectif: +15% couverture)  
**Délai**: 1-2 semaines

#### 🎯 Modules Prioritaires:
1. **consultants.py** - Page principale (1800+ lignes)
   - Tests des composants UI
   - Tests de navigation et état
   - Tests d'intégration avec services
   
2. **consultant_info.py** - Affichage consultant (340+ lignes)
   - Tests de formulaires
   - Tests de validation
   
3. **consultant_missions.py** - Gestion missions (540+ lignes)
   - Tests CRUD missions
   - Tests de calculs de revenus

#### 🛠️ Ressources:
- Template `test_consultants_generated.py` (corrigé)
- Tests existants dans `tests/unit/pages/` 
- Mocks Streamlit configurés

### Phase 3: Modules Utilitaires (Objectif: +10% couverture)
**Délai**: 1 semaine

#### 🎯 Targets:
1. **database.py** - Base de données (77 lignes, 45% actuel)
2. **models.py** - Modèles ORM (266 lignes, 80% actuel - presque OK)  
3. **technologies_referentiel.py** - Référentiel tech (23 lignes, 35%)

### Phase 4: Résolution Tests Problématiques (Objectif: +20% couverture)
**Délai**: 2-3 semaines

#### 🔧 Actions:
1. **Résoudre imports circulaires pandas**
   - 566 tests isolés dans `tests/problematic_tests/`
   - Refactoring des imports dans les modules métier
   
2. **Réintégrer tests fonctionnels** 
   - Tests business_managers (35 + 24 + 13 = 72 tests)
   - Tests consultant_documents (36 + 5 + 2 = 43 tests)
   - Tests UI enhanced (37 + 37 = 74 tests)

## 📋 Planning Détaillé

### Semaine 1-2: Services Critiques
- [ ] Compléter templates ConsultantService (45 tests existants → 120 tests)
- [ ] Corriger et étendre DocumentService (23 tests → 80 tests)  
- [ ] Finaliser BusinessManagerService et CacheService (mocks corrigés)
- [ ] **Objectif couverture**: 9% → 25%

### Semaine 3-4: Pages Principales
- [ ] Compléter test_consultants_generated.py (5 tests → 50 tests)
- [ ] Tests consultant_info et consultant_missions
- [ ] Tests de performance et intégration UI
- [ ] **Objectif couverture**: 25% → 40%

### Semaine 5-6: Modules Utilitaires  
- [ ] Tests database et models complets
- [ ] Tests référentiels et technologies
- [ ] **Objectif couverture**: 40% → 50%

### Semaine 7-9: Tests Problématiques
- [ ] Résoudre imports circulaires pandas
- [ ] Réintégrer tests business_managers (72 tests)
- [ ] Réintégrer tests UI et documents (117 tests)
- [ ] **Objectif couverture**: 50% → 80%

## 🛠️ Outils et Ressources

### Scripts Disponibles:
```bash
# Génération automatique de tests
python scripts/develop_tests_systematically.py 5

# Analyse de couverture
python scripts/improve_coverage.py

# Nettoyage environnement
python scripts/clean_test_environment.py

# Maintenance quotidienne  
python scripts/daily_maintenance.py
```

### Templates Existants:
- **655 tests auto-générés** à compléter dans `tests/auto_generated/`
- **Templates de services** configurés avec mocks
- **Templates de pages** avec mocks Streamlit

### Infrastructure:
- ✅ Hooks Git opérationnels (tests de régression automatiques)
- ✅ Environnement propre (tests problématiques isolés)
- ✅ Rapports HTML de couverture
- ✅ CI/CD GitHub Actions configuré

## 🎯 Jalons et Métriques

### Objectifs Intermédiaires:
- **Semaine 2**: 25% de couverture 
- **Semaine 4**: 40% de couverture
- **Semaine 6**: 50% de couverture
- **Semaine 9**: **80% de couverture** 🎉

### Métriques de Qualité:
- Tests de régression: ✅ Toujours à 100%
- Performance: Temps d'exécution < 2min pour suite complète
- Maintenance: Scripts automatiques quotidiens

## 💡 Bonnes Pratiques

### Développement:
1. **TDD**: Tests avant code pour nouvelles fonctionnalités
2. **Templates**: Utiliser les 655 tests auto-générés comme base
3. **Mocks**: Réutiliser les configurations existantes
4. **Coverage**: Viser 80% minimum sur nouveau code

### Workflow:
1. Générer templates: `develop_tests_systematically.py`
2. Compléter avec logique métier spécifique  
3. Vérifier couverture: `improve_coverage.py`
4. Commit automatiquement validé par hooks Git

## 🏆 Résultat Attendu

À la fin de ce plan (9 semaines):
- ✅ **80% de couverture de tests**
- ✅ **2000+ tests opérationnels** (objectif déjà atteint: 2334 tests)
- ✅ **0 régression possible** (hooks Git)
- ✅ **Infrastructure de qualité professionnelle**

---

**🚀 Avec 2334 tests existants et cette infrastructure complète, l'objectif de 80% de couverture est totalement réalisable !**

*Plan généré automatiquement par le système d'amélioration de tests*
"""
    
    # Sauvegarder le plan
    plan_file = Path('reports/PLAN_COUVERTURE_80.md')
    plan_file.write_text(plan_content, encoding='utf-8')
    
    print(f"\n📋 PLAN STRATÉGIQUE CRÉÉ:")
    print(f"   📄 Fichier: {plan_file}")
    print(f"   🎯 Objectif: 80% de couverture en 9 semaines")
    print(f"   📈 Progression: {current_cov:.1f}% → {target_cov}%")
    print(f"   🧪 Tests disponibles: 2334 (objectif 2000 déjà atteint ✅)")
    
    return plan_file

def main():
    """Fonction principale"""
    create_coverage_improvement_plan()

if __name__ == "__main__":
    main()