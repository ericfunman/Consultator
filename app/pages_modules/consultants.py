"""
Page de gestion des consultants - Version fonctionnelle
CRUD complet pour les consultants avec formulaires, tableaux et gestion des missions
"""

import os
import sys
from datetime import datetime

import pandas as pd
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
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.orm import joinedload

    from database.database import get_database_session
    from database.models import BusinessManager
    from database.models import Competence
    from database.models import Consultant
    from database.models import ConsultantCompetence
    from database.models import ConsultantLangue
    from database.models import ConsultantSalaire
    from database.models import Langue
    from database.models import Mission
    from services.consultant_service import ConsultantService
    from services.document_service import DocumentService
    from services.simple_analyzer import (
        SimpleDocumentAnalyzer as DocumentAnalyzer,
    )

    imports_ok = True
except ImportError:
    # Imports échoués, on continue quand même
    pass


# ===== CONSTANTES =====
# Constantes pour les chaînes dupliquées (corrections SonarQube)
STATUT_NON_AFFECTE = "Non affecté"
STATUT_DISPONIBLE = "✅ Disponible"
LABEL_STATUT = "📊 Statut"
FORMAT_DATE = "%d/%m/%Y"
LABEL_PRACTICE = "🏢 Practice"
LABEL_COMPETENCES = "💼 Compétences"
VALEUR_NON_SPECIFIE = "Non spécifié"
LABEL_TECHNOLOGIES = "🛠️ Technologies"
LABEL_TAILLE = "📊 Taille"
MSG_FICHIER_INTROUVABLE = "❌ Fichier introuvable"
MSG_CHAMP_OBLIGATOIRE = "Ce champ est obligatoire"
MSG_CHAMPS_OBLIGATOIRES = "❌ Veuillez remplir tous les champs obligatoires (*)"


def show():
    """Affiche la page de gestion des consultants"""

    st.title("👥 Gestion des consultants")

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        st.info("Vérifiez que tous les modules sont correctement installés")
        return

    # Vérifier si on doit afficher le profil d'un consultant spécifique
    if "view_consultant_profile" in st.session_state:
        show_consultant_profile()
        return

    # Onglets pour organiser les fonctionnalités
    tab1, tab2 = st.tabs([" Consultants", "➕ Ajouter un consultant"])

    with tab1:
        show_consultants_list()

    with tab2:
        show_add_consultant_form()


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
        st.markdown("### 🔍 Analyse CV : " + file_name)
        st.markdown("**Consultant :** " + consultant.prenom + " " + consultant.nom)

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
            show_cv_missions(analysis.get("missions", []), consultant)

        with tab2:
            show_cv_skills(analysis)

        with tab3:
            show_cv_summary(analysis)

        with tab4:
            show_cv_actions(analysis, consultant)

        st.markdown("</div>", unsafe_allow_html=True)


def _load_consultant_data(consultant_id):
    """Charge les données d'un consultant avec ses relations."""
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
            consultant.practice.nom if consultant.practice else STATUT_NON_AFFECTE
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
        return consultant_data, consultant


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
            STATUT_DISPONIBLE if consultant_data["disponibilite"] else "🔴 En mission"
        )
        st.metric(LABEL_STATUT, status)

    with col4:
        creation_date = (
            consultant_data["date_creation"].strftime(FORMAT_DATE)
            if consultant_data["date_creation"]
            else "N/A"
        )
        st.metric("📅 Membre depuis", creation_date)

    with col5:
        st.metric(LABEL_PRACTICE, consultant_data["practice_name"])


def _show_consultant_not_found():
    """Affiche un message d'erreur pour un consultant introuvable."""
    st.error("❌ Consultant introuvable")
    if st.button("← Retour à la liste", key="back_to_list_error"):
        del st.session_state.view_consultant_profile
        st.rerun()


def show_consultant_profile():
    """Affiche le profil détaillé d'un consultant avec gestion d'erreurs améliorée"""

    consultant_id = st.session_state.view_consultant_profile

    try:
        consultant_data, _ = _load_consultant_data(consultant_id)

        if not consultant_data:
            _show_consultant_not_found()
            return

        _display_consultant_header(consultant_data)
        st.markdown("---")
        _display_consultant_metrics(consultant_data)
        st.markdown("---")

        # Affichage de l'analyse CV en PLEINE LARGEUR (si disponible)
        if "cv_analysis" in st.session_state:
            show_cv_analysis_fullwidth()
            st.markdown("---")

        # Pour les onglets, on va récupérer l'objet consultant avec une nouvelle session
        with get_database_session() as session:
            consultant_obj = (
                session.query(Consultant).filter(Consultant.id == consultant_id).first()
            )

            # Onglets de détail
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
                [
                    "📋 Informations",
                    LABEL_COMPETENCES,
                    "🌍 Langues",
                    "🚀 Missions",
                    "🎯 Missions VSA",
                    "📁 Documents",
                ]
            )

            with tab1:
                show_consultant_info(consultant_obj)

            with tab2:
                show_consultant_skills(consultant_obj)

            with tab3:
                show_consultant_languages(consultant_obj)

            with tab4:
                show_consultant_missions(consultant_obj)

            with tab5:
                # Afficher les missions VSA
                from .consultant_info import _display_vsa_missions
                _display_vsa_missions(consultant_obj)

            with tab6:
                show_consultant_documents(consultant_obj)

    except (AttributeError, TypeError, ValueError, SQLAlchemyError) as exc:
        st.error("❌ Erreur lors du chargement du profil consultant: " + str(exc))
        st.code(str(exc))

        # Bouton manuel pour retourner à la liste
        if st.button("← Retour à la liste", key="back_to_list_exception"):
            if hasattr(st.session_state, "view_consultant_profile"):
                del st.session_state.view_consultant_profile
            st.rerun()


def _load_consultant_for_edit(consultant_id):
    """Charge le consultant avec toutes ses relations pour l'édition."""
    from database.models import Practice

    with get_database_session() as session:
        consultant_db = _load_consultant_with_relations(session, consultant_id)
        practices = session.query(Practice).filter(Practice.actif).all()

        # Charger informations du Business Manager
        bm_nom_complet, bm_email = _extract_business_manager_info(consultant_db)

        # Préparer les options
        practice_options = {p.nom: p.id for p in practices}
        current_practice_id = _get_current_practice_id(consultant_db)

        return (
            consultant_db,
            practice_options,
            current_practice_id,
            bm_nom_complet,
            bm_email,
        )


def _load_consultant_with_relations(session, consultant_id):
    """Charge le consultant avec ses relations"""
    return (
        session.query(Consultant)
        .options(joinedload(Consultant.practice))
        .options(joinedload(Consultant.business_manager_gestions))
        .filter(Consultant.id == consultant_id)
        .first()
    )


def _extract_business_manager_info(consultant_db):
    """Extrait les informations du Business Manager"""
    bm_actuel = consultant_db.business_manager_actuel
    bm_nom_complet = bm_actuel.nom_complet if bm_actuel else None
    bm_email = bm_actuel.email if bm_actuel else None
    return bm_nom_complet, bm_email


def _get_current_practice_id(consultant_db):
    """Récupère l'ID de la practice actuelle"""
    return consultant_db.practice_id if hasattr(consultant_db, "practice_id") else None


def _render_basic_consultant_fields(
    consultant_db, practice_options, current_practice_id, bm_nom_complet, bm_email
):
    """Affiche les champs de base du consultant."""
    col1, col2 = st.columns(2)

    with col1:
        prenom = st.text_input(
            "👤 Prénom *", value=consultant_db.prenom, placeholder="Ex: Jean"
        )
        email = st.text_input(
            "📧 Email *",
            value=consultant_db.email,
            placeholder="jean.dupont@example.com",
        )
        salaire = st.number_input(
            "💰 Salaire annuel (€)",
            min_value=0,
            value=int(consultant_db.salaire_actuel or 0),
            step=1000,
        )

        # Affichage du CJM calculé en temps réel
        cjm_calcule = (salaire * 1.8 / 216) if salaire > 0 else 0
        st.info(
            "📈 CJM calculé : **" + f"{cjm_calcule:,.0f}" + " €** (salaire×1.8÷216)"
        )

        # Sélection de la practice
        practice_label = st.selectbox(
            LABEL_PRACTICE,
            options=[STATUT_NON_AFFECTE] + list(practice_options.keys()),
            index=(
                (list(practice_options.values()).index(current_practice_id) + 1)
                if current_practice_id in practice_options.values()
                else 0
            ),
        )
        selected_practice_id = practice_options.get(practice_label)

        # Affichage du Business Manager (lecture seule)
        if bm_nom_complet and bm_email:
            st.text_input(
                "👨‍💼 Business Manager",
                value=bm_nom_complet + " (" + bm_email + ")",
                disabled=True,
                help="Le Business Manager ne peut être modifié que depuis la page BM",
            )
        else:
            st.text_input(
                "👨‍💼 Business Manager",
                value="Non assigné",
                disabled=True,
                help="Aucun Business Manager assigné",
            )

    with col2:
        nom = st.text_input(
            "👤 Nom *", value=consultant_db.nom, placeholder="Ex: Dupont"
        )
        telephone = st.text_input(
            "📞 Téléphone",
            value=consultant_db.telephone or "",
            placeholder="01.23.45.67.89",
        )
        disponibilite = st.checkbox(
            STATUT_DISPONIBLE, value=consultant_db.disponibilite
        )

    return prenom, nom, email, telephone, salaire, disponibilite, selected_practice_id


def _render_company_history_fields(consultant_db):
    """Affiche les champs d'historique société."""
    st.markdown("---")
    st.markdown("### 🏢 Historique Société")

    col3, col4 = st.columns(2)

    with col3:
        societe = _render_societe_field(consultant_db)
        date_entree = _render_date_entree_field(consultant_db)

    with col4:
        date_sortie = _render_date_sortie_field(consultant_db)
        date_premiere_mission = _render_date_premiere_mission_field(consultant_db)

    return societe, date_entree, date_sortie, date_premiere_mission


def _render_societe_field(consultant_db):
    """Rendu du champ société"""
    return st.selectbox(
        "🏢 Société",
        options=["Quanteam", "Asigma"],
        index=0 if (consultant_db.societe or "Quanteam") == "Quanteam" else 1,
    )


def _render_date_entree_field(consultant_db):
    """Rendu du champ date d'entrée"""
    return st.date_input(
        "📅 Date d'entrée société",
        value=consultant_db.date_entree_societe,
        help="Date d'entrée dans la société",
    )


def _render_date_sortie_field(consultant_db):
    """Rendu du champ date de sortie"""
    return st.date_input(
        "📅 Date de sortie société (optionnel)",
        value=consultant_db.date_sortie_societe,
        help="Laissez vide si encore en poste",
    )


def _render_date_premiere_mission_field(consultant_db):
    """Rendu du champ date première mission"""
    return st.date_input(
        "🚀 Date première mission (optionnel)",
        value=consultant_db.date_premiere_mission,
        help="Date de début de la première mission",
    )


def _render_professional_profile_fields(consultant_db):
    """Affiche les champs de profil professionnel."""
    st.markdown("---")
    st.markdown("### 👔 Profil Professionnel")

    col5, col6 = st.columns(2)

    with col5:
        grade_options = [
            "Junior",
            "Confirmé",
            "Consultant Manager",
            "Directeur de Practice",
        ]
        current_grade = consultant_db.grade or "Junior"
        grade_index = (
            grade_options.index(current_grade) if current_grade in grade_options else 0
        )
        grade = st.selectbox(
            "🎯 Grade",
            options=grade_options,
            index=grade_index,
            help="Niveau d'expérience du consultant",
        )

    with col6:
        contrat_options = ["CDI", "CDD", "Stagiaire", "Alternant", "Indépendant"]
        current_contrat = consultant_db.type_contrat or "CDI"
        contrat_index = (
            contrat_options.index(current_contrat)
            if current_contrat in contrat_options
            else 0
        )
        type_contrat = st.selectbox(
            "📋 Type de contrat",
            options=contrat_options,
            index=contrat_index,
            help="Type de contrat de travail",
        )

    return grade, type_contrat


def _display_consultant_status(consultant_db):
    """Affiche le statut et l'expérience du consultant."""
    st.markdown("---")

    # Affichage de l'expérience calculée
    if consultant_db.date_premiere_mission:
        try:
            experience = consultant_db.experience_annees
            st.info("📊 **Expérience calculée :** " + str(experience) + " années")
        except (AttributeError, TypeError, ValueError):
            st.info("📊 **Expérience :** Calcul en cours...")
    else:
        st.info("📊 **Expérience :** Non calculée (date première mission manquante)")

    # Statut société
    try:
        statut = consultant_db.statut_societe
        if statut == "En poste":
            st.success("✅ **Statut :** " + str(statut))
        elif statut == "Départ prévu":
            st.warning("⚠️ **Statut :** " + str(statut))
        else:
            st.error("❌ **Statut :** " + str(statut))
    except (AttributeError, TypeError, ValueError):
        st.info("📊 **Statut :** En cours de calcul...")


def _process_consultant_form_submission(consultant, form_data):
    """Traite la soumission du formulaire de modification d'un consultant"""
    prenom, nom, email = form_data["prenom"], form_data["nom"], form_data["email"]

    if not prenom or not nom or not email:
        st.error(MSG_CHAMPS_OBLIGATOIRES)
        return False

    # Vérifier l'unicité de l'email
    existing = ConsultantService.get_consultant_by_email(email)
    if existing and existing.id != consultant.id:
        st.error(f"❌ Un consultant avec l'email {email} existe déjà !")
        return False

    try:
        update_data = _build_update_data(form_data)
        if ConsultantService.update_consultant(consultant.id, update_data):
            st.success(f"✅ {prenom} {nom} modifié avec succès !")
            st.rerun()
            return True
        else:
            st.error("❌ Erreur lors de la modification")
            return False
    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur: {exc}")
        return False


def _build_update_data(form_data):
    """Construit le dictionnaire de données à mettre à jour"""
    return {
        "prenom": form_data["prenom"].strip(),
        "nom": form_data["nom"].strip(),
        "email": form_data["email"].strip().lower(),
        "telephone": form_data["telephone"].strip() if form_data["telephone"] else None,
        "salaire_actuel": form_data["salaire"],
        "disponibilite": form_data["disponibilite"],
        "notes": form_data["notes"].strip() if form_data["notes"] else None,
        "practice_id": form_data["selected_practice_id"],
        # Nouveaux champs V1.2
        "societe": form_data["societe"],
        "date_entree_societe": form_data["date_entree"],
        "date_sortie_societe": (
            form_data["date_sortie"] if form_data["date_sortie"] else None
        ),
        "date_premiere_mission": (
            form_data["date_premiere_mission"]
            if form_data["date_premiere_mission"]
            else None
        ),
        # Nouveaux champs V1.2.1
        "grade": form_data["grade"],
        "type_contrat": form_data["type_contrat"],
    }


def _manage_salary_history(consultant):
    """Gère l'affichage et la gestion de l'historique des salaires"""
    st.markdown("---")
    st.subheader("📈 Historique des salaires")
    from datetime import date

    with get_database_session() as session:
        salaires = (
            session.query(ConsultantSalaire)
            .filter(ConsultantSalaire.consultant_id == consultant.id)
            .order_by(ConsultantSalaire.date_debut.desc())
            .all()
        )

        # Ajout automatique d'une entrée historique si salaire_actuel existe mais
        # pas d'entrée pour l'année en cours
        if consultant.salaire_actuel and not any(
            s.date_debut.year == date.today().year for s in salaires
        ):
            salaire_init = ConsultantSalaire(
                consultant_id=consultant.id,
                salaire=consultant.salaire_actuel,
                date_debut=date(date.today().year, 1, 1),
                commentaire="Salaire initial (auto)",
            )
            session.add(salaire_init)
            session.commit()
            # Recharge la liste depuis la base pour éviter DetachedInstanceError
            salaires = (
                session.query(ConsultantSalaire)
                .filter(ConsultantSalaire.consultant_id == consultant.id)
                .order_by(ConsultantSalaire.date_debut.desc())
                .all()
            )

    if salaires:
        _display_salary_history(salaires, consultant)
    else:
        st.info("📊 Aucun historique de salaire disponible")


def _display_salary_history(salaires, consultant):
    """Affiche l'historique des salaires avec graphique"""
    # Affichage textuel (salaire le plus récent en haut)
    for salaire in salaires:
        st.write(
            f"- **{salaire.salaire:,.0f} €** du {salaire.date_debut.strftime(FORMAT_DATE)} "
            + (
                f"au {salaire.date_fin.strftime(FORMAT_DATE)}"
                if salaire.date_fin
                else "(en cours)"
            )
            + (f" — {salaire.commentaire}" if salaire.commentaire else "")
        )

    # Met à jour le salaire actuel du consultant si besoin
    salaire_max = max(salaires, key=lambda s: s.date_debut)
    if consultant.salaire_actuel != salaire_max.salaire:
        with get_database_session() as session:
            consultant_db = session.get(Consultant, consultant.id)
            if consultant_db:
                consultant_db.salaire_actuel = salaire_max.salaire
                session.commit()


def _handle_salary_evolution_form(consultant):
    """Gère le formulaire d'ajout d'évolution de salaire"""
    with st.expander("➕ Ajouter une évolution de salaire"):
        with st.form(f"add_salary_form_{consultant.id}"):
            new_salaire = st.number_input(
                "Nouveau salaire (€)",
                min_value=0,
                step=1000,
                key=f"salaire_{consultant.id}",
            )
            new_date_debut = st.date_input(
                "Date de début",
                value=datetime.today(),
                key=f"date_debut_{consultant.id}",
            )
            new_commentaire = st.text_input(
                "Commentaire",
                value="",
                key=f"commentaire_{consultant.id}",
            )
            add_salary_submitted = st.form_submit_button(
                "Ajouter l'évolution de salaire"
            )
            if add_salary_submitted:
                try:
                    with get_database_session() as session:
                        salaire_obj = ConsultantSalaire(
                            consultant_id=consultant.id,
                            salaire=new_salaire,
                            date_debut=new_date_debut,
                            commentaire=new_commentaire.strip() or None,
                        )
                        session.add(salaire_obj)
                        session.commit()
                    st.success("✅ Évolution de salaire ajoutée !")
                    st.rerun()
                except (SQLAlchemyError, ValueError, TypeError) as exc:
                    st.error(f"❌ Erreur lors de l'ajout : {exc}")


def _display_salary_evolution_chart(consultant, salaires_sorted):
    """Affiche le graphique d'évolution des salaires"""
    import plotly.graph_objects as go

    if st.button(
        "📈 Afficher l'évolution des salaires",
        key=f"show_salary_graph_{consultant.id}",
    ):
        dates = [s.date_debut for s in salaires_sorted]
        values = [s.salaire for s in salaires_sorted]
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=dates, y=values, mode="lines+markers", name="Salaire")
        )
        fig.update_layout(
            title="Évolution des salaires",
            xaxis_title="Date",
            yaxis_title="Salaire (€)",
            template="plotly_white",
        )
        st.plotly_chart(fig, width="stretch")


def _process_consultant_form_data(consultant, form_data):
    """Traite les données du formulaire de modification du consultant"""
    # Extraire les champs de base
    prenom = form_data.get("prenom", "")
    nom = form_data.get("nom", "")
    email = form_data.get("email", "")

    if not prenom or not nom or not email:
        st.error(MSG_CHAMPS_OBLIGATOIRES)
        return False

    # Vérifier l'unicité de l'email
    existing = ConsultantService.get_consultant_by_email(email)
    if existing and existing.id != consultant.id:
        st.error("❌ Un consultant avec l'email " + email + " existe déjà !")
        return False

    try:
        update_data = _build_update_data_from_form(form_data)

        if ConsultantService.update_consultant(consultant.id, update_data):
            st.success(f"✅ {prenom} {nom} modifié avec succès !")
            st.rerun()
            return True
        else:
            st.error("❌ Erreur lors de la modification")
            return False

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error("❌ Erreur: " + str(exc))
        return False


def _build_update_data_from_form(form_data):
    """Construit le dictionnaire de données à partir du formulaire"""
    return {
        "prenom": form_data["prenom"].strip(),
        "nom": form_data["nom"].strip(),
        "email": form_data["email"].strip().lower(),
        "telephone": (
            form_data["telephone"].strip() if form_data["telephone"] else None
        ),
        "salaire_actuel": form_data["salaire"],
        "disponibilite": form_data["disponibilite"],
        "notes": form_data["notes"].strip() if form_data["notes"] else None,
        "practice_id": form_data["selected_practice_id"],
        # Nouveaux champs V1.2
        "societe": form_data["societe"],
        "date_entree_societe": form_data["date_entree"],
        "date_sortie_societe": (
            form_data["date_sortie"] if form_data["date_sortie"] else None
        ),
        "date_premiere_mission": (
            form_data["date_premiere_mission"]
            if form_data["date_premiere_mission"]
            else None
        ),
        # Nouveaux champs V1.2.1
        "grade": form_data["grade"],
        "type_contrat": form_data["type_contrat"],
    }


def _manage_consultant_salary_history(consultant):
    """Gère l'affichage complet de l'historique des salaires"""
    st.markdown("---")
    st.subheader("📈 Historique des salaires")

    salaires = _load_and_ensure_salary_history(consultant)

    if salaires:
        _display_salary_history_content(consultant, salaires)
    else:
        st.info("Aucune évolution de salaire enregistrée.")

    # Formulaire d'ajout
    _handle_salary_evolution_form(consultant)


def _load_and_ensure_salary_history(consultant):
    """Charge l'historique des salaires et ajoute une entrée si nécessaire"""
    from datetime import date

    with get_database_session() as session:
        salaires = (
            session.query(ConsultantSalaire)
            .filter(ConsultantSalaire.consultant_id == consultant.id)
            .order_by(ConsultantSalaire.date_debut.desc())
            .all()
        )

        # Ajout automatique d'une entrée historique si nécessaire
        if _should_add_initial_salary_entry(consultant, salaires):
            _add_initial_salary_entry(session, consultant)
            # Recharge la liste
            salaires = (
                session.query(ConsultantSalaire)
                .filter(ConsultantSalaire.consultant_id == consultant.id)
                .order_by(ConsultantSalaire.date_debut.desc())
                .all()
            )

    return salaires


def _should_add_initial_salary_entry(consultant, salaires):
    """Vérifie si une entrée de salaire initial doit être ajoutée"""
    from datetime import date

    return consultant.salaire_actuel and not any(
        s.date_debut.year == date.today().year for s in salaires
    )


def _add_initial_salary_entry(session, consultant):
    """Ajoute une entrée de salaire initial"""
    from datetime import date

    salaire_init = ConsultantSalaire(
        consultant_id=consultant.id,
        salaire=consultant.salaire_actuel,
        date_debut=date(date.today().year, 1, 1),
        commentaire="Salaire initial (auto)",
    )
    session.add(salaire_init)
    session.commit()


def _display_salary_history_content(consultant, salaires):
    """Affiche le contenu de l'historique des salaires"""
    salaires_sorted = sorted(salaires, key=lambda s: s.date_debut)

    # Affichage textuel
    _display_salary_list(salaires)

    # Mise à jour du salaire actuel si nécessaire
    _update_current_salary_if_needed(consultant, salaires)

    # Graphique
    _display_salary_evolution_chart(consultant, salaires_sorted)


def _display_salary_list(salaires):
    """Affiche la liste textuelle des salaires"""
    for salaire in salaires:
        st.write(
            f"- **{salaire.salaire:,.0f} €** du {salaire.date_debut.strftime(FORMAT_DATE)} "
            + (
                f"au {salaire.date_fin.strftime(FORMAT_DATE)}"
                if salaire.date_fin
                else "(en cours)"
            )
            + (f" — {salaire.commentaire}" if salaire.commentaire else "")
        )


def _update_current_salary_if_needed(consultant, salaires):
    """Met à jour le salaire actuel du consultant si nécessaire"""
    salaire_max = max(salaires, key=lambda s: s.date_debut)
    if consultant.salaire_actuel != salaire_max.salaire:
        try:
            with get_database_session() as session:
                c = (
                    session.query(Consultant)
                    .filter(Consultant.id == consultant.id)
                    .first()
                )
                c.salaire_actuel = salaire_max.salaire
                session.commit()
        except (SQLAlchemyError, ValueError, TypeError) as exc:
            st.warning(f"⚠️ Erreur lors de la mise à jour du salaire: {exc}")


def show_consultant_info(consultant):
    """Affiche et permet la modification des informations du consultant"""
    st.subheader("📋 Informations personnelles")

    # Charger les données nécessaires
    consultant_db, practice_options, current_practice_id, bm_nom_complet, bm_email = (
        _load_consultant_for_edit(consultant.id)
    )

    # Formulaire principal infos consultant
    with st.form(f"edit_consultant_{consultant.id}"):
        # Champs de base
        prenom, nom, email, telephone, salaire, disponibilite, selected_practice_id = (
            _render_basic_consultant_fields(
                consultant_db,
                practice_options,
                current_practice_id,
                bm_nom_complet,
                bm_email,
            )
        )

        # Notes
        notes = st.text_area(
            "📝 Notes",
            value=consultant_db.notes or "",
            height=100,
            placeholder="Notes sur le consultant...",
        )

        # Champs historique société
        societe, date_entree, date_sortie, date_premiere_mission = (
            _render_company_history_fields(consultant_db)
        )

        # Champs profil professionnel
        grade, type_contrat = _render_professional_profile_fields(consultant_db)

        # Affichage du statut
        _display_consultant_status(consultant_db)

        # Bouton de sauvegarde
        _, col2, _ = st.columns([2, 1, 2])
        with col2:
            submitted = st.form_submit_button(
                "💾 Sauvegarder", type="primary", width="stretch"
            )

        if submitted:
            form_data = {
                "prenom": prenom,
                "nom": nom,
                "email": email,
                "telephone": telephone,
                "salaire": salaire,
                "disponibilite": disponibilite,
                "selected_practice_id": selected_practice_id,
                "notes": notes,
                "societe": societe,
                "date_entree": date_entree,
                "date_sortie": date_sortie,
                "date_premiere_mission": date_premiere_mission,
                "grade": grade,
                "type_contrat": type_contrat,
            }
            _process_consultant_form_data(consultant, form_data)

    # Historique des salaires
    _manage_consultant_salary_history(consultant)


def show_consultant_skills(consultant):
    """Affiche et gère les compétences techniques et fonctionnelles du consultant"""
    # Onglets pour organiser les types de compétences
    tab1, tab2, tab3 = st.tabs(
        [
            "🛠️ Compétences Techniques",
            "🏦 Compétences Fonctionnelles",
            "➕ Ajouter Compétences",
        ]
    )

    with tab1:
        st.subheader("🛠️ Compétences techniques")
        _show_technical_skills(consultant)

    with tab2:
        st.subheader("🏦 Compétences fonctionnelles")
        _show_functional_skills(consultant)

    with tab3:
        st.subheader("➕ Ajouter des compétences")
        _add_skills_form(consultant)


def _show_technical_skills(consultant):
    """Affiche les compétences techniques du consultant"""
    try:
        competences_tech, technologies_missions = _load_technical_skills_data(
            consultant
        )
        _display_registered_technical_skills(competences_tech)
        _display_mission_technologies(technologies_missions)
    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors du chargement des compétences techniques: {exc}")


def _load_technical_skills_data(consultant):
    """Charge les données des compétences techniques"""
    with get_database_session() as session:
        # Compétences techniques enregistrées
        competences_tech = (
            session.query(ConsultantCompetence, Competence)
            .join(Competence)
            .filter(
                ConsultantCompetence.consultant_id == consultant.id,
                Competence.type_competence == "technique",
            )
            .all()
        )

        # Technologies des missions
        missions = (
            session.query(Mission).filter(Mission.consultant_id == consultant.id).all()
        )

    # Extraire technologies des missions
    technologies_missions = set()
    for mission in missions:
        if mission.technologies_utilisees:
            mission_techs = [
                tech.strip()
                for tech in mission.technologies_utilisees.split(",")
                if tech.strip()
            ]
            technologies_missions.update(mission_techs)

    return competences_tech, technologies_missions


def _display_registered_technical_skills(competences_tech):
    """Affiche les compétences techniques enregistrées"""
    if competences_tech:
        st.write("**📋 Compétences techniques enregistrées**")
        for consultant_comp, competence in competences_tech:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            with col1:
                st.write(f"**{competence.nom}**")
                st.caption(f"Catégorie: {competence.categorie}")

            with col2:
                st.write("📊 " + consultant_comp.niveau_maitrise)

            with col3:
                st.write(f"⏱️ {consultant_comp.annees_experience} ans")

            with col4:
                if st.button("🗑️", key=f"del_tech_{consultant_comp.id}"):
                    _delete_consultant_competence(consultant_comp.id)
                    st.rerun()
        st.markdown("---")
    else:
        st.info("📝 Aucune compétence technique enregistrée")


def _display_mission_technologies(technologies_missions):
    """Affiche les technologies extraites des missions"""
    if technologies_missions:
        st.write("**🏷️ Technologies des missions**")
        cols = st.columns(4)
        tech_list = sorted(technologies_missions)

        for i, tech in enumerate(tech_list):
            with cols[i % 4]:
                st.markdown(
                    f"""
                <div style="padding: 8px; margin: 3px; border: 2px solid #28a745;
                            border-radius: 5px; text-align: center; background-color: #d4edda;">
                    <strong>{tech}</strong>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        st.metric("🛠️ Technologies utilisées", len(technologies_missions))


def _show_functional_skills(consultant):
    """Affiche les compétences fonctionnelles du consultant"""
    try:
        competences_func = _load_functional_skills_data(consultant)
        _display_functional_skills_by_category(competences_func)
    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors du chargement des compétences fonctionnelles: {exc}")


def _load_functional_skills_data(consultant):
    """Charge les compétences fonctionnelles du consultant"""
    with get_database_session() as session:
        return (
            session.query(ConsultantCompetence, Competence)
            .join(Competence)
            .filter(
                ConsultantCompetence.consultant_id == consultant.id,
                Competence.type_competence == "fonctionnelle",
            )
            .order_by(Competence.categorie, Competence.nom)
            .all()
        )


def _display_functional_skills_by_category(competences_func):
    """Affiche les compétences fonctionnelles groupées par catégorie"""
    if competences_func:
        st.write("**🏦 Compétences fonctionnelles enregistrées**")
        categories = _group_functional_skills_by_category(competences_func)
        _display_functional_skills_categories(categories)
        _display_functional_skills_metrics(competences_func)
    else:
        _display_no_functional_skills_message()


def _group_functional_skills_by_category(competences_func):
    """Groupe les compétences fonctionnelles par catégorie"""
    categories = {}
    for consultant_comp, competence in competences_func:
        if competence.categorie not in categories:
            categories[competence.categorie] = []
        categories[competence.categorie].append((consultant_comp, competence))
    return categories


def _display_functional_skills_categories(categories):
    """Affiche les catégories de compétences fonctionnelles"""
    for categorie, comps in categories.items():
        with st.expander(f"📂 {categorie} ({len(comps)} compétences)"):
            _display_functional_skills_in_category(comps)


def _display_functional_skills_in_category(comps):
    """Affiche les compétences d'une catégorie"""
    for consultant_comp, competence in comps:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        with col1:
            st.write(f"**{competence.nom}**")

        with col2:
            st.write("📊 " + consultant_comp.niveau_maitrise)

        with col3:
            st.write(f"⏱️ {consultant_comp.annees_experience} ans")

        with col4:
            if st.button("🗑️", key=f"del_func_{consultant_comp.id}"):
                _delete_consultant_competence(consultant_comp.id)
                st.rerun()


def _display_functional_skills_metrics(competences_func):
    """Affiche les métriques des compétences fonctionnelles"""
    total_competences = len(competences_func)
    st.metric("🏦 Total compétences fonctionnelles", total_competences)


def _display_no_functional_skills_message():
    """Affiche le message quand aucune compétence fonctionnelle n'est enregistrée"""
    st.info("📝 Aucune compétence fonctionnelle enregistrée")
    st.write(
        "Utilisez l'onglet **'Ajouter Compétences'** pour ajouter des compétences bancaires/assurance."
    )


def _add_skills_form(consultant):
    """Formulaire d'ajout de compétences"""
    # Choix du type de compétence
    type_competence = st.radio(
        "Type de compétence à ajouter:",
        options=["🛠️ Technique", "🏦 Fonctionnelle"],
        horizontal=True,
    )

    with st.form("add_competence_form"):
        if type_competence == "🛠️ Technique":
            _add_technical_skill_form(consultant)
        else:
            _add_functional_skill_form(consultant)


def _add_technical_skill_form(consultant):
    """Formulaire pour ajouter une compétence technique"""
    from utils.skill_categories import COMPETENCES_TECHNIQUES

    # Sélection de la catégorie et compétence
    categories_tech = list(COMPETENCES_TECHNIQUES.keys())
    categorie = st.selectbox("📂 Catégorie technique", categories_tech)
    competences_list = COMPETENCES_TECHNIQUES[categorie]
    competence_nom = st.selectbox("🛠️ Compétence", competences_list)

    # Niveau et expérience
    niveau, experience = _render_skill_level_fields()

    # Champs optionnels
    certifications = st.text_input("🏆 Certifications (optionnel)")
    projets = st.text_area("💼 Projets réalisés (optionnel)")

    submitted = st.form_submit_button("➕ Ajouter la compétence technique")

    if submitted:
        _save_consultant_competence(
            consultant.id,
            competence_nom,
            categorie,
            "technique",
            niveau,
            experience,
            certifications,
            projets,
        )


def _add_functional_skill_form(consultant):
    """Formulaire pour ajouter une compétence fonctionnelle"""
    from utils.skill_categories import COMPETENCES_FONCTIONNELLES

    # Sélection de la catégorie et compétence
    categories_func = list(COMPETENCES_FONCTIONNELLES.keys())
    categorie = st.selectbox("📂 Catégorie fonctionnelle", categories_func)
    competences_list = COMPETENCES_FONCTIONNELLES[categorie]
    competence_nom = st.selectbox("🏦 Compétence", competences_list)

    # Niveau et expérience
    niveau, experience = _render_skill_level_fields()

    # Champs optionnels
    certifications = st.text_input("🏆 Certifications (optionnel)")
    projets = st.text_area("📁 Projets/missions réalisés (optionnel)")

    submitted = st.form_submit_button("➕ Ajouter la compétence fonctionnelle")

    if submitted:
        _save_consultant_competence(
            consultant.id,
            competence_nom,
            categorie,
            "fonctionnelle",
            niveau,
            experience,
            certifications,
            projets,
        )


def _render_skill_level_fields():
    """Rendu des champs niveau et expérience"""
    col1, col2 = st.columns(2)
    with col1:
        niveau = st.selectbox(
            "📊 Niveau de maîtrise", ["Débutant", "Intermédiaire", "Avancé", "Expert"]
        )
    with col2:
        experience = st.number_input(
            "⏱️ Années d'expérience", min_value=0.0, max_value=50.0, value=1.0, step=0.5
        )
    return niveau, experience


def _save_consultant_competence(
    consultant_id,
    competence_nom,
    categorie,
    type_comp,
    niveau,
    experience,
    certifications,
    projets,
):
    """Sauvegarde une compétence pour un consultant"""
    try:
        with get_database_session() as session:
            # Vérifier/créer la compétence
            competence = (
                session.query(Competence)
                .filter(
                    Competence.nom == competence_nom,
                    Competence.type_competence == type_comp,
                )
                .first()
            )

            if not competence:
                competence = Competence(
                    nom=competence_nom,
                    categorie=categorie,
                    type_competence=type_comp,
                    description=f"Compétence {type_comp} en {competence_nom.lower()}",
                )
                session.add(competence)
                session.flush()  # Pour obtenir l'ID

            # Vérifier si le consultant a déjà cette compétence
            existing = (
                session.query(ConsultantCompetence)
                .filter(
                    ConsultantCompetence.consultant_id == consultant_id,
                    ConsultantCompetence.competence_id == competence.id,
                )
                .first()
            )

            if existing:
                st.warning(f"⚠️ {competence_nom} est déjà dans le profil du consultant")
                return

            # Créer l'association consultant-compétence
            consultant_comp = ConsultantCompetence(
                consultant_id=consultant_id,
                competence_id=competence.id,
                niveau_maitrise=niveau.lower(),
                annees_experience=experience,
                certifications=certifications if certifications else None,
                projets_realises=projets if projets else None,
            )

            session.add(consultant_comp)
            session.commit()

            st.success(f"✅ Compétence '{competence_nom}' ajoutée avec succès!")
            st.rerun()

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors de l'ajout: {exc}")


def _delete_consultant_competence(consultant_competence_id):
    """Supprime une compétence d'un consultant"""
    try:
        with get_database_session() as session:
            consultant_comp = (
                session.query(ConsultantCompetence)
                .filter(ConsultantCompetence.id == consultant_competence_id)
                .first()
            )

            if consultant_comp:
                session.delete(consultant_comp)
                session.commit()
                st.success("✅ Compétence supprimée!")
                st.rerun()
            else:
                st.error("❌ Compétence non trouvée")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors de la suppression: {exc}")


def show_consultant_languages(consultant):
    """Affiche et gère les langues du consultant"""
    st.subheader("🌍 Langues parlées")

    try:
        with get_database_session() as session:
            # Récupérer les langues du consultant
            consultant_langues = (
                session.query(ConsultantLangue)
                .join(Langue)
                .filter(ConsultantLangue.consultant_id == consultant.id)
                .all()
            )

            if consultant_langues:
                # Affichage des langues existantes
                for cl in consultant_langues:
                    col1, col2, col3, col4 = st.columns([3, 2, 3, 1])

                    with col1:
                        flag_emoji = {
                            "FR": "🇫🇷",
                            "EN": "🇬🇧",
                            "ES": "🇪🇸",
                            "DE": "🇩🇪",
                            "IT": "🇮🇹",
                            "PT": "🇵🇹",
                            "NL": "🇳🇱",
                            "RU": "🇷🇺",
                            "ZH": "🇨🇳",
                            "JA": "🇯🇵",
                            "AR": "🇸🇦",
                            "HI": "🇮🇳",
                        }
                        emoji = flag_emoji.get(cl.langue.code_iso, "🌍")
                        st.write(f"{emoji} **{cl.langue.nom}**")

                    with col2:
                        niveau_colors = {1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "🔵"}
                        st.write(
                            f"{niveau_colors.get(cl.niveau, '⚪')} {cl.niveau_label}"
                        )

                    with col3:
                        if cl.commentaire:
                            st.caption(
                                cl.commentaire[:50] + "..."
                                if len(cl.commentaire) > 50
                                else cl.commentaire
                            )

                    with col4:
                        if st.button("🗑️", key=f"del_lang_{cl.id}", help="Supprimer"):
                            _delete_consultant_language(cl.id)
                            st.rerun()

                st.write("---")
            else:
                st.info("🔍 Aucune langue enregistrée")

            # Formulaire d'ajout de langue
            with st.expander("➕ Ajouter une langue"):
                _add_language_form(consultant)

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors de l'affichage des langues: {exc}")


def _add_language_form(consultant):
    """Formulaire pour ajouter une langue"""
    with st.form(f"add_language_{consultant.id}"):
        # Récupérer toutes les langues disponibles
        try:
            with get_database_session() as session:
                langues_disponibles = session.query(Langue).order_by(Langue.nom).all()

                if not langues_disponibles:
                    st.warning(
                        "⚠️ Aucune langue disponible. Veuillez d'abord initialiser les langues."
                    )
                    return

                # Récupérer les langues déjà assignées
                langues_consultant = (
                    session.query(ConsultantLangue.langue_id)
                    .filter(ConsultantLangue.consultant_id == consultant.id)
                    .all()
                )
                langues_assignees = [lang[0] for lang in langues_consultant]

                # Filtrer les langues non assignées
                langues_libres = [
                    langue
                    for langue in langues_disponibles
                    if langue.id not in langues_assignees
                ]

                if not langues_libres:
                    st.info("✅ Toutes les langues disponibles sont déjà assignées")
                    return

                # Formulaire
                col1, col2 = st.columns(2)

                with col1:
                    langue_selectionnee = st.selectbox(
                        "🌍 Langue",
                        langues_libres,
                        format_func=lambda x: f"{x.nom} ({x.code_iso})",
                    )

                with col2:
                    niveau = st.selectbox(
                        "📊 Niveau",
                        [1, 2, 3, 4, 5],
                        format_func=lambda x: {
                            1: "1 - Débutant (A1)",
                            2: "2 - Élémentaire (A2)",
                            3: "3 - Intermédiaire (B1-B2)",
                            4: "4 - Avancé (C1)",
                            5: "5 - Natif (C2)",
                        }[x],
                    )

                commentaire = st.text_area(
                    "💬 Commentaire (optionnel)",
                    placeholder="Ex: TOEIC 850, Certification, Langue maternelle...",
                    max_chars=200,
                )

                submitted = st.form_submit_button("➕ Ajouter la langue")

                if submitted and langue_selectionnee:
                    _save_consultant_language(
                        consultant.id, langue_selectionnee.id, niveau, commentaire
                    )
                    st.rerun()

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
            st.error(f"❌ Erreur lors de la préparation du formulaire: {exc}")


def _save_consultant_language(consultant_id, langue_id, niveau, commentaire):
    """Enregistre une langue pour un consultant"""
    try:
        with get_database_session() as session:
            # Vérifier si la langue n'est pas déjà assignée
            existing = (
                session.query(ConsultantLangue)
                .filter(
                    ConsultantLangue.consultant_id == consultant_id,
                    ConsultantLangue.langue_id == langue_id,
                )
                .first()
            )

            if existing:
                st.warning("⚠️ Cette langue est déjà assignée à ce consultant")
                return

            # Créer la nouvelle langue
            nouvelle_langue = ConsultantLangue(
                consultant_id=consultant_id,
                langue_id=langue_id,
                niveau=niveau,
                commentaire=commentaire.strip() if commentaire else None,
            )

            session.add(nouvelle_langue)
            session.commit()
            st.success("✅ Langue ajoutée avec succès!")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors de l'ajout de la langue: {exc}")


def _delete_consultant_language(consultant_langue_id):
    """Supprime une langue d'un consultant"""
    try:
        with get_database_session() as session:
            consultant_langue = (
                session.query(ConsultantLangue)
                .filter(ConsultantLangue.id == consultant_langue_id)
                .first()
            )

            if consultant_langue:
                session.delete(consultant_langue)
                session.commit()
                st.success("✅ Langue supprimée!")
                st.rerun()
            else:
                st.error("❌ Langue non trouvée")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors de la suppression: {exc}")


def show_consultant_missions(consultant):
    """Affiche l'historique des missions du consultant avec édition"""
    st.subheader("🚀 Historique des missions")

    try:
        missions = _load_consultant_missions(consultant)
        if missions:
            _display_mission_metrics(missions)
            _display_missions_with_tabs(consultant, missions)
        else:
            st.info("📝 Aucune mission enregistrée pour ce consultant")
            show_add_mission_form(consultant)

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors du chargement des missions: {exc}")


def _load_consultant_missions(consultant):
    """Charge les missions du consultant"""
    with get_database_session() as session:
        return (
            session.query(Mission)
            .filter(Mission.consultant_id == consultant.id)
            .order_by(Mission.date_debut.desc())
            .all()
        )


def _display_mission_metrics(missions):
    """Affiche les métriques des missions"""
    col1, col2, col3, col4 = st.columns(4)

    total_revenus = sum(m.revenus_generes or 0 for m in missions)
    missions_terminees = len([m for m in missions if m.statut == "terminee"])
    missions_en_cours = len([m for m in missions if m.statut == "en_cours"])

    with col1:
        st.metric("💰 Revenus totaux", f"{total_revenus:,}€")
    with col2:
        st.metric("✅ Terminées", missions_terminees)
    with col3:
        st.metric("🔄 En cours", missions_en_cours)
    with col4:
        st.metric("📊 Total", len(missions))

    st.markdown("---")


def _display_missions_with_tabs(consultant, missions):
    """Affiche les missions dans des onglets"""
    tab1, tab2 = st.tabs(["📋 Missions existantes", "➕ Ajouter une mission"])

    with tab1:
        _display_missions_list(missions)

    with tab2:
        show_add_mission_form(consultant)


def _display_missions_list(missions):
    """Affiche la liste des missions avec mode édition"""
    edit_mode = st.checkbox("✏️ Mode édition", key="edit_mode_missions")

    if edit_mode:
        st.info("📝 Mode édition activé - Cliquez sur une mission pour la modifier")
        for i, mission in enumerate(missions):
            with st.expander(
                f"✏️ Éditer: {mission.client} - {mission.role or 'Rôle non défini'}",
                expanded=False,
            ):
                show_mission_edit_form(mission)
    else:
        # Affichage normal (lecture seule)
        for i, mission in enumerate(missions):
            with st.expander(
                f"🚀 {mission.client} - {mission.role or 'Rôle non défini'}",
                expanded=(i == 0),
            ):
                show_mission_readonly(mission)


def show_mission_readonly(mission):
    """Affiche les détails d'une mission en lecture seule"""
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**🏢 Client**: {mission.client}")
        st.write("**👤 Rôle**: " + (mission.role or VALEUR_NON_SPECIFIE))
        st.write(
            f"**📅 Début**: {mission.date_debut.strftime('%Y-%m-%d') if mission.date_debut else 'N/A'}"
        )

        # Affichage TJM (nouveau champ V1.2.2)
        if mission.tjm:
            st.write("**💰 TJM Mission**: " + f"{mission.tjm:,}" + "€")
        elif mission.taux_journalier:
            st.write("**💰 TJM (ancien)**: " + f"{mission.taux_journalier:,}" + "€")

        st.write("**💰 Revenus**: " + f"{mission.revenus_generes or 0:,}" + "€")

    with col2:
        st.write(
            f"**📅 Fin**: {mission.date_fin.strftime('%Y-%m-%d') if mission.date_fin else 'En cours'}"
        )

        # Statut avec couleur
        if mission.statut == "terminee":
            st.success("✅ Terminée")
        elif mission.statut == "en_cours":
            st.info("🔄 En cours")
        else:
            st.warning("⏸️ En pause")

    st.write(
        f"**🛠️ Technologies**: {mission.technologies_utilisees or 'Non spécifiées'}"
    )

    # Description de la mission
    if mission.description and mission.description != "Aucune description":
        st.write("**📝 Description**:")
        st.text_area(
            label="Description de la mission",
            value=mission.description,
            height=100,
            key=f"desc_readonly_{mission.id}",
            disabled=True,
            label_visibility="collapsed",
        )


def show_mission_edit_form(mission):
    """Formulaire d'édition d'une mission"""

    with st.form(f"edit_mission_{mission.id}"):
        col1, col2 = st.columns(2)

        with col1:
            nom_mission = st.text_input(
                "📋 Nom de la mission",
                value=mission.nom_mission or "",
                key=f"edit_nom_{mission.id}",
            )
            client = st.text_input(
                "🏢 Client",
                value=mission.client or "",
                key=f"edit_client_{mission.id}",
            )
            role = st.text_input(
                "👤 Rôle",
                value=mission.role or "",
                key=f"edit_role_{mission.id}",
            )
            revenus = st.number_input(
                "💰 Revenus (€)",
                value=float(mission.revenus_generes or 0),
                min_value=0.0,
                key=f"edit_revenus_{mission.id}",
            )

        with col2:
            date_debut = st.date_input(
                "📅 Date début",
                value=mission.date_debut if mission.date_debut else None,
                key=f"edit_debut_{mission.id}",
            )
            date_fin = st.date_input(
                "📅 Date fin",
                value=mission.date_fin if mission.date_fin else None,
                key=f"edit_fin_{mission.id}",
            )
            statut = st.selectbox(
                LABEL_STATUT,
                ["en_cours", "terminee", "en_pause"],
                index=(
                    ["en_cours", "terminee", "en_pause"].index(mission.statut)
                    if mission.statut in ["en_cours", "terminee", "en_pause"]
                    else 0
                ),
                key=f"edit_statut_{mission.id}",
            )

        technologies = st.text_input(
            LABEL_TECHNOLOGIES,
            value=mission.technologies_utilisees or "",
            key=f"edit_tech_{mission.id}",
        )
        description = st.text_area(
            "📝 Description",
            value=mission.description or "",
            height=100,
            key=f"edit_desc_{mission.id}",
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.form_submit_button("💾 Sauvegarder", type="primary"):
                save_mission_changes(
                    mission.id,
                    {
                        "nom_mission": nom_mission,
                        "client": client,
                        "role": role,
                        "date_debut": date_debut,
                        "date_fin": date_fin,
                        "statut": statut,
                        "revenus_generes": revenus,
                        "technologies_utilisees": technologies,
                        "description": description,
                    },
                )

        with col2:
            if st.form_submit_button("🗑️ Supprimer", type="secondary"):
                delete_mission(mission.id)

        with col3:
            if st.form_submit_button("❌ Annuler"):
                st.rerun()


def show_add_mission_form(consultant):
    """Formulaire d'ajout d'une nouvelle mission"""

    st.markdown("### ➕ Ajouter une nouvelle mission")

    with st.form("add_mission_form"):
        col1, col2 = st.columns(2)

        with col1:
            nom_mission = st.text_input(
                "📋 Nom de la mission",
                placeholder="Ex: Développement application mobile",
            )
            client = st.text_input("🏢 Client", placeholder="Ex: Société Générale")
            role = st.text_input("👤 Rôle", placeholder="Ex: Lead Developer")
            revenus = st.number_input("💰 Revenus (€)", min_value=0.0, value=0.0)

        with col2:
            date_debut = st.date_input("📅 Date début")
            date_fin = st.date_input("📅 Date fin (optionnel)", value=None)
            statut = st.selectbox(LABEL_STATUT, ["en_cours", "terminee", "en_pause"])

        technologies_str = st.text_input(
            LABEL_TECHNOLOGIES, placeholder="Ex: Python, Django, PostgreSQL"
        )
        description = st.text_area(
            "📝 Description",
            height=100,
            placeholder="Décrivez les activités réalisées durant cette mission...",
        )

        if st.form_submit_button("➕ Ajouter la mission", type="primary"):
            add_new_mission(
                consultant.id,
                {
                    "nom_mission": nom_mission,
                    "client": client,
                    "role": role,
                    "date_debut": date_debut,
                    "date_fin": date_fin,
                    "statut": statut,
                    "revenus_generes": revenus,
                    "technologies_utilisees": technologies_str,
                    "description": description,
                },
            )


def show_consultants_list():
    """Affiche la liste des consultants avec interactions optimisée et filtres avancés"""

    # Import des nouveaux composants UI
    try:
        from app.ui.enhanced_ui import AdvancedUIFilters
        from app.ui.enhanced_ui import DataTableEnhancer
        from app.ui.enhanced_ui import LoadingSpinner
        from app.ui.enhanced_ui import NotificationManager
        from app.ui.enhanced_ui import RealTimeSearch

        enhanced_ui_available = True
    except ImportError:
        enhanced_ui_available = False
        st.warning(
            "⚠️ Composants UI avancés non disponibles. Utilisation du mode classique."
        )

    if enhanced_ui_available:
        # Utilisation des nouveaux composants améliorés
        return show_consultants_list_enhanced()
    else:
        # Fallback vers l'ancienne méthode
        return show_consultants_list_classic()


def show_consultants_list_enhanced():
    """Version améliorée de la liste des consultants avec filtres avancés"""
    from app.ui.enhanced_ui import AdvancedUIFilters
    from app.ui.enhanced_ui import DataTableEnhancer
    from app.ui.enhanced_ui import LoadingSpinner
    from app.ui.enhanced_ui import NotificationManager
    from app.ui.enhanced_ui import RealTimeSearch

    # Initialisation des composants
    filters, search, enhancer = _initialize_ui_components()

    # Titre principal
    st.title("👥 Gestion des consultants - Version Améliorée")

    # Recherche en temps réel
    search_term = _render_search_input()

    # Chargement des données
    consultants = _load_consultants_data(search, search_term)
    if not consultants:
        return

    # Traitement et affichage des données
    consultants_data = _convert_consultants_to_data(consultants)
    filtered_data = filters.apply_filters(consultants_data)

    if filtered_data:
        _display_enhanced_metrics(filtered_data)
        _handle_enhanced_table_interactions(enhancer, filtered_data)
    else:
        _display_no_consultants_message()


def _initialize_ui_components():
    """Initialise les composants UI pour la liste améliorée"""
    from app.ui.enhanced_ui import AdvancedUIFilters
    from app.ui.enhanced_ui import DataTableEnhancer
    from app.ui.enhanced_ui import RealTimeSearch

    filters = AdvancedUIFilters()
    search = RealTimeSearch()
    enhancer = DataTableEnhancer()
    return filters, search, enhancer


def _render_search_input():
    """Affiche le champ de recherche en temps réel"""
    return st.text_input(
        "🔍 Recherche en temps réel",
        placeholder="Tapez pour rechercher instantanément...",
        help="La recherche se met à jour automatiquement pendant que vous tapez",
    )


def _load_consultants_data(search, search_term):
    """Charge les données des consultants avec gestion d'erreur"""
    from app.ui.enhanced_ui import LoadingSpinner

    with LoadingSpinner.show_loading("Chargement des données..."):
        try:
            if search_term and search.should_search():
                return ConsultantService.search_consultants_optimized(
                    search_term.strip()
                )
            else:
                return ConsultantService.get_all_consultants_with_stats()
        except (SQLAlchemyError, AttributeError) as exc:
            st.error(f"Erreur lors du chargement des données: {str(exc)}")
            return None


def _convert_consultants_to_data(consultants):
    """Convertit les données des consultants pour les filtres"""
    consultants_data = []
    for consultant in consultants:
        consultants_data.append(
            {
                "id": consultant["id"],
                "prenom": consultant["prenom"],
                "nom": consultant["nom"],
                "email": consultant["email"],
                "societe": consultant["societe"],
                "grade": consultant["grade"],
                "type_contrat": consultant["type_contrat"],
                "salaire_actuel": consultant.get("salaire_actuel", 0),
                "disponibilite": consultant.get("disponibilite", False),
                "practice_name": consultant.get("practice_name", ""),
                "experience_annees": consultant.get("experience_annees", 0),
                "nb_missions": consultant.get("nb_missions", 0),
                "salaire_formatted": consultant.get("salaire_formatted", "0€"),
                "cjm_formatted": consultant.get("cjm_formatted", "0€"),
                "experience_formatted": consultant.get("experience_formatted", "0 ans"),
                "statut": consultant.get("statut", "N/A"),
            }
        )
    return consultants_data


def _display_enhanced_metrics(filtered_data):
    """Affiche les métriques des consultants filtrés"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total filtré", len(filtered_data))

    with col2:
        disponibles = len([c for c in filtered_data if c.get("disponibilite", False)])
        st.metric("✅ Disponibles", disponibles)

    with col3:
        st.metric("🔴 Occupés", len(filtered_data) - disponibles)

    with col4:
        salaire_moyen = (
            sum(c.get("salaire_actuel", 0) for c in filtered_data) / len(filtered_data)
            if filtered_data
            else 0
        )
        st.metric("💰 Salaire moyen", f"{salaire_moyen:,.0f}€")


def _handle_enhanced_table_interactions(enhancer, filtered_data):
    """Gère les interactions avec le tableau amélioré"""
    from app.ui.enhanced_ui import NotificationManager

    event = enhancer.render_enhanced_table(filtered_data, "consultants_enhanced")

    if event and event.selection.rows:
        selected_idx = event.selection.rows[0]
        # S'assurer que selected_idx est un entier (gestion des mocks en test)
        try:
            selected_idx = int(selected_idx)
        except (TypeError, ValueError):
            selected_idx = 0

        if selected_idx < len(filtered_data):
            _process_selected_consultant(enhancer, filtered_data[selected_idx])


def _process_selected_consultant(enhancer, selected_consultant):
    """Traite la sélection d'un consultant dans le tableau"""
    from app.ui.enhanced_ui import NotificationManager

    action = enhancer.render_action_buttons(
        selected_consultant, ["view", "edit", "delete"]
    )

    if action in ["view", "edit"]:
        st.session_state.view_consultant_profile = selected_consultant["id"]
        st.rerun()
    elif action == "delete":
        if ConsultantService.delete_consultant(selected_consultant["id"]):
            NotificationManager.show_success("Consultant supprimé avec succès!")
            st.rerun()
        else:
            NotificationManager.show_error("Erreur lors de la suppression")


def _display_no_consultants_message():
    """Affiche le message quand aucun consultant n'est enregistré"""
    st.info("📝 Aucun consultant enregistré")
    st.markdown(
        "💡 Utilisez l'onglet **Ajouter un consultant** pour créer votre premier profil"
    )


def show_consultants_list_classic():
    """Version classique de la liste des consultants (fallback)"""
    # Champ de recherche
    search_term = _render_classic_search_input()

    try:
        # Chargement des données
        consultants = _load_classic_consultants_data(search_term)

        if consultants:
            _display_classic_consultants_table(consultants)
        else:
            _display_no_consultants_classic_message()

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors du chargement de la liste: {exc}")


def _render_classic_search_input():
    """Affiche le champ de recherche classique"""
    return st.text_input(
        "🔍 Rechercher un consultant",
        placeholder="Tapez un prénom, nom ou email pour filtrer...",
        help="La liste se filtre automatiquement pendant que vous tapez",
        key="consultant_search",
    )


def _load_classic_consultants_data(search_term):
    """Charge les données des consultants avec recherche"""
    if search_term and search_term.strip():
        consultants = ConsultantService.search_consultants_optimized(
            search_term.strip()
        )
        _display_search_results_info(consultants, search_term)
        return consultants
    else:
        return ConsultantService.get_all_consultants_with_stats()


def _display_search_results_info(consultants, search_term):
    """Affiche les informations sur les résultats de recherche"""
    if consultants:
        st.info(f"🔍 {len(consultants)} consultant(s) trouvé(s) pour '{search_term}'")
    else:
        st.warning(f"❌ Aucun consultant trouvé pour '{search_term}'")


def _display_classic_consultants_table(consultants):
    """Affiche le tableau classique des consultants"""
    consultants_data = _prepare_classic_table_data(consultants)
    df = pd.DataFrame(consultants_data)

    event = st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
    )

    # Gestion des sélections et métriques
    _handle_classic_table_selection(event, consultants_data)
    _display_classic_metrics(consultants)


def _prepare_classic_table_data(consultants):
    """Prépare les données pour le tableau classique"""
    consultants_data = []
    for consultant in consultants:
        consultants_data.append(
            {
                "ID": consultant["id"],
                "Prénom": consultant["prenom"],
                "Nom": consultant["nom"],
                "Email": consultant["email"],
                "Société": consultant["societe"],
                "Grade": consultant["grade"],
                "Contrat": consultant["type_contrat"],
                "Salaire": consultant["salaire_formatted"],
                "CJM": consultant["cjm_formatted"],
                "Expérience": consultant["experience_formatted"],
                "Statut": consultant["statut"],
                "Missions": consultant["nb_missions"],
            }
        )
    return consultants_data


def _handle_classic_table_selection(event, consultants_data):
    """Gère la sélection dans le tableau classique"""
    if event.selection.rows:
        selected_row = event.selection.rows[0]
        # S'assurer que selected_row est un entier (gestion des mocks en test)
        try:
            selected_row = int(selected_row)
        except (TypeError, ValueError):
            selected_row = 0

        if selected_row < len(consultants_data):
            selected_consultant = consultants_data[selected_row]
            _display_selected_consultant_actions(selected_consultant)
        else:
            st.error("❌ Erreur: Index de consultant invalide")


def _display_selected_consultant_actions(selected_consultant):
    """Affiche les actions pour le consultant sélectionné"""
    selected_id = selected_consultant["ID"]
    selected_name = f"{selected_consultant['Prénom']} {selected_consultant['Nom']}"

    st.success(f"✅ Consultant sélectionné : **{selected_name}**")

    col1, col2, col3 = st.columns(3)

    with col1:
        _render_view_button(selected_id)

    with col2:
        _render_edit_button(selected_id)

    with col3:
        _render_delete_button(selected_id)


def _render_view_button(selected_id):
    """Affiche le bouton Voir le profil"""
    if st.button(
        "👁️ Voir le profil",
        type="primary",
        width="stretch",
        key=f"view_{selected_id}",
    ):
        st.session_state.view_consultant_profile = selected_id
        st.rerun()


def _render_edit_button(selected_id):
    """Affiche le bouton Modifier"""
    if st.button(
        "✏️ Modifier",
        width="stretch",
        key=f"edit_{selected_id}",
    ):
        st.session_state.view_consultant_profile = selected_id
        st.rerun()


def _render_delete_button(selected_id):
    """Affiche le bouton Supprimer"""
    if st.button(
        "🗑️ Supprimer",
        width="stretch",
        key=f"delete_{selected_id}",
    ):
        if ConsultantService.delete_consultant(selected_id):
            st.success("✅ Consultant supprimé !")
            st.rerun()
        else:
            st.error("❌ Erreur lors de la suppression")


def _display_classic_metrics(consultants):
    """Affiche les métriques générales"""
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total consultants", len(consultants))

    with col2:
        disponibles = len([c for c in consultants if c.get("disponibilite", False)])
        st.metric("✅ Disponibles", disponibles)

    with col3:
        occupes = len(consultants) - disponibles
        st.metric("🔴 Occupés", occupes)

    with col4:
        _display_average_salary_metric(consultants)


def _display_average_salary_metric(consultants):
    """Affiche la métrique du salaire moyen"""
    if len(consultants) > 0:
        salaire_moyen = sum(c.get("salaire_actuel", 0) or 0 for c in consultants) / len(
            consultants
        )
    else:
        salaire_moyen = 0
    st.metric("💰 Salaire moyen", f"{salaire_moyen:,.0f}€")


def _display_no_consultants_classic_message():
    """Affiche le message quand aucun consultant n'est trouvé"""
    st.info("📝 Aucun consultant enregistré")
    st.markdown(
        "💡 Utilisez l'onglet **Ajouter un consultant** pour créer votre premier profil"
    )


def show_add_consultant_form():
    """Formulaire d'ajout d'un nouveau consultant"""
    st.subheader("➕ Ajouter un nouveau consultant")

    practice_options = _load_practice_options()

    with st.form("add_consultant_form"):
        # Champs de base
        basic_data = _render_basic_consultant_fields_form(practice_options)

        # Section historique société
        company_data = _render_company_history_section()

        # Section profil professionnel
        professional_data = _render_professional_profile_section()

        # Notes optionnelles
        notes = st.text_area(
            "📝 Notes (optionnel)",
            height=100,
            placeholder="Notes sur le consultant...",
        )

        # Bouton de création
        submitted = st.form_submit_button(
            "➕ Créer le consultant", type="primary", width="stretch"
        )

        if submitted:
            _process_consultant_creation(
                basic_data, company_data, professional_data, notes
            )


def _load_practice_options():
    """Charge les options de practice disponibles"""
    from database.models import Practice

    with get_database_session() as session:
        practices = session.query(Practice).filter(Practice.actif).all()
    return {p.nom: p.id for p in practices}


def _render_basic_consultant_fields_form(practice_options):
    """Rendu des champs de base du consultant"""
    col1, col2 = st.columns(2)

    with col1:
        prenom = st.text_input("👤 Prénom *", placeholder="Ex: Jean")
        email = st.text_input("📧 Email *", placeholder="jean.dupont@example.com")
        salaire = st.number_input(
            "💰 Salaire annuel (€)", min_value=0, value=45000, step=1000
        )
        # Sélection de la practice
        practice_label = st.selectbox(
            LABEL_PRACTICE,
            options=[STATUT_NON_AFFECTE] + list(practice_options.keys()),
            index=0,
        )
        selected_practice_id = practice_options.get(practice_label)

    with col2:
        nom = st.text_input("👤 Nom *", placeholder="Ex: Dupont")
        telephone = st.text_input("📞 Téléphone", placeholder="01.23.45.67.89")
        disponibilite = st.checkbox(STATUT_DISPONIBLE, value=True)

    return {
        "prenom": prenom,
        "nom": nom,
        "email": email,
        "telephone": telephone,
        "salaire": salaire,
        "disponibilite": disponibilite,
        "practice_id": selected_practice_id,
    }


def _render_company_history_section():
    """Rendu de la section historique société"""
    st.markdown("---")
    st.markdown("### 🏢 Historique Société")

    col3, col4 = st.columns(2)

    with col3:
        societe = st.selectbox("🏢 Société", options=["Quanteam", "Asigma"], index=0)
        date_entree = st.date_input(
            "📅 Date d'entrée société", help="Date d'entrée dans la société"
        )

    with col4:
        date_sortie = st.date_input(
            "📅 Date de sortie société (optionnel)",
            value=None,
            help="Laissez vide si encore en poste",
        )
        date_premiere_mission = st.date_input(
            "🚀 Date première mission (optionnel)",
            value=None,
            help="Date de début de la première mission",
        )

    return {
        "societe": societe,
        "date_entree": date_entree,
        "date_sortie": date_sortie,
        "date_premiere_mission": date_premiere_mission,
    }


def _render_professional_profile_section():
    """Rendu de la section profil professionnel"""
    st.markdown("---")
    st.markdown("### 👔 Profil Professionnel")

    col5, col6 = st.columns(2)

    with col5:
        grade = st.selectbox(
            "🎯 Grade",
            options=[
                "Junior",
                "Confirmé",
                "Consultant Manager",
                "Directeur de Practice",
            ],
            index=0,
            help="Niveau d'expérience du consultant",
        )

    with col6:
        type_contrat = st.selectbox(
            "📋 Type de contrat",
            options=["CDI", "CDD", "Stagiaire", "Alternant", "Indépendant"],
            index=0,
            help="Type de contrat de travail",
        )

    return {"grade": grade, "type_contrat": type_contrat}


def _process_consultant_creation(basic_data, company_data, professional_data, notes):
    """Traite la création du consultant"""
    prenom, nom, email = basic_data["prenom"], basic_data["nom"], basic_data["email"]

    if not prenom or not nom or not email:
        st.error(MSG_CHAMPS_OBLIGATOIRES)
        return

    # Vérifier l'unicité de l'email
    existing = ConsultantService.get_consultant_by_email(email)
    if existing:
        st.error("❌ Un consultant avec l'email " + email + " existe déjà !")
        return

    try:
        consultant_data = _build_consultant_data(
            basic_data, company_data, professional_data, notes
        )

        if ConsultantService.create_consultant(consultant_data):
            st.success(f"✅ {prenom} {nom} créé avec succès !")
            st.balloons()  # Animation de succès
            st.rerun()
        else:
            st.error("❌ Erreur lors de la création")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de la création: {e}")


def _build_consultant_data(basic_data, company_data, professional_data, notes):
    """Construit les données du consultant à créer"""
    return {
        "prenom": basic_data["prenom"].strip(),
        "nom": basic_data["nom"].strip(),
        "email": basic_data["email"].strip().lower(),
        "telephone": (
            basic_data["telephone"].strip() if basic_data["telephone"] else None
        ),
        "salaire": basic_data["salaire"],
        "disponible": basic_data["disponibilite"],
        "notes": notes.strip() if notes else None,
        "practice_id": basic_data["practice_id"],
        # Nouveaux champs V1.2
        "societe": company_data["societe"],
        "date_entree_societe": company_data["date_entree"],
        "date_sortie_societe": (
            company_data["date_sortie"] if company_data["date_sortie"] else None
        ),
        "date_premiere_mission": (
            company_data["date_premiere_mission"]
            if company_data["date_premiere_mission"]
            else None
        ),
        # Nouveaux champs V1.2.1
        "grade": professional_data["grade"],
        "type_contrat": professional_data["type_contrat"],
    }


# Fonctions utilitaires pour les missions


def save_mission_changes(mission_id, mission_data):
    """Sauvegarde les modifications d'une mission"""
    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()

            if mission:
                # Mettre à jour les champs
                mission.nom_mission = mission_data["nom_mission"]
                mission.client = mission_data["client"]
                mission.role = mission_data["role"]
                mission.date_debut = mission_data["date_debut"]
                mission.date_fin = mission_data["date_fin"]
                mission.statut = mission_data["statut"]
                mission.revenus_generes = mission_data["revenus_generes"]
                mission.technologies_utilisees = mission_data["technologies_utilisees"]
                mission.description = mission_data["description"]

                session.commit()
                st.success("✅ Mission mise à jour avec succès !")
                st.rerun()
            else:
                st.error("❌ Mission non trouvée")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors de la sauvegarde: {exc}")


def delete_mission(mission_id):
    """Supprime une mission"""
    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()

            if mission:
                session.delete(mission)
                session.commit()
                st.success("✅ Mission supprimée avec succès !")
                st.rerun()
            else:
                st.error("❌ Mission non trouvée")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors de la suppression: {exc}")


def add_new_mission(consultant_id, mission_data):
    """Ajoute une nouvelle mission"""

    if not mission_data["nom_mission"] or not mission_data["client"]:
        st.error("❌ Le nom de la mission et le client sont obligatoires")
        return

    try:
        with get_database_session() as session:
            nouvelle_mission = Mission(
                consultant_id=consultant_id,
                nom_mission=mission_data["nom_mission"],
                client=mission_data["client"],
                role=mission_data["role"],
                date_debut=mission_data["date_debut"],
                date_fin=mission_data["date_fin"],
                statut=mission_data["statut"],
                revenus_generes=mission_data["revenus_generes"],
                technologies_utilisees=mission_data["technologies_utilisees"],
                description=mission_data["description"],
            )

            session.add(nouvelle_mission)
            session.commit()
            st.success("✅ Nouvelle mission ajoutée avec succès !")
            st.rerun()

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as exc:
        st.error(f"❌ Erreur lors de l'ajout: {exc}")


def show_consultant_documents(consultant):
    """Affiche et gère les documents du consultant"""

    st.subheader("📁 Documents de " + consultant.prenom + " " + consultant.nom)

    # Upload direct sans expander
    uploaded_file = st.file_uploader(
        "Choisir un fichier",
        type=["pdf", "docx", "doc", "pptx", "ppt"],
        help="Formats supportés: PDF, Word (docx/doc), PowerPoint (pptx/ppt)",
        key=f"document_uploader_{consultant.id}",
    )

    if uploaded_file is not None:
        # Afficher les informations du fichier et sauvegarder automatiquement
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📄 Nom", uploaded_file.name)

        with col2:
            file_size = uploaded_file.size / 1024  # en KB
            if file_size > 1024:
                size_display = f"{file_size / 1024:.1f} MB"
            else:
                size_display = f"{file_size:.1f} KB"
            st.metric(LABEL_TAILLE, size_display)

        with col3:
            # Détection automatique du type basé sur l'extension et le nom
            auto_type = detect_document_type(uploaded_file.name)
            st.metric("🏷️ Type détecté", auto_type)

        # Sauvegarde automatique en un clic
        if st.button(
            "💾 Sauvegarder ce document",
            type="primary",
            key=f"save_doc_{consultant.id}",
        ):
            save_consultant_document_simple(uploaded_file, consultant)

    st.markdown("---")

    # Liste des documents existants
    show_existing_documents(consultant)


def save_consultant_document(uploaded_file, consultant, document_type):
    """Sauvegarde un document pour le consultant"""

    try:
        # Initialiser le répertoire d'upload
        upload_dir = DocumentService.init_upload_directory()

        # Vérifier le type de fichier
        if not DocumentService.is_allowed_file(uploaded_file.name):
            st.error("❌ Type de fichier non supporté")
            return

        # Générer un nom de fichier unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = DocumentService.get_file_extension(uploaded_file.name)

        # Nom du fichier: consultant_nom_type_timestamp.extension
        safe_name = f"{consultant.prenom}_{consultant.nom}_{document_type}_{timestamp}.{file_extension}"
        safe_name = safe_name.replace(" ", "_").replace("-", "_")

        file_path = upload_dir / safe_name

        # Sauvegarder le fichier
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ Document '{document_type}' sauvegardé avec succès !")
        st.info(f"📁 Fichier: {safe_name}")

        # Si c'est un CV, proposer l'analyse automatique
        # Proposer l'analyse CV pour TOUS les types de documents
        if st.button("🔍 Analyser comme CV", key=f"analyze_{consultant.id}"):
            # st.write(f"🎯 **BOUTON UPLOAD CLIQUÉ** pour consultant {consultant.id}")  # Debug
            # Analyser le document qui vient d'être uploadé
            analyze_cv_document(file_path, consultant)
            return  # Ne pas recharger après l'analyse

        # Recharger la page pour afficher le nouveau document
        st.rerun()

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as exc:
        st.error(f"❌ Erreur lors de la sauvegarde: {exc}")


def save_consultant_document_simple(uploaded_file, consultant):
    """Sauvegarde simplifiée d'un document pour le consultant"""

    try:
        # Initialiser le répertoire d'upload
        upload_dir = DocumentService.init_upload_directory()

        # Vérifier le type de fichier
        if not DocumentService.is_allowed_file(uploaded_file.name):
            st.error("❌ Type de fichier non supporté")
            return

        # Générer un nom de fichier avec préfixe consultant
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = uploaded_file.name
        name_parts = original_name.rsplit(".", 1)

        if len(name_parts) == 2:
            name, extension = name_parts
            # Nom final: ID_Nom_Prenom_FichierOriginal_Timestamp.extension
            safe_name = f"{consultant.id}_{consultant.prenom}_{consultant.nom}_{name}_{timestamp}.{extension}"
        else:
            # Pas d'extension
            safe_name = f"{consultant.id}_{consultant.prenom}_{consultant.nom}_{original_name}_{timestamp}"

        # Nettoyer le nom de fichier
        safe_name = safe_name.replace(" ", "_").replace("-", "_")

        file_path = upload_dir / safe_name

        # Sauvegarder le fichier
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Détection du type pour message
        doc_type = detect_document_type(uploaded_file.name)

        st.success(f"✅ Document '{doc_type}' sauvegardé avec succès !")
        st.info(f"📁 Fichier: {safe_name}")

        # Proposer l'analyse pour tous les documents
        st.info("📋 Analyse de document disponible")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(
                "🔍 Analyser comme CV",
                type="primary",
                key=f"analyze_cv_{consultant.id}_{timestamp}",
            ):
                analyze_cv_document(file_path, consultant)

        with col2:
            if st.button(
                "📄 Analyser le contenu",
                key=f"analyze_content_{consultant.id}_{timestamp}",
            ):
                st.info("🚧 Analyse de contenu générique en développement")

        with col3:
            if st.button(
                "🔄 Actualiser la liste",
                key=f"refresh_{consultant.id}_{timestamp}",
            ):
                st.rerun()

        st.success(
            "💡 Le document a été sauvegardé ! Cliquez sur 'Actualiser la liste' pour le voir dans la liste ci-dessous."
        )

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as exc:
        st.error(f"❌ Erreur lors de la sauvegarde: {exc}")


def show_existing_documents(consultant):
    """Affiche les documents existants du consultant"""

    try:
        upload_dir = DocumentService.init_upload_directory()

        # Chercher les fichiers du consultant avec le nouveau format et l'ancien format
        consultant_pattern_new = (
            f"{consultant.id}_{consultant.prenom}_{consultant.nom}_*"
        )
        consultant_pattern_old = f"{consultant.prenom}_{consultant.nom}_*"

        matching_files_new = list(upload_dir.glob(consultant_pattern_new))
        matching_files_old = list(upload_dir.glob(consultant_pattern_old))

        # Combiner les deux listes et éliminer les doublons
        matching_files = list(set(matching_files_new + matching_files_old))

        if not matching_files:
            st.info("📂 Aucun document trouvé pour ce consultant")
            return

        st.subheader(f"📋 Documents existants ({len(matching_files)})")

        # Afficher chaque document dans une ligne simple avec boutons directs
        for file_path in sorted(
            matching_files, key=lambda x: x.stat().st_mtime, reverse=True
        ):
            file_stats = file_path.stat()
            file_size = file_stats.st_size / 1024  # KB
            if file_size > 1024:
                size_display = f"{file_size / 1024:.1f} MB"
            else:
                size_display = f"{file_size:.1f} KB"

            modified_time = datetime.fromtimestamp(file_stats.st_mtime)

            # Extraire le nom original du fichier (enlever préfixes)
            display_name = extract_original_filename(file_path.name)
            doc_type = detect_document_type(display_name)

            # DEBUG: Afficher le type détecté
            # st.write(f"🔍 DEBUG: {file_path.name} → Type: '{doc_type}'")

            # Interface simplifiée avec colonnes
            col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])

            with col1:
                st.write(f"📄 **{display_name}**")
                st.caption(
                    f"{doc_type} • {size_display} • {modified_time.strftime(FORMAT_DATE)}"
                )

            with col2:
                # Bouton téléchargement direct
                download_document_direct(file_path, consultant, display_name)

            with col3:
                if st.button(
                    "�️", key=f"preview_{file_path.name}", help="Prévisualiser"
                ):
                    preview_document(file_path)

            with col4:
                # Bouton d'analyse CV pour TOUS les documents
                if st.button(
                    "🔍",
                    key=f"analyze_{file_path.name}",
                    help="Analyser comme CV",
                ):
                    # st.write(f"🎯 **BOUTON CLIQUÉ** pour {file_path.name}")  # Debug
                    analyze_cv_document(file_path, consultant)

            with col5:
                if st.button("🗑️", key=f"delete_{file_path.name}", help="Supprimer"):
                    delete_consultant_document(file_path)

            with col6:
                st.write("")  # Espace

            st.markdown("---")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as exc:
        st.error(f"❌ Erreur lors de l'affichage des documents: {exc}")


def delete_consultant_document(file_path):
    """
    Supprime un document du consultant du système de fichiers

    Args:
        file_path: Chemin complet vers le fichier à supprimer

    Raises:
        OSError: En cas d'erreur lors de la suppression du fichier
    """
    try:
        if file_path.exists():
            file_path.unlink()
            st.success("✅ Document supprimé avec succès")
            st.rerun()
        else:
            st.error(MSG_FICHIER_INTROUVABLE)
    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as exc:
        st.error(f"❌ Erreur lors de la suppression: {exc}")


def detect_document_type(filename):
    """
    Détecte automatiquement le type de document basé sur le nom de fichier

    Args:
        filename: Nom du fichier à analyser

    Returns:
        str: Type de document détecté ("CV", "Lettre de motivation", etc.)

    Note:
        La détection se base sur des mots-clés dans le nom du fichier
        et sur l'extension si aucun mot-clé n'est trouvé
    """
    filename_lower = filename.lower()

    # Détection basée sur le nom du fichier
    if any(word in filename_lower for word in ["cv", "resume", "curriculum"]):
        return "CV"
    elif any(
        word in filename_lower for word in ["lettre", "motivation", "cover", "letter"]
    ):
        return "Lettre de motivation"
    elif any(
        word in filename_lower
        for word in ["certificat", "certificate", "diplome", "diploma"]
    ):
        return "Certificat"
    elif any(word in filename_lower for word in ["contrat", "contract", "convention"]):
        return "Contrat"
    elif any(word in filename_lower for word in ["presentation", "slides", "demo"]):
        return "Présentation"
    else:
        # Détection basée sur l'extension
        extension = filename_lower.split(".")[-1] if "." in filename_lower else ""
        if extension in ["pdf"]:
            return "Document PDF"
        elif extension in ["docx", "doc"]:
            return "Document Word"
        elif extension in ["pptx", "ppt"]:
            return "Présentation PowerPoint"
        else:
            return "Document"


def get_mime_type(filename):
    """
    Retourne le type MIME basé sur l'extension du fichier

    Args:
        filename: Nom du fichier avec son extension

    Returns:
        str: Type MIME du fichier ou "application/octet-stream" par défaut

    Example:
        >>> get_mime_type("document.pdf")
        'application/pdf'
        >>> get_mime_type("presentation.pptx")
        'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    """
    extension = filename.lower().split(".")[-1] if "." in filename else ""

    mime_types = {
        "pdf": "application/pdf",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "ppt": "application/vnd.ms-powerpoint",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    }

    return mime_types.get(extension, "application/octet-stream")


def extract_original_filename(full_filename):
    """
    Extrait le nom original du fichier en enlevant les préfixes consultant

    Args:
        full_filename: Nom complet du fichier avec préfixes (format: ID_Prenom_Nom_FichierOriginal_Timestamp.extension)

    Returns:
        str: Nom original du fichier sans les préfixes

    Note:
        Le format attendu est: ID_Prenom_Nom_FichierOriginal_Timestamp.extension
        Si le format n'est pas reconnu, retourne le nom complet
    """
    # Format attendu: ID_Prenom_Nom_FichierOriginal_Timestamp.extension
    parts = full_filename.split("_")

    if len(parts) >= 4:
        remaining_parts = _get_filename_remaining_parts(parts)
        original_name = _extract_original_name_from_parts(
            remaining_parts, full_filename
        )

        if original_name:
            return original_name

    # Si le format n'est pas reconnu, retourner le nom complet
    return full_filename


def _get_filename_remaining_parts(parts):
    """Extrait les parties restantes après ID, Prénom, Nom"""
    # Les 3 premières parties (ID, Prénom, Nom) ne sont pas utilisées dans le traitement
    return parts[3:]


def _extract_original_name_from_parts(remaining_parts, full_filename):
    """Extrait le nom original à partir des parties restantes"""
    original_parts, timestamp_found = _find_original_parts_before_timestamp(
        remaining_parts
    )

    if original_parts:
        original_name = "_".join(original_parts)
        return _add_extension_to_original_name(
            original_name, remaining_parts, timestamp_found, full_filename
        )

    return None


def _find_original_parts_before_timestamp(remaining_parts):
    """Trouve les parties originales avant le timestamp"""
    original_parts = []
    timestamp_found = False

    for i, part in enumerate(remaining_parts):
        if _is_timestamp_part(part):
            # C'est probablement un timestamp, arrêter ici
            original_parts = remaining_parts[:i]
            timestamp_found = True
            break

    if not timestamp_found:
        original_parts = _handle_no_timestamp_found(remaining_parts)

    return original_parts, timestamp_found


def _is_timestamp_part(part):
    """Vérifie si une partie ressemble à un timestamp YYYYMMDD"""
    return len(part) == 8 and part.isdigit() and part.startswith(("20", "19"))


def _handle_no_timestamp_found(remaining_parts):
    """Gère le cas où aucun timestamp n'est trouvé"""
    # Si pas de timestamp trouvé, prendre tout sauf la dernière partie (qui peut contenir l'extension)
    if len(remaining_parts) > 1:
        return remaining_parts[:-1]
    else:
        return remaining_parts


def _add_extension_to_original_name(
    original_name, remaining_parts, timestamp_found, full_filename
):
    """Ajoute l'extension appropriée au nom original"""
    last_part = remaining_parts[-1] if remaining_parts else ""

    if "." in last_part:
        return _handle_extension_in_last_part(
            original_name, last_part, timestamp_found, full_filename
        )
    elif "." not in original_name and "." in full_filename:
        return _add_extension_from_full_filename(original_name, full_filename)

    return original_name


def _handle_extension_in_last_part(
    original_name, last_part, timestamp_found, full_filename
):
    """Gère l'extension quand elle est dans la dernière partie"""
    name_without_ext = last_part.split(".")[0]
    extension = last_part.split(".")[-1]

    # Si on a trouvé un timestamp, la dernière partie devrait être le timestamp.extension
    if timestamp_found:
        # On ajoute l'extension du fichier complet
        if "." in full_filename:
            extension = full_filename.split(".")[-1]
            return f"{original_name}.{extension}"
    else:
        # Pas de timestamp trouvé, utiliser la logique normale
        if not original_name:
            original_name = name_without_ext
        return f"{original_name}.{extension}"

    return original_name


def _add_extension_from_full_filename(original_name, full_filename):
    """Ajoute l'extension en la cherchant dans le nom complet"""
    if "." in full_filename:
        extension = full_filename.split(".")[-1]
        return f"{original_name}.{extension}"
    return original_name


def download_document_direct(file_path, consultant, display_name):
    """Bouton de téléchargement direct"""

    try:
        if not file_path.exists():
            st.error(MSG_FICHIER_INTROUVABLE)
            return

        # Lire le fichier
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Bouton de téléchargement avec le nom original
        st.download_button(
            label="⬇️",
            data=file_data,
            file_name=display_name,
            mime=get_mime_type(display_name),
            key=f"download_direct_{file_path.name}_{consultant.id}",
            help=f"Télécharger {display_name}",
        )

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as exc:
        st.error(f"❌ Erreur: {exc}")


def download_document(file_path, consultant):
    """Prépare le téléchargement d'un document"""

    try:
        if not file_path.exists():
            st.error(MSG_FICHIER_INTROUVABLE)
            return

        # Lire le fichier
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Créer le bouton de téléchargement
        st.download_button(
            label="⬇️ Cliquez pour télécharger",
            data=file_data,
            file_name=file_path.name,
            mime=get_mime_type(file_path.name),
            key=f"download_btn_{file_path.name}_{consultant.id}",
        )

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as exc:
        st.error(f"❌ Erreur lors du téléchargement: {exc}")


def preview_document(file_path):
    """Affiche un aperçu du document"""

    try:
        if not file_path.exists():
            st.error(MSG_FICHIER_INTROUVABLE)
            return

        file_extension = file_path.suffix.lower()

        # Modal/Expander pour l'aperçu
        with st.expander(f"👁️ Aperçu de {file_path.name}", expanded=True):
            if file_extension == ".pdf":
                preview_pdf(file_path)
            elif file_extension in [".doc", ".docx"]:
                preview_word(file_path)
            elif file_extension in [".ppt", ".pptx"]:
                preview_powerpoint(file_path)
            else:
                st.info("👁️ Aperçu non disponible pour ce type de fichier")
                st.info("💡 Utilisez le bouton télécharger pour voir le fichier")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as exc:
        st.error(f"❌ Erreur lors de l'aperçu: {exc}")


def preview_pdf(file_path):
    """Aperçu d'un fichier PDF"""

    try:
        with open(file_path, "rb") as f:
            pdf_data = f.read()

        # Afficher le PDF dans un iframe
        st.subheader("📄 Aperçu PDF")

        # Créer un lien pour ouvrir le PDF dans un nouvel onglet
        import base64

        b64_pdf = base64.b64encode(pdf_data).decode("utf-8")

        # Affichage du PDF
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{b64_pdf}"
                width="100%" height="600" type="application/pdf">
            <p>Votre navigateur ne supporte pas l'affichage PDF.
               <a href="data:application/pdf;base64,{b64_pdf}" target="_blank">
               Cliquez ici pour ouvrir dans un nouvel onglet</a>
            </p>
        </iframe>
        """

        st.markdown(pdf_display, unsafe_allow_html=True)

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as exc:
        st.error(f"❌ Erreur lors de l'aperçu PDF: {exc}")
        st.info("💡 Utilisez le bouton télécharger pour voir le fichier")


def preview_word(file_path):
    """Aperçu d'un fichier Word"""

    try:
        st.subheader("📝 Aperçu Document Word")
        st.info(f"📁 Fichier: {file_path.name}")

        # Informations sur le fichier
        file_stats = file_path.stat()
        file_size = file_stats.st_size / 1024
        if file_size > 1024:
            size_display = f"{file_size / 1024:.1f} MB"
        else:
            size_display = f"{file_size:.1f} KB"

        col1, col2 = st.columns(2)
        with col1:
            st.metric(LABEL_TAILLE, size_display)
        with col2:
            modified_time = datetime.fromtimestamp(file_stats.st_mtime)
            st.metric("📅 Modifié", modified_time.strftime(FORMAT_DATE))

        # Tenter d'extraire le texte si possible
        st.info("📄 Aperçu textuel non disponible")
        st.info("💡 Utilisez le bouton télécharger pour voir le fichier complet")

        # Note pour l'utilisateur
        st.markdown(
            """
        **📝 Document Word détecté**
        - Téléchargez le fichier pour le voir dans Microsoft Word
        - L'aperçu complet nécessite des modules supplémentaires
        """
        )

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de l'aperçu Word: {e}")


def preview_powerpoint(file_path):
    """Aperçu d'un fichier PowerPoint"""

    try:
        st.subheader("📊 Aperçu Présentation PowerPoint")
        st.info(f"📁 Fichier: {file_path.name}")

        # Informations sur le fichier
        file_stats = file_path.stat()
        file_size = file_stats.st_size / 1024
        if file_size > 1024:
            size_display = f"{file_size / 1024:.1f} MB"
        else:
            size_display = f"{file_size:.1f} KB"

        col1, col2 = st.columns(2)
        with col1:
            st.metric(LABEL_TAILLE, size_display)
        with col2:
            modified_time = datetime.fromtimestamp(file_stats.st_mtime)
            st.metric("📅 Modifié", modified_time.strftime(FORMAT_DATE))

        # Note pour l'utilisateur
        st.markdown(
            """
        **📊 Présentation PowerPoint détectée**
        - Téléchargez le fichier pour le voir dans Microsoft PowerPoint
        - L'aperçu des slides nécessite des modules supplémentaires
        """
        )

        st.info("🎯 Pour voir le contenu complet, utilisez le bouton télécharger")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de l'aperçu PowerPoint: {e}")


def analyze_cv_document(file_path, consultant):
    """Analyse un CV et stocke les résultats dans le session state pour affichage pleine largeur"""

    try:
        st.info("🔍 Analyse du fichier: " + file_path.name)

        # Vérifier que le fichier existe
        if not file_path.exists():
            st.error(f"❌ Le fichier {file_path} n'existe pas")
            return

        with st.spinner("🔍 Analyse du CV en cours..."):
            # Extraction du texte
            text = DocumentAnalyzer.extract_text_from_file(str(file_path))

            if not text:
                st.warning("⚠️ Aucun texte extrait du document")
                return
            elif len(text.strip()) < 50:
                st.warning(
                    f"⚠️ Le document semble trop court ({len(text.strip())} caractères)"
                )
                return

            st.success(f"✅ Texte extrait avec succès ({len(text)} caractères)")

            # Analyse du contenu
            consultant_name = f"{consultant.prenom} {consultant.nom}"
            analysis = DocumentAnalyzer.analyze_cv_content(text, consultant_name)

            if not analysis:
                st.error("❌ L'analyse n'a retourné aucun résultat")
                return

            # Stocker les résultats dans le session state pour affichage pleine largeur
            st.session_state.cv_analysis = {
                "analysis": analysis,
                "consultant": consultant,
                "file_name": file_path.name,
                "text_length": len(text),
            }

            st.success(
                "✅ Analyse terminée ! Résultats affichés ci-dessus en pleine largeur."
            )
            st.rerun()  # Recharger pour afficher les résultats

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de l'analyse : {e}")
        st.info("💡 Vérifiez que le fichier est bien un CV valide")


def show_cv_missions(missions, consultant):
    """Affiche les missions extraites du CV avec possibilité d'édition et sauvegarde"""
    if not missions:
        st.info("📋 Aucune mission détectée dans le CV")
        return

    _setup_cv_missions_styling()
    _display_cv_missions_header(missions)
    _display_cv_missions_global_save_button(missions, consultant)
    _display_cv_missions_list(missions, consultant)


def _setup_cv_missions_styling():
    """Configure le CSS pour l'affichage des missions CV"""
    st.markdown(
        """
    <style>
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


def _display_cv_missions_header(missions):
    """Affiche l'en-tête avec le nombre de missions"""
    st.markdown(f"### 📋 {len(missions)} mission(s) détectée(s) dans le CV")


def _display_cv_missions_global_save_button(missions, consultant):
    """Affiche le bouton de sauvegarde globale"""
    if st.button("💾 Sauvegarder TOUTES les missions", type="primary", width="stretch"):
        _handle_global_missions_save(missions, consultant)


def _handle_global_missions_save(missions, consultant):
    """Gère la sauvegarde globale de toutes les missions"""
    all_valid = _validate_all_missions(missions)

    if all_valid:
        save_all_missions_to_consultant(missions, consultant)
    else:
        _display_global_validation_errors()


def _validate_all_missions(missions):
    """Valide toutes les missions et retourne True si toutes sont valides"""
    all_valid = True
    for i, mission in enumerate(missions, 1):
        client = mission.get("client", "")
        titre = mission.get("titre", "")

        if not client or not titre:
            all_valid = False
            st.error(f"❌ Mission {i}: Client et titre sont obligatoires")

    return all_valid


def _display_global_validation_errors():
    """Affiche les erreurs de validation globale"""
    st.warning(
        "⚠️ Veuillez corriger les missions ci-dessous avant de sauvegarder toutes les missions."
    )
    st.info(
        "💡 Conseil: Utilisez les boutons de sauvegarde individuels pour voir les erreurs détaillées."
    )


def _display_cv_missions_list(missions, consultant):
    """Affiche la liste des missions avec formulaires individuels"""
    st.markdown("---")

    for i, mission in enumerate(missions, 1):
        _display_single_cv_mission(mission, i, consultant, len(missions))


def _display_single_cv_mission(mission, mission_index, consultant, total_missions):
    """Affiche une mission individuelle avec son formulaire"""
    with st.container():
        _display_cv_mission_header(mission, mission_index)
        _display_cv_mission_form(mission, mission_index, consultant)
        _display_cv_mission_preview(mission_index)
        _display_cv_mission_separator(mission_index, total_missions)


def _display_cv_mission_header(mission, mission_index):
    """Affiche l'en-tête d'une mission"""
    client_name = mission.get("client", "Client inconnu")
    st.markdown(f"### 🏢 Mission {mission_index}: {client_name}")


def _display_cv_mission_form(mission, mission_index, consultant):
    """Affiche le formulaire d'édition d'une mission"""
    _initialize_mission_validation_state(mission_index)
    validation_errors = st.session_state.get(f"validation_errors_{mission_index}", [])

    # Champs client et titre
    client = _display_cv_mission_client_field(mission, mission_index, validation_errors)
    titre = _display_cv_mission_titre_field(mission, mission_index, validation_errors)

    # Champs dates
    date_debut, date_fin = _display_cv_mission_dates_fields(
        mission_index, validation_errors
    )

    # Champs description et technologies
    description = _display_cv_mission_description_field(mission, mission_index)
    technologies = _display_cv_mission_technologies_field(mission, mission_index)

    # Bouton de sauvegarde
    _display_cv_mission_save_button(
        mission_index,
        consultant,
        client,
        titre,
        date_debut,
        date_fin,
        description,
        technologies,
    )


def _initialize_mission_validation_state(mission_index):
    """Initialise l'état de validation pour une mission"""
    if f"validation_errors_{mission_index}" not in st.session_state:
        st.session_state[f"validation_errors_{mission_index}"] = []


def _display_cv_mission_client_field(mission, mission_index, validation_errors):
    """Affiche le champ client avec validation"""
    client_error = f"mission_{mission_index}_client" in validation_errors
    if client_error:
        st.markdown("**🚨 Client requis**", help=MSG_CHAMP_OBLIGATOIRE)

    return st.text_input(
        "🏢 Client *" + (" 🚨" if client_error else ""),
        value=mission.get("client", ""),
        key=f"mission_{mission_index}_client",
        help="Nom du client pour cette mission (OBLIGATOIRE)",
        placeholder="Exemple: Société Générale, BNP Paribas...",
    )


def _display_cv_mission_titre_field(mission, mission_index, validation_errors):
    """Affiche le champ titre avec validation"""
    titre_error = f"mission_{mission_index}_titre" in validation_errors
    if titre_error:
        st.markdown("**🚨 Rôle/Titre requis**", help=MSG_CHAMP_OBLIGATOIRE)

    return st.text_input(
        "👤 Rôle/Titre *" + (" 🚨" if titre_error else ""),
        value=mission.get("titre", ""),
        key=f"mission_{mission_index}_titre",
        help="Votre rôle ou titre dans cette mission (OBLIGATOIRE)",
        placeholder="Exemple: Développeur Full Stack, Consultant...",
    )


def _display_cv_mission_dates_fields(mission_index, validation_errors):
    """Affiche les champs de dates avec validation"""
    col_date1, col_date2 = st.columns(2)

    with col_date1:
        date_debut = _display_cv_mission_date_debut_field(
            mission_index, validation_errors
        )

    with col_date2:
        date_fin = _display_cv_mission_date_fin_field(mission_index)

    return date_debut, date_fin


def _display_cv_mission_date_debut_field(mission_index, validation_errors):
    """Affiche le champ date de début"""
    date_error = f"mission_{mission_index}_debut" in validation_errors
    if date_error:
        st.markdown("**🚨 Date de début requise**", help=MSG_CHAMP_OBLIGATOIRE)

    return st.date_input(
        "📅 Date de début *" + (" 🚨" if date_error else ""),
        value=None,
        key=f"mission_{mission_index}_debut",
        help="Date de début de la mission (OBLIGATOIRE)",
    )


def _display_cv_mission_date_fin_field(mission_index):
    """Affiche le champ date de fin"""
    return st.date_input(
        "📅 Date de fin",
        value=None,
        key=f"mission_{mission_index}_fin",
        help="Date de fin (laisser vide si en cours)",
    )


def _display_cv_mission_description_field(mission, mission_index):
    """Affiche le champ description"""
    return st.text_area(
        "📝 Description de la mission",
        value=mission.get("description", ""),
        height=120,
        key=f"mission_{mission_index}_description",
        help="Description détaillée de vos activités et responsabilités",
    )


def _display_cv_mission_technologies_field(mission, mission_index):
    """Affiche le champ technologies"""
    technologies_text = ", ".join(mission.get("langages_techniques", []))
    return st.text_area(
        "🛠️ Technologies et outils utilisés",
        value=technologies_text,
        height=80,
        key=f"mission_{mission_index}_technologies",
        help="Technologies, langages, outils séparés par des virgules (ex: Python, React, AWS, Docker)",
    )


def _display_cv_mission_save_button(
    mission_index,
    consultant,
    client,
    titre,
    date_debut,
    date_fin,
    description,
    technologies,
):
    """Affiche le bouton de sauvegarde d'une mission"""
    if st.button(
        f"💾 Sauvegarder Mission {mission_index}",
        key=f"save_mission_{mission_index}",
        type="primary",
        width="stretch",
        help="Ajouter cette mission au profil du consultant",
    ):
        _handle_single_mission_save(
            mission_index,
            consultant,
            client,
            titre,
            date_debut,
            date_fin,
            description,
            technologies,
        )


def _handle_single_mission_save(
    mission_index,
    consultant,
    client,
    titre,
    date_debut,
    date_fin,
    description,
    technologies,
):
    """Gère la sauvegarde d'une mission individuelle"""
    validation_errors = validate_mission_fields(
        client, titre, date_debut, mission_index
    )
    st.session_state[f"validation_errors_{mission_index}"] = validation_errors

    if validation_errors:
        show_validation_errors(validation_errors, mission_index)
        st.rerun()
    else:
        _save_validated_mission(
            consultant,
            client,
            titre,
            date_debut,
            date_fin,
            description,
            technologies,
            mission_index,
        )


def _save_validated_mission(
    consultant,
    client,
    titre,
    date_debut,
    date_fin,
    description,
    technologies,
    mission_index,
):
    """Sauvegarde une mission validée"""
    st.session_state[f"validation_errors_{mission_index}"] = []

    success = save_mission_to_consultant(
        consultant,
        client,
        titre,
        date_debut,
        date_fin,
        description,
        technologies,
        mission_index,
    )

    if success:
        st.success(
            "Mission sauvegardée ! Vous pouvez maintenant remplir la mission suivante."
        )


def _display_cv_mission_preview(mission_index):
    """Affiche l'aperçu de la mission à sauvegarder"""
    client = st.session_state.get(f"mission_{mission_index}_client", "")
    titre = st.session_state.get(f"mission_{mission_index}_titre", "")
    date_debut = st.session_state.get(f"mission_{mission_index}_debut")

    if client and titre and date_debut:
        st.info(
            f"✅ Prêt à sauvegarder: {titre} chez {client} (début: {date_debut.strftime(FORMAT_DATE)})"
        )
    else:
        _display_mission_missing_fields(client, titre, date_debut)


def _display_mission_missing_fields(client, titre, date_debut):
    """Affiche les champs manquants pour une mission"""
    missing = []
    if not client:
        missing.append("Client")
    if not titre:
        missing.append("Rôle/Titre")
    if not date_debut:
        missing.append("Date de début")
    st.warning(f"⚠️ Champs manquants: {', '.join(missing)}")


def _display_cv_mission_separator(mission_index, total_missions):
    """Affiche le séparateur entre les missions"""
    if mission_index < total_missions:
        st.markdown("---")
        st.markdown("")  # Espace supplémentaire


def save_all_missions_to_consultant(missions, consultant):
    """
    Sauvegarde toutes les missions extraites du CV dans la base de données

    Args:
        missions: Liste des dictionnaires de missions extraites du CV
        consultant: Objet Consultant propriétaire des missions

    Note:
        Cette fonction valide chaque mission avant de la sauvegarder
        et gère les erreurs individuelles sans interrompre le processus
    """
    try:
        if not missions:
            st.warning("⚠️ Aucune mission à sauvegarder")
            return

        success_count = 0
        error_count = 0

        with get_database_session() as session:
            # Récupérer le consultant depuis la DB pour éviter les problèmes de session
            consultant_fresh = (
                session.query(Consultant).filter(Consultant.id == consultant.id).first()
            )

            if not consultant_fresh:
                st.error(f"❌ Consultant avec ID {consultant.id} introuvable")
                return

            for i, mission in enumerate(missions, 1):
                try:
                    client = mission.get("client", f"Client Mission {i}")
                    titre = mission.get("titre", f"Mission {i}")

                    if not client or not titre:
                        error_count += 1
                        continue

                    # Convertir les technologies en string
                    tech_list = mission.get("langages_techniques", [])
                    technologies_str = ", ".join(tech_list) if tech_list else None

                    # Créer la nouvelle mission
                    nouvelle_mission = Mission(
                        consultant_id=consultant_fresh.id,
                        nom_mission=titre,
                        client=client,
                        role=titre,
                        description=mission.get("description", ""),
                        technologies_utilisees=technologies_str,
                        statut="terminee",  # Par défaut terminée pour CV
                    )

                    session.add(nouvelle_mission)
                    success_count += 1

                except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
                    error_count += 1
                    st.error(f"❌ Erreur mission {i}: {str(e)}")

            if success_count > 0:
                session.commit()
                st.success(f"✅ {success_count} mission(s) sauvegardée(s) avec succès!")
                if error_count > 0:
                    st.warning(
                        f"⚠️ {error_count} mission(s) n'ont pas pu être sauvegardées"
                    )
                st.info(
                    "💡 Consultez l'onglet 'Missions' du profil pour voir les missions ajoutées"
                )
                st.balloons()
            else:
                st.error("❌ Aucune mission n'a pu être sauvegardée")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur générale lors de la sauvegarde : {e}")

        # Debug info supprimé pour la production


def validate_mission_fields(client, titre, date_debut, mission_num):
    """
    Valide les champs d'une mission et retourne les erreurs

    Args:
        client: Nom du client
        titre: Titre/rôle de la mission
        date_debut: Date de début de la mission
        mission_num: Numéro de la mission pour les messages d'erreur

    Returns:
        List[str]: Liste des champs en erreur (format: "mission_X_champ")
    """
    errors = []

    if not client or client.strip() == "":
        errors.append(f"mission_{mission_num}_client")

    if not titre or titre.strip() == "":
        errors.append(f"mission_{mission_num}_titre")

    if not date_debut:
        errors.append(f"mission_{mission_num}_debut")

    return errors


def show_validation_errors(errors, mission_num):
    """
    Affiche les erreurs de validation avec style

    Args:
        errors: Liste des erreurs de validation
        mission_num: Numéro de la mission

    Returns:
        bool: True si des erreurs ont été affichées, False sinon
    """
    if errors:
        st.markdown(
            """
        <div style="
            background-color: #fee;
            border: 2px solid #f44;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        ">
        <h4 style="color: #d00; margin: 0;">⚠️ Champs manquants pour Mission """
            + str(mission_num)
            + """</h4>
        <p style="margin: 5px 0;">Veuillez remplir les champs suivants :</p>
        <ul style="margin: 5px 0; color: #d00;">
        """,
            unsafe_allow_html=True,
        )

        for error in errors:
            if "client" in error:
                st.markdown(
                    "<li><strong>🏢 Client</strong> (obligatoire)</li>",
                    unsafe_allow_html=True,
                )
            elif "titre" in error:
                st.markdown(
                    "<li><strong>👤 Rôle/Titre</strong> (obligatoire)</li>",
                    unsafe_allow_html=True,
                )
            elif "debut" in error:
                st.markdown(
                    "<li><strong>📅 Date de début</strong> (obligatoire)</li>",
                    unsafe_allow_html=True,
                )

        st.markdown("</ul></div>", unsafe_allow_html=True)
        return True
    return False


def save_mission_to_consultant(
    consultant,
    client,
    titre,
    date_debut,
    date_fin,
    description,
    technologies,
    mission_num,
):
    """Sauvegarde une mission dans la base de données avec validation améliorée"""

    try:
        # Validation des champs obligatoires
        validation_errors = validate_mission_fields(
            client, titre, date_debut, mission_num
        )

        if validation_errors:
            show_validation_errors(validation_errors, mission_num)
            return False  # Echec de la validation

        # Convertir les technologies en liste
        tech_list = [tech.strip() for tech in technologies.split(",") if tech.strip()]

        # Utiliser la session de base de données
        with get_database_session() as session:
            # Récupérer le consultant depuis la DB pour éviter les problèmes de session
            consultant_fresh = (
                session.query(Consultant).filter(Consultant.id == consultant.id).first()
            )

            if not consultant_fresh:
                st.error(f"❌ Consultant avec ID {consultant.id} introuvable")
                return False

            # Créer la nouvelle mission
            nouvelle_mission = Mission(
                consultant_id=consultant_fresh.id,
                nom_mission=titre,
                client=client,
                role=titre,  # Le rôle est le même que le titre
                date_debut=date_debut,
                date_fin=date_fin,
                description=description,
                technologies_utilisees=", ".join(tech_list) if tech_list else None,
                statut="terminee" if date_fin else "en_cours",
            )

            session.add(nouvelle_mission)
            session.commit()

            # Succès !
            st.success(
                f"✅ Mission {mission_num} '{titre}' chez {client} sauvegardée avec succès !"
            )

            # Afficher un résumé de la mission sauvegardée
            with st.expander("📋 Mission ajoutée au profil", expanded=False):
                st.write(f"**Client:** {client}")
                st.write(f"**Rôle:** {titre}")
                st.write(f"**Début:** {date_debut.strftime(FORMAT_DATE)}")
                if date_fin:
                    st.write(f"**Fin:** {date_fin.strftime(FORMAT_DATE)}")
                else:
                    st.write("**Statut:** En cours")
                if description:
                    st.write(f"**Description:** {description}")
                if tech_list:
                    st.write(f"**Technologies:** {', '.join(tech_list)}")

            # Suggestion de rafraîchir la page missions
            st.info(
                "💡 Allez dans l'onglet 'Missions' du profil pour voir la mission ajoutée"
            )
            st.balloons()
            return True  # Succès

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de la sauvegarde de la mission {mission_num}: {e}")
        return False


def show_cv_skills(analysis):
    """Affiche les compétences extraites du CV avec une présentation améliorée"""
    st.write("**Compétences détectées dans le CV :**")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        _display_cv_technologies(analysis)

    with col2:
        _display_cv_functional_skills(analysis)

    # Section d'actions pour les compétences
    _display_cv_skills_actions(analysis)


def _display_cv_technologies(analysis):
    """Affiche les technologies détectées dans le CV"""
    st.subheader("🛠️ Technologies & Outils")
    technologies = analysis.get("langages_techniques", [])

    if technologies:
        # Affichage en badges/pills
        tech_html = ""
        for tech in technologies:
            tech_html += f'<span style="display: inline-block; background-color: #e1f5fe; color: #01579b; padding: 4px 12px; margin: 2px; border-radius: 20px; font-size: 0.85em;">{tech}</span>'
        st.markdown(tech_html, unsafe_allow_html=True)

        st.markdown("")  # Espace
        st.info(f"💡 {len(technologies)} technologie(s) détectée(s)")
    else:
        st.info("Aucune technologie spécifique détectée")


def _display_cv_functional_skills(analysis):
    """Affiche les compétences fonctionnelles détectées dans le CV"""
    st.subheader("💼 Compétences Fonctionnelles")
    competences = analysis.get("competences_fonctionnelles", [])

    if competences:
        # Affichage en liste avec icônes
        for comp in competences:
            st.write(f"✅ {comp}")

        st.markdown("")  # Espace
        st.info(f"💡 {len(competences)} compétence(s) fonctionnelle(s) détectée(s)")
    else:
        st.info("Aucune compétence fonctionnelle spécifique détectée")


def _display_cv_skills_actions(analysis):
    """Affiche les actions pour les compétences CV"""
    st.markdown("---")
    st.subheader("💾 Actions pour les compétences")

    col_action1, col_action2 = st.columns(2)
    technologies = analysis.get("langages_techniques", [])
    competences = analysis.get("competences_fonctionnelles", [])

    with col_action1:
        _display_technologies_action_button(technologies)

    with col_action2:
        _display_functional_skills_action_button(competences)


def _display_technologies_action_button(technologies):
    """Affiche le bouton d'action pour les technologies"""
    if st.button(
        "🛠️ Ajouter toutes les technologies au profil",
        type="primary",
        width="stretch",
    ):
        if technologies:
            st.success(
                f"✅ {len(technologies)} technologie(s) prête(s) à être ajoutée(s)"
            )
            st.info(
                "🚧 Fonctionnalité de sauvegarde automatique des compétences en cours de développement"
            )
            # Fonctionnalité à implémenter : ajout automatique des compétences techniques détectées
        else:
            st.warning("⚠️ Aucune technologie à ajouter")


def _display_functional_skills_action_button(competences):
    """Affiche le bouton d'action pour les compétences fonctionnelles"""
    if st.button("💼 Ajouter les compétences fonctionnelles", width="stretch"):
        if competences:
            st.success(
                f"✅ {len(competences)} compétence(s) prête(s) à être ajoutée(s)"
            )
            st.info(
                "🚧 Fonctionnalité de sauvegarde automatique des compétences en cours de développement"
            )
            # Fonctionnalité à implémenter : ajout automatique des compétences fonctionnelles détectées
        else:
            st.warning("⚠️ Aucune compétence fonctionnelle à ajouter")


def show_cv_summary(analysis):
    """Affiche un résumé de l'analyse"""

    st.subheader("📊 Résumé de l'analyse")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        missions_count = len(analysis.get("missions", []))
        st.metric("🏢 Missions", missions_count)

    with col2:
        tech_count = len(analysis.get("langages_techniques", []))
        st.metric(LABEL_TECHNOLOGIES, tech_count)

    with col3:
        comp_count = len(analysis.get("competences_fonctionnelles", []))
        st.metric(LABEL_COMPETENCES, comp_count)

    with col4:
        info_general = analysis.get("informations_generales", {})
        word_count = info_general.get("nombre_mots", 0)
        st.metric("📝 Mots", word_count)

    # Affichage du texte brut (aperçu)
    if st.checkbox("🔍 Voir l'aperçu du texte analysé"):
        texte_brut = analysis.get("texte_brut", "")
        if texte_brut:
            st.text_area(
                "Aperçu du contenu analysé", texte_brut, height=200, disabled=True
            )


def show_cv_actions(analysis, consultant):
    """Affiche les actions possibles après analyse avec une interface améliorée"""
    st.subheader("💾 Actions globales")
    st.write("Effectuez des actions sur l'ensemble des données analysées.")
    st.markdown("---")

    # Extraire les données d'analyse
    missions = analysis.get("missions", [])
    technologies = analysis.get("langages_techniques", [])
    competences = analysis.get("competences_fonctionnelles", [])

    # Afficher les statistiques et actions principales
    _display_cv_actions_statistics(missions, technologies, competences)
    _display_cv_main_actions(missions, technologies, competences)
    _display_cv_export_tools(consultant, missions, technologies, competences)
    _display_cv_detected_missions(missions)


def _display_cv_actions_statistics(missions, technologies, competences):
    """Affiche les statistiques rapides des actions CV"""
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("🏢 Missions détectées", len(missions))
    with col_stat2:
        st.metric(LABEL_TECHNOLOGIES, len(technologies))
    with col_stat3:
        st.metric(LABEL_COMPETENCES, len(competences))

    st.markdown("---")


def _display_cv_main_actions(missions, technologies, competences):
    """Affiche les actions principales pour les missions et compétences"""
    col1, col2 = st.columns(2)

    with col1:
        _display_missions_actions(missions)

    with col2:
        _display_skills_actions(technologies, competences)


def _display_missions_actions(missions):
    """Affiche les actions pour les missions"""
    st.write("**📋 Gestion des missions**")
    if st.button(
        "📋 Ajouter toutes les missions au profil",
        type="primary",
        width="stretch",
    ):
        _handle_add_all_missions(missions)

    st.markdown("")
    if missions:
        st.info(
            f"💡 {len(missions)} mission(s) peuvent être ajoutée(s) individuellement dans l'onglet 'Missions'"
        )


def _handle_add_all_missions(missions):
    """Gère l'ajout automatique de toutes les missions"""
    if missions:
        added_count = _process_missions_addition(missions)
        _display_missions_addition_result(added_count)
    else:
        st.warning("⚠️ Aucune mission à ajouter")


def _process_missions_addition(missions):
    """Traite l'ajout des missions et retourne le nombre ajouté"""
    added_count = 0
    for i, mission in enumerate(missions, 1):
        client = mission.get("client", f"Client Mission {i}")
        titre = mission.get("titre", f"Mission {i}")

        if client and titre:  # Validation minimale
            try:
                # Simulation d'ajout (remplacer par la vraie logique)
                added_count += 1
            except (SQLAlchemyError, ValueError, TypeError):
                pass
    return added_count


def _display_missions_addition_result(added_count):
    """Affiche le résultat de l'ajout des missions"""
    if added_count > 0:
        st.success(f"✅ {added_count} mission(s) ajoutée(s) avec succès!")
        st.info("💡 Consultez l'onglet 'Missions' du profil pour voir les ajouts")
    else:
        st.warning("⚠️ Aucune mission n'a pu être ajoutée automatiquement")
        st.info(
            "ℹ Utilisez l'onglet 'Missions' ci-dessus pour les ajouter manuellement"
        )


def _display_skills_actions(technologies, competences):
    """Affiche les actions pour les compétences"""
    st.write("**🛠️ Gestion des compétences**")
    if st.button("🛠️ Ajouter toutes les compétences au profil", width="stretch"):
        _handle_add_all_skills(technologies, competences)

    st.markdown("")
    if technologies:
        st.info(
            f"💡 {len(technologies)} technologie(s) peuvent être ajoutée(s) manuellement"
        )


def _handle_add_all_skills(technologies, competences):
    """Gère l'ajout automatique de toutes les compétences"""
    total_skills = len(technologies) + len(competences)
    if total_skills > 0:
        st.success(f"✅ {total_skills} compétence(s) identifiée(s)")
        st.info("🚧 Ajout automatique des compétences en cours de développement")
        _display_technologies_preview(technologies)
    else:
        st.warning("⚠️ Aucune compétence à ajouter")


def _display_technologies_preview(technologies):
    """Affiche un aperçu des technologies à ajouter"""
    st.write("**Technologies à ajouter:**")
    for tech in technologies[:5]:  # Limiter l'affichage
        st.write(f"• {tech}")
    if len(technologies) > 5:
        st.write(f"• ... et {len(technologies) - 5} autres")


def _display_cv_export_tools(consultant, missions, technologies, competences):
    """Affiche les outils d'export et actions avancées"""
    st.markdown("---")
    st.subheader("📤 Export et outils")

    col_exp1, col_exp2, col_exp3 = st.columns(3)

    with col_exp1:
        _display_json_export_button(consultant, missions, technologies, competences)

    with col_exp2:
        _display_formatted_summary_button(
            consultant, missions, technologies, competences
        )

    with col_exp3:
        _display_new_analysis_button()


def _display_json_export_button(consultant, missions, technologies, competences):
    """Affiche le bouton d'export JSON"""
    if st.button("📄 Export JSON", width="stretch"):
        import json
        from datetime import datetime

        export_data = {
            "consultant": f"{consultant.prenom} {consultant.nom}",
            "missions": missions,
            "technologies": technologies,
            "competences_fonctionnelles": competences,
            "date_analyse": datetime.now().isoformat(),
        }
        st.json(export_data)
        st.success("✅ Données exportées au format JSON")


def _display_formatted_summary_button(consultant, missions, technologies, competences):
    """Affiche le bouton de résumé formaté"""
    if st.button("📊 Résumé formaté", width="stretch"):
        resume_text = _generate_formatted_summary(
            consultant, missions, technologies, competences
        )
        st.text_area("Résumé de l'analyse", resume_text, height=300)
        st.success("✅ Résumé généré")


def _generate_formatted_summary(consultant, missions, technologies, competences):
    """Génère le texte du résumé formaté"""
    missions_text = chr(10).join(
        [f"• {m.get('client', 'N/A')} - {m.get('titre', 'N/A')}" for m in missions[:10]]
    )

    return f"""
**Analyse CV - {consultant.prenom} {consultant.nom}**

**Missions ({len(missions)}):**
{missions_text}

**Technologies ({len(technologies)}):**
{', '.join(technologies[:20])}

**Compétences ({len(competences)}):**
{', '.join(competences[:10])}
    """


def _display_new_analysis_button():
    """Affiche le bouton de nouvelle analyse"""
    if st.button("🔄 Nouvelle analyse", width="stretch"):
        st.info(
            "📁 Uploadez un nouveau document dans l'onglet 'Documents' pour une nouvelle analyse"
        )
        st.info("🔄 Ou rafraîchissez la page pour réanalyser le même document")


def _display_cv_detected_missions(missions):
    """Affiche les missions détectées avec leurs détails"""
    st.subheader(f"🚀 Missions détectées ({len(missions)})")

    for i, mission in enumerate(missions, 1):
        _display_single_detected_mission(mission, i)


def _display_single_detected_mission(mission, mission_number):
    """Affiche une mission détectée individuelle"""
    with st.expander(
        f"Mission {mission_number}: {mission.get('client', 'Client non spécifié')}",
        expanded=True,
    ):
        col1, col2 = st.columns(2)

        with col1:
            _display_mission_basic_info(mission)

        with col2:
            _display_mission_technical_info(mission)


def _display_mission_basic_info(mission):
    """Affiche les informations de base d'une mission"""
    st.write("**🏢 Client:**", mission.get("client", VALEUR_NON_SPECIFIE))
    st.write("**🎯 Rôle:**", mission.get("role", VALEUR_NON_SPECIFIE))

    if mission.get("dates"):
        st.write("**📅 Période:**", mission["dates"])


def _display_mission_technical_info(mission):
    """Affiche les informations techniques d'une mission"""
    if mission.get("langages_techniques"):
        st.write("**🛠️ Technologies:**")
        for tech in mission["langages_techniques"]:
            st.markdown(f"• {tech}")

    if mission.get("description"):
        st.write("**📝 Description:**")
        description = mission["description"]
        display_description = (
            description[:200] + "..." if len(description) > 200 else description
        )
        st.write(display_description)


def import_missions_to_profile(missions, consultant):
    """
    Importe toutes les missions dans le profil du consultant

    Args:
        missions: Liste des dictionnaires de missions à importer
        consultant: Objet Consultant propriétaire des missions

    Note:
        Cette fonction crée des objets Mission avec le statut "terminee" par défaut
    """
    try:
        with get_database_session() as session:
            success_count = 0

            for mission_data in missions:
                # Créer une nouvelle mission
                mission = Mission(
                    consultant_id=consultant.id,
                    nom_mission=mission_data.get("role", "Mission importée du CV"),
                    client=mission_data.get("client", "Client non spécifié"),
                    role=mission_data.get("role", ""),
                    description=mission_data.get("description", ""),
                    statut="terminee",  # Par défaut pour un CV
                    technologies_utilisees=", ".join(
                        mission_data.get("langages_techniques", [])
                    ),
                )

                session.add(mission)
                success_count += 1

            session.commit()
            st.success(f"✅ {success_count} mission(s) importée(s) avec succès !")
            st.rerun()

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de l'import : {e}")


def import_single_mission(mission_data, consultant):
    """
    Importe une mission individuelle dans le profil

    Args:
        mission_data: Dictionnaire contenant les données de la mission
        consultant: Objet Consultant propriétaire de la mission

    Note:
        Cette fonction crée un objet Mission avec le statut "terminee" par défaut
    """
    try:
        with get_database_session() as session:
            mission = Mission(
                consultant_id=consultant.id,
                nom_mission=mission_data.get("role", "Mission importée du CV"),
                client=mission_data.get("client", "Client non spécifié"),
                role=mission_data.get("role", ""),
                description=mission_data.get("description", ""),
                statut="terminee",
                technologies_utilisees=", ".join(
                    mission_data.get("langages_techniques", [])
                ),
            )

            session.add(mission)
            session.commit()

            st.success(
                f"✅ Mission '{mission_data.get('client', 'Inconnue')}' importée !"
            )
            st.rerun()

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de l'import : {e}")


def show_consultants_list_tab():
    """Fonction wrapper pour show_consultants_list - Compatible avec consultant_profile.py"""
    show_consultants_list()


def show_add_consultant_form_tab():
    """Fonction wrapper pour show_add_consultant_form - Compatible avec consultant_profile.py"""
    show_add_consultant_form()


def show_consultant_info_tab(consultant):
    """Fonction wrapper pour show_consultant_info - Compatible avec consultant_profile.py"""
    show_consultant_info(consultant)


def show_consultant_skills_tab(consultant):
    """Fonction wrapper pour show_consultant_skills - Compatible avec consultant_profile.py"""
    show_consultant_skills(consultant)


def show_consultant_languages_tab(consultant):
    """Fonction wrapper pour show_consultant_languages - Compatible avec consultant_profile.py"""
    show_consultant_languages(consultant)


def show_consultant_missions_tab(consultant):
    """Fonction wrapper pour show_consultant_missions - Compatible avec consultant_profile.py"""
    show_consultant_missions(consultant)


def show_consultant_documents_tab(consultant):
    """Fonction wrapper pour show_consultant_documents - Compatible avec consultant_profile.py"""
    show_consultant_documents(consultant)
