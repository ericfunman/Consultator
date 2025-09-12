Installation et Configuration
============================

Cette section explique comment installer et configurer Consultator sur votre système.

Prérequis système
-----------------

**Python**
    - Version 3.8 ou supérieure
    - Recommandé : Python 3.11 ou 3.12

**Système d'exploitation**
    - Windows 10/11
    - macOS 12+
    - Linux (Ubuntu 20.04+, CentOS 8+)

**Mémoire RAM**
    - Minimum : 4 GB
    - Recommandé : 8 GB ou plus

Installation rapide
-------------------

1. **Cloner le repository**

   .. code-block:: bash

      git clone https://github.com/votre-organisation/consultator.git
      cd consultator

2. **Créer un environnement virtuel**

   .. code-block:: bash

      python -m venv venv
      # Windows
      venv\Scripts\activate
      # Linux/macOS
      source venv/bin/activate

3. **Installer les dépendances**

   .. code-block:: bash

      pip install -r requirements.txt

4. **Initialiser la base de données**

   .. code-block:: bash

      python -c "from app.database.database import init_database; init_database()"

5. **Lancer l'application**

   .. code-block:: bash

      streamlit run run.py

Installation détaillée
----------------------

Configuration de l'environnement de développement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour les développeurs souhaitant contribuer au projet :

.. code-block:: bash

   # Installation des dépendances de développement
   pip install -r requirements-dev.txt

   # Installation des outils de qualité
   pip install -r requirements-test.txt

   # Configuration de pre-commit
   pre-commit install

Configuration de la base de données
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La base de données SQLite est créée automatiquement. Pour une configuration personnalisée :

.. code-block:: python

   # Dans config/settings.py
   DATABASE_URL = "sqlite:///data/consultator.db"

Configuration des variables d'environnement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Créer un fichier ``.env`` à la racine du projet :

.. code-block:: bash

   # Configuration de l'application
   APP_ENV=development
   DEBUG=True

   # Configuration de la base de données
   DATABASE_URL=sqlite:///data/consultator.db

   # Configuration du logging
   LOG_LEVEL=INFO
   LOG_FILE=logs/consultator.log

Dépannage
---------

Problèmes courants et solutions :

**Erreur d'importation de modules**
    Vérifier que l'environnement virtuel est activé et que toutes les dépendances sont installées.

**Erreur de base de données**
    Supprimer le fichier de base de données et relancer l'initialisation :

    .. code-block:: bash

       rm data/consultator.db
       python -c "from app.database.database import init_database; init_database()"

**Problèmes de performance**
    - Vérifier la version de Python (3.11+ recommandé)
    - Augmenter la mémoire RAM si nécessaire
    - Utiliser un SSD pour le stockage

Mise à jour
-----------

Pour mettre à jour Consultator :

.. code-block:: bash

   # Récupérer les dernières modifications
   git pull origin main

   # Mettre à jour les dépendances
   pip install -r requirements.txt --upgrade

   # Migrer la base de données si nécessaire
   python scripts/migrate_database.py

Support
-------

En cas de problème d'installation :

- Consulter la `documentation complète <https://consultator.readthedocs.io/>`_
- Ouvrir une `issue sur GitHub <https://github.com/votre-organisation/consultator/issues>`_
- Contacter l'équipe de développement
