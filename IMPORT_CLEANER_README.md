# 🧹 Nettoyeur Automatique d'Imports Python

Script intelligent pour nettoyer automatiquement les imports inutilisés dans votre projet Python.

## 📋 Fonctionnalités

- 🔍 **Analyse intelligente** : Détecte les imports utilisés et non utilisés
- 🧹 **Nettoyage automatique** : Supprime les imports inutilisés
- 💾 **Sauvegardes automatiques** : Préserve vos fichiers avant modification
- 📊 **Rapports détaillés** : Statistiques complètes des opérations
- ⚡ **Mode simulation** : Testez avant d'appliquer les changements

## 🚀 Utilisation Rapide

### Windows (recommandé)
```bash
# Double-cliquez sur clean_imports.bat
# OU lancez depuis l'invite de commande:
clean_imports.bat
```

### Python direct
```bash
# Analyse seulement (simulation)
python clean_imports.py --dry-run

# Nettoyage avec sauvegardes
python clean_imports.py --dry-run=false

# Mode verbeux
python clean_imports.py --verbose
```

## 📖 Options Disponibles

| Option | Description | Défaut |
|--------|-------------|---------|
| `--project-root` | Racine du projet | `.` |
| `--dry-run` | Mode simulation | `True` |
| `--no-backup` | Désactiver sauvegardes | `False` |
| `--verbose` | Mode détaillé | `False` |

## 🎯 Exemples d'utilisation

### 1. Analyse de sécurité (recommandé)
```bash
python clean_imports.py --dry-run --verbose
```
- Analyse tous les fichiers
- Affiche les imports à supprimer
- Aucune modification réelle

### 2. Nettoyage complet
```bash
python clean_imports.py --dry-run=false --verbose
```
- Supprime automatiquement les imports inutilisés
- Crée des sauvegardes dans `backups/imports_cleaning/`
- Affiche un rapport détaillé

### 3. Nettoyage d'un sous-dossier
```bash
python clean_imports.py --project-root=app/services --dry-run=false
```
- Nettoie seulement le dossier spécifié
- Utile pour les gros projets

## 📊 Que détecte le script ?

### ✅ Imports correctement identifiés
```python
# Import utilisé
import os
print(os.path.join("a", "b"))

# Import avec alias utilisé
from datetime import datetime as dt
now = dt.now()

# Import dans les commentaires (conservé)
import json  # Utilisé dans la docstring
```

### ❌ Imports détectés comme inutilisés
```python
# Import non utilisé
import sys  # Jamais utilisé dans le code

# Import partiellement utilisé
from typing import List, Dict, Optional  # Seule List est utilisée
```

## 🛡️ Sécurité et Sauvegardes

### Sauvegardes automatiques
- Créées dans `backups/imports_cleaning/`
- Structure identique au projet original
- Possibilité de restaurer facilement

### Mode simulation
- `--dry-run=true` : Aucune modification
- Analyse complète sans risque
- Rapport détaillé des changements proposés

## 📈 Statistiques et Rapports

Le script fournit des métriques détaillées :
```
📊 RÉSUMÉ DU NETTOYAGE DES IMPORTS
==================================================
📄 Fichiers analysés: 45
🔧 Fichiers modifiés: 12
🗑️  Imports supprimés: 87
❌ Erreurs: 0
💾 Sauvegardes: backups/imports_cleaning/
```

## ⚠️ Précautions d'usage

### Avant utilisation :
1. **Committez vos changements** : `git commit -m "before import cleaning"`
2. **Testez en mode simulation** : `--dry-run`
3. **Vérifiez les sauvegardes** : dans `backups/imports_cleaning/`

### Limitations connues :
- Détection limitée pour les imports dynamiques
- Ne traite pas les `__all__` exports
- Imports conditionnels peuvent être mal détectés

## 🔧 Dépannage

### Erreur "Python not found"
```bash
# Vérifiez l'installation de Python
python --version

# Ou utilisez le chemin complet
C:\Python39\python.exe clean_imports.py
```

### Erreur de permissions
```bash
# Lancez en mode administrateur
# Ou vérifiez les droits sur le dossier
```

### Faux positifs
Si des imports sont détectés comme inutilisés mais le sont réellement :
```python
# Ajoutez un commentaire pour les préserver
import rarely_used_module  # noqa: utilisé dans __init__.py
```

## 🎯 Intégration CI/CD

### GitHub Actions
```yaml
- name: Clean unused imports
  run: python clean_imports.py --dry-run=false
```

### Pre-commit hook
```bash
#!/bin/sh
python clean_imports.py --dry-run
```

## 📝 Format des sauvegardes

```
backups/imports_cleaning/
├── app/
│   ├── services/
│   │   └── consultant_service.py.backup
│   └── pages_modules/
│       └── consultants.py.backup
└── utils/
    └── skill_categories.py.backup
```

## 🤝 Contribution

Pour améliorer le script :
1. Fork le projet
2. Créez une branche feature
3. Testez vos modifications
4. Soumettez une PR

## 📄 Licence

MIT License - Utilisez librement !

---

**💡 Conseil** : Commencez toujours par le mode `--dry-run` pour voir les changements proposés avant de les appliquer !
