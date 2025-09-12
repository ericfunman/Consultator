Guide de démarrage rapide
=========================

Bienvenue dans Consultator ! Ce guide vous permettra de prendre en main l'application en quelques minutes.

Premiers pas
------------

1. **Démarrer l'application**

   Après l'installation, lancez Consultator :

   .. code-block:: bash

      streamlit run run.py

   L'application s'ouvrira dans votre navigateur à l'adresse ``http://localhost:8501``.

2. **Interface principale**

   L'application se compose de plusieurs sections accessibles via le menu latéral :

   - **🏠 Accueil** : Vue d'ensemble et métriques
   - **👥 Consultants** : Gestion des profils
   - **📊 Analyses** : Tableaux de bord et rapports
   - **⚙️ Configuration** : Paramètres système

Créer votre premier consultant
------------------------------

1. **Accéder à la gestion des consultants**

   Cliquez sur "👥 Consultants" dans le menu latéral.

2. **Ajouter un consultant**

   Cliquez sur le bouton "➕ Ajouter un consultant".

3. **Remplir le formulaire**

   .. code-block:: none

      Informations personnelles :
      - Nom : DUPONT
      - Prénom : Jean
      - Email : jean.dupont@consultant.com
      - Téléphone : +33 1 23 45 67 89

      Compétences techniques :
      - Python : 5 ans d'expérience
      - SQL : 3 ans d'expérience
      - Machine Learning : 2 ans d'expérience

4. **Sauvegarder**

   Cliquez sur "💾 Sauvegarder" pour enregistrer le profil.

Importer des données
--------------------

**Import depuis Excel**

1. Préparer votre fichier Excel avec les colonnes suivantes :

   .. list-table:: Format d'import Excel
      :header-rows: 1

      * - nom
        - prenom
        - email
        - telephone
        - competence_1
        - annees_exp_1
      * - DUPONT
        - Jean
        - jean.dupont@email.com
        - +33123456789
        - Python
        - 5

2. Aller dans "👥 Consultants" → "📥 Importer"
3. Sélectionner votre fichier Excel
4. Cliquer sur "🚀 Importer"

Explorer les analyses
---------------------

**Tableaux de bord**

1. Accéder à "📊 Analyses"
2. Consulter les métriques principales :

   - Nombre total de consultants
   - Répartition par compétence
   - Revenus moyens par consultant
   - Évolution des missions

**Filtres et recherche**

- Utiliser la barre de recherche pour trouver des consultants
- Filtrer par compétence, niveau d'expérience, ou statut
- Exporter les résultats au format Excel

Configuration initiale
----------------------

**Paramètres système**

1. Aller dans "⚙️ Configuration"
2. Configurer :

   - **Référentiel de compétences** : Ajouter/modifier les compétences disponibles
   - **Paramètres d'import** : Configurer les mappings Excel
   - **Préférences utilisateur** : Thème, langue, notifications

**Données de test**

Pour découvrir les fonctionnalités, vous pouvez charger des données de test :

.. code-block:: bash

   python scripts/generate_test_data.py

Fonctionnalités avancées
------------------------

**Gestion des missions**

- Associer des missions aux consultants
- Suivre les revenus et la durée des projets
- Analyser la rentabilité par compétence

**Rapports personnalisés**

- Créer des rapports sur mesure
- Exporter en PDF ou Excel
- Planifier des rapports automatiques

**Intégration chatbot IA**

- Poser des questions en langage naturel
- Obtenir des analyses instantanées
- Générer des recommandations

Prochaines étapes
-----------------

Maintenant que vous maîtrisez les bases :

1. **Explorez la documentation complète** : `📚 Documentation <https://consultator.readthedocs.io/>`_
2. **Personnalisez votre installation** : Configurez les compétences et paramètres
3. **Importez vos données réelles** : Migrez vos données existantes
4. **Découvrez les analyses avancées** : Créez vos premiers rapports

Support et communauté
---------------------

- **Documentation** : `https://consultator.readthedocs.io/ <https://consultator.readthedocs.io/>`_
- **Issues GitHub** : `Signaler un bug <https://github.com/votre-organisation/consultator/issues>`_
- **Discussions** : `Forum communautaire <https://github.com/votre-organisation/consultator/discussions>`_

N'hésitez pas à contacter l'équipe pour toute question !
