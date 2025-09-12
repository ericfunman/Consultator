Guide de développement
====================

Ce guide présente les bonnes pratiques et conventions de développement pour contribuer à Consultator.

Architecture du projet
----------------------

.. _dev-architecture:

Structure des dossiers
~~~~~~~~~~~~~~~~~~~~~~

::

   consultator/
   ├── app/                    # Code principal de l'application
   │   ├── database/          # Modèles et connexion base de données
   │   ├── pages/             # Pages Streamlit
   │   ├── services/          # Services métier
   │   ├── utils/             # Utilitaires et helpers
   │   └── components/        # Composants réutilisables
   ├── config/                # Configuration de l'application
   ├── tests/                 # Tests unitaires et d'intégration
   ├── docs/                  # Documentation Sphinx
   ├── scripts/               # Scripts utilitaires
   └── data/                  # Données et fichiers temporaires

Architecture en couches
~~~~~~~~~~~~~~~~~~~~~~~

**Couche présentation (Streamlit)**
    Pages et composants utilisateur dans ``app/pages/``

**Couche service**
    Logique métier dans ``app/services/``

**Couche données**
    Modèles et accès base de données dans ``app/database/``

**Couche utilitaires**
    Fonctions helpers dans ``app/utils/``

Standards de code
-----------------

.. _dev-standards:

Style Python
~~~~~~~~~~~~

**PEP 8**
    Respect strict des conventions PEP 8 avec Black pour le formatage automatique.

**Type hints**
    Utilisation systématique des annotations de type :

    .. code-block:: python

       from typing import List, Optional

       def get_consultant_by_id(consultant_id: int) -> Optional[Consultant]:
           """Récupère un consultant par son ID."""
           pass

**Docstrings**
    Documentation complète en français :

    .. code-block:: python

       def calculate_revenue(consultant: Consultant,
                           start_date: date,
                           end_date: date) -> float:
           """
           Calcule le revenu généré par un consultant sur une période.

           Args:
               consultant: Instance du consultant
               start_date: Date de début de la période
               end_date: Date de fin de la période

           Returns:
               Revenu total en euros

           Raises:
               ValueError: Si les dates sont invalides
           """
           pass

Nommage
~~~~~~~

.. list-table:: Conventions de nommage
   :header-rows: 1

   * - Élément
     - Convention
     - Exemples
   * - Classes
     - PascalCase
     - ``ConsultantService``, ``DatabaseManager``
   * - Fonctions
     - snake_case
     - ``get_consultant_by_id``, ``calculate_revenue``
   * - Variables
     - snake_case
     - ``consultant_list``, ``total_revenue``
   * - Constantes
     - UPPER_SNAKE_CASE
     - ``DATABASE_PATH``, ``MAX_RETRIES``
   * - Modules
     - snake_case
     - ``consultant_service.py``, ``database_utils.py``

Gestion d'erreurs
~~~~~~~~~~~~~~~~~

**Exceptions personnalisées**

.. code-block:: python

   class ConsultatorError(Exception):
       """Exception de base pour Consultator."""
       pass

   class ValidationError(ConsultatorError):
       """Erreur de validation des données."""
       pass

   class DatabaseError(ConsultatorError):
       """Erreur de base de données."""
       pass

**Gestion contextuelle**

.. code-block:: python

   from contextlib import contextmanager

   @contextmanager
   def database_session():
       """Context manager pour les sessions de base de données."""
       session = SessionLocal()
       try:
           yield session
           session.commit()
       except Exception as e:
           session.rollback()
           raise DatabaseError(f"Erreur base de données: {e}")
       finally:
           session.close()

**Logging**

.. code-block:: python

   import logging

   logger = logging.getLogger(__name__)

   def process_consultant_data(data: dict):
       logger.info("Début du traitement des données consultant")
       try:
           # Traitement des données
           logger.debug(f"Données reçues: {data.keys()}")
           result = validate_and_save(data)
           logger.info("Traitement terminé avec succès")
           return result
       except ValidationError as e:
           logger.warning(f"Erreur de validation: {e}")
           raise
       except Exception as e:
           logger.error(f"Erreur inattendue: {e}", exc_info=True)
           raise

Base de données
---------------

.. _dev-database:

Modèles SQLAlchemy
~~~~~~~~~~~~~~~~~~

**Définition des modèles**

.. code-block:: python

   from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
   from sqlalchemy.orm import relationship
   from sqlalchemy.ext.declarative import declarative_base

   Base = declarative_base()

   class Consultant(Base):
       __tablename__ = "consultants"

       id = Column(Integer, primary_key=True, index=True)
       nom = Column(String(100), nullable=False)
       prenom = Column(String(100), nullable=False)
       email = Column(String(200), unique=True, nullable=False)
       created_at = Column(DateTime, default=datetime.utcnow)

       # Relations
       competences = relationship("CompetenceConsultant",
                                back_populates="consultant")
       missions = relationship("Mission", back_populates="consultant")

**Migrations**

Utilisation d'Alembic pour les migrations :

.. code-block:: bash

   # Générer une nouvelle migration
   alembic revision --autogenerate -m "Ajout table missions"

   # Appliquer les migrations
   alembic upgrade head

Requêtes optimisées
~~~~~~~~~~~~~~~~~~~

**Eager loading**

.. code-block:: python

   from sqlalchemy.orm import joinedload

   def get_consultant_with_competences(consultant_id: int):
       return session.query(Consultant).options(
           joinedload(Consultant.competences)
       ).filter(Consultant.id == consultant_id).first()

**Pagination**

.. code-block:: python

   def get_consultants_paginated(page: int = 1, per_page: int = 20):
       offset = (page - 1) * per_page
       return session.query(Consultant).offset(offset).limit(per_page).all()

Services métier
---------------

.. _dev-services:

Pattern des services
~~~~~~~~~~~~~~~~~~~~

**Structure d'un service**

.. code-block:: python

   from typing import List, Optional
   from app.database.models import Consultant

   class ConsultantService:
       @staticmethod
       def get_all_consultants(page: int = 1, per_page: int = 20) -> List[Consultant]:
           """Récupère tous les consultants avec pagination."""
           with database_session() as session:
               return session.query(Consultant).offset(
                   (page - 1) * per_page
               ).limit(per_page).all()

       @staticmethod
       def get_consultant_by_id(consultant_id: int) -> Optional[Consultant]:
           """Récupère un consultant par son ID."""
           with database_session() as session:
               return session.query(Consultant).filter(
                   Consultant.id == consultant_id
               ).first()

       @staticmethod
       def create_consultant(data: dict) -> Consultant:
           """Crée un nouveau consultant."""
           # Validation des données
           validated_data = ConsultantValidator.validate(data)

           with database_session() as session:
               consultant = Consultant(**validated_data)
               session.add(consultant)
               return consultant

**Injection de dépendances**

.. code-block:: python

   from dependency_injector import containers, providers

   class Container(containers.DeclarativeContainer):
       config = providers.Configuration()

       database = providers.Singleton(DatabaseManager, config.database)

       consultant_service = providers.Factory(
           ConsultantService,
           database=database
       )

Tests
-----

.. _dev-testing:

Structure des tests
~~~~~~~~~~~~~~~~~~~

::

   tests/
   ├── unit/                  # Tests unitaires
   │   ├── test_consultant_service.py
   │   └── test_validators.py
   ├── integration/          # Tests d'intégration
   │   ├── test_database_integration.py
   │   └── test_api_integration.py
   ├── fixtures/             # Données de test
   │   ├── consultants.json
   │   └── sample_data.sql
   └── conftest.py           # Configuration pytest

Tests unitaires
~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from unittest.mock import Mock, patch
   from app.services.consultant_service import ConsultantService

   class TestConsultantService:
       def test_get_consultant_by_id_success(self, mock_session):
           # Arrange
           expected_consultant = Mock()
           mock_session.query.return_value.filter.return_value.first.return_value = expected_consultant

           # Act
           result = ConsultantService.get_consultant_by_id(1)

           # Assert
           assert result == expected_consultant
           mock_session.query.assert_called_once()

       def test_get_consultant_by_id_not_found(self, mock_session):
           # Arrange
           mock_session.query.return_value.filter.return_value.first.return_value = None

           # Act
           result = ConsultantService.get_consultant_by_id(999)

           # Assert
           assert result is None

Tests d'intégration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from app.database.database import init_database, reset_database

   @pytest.fixture(scope="session", autouse=True)
   def setup_test_database():
       """Initialise la base de test au début de la session."""
       init_database()
       yield
       reset_database()

   def test_consultant_creation_integration(test_client, sample_consultant_data):
       # Act
       response = test_client.post("/api/consultants", json=sample_consultant_data)

       # Assert
       assert response.status_code == 201
       data = response.get_json()
       assert data["nom"] == sample_consultant_data["nom"]
       assert "id" in data

Couverture de code
~~~~~~~~~~~~~~~~~~

Objectif de couverture : **90% minimum**

.. code-block:: bash

   # Exécuter les tests avec couverture
   pytest --cov=app --cov-report=html --cov-report=term

   # Générer le rapport HTML
   open htmlcov/index.html

CI/CD
-----

.. _dev-cicd:

Pipeline GitHub Actions
~~~~~~~~~~~~~~~~~~~~~~~

Le pipeline comprend :

1. **Linting** : flake8, black, isort
2. **Tests** : pytest avec couverture
3. **Sécurité** : audit des dépendances
4. **Documentation** : build Sphinx
5. **Déploiement** : vers staging/production

Configuration locale
~~~~~~~~~~~~~~~~~~~~

**Pre-commit hooks**

.. code-block:: bash

   # Installation
   pre-commit install

   # Exécution manuelle
   pre-commit run --all-files

**Qualité du code**

.. code-block:: bash

   # Analyse complète
   python run_quality_pipeline.py

   # Tests uniquement
   pytest

   # Linting
   flake8 app/ tests/

Déploiement
-----------

.. _dev-deployment:

Environnements
~~~~~~~~~~~~~~

- **Development** : Environnement local des développeurs
- **Staging** : Environnement de pré-production
- **Production** : Environnement de production

Variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # .env.development
   APP_ENV=development
   DEBUG=True
   DATABASE_URL=sqlite:///data/dev.db
   LOG_LEVEL=DEBUG

   # .env.production
   APP_ENV=production
   DEBUG=False
   DATABASE_URL=postgresql://user:pass@host:5432/consultator
   LOG_LEVEL=INFO

Containerisation
~~~~~~~~~~~~~~~~

**Dockerfile**

.. code-block:: dockerfile

   FROM python:3.11-slim

   WORKDIR /app

   # Installation des dépendances système
   RUN apt-get update && apt-get install -y \
       gcc \
       && rm -rf /var/lib/apt/lists/*

   # Installation des dépendances Python
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copie du code
   COPY . .

   # Exposition du port
   EXPOSE 8501

   # Commande de démarrage
   CMD ["streamlit", "run", "run.py", "--server.port=8501", "--server.address=0.0.0.0"]

**Docker Compose**

.. code-block:: yaml

   version: '3.8'
   services:
     consultator:
       build: .
       ports:
         - "8501:8501"
       volumes:
         - ./data:/app/data
       environment:
         - DATABASE_URL=sqlite:///data/consultator.db
       depends_on:
         - postgres

     postgres:
       image: postgres:15
       environment:
         POSTGRES_DB: consultator
         POSTGRES_USER: consultator
         POSTGRES_PASSWORD: password
       volumes:
         - postgres_data:/var/lib/postgresql/data

Monitoring
----------

.. _dev-monitoring:

Logs
~~~~

**Configuration centralisée**

.. code-block:: python

   import logging.config

   LOGGING_CONFIG = {
       'version': 1,
       'formatters': {
           'detailed': {
               'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
           }
       },
       'handlers': {
           'file': {
               'class': 'logging.FileHandler',
               'filename': 'logs/consultator.log',
               'formatter': 'detailed'
           },
           'console': {
               'class': 'logging.StreamHandler',
               'formatter': 'detailed'
           }
       },
       'root': {
           'level': 'INFO',
           'handlers': ['file', 'console']
       }
   }

   logging.config.dictConfig(LOGGING_CONFIG)

Métriques
~~~~~~~~~

**Performance**

- Temps de réponse des API
- Utilisation CPU/Mémoire
- Nombre de requêtes par minute
- Taux d'erreur

**Métier**

- Nombre de consultants actifs
- CA généré
- Taux de satisfaction client
- Temps de traitement des imports

Alertes
~~~~~~~

**Seuils critiques**

- Erreur 5xx > 5% des requêtes
- Temps de réponse > 5 secondes
- Utilisation disque > 90%
- Échec des sauvegardes

Contribution
------------

.. _dev-contribution:

Workflow Git
~~~~~~~~~~~~

1. **Créer une branche**

   .. code-block:: bash

      git checkout -b feature/nouvelle-fonctionnalite

2. **Développer**

   - Écrire des tests
   - Implémenter la fonctionnalité
   - Respecter les standards de code

3. **Commiter**

   .. code-block:: bash

      git add .
      git commit -m "feat: ajout nouvelle fonctionnalité

      - Description détaillée
      - Tests ajoutés
      - Documentation mise à jour"

4. **Créer une PR**

   - Push de la branche
   - Création de la Pull Request
   - Revue par les pairs

Types de commits
~~~~~~~~~~~~~~~~

- ``feat:`` Nouvelle fonctionnalité
- ``fix:`` Correction de bug
- ``docs:`` Modification de la documentation
- ``style:`` Changement de style (formatage, etc.)
- ``refactor:`` Refactorisation du code
- ``test:`` Ajout ou modification de tests
- ``chore:`` Tâche de maintenance

Code review
~~~~~~~~~~~

**Checklist**

- [ ] Tests unitaires présents et passant
- [ ] Code respecte les standards PEP 8
- [ ] Type hints présents
- [ ] Documentation à jour
- [ ] Pas de code dupliqué
- [ ] Performance acceptable
- [ ] Sécurité respectée

Support
-------

**Ressources**

- **Wiki équipe** : Guides détaillés et bonnes pratiques
- **Slack** : Canal #dev pour les questions techniques
- **Issues GitHub** : Bug reports et feature requests

**Points de contact**

- **Tech Lead** : jean.dupont@consultator.com
- **DevOps** : marie.martin@consultator.com
- **Product Owner** : paul.bernard@consultator.com
