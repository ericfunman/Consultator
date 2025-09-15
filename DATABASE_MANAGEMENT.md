# 🗄️ Guide de Gestion de la Base de Données

## ⚠️ ATTENTION IMPORTANTE

**Vos données sont précieuses !** Ce guide explique comment gérer la base de données en toute sécurité.

## 📊 État actuel de la base de données

✅ **Base de données restaurée avec succès :**
- 👥 **1000 consultants** (données réalistes générées)
- 🎯 **12 553 missions** (liées aux consultants)
- 🏢 **8 practices** (Data Engineering, Data Science, etc.)
- 📄 **1979 CVs** (documents associés)
- 👨‍💼 **10 business managers**
- 🔧 **41 compétences** (techniques et fonctionnelles)

## 🛠️ Tâches VS Code disponibles

### Tâches sûres (recommandées)
- **🚀 Run Consultator** : Lance l'application
- **📦 Install Dependencies** : Installe les dépendances
- **🗃️ Init Database** : Initialise la structure (sans supprimer les données)
- **🧪 Run Tests (Parallel)** : Exécute les tests en parallèle
- **🧪 Run Tests (Sequential)** : Exécute les tests séquentiellement
- **💾 Backup Database** : Crée une sauvegarde avant les opérations dangereuses
- **🔄 Restore Test Data** : Restaure les données de test (si nécessaire)

### ⚠️ Tâche dangereuse (à éviter)
- **🧹 ⚠️ RESET Database** : **SUPPRIME TOUTES LES DONNÉES** - À utiliser seulement si vous voulez repartir de zéro

## 🔄 Procédures recommandées

### Pour travailler en sécurité :
1. **Avant toute opération risquée** : Utilisez "💾 Backup Database"
2. **Pour restaurer les données** : Utilisez "🔄 Restore Test Data"
3. **Évitez** : "🧹 ⚠️ RESET Database" sauf si vous voulez vraiment tout supprimer

### Scripts disponibles :
- `generate_test_data.py` : Génère 1000 consultants avec données complètes
- `create_basic_test_data.py` : Génère des données de base
- `consultants_final.py` : Script alternatif pour les consultants

## 📈 Statistiques des données

Les données générées sont **réalistes et cohérentes** :
- Noms français (Dupont, Martin, Bernard, etc.)
- Emails professionnels (@email.com)
- Téléphones français (01xxxxxxxx)
- Salaires réalistes (45k-85k€)
- Compétences techniques actuelles
- Missions avec durées et tarifs réalistes

## 🔒 Sécurité des données

- ✅ **Sauvegarde automatique** recommandée avant les tests
- ✅ **Restauration facile** avec les scripts disponibles
- ✅ **Données cohérentes** pour les tests et développement
- ❌ **Pas de suppression accidentelle** grâce aux nouveaux noms de tâches

## 🚨 En cas de problème

Si vous perdez vos données :
1. Exécutez `python generate_test_data.py`
2. Ou utilisez la tâche VS Code "🔄 Restore Test Data"

---

**Rappel** : La tâche "🧹 ⚠️ RESET Database" supprime TOUT. Utilisez-la seulement si vous voulez repartir complètement de zéro !</content>
<parameter name="filePath">c:\Users\b302gja\Documents\Consultator en cours\Consultator\DATABASE_MANAGEMENT.md
