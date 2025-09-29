# 🎯 Plan d'Amélioration de la Couverture - De 25% à 73%

## 📊 Statut Actuel
- ✅ **Couverture SonarCloud : 25%** (auparavant 0%)
- 🔄 **Objectif : 73%** 
- 📝 **Tests défaillants identifiés : 124**

## 🎯 Stratégie d'Amélioration en 3 Phases

### Phase 1 : Correction des tests problématiques (25% → 45%)
**Cible : +20% de couverture**

#### 🔧 Problèmes identifiés :
1. **Imports incorrects dans les mocks**
   - `app.pages_modules.consultant_documents.DocumentAnalyzer` → `app.services.document_analyzer.DocumentAnalyzer`
   - Plusieurs tests utilisent de mauvais chemins pour les mocks

2. **Tests avec des signatures de fonction obsolètes**
   - Paramètres manquants dans `_apply_filters()` 
   - Nouvelles colonnes pas prises en compte (`'Entité'`)

3. **Tests Streamlit avec problèmes de session state**
   - `st.session_state.view_consultant_profile` non initialisé
   - Context manager pour `LoadingSpinner`

#### 🛠️ Actions Phase 1 :
- [ ] Corriger les imports de mock dans `test_consultant_documents_coverage.py`
- [ ] Fixer les signatures de fonction dans `test_consultant_list_coverage.py`
- [ ] Résoudre les problèmes de session state Streamlit
- [ ] Corriger les tests de dates (`StreamlitAPIException: Date value`)

### Phase 2 : Intégration des tests de régression (45% → 60%)
**Cible : +15% de couverture**

#### 🔧 Tests de régression à corriger :
- `test_import_regression.py` - Problèmes de relations consultant/mission
- Tests de validation des données importées
- Tests de détection de doublons

#### 🛠️ Actions Phase 2 :
- [ ] Réviser la logique de détection des missions dupliquées
- [ ] Corriger les assertions sur les relations consultant/mission
- [ ] Valider les mappings d'import

### Phase 3 : Optimisation et tests manquants (60% → 73%)
**Cible : +13% de couverture**

#### 🔧 Zones sous-testées :
- Modules pages avec 0% de couverture
- Fonctions utilitaires (`skill_categories.py`: 27%)
- Services métier partiellement couverts

#### 🛠️ Actions Phase 3 :
- [ ] Ajouter tests pour les pages principales (`home.py`, `consultants.py`)
- [ ] Couvrir les utilitaires (`technologies_referentiel.py`: 35%)
- [ ] Tests d'intégration pour les workflows complets

## 🏃‍♂️ Mise en Œuvre Immédiate

### 1. Correction Rapide - Mock Imports
```python
# ❌ Avant (test qui échoue)
@patch('app.pages_modules.consultant_documents.DocumentAnalyzer')

# ✅ Après (correct)
@patch('app.services.document_analyzer.DocumentAnalyzer')
```

### 2. Correction Rapide - Signatures de Fonction
```python
# ❌ Avant
_apply_filters(sample_dataframe, "", "Data Science", "Tous")

# ✅ Après  
_apply_filters(sample_dataframe, "", "Data Science", "Tous", "Tous")  # availability_filter ajouté
```

### 3. Correction Rapide - Session State
```python
# ✅ Initialisation required
st.session_state.view_consultant_profile = 123  # ID consultant
```

## 📈 Roadmap d'Implémentation

| Étape | Action | Gain Couverture | Timeline |
|-------|--------|----------------|----------|
| 1 | Fix mock imports | 25% → 30% | Immédiat |
| 2 | Fix function signatures | 30% → 35% | 30min |
| 3 | Fix Streamlit session state | 35% → 42% | 1h |
| 4 | Fix regression tests | 42% → 55% | 2h |
| 5 | Add missing page tests | 55% → 68% | 3h |
| 6 | Complete utilities coverage | 68% → 73% | 1h |

**Total estimé : 7h30 de travail**

## 🎯 Commençons par les Corrections Rapides

Démarrons immédiatement avec la correction des imports de mock qui devrait nous faire passer de 25% à ~30% rapidement.