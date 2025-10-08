"""
Script d'analyse des gaps de coverage pour Plan Option 2
Identifie les modules à faible coverage et génère un plan de tests ciblés
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json

@dataclass
class ModuleCoverage:
    """Informations de coverage pour un module"""
    name: str
    path: str
    lines_total: int
    lines_covered: int
    lines_missing: int
    coverage_percent: float
    missing_lines: List[int]
    priority: str = "LOW"
    
    def __str__(self):
        return f"{self.name}: {self.coverage_percent:.1f}% ({self.lines_covered}/{self.lines_total})"


def parse_coverage_xml(xml_path: str = "coverage.xml") -> List[ModuleCoverage]:
    """Parse le fichier coverage.xml et extrait les infos par module"""
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    modules = []
    
    for package in root.findall('.//package'):
        for cls in package.findall('.//class'):
            filename = cls.get('filename')
            
            # Ignorer les fichiers __init__.py et de test
            if '__init__' in filename or 'test_' in filename:
                continue
            
            lines = cls.findall('.//line')
            lines_total = len(lines)
            lines_covered = len([l for l in lines if l.get('hits') != '0'])
            lines_missing = lines_total - lines_covered
            
            missing_lines = [int(l.get('number')) for l in lines if l.get('hits') == '0']
            
            coverage_percent = (lines_covered / lines_total * 100) if lines_total > 0 else 0
            
            # Nom du module (sans chemin)
            module_name = Path(filename).stem
            
            module = ModuleCoverage(
                name=module_name,
                path=filename,
                lines_total=lines_total,
                lines_covered=lines_covered,
                lines_missing=lines_missing,
                coverage_percent=coverage_percent,
                missing_lines=missing_lines
            )
            
            modules.append(module)
    
    return modules


def prioritize_modules(modules: List[ModuleCoverage]) -> List[ModuleCoverage]:
    """Priorise les modules selon critères métier"""
    
    # Critères de priorisation
    HIGH_PRIORITY_KEYWORDS = ['service', 'model', 'database', 'validator']
    MEDIUM_PRIORITY_KEYWORDS = ['helper', 'util', 'form']
    
    for module in modules:
        # Priorisation basée sur:
        # 1. Mots-clés dans le nom
        # 2. Coverage < 70%
        # 3. Nombre de lignes manquantes
        
        name_lower = module.name.lower()
        
        if any(kw in name_lower for kw in HIGH_PRIORITY_KEYWORDS):
            if module.coverage_percent < 70:
                module.priority = "HIGH"
            elif module.coverage_percent < 80:
                module.priority = "MEDIUM"
            else:
                module.priority = "LOW"
        elif any(kw in name_lower for kw in MEDIUM_PRIORITY_KEYWORDS):
            if module.coverage_percent < 60:
                module.priority = "HIGH"
            elif module.coverage_percent < 75:
                module.priority = "MEDIUM"
            else:
                module.priority = "LOW"
        else:
            # Autres modules (pages, etc.)
            if module.coverage_percent < 50:
                module.priority = "MEDIUM"
            else:
                module.priority = "LOW"
    
    return sorted(modules, key=lambda m: (
        {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[m.priority],
        m.coverage_percent,
        -m.lines_missing
    ))


def generate_test_plan(modules: List[ModuleCoverage]) -> str:
    """Génère un plan de tests markdown"""
    
    # Filtrer modules avec coverage < 80%
    targets = [m for m in modules if m.coverage_percent < 80]
    
    # Grouper par priorité
    high_priority = [m for m in targets if m.priority == "HIGH"]
    medium_priority = [m for m in targets if m.priority == "MEDIUM"]
    low_priority = [m for m in targets if m.priority == "LOW"]
    
    # Calculer estimations
    total_missing = sum(m.lines_missing for m in targets)
    estimated_tests = int(total_missing * 0.3)  # ~3 lignes par test en moyenne
    
    plan = f"""# 📊 ANALYSE COVERAGE GAPS - PLAN DE TESTS CIBLÉS

**Date**: 2025-10-08  
**Coverage actuelle**: 67.7%  
**Objectif**: 80%

---

## 📈 RÉSUMÉ GLOBAL

- **Modules à < 80% coverage**: {len(targets)}
- **Lignes totales manquantes**: {total_missing}
- **Tests estimés à créer**: {estimated_tests}
- **Effort estimé**: {estimated_tests / 50}-{estimated_tests / 30} jours

---

## 🎯 MODULES HAUTE PRIORITÉ ({len(high_priority)} modules)

*Services critiques, modèles, validations*

| Module | Coverage | Manque | Tests Estimés | Fichier |
|--------|----------|--------|---------------|---------|
"""
    
    for m in high_priority[:10]:  # Top 10
        est_tests = int(m.lines_missing * 0.3)
        plan += f"| `{m.name}` | {m.coverage_percent:.1f}% | {m.lines_missing} lignes | ~{est_tests} tests | `{m.path}` |\n"
    
    plan += f"""
**Total HIGH**: {sum(m.lines_missing for m in high_priority)} lignes → ~{int(sum(m.lines_missing for m in high_priority) * 0.3)} tests

---

## 🔶 MODULES PRIORITÉ MOYENNE ({len(medium_priority)} modules)

*Helpers, utils, formulaires*

| Module | Coverage | Manque | Tests Estimés | Fichier |
|--------|----------|--------|---------------|---------|
"""
    
    for m in medium_priority[:10]:  # Top 10
        est_tests = int(m.lines_missing * 0.3)
        plan += f"| `{m.name}` | {m.coverage_percent:.1f}% | {m.lines_missing} lignes | ~{est_tests} tests | `{m.path}` |\n"
    
    plan += f"""
**Total MEDIUM**: {sum(m.lines_missing for m in medium_priority)} lignes → ~{int(sum(m.lines_missing for m in medium_priority) * 0.3)} tests

---

## 🔹 MODULES BASSE PRIORITÉ ({len(low_priority)} modules)

*Pages, affichage, autres*

Top 5 modules à faible coverage :

| Module | Coverage | Manque | Fichier |
|--------|----------|--------|---------|
"""
    
    for m in low_priority[:5]:
        plan += f"| `{m.name}` | {m.coverage_percent:.1f}% | {m.lines_missing} lignes | `{m.path}` |\n"
    
    plan += f"""
**Total LOW**: {sum(m.lines_missing for m in low_priority)} lignes → ~{int(sum(m.lines_missing for m in low_priority) * 0.3)} tests

---

## 📋 PLAN D'EXÉCUTION PAR BATCH

### Batch 1 : HIGH Priority (Estimation 2-3 jours)
"""
    
    for i, m in enumerate(high_priority[:5], 1):
        plan += f"\n#### {i}. Module `{m.name}`\n"
        plan += f"- **Coverage actuelle**: {m.coverage_percent:.1f}%\n"
        plan += f"- **Lignes manquantes**: {m.lines_missing}\n"
        plan += f"- **Tests à créer**: ~{int(m.lines_missing * 0.3)}\n"
        plan += f"- **Fichier**: `{m.path}`\n"
        plan += f"- **Lignes non couvertes**: {', '.join(map(str, m.missing_lines[:20]))}"
        if len(m.missing_lines) > 20:
            plan += f"... (et {len(m.missing_lines) - 20} autres)"
        plan += "\n"
    
    plan += f"""
**Impact attendu**: +4-5 points de coverage (67.7% → 72-73%)

---

### Batch 2 : MEDIUM Priority (Estimation 2 jours)
"""
    
    for i, m in enumerate(medium_priority[:5], 1):
        plan += f"\n#### {i}. Module `{m.name}`\n"
        plan += f"- **Coverage**: {m.coverage_percent:.1f}%\n"
        plan += f"- **Lignes manquantes**: {m.lines_missing}\n"
        plan += f"- **Tests à créer**: ~{int(m.lines_missing * 0.3)}\n"
    
    plan += f"""
**Impact attendu**: +3-4 points de coverage (72-73% → 76-77%)

---

### Batch 3 : Compléments (Estimation 1-2 jours)

Ciblage des derniers modules pour atteindre 80%

**Impact attendu**: +3-4 points de coverage (76-77% → 80%+)

---

## 🎯 PROCHAINES ACTIONS

1. ✅ **Valider ce plan** avec l'équipe
2. ⏳ **Démarrer Batch 1** : Créer tests pour top 5 modules HIGH
3. ⏳ Commit après chaque module complété
4. ⏳ Vérifier coverage après chaque batch
5. ⏳ Ajuster stratégie si nécessaire

---

**Génération automatique** : `analyze_coverage_gaps.py`
"""
    
    return plan


def main():
    """Point d'entrée principal"""
    
    print("🔍 Analyse des gaps de coverage...")
    
    # 1. Parser coverage.xml
    if not Path("coverage.xml").exists():
        print("❌ Erreur: coverage.xml introuvable")
        print("💡 Exécutez d'abord: pytest tests/ --cov=app --cov-report=xml")
        return
    
    modules = parse_coverage_xml()
    print(f"✅ {len(modules)} modules analysés")
    
    # 2. Prioriser les modules
    modules = prioritize_modules(modules)
    print("✅ Modules priorisés")
    
    # 3. Générer le plan
    plan = generate_test_plan(modules)
    
    # 4. Sauvegarder le plan
    output_file = "COVERAGE_ANALYSIS_AND_PLAN.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(plan)
    
    print(f"✅ Plan généré: {output_file}")
    
    # 5. Afficher résumé dans terminal
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DE L'ANALYSE")
    print("="*70)
    
    targets = [m for m in modules if m.coverage_percent < 80]
    high = [m for m in targets if m.priority == "HIGH"]
    medium = [m for m in targets if m.priority == "MEDIUM"]
    
    print(f"\n🎯 Modules cibles (< 80%): {len(targets)}")
    print(f"   - HIGH priority: {len(high)} modules")
    print(f"   - MEDIUM priority: {len(medium)} modules")
    
    print(f"\n📏 Lignes manquantes:")
    print(f"   - HIGH: {sum(m.lines_missing for m in high)} lignes")
    print(f"   - MEDIUM: {sum(m.lines_missing for m in medium)} lignes")
    print(f"   - TOTAL: {sum(m.lines_missing for m in targets)} lignes")
    
    total_missing = sum(m.lines_missing for m in targets)
    estimated_tests = int(total_missing * 0.3)
    print(f"\n🧪 Tests estimés à créer: {estimated_tests}")
    print(f"⏱️  Effort estimé: {estimated_tests / 50:.1f} - {estimated_tests / 30:.1f} jours")
    
    print(f"\n📄 Détails complets dans: {output_file}")
    print("\n🚀 Prochaine étape: Démarrer Batch 1 (modules HIGH priority)")


if __name__ == "__main__":
    main()
