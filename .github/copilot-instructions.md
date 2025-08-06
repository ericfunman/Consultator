<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Consultator - Instructions pour GitHub Copilot

## Context du projet
Consultator est une application Streamlit pour la gestion d'une practice data de 60 consultants. L'application permet de gérer les profils, compétences, missions et revenus des consultants avec des fonctionnalités d'analyse et un futur chatbot IA.

## Architecture et technologies
- **Framework** : Streamlit pour l'interface web
- **Base de données** : SQLite avec SQLAlchemy ORM
- **Structure** : Application modulaire avec pages, services, modèles
- **Python** : Version 3.8+ avec type hints recommandés
- **Frontend** : Streamlit natif avec Plotly pour les graphiques

## Standards de code

### Style Python
- Utiliser les type hints systématiquement
- Suivre PEP 8 pour le formatage
- Docstrings en français pour les fonctions principales
- Noms de variables et fonctions en français quand approprié
- Gestion d'erreurs avec try/except explicites

### Structure Streamlit
- Une fonction `show()` par page principale
- Utiliser `st.columns()` pour la mise en page
- Caching avec `@st.cache_data` pour les requêtes DB
- Session state pour la persistance des données
- Forms pour les soumissions de données

### Base de données
- Modèles SQLAlchemy avec relations explicites
- Sessions de DB gérées avec context managers
- Requêtes optimisées avec eager loading si nécessaire
- Transactions pour les opérations multi-tables

## Conventions spécifiques

### Nommage
- Classes : PascalCase (ex: `ConsultantService`)
- Fonctions : snake_case (ex: `get_consultant_by_id`)
- Variables : snake_case (ex: `consultant_list`)
- Constantes : UPPER_SNAKE_CASE (ex: `DATABASE_PATH`)

### Organisation des fichiers
- Pages Streamlit dans `app/pages/`
- Modèles de données dans `app/database/models.py`
- Services métier dans `app/services/`
- Utilitaires dans `app/utils/`
- Configuration dans `config/settings.py`

### Gestion des erreurs
- Messages d'erreur en français pour l'utilisateur
- Logs en anglais pour le debug
- Utiliser `st.error()`, `st.warning()`, `st.success()` pour l'UX
- Validation des formulaires côté client ET serveur

## Fonctionnalités clés à respecter

### CRUD Consultants
- Formulaires avec validation complète
- Upload de CV avec parsing automatique
- Gestion des compétences avec années d'expérience
- Historique des missions avec revenus

### Interface utilisateur
- Design cohérent avec les couleurs de l'app (#1f77b4 pour le bleu principal)
- Tableaux interactifs avec tri et filtres
- Métriques visuelles avec `st.metric()`
- Navigation fluide entre les pages

### Performance
- Pagination pour les grandes listes
- Cache des requêtes fréquentes
- Chargement lazy des données volumineuses
- Optimisation des requêtes SQL

## Patterns recommandés

### Services
```python
class ConsultantService:
    @staticmethod
    def get_all_consultants(page: int = 1, per_page: int = 20) -> List[Consultant]:
        # Implémentation avec pagination
        pass
    
    @staticmethod
    def create_consultant(data: dict) -> Consultant:
        # Validation et création
        pass
```

### Pages Streamlit
```python
def show():
    st.title("📋 Titre de la page")
    
    # Tabs pour organiser le contenu
    tab1, tab2 = st.tabs(["Vue", "Actions"])
    
    with tab1:
        show_content()
    
    with tab2:
        show_actions()

def show_content():
    # Contenu principal avec colonnes
    col1, col2 = st.columns(2)
    # ...
```

### Formulaires
```python
with st.form("form_name"):
    # Champs du formulaire
    data = collect_form_data()
    
    submitted = st.form_submit_button("Valider")
    if submitted:
        if validate_data(data):
            save_data(data)
            st.success("✅ Données sauvegardées !")
        else:
            st.error("❌ Erreurs de validation")
```

## Données de test
Utiliser des données françaises réalistes :
- Noms : Dupont, Martin, Bernard, Durand, Moreau
- Prénoms : Jean, Marie, Pierre, Paul, Sophie
- Compétences : Référentiel dans `utils/skill_categories.py`
- Missions : Clients français (Société Générale, BNP Paribas, etc.)

## Évolutions futures
- Phase 2 : Analytics avancés avec Plotly
- Phase 3 : Chatbot IA avec LangChain/OpenAI
- Export Excel/PDF avec pandas et reportlab
- API REST avec FastAPI si nécessaire

## Priorités de développement
1. CRUD consultants complet et robuste
2. Gestion des compétences avec référentiel
3. Parsing CV automatique (PDF/Word)
4. Tableaux de bord avec métriques
5. Recherche avancée et filtres
6. Chatbot IA intégré
