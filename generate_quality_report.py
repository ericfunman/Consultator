#!/usr/bin/env python3
"""
Rapport de Qualité du Code - Consultator
Analyse statique et recommandations d'amélioration
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import ast
import inspect

def analyze_codebase():
    """Analyse complète de la qualité du code"""

    print("🔍 Analyse de la qualité du code en cours...")

    # Métriques de base
    metrics = {
        'total_files': 0,
        'total_lines': 0,
        'python_files': 0,
        'test_files': 0,
        'empty_lines': 0,
        'comment_lines': 0,
        'code_lines': 0,
        'functions': 0,
        'classes': 0,
        'imports': 0,
        'complexity_warnings': 0,
        'security_issues': 0,
        'code_smells': 0
    }

    # Analyse par module
    modules_analysis = {}
    security_findings = []
    code_quality_issues = []

    # Extensions à analyser
    extensions = ['.py', '.json', '.yml', '.yaml', '.toml', '.md']

    for root, dirs, files in os.walk('.'):
        # Ignorer certains dossiers
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', '.git', 'node_modules', '.venv']]

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                metrics['total_files'] += 1

                if file.endswith('.py'):
                    metrics['python_files'] += 1
                    if 'test' in file.lower():
                        metrics['test_files'] += 1

                    # Analyse du fichier Python
                    try:
                        analysis = analyze_python_file(filepath)
                        modules_analysis[filepath] = analysis

                        # Accumuler les métriques
                        for key, value in analysis['metrics'].items():
                            if key in metrics:
                                metrics[key] += value

                        # Collecter les problèmes
                        security_findings.extend(analysis['security_issues'])
                        code_quality_issues.extend(analysis['code_quality_issues'])

                    except Exception as e:
                        print(f"⚠️ Erreur lors de l'analyse de {filepath}: {e}")

    return {
        'metrics': metrics,
        'modules_analysis': modules_analysis,
        'security_findings': security_findings,
        'code_quality_issues': code_quality_issues,
        'timestamp': datetime.now().isoformat()
    }

def analyze_python_file(filepath):
    """Analyse détaillée d'un fichier Python"""

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    lines = content.split('\n')

    # Métriques de base
    file_metrics = {
        'lines': len(lines),
        'empty_lines': sum(1 for line in lines if line.strip() == ''),
        'comment_lines': sum(1 for line in lines if line.strip().startswith('#')),
        'functions': 0,
        'classes': 0,
        'imports': 0,
        'complexity_warnings': 0
    }

    file_metrics['code_lines'] = file_metrics['lines'] - file_metrics['empty_lines'] - file_metrics['comment_lines']

    # Analyse AST pour métriques avancées
    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                file_metrics['functions'] += 1
                # Complexité cyclomatique simple
                if count_decisions(node) > 10:
                    file_metrics['complexity_warnings'] += 1
            elif isinstance(node, ast.ClassDef):
                file_metrics['classes'] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                file_metrics['imports'] += 1

    except SyntaxError:
        pass

    # Analyse de sécurité
    security_issues = detect_security_issues(content, filepath)

    # Analyse qualité du code
    code_quality_issues = detect_code_quality_issues(content, filepath)

    return {
        'metrics': file_metrics,
        'security_issues': security_issues,
        'code_quality_issues': code_quality_issues,
        'file_info': {
            'path': filepath,
            'size': len(content),
            'extension': Path(filepath).suffix
        }
    }

def count_decisions(node):
    """Compte le nombre de décisions (complexité cyclomatique simple)"""
    count = 1  # Base complexity
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
            count += 1
        elif isinstance(child, ast.BoolOp):
            count += len(child.values) - 1
    return count

def detect_security_issues(content, filepath):
    """Détecte les problèmes de sécurité"""
    issues = []

    # Injection SQL
    if re.search(r'(SELECT|INSERT|UPDATE|DELETE).*\+.*%|\.format\(.*\)', content, re.IGNORECASE):
        issues.append({
            'type': 'SQL_INJECTION',
            'severity': 'HIGH',
            'description': 'Possible injection SQL détectée',
            'file': filepath,
            'line': 'N/A'
        })

    # Secrets en dur
    if re.search(r'(password|secret|key|token)\s*=\s*["\'][^"\']*["\']', content, re.IGNORECASE):
        issues.append({
            'type': 'HARDCODED_SECRET',
            'severity': 'MEDIUM',
            'description': 'Secret potentiellement codé en dur',
            'file': filepath,
            'line': 'N/A'
        })

    # eval() usage
    if 'eval(' in content:
        issues.append({
            'type': 'CODE_INJECTION',
            'severity': 'HIGH',
            'description': 'Usage de eval() détecté',
            'file': filepath,
            'line': 'N/A'
        })

    # Pickle usage
    if 'pickle.' in content or 'import pickle' in content:
        issues.append({
            'type': 'INSECURE_DESERIALIZATION',
            'severity': 'MEDIUM',
            'description': 'Usage de pickle détecté (risque de désérialisation)',
            'file': filepath,
            'line': 'N/A'
        })

    return issues

def detect_code_quality_issues(content, filepath):
    """Détecte les problèmes de qualité du code"""
    issues = []

    lines = content.split('\n')

    # Lignes trop longues
    for i, line in enumerate(lines, 1):
        if len(line) > 120:
            issues.append({
                'type': 'LINE_TOO_LONG',
                'severity': 'LOW',
                'description': f'Ligne trop longue ({len(line)} caractères)',
                'file': filepath,
                'line': i
            })

    # Fonctions trop longues
    functions = re.findall(r'def\s+\w+\s*\([^)]*\)\s*:', content)
    for func in functions:
        func_start = content.find(func)
        if func_start != -1:
            # Trouver la fin de la fonction (approximatif)
            func_end = func_start + 1000  # Approximation
            func_content = content[func_start:func_end]
            func_lines = len(func_content.split('\n'))
            if func_lines > 50:
                issues.append({
                    'type': 'FUNCTION_TOO_LONG',
                    'severity': 'MEDIUM',
                    'description': f'Fonction potentiellement trop longue ({func_lines} lignes)',
                    'file': filepath,
                    'line': 'N/A'
                })

    # Imports non utilisés (détection simple)
    import_lines = [i for i, line in enumerate(lines, 1) if line.strip().startswith(('import ', 'from '))]
    for import_line in import_lines:
        if import_line < len(lines):
            # Vérifier si l'import est utilisé dans les 20 lignes suivantes
            import_match = re.match(r'(?:import\s+(\w+)|from\s+\w+\s+import\s+(\w+))', lines[import_line-1])
            if import_match:
                module_name = import_match.group(1) or import_match.group(2)
                if module_name:
                    # Vérification simple d'usage
                    usage_found = False
                    for j in range(import_line, min(import_line + 20, len(lines))):
                        if module_name in lines[j]:
                            usage_found = True
                            break
                    if not usage_found:
                        issues.append({
                            'type': 'UNUSED_IMPORT',
                            'severity': 'LOW',
                            'description': f'Import potentiellement non utilisé: {module_name}',
                            'file': filepath,
                            'line': import_line
                        })

    # Variables globales
    if re.search(r'^\s*[A-Z][A-Z_]*\s*=', content, re.MULTILINE):
        issues.append({
            'type': 'GLOBAL_VARIABLE',
            'severity': 'LOW',
            'description': 'Variable globale détectée',
            'file': filepath,
            'line': 'N/A'
        })

    return issues

def generate_quality_report(analysis_results):
    """Génère le rapport de qualité"""

    metrics = analysis_results['metrics']

    report = f"""
# 📊 RAPPORT DE QUALITÉ DU CODE - CONSULTATOR

**Date de génération:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
**Version analysée:** Master Branch

## 📈 MÉTRIQUES GLOBALES

### 📁 Structure du projet
- **Total fichiers:** {metrics['total_files']}
- **Fichiers Python:** {metrics['python_files']}
- **Fichiers de test:** {metrics['test_files']}
- **Ratio test/code:** {metrics['test_files']/max(metrics['python_files']-metrics['test_files'], 1):.2f}

### 📝 Métriques de code
- **Lignes totales:** {metrics['total_lines']:,}
- **Lignes de code:** {metrics['code_lines']:,}
- **Lignes vides:** {metrics['empty_lines']:,}
- **Commentaires:** {metrics['comment_lines']:,}
- **Ratio commentaires/code:** {metrics['comment_lines']/max(metrics['code_lines'], 1):.2%}

### 🏗️ Architecture
- **Fonctions:** {metrics['functions']}
- **Classes:** {metrics['classes']}
- **Imports:** {metrics['imports']}
- **Complexité moyenne:** {metrics['complexity_warnings']/max(metrics['functions'], 1):.2f} warnings/fonction

## 🔒 SÉCURITÉ

### ⚠️ Problèmes de sécurité détectés: {len(analysis_results['security_findings'])}

"""

    # Détails sécurité
    severity_count = Counter(issue['severity'] for issue in analysis_results['security_findings'])

    report += f"""
**Par sévérité:**
- 🔴 Critique: {severity_count.get('CRITICAL', 0)}
- 🟠 Haute: {severity_count.get('HIGH', 0)}
- 🟡 Moyenne: {severity_count.get('MEDIUM', 0)}
- 🟢 Faible: {severity_count.get('LOW', 0)}

"""

    for issue in analysis_results['security_findings'][:10]:  # Top 10
        report += f"""
### {issue['type']}
- **Sévérité:** {issue['severity']}
- **Description:** {issue['description']}
- **Fichier:** {issue['file']}
"""

    report += """

## 🧹 QUALITÉ DU CODE

### ⚠️ Problèmes de qualité détectés: {len(analysis_results['code_quality_issues'])}

"""

    # Détails qualité
    quality_severity = Counter(issue['severity'] for issue in analysis_results['code_quality_issues'])

    report += f"""
**Par sévérité:**
- 🔴 Critique: {quality_severity.get('CRITICAL', 0)}
- 🟠 Haute: {quality_severity.get('HIGH', 0)}
- 🟡 Moyenne: {quality_severity.get('MEDIUM', 0)}
- 🟢 Faible: {quality_severity.get('LOW', 0)}

"""

    # Top 10 problèmes qualité
    for issue in analysis_results['code_quality_issues'][:10]:
        report += f"""
### {issue['type']}
- **Sévérité:** {issue['severity']}
- **Description:** {issue['description']}
- **Fichier:** {issue['file']}
- **Ligne:** {issue['line']}
"""

    # Recommandations
    report += """

## 🎯 RECOMMANDATIONS D'AMÉLIORATION

### 🔴 PRIORITÉ HAUTE

1. **Sécurité**
   - Supprimer les secrets codés en dur
   - Remplacer eval() par des alternatives sûres
   - Sécuriser la désérialisation pickle
   - Implémenter une validation d'entrée robuste

2. **Performance**
   - Optimiser les fonctions complexes (>10 décisions)
   - Implémenter la mise en cache pour les requêtes fréquentes
   - Réduire la taille des fonctions longues (>50 lignes)

### 🟡 PRIORITÉ MOYENNE

3. **Maintenabilité**
   - Réduire la longueur des lignes (>120 caractères)
   - Supprimer les imports non utilisés
   - Améliorer la couverture de tests (actuellement ~{metrics['test_files']/max(metrics['python_files']-metrics['test_files'], 1)*100:.1f}%)

4. **Documentation**
   - Augmenter le ratio commentaires/code (actuellement {metrics['comment_lines']/max(metrics['code_lines'], 1):.1%})
   - Documenter les fonctions complexes
   - Créer une documentation API

### 🟢 PRIORITÉ FAIBLE

5. **Standards**
   - Uniformiser le style de code (PEP 8)
   - Implémenter des types hints complets
   - Configurer des hooks pre-commit

## 📊 SCORES DE QUALITÉ

### Sécurité: {'🔴 CRITIQUE' if len(analysis_results['security_findings']) > 5 else '🟠 À AMÉLIORER' if len(analysis_results['security_findings']) > 0 else '🟢 BON'}

### Maintenabilité: {'🔴 À RÉFACTORER' if metrics['complexity_warnings'] > 20 else '🟠 À OPTIMISER' if metrics['complexity_warnings'] > 10 else '🟢 BONNE'}

### Testabilité: {'🔴 INSUFFISANTE' if metrics['test_files']/max(metrics['python_files']-metrics['test_files'], 1) < 0.5 else '🟠 À AMÉLIORER' if metrics['test_files']/max(metrics['python_files']-metrics['test_files'], 1) < 0.8 else '🟢 EXCELLENTE'}

### Documentation: {'🔴 INSUFFISANTE' if metrics['comment_lines']/max(metrics['code_lines'], 1) < 0.1 else '🟠 À AMÉLIORER' if metrics['comment_lines']/max(metrics['code_lines'], 1) < 0.2 else '🟢 EXCELLENTE'}

---

*Rapport généré automatiquement par l'analyseur de qualité du code*
"""

    return report

def save_report_to_file(report_content, output_path="docs/quality_report.md"):
    """Sauvegarde le rapport dans un fichier"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"✅ Rapport sauvegardé: {output_path}")
    return output_path

if __name__ == "__main__":
    print("🚀 Génération du rapport de qualité du code...")

    # Analyser la codebase
    analysis_results = analyze_codebase()

    # Générer le rapport
    report = generate_quality_report(analysis_results)

    # Sauvegarder
    output_file = save_report_to_file(report)

    print("📊 Analyse terminée!")
    print(f"📁 Fichiers analysés: {analysis_results['metrics']['total_files']}")
    print(f"🐍 Fichiers Python: {analysis_results['metrics']['python_files']}")
    print(f"🧪 Tests: {analysis_results['metrics']['test_files']}")
    print(f"🔒 Problèmes sécurité: {len(analysis_results['security_findings'])}")
    print(f"🧹 Problèmes qualité: {len(analysis_results['code_quality_issues'])}")

if __name__ == "__main__":
    print("🚀 Génération du rapport de qualité du code...")

    # Analyser la codebase
    analysis_results = analyze_codebase()

    # Générer le rapport
    report = generate_quality_report(analysis_results)

    # Sauvegarder
if __name__ == "__main__":
    print("🚀 Génération du rapport de qualité du code...")

    # Analyser la codebase
    analysis_results = analyze_codebase()

    # Générer le rapport
    report = generate_quality_report(analysis_results)

    # Sauvegarder
    output_file = save_report_to_file(report)

    print("📊 Analyse terminée!")
    print(f"📁 Fichiers analysés: {analysis_results['metrics']['total_files']}")
    print(f"🐍 Fichiers Python: {analysis_results['metrics']['python_files']}")
    print(f"🧪 Tests: {analysis_results['metrics']['test_files']}")
    print(f"🔒 Problèmes sécurité: {len(analysis_results['security_findings'])}")
    print(f"🧹 Problèmes qualité: {len(analysis_results['code_quality_issues'])}")
