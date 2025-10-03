# 🚀 Guide Rapide - Dashboards Consultator

## ⚡ Démarrage en 3 Minutes

### 1️⃣ Créer un Dashboard (30 secondes)

```
Business Managers → 📊 Dashboard → ⚙️ Gestion → ➕ Créer mon premier dashboard
```

**Formulaire :**
- Nom : "Mon Dashboard"
- Description : "Vue d'ensemble"
- Rôle : Practice Manager
- ✅ Créer

### 2️⃣ Ajouter des Widgets (1 minute)

```
📊 Dashboard → 🎨 Builder Avancé
```

**Étapes :**
1. Sélectionner votre dashboard dans la liste déroulante
2. Cliquer sur **✏️ Éditer**
3. Parcourir le **Catalogue de Widgets** (onglets par catégorie)
4. Cliquer sur un widget pour le sélectionner (bordure bleue)
5. Configurer :
   - **Taille (Span)** : Largeur en colonnes (ex: 2)
   - **Hauteur** : Nombre de lignes (ex: 3)
   - **Paramètres** : Selon le widget (période, nombre de résultats...)
6. Cliquer sur **➕ Ajouter le widget**
7. Répéter pour ajouter d'autres widgets

### 3️⃣ Visualiser (30 secondes)

```
📊 Dashboard → 👁️ Visualisation
```

**Actions :**
- Sélectionner votre dashboard
- Cliquer sur **🔄 Actualiser** pour rafraîchir les données
- Admirer votre travail ! 🎉

---

## 🎯 Widgets Essentiels pour Débuter

### Dashboard "Vue d'Ensemble"

| Widget | Catégorie | Span | Height | Paramètres |
|--------|-----------|------|--------|------------|
| **Total Consultants** | 📊 Métriques | 1 | 2 | - |
| **Missions Actives** | 💼 Missions | 1 | 2 | - |
| **CA Total** | 💰 Revenus | 1 | 2 | - |
| **Taux Disponibilité** | 📊 Métriques | 1 | 2 | - |
| **Revenus Mensuels** | 💰 Revenus | 2 | 3 | Période: 6 mois |
| **Top Clients** | 💼 Missions | 2 | 3 | Nombre: 10 |

**Temps de création** : ~5 minutes

### Dashboard "Business Managers"

| Widget | Catégorie | Span | Height | Paramètres |
|--------|-----------|------|--------|------------|
| **Total BM** | 👥 BM | 1 | 2 | - |
| **Performance BM** | 👥 BM | 2 | 4 | Nombre: 10 |
| **Revenus par BM** | 💰 Revenus | 2 | 4 | Période: 3 mois |
| **Consultants par BM** | 👥 BM | 1 | 3 | - |

**Temps de création** : ~4 minutes

---

## 🔧 Réorganiser les Widgets

### ⚠️ Le Drag & Drop n'est PAS implémenté

**Méthodes disponibles :**

#### Méthode 1 : Boutons Monter/Descendre
1. Dans la liste des widgets du dashboard
2. Utiliser **⬆️ Monter** ou **⬇️ Descendre**
3. Chaque clic déplace le widget d'une position

#### Méthode 2 : Supprimer et Recréer
1. Supprimer le widget mal placé (**🗑️**)
2. Le recréer dans l'ordre souhaité

#### Méthode 3 : Éditer la Configuration JSON (Avancé)
1. Aller dans **⚙️ Gestion** → **Liste des Dashboards**
2. Cliquer sur **✏️ Éditer**
3. Modifier manuellement le JSON `grid_config`
4. Sauvegarder

---

## ❌ Erreurs Courantes et Solutions

### ❌ "type 'property' is not supported"
**Cause** : Bug dans le calcul des revenus
**Solution** : ✅ **CORRIGÉ** - Redémarrer l'app :
```powershell
Stop-Process -Name python -Force
python run.py
```

### ❌ Le bouton "Créer mon premier dashboard" ne fait rien
**Solution** :
1. Recharger la page (F5)
2. Vérifier l'onglet actif (**⚙️ Gestion**)
3. Utiliser **🎨 Builder Avancé** → **➕ Nouveau Dashboard**

### ❌ Les widgets ne s'affichent pas
**Vérifications** :
- Avez-vous des consultants/missions en base ?
- Le rôle d'accès correspond-il à votre profil ?
- Actualiser le dashboard avec **🔄**

### ❌ Impossible de glisser-déposer des widgets
**Normal !** Le drag & drop n'est pas implémenté.
**Utiliser** : Boutons ⬆️⬇️ ou supprimer/recréer

---

## 📊 Catalogue des 20 Widgets

### 📊 Métriques Consultants (4)
1. **Total Consultants** - Nombre total avec évolution
2. **Top Compétences** - Compétences les plus fréquentes
3. **Consultants par Entité** - Répartition organisationnelle
4. **Taux de Disponibilité** - % consultants disponibles

### 💼 Missions (4)
5. **Missions Actives** - Nombre de missions en cours
6. **Timeline Missions** - Chronologie des missions
7. **Top Clients** - Clients générant le plus de CA
8. **TJM Moyen** - Taux Journalier Moyen par compétence

### 💰 Revenus (4)
9. **CA Total** - Chiffre d'affaires estimé
10. **Revenus Mensuels** - Évolution mensuelle
11. **Revenus par Consultant** - Top 10 générateurs de CA
12. **Revenus par BM** - Performance par Business Manager

### 👥 Business Managers (4)
13. **Total BM** - Nombre de BM actifs
14. **Performance BM** - Classement par CA
15. **Consultants par BM** - Répartition des consultants
16. **Taux de Remplissage** - % consultants en mission

### 📈 Analytics Avancés (4)
17. **Heatmap Compétences** - Carte thermique
18. **Prédiction CA** - Prévisions IA
19. **Analyse Temporelle** - Tendances multi-périodes
20. **KPIs Personnalisés** - Indicateurs configurables

---

## 💡 Astuces Pro

### ⚡ Performances
- **Max 8-10 widgets** par dashboard pour éviter les lenteurs
- **Actualiser régulièrement** pour voir les nouvelles données
- **Éviter les widgets lourds** (heatmap, prédiction) en grand nombre

### 🎨 Design
- **Hiérarchie visuelle** : Métriques importantes en haut à gauche
- **Cohérence** : Grouper les widgets de même catégorie
- **Lisibilité** : Ne pas surcharger, privilégier plusieurs dashboards

### 🔄 Workflow
1. **Créer un template** : Dashboard type à dupliquer
2. **Tester avec peu de widgets** : Valider avant d'ajouter
3. **Sauvegarder régulièrement** : Pas de brouillon automatique
4. **Dupliquer avant grosse modif** : Garder une copie de secours

---

## 🆘 Support Rapide

### Commandes Utiles

**Redémarrer l'app** :
```powershell
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
python run.py
```

**Vérifier les versions** :
```bash
streamlit --version  # Nécessite ≥ 1.28
python --version      # Nécessite ≥ 3.8
```

**Logs** :
Consulter le terminal où tourne `python run.py` pour les erreurs

### Ressources

- **Notice complète** : `NOTICE_DASHBOARD.md`
- **Guide système** : `DASHBOARD_SYSTEM_GUIDE.md`
- **Code source** :
  - Widgets : `app/services/widget_factory.py`
  - Service : `app/services/dashboard_service.py`
  - Interface : `app/pages_modules/dashboard_page.py`

---

## ✅ Checklist Rapide

**Avant de commencer** :
- [ ] Application lancée (`python run.py`)
- [ ] Naviguer vers Business Managers → Dashboard
- [ ] Au moins 1 consultant en base de données

**Création** :
- [ ] Dashboard créé via **⚙️ Gestion**
- [ ] 3-4 widgets ajoutés via **🎨 Builder**
- [ ] Configuration sauvegardée

**Vérification** :
- [ ] Dashboard visible dans **👁️ Visualisation**
- [ ] Données affichées correctement
- [ ] Pas d'erreur dans le terminal

---

**🎯 Objectif** : Dashboard fonctionnel en moins de 5 minutes !

**📖 Documentation complète** : Voir `NOTICE_DASHBOARD.md` pour tous les détails.
