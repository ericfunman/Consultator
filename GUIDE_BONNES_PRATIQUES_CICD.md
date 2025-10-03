# 🚀 Guide des Bonnes Pratiques CI/CD - Consultator

Ce guide vous aide à éviter les échecs de pipeline CI/CD en validant votre code **avant** de pousser.

## 📋 Table des matières
1. [Validation rapide avant push](#validation-rapide)
2. [Formatage automatique du code](#formatage-automatique)
3. [Résolution des problèmes courants](#problèmes-courants)
4. [Configuration locale vs CI/CD](#configuration)

---

## 🎯 Validation rapide avant push

### Option 1: Script automatique (recommandé)

**Windows (PowerShell):**
```powershell
.\validate_before_push.ps1
```

**Linux/Mac:**
```bash
chmod +x validate_before_push.sh
./validate_before_push.sh
```

### Option 2: Commandes manuelles

```bash
# 1. Vérifier le formatage Black
python -m black --check --diff --line-length 120 app/ tests/

# 2. Vérifier l'ordre des imports (optionnel)
python -m isort --check-only --diff app/ tests/

# 3. Vérifier le linting (optionnel)
python -m flake8 app/ --max-line-length=150

# 4. Lancer les tests de régression
python -m pytest tests/regression/ -v
```

---

## 🎨 Formatage automatique du code

### Formater tout le projet d'un coup

```bash
# Black (formatage principal - OBLIGATOIRE)
python -m black app/ tests/ --line-length 120

# isort (ordre des imports - RECOMMANDÉ)
python -m isort app/ tests/
```

### Formater uniquement les fichiers modifiés

```bash
# Lister les fichiers modifiés
git diff --name-only

# Formater seulement ces fichiers
python -m black <fichier1.py> <fichier2.py> --line-length 120
python -m isort <fichier1.py> <fichier2.py>
```

---

## 🔧 Résolution des problèmes courants

### ❌ Erreur: "would reformat" (Black)

**Problème:** Votre code n'est pas formaté selon les standards Black.

**Solution:**
```bash
# Formater automatiquement
python -m black app/ tests/ --line-length 120

# Vérifier que c'est corrigé
python -m black --check app/ tests/ --line-length 120

# Commiter les changements
git add -A
git commit -m "Format: Black formatting"
git push origin master
```

### ⚠️ Avertissement: "Imports incorrectly sorted" (isort)

**Problème:** L'ordre des imports ne suit pas les conventions.

**Solution:**
```bash
# Réorganiser automatiquement
python -m isort app/ tests/

# Vérifier
python -m isort --check-only app/ tests/

# Commiter si nécessaire
git add -A
git commit -m "Fix: isort imports ordering"
```

**Note:** isort est **non-bloquant** dans le CI/CD, mais recommandé.

### 🧪 Erreur: Tests de régression échouent

**Problème:** Modifications qui cassent les tests existants.

**Solution:**
```bash
# Lancer les tests en local
python -m pytest tests/regression/ -v --tb=short

# Identifier le test qui échoue
python -m pytest tests/regression/test_xxx.py::test_function -v

# Corriger le code ou le test
# ...

# Relancer les tests
python -m pytest tests/regression/ -v
```

---

## ⚙️ Configuration locale vs CI/CD

### Fichiers de configuration importants

| Fichier | Rôle | Valeur critique |
|---------|------|-----------------|
| `.isort.cfg` | Configuration isort | `line_length = 120` |
| `pyproject.toml` | Configuration Black (si existe) | `line-length = 120` |
| `.github/workflows/main-pipeline.yml` | Pipeline CI/CD complet | Jobs quality-checks |
| `.github/workflows/tests-simplified.yml` | Tests rapides | Tests uniquement |

### Vérifier l'alignement de configuration

```bash
# Vérifier la config isort
cat .isort.cfg | grep line_length
# Doit afficher: line_length = 120

# Vérifier que Black utilise 120
python -m black --version
python -m black --help | grep line-length
```

### Installer les outils en local

```bash
# Installer tous les outils de qualité
pip install -r requirements-test.txt

# Ou individuellement
pip install black isort flake8 pylint bandit pytest pytest-cov
```

---

## 🎯 Workflow recommandé

```bash
# 1. Avant de commencer à coder
git pull origin master

# 2. Créer une branche (optionnel mais recommandé)
git checkout -b feature/ma-fonctionnalite

# 3. Coder normalement
# ... (votre code)

# 4. Formater le code
python -m black app/ tests/ --line-length 120
python -m isort app/ tests/

# 5. Valider en local
.\validate_before_push.ps1  # Windows
# OU
./validate_before_push.sh   # Linux/Mac

# 6. Commiter
git add -A
git commit -m "Feature: Description de la fonctionnalité"

# 7. Pousser
git push origin master
# OU
git push origin feature/ma-fonctionnalite
```

---

## 🆘 En cas d'urgence

Si le CI/CD échoue après un push :

1. **Voir les logs GitHub Actions:**
   ```
   https://github.com/ericfunman/Consultator/actions
   ```

2. **Corriger localement:**
   ```bash
   # Formater
   python -m black app/ tests/ --line-length 120
   python -m isort app/ tests/
   
   # Valider
   .\validate_before_push.ps1
   
   # Pousser la correction
   git add -A
   git commit -m "Fix: CI/CD formatting issues"
   git push origin master
   ```

3. **Script de diagnostic:**
   ```bash
   python check_ci_no_ssl.py
   ```

---

## 📚 Ressources

- **Black**: https://black.readthedocs.io/
- **isort**: https://pycqa.github.io/isort/
- **Flake8**: https://flake8.pycqa.org/
- **GitHub Actions**: https://docs.github.com/actions

---

## 💡 Conseils supplémentaires

### Activer le formatage automatique dans VS Code

Ajoutez dans `.vscode/settings.json`:
```json
{
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "120"],
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### Utiliser pre-commit hooks

Les hooks pre-commit sont déjà configurés ! Ils se lancent automatiquement à chaque commit.

Si besoin de les réactiver:
```bash
# Windows
activate_git_hooks.bat

# Linux/Mac
chmod +x .git/hooks/pre-commit
```

---

**Dernière mise à jour:** 3 octobre 2025  
**Version:** 1.0  
**Auteur:** Consultator Team
