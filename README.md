# 👥 Consultator

**Plateforme de gestion intelligente pour practice data**

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

### Installation
```bash
# Cloner le projet
git clone <repo-url>
cd Consultator

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run.py
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

### Version 1.0 - CRUD Core ✅
- [x] Structure projet et DB
- [x] Gestion consultants de base
- [x] Interface Streamlit
- [x] Upload CV (structure)

### Version 1.1 - Fonctionnalités avancées
- [ ] CRUD compétences complet
- [ ] Gestion missions avec revenus
- [ ] Parsing CV automatique
- [ ] Tableaux de bord analytics

### Version 1.2 - Intelligence
- [ ] Chatbot IA intégré
- [ ] Recommandations staffing
- [ ] Export rapports automatiques
- [ ] Notifications et alertes

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
