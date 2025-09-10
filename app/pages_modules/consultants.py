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
            show_cv_summary(analysis, consultant)

        with tab4:
            show_cv_actions(analysis, consultant)

        st.markdown("</div>", unsafe_allow_html=True)


def show_consultant_profile():
    """Affiche le profil détaillé d'un consultant avec gestion d'erreurs améliorée"""

    consultant_id = st.session_state.view_consultant_profile

    try:
        # Charger le consultant avec toutes les relations nécessaires dans la même
        # session
        with get_database_session() as session:
            consultant = (
                session.query(Consultant)
                .options(joinedload(Consultant.practice))
                .filter(Consultant.id == consultant_id)
                .first()
            )

            if not consultant:
                st.error("❌ Consultant introuvable")
                if st.button("← Retour à la liste", key="back_to_list_error"):
                    del st.session_state.view_consultant_profile
                    st.rerun()
                return

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

        # En-tête avec bouton retour
        col1, col2 = st.columns([6, 1])

        with col1:
            st.title(
                "👤 Profil de "
                + consultant_data["prenom"]
                + " "
                + consultant_data["nom"]
            )

        with col2:
            if st.button("← Retour", key="back_to_list"):
                del st.session_state.view_consultant_profile
                st.rerun()

        st.markdown("---")

        # Métriques principales
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
                show_consultant_info(consultant_obj)

            with tab2:
                show_consultant_skills(consultant_obj)

            with tab3:
                show_consultant_languages(consultant_obj)

            with tab4:
                show_consultant_missions(consultant_obj)

            with tab5:
                show_consultant_documents(consultant_obj)

    except (AttributeError, TypeError, ValueError, SQLAlchemyError, Exception) as e:
        st.error("❌ Erreur lors du chargement du profil consultant: " + str(e))
        st.code(str(e))

        # Bouton manuel pour retourner à la liste
        if st.button("← Retour à la liste", key="back_to_list_exception"):
            if hasattr(st.session_state, 'view_consultant_profile'):
                del st.session_state.view_consultant_profile
            st.rerun()


def show_consultant_info(consultant):
    """Affiche et permet la modification des informations du consultant"""

    st.subheader("📋 Informations personnelles")

    from sqlalchemy.orm import joinedload

    from database.models import Consultant
    from database.models import Practice

    # Recharger le consultant avec la relation practice pour éviter
    # DetachedInstanceError
    with get_database_session() as session:
        consultant_db = (
            session.query(Consultant)
            .options(joinedload(Consultant.practice))
            .options(joinedload(Consultant.business_manager_gestions))
            .filter(Consultant.id == consultant.id)
            .first()
        )
        practices = session.query(Practice).filter(Practice.actif).all()

        # Charger le BM actuel dans la même session pour éviter les erreurs de session
        bm_actuel = consultant_db.business_manager_actuel
        bm_nom_complet = bm_actuel.nom_complet if bm_actuel else None
        bm_email = bm_actuel.email if bm_actuel else None
    practice_options = {p.nom: p.id for p in practices}
    current_practice_id = (
        consultant_db.practice_id if hasattr(consultant_db, "practice_id") else None
    )

    # Formulaire principal infos consultant
    with st.form(f"edit_consultant_{consultant.id}"):
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
                "🏢 Practice",
                options=["Non affecté"] + list(practice_options.keys()),
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
                "✅ Disponible", value=consultant_db.disponibilite
            )

        # Notes
        notes = st.text_area(
            "📝 Notes",
            value=consultant_db.notes or "",
            height=100,
            placeholder="Notes sur le consultant...",
        )

        # Section historique société (nouveaux champs V1.2)
        st.markdown("---")
        st.markdown("### 🏢 Historique Société")

        col3, col4 = st.columns(2)

        with col3:
            societe = st.selectbox(
                "🏢 Société",
                options=["Quanteam", "Asigma"],
                index=0 if (consultant_db.societe or "Quanteam") == "Quanteam" else 1,
            )
            date_entree = st.date_input(
                "📅 Date d'entrée société",
                value=consultant_db.date_entree_societe,
                help="Date d'entrée dans la société",
            )

        with col4:
            date_sortie = st.date_input(
                "📅 Date de sortie société (optionnel)",
                value=consultant_db.date_sortie_societe,
                help="Laissez vide si encore en poste",
            )
            date_premiere_mission = st.date_input(
                "🚀 Date première mission (optionnel)",
                value=consultant_db.date_premiere_mission,
                help="Date de début de la première mission",
            )

        # Section profil professionnel (nouveaux champs V1.2.1)
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
                grade_options.index(current_grade)
                if current_grade in grade_options
                else 0
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

        st.markdown("---")

        # Affichage de l'expérience calculée
        if consultant_db.date_premiere_mission:
            try:
                experience = consultant_db.experience_annees
                st.info("📊 **Expérience calculée :** " + str(experience) + " années")
            except BaseException:
                st.info("📊 **Expérience :** Calcul en cours...")
        else:
            st.info(
                "📊 **Expérience :** Non calculée (date première mission manquante)"
            )

        # Statut société
        try:
            statut = consultant_db.statut_societe
            if statut == "En poste":
                st.success("✅ **Statut :** " + str(statut))
            elif statut == "Départ prévu":
                st.warning("⚠️ **Statut :** " + str(statut))
            else:
                st.error("❌ **Statut :** " + str(statut))
        except BaseException:
            st.info("📊 **Statut :** En cours de calcul...")

        # Bouton de sauvegarde
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submitted = st.form_submit_button(
                "💾 Sauvegarder", type="primary", use_container_width=True
            )

        if submitted:
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Vérifier l'unicité de l'email
                existing = ConsultantService.get_consultant_by_email(email)
                if existing and existing.id != consultant.id:
                    st.error(
                        "❌ Un consultant avec l'email " + email + " existe déjà !"
                    )
                else:
                    try:
                        update_data = {
                            "prenom": prenom.strip(),
                            "nom": nom.strip(),
                            "email": email.strip().lower(),
                            "telephone": (telephone.strip() if telephone else None),
                            "salaire_actuel": salaire,
                            "disponibilite": disponibilite,
                            "notes": notes.strip() if notes else None,
                            "practice_id": selected_practice_id,
                            # Nouveaux champs V1.2
                            "societe": societe,
                            "date_entree_societe": date_entree,
                            "date_sortie_societe": date_sortie if date_sortie else None,
                            "date_premiere_mission": (
                                date_premiere_mission if date_premiere_mission else None
                            ),
                            # Nouveaux champs V1.2.1
                            "grade": grade,
                            "type_contrat": type_contrat,
                        }

                        if ConsultantService.update_consultant(
                            consultant.id, update_data
                        ):
                            st.success(f"✅ {prenom} {nom} modifié avec succès !")
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la modification")

                    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
                        st.error("❌ Erreur: " + str(e))

    # Historique des salaires (hors formulaire principal)
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
        # Trier par date_debut croissante pour le graphique
        salaires_sorted = sorted(salaires, key=lambda s: s.date_debut)
        # Affichage textuel (salaire le plus récent en haut)
        for salaire in salaires:
            st.write(
                f"- **{salaire.salaire:,.0f} €** du {salaire.date_debut.strftime('%d/%m/%Y')} "
                + (
                    f"au {salaire.date_fin.strftime('%d/%m/%Y')}"
                    if salaire.date_fin
                    else "(en cours)"
                )
                + (f" — {salaire.commentaire}" if salaire.commentaire else "")
            )
        # Met à jour le salaire actuel du consultant si besoin
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
            except (SQLAlchemyError, ValueError, TypeError) as e:
                st.warning(f"⚠️ Erreur lors de la mise à jour du salaire: {e}")
                # Ne pas interrompre le processus pour une erreur mineure
        # Affichage du graphique
        import plotly.graph_objects as go

        if st.button(
            "📈 Afficher l'évolution des salaires",
            key=f"show_salary_graph_{
                consultant.id}",
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
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune évolution de salaire enregistrée.")

    # Ajout d'une évolution de salaire (hors formulaire principal)
    with st.expander("➕ Ajouter une évolution de salaire"):
        with st.form(f"add_salary_form_{consultant.id}"):
            new_salaire = st.number_input(
                "Nouveau salaire (€)",
                min_value=0,
                step=1000,
                key=f"salaire_{
                    consultant.id}",
            )
            new_date_debut = st.date_input(
                "Date de début",
                value=datetime.today(),
                key=f"date_debut_{
                    consultant.id}",
            )
            new_commentaire = st.text_input(
                "Commentaire",
                value="",
                key=f"commentaire_{
                    consultant.id}",
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
                except (SQLAlchemyError, ValueError, TypeError) as e:
                    st.error(f"❌ Erreur lors de l'ajout : {e}")


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
        # Récupérer les compétences techniques enregistrées
        with get_database_session() as session:
            competences_tech = (
                session.query(ConsultantCompetence, Competence)
                .join(Competence)
                .filter(
                    ConsultantCompetence.consultant_id == consultant.id,
                    Competence.type_competence == "technique",
                )
                .all()
            )

            # Récupérer aussi les technologies des missions
            missions = (
                session.query(Mission)
                .filter(Mission.consultant_id == consultant.id)
                .all()
            )

        # Technologies des missions
        technologies_missions = set()
        for mission in missions:
            if mission.technologies_utilisees:
                mission_techs = [
                    tech.strip()
                    for tech in mission.technologies_utilisees.split(",")
                    if tech.strip()
                ]
                technologies_missions.update(mission_techs)

        # Affichage des compétences enregistrées
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

        # Technologies extraites des missions
        if technologies_missions:
            st.write("**🏷️ Technologies des missions**")

            cols = st.columns(4)
            tech_list = sorted(list(technologies_missions))

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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors du chargement des compétences techniques: {e}")


def _show_functional_skills(consultant):
    """Affiche les compétences fonctionnelles du consultant"""
    try:
        with get_database_session() as session:
            competences_func = (
                session.query(ConsultantCompetence, Competence)
                .join(Competence)
                .filter(
                    ConsultantCompetence.consultant_id == consultant.id,
                    Competence.type_competence == "fonctionnelle",
                )
                .order_by(Competence.categorie, Competence.nom)
                .all()
            )

        if competences_func:
            st.write("**🏦 Compétences fonctionnelles enregistrées**")

            # Grouper par catégorie
            categories = {}
            for consultant_comp, competence in competences_func:
                if competence.categorie not in categories:
                    categories[competence.categorie] = []
                categories[competence.categorie].append((consultant_comp, competence))

            for categorie, comps in categories.items():
                with st.expander(f"📂 {categorie} ({len(comps)} compétences)"):
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

            # Métriques
            total_competences = len(competences_func)
            st.metric("🏦 Total compétences fonctionnelles", total_competences)
        else:
            st.info("📝 Aucune compétence fonctionnelle enregistrée")
            st.write(
                "Utilisez l'onglet **'Ajouter Compétences'** pour ajouter des compétences bancaires/assurance."
            )

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors du chargement des compétences fonctionnelles: {e}")


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

    # Sélection de la catégorie
    categories_tech = list(COMPETENCES_TECHNIQUES.keys())
    categorie = st.selectbox("📂 Catégorie technique", categories_tech)

    # Sélection de la compétence
    competences_list = COMPETENCES_TECHNIQUES[categorie]
    competence_nom = st.selectbox("🛠️ Compétence", competences_list)

    # Niveau et expérience
    col1, col2 = st.columns(2)
    with col1:
        niveau = st.selectbox(
            "📊 Niveau de maîtrise", ["Débutant", "Intermédiaire", "Avancé", "Expert"]
        )

    with col2:
        experience = st.number_input(
            "⏱️ Années d'expérience", min_value=0.0, max_value=50.0, value=1.0, step=0.5
        )

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

    # Sélection de la catégorie
    categories_func = list(COMPETENCES_FONCTIONNELLES.keys())
    categorie = st.selectbox("📂 Catégorie fonctionnelle", categories_func)

    # Sélection de la compétence
    competences_list = COMPETENCES_FONCTIONNELLES[categorie]
    competence_nom = st.selectbox("🏦 Compétence", competences_list)

    # Niveau et expérience
    col1, col2 = st.columns(2)
    with col1:
        niveau = st.selectbox(
            "📊 Niveau de maîtrise", ["Débutant", "Intermédiaire", "Avancé", "Expert"]
        )

    with col2:
        experience = st.number_input(
            "⏱️ Années d'expérience", min_value=0.0, max_value=50.0, value=1.0, step=0.5
        )

    # Champs optionnels
    certifications = st.text_input("🏆 Certifications (optionnel)")
    projets = st.text_area("� Projets/missions réalisés (optionnel)")

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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de l'ajout: {e}")


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
            else:
                st.error("❌ Compétence non trouvée")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")


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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de l'affichage des langues: {e}")


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
                    langue for langue in langues_disponibles if langue.id not in langues_assignees
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

        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            st.error(f"❌ Erreur lors de la préparation du formulaire: {e}")


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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de l'ajout de la langue: {e}")


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
            else:
                st.error("❌ Langue non trouvée")

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")


def show_consultant_missions(consultant):
    """Affiche l'historique des missions du consultant avec édition"""

    st.subheader("🚀 Historique des missions")

    try:
        with get_database_session() as session:
            missions = (
                session.query(Mission)
                .filter(Mission.consultant_id == consultant.id)
                .order_by(Mission.date_debut.desc())
                .all()
            )

        if missions:
            # Métriques des missions
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

            # Onglets pour organiser les fonctionnalités
            tab1, tab2 = st.tabs(["📋 Missions existantes", "➕ Ajouter une mission"])

            with tab1:
                # Mode édition
                edit_mode = st.checkbox("✏️ Mode édition", key="edit_mode_missions")

                if edit_mode:
                    st.info(
                        "📝 Mode édition activé - Cliquez sur une mission pour la modifier"
                    )

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

            with tab2:
                show_add_mission_form(consultant)
        else:
            st.info("📝 Aucune mission enregistrée pour ce consultant")
            show_add_mission_form(consultant)

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors du chargement des missions: {e}")


def show_mission_readonly(mission):
    """Affiche les détails d'une mission en lecture seule"""
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**🏢 Client**: {mission.client}")
        st.write("**👤 Rôle**: " + (mission.role or "Non spécifié"))
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
                "📊 Statut",
                ["en_cours", "terminee", "en_pause"],
                index=(
                    ["en_cours", "terminee", "en_pause"].index(mission.statut)
                    if mission.statut in ["en_cours", "terminee", "en_pause"]
                    else 0
                ),
                key=f"edit_statut_{mission.id}",
            )

        technologies = st.text_input(
            "🛠️ Technologies",
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
            statut = st.selectbox("📊 Statut", ["en_cours", "terminee", "en_pause"])

        technologies_str = st.text_input(
            "🛠️ Technologies", placeholder="Ex: Python, Django, PostgreSQL"
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
    """Affiche la liste des consultants avec interactions optimisée"""

    # Champ de recherche en temps réel
    search_term = st.text_input(
        "🔍 Rechercher un consultant",
        placeholder="Tapez un prénom, nom ou email pour filtrer...",
        help="La liste se filtre automatiquement pendant que vous tapez",
        key="consultant_search",
    )

    try:
        # Utiliser les nouvelles méthodes optimisées
        if search_term and search_term.strip():
            consultants = ConsultantService.search_consultants_optimized(
                search_term.strip()
            )
            if consultants:
                st.info(
                    "🔍 "
                    + str(len(consultants))
                    + " consultant(s) trouvé(s) pour '"
                    + search_term
                    + "'"
                )
            else:
                st.warning("❌ Aucun consultant trouvé pour '" + search_term + "'")
        else:
            # Utiliser la méthode optimisée qui récupère tout en une requête
            consultants = ConsultantService.get_all_consultants_with_stats()

        if consultants:
            # Les données sont déjà préparées par le service optimisé
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

            # Afficher le tableau avec sélection
            df = pd.DataFrame(consultants_data)

            event = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
            )

            # Actions sur sélection
            if event.selection.rows:
                selected_row = event.selection.rows[0]
                selected_id = consultants_data[selected_row]["ID"]
                selected_name = f"{
                    consultants_data[selected_row]['Prénom']} {
                    consultants_data[selected_row]['Nom']}"

                st.success(f"✅ Consultant sélectionné : **{selected_name}**")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(
                        "👁️ Voir le profil",
                        type="primary",
                        use_container_width=True,
                        key=f"view_{selected_id}",
                    ):
                        st.session_state.view_consultant_profile = selected_id
                        st.rerun()

                with col2:
                    if st.button(
                        "✏️ Modifier",
                        use_container_width=True,
                        key=f"edit_{selected_id}",
                    ):
                        st.session_state.view_consultant_profile = selected_id
                        st.rerun()

                with col3:
                    if st.button(
                        "🗑️ Supprimer",
                        use_container_width=True,
                        key=f"delete_{selected_id}",
                    ):
                        if ConsultantService.delete_consultant(selected_id):
                            st.success("✅ Consultant supprimé !")
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la suppression")

            # Métriques générales
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("👥 Total consultants", len(consultants))

            with col2:
                disponibles = len(
                    [c for c in consultants if c.get("disponibilite", False)]
                )
                st.metric("✅ Disponibles", disponibles)

            with col3:
                occupes = len(consultants) - disponibles
                st.metric("🔴 Occupés", occupes)

            with col4:
                if len(consultants) > 0:
                    salaire_moyen = (
                        sum(c.get("salaire_actuel", 0) or 0 for c in consultants)
                        / len(consultants)
                    )
                else:
                    salaire_moyen = 0
                st.metric("💰 Salaire moyen", f"{salaire_moyen:,.0f}€")

        else:
            st.info("📝 Aucun consultant enregistré")
            st.markdown(
                "💡 Utilisez l'onglet **Ajouter un consultant** pour créer votre premier profil"
            )

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors du chargement de la liste: {e}")


def show_add_consultant_form():
    """Formulaire d'ajout d'un nouveau consultant"""

    st.subheader("➕ Ajouter un nouveau consultant")

    from database.models import Practice

    with get_database_session() as session:
        practices = session.query(Practice).filter(Practice.actif).all()
    practice_options = {p.nom: p.id for p in practices}

    with st.form("add_consultant_form"):
        col1, col2 = st.columns(2)

        with col1:
            prenom = st.text_input("👤 Prénom *", placeholder="Ex: Jean")
            email = st.text_input("📧 Email *", placeholder="jean.dupont@example.com")
            salaire = st.number_input(
                "💰 Salaire annuel (€)", min_value=0, value=45000, step=1000
            )
            # Sélection de la practice
            practice_label = st.selectbox(
                "🏢 Practice",
                options=["Non affecté"] + list(practice_options.keys()),
                index=0,
            )
            selected_practice_id = practice_options.get(practice_label)

        with col2:
            nom = st.text_input("👤 Nom *", placeholder="Ex: Dupont")
            telephone = st.text_input("📞 Téléphone", placeholder="01.23.45.67.89")
            disponibilite = st.checkbox("✅ Disponible", value=True)

        # Section historique société (nouveaux champs V1.2)
        st.markdown("---")
        st.markdown("### 🏢 Historique Société")

        col3, col4 = st.columns(2)

        with col3:
            societe = st.selectbox(
                "🏢 Société", options=["Quanteam", "Asigma"], index=0
            )
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

        # Section profil professionnel (nouveaux champs V1.2.1)
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

        # Notes optionnelles
        notes = st.text_area(
            "📝 Notes (optionnel)",
            height=100,
            placeholder="Notes sur le consultant...",
        )

        # Bouton de création
        submitted = st.form_submit_button(
            "➕ Créer le consultant", type="primary", use_container_width=True
        )

        if submitted:
            if not prenom or not nom or not email:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Vérifier l'unicité de l'email
                existing = ConsultantService.get_consultant_by_email(email)
                if existing:
                    st.error(
                        "❌ Un consultant avec l'email " + email + " existe déjà !"
                    )
                else:
                    try:
                        consultant_data = {
                            "prenom": prenom.strip(),
                            "nom": nom.strip(),
                            "email": email.strip().lower(),
                            "telephone": (telephone.strip() if telephone else None),
                            "salaire": salaire,
                            "disponible": disponibilite,
                            "notes": notes.strip() if notes else None,
                            "practice_id": selected_practice_id,
                            # Nouveaux champs V1.2
                            "societe": societe,
                            "date_entree_societe": date_entree,
                            "date_sortie_societe": date_sortie if date_sortie else None,
                            "date_premiere_mission": (
                                date_premiere_mission if date_premiere_mission else None
                            ),
                            # Nouveaux champs V1.2.1
                            "grade": grade,
                            "type_contrat": type_contrat,
                        }

                        if ConsultantService.create_consultant(consultant_data):
                            st.success(f"✅ {prenom} {nom} créé avec succès !")
                            st.balloons()  # Animation de succès
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la création")

                    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
                        st.error(f"❌ Erreur lors de la création: {e}")


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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de la sauvegarde: {e}")


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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")


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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        st.error(f"❌ Erreur lors de l'ajout: {e}")


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
            st.metric("📊 Taille", size_display)

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


def save_consultant_document(uploaded_file, consultant, document_type, description):
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
        safe_name = f"{
            consultant.prenom}_{
            consultant.nom}_{document_type}_{timestamp}.{file_extension}"
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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de la sauvegarde: {e}")


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
            safe_name = f"{
                consultant.id}_{
                consultant.prenom}_{
                consultant.nom}_{name}_{timestamp}.{extension}"
        else:
            # Pas d'extension
            safe_name = f"{
                consultant.id}_{
                consultant.prenom}_{
                consultant.nom}_{original_name}_{timestamp}"

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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de la sauvegarde: {e}")


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
                st.write(f"� **{display_name}**")
                st.caption(
                    f"{doc_type} • {size_display} • {
                        modified_time.strftime('%d/%m/%Y')}"
                )

            with col2:
                # Bouton téléchargement direct
                download_document_direct(file_path, consultant, display_name)

            with col3:
                if st.button(
                    "�️", key=f"preview_{file_path.name}", help="Prévisualiser"
                ):
                    preview_document(file_path, consultant)

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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de l'affichage des documents: {e}")


def delete_consultant_document(file_path):
    """Supprime un document du consultant"""

    try:
        if file_path.exists():
            file_path.unlink()
            st.success("✅ Document supprimé avec succès")
            st.rerun()
        else:
            st.error("❌ Fichier introuvable")
    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")


def detect_document_type(filename):
    """Détecte automatiquement le type de document basé sur le nom de fichier"""

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
    """Retourne le type MIME basé sur l'extension du fichier"""

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
    """Extrait le nom original du fichier en enlevant les préfixes consultant"""

    # Format attendu: ID_Prenom_Nom_FichierOriginal_Timestamp.extension
    parts = full_filename.split("_")

    if len(parts) >= 4:
        # Identifier les parties : ID, Prénom, Nom, puis le reste
        id_part = parts[0]  # noqa: F841
        prenom_part = parts[1]  # noqa: F841
        nom_part = parts[2]  # noqa: F841

        # Le reste après Nom
        remaining_parts = parts[3:]

        # Chercher le timestamp (format YYYYMMDD) dans les parties restantes
        original_parts = []
        timestamp_found = False

        for i, part in enumerate(remaining_parts):
            # Vérifier si cette partie ressemble à un timestamp YYYYMMDD
            if len(part) == 8 and part.isdigit() and part.startswith(('20', '19')):
                # C'est probablement un timestamp, arrêter ici
                original_parts = remaining_parts[:i]
                timestamp_found = True
                break

        if not timestamp_found:
            # Si pas de timestamp trouvé, prendre tout sauf la dernière partie (qui peut contenir l'extension)
            if len(remaining_parts) > 1:
                original_parts = remaining_parts[:-1]
            else:
                original_parts = remaining_parts

        if original_parts:
            original_name = "_".join(original_parts)

            # Gérer l'extension
            last_part = remaining_parts[-1] if remaining_parts else ""
            if "." in last_part:
                # La dernière partie contient l'extension
                name_without_ext = last_part.split(".")[0]
                extension = last_part.split(".")[-1]

                # Si on a trouvé un timestamp, la dernière partie devrait être le timestamp.extension
                # Donc on utilise les original_parts pour construire le nom
                if timestamp_found:
                    # Les original_parts contiennent le nom original sans extension
                    # On ajoute l'extension du fichier complet
                    if "." in full_filename:
                        extension = full_filename.split(".")[-1]
                        original_name = f"{original_name}.{extension}"
                else:
                    # Pas de timestamp trouvé, utiliser la logique normale
                    if not original_name:
                        original_name = name_without_ext
                    original_name = f"{original_name}.{extension}"
            elif "." not in original_name and "." in full_filename:
                # Chercher l'extension dans le nom complet
                if "." in full_filename:
                    extension = full_filename.split(".")[-1]
                    original_name = f"{original_name}.{extension}"

            return original_name

    # Si le format n'est pas reconnu, retourner le nom complet
    return full_filename


def download_document_direct(file_path, consultant, display_name):
    """Bouton de téléchargement direct"""

    try:
        if not file_path.exists():
            st.error("❌ Fichier introuvable")
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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur: {e}")


def download_document(file_path, consultant):
    """Prépare le téléchargement d'un document"""

    try:
        if not file_path.exists():
            st.error("❌ Fichier introuvable")
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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors du téléchargement: {e}")


def preview_document(file_path, consultant):
    """Affiche un aperçu du document"""

    try:
        if not file_path.exists():
            st.error("❌ Fichier introuvable")
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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de l'aperçu: {e}")


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

    except (SQLAlchemyError, ValueError, TypeError, AttributeError, OSError) as e:
        st.error(f"❌ Erreur lors de l'aperçu PDF: {e}")
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
            st.metric("📊 Taille", size_display)
        with col2:
            modified_time = datetime.fromtimestamp(file_stats.st_mtime)
            st.metric("📅 Modifié", modified_time.strftime("%d/%m/%Y"))

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
            st.metric("📊 Taille", size_display)
        with col2:
            modified_time = datetime.fromtimestamp(file_stats.st_mtime)
            st.metric("📅 Modifié", modified_time.strftime("%d/%m/%Y"))

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

    # Utiliser explicitement toute la largeur disponible
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

    # En-tête avec métriques
    st.markdown(f"### 📋 {len(missions)} mission(s) détectée(s) dans le CV")

    # Bouton global en pleine largeur avec validation globale
    if st.button(
        "💾 Sauvegarder TOUTES les missions", type="primary", use_container_width=True
    ):
        # Validation globale de toutes les missions
        all_valid = True
        for i, mission in enumerate(missions, 1):
            client = mission.get("client", "")
            titre = mission.get("titre", "")

            if not client or not titre:
                all_valid = False
                st.error(f"❌ Mission {i}: Client et titre sont obligatoires")

        if all_valid:
            save_all_missions_to_consultant(missions, consultant)
        else:
            st.warning(
                "⚠️ Veuillez corriger les missions ci-dessous avant de sauvegarder toutes les missions."
            )
            st.info(
                "💡 Conseil: Utilisez les boutons de sauvegarde individuels pour voir les erreurs détaillées."
            )

    st.markdown("---")

    # Afficher chaque mission individuellement - PLEINE LARGEUR
    for i, mission in enumerate(missions, 1):
        # Container pleine largeur pour chaque mission
        with st.container():
            client_name = mission.get("client", "Client inconnu")
            st.markdown(f"### 🏢 Mission {i}: {client_name}")

            # Champs principaux - layout optimisé avec validation visuelle

            # Initialiser la validation dans session_state si nécessaire
            if f"validation_errors_{i}" not in st.session_state:
                st.session_state[f"validation_errors_{i}"] = []

            validation_errors = st.session_state.get(f"validation_errors_{i}", [])

            # Client avec validation visuelle
            client_error = f"mission_{i}_client" in validation_errors
            if client_error:
                st.markdown("**🚨 Client requis**", help="Ce champ est obligatoire")

            client = st.text_input(
                "🏢 Client *" + (" 🚨" if client_error else ""),
                value=mission.get("client", ""),
                key=f"mission_{i}_client",
                help="Nom du client pour cette mission (OBLIGATOIRE)",
                placeholder="Exemple: Société Générale, BNP Paribas...",
            )

            # Titre avec validation visuelle
            titre_error = f"mission_{i}_titre" in validation_errors
            if titre_error:
                st.markdown("**🚨 Rôle/Titre requis**", help="Ce champ est obligatoire")

            titre = st.text_input(
                "👤 Rôle/Titre *" + (" 🚨" if titre_error else ""),
                value=mission.get("titre", ""),
                key=f"mission_{i}_titre",
                help="Votre rôle ou titre dans cette mission (OBLIGATOIRE)",
                placeholder="Exemple: Développeur Full Stack, Consultant...",
            )

            # Dates côte à côte mais dans un layout flexible
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                date_error = f"mission_{i}_debut" in validation_errors
                if date_error:
                    st.markdown(
                        "**🚨 Date de début requise**", help="Ce champ est obligatoire"
                    )

                date_debut = st.date_input(
                    "📅 Date de début *" + (" 🚨" if date_error else ""),
                    value=None,
                    key=f"mission_{i}_debut",
                    help="Date de début de la mission (OBLIGATOIRE)",
                )
            with col_date2:
                date_fin = st.date_input(
                    "📅 Date de fin",
                    value=None,
                    key=f"mission_{i}_fin",
                    help="Date de fin (laisser vide si en cours)",
                )

            # Description en pleine largeur
            description = st.text_area(
                "📝 Description de la mission",
                value=mission.get("description", ""),
                height=120,
                key=f"mission_{i}_description",
                help="Description détaillée de vos activités et responsabilités",
            )

            # Technologies en pleine largeur
            technologies_text = ", ".join(mission.get("langages_techniques", []))
            technologies = st.text_area(
                "🛠️ Technologies et outils utilisés",
                value=technologies_text,
                height=80,
                key=f"mission_{i}_technologies",
                help="Technologies, langages, outils séparés par des virgules (ex: Python, React, AWS, Docker)",
            )

            # Bouton de sauvegarde en pleine largeur avec validation
            if st.button(
                f"💾 Sauvegarder Mission {i}",
                key=f"save_mission_{i}",
                type="primary",
                use_container_width=True,
                help="Ajouter cette mission au profil du consultant",
            ):
                # Validation avant sauvegarde
                validation_errors = validate_mission_fields(
                    client, titre, date_debut, i
                )
                st.session_state[f"validation_errors_{i}"] = validation_errors

                if validation_errors:
                    # Afficher les erreurs et rerun pour mettre à jour l'affichage
                    show_validation_errors(validation_errors, i)
                    st.rerun()
                else:
                    # Nettoyer les erreurs précédentes
                    st.session_state[f"validation_errors_{i}"] = []

                    # Sauvegarder la mission
                    success = save_mission_to_consultant(
                        consultant,
                        client,
                        titre,
                        date_debut,
                        date_fin,
                        description,
                        technologies,
                        i,
                    )

                    if success:
                        # Optionnel: nettoyer le formulaire après succès
                        st.success(
                            "Mission sauvegardée ! Vous pouvez maintenant remplir la mission suivante."
                        )

            # Afficher un aperçu rapide de ce qui sera sauvegardé
            if client and titre and date_debut:
                st.info(
                    f"✅ Prêt à sauvegarder: {titre} chez {client} (début: {
                        date_debut.strftime('%d/%m/%Y')})"
                )
            else:
                missing = []
                if not client:
                    missing.append("Client")
                if not titre:
                    missing.append("Rôle/Titre")
                if not date_debut:
                    missing.append("Date de début")
                st.warning(f"⚠️ Champs manquants: {', '.join(missing)}")

            # Séparateur entre les missions
            if i < len(missions):
                st.markdown("---")
                st.markdown("")  # Espace supplémentaire


def save_all_missions_to_consultant(missions, consultant):
    """Sauvegarde toutes les missions extraites du CV dans la base de données"""

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
    """Valide les champs d'une mission et retourne les erreurs"""
    errors = []

    if not client or client.strip() == "":
        errors.append(f"mission_{mission_num}_client")

    if not titre or titre.strip() == "":
        errors.append(f"mission_{mission_num}_titre")

    if not date_debut:
        errors.append(f"mission_{mission_num}_debut")

    return errors


def show_validation_errors(errors, mission_num):
    """Affiche les erreurs de validation avec style"""
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
                st.write(f"**Début:** {date_debut.strftime('%d/%m/%Y')}")
                if date_fin:
                    st.write(f"**Fin:** {date_fin.strftime('%d/%m/%Y')}")
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

    with col2:
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

    # Section d'actions pour les compétences
    st.markdown("---")
    st.subheader("💾 Actions pour les compétences")

    col_action1, col_action2 = st.columns(2)

    with col_action1:
        if st.button(
            "🛠️ Ajouter toutes les technologies au profil",
            type="primary",
            use_container_width=True,
        ):
            if technologies:
                st.success(
                    f"✅ {
                        len(technologies)} technologie(s) prête(s) à être ajoutée(s)"
                )
                st.info(
                    "🚧 Fonctionnalité de sauvegarde automatique des compétences en cours de développement"
                )
                # TODO: Implémenter l'ajout automatique des compétences
            else:
                st.warning("⚠️ Aucune technologie à ajouter")

    with col_action2:
        if st.button(
            "💼 Ajouter les compétences fonctionnelles", use_container_width=True
        ):
            if competences:
                st.success(
                    f"✅ {
                        len(competences)} compétence(s) prête(s) à être ajoutée(s)"
                )
                st.info(
                    "🚧 Fonctionnalité de sauvegarde automatique des compétences en cours de développement"
                )
                # TODO: Implémenter l'ajout automatique des compétences
            else:
                st.warning("⚠️ Aucune compétence fonctionnelle à ajouter")


def show_cv_summary(analysis, consultant):
    """Affiche un résumé de l'analyse"""

    st.subheader("📊 Résumé de l'analyse")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        missions_count = len(analysis.get("missions", []))
        st.metric("🏢 Missions", missions_count)

    with col2:
        tech_count = len(analysis.get("langages_techniques", []))
        st.metric("🛠️ Technologies", tech_count)

    with col3:
        comp_count = len(analysis.get("competences_fonctionnelles", []))
        st.metric("💼 Compétences", comp_count)

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

    # Statistiques rapides
    missions = analysis.get("missions", [])
    technologies = analysis.get("langages_techniques", [])
    competences = analysis.get("competences_fonctionnelles", [])

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("🏢 Missions détectées", len(missions))
    with col_stat2:
        st.metric("🛠️ Technologies", len(technologies))
    with col_stat3:
        st.metric("💼 Compétences", len(competences))

    st.markdown("---")

    # Actions principales
    col1, col2 = st.columns(2)

    with col1:
        st.write("**📋 Gestion des missions**")
        if st.button(
            "📋 Ajouter toutes les missions au profil",
            type="primary",
            use_container_width=True,
        ):
            if missions:
                added_count = 0
                for i, mission in enumerate(missions, 1):
                    # Logique d'ajout automatique simplifié
                    client = mission.get("client", f"Client Mission {i}")
                    titre = mission.get("titre", f"Mission {i}")

                    if client and titre:  # Validation minimale
                        try:
                            # Simulation d'ajout (remplacer par la vraie logique)
                            added_count += 1
                        except BaseException:
                            pass

                if added_count > 0:
                    st.success(f"✅ {added_count} mission(s) ajoutée(s) avec succès!")
                    st.info(
                        "💡 Consultez l'onglet 'Missions' du profil pour voir les ajouts"
                    )
                else:
                    st.warning("⚠️ Aucune mission n'a pu être ajoutée automatiquement")
                    st.info(
                        "� Utilisez l'onglet 'Missions' ci-dessus pour les ajouter manuellement"
                    )
            else:
                st.warning("⚠️ Aucune mission à ajouter")

        st.markdown("")
        if missions:
            st.info(
                f"💡 {
                    len(missions)} mission(s) peuvent être ajoutée(s) individuellement dans l'onglet 'Missions'"
            )

    with col2:
        st.write("**🛠️ Gestion des compétences**")
        if st.button(
            "🛠️ Ajouter toutes les compétences au profil", use_container_width=True
        ):
            total_skills = len(technologies) + len(competences)
            if total_skills > 0:
                st.success(f"✅ {total_skills} compétence(s) identifiée(s)")
                st.info(
                    "🚧 Ajout automatique des compétences en cours de développement"
                )
                st.write("**Technologies à ajouter:**")
                for tech in technologies[:5]:  # Limiter l'affichage
                    st.write(f"• {tech}")
                if len(technologies) > 5:
                    st.write(f"• ... et {len(technologies) - 5} autres")
            else:
                st.warning("⚠️ Aucune compétence à ajouter")

        st.markdown("")
        if technologies:
            st.info(
                f"💡 {
                    len(technologies)} technologie(s) peuvent être ajoutée(s) manuellement"
            )

    # Export et outils avancés
    st.markdown("---")
    st.subheader("📤 Export et outils")

    col_exp1, col_exp2, col_exp3 = st.columns(3)

    with col_exp1:
        if st.button("📄 Export JSON", use_container_width=True):
            import json

            export_data = {
                "consultant": f"{consultant.prenom} {consultant.nom}",
                "missions": missions,
                "technologies": technologies,
                "competences_fonctionnelles": competences,
                "date_analyse": datetime.now().isoformat(),
            }
            st.json(export_data)
            st.success("✅ Données exportées au format JSON")

    with col_exp2:
        if st.button("📊 Résumé formaté", use_container_width=True):
            resume_text = f"""
**Analyse CV - {consultant.prenom} {consultant.nom}**

**Missions ({len(missions)}):**
{chr(10).join([f"• {m.get('client', 'N/A')} - {m.get('titre', 'N/A')}" for m in missions[:10]])}

**Technologies ({len(technologies)}):**
{', '.join(technologies[:20])}

**Compétences ({len(competences)}):**
{', '.join(competences[:10])}
            """
            st.text_area("Résumé de l'analyse", resume_text, height=300)
            st.success("✅ Résumé généré")

    with col_exp3:
        if st.button("� Nouvelle analyse", use_container_width=True):
            st.info(
                "� Uploadez un nouveau document dans l'onglet 'Documents' pour une nouvelle analyse"
            )
            st.info("🔄 Ou rafraîchissez la page pour réanalyser le même document")

    st.subheader(f"🚀 Missions détectées ({len(missions)})")

    for i, mission in enumerate(missions, 1):
        with st.expander(
            f"Mission {i}: {mission.get('client', 'Client non spécifié')}",
            expanded=True,
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**🏢 Client:**", mission.get("client", "Non spécifié"))
                st.write("**🎯 Rôle:**", mission.get("role", "Non spécifié"))

                if mission.get("dates"):
                    st.write("**📅 Période:**", mission["dates"])

            with col2:
                if mission.get("langages_techniques"):
                    st.write("**🛠️ Technologies:**")
                    for tech in mission["langages_techniques"]:
                        st.markdown(f"• {tech}")

                if mission.get("description"):
                    st.write("**📝 Description:**")
                    st.write(
                        mission["description"][:200] + "..."
                        if len(mission["description"]) > 200
                        else mission["description"]
                    )


def import_missions_to_profile(missions, consultant):
    """Importe toutes les missions dans le profil du consultant"""

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
    """Importe une mission individuelle dans le profil"""

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
