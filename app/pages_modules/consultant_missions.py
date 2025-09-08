"""
Module de gestion des missions du consultant
Fonctions pour afficher, ajouter et modifier les missions
"""

import os
import sys
from datetime import date
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import streamlit as st

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Variables pour les imports
ConsultantService = None
get_database_session = None
Consultant = None
imports_ok = False

try:
    from sqlalchemy.orm import joinedload

    from database.database import get_database_session
    from database.models import Client
    from database.models import Consultant
    from database.models import Mission
    from services.consultant_service import ConsultantService

    imports_ok = True
except ImportError as e:
    # Imports échoués, on continue quand même
    pass


def show_consultant_missions(consultant):
    """Affiche les missions du consultant"""

    if not imports_ok:
        st.error("❌ Les services de base ne sont pas disponibles")
        return

    if not consultant:
        st.error("❌ Consultant non fourni")
        return

    st.markdown("### 🚀 Missions")

    try:
        # Récupérer les missions du consultant
        with get_database_session() as session:
            missions = (
                session.query(Mission)
                .options(joinedload(Mission.client))
                .filter(Mission.consultant_id == consultant.id)
                .order_by(Mission.date_debut.desc())
                .all()
            )

        if not missions:
            st.info("ℹ️ Aucune mission enregistrée pour ce consultant")
            show_add_mission_form(consultant.id)
            return

        # Statistiques des missions
        show_missions_statistics(missions)

        # Liste des missions
        st.markdown("#### 📋 Liste des missions")

        for mission in missions:
            with st.expander(
                f"🎯 {mission.titre} - {mission.client.nom if mission.client else 'Client inconnu'}"
            ):
                show_mission_details(mission)

        # Actions générales
        st.markdown("#### 🎯 Actions générales")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("➕ Nouvelle mission", key=f"add_mission_{consultant.id}"):
                st.session_state.add_mission = consultant.id
                st.rerun()

        with col2:
            if st.button(
                "📊 Analyse missions", key=f"analyze_missions_{consultant.id}"
            ):
                show_missions_analysis(missions)

        with col3:
            if st.button("📈 Revenus", key=f"revenues_{consultant.id}"):
                show_missions_revenues(missions)

        # Formulaire d'ajout (si activé)
        if (
            "add_mission" in st.session_state
            and st.session_state.add_mission == consultant.id
        ):
            show_add_mission_form(consultant.id)

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage des missions: {e}")
        st.code(str(e))


def show_mission_details(mission):
    """Affiche les détails d'une mission"""

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📅 Période**")
        if mission.date_debut:
            st.write(f"**Début :** {mission.date_debut.strftime('%d/%m/%Y')}")
        if mission.date_fin:
            st.write(f"**Fin :** {mission.date_fin.strftime('%d/%m/%Y')}")
        elif mission.en_cours:
            st.write("**Statut :** 🔄 En cours")

        st.markdown("**🏢 Client**")
        if mission.client:
            st.write(f"**Nom :** {mission.client.nom}")
            if mission.client.secteur:
                st.write(f"**Secteur :** {mission.client.secteur}")

    with col2:
        st.markdown("**💰 Rémunération**")
        if mission.tjm:
            st.write(f"**TJM Mission :** {mission.tjm:,}€")
        elif mission.taux_journalier:
            st.write(f"**TJM (ancien) :** {mission.taux_journalier:,}€")
        if mission.salaire_mensuel:
            st.write(f"**Salaire mensuel :** {mission.salaire_mensuel:,}€")

        st.markdown("**📊 Informations**")
        if mission.description:
            st.write(f"**Description :** {mission.description[:100]}...")

    # Compétences utilisées
    if mission.competences_requises:
        st.markdown("**🛠️ Compétences requises**")
        st.write(mission.competences_requises)

    # Actions sur la mission
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✏️ Modifier", key=f"edit_mission_{mission.id}"):
            st.session_state.edit_mission = mission.id
            st.rerun()

    with col2:
        if st.button("📋 Détails", key=f"details_mission_{mission.id}"):
            st.session_state.view_mission_details = mission.id
            st.rerun()

    with col3:
        if st.button("🗑️ Supprimer", key=f"delete_mission_{mission.id}"):
            if delete_mission(mission.id):
                st.rerun()

    # Formulaire de modification (si activé)
    if (
        "edit_mission" in st.session_state
        and st.session_state.edit_mission == mission.id
    ):
        show_edit_mission_form(mission.id)

    # Détails étendus (si activé)
    if (
        "view_mission_details" in st.session_state
        and st.session_state.view_mission_details == mission.id
    ):
        show_mission_full_details(mission)


def show_missions_statistics(missions):
    """Affiche les statistiques des missions"""

    if not missions:
        return

    st.markdown("#### 📊 Statistiques")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_missions = len(missions)
        st.metric("Total missions", total_missions)

    with col2:
        current_missions = sum(1 for m in missions if m.en_cours)
        st.metric("En cours", current_missions)

    with col3:
        completed_missions = sum(1 for m in missions if m.date_fin and not m.en_cours)
        st.metric("Terminées", completed_missions)

    with col4:
        # Calcul du revenu total estimé
        total_revenue = sum(
            (m.taux_journalier or 0) * 22 * 12
            for m in missions
            if not m.date_fin  # Missions sans date de fin = 1 an estimé
        )
        total_revenue += sum(
            (m.taux_journalier or 0) * 22 * ((m.date_fin - m.date_debut).days // 30)
            for m in missions
            if m.date_fin and m.date_debut
        )
        st.metric("Revenus estimés", f"{total_revenue:,.0f}€")


def show_add_mission_form(consultant_id: int):
    """Affiche le formulaire d'ajout de mission"""

    st.markdown("### ➕ Ajouter une mission")

    try:
        # Récupérer les clients disponibles
        with get_database_session() as session:
            clients = session.query(Client).all()
            client_options = {c.id: c.nom for c in clients}

        if not client_options:
            st.warning("⚠️ Aucun client trouvé. Veuillez créer des clients d'abord.")
            return

        with st.form(f"add_mission_form_{consultant_id}", clear_on_submit=True):
            st.markdown("#### 📋 Informations générales")

            titre = st.text_input(
                "Titre de la mission *", help="Titre descriptif de la mission"
            )

            client_id = st.selectbox(
                "Client *",
                options=list(client_options.keys()),
                format_func=lambda x: client_options[x],
                help="Client pour lequel la mission est réalisée",
            )

            col1, col2 = st.columns(2)

            with col1:
                date_debut = st.date_input(
                    "Date de début *",
                    value=datetime.now().date(),
                    help="Date de début de la mission",
                )

                en_cours = st.checkbox(
                    "Mission en cours",
                    value=True,
                    help="La mission est-elle toujours en cours ?",
                )

            with col2:
                date_fin = st.date_input(
                    "Date de fin",
                    value=None,
                    disabled=en_cours,
                    help="Date de fin de la mission (laisser vide si en cours)",
                )

            st.markdown("#### 💰 Rémunération")

            col1, col2, col3 = st.columns(3)

            with col1:
                taux_journalier = st.number_input(
                    "Taux journalier (€)",
                    min_value=0,
                    step=10,
                    help="Taux journalier moyen de la mission (ancien champ)",
                )

            with col2:
                tjm = st.number_input(
                    "TJM Mission (€)",
                    min_value=0,
                    step=10,
                    help="Taux Journalier Moyen spécifique à cette mission",
                )

            with col3:
                salaire_mensuel = st.number_input(
                    "Salaire mensuel (€)",
                    min_value=0,
                    step=100,
                    help="Salaire mensuel fixe (si applicable)",
                )

            st.markdown("#### 📝 Description")

            description = st.text_area(
                "Description de la mission",
                height=100,
                help="Description détaillée de la mission, responsabilités, livrables...",
            )

            competences_requises = st.text_area(
                "Compétences requises",
                height=80,
                help="Liste des compétences techniques et fonctionnelles requises",
            )

            # Boutons
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                submitted = st.form_submit_button("💾 Créer", type="primary")

            with col2:
                cancel = st.form_submit_button("❌ Annuler")

            with col3:
                pass

            if submitted:
                if validate_mission_form(
                    titre, client_id, date_debut, en_cours, date_fin
                ):
                    success = create_mission(
                        consultant_id,
                        {
                            "titre": titre,
                            "client_id": client_id,
                            "date_debut": date_debut,
                            "date_fin": date_fin,
                            "en_cours": en_cours,
                            "taux_journalier": taux_journalier,
                            "tjm": tjm,  # Nouveau champ TJM V1.2.2
                            "salaire_mensuel": salaire_mensuel,
                            "description": description,
                            "competences_requises": competences_requises,
                        },
                    )

                    if success:
                        st.success("✅ Mission créée avec succès !")
                        if "add_mission" in st.session_state:
                            del st.session_state.add_mission
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la création de la mission")
                else:
                    st.error("❌ Veuillez corriger les erreurs ci-dessus")

            if cancel:
                if "add_mission" in st.session_state:
                    del st.session_state.add_mission
                st.rerun()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire: {e}")


def validate_mission_form(
    titre: str,
    client_id: int,
    date_debut: date,
    en_cours: bool,
    date_fin: Optional[date],
) -> bool:
    """Valide les données du formulaire de mission"""

    errors = []

    if not titre or not titre.strip():
        errors.append("Le titre de la mission est obligatoire")

    if not client_id:
        errors.append("Le client est obligatoire")

    if not date_debut:
        errors.append("La date de début est obligatoire")

    if not en_cours and date_fin and date_fin <= date_debut:
        errors.append("La date de fin doit être postérieure à la date de début")

    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        return False

    return True


def create_mission(consultant_id: int, data: Dict[str, Any]) -> bool:
    """Crée une nouvelle mission"""

    try:
        with get_database_session() as session:
            mission = Mission(
                consultant_id=consultant_id,
                titre=data["titre"].strip(),
                client_id=data["client_id"],
                date_debut=data["date_debut"],
                date_fin=data["date_fin"] if not data["en_cours"] else None,
                en_cours=data["en_cours"],
                taux_journalier=(
                    data["taux_journalier"] if data["taux_journalier"] > 0 else None
                ),
                # Nouveau champ TJM V1.2.2
                tjm=data["tjm"] if data["tjm"] > 0 else None,
                salaire_mensuel=(
                    data["salaire_mensuel"] if data["salaire_mensuel"] > 0 else None
                ),
                description=(
                    data["description"].strip() if data["description"] else None
                ),
                competences_requises=(
                    data["competences_requises"].strip()
                    if data["competences_requises"]
                    else None
                ),
            )

            session.add(mission)
            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la création de la mission: {e}")
        return False


def show_edit_mission_form(mission_id: int):
    """Affiche le formulaire de modification de mission"""

    st.markdown("### ✏️ Modifier une mission")

    try:
        with get_database_session() as session:
            mission = (
                session.query(Mission)
                .options(joinedload(Mission.client))
                .filter(Mission.id == mission_id)
                .first()
            )

            if not mission:
                st.error("❌ Mission introuvable")
                return

            clients = session.query(Client).all()
            client_options = {c.id: c.nom for c in clients}

        with st.form(f"edit_mission_form_{mission_id}", clear_on_submit=False):
            st.markdown("#### 📋 Informations générales")

            titre = st.text_input(
                "Titre de la mission *",
                value=mission.titre,
                help="Titre descriptif de la mission",
            )

            client_id = st.selectbox(
                "Client *",
                options=list(client_options.keys()),
                format_func=lambda x: client_options[x],
                index=(
                    list(client_options.keys()).index(mission.client_id)
                    if mission.client_id in client_options
                    else 0
                ),
                help="Client pour lequel la mission est réalisée",
            )

            col1, col2 = st.columns(2)

            with col1:
                date_debut = st.date_input(
                    "Date de début *",
                    value=mission.date_debut,
                    help="Date de début de la mission",
                )

                en_cours = st.checkbox(
                    "Mission en cours",
                    value=mission.en_cours,
                    help="La mission est-elle toujours en cours ?",
                )

            with col2:
                date_fin = st.date_input(
                    "Date de fin",
                    value=mission.date_fin,
                    disabled=en_cours,
                    help="Date de fin de la mission (laisser vide si en cours)",
                )

            st.markdown("#### 💰 Rémunération")

            col1, col2 = st.columns(2)

            with col1:
                taux_journalier = st.number_input(
                    "Taux journalier (€)",
                    value=mission.taux_journalier or 0,
                    min_value=0,
                    step=10,
                    help="Taux journalier moyen de la mission",
                )

            with col2:
                salaire_mensuel = st.number_input(
                    "Salaire mensuel (€)",
                    value=mission.salaire_mensuel or 0,
                    min_value=0,
                    step=100,
                    help="Salaire mensuel fixe (si applicable)",
                )

            st.markdown("#### 📝 Description")

            description = st.text_area(
                "Description de la mission",
                value=mission.description or "",
                height=100,
                help="Description détaillée de la mission, responsabilités, livrables...",
            )

            competences_requises = st.text_area(
                "Compétences requises",
                value=mission.competences_requises or "",
                height=80,
                help="Liste des compétences techniques et fonctionnelles requises",
            )

            # Boutons
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                submitted = st.form_submit_button("💾 Enregistrer", type="primary")

            with col2:
                cancel = st.form_submit_button("❌ Annuler")

            with col3:
                delete = st.form_submit_button("🗑️ Supprimer", type="secondary")

            if submitted:
                if validate_mission_form(
                    titre, client_id, date_debut, en_cours, date_fin
                ):
                    success = update_mission(
                        mission_id,
                        {
                            "titre": titre,
                            "client_id": client_id,
                            "date_debut": date_debut,
                            "date_fin": date_fin,
                            "en_cours": en_cours,
                            "taux_journalier": taux_journalier,
                            "salaire_mensuel": salaire_mensuel,
                            "description": description,
                            "competences_requises": competences_requises,
                        },
                    )

                    if success:
                        st.success("✅ Mission mise à jour avec succès !")
                        if "edit_mission" in st.session_state:
                            del st.session_state.edit_mission
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la mise à jour")
                else:
                    st.error("❌ Veuillez corriger les erreurs")

            if delete:
                st.warning("⚠️ Cette action est irréversible !")
                if st.checkbox("Je confirme vouloir supprimer cette mission"):
                    if delete_mission(mission_id):
                        if "edit_mission" in st.session_state:
                            del st.session_state.edit_mission
                        st.rerun()

            if cancel:
                if "edit_mission" in st.session_state:
                    del st.session_state.edit_mission
                st.rerun()

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire de modification: {e}")


def update_mission(mission_id: int, data: Dict[str, Any]) -> bool:
    """Met à jour une mission"""

    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()

            if not mission:
                st.error("❌ Mission introuvable")
                return False

            # Mettre à jour les données
            mission.titre = data["titre"].strip()
            mission.client_id = data["client_id"]
            mission.date_debut = data["date_debut"]
            mission.date_fin = data["date_fin"] if not data["en_cours"] else None
            mission.en_cours = data["en_cours"]
            mission.taux_journalier = (
                data["taux_journalier"] if data["taux_journalier"] > 0 else None
            )
            mission.salaire_mensuel = (
                data["salaire_mensuel"] if data["salaire_mensuel"] > 0 else None
            )
            mission.description = (
                data["description"].strip() if data["description"] else None
            )
            mission.competences_requises = (
                data["competences_requises"].strip()
                if data["competences_requises"]
                else None
            )

            session.commit()

            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la mise à jour de la mission: {e}")
        return False


def delete_mission(mission_id: int) -> bool:
    """Supprime une mission"""

    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()

            if not mission:
                st.error("❌ Mission introuvable")
                return False

            session.delete(mission)
            session.commit()

            st.info("✅ Mission supprimée")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression de la mission: {e}")
        return False


def show_mission_full_details(mission):
    """Affiche les détails complets d'une mission"""

    st.markdown("### 📋 Détails complets de la mission")

    # Informations détaillées
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📅 Chronologie")
        if mission.date_debut:
            st.write(f"**Date de début :** {mission.date_debut.strftime('%d/%m/%Y')}")

        if mission.date_fin:
            st.write(f"**Date de fin :** {mission.date_fin.strftime('%d/%m/%Y')}")
            # Calcul de la durée
            duration_days = (mission.date_fin - mission.date_debut).days
            duration_months = duration_days // 30
            st.write(f"**Durée :** {duration_months} mois ({duration_days} jours)")
        elif mission.en_cours:
            # Durée depuis le début
            today = date.today()
            duration_days = (today - mission.date_debut).days
            duration_months = duration_days // 30
            st.write(
                f"**Durée actuelle :** {duration_months} mois ({duration_days} jours)"
            )
            st.write("**Statut :** 🔄 En cours")

    with col2:
        st.markdown("#### 💰 Aspects financiers")

        # Affichage TJM (nouveau champ V1.2.2)
        if mission.tjm:
            st.write(f"**TJM Mission :** {mission.tjm:,}€")
        elif mission.taux_journalier:
            st.write(f"**Taux journalier (ancien) :** {mission.taux_journalier:,}€")

        # Calcul du revenu estimé avec le bon TJM
        tjm_value = mission.tjm if mission.tjm else mission.taux_journalier
        if tjm_value:
            if mission.date_fin:
                duration_days = (mission.date_fin - mission.date_debut).days
                estimated_revenue = tjm_value * (duration_days // 7 * 5)  # Jours ouvrés
                st.write(f"**Revenus estimés :** {estimated_revenue:,.0f}€")
            elif mission.en_cours:
                today = date.today()
                duration_days = (today - mission.date_debut).days
                estimated_revenue = tjm_value * (duration_days // 7 * 5)
                st.write(f"**Revenus à ce jour :** {estimated_revenue:,.0f}€")

        if mission.salaire_mensuel:
            st.write(f"**Salaire mensuel :** {mission.salaire_mensuel:,}€")

    # Description complète
    if mission.description:
        st.markdown("#### 📝 Description détaillée")
        st.write(mission.description)

    # Compétences
    if mission.competences_requises:
        st.markdown("#### 🛠️ Compétences requises")
        st.write(mission.competences_requises)

    # Informations client
    if mission.client:
        st.markdown("#### 🏢 Informations client")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Nom :** {mission.client.nom}")
            if mission.client.secteur:
                st.write(f"**Secteur :** {mission.client.secteur}")

        with col2:
            if mission.client.adresse:
                st.write(f"**Adresse :** {mission.client.adresse}")
            if mission.client.contact_principal:
                st.write(f"**Contact :** {mission.client.contact_principal}")

    # Bouton pour fermer
    if st.button("❌ Fermer les détails", key=f"close_details_{mission.id}"):
        del st.session_state.view_mission_details
        st.rerun()


def show_missions_analysis(missions):
    """Affiche une analyse des missions"""

    st.markdown("### 📊 Analyse des missions")

    if not missions:
        st.info("ℹ️ Aucune mission à analyser")
        return

    # Analyse par client
    client_counts = {}
    for mission in missions:
        client_name = mission.client.nom if mission.client else "Client inconnu"
        client_counts[client_name] = client_counts.get(client_name, 0) + 1

    # Analyse par statut
    status_counts = {
        "En cours": sum(1 for m in missions if m.en_cours),
        "Terminées": sum(1 for m in missions if m.date_fin and not m.en_cours),
        "Planifiées": sum(
            1
            for m in missions
            if not m.en_cours
            and not m.date_fin
            and m.date_debut > datetime.now().date()
        ),
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏢 Répartition par client")
        for client, count in sorted(
            client_counts.items(), key=lambda x: x[1], reverse=True
        ):
            st.write(f"**{client} :** {count} mission(s)")

    with col2:
        st.markdown("#### 📊 Répartition par statut")
        for status, count in status_counts.items():
            if count > 0:
                st.write(f"**{status} :** {count} mission(s)")

    # Analyse temporelle
    st.markdown("#### 📈 Analyse temporelle")

    # Grouper par année
    missions_by_year = {}
    for mission in missions:
        if mission.date_debut:
            year = mission.date_debut.year
            if year not in missions_by_year:
                missions_by_year[year] = []
            missions_by_year[year].append(mission)

    for year in sorted(missions_by_year.keys(), reverse=True):
        year_missions = missions_by_year[year]
        st.write(f"**{year} :** {len(year_missions)} mission(s)")

        # Calcul des revenus pour l'année
        year_revenue = 0
        for mission in year_missions:
            if mission.taux_journalier and mission.date_fin:
                # Revenus pour les missions terminées
                duration_days = (mission.date_fin - mission.date_debut).days
                year_revenue += mission.taux_journalier * (duration_days // 7 * 5)
            elif (
                mission.taux_journalier
                and mission.en_cours
                and mission.date_debut.year == year
            ):
                # Estimation pour les missions en cours de l'année
                today = date.today()
                if today.year == year:
                    duration_days = (today - mission.date_debut).days
                    year_revenue += mission.taux_journalier * (duration_days // 7 * 5)

        if year_revenue > 0:
            st.write(f"**Revenus {year} :** {year_revenue:,.0f}€")


def show_missions_revenues(missions):
    """Affiche l'analyse des revenus des missions"""

    st.markdown("### 📈 Analyse des revenus")

    if not missions:
        st.info("ℹ️ Aucune mission pour analyser les revenus")
        return

    # Calcul des revenus par mission
    revenue_data = []
    total_revenue = 0

    for mission in missions:
        revenue = 0
        if mission.taux_journalier:
            if mission.date_fin:
                # Mission terminée
                duration_days = (mission.date_fin - mission.date_debut).days
                working_days = duration_days // 7 * 5  # Jours ouvrés approximatifs
                revenue = mission.taux_journalier * working_days
            elif mission.en_cours:
                # Mission en cours
                today = date.today()
                duration_days = (today - mission.date_debut).days
                working_days = duration_days // 7 * 5
                revenue = mission.taux_journalier * working_days

        if revenue > 0:
            revenue_data.append(
                {
                    "Mission": mission.titre,
                    "Client": mission.client.nom if mission.client else "Inconnu",
                    "Revenus": revenue,
                    "TJM": mission.taux_journalier or 0,
                    "Statut": "En cours" if mission.en_cours else "Terminée",
                }
            )
            total_revenue += revenue

    if revenue_data:
        import pandas as pd

        df = pd.DataFrame(revenue_data)

        # Trier par revenus décroissants
        df = df.sort_values("Revenus", ascending=False)

        # Formater les colonnes
        df["Revenus"] = df["Revenus"].apply(lambda x: f"{x:,.0f}€")
        df["TJM"] = df["TJM"].apply(lambda x: f"{x:,}€" if x > 0 else "N/A")

        st.dataframe(df, use_container_width=True, hide_index=True)

        # Statistiques globales
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total revenus", f"{total_revenue:,.0f}€")

        with col2:
            avg_tjm = sum(
                m.taux_journalier for m in missions if m.taux_journalier
            ) / len([m for m in missions if m.taux_journalier])
            st.metric("TJM moyen", f"{avg_tjm:,.0f}€")

        with col3:
            active_missions = sum(1 for m in missions if m.en_cours)
            st.metric("Missions actives", active_missions)

    else:
        st.info("ℹ️ Aucune donnée de revenus disponible")
