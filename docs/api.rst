API Reference
============

Cette section documente l'architecture API de Consultator, incluant les services métier et l'API REST (future).

Architecture des services
-------------------------

Consultator utilise une architecture en couches avec des services métier dédiés.

.. _api-services:

Services métier
~~~~~~~~~~~~~~~

.. automodule:: app.services.consultant_service
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.services.business_manager_service
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.services.practice_service
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.services.chatbot_service
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.services.document_service
   :members:
   :undoc-members:
   :show-inheritance:

Modèles de données
------------------

.. _api-models:

.. automodule:: app.database.models
   :members:
   :undoc-members:
   :show-inheritance:

Utilitaires
-----------

.. _api-utils:

.. automodule:: app.utils.helpers
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.utils.validators
   :members:
   :undoc-members:
   :show-inheritance:

API REST (Future)
-----------------

Une API REST complète sera disponible dans les prochaines versions.

Endpoints prévus
~~~~~~~~~~~~~~~~~

**Consultants**

.. http:get:: /api/v1/consultants

   Liste tous les consultants.

   **Exemple de requête**

   .. code-block:: http

      GET /api/v1/consultants?page=1&per_page=20 HTTP/1.1
      Host: api.consultator.com
      Authorization: Bearer <token>

   **Paramètres de requête**

   - **page** (int) -- Numéro de page (défaut: 1)
   - **per_page** (int) -- Nombre d'éléments par page (défaut: 20)
   - **search** (str) -- Terme de recherche
   - **skill** (str) -- Filtre par compétence

   **Exemple de réponse**

   .. code-block:: json

      {
        "data": [
          {
            "id": 1,
            "nom": "DUPONT",
            "prenom": "Jean",
            "email": "jean.dupont@consultant.com",
            "competences": [
              {
                "nom": "Python",
                "annees_experience": 5,
                "niveau": "Expert"
              }
            ]
          }
        ],
        "pagination": {
          "page": 1,
          "per_page": 20,
          "total": 150,
          "pages": 8
        }
      }

.. http:post:: /api/v1/consultants

   Crée un nouveau consultant.

   **Exemple de requête**

   .. code-block:: http

      POST /api/v1/consultants HTTP/1.1
      Host: api.consultator.com
      Authorization: Bearer <token>
      Content-Type: application/json

   .. code-block:: json

      {
        "nom": "MARTIN",
        "prenom": "Marie",
        "email": "marie.martin@consultant.com",
        "competences": [
          {
            "nom": "Data Science",
            "annees_experience": 3
          }
        ]
      }

.. http:get:: /api/v1/consultants/{id}

   Récupère les détails d'un consultant.

.. http:put:: /api/v1/consultants/{id}

   Met à jour un consultant.

.. http:delete:: /api/v1/consultants/{id}

   Supprime un consultant.

**Analyses**

.. http:get:: /api/v1/analytics/dashboard

   Récupère les métriques du tableau de bord.

   **Exemple de réponse**

   .. code-block:: json

      {
        "total_consultants": 150,
        "consultants_actifs": 120,
        "ca_total": 2500000,
        "competences_top": [
          {"nom": "Python", "count": 45},
          {"nom": "SQL", "count": 38},
          {"nom": "Machine Learning", "count": 32}
        ]
      }

.. http:get:: /api/v1/analytics/reports/{type}

   Génère un rapport spécifique.

   **Paramètres d'URL**

   - **type** (str) -- Type de rapport (revenue, skills, performance)

**Authentification**

.. http:post:: /api/v1/auth/login

   Authentification utilisateur.

   **Exemple de requête**

   .. code-block:: json

      {
        "username": "admin",
        "password": "password"
      }

   **Exemple de réponse**

   .. code-block:: json

      {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "token_type": "bearer",
        "expires_in": 3600
      }

.. http:post:: /api/v1/auth/refresh

   Rafraîchit le token d'accès.

Format des données
~~~~~~~~~~~~~~~~~~

**Consultant**

.. code-block:: json

   {
     "id": "integer",
     "nom": "string",
     "prenom": "string",
     "email": "string",
     "telephone": "string",
     "date_naissance": "date",
     "adresse": "string",
     "competences": [
       {
         "nom": "string",
         "annees_experience": "integer",
         "niveau": "string",
         "certifications": ["string"]
       }
     ],
     "missions": [
       {
         "id": "integer",
         "client": "string",
         "poste": "string",
         "date_debut": "date",
         "date_fin": "date",
         "tarif_journalier": "number",
         "statut": "string"
       }
     ],
     "created_at": "datetime",
     "updated_at": "datetime"
   }

**Compétence**

.. code-block:: json

   {
     "id": "integer",
     "nom": "string",
     "categorie": "string",
     "description": "string",
     "niveau_requis": "string"
   }

Codes d'erreur
~~~~~~~~~~~~~~

.. list-table:: Codes d'erreur HTTP
   :header-rows: 1

   * - Code
     - Description
     - Exemple d'usage
   * - 200
     - Succès
     - Requête traitée avec succès
   * - 201
     - Créé
     - Ressource créée avec succès
   * - 400
     - Requête invalide
     - Données manquantes ou format incorrect
   * - 401
     - Non autorisé
     - Token manquant ou invalide
   * - 403
     - Interdit
     - Permissions insuffisantes
   * - 404
     - Non trouvé
     - Ressource inexistante
   * - 409
     - Conflit
     - Ressource déjà existante
   * - 422
     - Entité non traitable
     - Erreurs de validation
   * - 500
     - Erreur serveur
     - Erreur interne du serveur

**Format des erreurs**

.. code-block:: json

   {
     "error": {
       "code": "VALIDATION_ERROR",
       "message": "Les données fournies sont invalides",
       "details": [
         {
           "field": "email",
           "message": "Format d'email invalide"
         }
       ]
     }
   }

Limitation et quotas
~~~~~~~~~~~~~~~~~~~~

- **Requêtes par minute** : 60 par utilisateur authentifié
- **Taille maximale du payload** : 10 MB
- **Timeout des requêtes** : 30 secondes
- **Rate limiting** : Implémenté avec en-têtes X-RateLimit-*

Webhooks
--------

Configuration des webhooks pour les événements temps réel.

Événements supportés
~~~~~~~~~~~~~~~~~~~~

- ``consultant.created`` : Nouveau consultant ajouté
- ``consultant.updated`` : Consultant modifié
- ``consultant.deleted`` : Consultant supprimé
- ``mission.started`` : Nouvelle mission démarrée
- ``mission.completed`` : Mission terminée

Configuration webhook
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   POST /api/v1/webhooks HTTP/1.1
   Content-Type: application/json

   {
     "url": "https://mon-app.com/webhooks/consultator",
     "events": ["consultant.created", "consultant.updated"],
     "secret": "mon-secret-webhook"
   }

Format des payloads webhook
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "event": "consultant.created",
     "timestamp": "2024-01-15T10:30:00Z",
     "data": {
       "consultant": {
         "id": 123,
         "nom": "DUPONT",
         "prenom": "Jean"
       }
     },
     "signature": "sha256=abc123..."
   }

SDKs et bibliothèques
---------------------

**Python SDK**

.. code-block:: python

   from consultator_sdk import Client

   client = Client(api_key="your-api-key")

   # Lister les consultants
   consultants = client.consultants.list(search="Python")

   # Créer un consultant
   consultant = client.consultants.create({
       "nom": "MARTIN",
       "prenom": "Sophie",
       "competences": [{"nom": "Data Science", "annees_experience": 4}]
   })

**JavaScript SDK**

.. code-block:: javascript

   import { Consultator } from 'consultator-sdk';

   const client = new Consultator({ apiKey: 'your-api-key' });

   // Récupérer un consultant
   const consultant = await client.consultants.get(123);

   // Mettre à jour un consultant
   await client.consultants.update(123, {
       email: 'nouveau.email@consultant.com'
   });

Migration depuis l'API actuelle
--------------------------------

Pour migrer depuis l'utilisation directe des services Python :

1. **Remplacer les imports de services**

   .. code-block:: python

      # Avant
      from app.services.consultant_service import ConsultantService
      consultants = ConsultantService.get_all_consultants()

      # Après
      import requests
      response = requests.get('/api/v1/consultants',
                            headers={'Authorization': 'Bearer ' + token})
      consultants = response.json()['data']

2. **Adapter la gestion d'erreurs**

   .. code-block:: python

      # Gestion d'erreurs HTTP
      try:
          response = requests.post('/api/v1/consultants', json=data)
          response.raise_for_status()
          consultant = response.json()
      except requests.exceptions.HTTPError as e:
          if e.response.status_code == 422:
              errors = e.response.json()['error']['details']
              # Traiter les erreurs de validation

3. **Implémenter la pagination**

   .. code-block:: python

      def get_all_consultants(token, page=1):
          consultants = []
          while True:
              response = requests.get(f'/api/v1/consultants?page={page}',
                                    headers={'Authorization': f'Bearer {token}'})
              data = response.json()
              consultants.extend(data['data'])

              if page >= data['pagination']['pages']:
                  break
              page += 1

          return consultants

Support et évolution
--------------------

L'API évolue selon le principe de compatibilité ascendante. Les changements breaking seront annoncés 3 mois à l'avance.

**Versions supportées**

- **v1** (actuelle) : API complète et stable
- **v2** (future) : Nouvelles fonctionnalités (Q2 2025)

**Support**

- **Documentation** : `https://api.consultator.com/docs <https://api.consultator.com/docs>`_
- **Status page** : `https://status.consultator.com <https://status.consultator.com>`_
- **Changelog** : `https://api.consultator.com/changelog <https://api.consultator.com/changelog>`_
