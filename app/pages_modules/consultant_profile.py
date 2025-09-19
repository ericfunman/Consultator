"""
Module de gestion du profil consultant
Fonctions principales pour l'affichage et la navigation du profil
"""

import os
import sys

import streamlit as st

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Variables pour les imports
ConsultantService = None
get_database_session = None
Mission = None
imports_ok = False

try:
    from sqlalchemy.orm import joinedload

    from database.database import get_database_session
    from database.models import Consultant
    from database.models import Mission
    from services.consultant_service import ConsultantService
    from services.document_service import DocumentService

    imports_ok = True
except ImportError:
    # Imports échoués, on continue quand même
    pass


def show():
    """Affiche la page de gestion des consultants"""

    st.title("👥 Gestion des consultants")
    st.markdown("### Gérez les profils de vos consultants")

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        st.info("Vérifiez que tous les modules sont correctement installés")
        return

    # Vérifier si on doit afficher le profil d'un consultant spécifique
    if "view_consultant_profile" in st.session_state:
        show_consultant_profile()
        return

    # Onglets pour organiser les fonctionnalités
    tab1, tab2 = st.tabs(["📋 Liste des consultants", "➕ Ajouter un consultant"])

    with tab1:
        # Utiliser la fonction du fichier consultants.py principal
        from .consultants import show_consultants_list_tab

        show_consultants_list_tab()

    with tab2:
        # Utiliser la fonction du fichier consultants.py principal
        from .consultants import show_add_consultant_form_tab

        show_add_consultant_form_tab()


def _load_consultant_data(consultant_id):
    """Charge les données d'un consultant avec gestion d'erreurs."""
    with get_database_session() as session:
        consultant = (
            session.query(Consultant)
            .options(joinedload(Consultant.practice))
            .filter(Consultant.id == consultant_id)
            .first()
        )

        if not consultant:
            return None, None

        # Charger toutes les données nécessaires dans la session
        practice_name = (
            consultant.practice.nom if consultant.practice else "Non affecté"
        )

        # Créer un dictionnaire avec toutes les données nécessaires
        consultant_data = {
            "id": consultant.id,
            "prenom": consultant.prenom,
            "nom": consultant.nom,
            "email": consultant.email,
            "telephone": consultant.telephone,
            "salaire_actuel": consultant.salaire_actuel,
            "disponibilite": consultant.disponibilite,
            "notes": consultant.notes,
            "date_creation": consultant.date_creation,
            "practice_name": practice_name,
        }

        return consultant_data, session


def _show_consultant_not_found(consultant_id):
    """Affiche une erreur si le consultant n'est pas trouvé."""
    st.error(f"❌ Consultant introuvable (ID: {consultant_id})")
    st.warning(
        "💡 Vérifiez que l'ID est correct et que le consultant existe dans la base de données"
    )

    # Debug: Lister tous les consultants pour voir lesquels existent
    with get_database_session() as session:
        all_consultants = session.query(Consultant).all()
        st.write("**🔍 Consultants existants dans la DB:**")
        for c in all_consultants[:10]:  # Afficher les 10 premiers
            st.write(f"- ID: {c.id}, Nom: {c.prenom} {c.nom}")
        if len(all_consultants) > 10:
            st.write(f"... et {len(all_consultants) - 10} autres")

    if st.button("← Retour à la liste", key="back_to_list_error"):
        del st.session_state.view_consultant_profile
        st.rerun()


def _display_consultant_header(consultant_data):
    """Affiche l'en-tête du profil consultant."""
    col1, col2 = st.columns([6, 1])

    with col1:
        st.title(
            "👤 Profil de " + consultant_data["prenom"] + " " + consultant_data["nom"]
        )

    with col2:
        if st.button("← Retour", key="back_to_list"):
            del st.session_state.view_consultant_profile
            st.rerun()

    st.markdown("---")


def _display_consultant_metrics(consultant_data):
    """Affiche les métriques principales du consultant."""
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        salaire = consultant_data["salaire_actuel"] or 0
        st.metric("💰 Salaire annuel", f"{salaire:,}€")

    with col2:
        # Calcul du CJM (Coût Journalier Moyen)
        cjm = (salaire * 1.8 / 216) if salaire else 0
        st.metric("📈 CJM", f"{cjm:,.0f}€")

    with col3:
        status = (
            "✅ Disponible" if consultant_data["disponibilite"] else "🔴 En mission"
        )
        st.metric("📊 Statut", status)

    with col4:
        creation_date = (
            consultant_data["date_creation"].strftime("%d/%m/%Y")
            if consultant_data["date_creation"]
            else "N/A"
        )
        st.metric("📅 Membre depuis", creation_date)

    with col5:
        st.metric("🏢 Practice", consultant_data["practice_name"])

    st.markdown("---")


def _display_consultant_tabs(consultant_id):
    """Affiche les onglets de détail du consultant."""
    with get_database_session() as session:
        consultant_obj = (
            session.query(Consultant).filter(Consultant.id == consultant_id).first()
        )

        # Onglets de détail
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "📋 Informations",
                "💼 Compétences",
                "🌍 Langues",
                "🚀 Missions",
                "📁 Documents",
            ]
        )

        with tab1:
            from .consultants import show_consultant_info_tab

            show_consultant_info_tab(consultant_obj)

        with tab2:
            from .consultants import show_consultant_skills_tab

            show_consultant_skills_tab(consultant_obj)

        with tab3:
            from .consultants import show_consultant_languages_tab

            show_consultant_languages_tab(consultant_obj)

        with tab4:
            from .consultants import show_consultant_missions_tab

            show_consultant_missions_tab(consultant_obj)

        with tab5:
            from .consultants import show_consultant_documents_tab

            show_consultant_documents_tab(consultant_obj)


def show_consultant_profile():
    """Affiche le profil détaillé d'un consultant avec gestion d'erreurs améliorée"""

    consultant_id = st.session_state.view_consultant_profile

    try:
        consultant_data, _ = _load_consultant_data(consultant_id)

        if not consultant_data:
            _show_consultant_not_found(consultant_id)
            return

        _display_consultant_header(consultant_data)
        _display_consultant_metrics(consultant_data)

        # Affichage de l'analyse CV en PLEINE LARGEUR (si disponible)
        if "cv_analysis" in st.session_state:
            show_cv_analysis_fullwidth()
            st.markdown("---")

        _display_consultant_tabs(consultant_id)

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du profil consultant: {e}")
        st.code(str(e))

        # Bouton manuel pour retourner à la liste
        if st.button("← Retour à la liste", key="back_to_list_exception"):
            del st.session_state.view_consultant_profile
            st.rerun()


def show_cv_analysis_fullwidth():
    """Affiche l'analyse CV en pleine largeur au-dessus des onglets"""

    if "cv_analysis" not in st.session_state:
        return

    cv_data = st.session_state.cv_analysis
    analysis = cv_data["analysis"]
    consultant = cv_data["consultant"]
    file_name = cv_data["file_name"]

    # CSS pour forcer la pleine largeur
    st.markdown(
        """
    <style>
    .cv-analysis-container {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 1rem !important;
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 2px solid #1f77b4;
    }
    .stContainer {
        max-width: 100% !important;
        width: 100% !important;
    }
    .element-container {
        width: 100% !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # En-tête de l'analyse
    col_header1, col_header2, col_header3 = st.columns([6, 1, 1])

    with col_header1:
        st.markdown(f"### 🔍 Analyse CV : {file_name}")
        st.markdown(f"**Consultant :** {consultant.prenom} {consultant.nom}")

    with col_header2:
        if st.button("🔄 Réanalyser", help="Lancer une nouvelle analyse"):
            del st.session_state.cv_analysis
            st.rerun()

    with col_header3:
        if st.button("❌ Fermer", help="Fermer l'analyse"):
            del st.session_state.cv_analysis
            st.rerun()

    # Container principal en pleine largeur
    with st.container():
        st.markdown('<div class="cv-analysis-container">', unsafe_allow_html=True)

        # Onglets pour les résultats - mais EN PLEINE LARGEUR
        tab1, tab2, tab3, tab4 = st.tabs(
            ["📋 Missions", "🛠️ Compétences", "📊 Résumé", "💾 Actions"]
        )

        with tab1:
            show_cv_missions_tab(analysis.get("missions", []))

        with tab2:
            show_cv_skills_tab(analysis)

        with tab3:
            show_cv_summary_tab(analysis)

        with tab4:
            show_cv_actions_tab(analysis)

        st.markdown("</div>", unsafe_allow_html=True)


def show_cv_missions_tab(missions):
    """Affiche l'onglet des missions du CV"""
    st.markdown("### 📋 Missions détectées")

    if not missions:
        st.info("Aucune mission détectée dans le CV")
        return

    for i, mission in enumerate(missions, 1):
        with st.expander(
            f"Mission {i}: {mission.get('titre', 'Sans titre')}", expanded=False
        ):
            st.write(f"**Client:** {mission.get('client', 'Non spécifié')}")
            st.write(f"**Période:** {mission.get('periode', 'Non spécifiée')}")
            st.write(
                f"**Technologies:** {mission.get('technologies', 'Non spécifiées')}"
            )
            if mission.get("description"):
                st.write(f"**Description:** {mission.get('description')}")


def show_cv_skills_tab(analysis):
    """Affiche l'onglet des compétences du CV"""
    st.markdown("### 🛠️ Compétences détectées")

    competences = analysis.get("competences", [])
    if not competences:
        st.info("Aucune compétence détectée dans le CV")
        return

    # Grouper par catégorie
    skills_by_category = {}
    for skill in competences:
        category = categorize_skill(skill)
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)

    for category, skills in skills_by_category.items():
        st.markdown(f"**{category}**")
        for skill in skills:
            st.write(f"• {skill}")
        st.markdown("---")


def show_cv_summary_tab(analysis):
    """Affiche l'onglet de résumé du CV"""
    st.markdown("### 📊 Résumé de l'analyse")

    # Score qualité
    score = calculate_cv_quality_score(analysis)
    st.metric("Score qualité du CV", f"{score}/100")

    # Statistiques
    col1, col2, col3 = st.columns(3)

    with col1:
        missions_count = len(analysis.get("missions", []))
        st.metric("Missions détectées", missions_count)

    with col2:
        skills_count = len(analysis.get("competences", []))
        st.metric("Compétences détectées", skills_count)

    with col3:
        contact = analysis.get("contact", {})
        completeness = sum(
            [1 for field in ["email", "phone", "linkedin"] if contact.get(field)]
        )
        st.metric("Complétude contact", f"{completeness}/3")

    # Résumé textuel
    resume = analysis.get("resume", "")
    if resume:
        st.markdown("**Résumé extrait:**")
        st.write(resume)


def show_cv_actions_tab(analysis):
    """Affiche l'onglet des actions du CV"""
    st.markdown("### 💾 Actions disponibles")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Télécharger le rapport d'analyse", key="download_cv_report"):
            st.info("Fonctionnalité de téléchargement à implémenter")

        if st.button("🔄 Synchroniser avec le profil", key="sync_cv_profile"):
            st.info("Fonctionnalité de synchronisation à implémenter")

    with col2:
        if st.button("📧 Partager l'analyse", key="share_cv_analysis"):
            st.info("Fonctionnalité de partage à implémenter")

        if st.button("🗂️ Archiver l'analyse", key="archive_cv_analysis"):
            st.info("Fonctionnalité d'archivage à implémenter")


def categorize_skill(skill):
    """Catégorise une compétence"""
    skill_lower = skill.lower()

    # Check for exact matches first, then substrings
    if any(
        keyword == skill_lower
        for keyword in [
            "python",
            "java",
            "javascript",
            "c++",
            "php",
            "ruby",
            "go",
            "rust",
            "c#",
            ".net",
        ]
    ):
        return "💻 Langages de programmation"
    elif any(
        keyword == skill_lower
        for keyword in [
            "sql",
            "mysql",
            "postgresql",
            "mongodb",
            "oracle",
            "sqlite",
            "redis",
        ]
    ):
        return "🗄️ Bases de données"
    elif any(
        keyword == skill_lower
        for keyword in [
            "aws",
            "azure",
            "gcp",
            "docker",
            "kubernetes",
            "terraform",
            "jenkins",
        ]
    ):
        return "☁️ Cloud & DevOps"
    elif any(
        keyword == skill_lower
        for keyword in ["agile", "scrum", "kanban", "uml", "merise"]
    ):
        return "📋 Méthodologies"
    # Then check for substrings
    elif any(
        keyword in skill_lower
        for keyword in [
            "python",
            "java",
            "javascript",
            "c++",
            "php",
            "ruby",
            "golang",
            "rust",
            "csharp",
            "dotnet",
        ]
    ):
        return "💻 Langages de programmation"
    elif any(
        keyword in skill_lower
        for keyword in [
            "sql",
            "mysql",
            "postgres",
            "mongo",
            "oracle",
            "sqlite",
            "redis",
        ]
    ):
        return "🗄️ Bases de données"
    elif any(
        keyword in skill_lower
        for keyword in [
            "aws",
            "azure",
            "gcp",
            "docker",
            "kubernetes",
            "terraform",
            "jenkins",
            "devops",
            "cloud",
        ]
    ):
        return "☁️ Cloud & DevOps"
    elif any(
        keyword in skill_lower
        for keyword in ["agile", "scrum", "kanban", "uml", "merise", "methodology"]
    ):
        return "📋 Méthodologies"
    else:
        return "🛠️ Autres technologies"


def calculate_cv_quality_score(analysis):
    """Calcule un score de qualité pour le CV"""
    score = 0

    # Missions (30 points)
    missions = analysis.get("missions", [])
    if len(missions) >= 5:
        score += 30
    elif len(missions) >= 3:
        score += 20
    elif len(missions) >= 1:
        score += 10

    # Compétences (30 points)
    competences = analysis.get("competences", [])
    if len(competences) >= 10:
        score += 30
    elif len(competences) >= 5:
        score += 20
    elif len(competences) >= 1:
        score += 10

    # Contact (20 points)
    contact = analysis.get("contact", {})
    contact_fields = ["email", "phone", "linkedin"]
    filled_fields = sum([1 for field in contact_fields if contact.get(field)])
    if filled_fields == 3:
        score += 20
    elif filled_fields >= 1:
        score += 10

    # Résumé (20 points)
    if analysis.get("resume"):
        score += 20

    return min(score, 100)
