
# 📊 RAPPORT DE QUALITÉ DU CODE - CONSULTATOR

**Date de génération:** 15/09/2025 15:34:59
**Version analysée:** Master Branch

## 📈 MÉTRIQUES GLOBALES

### 📁 Structure du projet
- **Total fichiers:** 225
- **Fichiers Python:** 162
- **Fichiers de test:** 47
- **Ratio test/code:** 0.41

### 📝 Métriques de code
- **Lignes totales:** 0
- **Lignes de code:** 41,972
- **Lignes vides:** 9,587
- **Commentaires:** 3,672
- **Ratio commentaires/code:** 8.75%

### 🏗️ Architecture
- **Fonctions:** 1247
- **Classes:** 113
- **Imports:** 1272
- **Complexité moyenne:** 0.14 warnings/fonction

## 🔒 SÉCURITÉ

### ⚠️ Problèmes de sécurité détectés: 20


**Par sévérité:**
- 🔴 Critique: 0
- 🟠 Haute: 5
- 🟡 Moyenne: 15
- 🟢 Faible: 0


### HARDCODED_SECRET
- **Sévérité:** MEDIUM
- **Description:** Secret potentiellement codé en dur
- **Fichier:** .\enhance_tests_coverage.py

### SQL_INJECTION
- **Sévérité:** HIGH
- **Description:** Possible injection SQL détectée
- **Fichier:** .\generate_quality_report.py

### CODE_INJECTION
- **Sévérité:** HIGH
- **Description:** Usage de eval() détecté
- **Fichier:** .\generate_quality_report.py

### INSECURE_DESERIALIZATION
- **Sévérité:** MEDIUM
- **Description:** Usage de pickle détecté (risque de désérialisation)
- **Fichier:** .\generate_quality_report.py

### SQL_INJECTION
- **Sévérité:** HIGH
- **Description:** Possible injection SQL détectée
- **Fichier:** .\generate_quality_report_final.py

### CODE_INJECTION
- **Sévérité:** HIGH
- **Description:** Usage de eval() détecté
- **Fichier:** .\generate_word_report.py

### HARDCODED_SECRET
- **Sévérité:** MEDIUM
- **Description:** Secret potentiellement codé en dur
- **Fichier:** .\sonar_integration.py

### HARDCODED_SECRET
- **Sévérité:** MEDIUM
- **Description:** Secret potentiellement codé en dur
- **Fichier:** .\app\pages_modules\business_managers.py

### HARDCODED_SECRET
- **Sévérité:** MEDIUM
- **Description:** Secret potentiellement codé en dur
- **Fichier:** .\app\pages_modules\consultants.py

### HARDCODED_SECRET
- **Sévérité:** MEDIUM
- **Description:** Secret potentiellement codé en dur
- **Fichier:** .\app\pages_modules\consultants_clean.py


## 🧹 QUALITÉ DU CODE

### ⚠️ Problèmes de qualité détectés: {len(analysis_results['code_quality_issues'])}


**Par sévérité:**
- 🔴 Critique: 0
- 🟠 Haute: 0
- 🟡 Moyenne: 0
- 🟢 Faible: 550


### LINE_TOO_LONG
- **Sévérité:** LOW
- **Description:** Ligne trop longue (141 caractères)
- **Fichier:** .\analyze_docstrings_detailed.py
- **Ligne:** 57

### UNUSED_IMPORT
- **Sévérité:** LOW
- **Description:** Import potentiellement non utilisé: os
- **Fichier:** .\analyze_docstrings_detailed.py
- **Ligne:** 2

### UNUSED_IMPORT
- **Sévérité:** LOW
- **Description:** Import potentiellement non utilisé: Path
- **Fichier:** .\analyze_docstrings_detailed.py
- **Ligne:** 3

### UNUSED_IMPORT
- **Sévérité:** LOW
- **Description:** Import potentiellement non utilisé: os
- **Fichier:** .\analyze_documentation.py
- **Ligne:** 7

### UNUSED_IMPORT
- **Sévérité:** LOW
- **Description:** Import potentiellement non utilisé: ast
- **Fichier:** .\analyze_documentation.py
- **Ligne:** 9

### UNUSED_IMPORT
- **Sévérité:** LOW
- **Description:** Import potentiellement non utilisé: Path
- **Fichier:** .\analyze_documentation.py
- **Ligne:** 10

### UNUSED_IMPORT
- **Sévérité:** LOW
- **Description:** Import potentiellement non utilisé: Dict
- **Fichier:** .\analyze_documentation.py
- **Ligne:** 11

### LINE_TOO_LONG
- **Sévérité:** LOW
- **Description:** Ligne trop longue (144 caractères)
- **Fichier:** .\analyze_documentation_complete.py
- **Ligne:** 88

### LINE_TOO_LONG
- **Sévérité:** LOW
- **Description:** Ligne trop longue (140 caractères)
- **Fichier:** .\analyze_documentation_complete.py
- **Ligne:** 92

### UNUSED_IMPORT
- **Sévérité:** LOW
- **Description:** Import potentiellement non utilisé: ast
- **Fichier:** .\analyze_documentation_complete.py
- **Ligne:** 1


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
