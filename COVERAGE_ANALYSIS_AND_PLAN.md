# 📊 ANALYSE COVERAGE GAPS - PLAN DE TESTS CIBLÉS

**Date**: 2025-10-08  
**Coverage actuelle**: 67.7%  
**Objectif**: 80%

---

## 📈 RÉSUMÉ GLOBAL

- **Modules à < 80% coverage**: 18
- **Lignes totales manquantes**: 3062
- **Tests estimés à créer**: 918
- **Effort estimé**: 18.36-30.6 jours

---

## 🎯 MODULES HAUTE PRIORITÉ (2 modules)

*Services critiques, modèles, validations*

| Module | Coverage | Manque | Tests Estimés | Fichier |
|--------|----------|--------|---------------|---------|
| `business_manager_service` | 48.4% | 32 lignes | ~9 tests | `services/business_manager_service.py` |
| `chatbot_service` | 67.3% | 423 lignes | ~126 tests | `services/chatbot_service.py` |

**Total HIGH**: 455 lignes → ~136 tests

---

## 🔶 MODULES PRIORITÉ MOYENNE (6 modules)

*Helpers, utils, formulaires*

| Module | Coverage | Manque | Tests Estimés | Fichier |
|--------|----------|--------|---------------|---------|
| `main_simple` | 0.0% | 0 lignes | ~0 tests | `main_simple.py` |
| `home` | 28.0% | 59 lignes | ~17 tests | `pages_modules/home.py` |
| `consultants` | 47.4% | 957 lignes | ~287 tests | `pages_modules/consultants.py` |
| `consultant_documents` | 48.2% | 262 lignes | ~78 tests | `pages_modules/consultant_documents.py` |
| `consultant_forms` | 65.7% | 81 lignes | ~24 tests | `pages_modules/consultant_forms.py` |
| `document_service` | 78.9% | 43 lignes | ~12 tests | `services/document_service.py` |

**Total MEDIUM**: 1402 lignes → ~420 tests

---

## 🔹 MODULES BASSE PRIORITÉ (10 modules)

*Pages, affichage, autres*

Top 5 modules à faible coverage :

| Module | Coverage | Manque | Fichier |
|--------|----------|--------|---------|
| `practices` | 51.2% | 119 lignes | `pages_modules/practices.py` |
| `business_managers` | 52.3% | 291 lignes | `pages_modules/business_managers.py` |
| `consultant_list` | 61.0% | 96 lignes | `pages_modules/consultant_list.py` |
| `enhanced_ui` | 64.5% | 87 lignes | `ui/enhanced_ui.py` |
| `consultant_languages` | 65.3% | 109 lignes | `pages_modules/consultant_languages.py` |

**Total LOW**: 1205 lignes → ~361 tests

---

## 📋 PLAN D'EXÉCUTION PAR BATCH

### Batch 1 : HIGH Priority (Estimation 2-3 jours)

#### 1. Module `business_manager_service`
- **Coverage actuelle**: 48.4%
- **Lignes manquantes**: 32
- **Tests à créer**: ~9
- **Fichier**: `services/business_manager_service.py`
- **Lignes non couvertes**: 29, 30, 31, 34, 35, 37, 46, 60, 61, 62, 63, 69, 70, 71, 73, 74, 75, 81, 84, 85... (et 12 autres)

#### 2. Module `chatbot_service`
- **Coverage actuelle**: 67.3%
- **Lignes manquantes**: 423
- **Tests à créer**: ~126
- **Fichier**: `services/chatbot_service.py`
- **Lignes non couvertes**: 34, 36, 37, 80, 92, 96, 100, 102, 104, 106, 108, 110, 112, 114, 417, 418, 421, 422, 425, 426... (et 403 autres)

**Impact attendu**: +4-5 points de coverage (67.7% → 72-73%)

---

### Batch 2 : MEDIUM Priority (Estimation 2 jours)

#### 1. Module `main_simple`
- **Coverage**: 0.0%
- **Lignes manquantes**: 0
- **Tests à créer**: ~0

#### 2. Module `home`
- **Coverage**: 28.0%
- **Lignes manquantes**: 59
- **Tests à créer**: ~17

#### 3. Module `consultants`
- **Coverage**: 47.4%
- **Lignes manquantes**: 957
- **Tests à créer**: ~287

#### 4. Module `consultant_documents`
- **Coverage**: 48.2%
- **Lignes manquantes**: 262
- **Tests à créer**: ~78

#### 5. Module `consultant_forms`
- **Coverage**: 65.7%
- **Lignes manquantes**: 81
- **Tests à créer**: ~24

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
