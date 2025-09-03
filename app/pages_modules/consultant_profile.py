"""
Module de gestion du profil consultant
Fonctions principales pour l'affichage et la navigation du profil
"""

import os
import sys
from datetime import datetime

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
    from app.database.database import get_database_session
    from app.database.models import Mission, Competence, ConsultantCompetence, Consultant, ConsultantSalaire, Langue, ConsultantLangue, BusinessManager
    from app.services.consultant_service import ConsultantService
    from app.services.simple_analyzer import SimpleDocumentAnalyzer as DocumentAnalyzer
    from app.services.document_service import DocumentService
    from sqlalchemy.orm import joinedload

    imports_ok = True
except ImportError as e:
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
    tab1, tab2 = st.tabs(
        ["📋 Liste des consultants", "➕ Ajouter un consultant"]
    )

    with tab1:
        # Utiliser la fonction du fichier consultants.py principal
        from .consultants import show_consultants_list_tab
        show_consultants_list_tab()

    with tab2:
        # Utiliser la fonction du fichier consultants.py principal
        from .consultants import show_add_consultant_form_tab
        show_add_consultant_form_tab()


def show_consultant_profile():
    """Affiche le profil détaillé d'un consultant avec gestion d'erreurs améliorée"""

    consultant_id = st.session_state.view_consultant_profile

<<<<<<< HEAD
    # Debug: Afficher l'ID récupéré
    st.info(f"🔍 Debug: ID du consultant récupéré = {consultant_id} (type: {type(consultant_id)})")

=======
>>>>>>> 61f896e ( Clean: Suppression des messages de debug)
    try:
        # Charger le consultant avec toutes les relations nécessaires dans la même session
        with get_database_session() as session:
            consultant = session.query(Consultant)\
                .options(joinedload(Consultant.practice))\
                .filter(Consultant.id == consultant_id)\
                .first()

            if not consultant:
                st.error(f"❌ Consultant introuvable (ID: {consultant_id})")
                st.warning("💡 Vérifiez que l'ID est correct et que le consultant existe dans la base de données")

                # Debug: Lister tous les consultants pour voir lesquels existent
                all_consultants = session.query(Consultant).all()
                st.write("**🔍 Consultants existants dans la DB:**")
                for c in all_consultants[:10]:  # Afficher les 10 premiers
                    st.write(f"- ID: {c.id}, Nom: {c.prenom} {c.nom}")
                if len(all_consultants) > 10:
                    st.write(f"... et {len(all_consultants) - 10} autres")

                if st.button("← Retour à la liste", key="back_to_list_error"):
                    del st.session_state.view_consultant_profile
                    st.rerun()
                return

            # Charger toutes les données nécessaires dans la session
            practice_name = consultant.practice.nom if consultant.practice else "Non affecté"

            # Créer un dictionnaire avec toutes les données nécessaires
            consultant_data = {
                'id': consultant.id,
                'prenom': consultant.prenom,
                'nom': consultant.nom,
                'email': consultant.email,
                'telephone': consultant.telephone,
                'salaire_actuel': consultant.salaire_actuel,
                'disponibilite': consultant.disponibilite,
                'notes': consultant.notes,
                'date_creation': consultant.date_creation,
                'practice_name': practice_name
            }

        # En-tête avec bouton retour
        col1, col2 = st.columns([6, 1])

        with col1:
            st.title(f"👤 Profil de {consultant_data['prenom']} {consultant_data['nom']}")

        with col2:
            if st.button("← Retour", key="back_to_list"):
                del st.session_state.view_consultant_profile
                st.rerun()

        st.markdown("---")

        # Métriques principales
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            salaire = consultant_data['salaire_actuel'] or 0
            st.metric("💰 Salaire annuel", f"{salaire:,}€")

        with col2:
            # Calcul du CJM (Coût Journalier Moyen)
            cjm = (salaire * 1.8 / 216) if salaire else 0
            st.metric("📈 CJM", f"{cjm:,.0f}€")

        with col3:
            status = (
                "✅ Disponible" if consultant_data['disponibilite'] else "🔴 En mission"
            )
            st.metric("📊 Statut", status)

        with col4:
            creation_date = (
                consultant_data['date_creation'].strftime("%d/%m/%Y")
                if consultant_data['date_creation']
                else "N/A"
            )
            st.metric("📅 Membre depuis", creation_date)

        with col5:
            st.metric("🏢 Practice", consultant_data['practice_name'])

        st.markdown("---")

        # Affichage de l'analyse CV en PLEINE LARGEUR (si disponible)
        if 'cv_analysis' in st.session_state:
            show_cv_analysis_fullwidth()
            st.markdown("---")

        # Pour les onglets, on va récupérer l'objet consultant avec une nouvelle session
        with get_database_session() as session:
            consultant_obj = session.query(Consultant).filter(Consultant.id == consultant_id).first()

            # Onglets de détail
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                ["📋 Informations", "💼 Compétences", "🌍 Langues", "🚀 Missions", "📁 Documents"]
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

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du profil consultant: {e}")
        st.code(str(e))

        # Bouton manuel pour retourner à la liste
        if st.button("← Retour à la liste", key="back_to_list_exception"):
            del st.session_state.view_consultant_profile
            st.rerun()


def show_cv_analysis_fullwidth():
    """Affiche l'analyse CV en pleine largeur au-dessus des onglets"""

    if 'cv_analysis' not in st.session_state:
        return

    cv_data = st.session_state.cv_analysis
    analysis = cv_data['analysis']
    consultant = cv_data['consultant']
    file_name = cv_data['file_name']

    # CSS pour forcer la pleine largeur
    st.markdown("""
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
    """, unsafe_allow_html=True)

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
            from .consultants import show_cv_missions_tab
            show_cv_missions_tab(analysis.get("missions", []), consultant)

        with tab2:
            from .consultants import show_cv_skills_tab
            show_cv_skills_tab(analysis)

        with tab3:
            from .consultants import show_cv_summary_tab
            show_cv_summary_tab(analysis, consultant)

        with tab4:
            from .consultants import show_cv_actions_tab
            show_cv_actions_tab(analysis, consultant)

        st.markdown('</div>', unsafe_allow_html=True)
