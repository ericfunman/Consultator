Tutoriels
=========

Cette section contient des guides pratiques pour maîtriser les fonctionnalités avancées de Consultator.

.. _tutorials-import-data:

Import de données Excel
-----------------------

Apprenez à importer efficacement vos données de consultants depuis Excel.

Préparation des données
~~~~~~~~~~~~~~~~~~~~~~~

**Format requis**

Votre fichier Excel doit contenir les colonnes suivantes :

.. list-table:: Colonnes obligatoires
   :header-rows: 1

   * - Colonne
     - Type
     - Description
     - Exemple
   * - nom
     - Texte
     - Nom de famille en majuscules
     - DUPONT
   * - prenom
     - Texte
     - Prénom
     - Jean
   * - email
     - Texte
     - Adresse email professionnelle
     - jean.dupont@consultant.com

.. list-table:: Colonnes optionnelles
   :header-rows: 1

   * - Colonne
     - Type
     - Description
   * - telephone
     - Texte
     - Numéro de téléphone
   * - competence_1
     - Texte
     - Première compétence
   * - annees_exp_1
     - Nombre
     - Années d'expérience pour competence_1
   * - competence_2
     - Texte
     - Deuxième compétence
   * - annees_exp_2
     - Nombre
     - Années d'expérience pour competence_2

**Exemple de fichier Excel**

.. csv-table:: Exemple de données
   :header: nom, prenom, email, telephone, competence_1, annees_exp_1, competence_2, annees_exp_2

   DUPONT,Jean,jean.dupont@email.com,+33123456789,Python,5,SQL,3
   MARTIN,Marie,marie.martin@email.com,+33987654321,Data Science,4,Machine Learning,2
   BERNARD,Paul,paul.bernard@email.com,+33555666777,Java,8,Spring,6

Import étape par étape
~~~~~~~~~~~~~~~~~~~~~~~

1. **Accès à la fonctionnalité d'import**

   - Lancez Consultator
   - Allez dans "👥 Consultants"
   - Cliquez sur "📥 Importer des données"

2. **Sélection du fichier**

   - Cliquez sur "Choisir un fichier"
   - Sélectionnez votre fichier Excel (.xlsx ou .xls)
   - Vérifiez que le fichier est correctement chargé

3. **Configuration du mapping**

   .. image:: _static/import_mapping.png
      :alt: Interface de mapping des colonnes

   - Vérifiez automatiquement le mapping des colonnes
   - Ajustez manuellement si nécessaire
   - Consultez l'aperçu des données

4. **Validation des données**

   Le système vérifie automatiquement :

   - **Format des emails** : Validation des adresses email
   - **Cohérence des compétences** : Vérification des noms de compétences
   - **Doublons** : Détection des consultants déjà existants

5. **Import final**

   - Lancez l'import
   - Suivez la progression en temps réel
   - Consultez le rapport d'import

Gestion des erreurs d'import
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Erreurs courantes et solutions**

.. list-table:: Problèmes fréquents
   :header-rows: 1

   * - Erreur
     - Cause
     - Solution
   * - Email invalide
     - Format d'email incorrect
     - Vérifier et corriger l'adresse email
   * - Compétence inconnue
     - Compétence non référencée
     - Ajouter la compétence au référentiel ou corriger le nom
   * - Doublon détecté
     - Consultant déjà existant
     - Choisir de mettre à jour ou ignorer
   * - Colonne manquante
     - Colonne obligatoire absente
     - Ajouter la colonne ou modifier le mapping

**Rapport d'erreurs détaillé**

Après l'import, consultez le rapport qui détaille :

- Nombre de consultants importés avec succès
- Liste des erreurs par ligne
- Suggestions de correction automatique

.. _tutorials-custom-reports:

Création de rapports personnalisés
----------------------------------

Apprenez à créer des rapports sur mesure pour vos besoins d'analyse.

Types de rapports disponibles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Rapports standards**

- **Tableau de bord général** : Vue d'ensemble des métriques
- **Rapport par compétence** : Analyse détaillée des compétences
- **Rapport financier** : Revenus et performance économique
- **Rapport RH** : Évolution des effectifs et turnover

**Rapports personnalisés**

Création d'un rapport sur mesure :

1. **Définition des critères**

   - Période d'analyse (date de début/fin)
   - Filtres sur les consultants (compétences, statut, etc.)
   - Métriques à inclure
   - Format de sortie (PDF, Excel, HTML)

2. **Configuration des métriques**

   .. code-block:: python

      # Exemple de configuration de rapport
      report_config = {
          "title": "Rapport Data Science Q4 2024",
          "period": {
              "start": "2024-10-01",
              "end": "2024-12-31"
          },
          "filters": {
              "skills": ["Python", "Machine Learning", "Data Science"],
              "status": "active"
          },
          "metrics": [
              "consultant_count",
              "average_revenue",
              "skill_distribution",
              "project_completion_rate"
          ],
          "format": "pdf"
      }

3. **Génération automatique**

   - Planification des rapports récurrents
   - Export automatique vers le cloud
   - Distribution par email

Analyse des compétences
~~~~~~~~~~~~~~~~~~~~~~~

**Matrice de compétences**

Visualisez les compétences de votre équipe :

.. code-block:: python

   # Génération d'une matrice compétence/niveau
   skill_matrix = consultant_service.generate_skill_matrix(
       consultants=active_consultants,
       skills=["Python", "SQL", "Machine Learning", "AWS"],
       group_by="seniority"
   )

**Gap analysis**

Identifiez les besoins en recrutement :

.. code-block:: python

   # Analyse des écarts de compétences
   gaps = analytics_service.identify_skill_gaps(
       required_skills=project_requirements,
       available_skills=current_team_skills,
       timeframe_months=6
   )

**Prévisions de compétences**

.. code-block:: python

   # Prévision des besoins futurs
   forecast = analytics_service.forecast_skill_demand(
       historical_data=mission_history,
       market_trends=market_data,
       prediction_months=12
   )

.. _tutorials-chatbot-setup:

Configuration du chatbot IA
---------------------------

Configurez et optimisez le chatbot IA pour vos besoins métier.

Configuration de base
~~~~~~~~~~~~~~~~~~~~~~

1. **Accès aux paramètres**

   - Allez dans "⚙️ Configuration"
   - Section "🤖 Chatbot IA"

2. **Configuration des sources de connaissances**

   - **Base de données consultants** : Activé par défaut
   - **Documents uploadés** : CV, présentations, etc.
   - **Base de connaissances métier** : Documents internes

3. **Paramètres de réponse**

   - **Style de réponse** : Professionnel, Conversationnel, Technique
   - **Niveau de détail** : Synthétique, Détaillé, Exhaustif
   - **Langue** : Français, Anglais

Entraînement du modèle
~~~~~~~~~~~~~~~~~~~~~~

**Ajout de connaissances spécifiques**

.. code-block:: python

   # Entraînement sur des documents métier
   chatbot_service.train_on_documents([
       "docs/referentiel_competences.pdf",
       "docs/methodologie_projets.docx",
       "data/base_connaissances.json"
   ])

**Personnalisation des réponses**

.. code-block:: python

   # Configuration des réponses personnalisées
   custom_responses = {
       "tarifs": "Nos tarifs varient de 500€ à 1200€ par jour selon l'expertise.",
       "delais": "Les délais de mobilisation sont généralement de 2-4 semaines.",
       "methodologie": "Nous suivons une approche agile avec Scrum/Kanban."
   }

   chatbot_service.add_custom_responses(custom_responses)

Utilisation avancée
~~~~~~~~~~~~~~~~~~~

**Requêtes complexes**

Le chatbot peut traiter des demandes sophistiquées :

- *"Quels sont mes consultants Python seniors disponibles en région parisienne ?"*
- *"Peux-tu me proposer une équipe de 3 personnes pour un projet Data Science de 6 mois ?"*
- *"Quel est le coût moyen d'un consultant AWS certifié ?"*

**Intégration avec les analyses**

.. code-block:: python

   # Génération de rapports via le chatbot
   report_request = "Génère-moi un rapport des compétences Data Science pour le trimestre dernier"
   report = chatbot_service.generate_report_from_query(report_request)

   # Analyse prédictive
   prediction = chatbot_service.predict_from_query(
       "Quelles compétences seront demandées dans 6 mois ?"
   )

Maintenance et optimisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Mise à jour des connaissances**

.. code-block:: bash

   # Mise à jour périodique des connaissances
   python scripts/update_chatbot_knowledge.py

**Monitoring des performances**

- Taux de réponses satisfaisantes
- Temps de réponse moyen
- Types de questions fréquentes
- Améliorations suggérées

.. _tutorials-api-integration:

Intégration API externe
-----------------------

Connectez Consultator à vos outils existants via l'API.

Authentification API
~~~~~~~~~~~~~~~~~~~~

**Obtention d'un token**

.. code-block:: bash

   curl -X POST https://api.consultator.com/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "votre-email", "password": "votre-mot-de-passe"}'

**Utilisation du token**

.. code-block:: bash

   curl -H "Authorization: Bearer VOTRE_TOKEN" \
        https://api.consultator.com/v1/consultants

Synchronisation avec un CRM
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Export vers Salesforce**

.. code-block:: python

   import requests
   from simple_salesforce import Salesforce

   def sync_consultants_to_salesforce():
       # Récupération des consultants
       response = requests.get(
           "https://api.consultator.com/v1/consultants",
           headers={"Authorization": f"Bearer {token}"}
       )
       consultants = response.json()["data"]

       # Connexion Salesforce
       sf = Salesforce(username=username, password=password, security_token=token)

       # Synchronisation
       for consultant in consultants:
           sf.Contact.create({
               "LastName": consultant["nom"],
               "FirstName": consultant["prenom"],
               "Email": consultant["email"],
               "Title": "Consultant"
           })

**Import depuis HubSpot**

.. code-block:: python

   from hubspot import HubSpot

   def import_contacts_from_hubspot():
       api_client = HubSpot(access_token=access_token)
       contacts = api_client.crm.contacts.get_all()

       for contact in contacts:
           consultant_data = {
               "nom": contact.properties["lastname"],
               "prenom": contact.properties["firstname"],
               "email": contact.properties["email"]
           }

           requests.post(
               "https://api.consultator.com/v1/consultants",
               json=consultant_data,
               headers={"Authorization": f"Bearer {token}"}
           )

Intégration avec Jira
~~~~~~~~~~~~~~~~~~~~~

**Synchronisation des projets**

.. code-block:: python

   from jira import JIRA

   def sync_projects_from_jira():
       jira = JIRA(server=jira_url, basic_auth=(username, password))

       # Récupération des projets actifs
       projects = jira.projects()

       for project in projects:
           # Création d'une mission dans Consultator
           mission_data = {
               "nom_projet": project.name,
               "client": project.lead.displayName,
               "statut": "en_cours"
           }

           requests.post(
               "https://api.consultator.com/v1/missions",
               json=mission_data,
               headers={"Authorization": f"Bearer {token}"}
           )

Webhook pour les événements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Configuration d'un webhook**

.. code-block:: python

   webhook_config = {
       "url": "https://mon-app.com/webhooks/consultator",
       "events": ["consultant.created", "mission.completed"],
       "secret": "mon-secret-webhook"
   }

   requests.post(
       "https://api.consultator.com/v1/webhooks",
       json=webhook_config,
       headers={"Authorization": f"Bearer {token}"}
   )

**Traitement des événements**

.. code-block:: python

   from flask import Flask, request
   import hmac
   import hashlib

   app = Flask(__name__)

   @app.route('/webhooks/consultator', methods=['POST'])
   def handle_webhook():
       payload = request.get_data()
       signature = request.headers.get('X-Consultator-Signature')

       # Vérification de la signature
       expected_signature = hmac.new(
           webhook_secret.encode(),
           payload,
           hashlib.sha256
       ).hexdigest()

       if not hmac.compare_digest(signature, expected_signature):
           return 'Invalid signature', 400

       # Traitement de l'événement
       event_data = request.get_json()
       event_type = event_data['event']

       if event_type == 'consultant.created':
           # Mise à jour du CRM externe
           update_external_crm(event_data['data']['consultant'])

       return 'OK', 200

.. _tutorials-performance:

Optimisation des performances
-----------------------------

Techniques pour maintenir des performances optimales avec une base de données importante.

Indexation de la base de données
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Index stratégiques**

.. code-block:: sql

   -- Index sur les recherches fréquentes
   CREATE INDEX idx_consultant_email ON consultants(email);
   CREATE INDEX idx_consultant_nom_prenom ON consultants(nom, prenom);

   -- Index sur les compétences
   CREATE INDEX idx_competence_nom ON competences(nom);
   CREATE INDEX idx_consultant_competence_consultant_id ON consultant_competence(consultant_id);
   CREATE INDEX idx_consultant_competence_competence_id ON consultant_competence(competence_id);

   -- Index composites pour les analyses
   CREATE INDEX idx_mission_consultant_dates ON missions(consultant_id, date_debut, date_fin);

**Maintenance des index**

.. code-block:: bash

   # Analyse et reconstruction des index
   python scripts/optimize_database_indexes.py

Cache intelligent
~~~~~~~~~~~~~~~~~

**Cache des requêtes fréquentes**

.. code-block:: python

   from streamlit import cache_data
   import time

   @cache_data(ttl=3600)  # Cache pendant 1 heure
   def get_consultant_stats():
       """Cache les statistiques des consultants."""
       return consultant_service.get_statistics()

   @cache_data(ttl=1800)  # Cache pendant 30 minutes
   def get_skill_distribution():
       """Cache la distribution des compétences."""
       return analytics_service.get_skill_distribution()

**Cache des données de référence**

.. code-block:: python

   @st.cache_data
   def load_referentiel_competences():
       """Cache le référentiel des compétences."""
       return competence_service.get_all_competences()

Optimisation des requêtes
~~~~~~~~~~~~~~~~~~~~~~~~~

**Requêtes paginées**

.. code-block:: python

   def get_consultants_optimized(page=1, per_page=50, filters=None):
       """Récupération optimisée avec pagination."""
       query = session.query(Consultant)

       # Application des filtres
       if filters:
           if filters.get('skill'):
               query = query.join(Consultant.competences).filter(
                   Competence.nom.ilike(f"%{filters['skill']}%")
               )
           if filters.get('status'):
               query = query.filter(Consultant.statut == filters['status'])

       # Pagination
       offset = (page - 1) * per_page
       return query.offset(offset).limit(per_page).all()

**Chargement sélectif**

.. code-block:: python

   def get_consultant_summary(consultant_id):
       """Chargement sélectif des données essentielles."""
       return session.query(
           Consultant.id,
           Consultant.nom,
           Consultant.prenom,
           Consultant.email,
           func.count(Competence.id).label('nb_competences')
       ).join(Consultant.competences).filter(
           Consultant.id == consultant_id
       ).group_by(Consultant.id).first()

Monitoring des performances
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Métriques clés à surveiller**

- **Temps de réponse des pages** : < 2 secondes
- **Temps de chargement des données** : < 5 secondes pour 1000 consultants
- **Utilisation mémoire** : < 80% de la RAM disponible
- **Temps de requête base de données** : < 500ms en moyenne

**Outils de monitoring**

.. code-block:: python

   import time
   import logging

   def monitor_query_performance(func):
       """Décorateur pour mesurer les performances des requêtes."""
       def wrapper(*args, **kwargs):
           start_time = time.time()
           result = func(*args, **kwargs)
           execution_time = time.time() - start_time

           if execution_time > 1.0:  # Log si > 1 seconde
               logging.warning(f"Requête lente: {func.__name__} - {execution_time:.2f}s")

           return result
       return wrapper

   @monitor_query_performance
   def get_consultants_with_skills():
       return consultant_service.get_all_with_competences()

Maintenance préventive
~~~~~~~~~~~~~~~~~~~~~~

**Tâches automatisées**

.. code-block:: bash

   # Optimisation quotidienne de la base
   0 2 * * * python scripts/daily_database_maintenance.py

   # Reconstruction des index hebdomadaire
   0 3 * * 1 python scripts/weekly_index_rebuild.py

   # Archive des données anciennes mensuelle
   0 4 1 * * python scripts/monthly_data_archive.py

**Seuils d'alerte**

- Nombre de consultants > 5000 : optimisation obligatoire
- Taille base de données > 10GB : archivage recommandé
- Temps de sauvegarde > 30min : optimisation nécessaire
