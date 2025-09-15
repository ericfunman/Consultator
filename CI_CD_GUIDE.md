# 🚀 Guide CI/CD - Consultator

## Vue d'ensemble

Le pipeline CI/CD de Consultator est conçu pour maintenir la qualité du code, automatiser les tests et assurer un déploiement fiable. Il utilise GitHub Actions pour l'intégration continue et pre-commit hooks pour la qualité locale.

## 🏗️ Architecture du Pipeline

### Workflows GitHub Actions

#### 1. Workflow Principal (`ci.yml`)
- **Déclencheur** : Push/PR sur `master` et `main`
- **Multi-version Python** : Tests sur Python 3.8, 3.9, 3.10, 3.11
- **Étapes** :
  - Installation des dépendances avec cache
  - Initialisation de la base de données
  - Exécution des tests avec couverture
  - Upload vers Codecov

#### 2. Workflow Qualité (`ci.yml` - job `quality`)
- **Outils intégrés** :
  - **Black** : Formatage automatique
  - **isort** : Tri des imports
  - **Flake8** : Linting PEP8
  - **Pylint** : Analyse qualité avancée
  - **Bandit** : Analyse sécurité
  - **Radon** : Complexité cyclomatique

#### 3. Workflow Déploiement (`ci.yml` - job `deploy`)
- **Déclencheur** : Push sur `master` uniquement
- **Condition** : Tests et qualité réussis
- **Destination** : Streamlit Cloud (configuration manuelle requise)

## 🔧 Pre-commit Hooks

### Installation
```bash
# Installation automatique
python setup_ci_cd.py

# Ou installation manuelle
pip install pre-commit
pre-commit install
pre-commit install --install-hooks
```

### Hooks configurés

| Hook | Description | Configuration |
|------|-------------|---------------|
| `trailing-whitespace` | Supprime les espaces en fin de ligne | Automatique |
| `end-of-file-fixer` | Assure la présence d'un saut de ligne final | Automatique |
| `black` | Formatage PEP8 automatique | `--line-length=88` |
| `isort` | Tri automatique des imports | `--profile black` |
| `flake8` | Vérification PEP8 | `--max-line-length=88` |
| `pylint` | Analyse qualité avancée | `--output-format=text` |
| `bandit` | Analyse sécurité | `-r app/` (exclut `tests/`) |
| `radon` | Complexité cyclomatique | `--min C --show-complexity` |
| `pytest` | Tests automatiques | `--cov=app --cov-report=term-missing` |

### Utilisation courante
```bash
# Exécuter tous les hooks
pre-commit run --all-files

# Exécuter un hook spécifique
pre-commit run black

# Exécuter sur les fichiers modifiés uniquement
pre-commit run

# Mettre à jour les versions des hooks
pre-commit autoupdate
```

## 📊 Métriques et Rapports

### Couverture de Code
- **Outil** : pytest-cov + Codecov
- **Seuil actuel** : 25% (en progression)
- **Objectif** : 80%+
- **Rapport** : Automatique sur chaque PR

### Qualité du Code
- **Pylint Score** : 8.24/10 (objectif 9.0/10)
- **Sécurité** : 0 vulnérabilités (Bandit)
- **Complexité** : Surveillance des fonctions > 10

### Tests
- **Framework** : pytest avec xdist
- **Parallélisation** : Automatique (`-n auto`)
- **Types** : Unitaires, fonctionnels, intégration
- **Nombre** : 296 tests actifs

## 🚀 Déploiement

### Environnements
- **Développement** : Locale avec hot-reload
- **Staging** : Tests automatisés
- **Production** : Streamlit Cloud

### Configuration Déploiement
```yaml
# .github/workflows/ci.yml - Job deploy
deploy:
  runs-on: ubuntu-latest
  needs: [test, quality]
  if: github.ref == 'refs/heads/master'
  steps:
    - name: Deploy to Streamlit Cloud
      run: echo "Configuration Streamlit Cloud manuelle requise"
```

### Variables d'environnement
```bash
# Variables à configurer dans GitHub Secrets
STREAMLIT_CLOUD_TOKEN=your_token_here
STREAMLIT_APP_ID=your_app_id_here
```

## 🔍 Debugging et Dépannage

### Échec des Tests
```bash
# Exécution locale détaillée
python -m pytest tests/ -v --tb=long

# Tests spécifiques
python -m pytest tests/test_consultants.py -v

# Avec couverture
python -m pytest tests/ --cov=app --cov-report=html
```

### Problèmes de Qualité
```bash
# Vérification Black
black --check --diff app/

# Vérification Pylint
pylint app/ --output-format=text

# Analyse sécurité
bandit -r app/ -f json
```

### Problèmes de Performance
```bash
# Tests de performance
python -m pytest tests/ --durations=10

# Complexité du code
radon cc app/ -a -s
```

## 📈 Optimisations

### Cache et Performance
- **Dépendances pip** : Cache automatique GitHub Actions
- **Tests parallèles** : Utilisation optimale des cœurs CPU
- **Hooks sélectifs** : Exécution uniquement sur fichiers modifiés

### Métriques de Suivi
```bash
# Couverture par module
python -m pytest tests/ --cov=app --cov-report=term-missing

# Temps d'exécution des tests
python -m pytest tests/ --durations=0

# Complexité cyclomatique
radon cc app/ -a
```

## 🔒 Sécurité

### Analyse Automatisée
- **Bandit** : Détection de vulnérabilités connues
- **Audit des dépendances** : Via pip-audit (prévu)
- **Secrets** : Scan automatique des commits

### Bonnes Pratiques
- Pas de secrets hardcodés
- Validation des inputs
- Gestion sécurisée des fichiers
- Audit des permissions

## 📚 Ressources

### Documentation
- [GitHub Actions](https://docs.github.com/en/actions)
- [Pre-commit](https://pre-commit.com/)
- [Pytest](https://docs.pytest.org/)
- [Codecov](https://docs.codecov.io/)

### Outils Recommandés
- **VS Code** : Extension Python, Pylint, Black
- **PyCharm** : Intégration native des outils
- **GitHub Desktop** : Gestion des commits

## 🎯 Prochaines Améliorations

### Phase 5 - CI/CD Avancé
- [ ] Déploiement automatisé complet
- [ ] Tests de performance automatisés
- [ ] Intégration SonarCloud
- [ ] Notifications Slack/Discord
- [ ] Environnements multiples (dev/staging/prod)

### Métriques Cibles
- **Couverture** : 80%+
- **Temps CI** : < 10 minutes
- **Score Qualité** : 9.0/10+
- **Tests** : 400+ tests

---

*Guide mis à jour le : 15 septembre 2025*
