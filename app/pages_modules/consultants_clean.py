"""
Page de gestion des consultants
CRUD complet pour les consultants avec formulaires, tableaux et gestion de documents
"""

import os
import sys

import pandas as pd
import streamlit as st

# Import des modèles et services
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.database import get_database_session
from database.models import Mission
from services.consultant_service import ConsultantService


def show():
    """Affiche la page de gestion des consultants"""

    print(
        "🚨 TERMINAL LOG: La fonction show() de consultants.py a été appelée!"
    )

    st.title("🚨 NOUVEAU TITRE UNIQUE 19/08/2025 - Gestion des consultants 🚨")
    st.markdown(
        "### ✅ CETTE PAGE A ÉTÉ MISE À JOUR - Gérez les profils de vos consultants"
    )

    # TEST FORCÉ POUR VÉRIFIER QUE CE FICHIER EST UTILISÉ - VERSION 19/08/2025 15:45
    st.error(
        "🚨 DEBUG ACTIF - CONSULTANTS.PY PAGES_MODULES - 19/08/2025 15:45 🚨"
    )
    st.success(
        "✅ Ce message confirme que le bon fichier consultants.py est utilisé"
    )
    st.balloons()

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

    # Informations principales
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Salaire annuel",
            f"{consultant.salaire_actuel or 0:,}€",
            delta=None,
        )

    with col2:
        status = "Disponible" if consultant.disponibilite else "En mission"
        st.metric("📊 Statut", status)

    with col3:
        creation_date = (
            consultant.date_creation.strftime("%d/%m/%Y")
            if consultant.date_creation
            else "N/A"
        )
        st.metric("📅 Membre depuis", creation_date)

    st.markdown("---")

    # Détails du profil
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 Informations",
            "💼 Compétences",
            "🚀 Missions",
            "📄 Documents",
            "⚙️ Actions",
        ]
    )

    with tab1:
        show_consultant_info(consultant)

    with tab2:
        show_consultant_skills(consultant)

    with tab3:
        show_consultant_missions(consultant)

    with tab4:
        show_consultant_documents(consultant)

    with tab5:
        show_consultant_actions(consultant)


def show_consultant_skills(consultant):
    """Affiche les compétences technologiques du consultant"""

    st.subheader("💼 Compétences technologiques")

    # Debug forcé pour vérifier que cette fonction est appelée
    st.error("🔥 DEBUG: Cette fonction est bien appelée !")
    st.write(
        f"🔍 Consultant ID: {consultant.id}, Nom: {consultant.nom} {consultant.prenom}"
    )

    # Récupérer les technologies des missions du consultant
    technologies_missions = get_consultant_technologies_from_missions(
        consultant.id
    )

    # Récupérer les compétences manuelles (si elles existent)
    competences_manuelles = get_consultant_manual_skills(consultant.id)

    # Combiner toutes les technologies
    all_technologies = set()

    # Technologies des missions
    for tech in technologies_missions:
        all_technologies.add(tech)

    # Compétences ajoutées manuellement
    for comp in competences_manuelles:
        all_technologies.add(comp)

    # Onglets pour organiser les fonctionnalités
    tab1, tab2 = st.tabs(
        ["📋 Compétences actuelles", "➕ Ajouter des compétences"]
    )

    with tab1:
        if all_technologies:
            st.write("**🏷️ Technologies maîtrisées**")

            for tech in sorted(all_technologies):
                source = (
                    "🚀 Mission"
                    if tech in technologies_missions
                    else "✋ Manuel"
                )
                st.write(f"• {tech} ({source})")

            # Métriques des compétences
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🛠️ Total technologies", len(all_technologies))

            with col2:
                st.metric("🚀 Depuis missions", len(technologies_missions))

            with col3:
                st.metric(
                    "✋ Ajoutées manuellement", len(competences_manuelles)
                )

        else:
            st.info("🔍 Aucune compétence technologique trouvée")

    with tab2:
        st.markdown("### ➕ Ajouter des compétences manuellement")
        st.info("Fonctionnalité d'ajout de compétences à venir")


def get_consultant_technologies_from_missions(consultant_id):
    """Récupère toutes les technologies utilisées dans les missions du consultant"""
    technologies = set()

    try:
        with get_database_session() as session:
            missions = (
                session.query(Mission)
                .filter(Mission.consultant_id == consultant_id)
                .all()
            )

            # Debug temporaire
            st.write(
                f"🔍 Debug: {len(missions)} missions trouvées pour consultant ID {consultant_id}"
            )

            for mission in missions:
                if (
                    mission.technologies_utilisees
                    and mission.technologies_utilisees.strip()
                ):
                    # Diviser les technologies et les nettoyer
                    mission_techs = [
                        tech.strip()
                        for tech in mission.technologies_utilisees.split(",")
                        if tech.strip()
                    ]
                    technologies.update(mission_techs)
                    st.write(f"✅ Mission {mission.client}: {mission_techs}")
                else:
                    st.write(
                        f"❌ Mission {mission.client}: pas de technologies"
                    )

    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des technologies: {e}")

    st.write(f"🎯 Technologies finales: {list(technologies)}")
    return list(technologies)


def get_consultant_manual_skills(consultant_id):
    """Récupère les compétences ajoutées manuellement pour le consultant"""
    key = f"manual_skills_{consultant_id}"
    return st.session_state.get(key, [])


def show_consultant_info(consultant):
    """Affiche les informations de base du consultant"""
    st.subheader("📋 Informations personnelles")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**👤 Prénom**: {consultant.prenom}")
        st.write(f"**📧 Email**: {consultant.email}")
        st.write(f"**💰 Salaire**: {consultant.salaire_actuel or 0:,}€")

    with col2:
        st.write(f"**👤 Nom**: {consultant.nom}")
        st.write(f"**📞 Téléphone**: {consultant.telephone or 'N/A'}")
        st.write(
            f"**✅ Disponible**: {'Oui' if consultant.disponibilite else 'Non'}"
        )


def show_consultant_missions(consultant):
    """Affiche les missions du consultant"""
    st.subheader("🚀 Missions")

    try:
        with get_database_session() as session:
            missions = (
                session.query(Mission)
                .filter(Mission.consultant_id == consultant.id)
                .all()
            )

        if missions:
            for mission in missions:
                with st.expander(
                    f"🚀 {mission.client} - {mission.role or 'Rôle non défini'}"
                ):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**🏢 Client**: {mission.client}")
                        st.write(
                            f"**👤 Rôle**: {mission.role or 'Non spécifié'}"
                        )
                        st.write(
                            f"**💰 Revenus**: {mission.revenus_generes or 0:,}€"
                        )

                    with col2:
                        st.write(
                            f"**📅 Début**: {mission.date_debut.strftime('%Y-%m-%d') if mission.date_debut else 'N/A'}"
                        )
                        st.write(
                            f"**📅 Fin**: {mission.date_fin.strftime('%Y-%m-%d') if mission.date_fin else 'En cours'}"
                        )
                        st.write(f"**📊 Statut**: {mission.statut}")

                    st.write(
                        f"**🛠️ Technologies**: {mission.technologies_utilisees or 'Non spécifiées'}"
                    )
        else:
            st.info("📝 Aucune mission enregistrée")

    except Exception as e:
        st.error(f"❌ Erreur: {e}")


def show_consultant_documents(consultant):
    """Affiche les documents du consultant"""
    st.subheader("📄 Documents")
    st.info("Fonctionnalité de gestion des documents à venir")


def show_consultant_actions(consultant):
    """Affiche les actions possibles"""
    st.subheader("⚙️ Actions")
    st.info("Actions supplémentaires à venir")


def show_consultants_list():
    """Affiche la liste des consultants"""

    st.subheader("📋 Liste des consultants")

    try:
        consultants = ConsultantService.get_all_consultants()

        if consultants:
            # Préparer les données pour le tableau
            consultants_data = []
            for consultant in consultants:
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
                    }
                )

            # Afficher le tableau
            df = pd.DataFrame(consultants_data)

            # Configuration du tableau avec sélection
            event = st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
            )

            # Gestion de la sélection
            if event.selection.rows:
                selected_row = event.selection.rows[0]
                selected_consultant_id = consultants_data[selected_row]["ID"]

                # Boutons d'action pour le consultant sélectionné
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "👁️ Voir le profil",
                        type="primary",
                        use_container_width=True,
                    ):
                        st.session_state.view_consultant_profile = (
                            selected_consultant_id
                        )
                        st.rerun()

                with col2:
                    if st.button("✏️ Modifier", use_container_width=True):
                        st.session_state.view_consultant_profile = (
                            selected_consultant_id
                        )
                        st.rerun()
        else:
            st.info("📝 Aucun consultant enregistré")

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {e}")


def show_add_consultant_form():
    """Affiche le formulaire d'ajout d'un nouveau consultant"""

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

        submitted = st.form_submit_button(
            "➕ Créer le consultant", type="primary"
        )

        if submitted:
            if not prenom or not nom or not email:
                st.error(
                    "❌ Veuillez remplir tous les champs obligatoires (*)"
                )
            else:
                try:
                    consultant_data = {
                        "prenom": prenom.strip(),
                        "nom": nom.strip(),
                        "email": email.strip().lower(),
                        "telephone": telephone.strip() if telephone else None,
                        "salaire_actuel": salaire,
                        "disponibilite": disponibilite,
                    }

                    ConsultantService.create_consultant(consultant_data)
                    st.success(f"✅ {prenom} {nom} a été créé avec succès !")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Erreur lors de la création: {e}")
