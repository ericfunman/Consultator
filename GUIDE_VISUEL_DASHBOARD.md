# 🎯 Guide Visuel - Créer un Dashboard

## 🚀 Processus en 3 Étapes

### Étape 1️⃣ : Créer la Structure
**Où** : Business Managers → 📊 Dashboard → ⚙️ Gestion

1. Cliquer sur **"➕ Créer mon premier dashboard"**
2. Remplir le formulaire :
   - Nom : "Mon Dashboard"
   - Description : "Vue d'ensemble"
   - Rôle : Practice Manager
3. Cliquer **"✅ Créer Dashboard"**

**Résultat** : Dashboard vide créé ✅

---

### Étape 2️⃣ : Ajouter des Widgets
**Où** : Business Managers → 📊 Dashboard → 🎨 Builder Avancé

#### A. Sélectionner votre dashboard
1. Dans la **liste déroulante** en haut, choisir votre dashboard
2. Cliquer sur **"✏️ Éditer"**

#### B. Parcourir le catalogue (à gauche)
Le catalogue contient **20 widgets** organisés en **5 catégories** :

```
📊 Métriques Consultants
├─ Total Consultants
├─ Top Compétences
├─ Consultants par Entité
└─ Taux de Disponibilité

💼 Missions
├─ Missions Actives
├─ Timeline Missions
├─ Top Clients
└─ TJM Moyen

💰 Revenus
├─ CA Total
├─ Revenus Mensuels
├─ Revenus par Consultant
└─ Revenus par BM

👥 Business Managers
├─ Total BM
├─ Performance BM
├─ Consultants par BM
└─ Taux de Remplissage

📈 Analytics Avancés
├─ Heatmap Compétences
├─ Prédiction CA
├─ Analyse Temporelle
└─ KPIs Personnalisés
```

#### C. Sélectionner un widget
1. **Cliquer sur la carte widget** dans le catalogue
2. La carte s'affiche avec une **bordure bleue** (= sélectionné)
3. À droite, un panneau de configuration apparaît

#### D. Configurer le widget
**Taille (Span)** : Largeur en colonnes
- 1 = Petite largeur
- 2 = Moyenne largeur (recommandé)
- 3-4 = Grande largeur

**Hauteur** : Nombre de lignes verticales
- 1-2 = Petit widget (métriques simples)
- 3-4 = Moyen (graphiques)
- 5-8 = Grand (tableaux, heatmap)

**Paramètres** : Dépendent du widget
- Ex : "Revenus Mensuels" → Période (3, 6, 12 mois)
- Ex : "Top Clients" → Nombre (5, 10, 15)

#### E. Ajouter le widget
1. Cliquer sur **"➕ Ajouter le widget"**
2. Le widget apparaît **dans la grille centrale**
3. **Répéter** pour ajouter d'autres widgets

---

### Étape 3️⃣ : Visualiser et Réorganiser
**Où** : Business Managers → 📊 Dashboard → 👁️ Visualisation

#### Visualiser
1. Sélectionner votre dashboard dans la liste
2. Cliquer sur **"🔄 Actualiser"** pour rafraîchir les données
3. Admirer votre création ! 🎉

#### Réorganiser (si nécessaire)
**⚠️ Le glisser-déposer ne fonctionne PAS**

**Méthodes alternatives** :
1. **Boutons ⬆️⬇️** : Retourner en mode édition, utiliser les boutons
2. **Supprimer/Recréer** : Supprimer le widget mal placé, le recréer dans l'ordre
3. **Patience** : Planifier l'ordre avant d'ajouter les widgets

---

## 🎨 Exemple Pratique : Dashboard "Vue d'Ensemble"

### Configuration
- **Nom** : Vue d'Ensemble
- **Description** : Métriques clés de ma practice
- **6 widgets** organisés en grille 2×3

### Widgets à ajouter (dans l'ordre)

| # | Widget | Catégorie | Span | Height | Paramètres |
|---|--------|-----------|------|--------|------------|
| 1 | Total Consultants | 📊 Métriques | 1 | 2 | Aucun |
| 2 | Missions Actives | 💼 Missions | 1 | 2 | Aucun |
| 3 | CA Total | 💰 Revenus | 1 | 2 | Aucun |
| 4 | Taux Disponibilité | 📊 Métriques | 1 | 2 | Aucun |
| 5 | Revenus Mensuels | 💰 Revenus | 2 | 3 | Période: 6 mois |
| 6 | Top Clients | 💼 Missions | 2 | 3 | Nombre: 10 |

### Temps de création
**~8 minutes** pour un utilisateur débutant

---

## ❌ Erreurs Courantes

### "Je ne vois pas le catalogue de widgets"
**Solution** : 
1. Vérifier que vous êtes dans l'onglet **🎨 Builder Avancé**
2. Sélectionner un dashboard dans la liste déroulante
3. Cliquer sur **✏️ Éditer**
4. Le catalogue apparaît à gauche

### "Je clique sur un widget mais rien ne se passe"
**Vérifier** :
1. Êtes-vous en **mode édition** ? (bouton ✏️ cliqué)
2. La carte du widget a-t-elle une **bordure bleue** ?
3. Le panneau de configuration apparaît-il **à droite** ?

Si non, **recharger la page** (F5) et réessayer

### "Comment je glisse-dépose un widget ?"
**Réponse** : **Vous ne pouvez pas** ! 

Le glisser-déposer n'est **pas implémenté** dans cette version.

**Alternative** : Utiliser les **boutons ⬆️⬇️** en mode édition pour réorganiser

### "Mon widget ne s'affiche pas dans la visualisation"
**Causes possibles** :
1. **Pas de données** : Vérifier qu'il y a des consultants/missions en base
2. **Rôle d'accès** : Le dashboard est-il accessible à votre rôle ?
3. **Erreur widget** : Vérifier les logs du terminal pour erreurs

**Solution** : Actualiser avec **🔄** et vérifier les logs

---

## 💡 Astuces Pro

### Planifier avant d'ajouter
Dessinez sur papier où vous voulez chaque widget avant de les ajouter.
→ Évite de devoir réorganiser après

### Commencer simple
Créez un dashboard avec 3-4 widgets simples d'abord.
→ Ajoutez les widgets complexes une fois à l'aise

### Tester régulièrement
Allez dans **Visualisation** après chaque 2-3 widgets ajoutés.
→ Validez que tout s'affiche correctement

### Dupliquer pour expérimenter
Créez un dashboard, dupliquez-le, expérimentez sur la copie.
→ Garde une version de secours

---

## 🔗 Ressources

**Documentations complètes** :
- `GUIDE_RAPIDE_DASHBOARD.md` - Démarrage rapide (3 min)
- `NOTICE_DASHBOARD.md` - Guide complet (15 min)
- `RAPPORT_TECHNIQUE_DASHBOARD.md` - Aspects techniques

**Dans l'application** :
- **Onglet 🎨 Builder Avancé** → Cliquer sur **"ℹ️ Comment utiliser le Builder"**
- Instructions intégrées dans l'interface

**Support** :
- Logs dans le terminal où tourne `python run.py`
- Documentation technique dans `/app/services/`

---

## ✅ Checklist Création Dashboard

- [ ] Dashboard créé via **⚙️ Gestion**
- [ ] Passage sur **🎨 Builder Avancé**
- [ ] Dashboard sélectionné dans la liste
- [ ] Mode édition activé (✏️)
- [ ] 3-4 widgets ajoutés depuis le catalogue
- [ ] Configuration de chaque widget validée
- [ ] Visualisation testée (👁️)
- [ ] Données affichées correctement
- [ ] Aucune erreur dans les logs

**🎯 Objectif** : Dashboard fonctionnel en 10 minutes !

---

**Dernière mise à jour** : 3 octobre 2025
**Version** : Guide visuel v1.0
