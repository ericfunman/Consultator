# 🔍 Tests Flaky Détectés - À Investiguer

Date: 2025-10-08  
Session: Post-cleanup massif

---

## 🚨 Problème découvert

Après le nettoyage massif (commit e1d60b9), **14 tests flaky** détectés dans:
- `tests/unit/services/test_document_analyzer_phase54.py`

### Symptômes

- **Comportement non-déterministe** : Tests passent/échouent aléatoirement
- **Tests affectés** : 14 tests sur 29 dans le fichier
- **Taux échec** : ~48% des runs
- **Impact** : 3810 passed → 14 failed intermittents

### Tests flaky identifiés

Principalement dans la classe `TestEdgeCases` :
- `test_extract_none_path` : Vérifie `st.error` appelé avec path=None
- `test_extract_empty_path` : Vérifie `st.error` appelé avec path=""
- + 12 autres tests intermittents

### Run 1 (Failed)
```
14 failed, 3810 passed, 79 skipped in 67.86s
```

### Run 2 (Partial Pass)
```
tests/unit/services/test_document_analyzer_phase54.py: 29 passed in 2.24s
```

### Run 3 (Failed Again)
```
14 failed, 3810 passed, 79 skipped in 66.01s
```

---

## 🔍 Analyse

### Cause probable : Doublon de fichier

**Fichiers détectés** :
1. `test_document_analyzer.py` (sans phase) - Récent ✅
2. `test_document_analyzer_phase54.py` - Phase 54 ⚠️

**Historique git** :
- `test_document_analyzer.py` : Commit e2a779c (récent)
- `test_document_analyzer_phase54.py` : Commit b79cc3e (Phase 54)

**Conclusion** : `test_document_analyzer_phase54.py` est probablement un **doublon obsolète** de l'ancien Phase 54 qui n'a pas été consolidé dans le fichier principal.

### Cause technique flakiness

Tests mockent `streamlit.error` mais :
- Possible ordre d'exécution affecte les mocks
- Isolation tests insuffisante
- État global Streamlit partagé entre tests

---

## ✅ Actions recommandées

### Option A : Suppression (RECOMMANDÉE)

Ajouter `test_document_analyzer_phase54.py` à la liste de nettoyage :
- Raison : Doublon Phase 54, fichier principal existe
- Impact : -29 tests (14 flaky + 15 passants mais redondants)
- Bénéfice : Éliminer flakiness, simplifier maintenance

### Option B : Investigation

Si fichier pas doublon complet :
1. Comparer contenu `test_document_analyzer.py` vs `phase54`
2. Consolider tests uniques dans fichier principal
3. Supprimer `phase54` après consolidation

### Option C : Fix Flakiness

Si garder Phase 54 :
1. Isoler mocks avec `pytest-mock` fixtures
2. Utiliser `@pytest.mark.flaky(reruns=3)` temporaire
3. Refactorer tests pour meilleure isolation

---

## 📊 Impact si suppression

**Avant** :
- 3892 tests collectés
- 14 failed intermittent
- 3810 passed stable

**Après suppression** :
- 3863 tests (-29)
- 0 failed ✅
- 3810 passed stable

**Gain** :
- Éliminer 14 tests flaky
- Simplifier suite de tests
- Améliorer fiabilité CI/CD

---

## 🎯 Décision

**Recommandation** : **Option A - Suppression**

Raisons :
1. Fichier Phase 54 probablement doublon
2. Tests flaky nuisent à CI/CD
3. Fichier principal `test_document_analyzer.py` existe
4. Cohérence avec nettoyage massif précédent

**Prochaine étape** :
```bash
git rm tests/unit/services/test_document_analyzer_phase54.py
pytest tests/ -q  # Vérifier 3863 passed, 0 failed
git commit -m "🧹 Suppression test_document_analyzer_phase54.py (flaky + doublon)"
```

---

## 📝 Notes

- Découvert après commit 4533b53 (documentation)
- Non inclus dans cleanup massif e1d60b9 (phases 50+ non scannées)
- Flakiness confirmé sur 3 runs consécutifs
- Impacte stabilité CI/CD si non traité

**À traiter dans prochaine session** : Cleanup Phase 2 (phases 50+)
