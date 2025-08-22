# 🚀 Installation et Configuration - Consultator

## 📋 Prérequis

- Python 3.8+
- Git

## ⚡ Installation rapide

### 1. Cloner le repository
```bash
git clone https://github.com/ericfunman/Consultator.git
cd Consultator
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Initialiser la base de données
```bash
# Option A : Via le script Python
python -c "from app.database.database import init_database; init_database()"

# Option B : Via la tâche VS Code (si disponible)
# Ctrl+Shift+P -> "Tasks: Run Task" -> "🗃️ Init Database"
```

### 4. Lancer l'application
```bash
python run.py
```

L'application sera accessible sur http://localhost:8502

## 🗃️ Base de données

### Structure automatique
Au premier lancement, la base de données SQLite sera automatiquement créée dans :
```
data/consultator.db
```

### Tables créées automatiquement
- **consultants** : Informations des consultants
- **competences** : Compétences techniques et métier  
- **missions** : Historique des missions

### Données de test (optionnel)
Pour ajouter des données de démonstration :
```bash
# À implémenter si besoin
python scripts/populate_test_data.py
```

## 🔧 Configuration

### Variables d'environnement
Aucune configuration particulière requise pour un usage local.

### Port personnalisé
Pour changer le port par défaut (8502) :
```bash
# Modifier dans run.py ou utiliser
streamlit run app/main.py --server.port 8503
```

## ⚠️ Notes importantes

- La base de données `data/consultator.db` n'est **pas** versionnée sur Git (fichier local)
- Elle sera créée automatiquement au premier démarrage
- Pour remettre à zéro : utilisez la tâche "🧹 Clean Data" ou la fonction `reset_database()`

## 🛠️ Développement

Voir [DEVELOPMENT.md](DEVELOPMENT.md) pour les instructions de développement.
