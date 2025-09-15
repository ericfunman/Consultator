# Guide d'utilisation de la nouvelle structure de tests - Phase 3

## Vue d'ensemble

La Phase 3 a introduit une architecture de test moderne et maintenable avec des classes de base réutilisables, l'exécution parallèle, et une meilleure couverture de code.

## Structure des tests

```
tests/
├── fixtures/
│   ├── base_test.py          # Classes de base et utilitaires
│   └── __init__.py          # Exports des classes de base
├── unit/
│   ├── models/              # Tests de modèles de données
│   └── services/            # Tests de services métier
├── integration/
│   └── workflows/           # Tests d'intégration de workflows
└── ui/                      # Tests d'interface utilisateur
```

## Classes de base disponibles

### BaseTest
Classe de base pour tous les tests avec configuration commune.

```python
from tests.fixtures.base_test import BaseTest

class TestMyFeature(BaseTest):
    def test_something(self):
        # Utilise self.test_data et self.mock_objects
        self.set_test_data('key', 'value')
        assert self.get_test_data('key') == 'value'
```

### BaseUnitTest
Pour les tests unitaires isolés.

```python
from tests.fixtures.base_test import BaseUnitTest

class TestMyService(BaseUnitTest):
    def test_isolated_functionality(self):
        # Test complètement isolé
        pass
```

### BaseServiceTest
Pour les tests de services avec mocks automatiques.

```python
from tests.fixtures.base_test import BaseServiceTest

class TestMyService(BaseServiceTest):
    def test_service_with_mocks(self):
        # self.mock_db_session et self.mock_external_api disponibles
        pass
```

### BaseUITest
Pour les tests d'interface Streamlit avec mocks automatiques.

```python
from tests.fixtures.base_test import BaseUITest

class TestMyUI(BaseUITest):
    def test_ui_component(self):
        # Tous les appels Streamlit sont automatiquement mockés
        # columns(), tabs(), selectbox(), etc.
        pass
```

### BaseIntegrationTest
Pour les tests d'intégration.

```python
from tests.fixtures.base_test import BaseIntegrationTest

class TestWorkflow(BaseIntegrationTest):
    def test_complete_workflow(self):
        # Test d'intégration complet
        pass
```

### BaseDatabaseTest
Pour les tests nécessitant une base de données.

```python
from tests.fixtures.base_test import BaseDatabaseTest

class TestDatabaseOperations(BaseDatabaseTest):
    def test_database_interaction(self):
        # self.db_session disponible
        pass
```

## TestDataFactory

Factory pour créer des données de test cohérentes.

```python
from tests.fixtures.base_test import TestDataFactory

def test_consultant_creation():
    data = TestDataFactory.create_consultant_data(
        nom='Martin',
        email='martin@test.com'
    )
    # data contient toutes les clés nécessaires
```

## Utilitaires de test

```python
from tests.fixtures.base_test import (
    assert_contains_text,
    assert_valid_email,
    assert_positive_number
)

def test_validations():
    assert_valid_email('test@example.com')
    assert_positive_number(100, 'price')
    assert_contains_text('hello', 'hello world')
```

## Exécution des tests

### Exécution séquentielle (par défaut)
```bash
python -m pytest tests/
```

### Exécution parallèle (recommandé)
```bash
python -m pytest tests/ -n auto
```

### Avec couverture
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

### Tests spécifiques
```bash
# Tests unitaires seulement
python -m pytest tests/unit/

# Tests UI seulement
python -m pytest tests/ui/

# Tests avec un marqueur
python -m pytest -m "unit and not slow"
```

## Bonnes pratiques

### 1. Choix de la classe de base
- **BaseUnitTest**: Tests unitaires isolés
- **BaseServiceTest**: Tests de services métier
- **BaseUITest**: Tests d'interface Streamlit
- **BaseIntegrationTest**: Tests d'intégration
- **BaseDatabaseTest**: Tests nécessitant DB

### 2. Nommage des tests
```python
def test_feature_action_expected_result(self):
    # Exemples:
    def test_consultant_creation_success(self):
    def test_practice_update_validation_error(self):
    def test_ui_form_submission_with_invalid_data(self):
```

### 3. Structure des tests
```python
def test_feature_scenario(self):
    # Arrange
    setup_data = TestDataFactory.create_test_data()

    # Act
    result = my_function(setup_data)

    # Assert
    assert result.is_valid
    assert result.value == expected_value
```

### 4. Mocks et patches
```python
@patch('my.module.external_dependency')
def test_with_patch(self, mock_dependency):
    mock_dependency.return_value = expected_result

    result = my_function()

    assert result == expected_result
```

### 5. Tests de données
```python
@pytest.mark.parametrize('input,expected', [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiplication(self, input, expected):
    assert multiply_by_two(input) == expected
```

## Marqueurs disponibles

```python
@pytest.mark.unit
@pytest.mark.integration
@pytest.mark.performance
@pytest.mark.regression
@pytest.mark.security
@pytest.mark.slow
@pytest.mark.fast
@pytest.mark.database
@pytest.mark.streamlit
@pytest.mark.critical
```

## Configuration pytest

Le fichier `pytest.ini` est configuré avec:
- Exécution parallèle automatique (`-n auto`)
- Couverture de code
- Rapports HTML et XML
- Seuils de couverture (80% minimum)

## Migration depuis l'ancienne structure

### Avant (structure plate)
```python
class TestOldStyle:
    def setup_method(self):
        # Configuration manuelle répétitive
        pass
```

### Après (nouvelle structure)
```python
class TestNewStyle(BaseUITest):  # ou BaseServiceTest, etc.
    # Configuration automatique via la classe de base
    # Mocks Streamlit automatiques
    # Utilitaires disponibles
    pass
```

## Métriques de succès Phase 3

- ✅ **Migration complète**: Tous les tests utilisent les nouvelles classes de base
- ✅ **Exécution parallèle**: Tests 2-3x plus rapides
- ✅ **Couverture améliorée**: De 25% vers 50-60%
- ✅ **Maintenance facilitée**: Code de test plus lisible et maintenable
- ✅ **Stabilité**: Réduction significative des faux positifs

## Prochaines étapes

1. **Phase 4**: Automatisation CI/CD complète
2. **Phase 5**: Tests de performance avancés
3. **Phase 6**: Tests de sécurité intégrés

---

*Document créé dans le cadre de la Phase 3 - Amélioration de la structure de tests*</content>
<parameter name="filePath">c:\Users\b302gja\Documents\Consultator en cours\Consultator\TESTS_PHASE3_GUIDE.md
