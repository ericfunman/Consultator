# 👥 Consultator

**Plateforme de gestion intelligente pour practice data**

[![CI/CD Pipeline](https://github.com/ericfunman/Consultator/actions/workflows/ci.yml/badge.svg)](https://github.com/ericfunman/Consultator/actions/workflows/ci.yml)
[![Code Coverage](https://codecov.io/gh/ericfunman/Consultator/branch/master/graph/badge.svg)](https://codecov.io/gh/ericfunman/Consultator)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-green.svg)](https://github.com/ericfunman/Consultator)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Une application Streamlit moderne pour gérer efficacement vos équipes de consultants, leurs compétences, missions et performances.

## 🎯 Fonctionnalités

### Phase 1 - CRUD de base ✅
- **Gestion des consultants** : Ajout, modification, suppression des profils
- **Gestion des compétences** : Association compétences techniques et fonctionnelles
- **Gestion des missions** : Suivi des missions et revenus
- **Import de CV** : Parsing automatique des CVs (PDF/Word)
- **Tableaux de bord** : Métriques et visualisations

### Phase 2 - Analytics (À venir)
- **Dashboards avancés** : Analyses détaillées des compétences et revenus
- **Rapports automatiques** : Export Excel/PDF
- **Métriques business** : KPIs et indicateurs de performance

### Phase 3 - IA (À venir)
- **Chatbot intégré** : Recherche intelligente par compétences
- **Analyses prédictives** : Recommandations de staffing
- **Matching automatique** : Consultant → Mission optimal

## 🚀 Installation et démarrage

### Prérequis
- Python 3.8+
- pip
- Git

### Installation
```bash
# Cloner le projet
git clone https://github.com/ericfunman/Consultator.git
cd Consultator

# Installer les dépendances
pip install -r requirements.txt

# Configuration du pipeline CI/CD (recommandé)
python setup_ci_cd.py

# Lancer l'application
python run.py
```

### Configuration CI/CD (Optionnel mais recommandé)
```bash
# Installation des outils de développement
python setup_ci_cd.py

# Ou installation manuelle
pip install pre-commit pytest-cov pylint black flake8 isort bandit radon
pre-commit install
```

### Accès
- **URL locale** : http://localhost:8501
- **Interface** : Streamlit moderne et responsive

## 📁 Structure du projet

```
Consultator/
├── 📁 app/                     # Application principale
│   ├── main.py                 # Point d'entrée Streamlit
│   ├── 📁 pages/               # Pages de l'application
│   │   ├── home.py            # Dashboard principal
│   │   ├── consultants.py     # Gestion consultants
│   │   ├── skills.py          # Gestion compétences
│   │   └── missions.py        # Gestion missions
│   ├── 📁 database/           # Modèles et DB
│   │   ├── models.py          # Modèles SQLAlchemy
│   │   └── database.py        # Configuration DB
│   ├── 📁 services/           # Logique métier
│   ├── 📁 utils/              # Utilitaires
│   │   └── skill_categories.py # Référentiel compétences
│   └── 📁 components/         # Composants réutilisables
├── 📁 data/                   # Base de données et uploads
│   ├── consultator.db         # Base SQLite
│   └── uploads/               # CVs uploadés
├── 📁 config/                 # Configuration
│   └── settings.py            # Paramètres application
├── requirements.txt           # Dépendances Python
├── run.py                     # Script de lancement
└── README.md                  # Documentation
```

## 🗂️ Modèle de données

### Entités principales
- **Consultant** : Profil complet (nom, contact, salaire, disponibilité)
- **Compétence** : Référentiel technique/fonctionnel par catégorie
- **Mission** : Historique missions avec revenus et technologies
- **CV** : Gestion upload et parsing automatique

### Relations
- Consultant ↔ Compétences (Many-to-Many avec années d'expérience)
- Consultant ↔ Missions (One-to-Many avec détails financiers)
- Consultant ↔ CVs (One-to-Many avec contenu parsé)

## 🎯 Référentiel des compétences

### Techniques par catégorie
- **Backend** : Java, Python, .NET, Node.js, microservices...
- **Frontend** : React, Angular, Vue.js, TypeScript...
- **Data** : SQL, Spark, Kafka, ML, Python Data...
- **Cloud** : AWS, Azure, GCP, Docker, Kubernetes...
- **Mobile** : React Native, Flutter, iOS, Android...

### Fonctionnelles par secteur
- **Finance** : Banking, Trading, Risk Management...
- **Assurance** : Actuariat, Solvency II, Souscription...
- **Santé** : FDA, Clinical Trials, HIPAA...
- **Industrie** : Lean Manufacturing, IoT, Industrie 4.0...

## 🛠️ Technologies utilisées

### Core Stack
- **Backend** : Python 3.8+, SQLAlchemy
- **Frontend** : Streamlit, Plotly, Pandas
- **Database** : SQLite (local)
- **ML/IA** : Prévu pour Phase 3 (OpenAI, LangChain)

### Librairies principales
- `streamlit` : Interface web moderne
- `pandas` : Manipulation de données
- `sqlalchemy` : ORM base de données
- `plotly` : Visualisations interactives
- `pypdf` / `python-docx` : Parsing CVs

### Outils de qualité et CI/CD
- **Tests** : pytest, pytest-cov, pytest-xdist
- **Qualité** : pylint, black, flake8, isort, bandit, radon
- **CI/CD** : GitHub Actions, pre-commit hooks
- **Couverture** : Codecov

## 🔄 Pipeline CI/CD

### Workflows automatisés
- **Tests automatisés** : Exécution sur push/PR (multi-version Python)
- **Contrôle qualité** : Black, isort, flake8, pylint, bandit
- **Couverture de code** : Rapport automatique avec Codecov
- **Sécurité** : Analyse Bandit intégrée
- **Complexité** : Vérification Radon

### Pre-commit hooks
```bash
# Installation
pre-commit install

# Exécution manuelle
pre-commit run --all-files

# Hooks disponibles
- trailing-whitespace    # Suppression espaces fin de ligne
- black                 # Formatage automatique
- isort                 # Tri des imports
- flake8               # Linting PEP8
- pylint               # Analyse qualité avancée
- bandit               # Analyse sécurité
- radon                # Complexité cyclomatique
- pytest               # Tests automatiques
```

### Métriques de qualité
- **Couverture de code** : >75% (objectif 80%+)
- **Score Pylint** : 8.24/10 (objectif 9.0/10)
- **Tests** : 296 tests fonctionnels
- **Sécurité** : 0 vulnérabilités détectées

## 📋 Cas d'usage

### 🏢 Directeur Practice Data
- Vue d'ensemble des 60 consultants
- Métriques de performance et revenus
- Planification des missions

### 👥 Manager équipe
- Recherche par compétences
- Disponibilité consultants
- Suivi missions en cours

### 📊 Business Analyst
- Analyses de compétences
- ROI par consultant
- Évolution du portefeuille

## 🔮 Roadmap

### ✅ Phase 1 - CRUD Core (Terminée)
- [x] Structure projet et DB
- [x] Gestion consultants de base
- [x] Interface Streamlit
- [x] Upload CV (structure)

### ✅ Phase 2 - Analytics avancés (Terminée)
- [x] Dashboards avec Plotly
- [x] Métriques et visualisations
- [x] Tableaux de bord interactifs

### ✅ Phase 3 - Tests et qualité (Terminée)
- [x] Suite de tests complète (296 tests)
- [x] Tests parallèles et couverture
- [x] Classes de base réutilisables
- [x] Chatbot IA intégré

### 🚀 Phase 4 - CI/CD Automatisé (En cours)
- [x] GitHub Actions workflows
- [x] Pre-commit hooks configurés
- [x] Tests automatisés sur push/PR
- [x] Intégration Codecov
- [x] Analyse sécurité automatisée
- [ ] Déploiement automatisé
- [ ] Documentation CI/CD

### 🔮 Phase 5 - Fonctionnalités avancées
- [ ] Parsing CV automatique (PDF/Word)
- [ ] Export Excel/PDF avancé
- [ ] Recherche sémantique IA
- [ ] API REST FastAPI
- [ ] Notifications temps réel

### 🔮 Phase 6 - Intelligence artificielle
- [ ] Analyses prédictives staffing
- [ ] Recommandations automatiques
- [ ] Chatbot conversationnel avancé
- [ ] Intégration modèles ML personnalisés

## 🤝 Contribution

Le projet est en développement actif. Les contributions sont les bienvenues !

### Développement local
```bash
# Installation mode développement
pip install -r requirements.txt

# Lancement avec hot-reload
streamlit run app/main.py

# Tests (à venir)
pytest tests/
```

## 📞 Support

Pour toute question ou suggestion :
- 📧 Email : support@consultator.com
- 💬 Issues : GitHub Issues
- 📚 Wiki : Documentation complète

---

**Consultator v1.0.0** - Transformez la gestion de votre practice data ! 🚀
