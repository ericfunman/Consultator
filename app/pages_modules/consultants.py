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
    from database.database import get_database_session
    from database.models import Mission
    from services.consultant_service import ConsultantService
    from services.simple_analyzer import SimpleDocumentAnalyzer as DocumentAnalyzer
    from services.document_service import DocumentService

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
        show_consultants_list()

    with tab2:
        show_add_consultant_form()


def show_consultant_profile():
    """Affiche le profil détaillé d'un consultant"""

    consultant_id = st.session_state.view_consultant_profile
    # Charger le consultant avec la relation practice pour éviter DetachedInstanceError
    from sqlalchemy.orm import joinedload
    from database.models import Consultant
    with get_database_session() as session:
        consultant = session.query(Consultant).options(joinedload(Consultant.practice)).filter(Consultant.id == consultant_id).first()

    if not consultant:
        st.error("❌ Consultant introuvable")
        del st.session_state.view_consultant_profile
        st.rerun()
        return

    # En-tête avec bouton retour
    col1, col2 = st.columns([6, 1])

    with col1:
        st.title(f"👤 Profil de {consultant.prenom} {consultant.nom}")

    with col2:
        if st.button("← Retour", key="back_to_list"):
            del st.session_state.view_consultant_profile
            st.rerun()

    st.markdown("---")

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Salaire annuel", f"{consultant.salaire_actuel or 0:,}€")

    with col2:
        status = (
            "✅ Disponible" if consultant.disponibilite else "🔴 En mission"
        )
        st.metric("📊 Statut", status)

    with col3:
        creation_date = (
            consultant.date_creation.strftime("%d/%m/%Y")
            if consultant.date_creation
            else "N/A"
        )
        st.metric("📅 Membre depuis", creation_date)

    with col4:
        practice_name = consultant.practice.nom if hasattr(consultant, 'practice') and consultant.practice else "Non affecté"
        st.metric("🏢 Practice", practice_name)

    st.markdown("---")

    # Onglets de détail
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Informations", "💼 Compétences", "🚀 Missions", "📁 Documents"]
    )

    with tab1:
        show_consultant_info(consultant)

    with tab2:
        show_consultant_skills(consultant)

    with tab3:
        show_consultant_missions(consultant)

    with tab4:
        show_consultant_documents(consultant)


def show_consultant_info(consultant):
    """Affiche et permet la modification des informations du consultant"""

    st.subheader("📋 Informations personnelles")

    from database.models import Practice, Consultant
    from sqlalchemy.orm import joinedload
    # Recharger le consultant avec la relation practice pour éviter DetachedInstanceError
    with get_database_session() as session:
        consultant_db = session.query(Consultant).options(joinedload(Consultant.practice)).filter(Consultant.id == consultant.id).first()
        practices = session.query(Practice).filter(Practice.actif == True).all()
    practice_options = {p.nom: p.id for p in practices}
    current_practice_id = consultant_db.practice_id if hasattr(consultant_db, 'practice_id') else None

    from database.models import ConsultantSalaire
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
            # Sélection de la practice
            practice_label = st.selectbox(
                "🏢 Practice",
                options=["Non affecté"] + list(practice_options.keys()),
                index=(list(practice_options.values()).index(current_practice_id) + 1) if current_practice_id in practice_options.values() else 0
            )
            selected_practice_id = practice_options.get(practice_label)

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

        # Historique des salaires
        st.markdown("---")
        st.subheader("📈 Historique des salaires")
        with get_database_session() as session:
            salaires = session.query(ConsultantSalaire).filter(ConsultantSalaire.consultant_id == consultant.id).order_by(ConsultantSalaire.date_debut.desc()).all()
        if salaires:
            for salaire in salaires:
                st.write(f"- **{salaire.salaire:,.0f} €** du {salaire.date_debut.strftime('%d/%m/%Y')} " + (f"au {salaire.date_fin.strftime('%d/%m/%Y')}" if salaire.date_fin else "(en cours)") + (f" — {salaire.commentaire}" if salaire.commentaire else ""))
        else:
            st.info("Aucune évolution de salaire enregistrée.")

        # Ajout d'une évolution de salaire
        with st.expander("➕ Ajouter une évolution de salaire"):
            with st.form(f"add_salary_form_{consultant.id}"):
                new_salaire = st.number_input("Nouveau salaire (€)", min_value=0, step=1000, key=f"salaire_{consultant.id}")
                new_date_debut = st.date_input("Date de début", value=datetime.today(), key=f"date_debut_{consultant.id}")
                new_commentaire = st.text_input("Commentaire", value="", key=f"commentaire_{consultant.id}")
                add_salary_submitted = st.form_submit_button("Ajouter l'évolution de salaire")
                if add_salary_submitted:
                    try:
                        with get_database_session() as session:
                            salaire_obj = ConsultantSalaire(
                                consultant_id=consultant.id,
                                salaire=new_salaire,
                                date_debut=new_date_debut,
                                commentaire=new_commentaire.strip() or None
                            )
                            session.add(salaire_obj)
                            session.commit()
                        st.success("✅ Évolution de salaire ajoutée !")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erreur lors de l'ajout : {e}")

        # Bouton de sauvegarde
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submitted = st.form_submit_button(
                "💾 Sauvegarder", type="primary", use_container_width=True
            )

        if submitted:
            if not prenom or not nom or not email:
                st.error(
                    "❌ Veuillez remplir tous les champs obligatoires (*)"
                )
            else:
                # Vérifier l'unicité de l'email
                existing = ConsultantService.get_consultant_by_email(email)
                if existing and existing.id != consultant.id:
                    st.error(
                        f"❌ Un consultant avec l'email {email} existe déjà !"
                    )
                else:
                    try:
                        update_data = {
                            "prenom": prenom.strip(),
                            "nom": nom.strip(),
                            "email": email.strip().lower(),
                            "telephone": (
                                telephone.strip() if telephone else None
                            ),
                            "salaire_actuel": salaire,
                            "disponibilite": disponibilite,
                            "notes": notes.strip() if notes else None,
                            "practice_id": selected_practice_id,
                        }

                        if ConsultantService.update_consultant(
                            consultant.id, update_data
                        ):
                            st.success(
                                f"✅ {prenom} {nom} modifié avec succès !"
                            )
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la modification")

                    except Exception as e:
                        st.error(f"❌ Erreur: {e}")


def show_consultant_skills(consultant):
    """Affiche les compétences du consultant basées sur ses missions"""

    st.subheader("💼 Compétences technologiques")

    try:
        # Récupérer les technologies des missions
        with get_database_session() as session:
            missions = (
                session.query(Mission)
                .filter(Mission.consultant_id == consultant.id)
                .all()
            )

        technologies = set()
        for mission in missions:
            if mission.technologies_utilisees:
                mission_techs = [
                    tech.strip()
                    for tech in mission.technologies_utilisees.split(",")
                    if tech.strip()
                ]
                technologies.update(mission_techs)

        if technologies:
            st.write("**🏷️ Technologies maîtrisées** (extraites des missions)")

            # Affichage en colonnes
            cols = st.columns(4)
            tech_list = sorted(list(technologies))

            for i, tech in enumerate(tech_list):
                with cols[i % 4]:
                    st.markdown(
                        f"""
                    <div style="padding: 8px; margin: 3px; border: 2px solid #1f77b4; 
                                border-radius: 5px; text-align: center; background-color: #e8f4fd;">
                        <strong>{tech}</strong>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

            st.markdown("---")
            st.metric("🛠️ Total technologies", len(technologies))
        else:
            st.info("🔍 Aucune technologie trouvée dans les missions")

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des compétences: {e}")


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
            missions_terminees = len(
                [m for m in missions if m.statut == "terminee"]
            )
            missions_en_cours = len(
                [m for m in missions if m.statut == "en_cours"]
            )

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
            tab1, tab2 = st.tabs(
                ["📋 Missions existantes", "➕ Ajouter une mission"]
            )

            with tab1:
                # Mode édition
                edit_mode = st.checkbox(
                    "✏️ Mode édition", key="edit_mode_missions"
                )

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

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des missions: {e}")


def show_mission_readonly(mission):
    """Affiche les détails d'une mission en lecture seule"""
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**🏢 Client**: {mission.client}")
        st.write(f"**👤 Rôle**: {mission.role or 'Non spécifié'}")
        st.write(
            f"**📅 Début**: {mission.date_debut.strftime('%Y-%m-%d') if mission.date_debut else 'N/A'}"
        )
        st.write(f"**💰 Revenus**: {mission.revenus_generes or 0:,}€")

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
            client = st.text_input(
                "🏢 Client", placeholder="Ex: Société Générale"
            )
            role = st.text_input("👤 Rôle", placeholder="Ex: Lead Developer")
            revenus = st.number_input(
                "💰 Revenus (€)", min_value=0.0, value=0.0
            )

        with col2:
            date_debut = st.date_input("📅 Date début")
            date_fin = st.date_input("📅 Date fin (optionnel)", value=None)
            statut = st.selectbox(
                "📊 Statut", ["en_cours", "terminee", "en_pause"]
            )

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
    """Affiche la liste des consultants avec interactions"""

    st.subheader("📋 Liste des consultants")

    try:
        consultants = ConsultantService.get_all_consultants()

        if consultants:
            # Préparer les données pour le tableau
            consultants_data = []
            for consultant in consultants:
                # Compter les missions
                try:
                    with get_database_session() as session:
                        nb_missions = (
                            session.query(Mission)
                            .filter(Mission.consultant_id == consultant.id)
                            .count()
                        )
                except:
                    nb_missions = 0

                consultants_data.append(
                    {
                        "ID": consultant.id,
                        "Prénom": consultant.prenom,
                        "Nom": consultant.nom,
                        "Email": consultant.email,
                        "Salaire": f"{consultant.salaire_actuel or 0:,}€",
                        "Statut": (
                            "✅ Disponible"
                            if consultant.disponibilite
                            else "🔴 Occupé"
                        ),
                        "Missions": nb_missions,
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
                selected_name = f"{consultants_data[selected_row]['Prénom']} {consultants_data[selected_row]['Nom']}"

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
                disponibles = len([c for c in consultants if c.disponibilite])
                st.metric("✅ Disponibles", disponibles)

            with col3:
                occupes = len(consultants) - disponibles
                st.metric("🔴 Occupés", occupes)

            with col4:
                salaire_moyen = (
                    sum(c.salaire_actuel or 0 for c in consultants)
                    / len(consultants)
                    if consultants
                    else 0
                )
                st.metric("💰 Salaire moyen", f"{salaire_moyen:,.0f}€")

        else:
            st.info("📝 Aucun consultant enregistré")
            st.markdown(
                "💡 Utilisez l'onglet **Ajouter un consultant** pour créer votre premier profil"
            )

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement de la liste: {e}")


def show_add_consultant_form():
    """Formulaire d'ajout d'un nouveau consultant"""

    st.subheader("➕ Ajouter un nouveau consultant")

    from database.models import Practice
    with get_database_session() as session:
        practices = session.query(Practice).filter(Practice.actif == True).all()
    practice_options = {p.nom: p.id for p in practices}

    with st.form("add_consultant_form"):
        col1, col2 = st.columns(2)

        with col1:
            prenom = st.text_input("👤 Prénom *", placeholder="Ex: Jean")
            email = st.text_input(
                "📧 Email *", placeholder="jean.dupont@example.com"
            )
            salaire = st.number_input(
                "💰 Salaire annuel (€)", min_value=0, value=45000, step=1000
            )
            # Sélection de la practice
            practice_label = st.selectbox(
                "🏢 Practice",
                options=["Non affecté"] + list(practice_options.keys()),
                index=0
            )
            selected_practice_id = practice_options.get(practice_label)

        with col2:
            nom = st.text_input("👤 Nom *", placeholder="Ex: Dupont")
            telephone = st.text_input(
                "📞 Téléphone", placeholder="01.23.45.67.89"
            )
            disponibilite = st.checkbox("✅ Disponible", value=True)

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
                st.error(
                    "❌ Veuillez remplir tous les champs obligatoires (*)"
                )
            else:
                # Vérifier l'unicité de l'email
                existing = ConsultantService.get_consultant_by_email(email)
                if existing:
                    st.error(
                        f"❌ Un consultant avec l'email {email} existe déjà !"
                    )
                else:
                    try:
                        consultant_data = {
                            "prenom": prenom.strip(),
                            "nom": nom.strip(),
                            "email": email.strip().lower(),
                            "telephone": (
                                telephone.strip() if telephone else None
                            ),
                            "salaire": salaire,
                            "disponible": disponibilite,
                            "notes": notes.strip() if notes else None,
                            "practice_id": selected_practice_id,
                        }

                        if ConsultantService.create_consultant(
                            consultant_data
                        ):
                            st.success(f"✅ {prenom} {nom} créé avec succès !")
                            st.balloons()  # Animation de succès
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la création")

                    except Exception as e:
                        st.error(f"❌ Erreur lors de la création: {e}")


# Fonctions utilitaires pour les missions


def save_mission_changes(mission_id, mission_data):
    """Sauvegarde les modifications d'une mission"""
    try:
        with get_database_session() as session:
            mission = (
                session.query(Mission).filter(Mission.id == mission_id).first()
            )

            if mission:
                # Mettre à jour les champs
                mission.nom_mission = mission_data["nom_mission"]
                mission.client = mission_data["client"]
                mission.role = mission_data["role"]
                mission.date_debut = mission_data["date_debut"]
                mission.date_fin = mission_data["date_fin"]
                mission.statut = mission_data["statut"]
                mission.revenus_generes = mission_data["revenus_generes"]
                mission.technologies_utilisees = mission_data[
                    "technologies_utilisees"
                ]
                mission.description = mission_data["description"]

                session.commit()
                st.success("✅ Mission mise à jour avec succès !")
                st.rerun()
            else:
                st.error("❌ Mission non trouvée")

    except Exception as e:
        st.error(f"❌ Erreur lors de la sauvegarde: {e}")


def delete_mission(mission_id):
    """Supprime une mission"""
    try:
        with get_database_session() as session:
            mission = (
                session.query(Mission).filter(Mission.id == mission_id).first()
            )

            if mission:
                session.delete(mission)
                session.commit()
                st.success("✅ Mission supprimée avec succès !")
                st.rerun()
            else:
                st.error("❌ Mission non trouvée")

    except Exception as e:
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

    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout: {e}")


def show_consultant_documents(consultant):
    """Affiche et gère les documents du consultant"""

    st.subheader(f"📁 Documents de {consultant.prenom} {consultant.nom}")

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
                size_display = f"{file_size/1024:.1f} MB"
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


def save_consultant_document(
    uploaded_file, consultant, document_type, description
):
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

    except Exception as e:
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

        # Debug : afficher le type détecté
        st.write(f"🔍 Type détecté: '{doc_type}'")

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

    except Exception as e:
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
                size_display = f"{file_size/1024:.1f} MB"
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
                    f"{doc_type} • {size_display} • {modified_time.strftime('%d/%m/%Y')}"
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
                if st.button(
                    "🗑️", key=f"delete_{file_path.name}", help="Supprimer"
                ):
                    delete_consultant_document(file_path)

            with col6:
                st.write("")  # Espace

            st.markdown("---")

    except Exception as e:
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
    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression: {e}")


def detect_document_type(filename):
    """Détecte automatiquement le type de document basé sur le nom de fichier"""

    filename_lower = filename.lower()

    # Détection basée sur le nom du fichier
    if any(word in filename_lower for word in ["cv", "resume", "curriculum"]):
        return "CV"
    elif any(
        word in filename_lower
        for word in ["lettre", "motivation", "cover", "letter"]
    ):
        return "Lettre de motivation"
    elif any(
        word in filename_lower
        for word in ["certificat", "certificate", "diplome", "diploma"]
    ):
        return "Certificat"
    elif any(
        word in filename_lower
        for word in ["contrat", "contract", "convention"]
    ):
        return "Contrat"
    elif any(
        word in filename_lower for word in ["presentation", "slides", "demo"]
    ):
        return "Présentation"
    else:
        # Détection basée sur l'extension
        extension = (
            filename_lower.split(".")[-1] if "." in filename_lower else ""
        )
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
        # Enlever ID, Prénom, Nom et Timestamp (dernière partie avant extension)
        # Garder tout ce qui est entre le nom et le timestamp
        original_parts = parts[3:-1]  # Tout sauf ID, Prénom, Nom et Timestamp

        if original_parts:
            original_name = "_".join(original_parts)

            # Remettre l'extension si elle a été séparée
            if "." in parts[-1]:
                timestamp_and_ext = parts[-1].split(".")
                if len(timestamp_and_ext) == 2:
                    extension = timestamp_and_ext[1]
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

    except Exception as e:
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

    except Exception as e:
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
                st.info(
                    "💡 Utilisez le bouton télécharger pour voir le fichier"
                )

    except Exception as e:
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

    except Exception as e:
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
            size_display = f"{file_size/1024:.1f} MB"
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
        st.info(
            "💡 Utilisez le bouton télécharger pour voir le fichier complet"
        )

        # Note pour l'utilisateur
        st.markdown(
            """
        **📝 Document Word détecté**
        - Téléchargez le fichier pour le voir dans Microsoft Word
        - L'aperçu complet nécessite des modules supplémentaires
        """
        )

    except Exception as e:
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
            size_display = f"{file_size/1024:.1f} MB"
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

        st.info(
            "🎯 Pour voir le contenu complet, utilisez le bouton télécharger"
        )

    except Exception as e:
        st.error(f"❌ Erreur lors de l'aperçu PowerPoint: {e}")


def analyze_cv_document(file_path, consultant):
    """Analyse un CV et affiche les résultats avec mise à jour automatique"""
    
    try:
        st.info(f"🔍 Analyse du fichier: {file_path.name}")

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

            # Affichage des résultats
            st.success("✅ Analyse terminée !")

            # Onglets pour organiser les résultats
            tab1, tab2, tab3, tab4 = st.tabs(
                ["📋 Missions", "�️ Compétences", "📊 Résumé", "💾 Actions"]
            )

            with tab1:
                show_cv_missions(analysis.get("missions", []), consultant)

            with tab2:
                show_cv_skills(analysis)

            with tab3:
                show_cv_summary(analysis, consultant)

            with tab4:
                show_cv_actions(analysis, consultant)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse : {e}")
        st.info("💡 Vérifiez que le fichier est bien un CV valide")


def show_cv_missions(missions, consultant):
    """Affiche les missions extraites du CV avec possibilité d'édition et sauvegarde"""

    if not missions:
        st.info("📋 Aucune mission détectée dans le CV")
        return

    st.write(f"**{len(missions)} mission(s) détectée(s) :**")
    
    # Trier les missions par ordre antéchronologique si possible
    # Pour le moment, on les affiche dans l'ordre détecté
    
    for i, mission in enumerate(missions, 1):
        with st.expander(f"🏢 Mission {i}: {mission.get('client', 'Client inconnu')}", expanded=True):
            
            # Créer des champs éditables pour chaque mission
            col1, col2 = st.columns(2)
            
            with col1:
                client = st.text_input(
                    "Client", 
                    value=mission.get('client', ''),
                    key=f"mission_{i}_client"
                )
                
                titre = st.text_input(
                    "Rôle/Titre", 
                    value=mission.get('titre', ''),
                    key=f"mission_{i}_titre"
                )
                
                # Dates de début et fin
                date_debut = st.date_input(
                    "Date de début",
                    value=None,
                    key=f"mission_{i}_debut"
                )
                
                date_fin = st.date_input(
                    "Date de fin",
                    value=None,
                    key=f"mission_{i}_fin"
                )
            
            with col2:
                description = st.text_area(
                    "Description",
                    value=mission.get('description', ''),
                    height=100,
                    key=f"mission_{i}_description"
                )
                
                # Technologies sous forme de tags
                technologies_text = ", ".join(mission.get('langages_techniques', []))
                technologies = st.text_area(
                    "Technologies (séparées par des virgules)",
                    value=technologies_text,
                    height=60,
                    key=f"mission_{i}_technologies"
                )
            
            # Bouton de sauvegarde pour cette mission
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button(f"💾 Sauvegarder Mission {i}", key=f"save_mission_{i}"):
                    save_mission_to_consultant(
                        consultant, client, titre, date_debut, date_fin, 
                        description, technologies, i
                    )
            
            with col2:
                if st.button(f"🗑️ Ignorer", key=f"ignore_mission_{i}"):
                    st.info(f"Mission {i} ignorée")
            
            st.markdown("---")


def save_mission_to_consultant(consultant, client, titre, date_debut, date_fin, description, technologies, mission_num):
    """Sauvegarde une mission dans la base de données"""
    
    try:
        # Convertir les technologies en liste
        tech_list = [tech.strip() for tech in technologies.split(',') if tech.strip()]
        
        # Préparer les données de la mission
        mission_data = {
            'consultant_id': consultant.id,
            'client': client,
            'titre': titre,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'description': description,
            'technologies': ', '.join(tech_list)
        }
        
        # TODO: Implémenter la sauvegarde en base de données
        # Pour le moment, on affiche juste un message de succès
        st.success(f"✅ Mission {mission_num} '{titre}' chez {client} sauvegardée !")
        st.info("💡 La sauvegarde en base de données sera implémentée prochainement")
        
        # Afficher un résumé de la mission
        with st.expander("📋 Résumé de la mission sauvegardée", expanded=False):
            st.write(f"**Client:** {client}")
            st.write(f"**Rôle:** {titre}")
            if date_debut:
                st.write(f"**Début:** {date_debut}")
            if date_fin:
                st.write(f"**Fin:** {date_fin}")
            st.write(f"**Description:** {description}")
            if tech_list:
                st.write(f"**Technologies:** {', '.join(tech_list)}")
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la sauvegarde de la mission {mission_num}: {e}")


def show_cv_skills(analysis):
    """Affiche les compétences extraites du CV"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛠️ Technologies")
        technologies = analysis.get("langages_techniques", [])
        if technologies:
            for tech in technologies:
                st.write(f"• {tech}")
        else:
            st.info("Aucune technologie détectée")
    
    with col2:
        st.subheader("💼 Compétences Fonctionnelles")
        competences = analysis.get("competences_fonctionnelles", [])
        if competences:
            for comp in competences:
                st.write(f"• {comp}")
        else:
            st.info("Aucune compétence fonctionnelle détectée")

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
            st.text_area("Aperçu du contenu analysé", texte_brut, height=200, disabled=True)

def show_cv_actions(analysis, consultant):
    """Affiche les actions possibles après analyse"""
    
    st.subheader("💾 Actions de sauvegarde")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Ajouter toutes les missions au profil", type="primary"):
            missions = analysis.get("missions", [])
            if missions:
                st.success(f"✅ {len(missions)} mission(s) prête(s) à être ajoutée(s)")
                st.info("🚧 Fonctionnalité de sauvegarde en cours de développement")
            else:
                st.warning("⚠️ Aucune mission à ajouter")
    
    with col2:
        if st.button("🛠️ Ajouter toutes les compétences au profil"):
            technologies = analysis.get("langages_techniques", [])
            if technologies:
                st.success(f"✅ {len(technologies)} technologie(s) prête(s) à être ajoutée(s)")
                st.info("🚧 Fonctionnalité de sauvegarde en cours de développement")
            else:
                st.warning("⚠️ Aucune technologie à ajouter")
    
    # Export options
    st.markdown("---")
    st.subheader("📤 Export des résultats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export JSON"):
            st.info("🚧 Export JSON en cours de développement")
    
    with col2:
        if st.button("📊 Export Excel"):
            st.info("🚧 Export Excel en cours de développement")
    
    with col3:
        if st.button("📋 Copier résumé"):
            st.info("🚧 Copie en cours de développement")

    st.subheader(f"🚀 Missions détectées ({len(missions)})")

    for i, mission in enumerate(missions, 1):
        with st.expander(
            f"Mission {i}: {mission.get('client', 'Client non spécifié')}",
            expanded=True,
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    "**🏢 Client:**", mission.get("client", "Non spécifié")
                )
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


def show_cv_skills(analysis):
    """Affiche les compétences extraites du CV"""

    st.subheader("🛠️ Compétences techniques détectées")

    skills = analysis.get("langages_techniques", [])
    if skills:
        # Afficher par colonnes
        cols = st.columns(4)
        for i, skill in enumerate(skills):
            with cols[i % 4]:
                st.markdown(
                    f"""
                <div style="padding: 8px; margin: 3px; border: 2px solid #1f77b4; 
                            border-radius: 5px; text-align: center; background-color: #e8f4fd;">
                    <strong>{skill}</strong>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        st.metric("📊 Total compétences", len(skills))
    else:
        st.info("🔍 Aucune compétence technique spécifique détectée")


def show_cv_summary(analysis, consultant):
    """Affiche un résumé de l'analyse"""

    st.subheader("📊 Résumé de l'analyse")

    col1, col2, col3 = st.columns(3)

    with col1:
        nb_missions = len(analysis.get("missions", []))
        st.metric("🚀 Missions", nb_missions)

    with col2:
        nb_skills = len(analysis.get("langages_techniques", []))
        st.metric("🛠️ Compétences", nb_skills)

    with col3:
        nb_clients = len(
            set(
                m.get("client", "")
                for m in analysis.get("missions", [])
                if m.get("client")
            )
        )
        st.metric("🏢 Clients", nb_clients)

    # Informations générales
    if analysis.get("informations_generales"):
        st.subheader("ℹ️ Informations détectées")
        info = analysis["informations_generales"]

        if info.get("email"):
            st.write(f"📧 **Email:** {info['email']}")
        if info.get("telephone"):
            st.write(f"📞 **Téléphone:** {info['telephone']}")


def show_cv_actions(analysis, consultant):
    """Affiche les actions possibles après analyse"""

    st.subheader("💾 Actions disponibles")

    missions = analysis.get("missions", [])
    if missions:
        st.write(f"**{len(missions)} mission(s) détectée(s) dans le CV**")

        # Afficher un aperçu des missions détectées
        with st.expander("👀 Aperçu des missions détectées", expanded=True):
            for i, mission in enumerate(
                missions[:3]
            ):  # Afficher les 3 premières
                st.write(f"**Mission {i+1}:**")
                st.write(f"- Client: {mission.get('client', 'Non spécifié')}")
                st.write(f"- Rôle: {mission.get('role', 'Non spécifié')}")
                if mission.get("langages_techniques"):
                    st.write(
                        f"- Technologies: {', '.join(mission['langages_techniques'][:5])}"
                    )
                st.write("---")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "📥 Importer toutes les missions dans le profil",
                type="primary",
            ):
                import_missions_to_profile(missions, consultant)

        with col2:
            if st.button("🔍 Voir toutes les missions détaillées"):
                st.session_state["show_detailed_missions"] = True
                st.rerun()

        # Affichage détaillé si demandé
        if st.session_state.get("show_detailed_missions", False):
            st.markdown("---")
            st.subheader("📋 Toutes les missions détectées")

            for i, mission in enumerate(missions):
                with st.expander(
                    f"Mission {i+1}: {mission.get('client', 'Client non spécifié')}",
                    expanded=False,
                ):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(
                            f"**🏢 Client:** {mission.get('client', 'Non spécifié')}"
                        )
                        st.write(
                            f"**🎯 Rôle:** {mission.get('role', 'Non spécifié')}"
                        )

                        if mission.get("dates"):
                            st.write(f"**📅 Période:** {mission['dates']}")

                        if mission.get("description"):
                            st.write(
                                f"**📝 Description:** {mission['description'][:200]}..."
                            )

                        if mission.get("langages_techniques"):
                            st.write(
                                f"**🛠️ Technologies:** {', '.join(mission['langages_techniques'])}"
                            )

                    with col2:
                        if st.button("📥 Importer", key=f"import_mission_{i}"):
                            import_single_mission(mission, consultant)

            if st.button("❌ Fermer les détails"):
                st.session_state["show_detailed_missions"] = False
                st.rerun()

    else:
        st.info("🔍 Aucune mission détectée dans le CV")
        st.write("Cela peut arriver si:")
        st.write("- Le document n'est pas un CV")
        st.write("- Le format du CV n'est pas reconnu")
        st.write("- Les missions ne sont pas clairement structurées")

        # Debug - afficher un aperçu du texte analysé
        if analysis.get("texte_brut"):
            with st.expander("🔍 Aperçu du texte analysé"):
                st.text_area(
                    "Texte extrait (premier aperçu):",
                    analysis["texte_brut"],
                    height=200,
                    disabled=True,
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
                    nom_mission=mission_data.get(
                        "role", "Mission importée du CV"
                    ),
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
            st.success(
                f"✅ {success_count} mission(s) importée(s) avec succès !"
            )
            st.rerun()

    except Exception as e:
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

    except Exception as e:
        st.error(f"❌ Erreur lors de l'import : {e}")
