# 📋 Phase 63 - Plan d'Attaque : `consultant_service.py`

## 🎯 Objectif
Passer de **69% → 85%+** en couvrant les **167 lignes manquantes**

---

## 📊 État Actuel
- **Coverage** : 69% (366/533 statements)
- **Lignes manquantes** : 167 statements
- **Tests existants** : 45 tests passent
- **Estimation** : ~50 nouveaux tests nécessaires (3.3 lignes/test)

---

## 🧩 Stratégie par Batches (3 sessions)

### **Batch 1 : Méthodes de recherche et filtres** (Lignes 67-234)
**Target** : Lines 67-110, 148-234
**Tests à créer** : ~18 tests
**Temps estimé** : 1.5-2h

#### Méthodes à tester :
1. `get_all_consultants_objects()` - Error paths (lines 67-69)
   - Test avec SQLAlchemyError
   - Test avec ValueError
   - Test avec TypeError/AttributeError

2. `_build_search_query()` - Création de requête (lines 74-110)
   - Test avec tous filtres vides
   - Test avec practice_filter défini
   - Test avec grade_filter défini
   - Test avec availability_filter défini
   - Test avec combinaisons multiples

3. `_apply_search_filters()` - Application filtres (lines 148, 151, 154)
   - Test avec search_term vide
   - Test avec search_term SQL injection attempt
   - Test avec caractères spéciaux

4. `_calculate_experience_years()` - Calcul d'expérience (lines 230-234)
   - Test avec date_premiere_mission None
   - Test avec date dans le futur
   - Test avec date valide
   - Test avec date très ancienne (>50 ans)

**Coverage attendu après Batch 1** : 69% → **~75%** (+6%)

---

### **Batch 2 : Méthodes de statistiques et comptage** (Lignes 266-415)
**Target** : Lines 266-268, 276-278, 284-323, 354-415
**Tests à créer** : ~20 tests
**Temps estimé** : 2-2.5h

#### Méthodes à tester :
1. `get_consultants_count()` - Error paths (lines 266-268)
   - Test avec SQLAlchemyError
   - Test avec session None

2. `_build_stats_query()` - Statistiques (lines 284-308, 314-323)
   - Test avec tous filtres None
   - Test avec practice_filter
   - Test avec grade_filter
   - Test avec availability_filter
   - Test combinaisons multiples
   - Test query.filter() appelé correctement

3. `get_search_count()` - Comptage recherche (lines 276-278)
   - Test avec erreur de requête
   - Test avec résultat 0
   - Test avec grand nombre (>1000)

4. `get_statistics()` - Stats globales (lines 354-360)
   - Test avec DB vide
   - Test avec SQLAlchemyError
   - Test avec données valides

5. `_calculate_statistics()` - Calculs internes (lines 397-415)
   - Test avec consultants=None
   - Test avec liste vide
   - Test avec salaires None/0
   - Test avec divisions par zéro

**Coverage attendu après Batch 2** : 75% → **~82%** (+7%)

---

### **Batch 3 : CRUD et méthodes complexes** (Lignes 434-1360)
**Target** : Lignes manquantes 434-1360
**Tests à créer** : ~15 tests (sélectifs)
**Temps estimé** : 2-3h

#### Méthodes à tester (SÉLECTIF - High value only) :
1. `get_consultant_by_id()` - Error paths (lines 434-436, 482-484)
   - Test avec ID invalide (string, négatif)
   - Test avec SQLAlchemyError
   - Test avec consultant non trouvé

2. `create_consultant()` - Création (lines 507-509, 527)
   - Test avec données None/vides
   - Test avec email invalide
   - Test avec practice_id inexistant
   - Test avec SQLAlchemyError sur commit

3. `update_consultant()` - Mise à jour (lines 573-575, 596-598)
   - Test avec consultant_id inexistant
   - Test avec données invalides
   - Test avec SQLAlchemyError

4. `delete_consultant()` - Suppression (lines 681-683, 725, 732-734)
   - Test avec consultant_id inexistant
   - Test avec SQLAlchemyError
   - Test avec cascade (missions, compétences)

5. **SKIP** : Méthodes de compétences (lines 771-1360)
   - **Raison** : Très volumineuses, complexes, ROI moyen
   - **Décision** : Se concentrer sur CRUD principal
   - **Alternative** : Phase 64 dédiée si nécessaire

**Coverage attendu après Batch 3** : 82% → **~87%** (+5%)

---

## 🎯 Objectif Final Révisé
- **Coverage final** : **85-87%** (au lieu de 90%+)
- **Raison** : Méthodes de compétences très complexes (lines 771-1360)
- **Impact global** : 68.6% → **69.8%** (+1.2%)
- **Gain total** : +150 lignes couvertes sur 167

---

## ✅ Critères de Succès
- [ ] Batch 1 : 18 tests créés, coverage → 75%
- [ ] Batch 2 : 20 tests créés, coverage → 82%
- [ ] Batch 3 : 15 tests créés, coverage → 87%
- [ ] Tous les tests passent (>95%)
- [ ] Commits après chaque batch
- [ ] Verification SonarCloud

---

## 🚀 Commençons par Batch 1 !
Focus : Méthodes de recherche et filtres (lignes 67-234)
