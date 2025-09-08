# 🧹 Nettoyeur d'Imports - Version Projet

Script spécialisé pour nettoyer automatiquement les imports inutilisés dans le projet Consultator uniquement.

## 🎯 Objectif

Nettoyer les imports inutilisés dans les fichiers du projet tout en préservant :
- Les dépendances externes (venv, site-packages)
- Les fichiers de test externes
- La stabilité du projet

## 📁 Fichiers créés

- `clean_imports_project.py` - Script Python principal
- `clean_imports_project.bat` - Script Windows pour exécution facile
- `IMPORT_CLEANER_PROJECT_README.md` - Cette documentation

## 🚀 Utilisation

### Mode Simulation (Recommandé)
```bash
# Via Python
python clean_imports_project.py --dry-run --verbose

# Via batch (Windows)
clean_imports_project.bat
```

### Mode Production
```bash
# Via Python
python clean_imports_project.py --dry-run=False --verbose

# Via batch (Windows)
clean_imports_project.bat --apply
```

## ⚙️ Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Mode simulation (défaut) |
| `--dry-run=False` | Applique les changements |
| `--no-backup` | Désactive les sauvegardes |
| `--verbose` | Mode détaillé |

## 🔍 Analyse des fichiers

Le script analyse uniquement :
- ✅ `app/` - Code principal de l'application
- ✅ `config/` - Configuration
- ✅ `scripts/` - Scripts utilitaires
- ✅ `utils/` - Utilitaires
- ✅ `components/` - Composants
- ✅ `main.py`, `run.py` - Points d'entrée

Exclut automatiquement :
- ❌ `__pycache__/`, `.git/`, `venv/`
- ❌ `site-packages/`, `Scripts/`
- ❌ Fichiers de test externes
- ❌ Dépendances externes

## 🛡️ Sécurité

### Sauvegardes automatiques
- Créées dans `backups/imports_cleaning_project/`
- Timestampées automatiquement
- Possibilité de restauration facile

### Mode simulation
- Analyse complète sans modification
- Rapport détaillé des changements prévus
- Validation avant application

### Gestion d'erreurs
- Détection des erreurs de parsing
- Continuation malgré les erreurs individuelles
- Rapport d'erreurs détaillé

## 📊 Exemple de sortie

```
🔍 Démarrage de l'analyse des imports du projet...
📁 Projet: C:\Users\b302gja\Documents\Consultatorv1.5.1\Consultator
📄 45 fichiers Python du projet trouvés

⚠️  app/services/consultant_service.py: 3 imports inutilisés
  - Import inutilisé: typing.List
  - Import inutilisé: typing.Optional
  - Import inutilisé: datetime

🧹 Simulation du nettoyage (DRY RUN)...
📊 12 imports inutilisés trouvés dans 8 fichiers du projet

📊 RÉSUMÉ DU NETTOYAGE DES IMPORTS - PROJET
============================================================
📄 Fichiers analysés: 45
🔧 Fichiers modifiés: 0 (dry-run)
🗑️  Imports supprimés: 0 (dry-run)
❌ Erreurs: 0
💾 Sauvegardes: backups/imports_cleaning_project
============================================================
```

## 🔧 Algorithme d'analyse

1. **Parcours AST** : Analyse syntaxique du code Python
2. **Collecte des imports** : Identification de tous les imports
3. **Collecte des usages** : Détection des noms utilisés
4. **Vérification commentaires** : Recherche dans docstrings/commentaires
5. **Filtrage intelligent** : Exclusion des faux positifs

## ⚠️ Précautions

### Avant l'exécution
```bash
# Faire un commit propre
git add .
git commit -m "Before import cleaning"

# Sauvegarder manuellement si nécessaire
cp -r app/ app_backup/
```

### Après le nettoyage
```bash
# Vérifier que l'application fonctionne
python run.py

# Lancer les tests
python -m pytest

# Vérifier les changements
git diff
```

### ⚠️ **Important : Annotations de type**
Le script peut supprimer des imports de `typing` utilisés uniquement dans les annotations de type. Vérifiez toujours :
- `List`, `Dict`, `Optional`, `Union` utilisés dans les type hints
- Restaurez-les manuellement si nécessaire depuis les sauvegardes

## 🐛 Dépannage

### Erreurs communes

**"Module not found" après nettoyage**
- Vérifier que l'import était vraiment inutilisé
- Restaurer depuis la sauvegarde
- Ajouter l'import manuellement si nécessaire

**Erreur de syntaxe**
- Le script préserve la syntaxe Python
- Vérifier le fichier original en cas de problème

**Faux positifs**
- Imports utilisés dans les commentaires/docstrings sont préservés
- Imports conditionnels sont analysés avec soin

### Récupération
```bash
# Restaurer depuis les sauvegardes
cp backups/imports_cleaning_project/app/* app/

# Ou restaurer depuis git
git checkout HEAD~1 -- app/
```

## 📈 Métriques

Le script fournit des métriques détaillées :
- Nombre de fichiers analysés
- Nombre d'imports supprimés par fichier
- Taux de succès
- Erreurs rencontrées

## 🔄 Intégration CI/CD

Pour intégrer dans un pipeline :

```yaml
# .github/workflows/clean-imports.yml
name: Clean Imports
on: [push]

jobs:
  clean-imports:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Clean imports
        run: python clean_imports_project.py --dry-run=False
      - name: Run tests
        run: python -m pytest
```

## 📝 Logs

Les logs sont enregistrés avec différents niveaux :
- `INFO` : Informations générales
- `WARNING` : Avertissements
- `ERROR` : Erreurs
- `DEBUG` : Informations détaillées (--verbose)

## 🎯 Recommandations

1. **Toujours commencer par un dry-run**
2. **Faire un commit avant les changements**
3. **Tester l'application après nettoyage**
4. **Vérifier les métriques de performance**
5. **Documenter les changements majeurs**

## 📞 Support

En cas de problème :
1. Vérifier les logs détaillés
2. Restaurer depuis les sauvegardes
3. Consulter cette documentation
4. Ouvrir une issue sur le repository

---

*Script créé pour le projet Consultator v1.5.1*
