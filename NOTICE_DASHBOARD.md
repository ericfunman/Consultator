# 📊 Notice d'Utilisation - Système de Dashboards Consultator

## 🎯 Objectif

Le système de dashboards de Consultator permet de créer, personnaliser et gérer des tableaux de bord interactifs pour visualiser les données des consultants, missions et business managers.

---

## 📍 Accès au Module Dashboard

1. Naviguer vers **Business Managers** dans le menu principal
2. Cliquer sur l'onglet **📊 Dashboard**
3. Vous verrez 4 sous-onglets :
   - **📊 Visualisation** : Affichage des dashboards
   - **🎨 Builder Avancé** : Création/édition avec drag & drop
   - **📈 Analytics+** : Analyses avancées
   - **⚙️ Gestion** : Administration des dashboards

---

## 🚀 Créer votre Premier Dashboard

### Méthode 1 : Création Simple (Recommandée pour débuter)

1. Aller dans l'onglet **⚙️ Gestion**
2. Cliquer sur **➕ Créer mon premier dashboard**
3. Remplir le formulaire :
   - **Nom** : Ex. "Dashboard Practice Data"
   - **Description** : Ex. "Vue d'ensemble de ma practice"
   - **Rôle d'accès** : Choisir qui peut voir ce dashboard
   - **Template** : Cocher si vous voulez le réutiliser
4. Cliquer sur **✅ Créer le Dashboard**
5. Le dashboard est créé avec une structure vide

### Méthode 2 : Builder Avancé (Pour utilisateurs expérimentés)

1. Aller dans l'onglet **🎨 Builder Avancé**
2. Cliquer sur **➕ Nouveau Dashboard**
3. Configuration initiale :
   - **Nom** : Nom du dashboard
   - **Description** : Description détaillée
   - **Colonnes** : Nombre de colonnes (1-4, défaut: 2)
   - **Hauteur de ligne** : Pixels par ligne (défaut: 150px)
4. Cliquer sur **🚀 Créer et Commencer à Construire**

---

## 🎨 Ajouter des Widgets (Builder Avancé)

### Étape 1 : Accéder au Mode Édition

1. Dans l'onglet **🎨 Builder Avancé**
2. Sélectionner un dashboard existant dans la liste déroulante
3. Cliquer sur **✏️ Éditer**

### Étape 2 : Catalogue de Widgets Disponibles

Le système propose **20 widgets** organisés en 5 catégories :

#### 📊 **Métriques Consultants** (4 widgets)
- **Total Consultants** : Nombre total avec évolution
- **Top Compétences** : Classement des compétences les plus fréquentes
- **Consultants par Entité** : Répartition par entité organisationnelle
- **Taux de Disponibilité** : % de consultants disponibles

#### 💼 **Missions** (4 widgets)
- **Missions Actives** : Nombre de missions en cours
- **Timeline Missions** : Chronologie des missions
- **Top Clients** : Clients générant le plus de revenus
- **TJM Moyen** : Taux Journalier Moyen par compétence

#### 💰 **Revenus** (4 widgets)
- **CA Total** : Chiffre d'affaires estimé
- **Revenus Mensuels** : Évolution mensuelle du CA
- **Revenus par Consultant** : Top 10 consultants générateurs de CA
- **Revenus par BM** : Performance par Business Manager

#### 👥 **Business Managers** (4 widgets)
- **Total BM** : Nombre de Business Managers actifs
- **Performance BM** : Classement par CA généré
- **Consultants par BM** : Répartition des consultants
- **Taux de Remplissage** : % de consultants en mission

#### 📈 **Analytics Avancés** (4 widgets)
- **Heatmap Compétences** : Carte thermique des compétences
- **Prédiction CA** : Prévisions de chiffre d'affaires (IA)
- **Analyse Temporelle** : Tendances sur plusieurs périodes
- **KPIs Personnalisés** : Indicateurs configurables

### Étape 3 : Ajouter un Widget

1. **Parcourir le Catalogue** :
   - Naviguer entre les onglets de catégories
   - Lire la description et aperçu de chaque widget
   
2. **Sélectionner un Widget** :
   - Cliquer sur la carte du widget souhaité
   - Vérifier que la carte s'affiche avec une **bordure bleue** (sélection active)

3. **Configurer le Widget** :
   - **Taille (Span)** : Nombre de colonnes occupées (1 à colonnes_max)
   - **Hauteur (Height)** : Nombre de lignes occupées (1-8)
   - **Paramètres** : Selon le type de widget
     - Ex : Période pour "Revenus Mensuels" (3, 6, 12 mois)
     - Ex : Nombre de résultats pour "Top Clients" (5, 10, 15)

4. **Ajouter à la Grille** :
   - Cliquer sur **➕ Ajouter le widget**
   - Le widget apparaît immédiatement dans la grille

### Étape 4 : Organiser les Widgets (Drag & Drop)

**⚠️ IMPORTANT** : Le drag & drop nécessite :
- Un navigateur moderne (Chrome, Firefox, Edge récent)
- JavaScript activé
- Streamlit v1.28+ (vérifier avec `streamlit --version`)

**Comment réorganiser** :
1. **Glisser** : Cliquer et maintenir sur un widget
2. **Déplacer** : Faire glisser vers la nouvelle position
3. **Déposer** : Relâcher pour placer le widget
4. La grille se réorganise automatiquement

**Limites connues** :
- ⚠️ Le drag & drop Streamlit est **expérimental** et peut ne pas fonctionner dans tous les cas
- Si le drag & drop ne fonctionne pas :
  - Utiliser les **boutons de réorganisation** : ⬆️ Monter / ⬇️ Descendre
  - Supprimer et recréer le widget dans l'ordre souhaité
  - Éditer la configuration JSON manuellement (utilisateurs avancés)

---

## 🔧 Gérer les Widgets Existants

### Modifier un Widget

1. Cliquer sur **✏️** à côté du widget dans la liste
2. Ajuster la taille, hauteur ou paramètres
3. Cliquer sur **💾 Sauvegarder**

### Supprimer un Widget

1. Cliquer sur **🗑️** à côté du widget
2. Confirmer la suppression
3. Le widget disparaît de la grille

### Réorganiser sans Drag & Drop

Si le glisser-déposer ne fonctionne pas :
1. Utiliser les boutons **⬆️ Monter** et **⬇️ Descendre**
2. Chaque clic déplace le widget d'une position
3. Sauvegarder pour appliquer

---

## 📊 Visualiser un Dashboard

1. Aller dans l'onglet **📊 Visualisation**
2. Sélectionner un dashboard dans la liste déroulante
3. Le dashboard s'affiche avec tous les widgets configurés
4. **Fonctionnalités** :
   - **Actualiser** : Bouton 🔄 pour recharger les données
   - **Plein écran** : Mode présentation (si disponible)
   - **Export** : Exporter en PDF (fonctionnalité future)

---

## ⚙️ Administration des Dashboards

### Dupliquer un Dashboard

1. Aller dans **⚙️ Gestion** → **📋 Liste des Dashboards**
2. Cliquer sur **📋 Dupliquer** pour le dashboard souhaité
3. Modifier le nom du duplicata
4. Éditer le nouveau dashboard indépendamment

### Éditer les Métadonnées

1. Sélectionner un dashboard dans la liste
2. Cliquer sur **✏️ Éditer**
3. Modifier :
   - Nom
   - Description
   - Rôle d'accès
   - Statut template
4. Sauvegarder les modifications

### Supprimer un Dashboard

1. Cliquer sur **🗑️ Supprimer**
2. **⚠️ ATTENTION** : Suppression définitive sans récupération
3. Confirmer la suppression

### Statistiques

Visualiser dans l'onglet **⚙️ Gestion** → **📊 Statistiques** :
- Nombre total de dashboards
- Répartition par rôle d'accès
- Templates disponibles
- Dashboards les plus utilisés

---

## 💡 Cas d'Usage Pratiques

### Dashboard "Vue Practice"
**Objectif** : Aperçu global de l'activité

**Widgets recommandés** :
1. **Total Consultants** (span: 1, height: 2)
2. **Missions Actives** (span: 1, height: 2)
3. **CA Total** (span: 1, height: 2)
4. **Taux de Disponibilité** (span: 1, height: 2)
5. **Revenus Mensuels** (span: 2, height: 3) - graphique 6 mois
6. **Top Clients** (span: 2, height: 3) - top 10

### Dashboard "Performance BM"
**Objectif** : Suivi des Business Managers

**Widgets recommandés** :
1. **Total BM** (span: 1, height: 2)
2. **Performance BM** (span: 2, height: 4) - classement complet
3. **Consultants par BM** (span: 1, height: 3)
4. **Revenus par BM** (span: 2, height: 4) - avec graphique

### Dashboard "Compétences"
**Objectif** : Cartographie des compétences

**Widgets recommandés** :
1. **Top Compétences** (span: 1, height: 3) - top 15
2. **Heatmap Compétences** (span: 2, height: 5)
3. **TJM Moyen** (span: 1, height: 4) - par compétence

---

## 🐛 Dépannage

### Le bouton "Créer mon premier dashboard" ne fait rien

**Solution** :
- Vérifier que vous êtes dans l'onglet **⚙️ Gestion**
- Recharger la page Streamlit (F5)
- Vérifier les logs du terminal pour erreurs Python
- Si problème persiste, utiliser le **🎨 Builder Avancé**

### Le drag & drop ne fonctionne pas

**Causes possibles** :
1. **Version Streamlit** : Nécessite Streamlit ≥ 1.28
   ```bash
   streamlit --version
   pip install --upgrade streamlit
   ```
2. **Navigateur** : Utiliser Chrome/Firefox/Edge récent
3. **JavaScript désactivé** : Activer JavaScript dans les paramètres
4. **Solution alternative** : Utiliser les boutons ⬆️⬇️ de réorganisation

### Les widgets ne s'affichent pas

**Vérifications** :
1. **Données en base** : Assurez-vous d'avoir des consultants/missions
2. **Permissions** : Vérifier le rôle d'accès du dashboard
3. **Erreurs console** : Ouvrir la console navigateur (F12)
4. **Logs Streamlit** : Vérifier les erreurs dans le terminal

### Erreur "type 'property' is not supported"

**Cause** : Bug corrigé dans la dernière version
**Solution** :
1. Redémarrer l'application :
   ```bash
   # Tuer les processus Python
   Stop-Process -Name python -Force
   
   # Relancer
   python run.py
   ```
2. Si erreur persiste, vérifier que la correction est appliquée dans `dashboard_service.py`

### Le dashboard est vide après création

**Normal** : Un dashboard créé via le formulaire simple est vide par défaut

**Actions** :
1. Aller dans **🎨 Builder Avancé**
2. Sélectionner le dashboard créé
3. Cliquer sur **✏️ Éditer**
4. Ajouter des widgets depuis le catalogue

---

## 🔒 Gestion des Rôles

### Rôles Disponibles

- **👤 Practice Manager** : Accès complet à tous les dashboards
- **👥 Business Manager** : Dashboards de leur practice uniquement
- **📊 Consultant** : Dashboards publics et personnels
- **🌐 Public** : Dashboards visibles par tous

### Configurer les Permissions

1. Lors de la création/édition d'un dashboard
2. Sélectionner le **Rôle d'accès**
3. Sauvegarder
4. Les utilisateurs sans permission ne verront pas le dashboard

---

## 📚 Ressources Supplémentaires

### Fichiers de Configuration

- **Configuration grille** : JSON stocké en base de données
- **Widgets disponibles** : `app/services/widget_factory.py`
- **Service dashboard** : `app/services/dashboard_service.py`
- **Interface** : `app/pages_modules/dashboard_page.py`

### Documentation Technique

- **Guide système** : `DASHBOARD_SYSTEM_GUIDE.md`
- **Architecture** : `ARCHITECTURE.md` (si disponible)
- **Copilot instructions** : `.github/copilot-instructions.md`

### Support

- **Issues GitHub** : Reporter les bugs sur le dépôt
- **Logs** : Consulter le terminal pour messages d'erreur
- **Debug** : Activer le mode debug Streamlit si nécessaire

---

## ✅ Checklist de Mise en Route

- [ ] L'application Streamlit est lancée (`python run.py`)
- [ ] Naviguer vers **Business Managers** → **Dashboard**
- [ ] Créer un premier dashboard via **⚙️ Gestion**
- [ ] Ajouter 2-3 widgets via **🎨 Builder Avancé**
- [ ] Visualiser le résultat dans **📊 Visualisation**
- [ ] Tester la réorganisation des widgets
- [ ] Sauvegarder et actualiser

---

## 🎓 Conseils d'Expert

1. **Commencer simple** : Ne pas surcharger un dashboard (max 8-10 widgets)
2. **Hiérarchie visuelle** : Métriques importantes en haut, graphiques en dessous
3. **Cohérence** : Utiliser des widgets de même catégorie ensemble
4. **Performance** : Widgets avec beaucoup de données = plus lent
5. **Templates** : Créer un dashboard template pour réutiliser la structure
6. **Actualisation** : Penser à actualiser pour voir les nouvelles données
7. **Mobile** : L'interface est optimisée pour desktop, limites sur mobile

---

**Version Notice** : 1.0
**Dernière mise à jour** : 3 octobre 2025
**Compatibilité** : Consultator v1.2+

---

## 🆘 En cas de problème persistant

1. **Redémarrer l'application** :
   ```powershell
   Stop-Process -Name python -Force -ErrorAction SilentlyContinue
   python run.py
   ```

2. **Vérifier les versions** :
   ```bash
   python --version  # Python 3.8+
   streamlit --version  # Streamlit 1.28+
   ```

3. **Réinitialiser un dashboard corrompu** :
   - Supprimer le dashboard problématique
   - Recréer un nouveau dashboard
   - Réimporter les widgets un par un

4. **Contacter le support technique** avec :
   - Description du problème
   - Logs du terminal (copier/coller les erreurs)
   - Actions effectuées avant l'erreur
   - Version de Consultator et Streamlit
