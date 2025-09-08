# 🔧 Guide des Hooks Pre-commit pour Consultator

## 📋 Vue d'ensemble

Les hooks pre-commit sont des scripts qui s'exécutent automatiquement avant chaque commit Git. Ils permettent de maintenir automatiquement la qualité du code en vérifiant et corrigeant les problèmes courants.

## 🎯 Objectifs

- **Qualité de code** : Vérifications automatiques avec pylint et flake8
- **Formatage** : Formatage automatique avec Black et tri des imports avec isort
- **Sécurité** : Analyse des vulnérabilités avec bandit
- **Types** : Vérification des annotations de type avec mypy
- **Documentation** : Vérification des docstrings avec pydocstyle

## 📁 Fichiers créés

- `.pre-commit-config.yaml` - Configuration des hooks
- `install_precommit.bat` - Script d'installation Windows
- `install_precommit.sh` - Script d'installation Linux/Mac
- `requirements-dev.txt` - Dépendances mises à jour

## 🚀 Installation

### Windows
```bash
# Double-cliquez sur install_precommit.bat
# ou exécutez dans un terminal :
install_precommit.bat
```

### Linux/Mac
```bash
# Rendez le script exécutable
chmod +x install_precommit.sh

# Exécutez le script
./install_precommit.sh
```

### Installation manuelle
```bash
# Installer pre-commit
pip install pre-commit

# Installer les hooks
pre-commit install

# Tester sur tous les fichiers
pre-commit run --all-files
```

## ⚙️ Hooks configurés

### 1. **Vérifications générales** (pre-commit-hooks)
- ✅ Suppression des espaces en fin de ligne
- ✅ Correction des fins de fichier
- ✅ Validation des fichiers YAML
- ✅ Détection des gros fichiers (>500KB)
- ✅ Détection des conflits de merge
- ✅ Détection des statements de debug

### 2. **Formatage automatique** (Black)
- ✅ Formatage PEP 8 automatique
- ✅ Longueur de ligne : 88 caractères
- ✅ Compatible avec les autres outils

### 3. **Tri des imports** (isort)
- ✅ Tri automatique des imports
- ✅ Compatible avec Black
- ✅ Mode vérification uniquement (pas de modification auto)

### 4. **Analyse de code** (flake8)
- ✅ Vérification PEP 8
- ✅ Détection des erreurs de code
- ✅ Extensions : docstrings, bugbear, comprehensions

### 5. **Analyse approfondie** (pylint)
- ✅ Analyse statique complète
- ✅ Utilise la configuration `.pylintrc` existante
- ✅ Désactive certains warnings pour APIs

### 6. **Vérification des types** (mypy)
- ✅ Vérification des annotations de type
- ✅ Ignore les imports manquants
- ✅ Mode optionnel non-strict

### 7. **Sécurité** (bandit)
- ✅ Détection des vulnérabilités
- ✅ Analyse des patterns dangereux
- ✅ Exclut les fichiers de test

### 8. **Documentation** (pydocstyle)
- ✅ Vérification des docstrings PEP 257
- ✅ Convention NumPy
- ✅ Exclut les fichiers génériques

## 📂 Fichiers inclus/exclus

### ✅ **Fichiers analysés**
- `app/*.py` - Code principal
- `config/*.py` - Configuration
- `scripts/*.py` - Scripts utilitaires
- `utils/*.py` - Utilitaires
- `components/*.py` - Composants
- `main.py`, `run.py` - Points d'entrée
- Fichiers de configuration Python

### ❌ **Fichiers exclus**
- `__pycache__/` - Cache Python
- `.venv/`, `venv/` - Environnements virtuels
- `backups/` - Sauvegardes
- `*.db`, `*.sqlite*` - Bases de données
- `*.log`, `*.tmp` - Fichiers temporaires
- Fichiers de test (optionnel)

## 🎮 Utilisation quotidienne

### Commit normal
```bash
# Les hooks s'exécutent automatiquement
git add .
git commit -m "Mon message de commit"
```

### Exécution manuelle
```bash
# Vérifier tous les fichiers
pre-commit run --all-files

# Vérifier un fichier spécifique
pre-commit run --files app/main.py

# Vérifier les fichiers modifiés
pre-commit run
```

### Désactiver temporairement
```bash
# Pour les commits urgents (à éviter)
git commit --no-verify -m "Commit urgent"
```

## 🔧 Personnalisation

### Modifier la configuration
Éditez `.pre-commit-config.yaml` pour :
- Ajouter/supprimer des hooks
- Modifier les arguments
- Changer les exclusions

### Désactiver un hook
```yaml
# Dans .pre-commit-config.yaml
- id: pylint
  # Ajouter cette ligne pour désactiver
  # pass_filenames: false
```

### Hooks conditionnels
```yaml
# Exécuter seulement sur certains fichiers
- id: mypy
  files: ^(app|config)/
```

## 🐛 Dépannage

### Erreurs communes

**"pre-commit not found"**
```bash
pip install pre-commit
```

**Hooks qui échouent**
- Corrigez les erreurs signalées
- Ou ajustez la configuration pour être moins strict
- Ou désactivez temporairement avec `--no-verify`

**Faux positifs**
- Ajustez les exclusions dans `.pre-commit-config.yaml`
- Modifiez les arguments des hooks

**Performance lente**
- Réduisez le nombre de hooks
- Utilisez `pre-commit run --files <fichier>` pour les tests
- Excluez plus de répertoires

### Réinitialisation
```bash
# Désinstaller les hooks
pre-commit uninstall

# Supprimer le cache
pre-commit clean

# Réinstaller
pre-commit install
```

## 📊 Métriques et rapports

### Voir les résultats
```bash
# Résumé des hooks
pre-commit run --all-files --verbose

# Statistiques
pre-commit run --all-files 2>&1 | grep -E "(passed|failed|skipped)"
```

### Intégration CI/CD
```yaml
# .github/workflows/pre-commit.yml
name: Pre-commit checks
on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - name: Run pre-commit
        run: |
          pip install pre-commit
          pre-commit run --all-files
```

## 🎯 Bonnes pratiques

### Pour les développeurs
1. **Commitez régulièrement** - Les vérifications sont plus rapides
2. **Corrigez immédiatement** - Ne laissez pas s'accumuler les erreurs
3. **Utilisez `--no-verify`** avec parcimonie
4. **Testez localement** avant de pousser

### Pour l'équipe
1. **Standardisez la configuration** - Tous utilisent la même
2. **Documentez les exceptions** - Pourquoi certains hooks sont désactivés
3. **Mettez à jour régulièrement** - Nouvelles versions des outils
4. **Formez l'équipe** - Comprendre les erreurs

### Performance
1. **Excluez les gros répertoires** - venv, node_modules, etc.
2. **Utilisez des hooks légers** - flake8 plutôt que pylint pour les gros projets
3. **Parallélisez** - pre-commit utilise plusieurs cœurs
4. **Cachez** - Les résultats sont mis en cache automatiquement

## 🔄 Mise à jour

### Mettre à jour pre-commit
```bash
pip install --upgrade pre-commit
```

### Mettre à jour les hooks
```bash
pre-commit autoupdate
```

### Mettre à jour la configuration
```bash
# Vérifier les nouvelles versions
pre-commit run --all-files --verbose
```

## 📞 Support

### Ressources
- [Documentation pre-commit](https://pre-commit.com/)
- [Configuration des hooks](https://pre-commit.com/hooks.html)
- [Guide pylint](https://pylint.readthedocs.io/)
- [Guide flake8](https://flake8.pycqa.org/)

### Commandes utiles
```bash
# Aide générale
pre-commit --help

# Liste des hooks installés
pre-commit run --help

# Voir la configuration
pre-commit validate-config
```

---

*Configuration créée pour le projet Consultator v1.5.1*
