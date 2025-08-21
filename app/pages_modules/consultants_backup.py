"""
Page de gestion des consultants - Version fonctionnelle
CRUD complet pour les consultants avec formulaires, tableaux et gestion des missions
"""

import os
import sys

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
    consultant = ConsultantService.get_consultant_by_id(consultant_id)

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
    col1, col2, col3 = st.columns(3)

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

    st.markdown("---")

    # Onglets de détail
    tab1, tab2, tab3 = st.tabs(
        ["📋 Informations", "💼 Compétences", "🚀 Missions"]
    )

    with tab1:
        show_consultant_info(consultant)

    with tab2:
        show_consultant_skills(consultant)

    with tab3:
        show_consultant_missions(consultant)


def show_consultant_info(consultant):
    """Affiche et permet la modification des informations du consultant"""

    st.subheader("📋 Informations personnelles")

    with st.form(f"edit_consultant_{consultant.id}"):
        col1, col2 = st.columns(2)

        with col1:
            prenom = st.text_input(
                "👤 Prénom *", value=consultant.prenom, placeholder="Ex: Jean"
            )
            email = st.text_input(
                "📧 Email *",
                value=consultant.email,
                placeholder="jean.dupont@example.com",
            )
            salaire = st.number_input(
                "💰 Salaire annuel (€)",
                min_value=0,
                value=int(consultant.salaire_actuel or 0),
                step=1000,
            )

        with col2:
            nom = st.text_input(
                "👤 Nom *", value=consultant.nom, placeholder="Ex: Dupont"
            )
            telephone = st.text_input(
                "📞 Téléphone",
                value=consultant.telephone or "",
                placeholder="01.23.45.67.89",
            )
            disponibilite = st.checkbox(
                "✅ Disponible", value=consultant.disponibilite
            )

        # Notes
        notes = st.text_area(
            "📝 Notes",
            value=consultant.notes or "",
            height=100,
            placeholder="Notes sur le consultant...",
        )

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
