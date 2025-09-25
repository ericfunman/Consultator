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

# Constantes pour les statuts de mission
STATUS_EN_COURS = "En cours"
STATUS_TERMINEE = "Terminée"
STATUS_PLANIFIEE = "Planifiée"

# Constantes pour les messages d'erreur
MSG_MISSION_INTROUVABLE = "❌ Mission introuvable"
MSG_SERVICES_INDISPONIBLES = "❌ Les services de base ne sont pas disponibles"
MSG_CONSULTANT_INTROUVABLE = "❌ Consultant introuvable"
MSG_ERREUR_CHARGEMENT = "❌ Erreur lors du chargement des missions"
MSG_ERREUR_CREATION = "❌ Erreur lors de la création de la mission"
MSG_ERREUR_MODIFICATION = "❌ Erreur lors de la modification de la mission"
MSG_ERREUR_SUPPRESSION = "❌ Erreur lors de la suppression de la mission"
MSG_AUCUNE_MISSION = "ℹ️ Aucune mission trouvée pour ce consultant"

# Constantes pour les messages de succès
MSG_SUCCESS_CREATION = "✅ Mission créée avec succès !"
MSG_SUCCESS_MODIFICATION = "✅ Mission modifiée avec succès !"
MSG_SUCCESS_SUPPRESSION = "✅ Mission supprimée avec succès !"

# Constantes pour les valeurs par défaut
DEFAULT_VALUE = "N/A"
DEFAULT_CLIENT = "Non renseigné"

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Variables pour les imports
ConsultantService = None
get_database_session = None
Consultant = None
Mission = None
imports_ok = False

try:
    from sqlalchemy.orm import joinedload

    from database.database import get_database_session
    from database.models import Client
    from database.models import Consultant
    from database.models import Mission
    from services.consultant_service import ConsultantService

    imports_ok = True
except ImportError:
    # Imports échoués, on continue quand même
    pass


def show_consultant_missions(consultant):
    """
    Affiche la page complète des missions d'un consultant.

    Interface principale pour la gestion des missions incluant :
    - Liste des missions avec détails
    - Statistiques générales
    - Actions d'ajout/modification/suppression
    - Analyses et rapports de revenus

    Args:
        consultant: Objet Consultant dont on veut afficher les missions

    Raises:
        ImportError: Si les services de base ne sont pas disponibles
        Exception: Pour toute erreur lors de l'affichage ou des opérations DB

    Example:
        >>> consultant = ConsultantService.get_consultant_by_id(123)
        >>> show_consultant_missions(consultant)
        # Affiche la page complète des missions du consultant
    """

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


def _display_mission_period(mission):
    """Affiche la période de la mission."""
    st.markdown("**📅 Période**")
    if mission.date_debut:
        st.write(f"**Début :** {mission.date_debut.strftime('%d/%m/%Y')}")
    if mission.date_fin:
        st.write(f"**Fin :** {mission.date_fin.strftime('%d/%m/%Y')}")
    elif mission.en_cours:
        st.write("**Statut :** 🔄 En cours")


def _display_mission_client(mission):
    """Affiche les informations du client."""
    st.markdown("**🏢 Client**")
    if mission.client:
        st.write(f"**Nom :** {mission.client.nom}")
        if mission.client.secteur:
            st.write(f"**Secteur :** {mission.client.secteur}")


def _display_mission_remuneration(mission):
    """Affiche les informations de rémunération."""
    st.markdown("**💰 Rémunération**")
    if mission.tjm:
        st.write(f"**TJM Mission :** {mission.tjm:,}€")
    elif mission.taux_journalier:
        st.write(f"**TJM (ancien) :** {mission.taux_journalier:,}€")
    if mission.salaire_mensuel:
        st.write(f"**Salaire mensuel :** {mission.salaire_mensuel:,}€")


def _display_mission_info(mission):
    """Affiche les informations générales de la mission."""
    st.markdown("**📊 Informations**")
    if mission.description:
        st.write(f"**Description :** {mission.description[:100]}...")


def _display_mission_actions(mission):
    """Affiche les boutons d'action pour la mission."""
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


def show_mission_details(mission):
    """
    Affiche les détails d'une mission dans un expander Streamlit.

    Présente les informations clés de la mission :
    - Période (début/fin/statut)
    - Informations client
    - Rémunération (TJM, salaire mensuel)
    - Description et compétences
    - Actions disponibles (modifier, détails, supprimer)

    Args:
        mission: Objet Mission à afficher

    Note:
        Inclut des formulaires conditionnels pour modification
        et affichage des détails étendus selon l'état de session_state
    """

    col1, col2 = st.columns(2)

    with col1:
        _display_mission_period(mission)
        _display_mission_client(mission)

    with col2:
        _display_mission_remuneration(mission)
        _display_mission_info(mission)

    # Compétences utilisées
    if mission.competences_requises:
        st.markdown("**🛠️ Compétences requises**")
        st.write(mission.competences_requises)

    # Actions sur la mission
    _display_mission_actions(mission)

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
    """
    Affiche les statistiques générales des missions d'un consultant.

    Calcule et présente les métriques clés :
    - Nombre total de missions
    - Missions en cours vs terminées
    - Revenus estimés totaux

    Args:
        missions: Liste des objets Mission du consultant

    Note:
        Les revenus sont estimés sur 12 mois pour les missions sans date de fin,
        et calculés précisément pour les missions terminées.
    """

    if not missions:
        return

    st.markdown("#### 📊 Statistiques")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_missions = len(missions)
        st.metric("Total missions", total_missions)

    with col2:
        current_missions = sum(1 for m in missions if m.en_cours)
        st.metric(STATUS_EN_COURS, current_missions)

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


def _load_clients_for_mission():
    """Charge la liste des clients disponibles pour les missions"""
    with get_database_session() as session:
        clients = session.query(Client).all()
        client_options = {c.id: c.nom for c in clients}
    return client_options


def _render_mission_general_info():
    """Rend les champs d'informations générales de la mission"""
    st.markdown("#### 📋 Informations générales")

    titre = st.text_input(
        "Titre de la mission *", help="Titre descriptif de la mission"
    )

    client_options = _load_clients_for_mission()
    if not client_options:
        st.warning("⚠️ Aucun client trouvé. Veuillez créer des clients d'abord.")
        return None, None, None, None, None

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

    return titre, client_id, date_debut, date_fin, en_cours


def _render_mission_remuneration():
    """Rend les champs de rémunération de la mission"""
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

    return taux_journalier, tjm, salaire_mensuel


def _render_mission_description():
    """Rend les champs de description de la mission"""
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

    return description, competences_requises


def _handle_mission_form_submission(consultant_id: int, mission_data: dict):
    """Gère la soumission du formulaire de mission"""
    if validate_mission_form(
        mission_data["titre"],
        mission_data["client_id"],
        mission_data["date_debut"],
        mission_data["en_cours"],
        mission_data["date_fin"],
    ):
        success = create_mission(consultant_id, mission_data)

        if success:
            st.success("✅ Mission créée avec succès !")
            if "add_mission" in st.session_state:
                del st.session_state.add_mission
            st.rerun()
            return True
        else:
            st.error("❌ Erreur lors de la création de la mission")
            return False
    else:
        st.error("❌ Veuillez corriger les erreurs ci-dessus")
        return False


def show_add_mission_form(consultant_id: int):
    """
    Affiche le formulaire d'ajout d'une nouvelle mission.

    Formulaire complet avec validation incluant :
    - Informations générales (titre, client, dates)
    - Rémunération (TJM, salaire mensuel)
    - Description et compétences requises
    - Gestion des états (en cours/terminée)

    Args:
        consultant_id: ID du consultant pour lequel créer la mission

    Raises:
        Exception: En cas d'erreur lors du chargement des clients ou du formulaire

    Note:
        Supporte le nouveau champ TJM (V1.2.2) en plus de l'ancien taux_journalier
        pour assurer la compatibilité ascendante.
    """

    st.markdown("### ➕ Ajouter une mission")

    try:
        with st.form(f"add_mission_form_{consultant_id}", clear_on_submit=True):
            # Informations générales
            general_info = _render_mission_general_info()
            if general_info[0] is None:  # Pas de clients disponibles
                return

            titre, client_id, date_debut, date_fin, en_cours = general_info

            # Rémunération
            taux_journalier, tjm, salaire_mensuel = _render_mission_remuneration()

            # Description
            description, competences_requises = _render_mission_description()

            # Boutons
            col1, col2 = st.columns(2)

            with col1:
                submitted = st.form_submit_button("💾 Créer", type="primary")

            with col2:
                cancel = st.form_submit_button("❌ Annuler")

            if submitted:
                mission_data = {
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
                }
                _handle_mission_form_submission(consultant_id, mission_data)

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
    """
    Valide les données du formulaire de mission.

    Vérifications effectuées :
    - Titre obligatoire et non vide
    - Client obligatoire
    - Date de début obligatoire
    - Cohérence des dates (fin > début si applicable)

    Args:
        titre: Titre de la mission
        client_id: ID du client
        date_debut: Date de début de la mission
        en_cours: Si la mission est en cours
        date_fin: Date de fin (optionnel si en cours)

    Returns:
        bool: True si valide, False sinon (affiche les erreurs)

    Example:
        >>> is_valid = validate_mission_form(
        ...     "Projet Data", 123, date(2024, 1, 1), False, date(2024, 6, 30)
        ... )
        >>> print(is_valid)
        True
    """

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
    """
    Crée une nouvelle mission dans la base de données.

    Args:
        consultant_id: ID du consultant propriétaire de la mission
        data: Dictionnaire contenant les données de la mission :
            - titre: Titre de la mission
            - client_id: ID du client
            - date_debut: Date de début
            - date_fin: Date de fin (optionnel)
            - en_cours: Statut en cours
            - taux_journalier: TJM ancien format
            - tjm: TJM nouveau format (V1.2.2)
            - salaire_mensuel: Salaire mensuel fixe
            - description: Description détaillée
            - competences_requises: Compétences nécessaires

    Returns:
        bool: True si création réussie, False sinon

    Raises:
        Exception: En cas d'erreur de base de données

    Example:
        >>> data = {
        ...     "titre": "Projet Analytics",
        ...     "client_id": 123,
        ...     "date_debut": date(2024, 1, 1),
        ...     "en_cours": True,
        ...     "tjm": 450
        ... }
        >>> success = create_mission(456, data)
        >>> print(success)
        True
    """

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


def _load_mission_for_edit(mission_id: int):
    """Charge une mission pour modification."""
    with get_database_session() as session:
        mission = (
            session.query(Mission)
            .options(joinedload(Mission.client))
            .filter(Mission.id == mission_id)
            .first()
        )
        if not mission:
            return None, {}

        clients = session.query(Client).all()
        client_options = {c.id: c.nom for c in clients}
        return mission, client_options


def _render_edit_mission_general_info(mission, client_options):
    """Affiche la section informations générales du formulaire d'édition."""
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

    return titre, client_id, date_debut, en_cours, date_fin


def _render_edit_mission_remuneration(mission):
    """Affiche la section rémunération du formulaire d'édition."""
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

    return taux_journalier, salaire_mensuel


def _render_edit_mission_description(mission):
    """Affiche la section description du formulaire d'édition."""
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

    return description, competences_requises


def _handle_mission_update(mission_id, form_data):
    """Gère la mise à jour d'une mission."""
    titre, client_id, date_debut, en_cours, date_fin = form_data[:5]
    if validate_mission_form(titre, client_id, date_debut, en_cours, date_fin):
        taux_journalier, salaire_mensuel, description, competences_requises = form_data[
            5:
        ]
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


def _handle_mission_deletion(mission_id):
    """Gère la suppression d'une mission."""
    st.warning("⚠️ Cette action est irréversible !")
    if st.checkbox("Je confirme vouloir supprimer cette mission"):
        if delete_mission(mission_id):
            if "edit_mission" in st.session_state:
                del st.session_state.edit_mission
            st.rerun()


def _handle_mission_cancellation():
    """Gère l'annulation de l'édition d'une mission."""
    if "edit_mission" in st.session_state:
        del st.session_state.edit_mission
    st.rerun()


def _handle_edit_mission_buttons(mission_id, form_data):
    """Gère les actions des boutons du formulaire d'édition."""
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        submitted = st.form_submit_button("💾 Enregistrer", type="primary")

    with col2:
        cancel = st.form_submit_button("❌ Annuler")

    with col3:
        delete = st.form_submit_button("🗑️ Supprimer", type="secondary")

    if submitted:
        _handle_mission_update(mission_id, form_data)

    if delete:
        _handle_mission_deletion(mission_id)

    if cancel:
        _handle_mission_cancellation()


def show_edit_mission_form(mission_id: int):
    """
    Affiche le formulaire de modification d'une mission existante.

    Formulaire pré-rempli avec les données actuelles permettant :
    - Modification de toutes les informations
    - Gestion des statuts (en cours/terminée)
    - Suppression de la mission
    - Validation des modifications

    Args:
        mission_id: ID de la mission à modifier

    Raises:
        Exception: En cas d'erreur de chargement des données

    Note:
        Inclut une confirmation pour la suppression afin d'éviter
        les suppressions accidentelles.
    """

    st.markdown("### ✏️ Modifier une mission")

    try:
        mission, client_options = _load_mission_for_edit(mission_id)
        if not mission:
            st.error(MSG_MISSION_INTROUVABLE)
            return

        with st.form(f"edit_mission_form_{mission_id}", clear_on_submit=False):
            # Récupération des données du formulaire
            titre, client_id, date_debut, en_cours, date_fin = (
                _render_edit_mission_general_info(mission, client_options)
            )
            taux_journalier, salaire_mensuel = _render_edit_mission_remuneration(
                mission
            )
            description, competences_requises = _render_edit_mission_description(
                mission
            )

            # Gestion des boutons
            form_data = (
                titre,
                client_id,
                date_debut,
                en_cours,
                date_fin,
                taux_journalier,
                salaire_mensuel,
                description,
                competences_requises,
            )
            _handle_edit_mission_buttons(mission_id, form_data)

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du formulaire de modification: {e}")


def update_mission(mission_id: int, data: Dict[str, Any]) -> bool:
    """
    Met à jour une mission existante dans la base de données.

    Args:
        mission_id: ID de la mission à mettre à jour
        data: Dictionnaire contenant les nouvelles données (même format que create_mission)

    Returns:
        bool: True si mise à jour réussie, False sinon

    Raises:
        Exception: En cas d'erreur de base de données ou mission introuvable

    Example:
        >>> data = {"titre": "Nouveau titre", "en_cours": False}
        >>> success = update_mission(123, data)
        >>> print(success)
        True
    """

    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()

            if not mission:
                st.error(MSG_MISSION_INTROUVABLE)
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
    """
    Supprime une mission de la base de données.

    Args:
        mission_id: ID de la mission à supprimer

    Returns:
        bool: True si suppression réussie, False sinon

    Raises:
        Exception: En cas d'erreur de base de données

    Note:
        Opération irréversible - la mission et toutes ses données
        associées seront définitivement supprimées.

    Example:
        >>> success = delete_mission(123)
        >>> print(success)
        True
    """

    try:
        with get_database_session() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()

            if not mission:
                st.error(MSG_MISSION_INTROUVABLE)
                return False

            session.delete(mission)
            session.commit()

            st.info("✅ Mission supprimée")
            return True

    except Exception as e:
        st.error(f"❌ Erreur lors de la suppression de la mission: {e}")
        return False


def _display_mission_chronology(mission):
    """Affiche la chronologie d'une mission."""
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
        st.write(f"**Durée actuelle :** {duration_months} mois ({duration_days} jours)")
        st.write("**Statut :** 🔄 En cours")


def _display_mission_financial_aspects(mission):
    """Affiche les aspects financiers d'une mission."""
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


def _display_mission_descriptions(mission):
    """Affiche les descriptions et compétences d'une mission."""
    # Description complète
    if mission.description:
        st.markdown("#### 📝 Description détaillée")
        st.write(mission.description)

    # Compétences
    if mission.competences_requises:
        st.markdown("#### 🛠️ Compétences requises")
        st.write(mission.competences_requises)


def _display_mission_client_info(mission):
    """Affiche les informations client d'une mission."""
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


def show_mission_full_details(mission):
    """
    Affiche les détails complets et étendus d'une mission.

    Vue détaillée incluant :
    - Chronologie complète avec calcul de durée
    - Aspects financiers détaillés avec estimations
    - Description complète et compétences
    - Informations complètes du client
    - Bouton de fermeture

    Args:
        mission: Objet Mission dont afficher les détails complets

    Note:
        Calcule automatiquement la durée et les revenus estimés
        en fonction du statut de la mission (en cours/terminée).
    """

    st.markdown("### 📋 Détails complets de la mission")

    # Informations détaillées
    col1, col2 = st.columns(2)

    with col1:
        _display_mission_chronology(mission)

    with col2:
        _display_mission_financial_aspects(mission)

    _display_mission_descriptions(mission)
    _display_mission_client_info(mission)

    # Bouton pour fermer
    if st.button("❌ Fermer les détails", key=f"close_details_{mission.id}"):
        del st.session_state.view_mission_details
        st.rerun()


def _calculate_mission_statistics(missions):
    """Calcule les statistiques des missions par client et statut."""
    # Analyse par client
    client_counts = {}
    for mission in missions:
        client_name = mission.client.nom if mission.client else "Client inconnu"
        client_counts[client_name] = client_counts.get(client_name, 0) + 1

    # Analyse par statut
    status_counts = {
        STATUS_EN_COURS: sum(1 for m in missions if m.en_cours),
        "Terminées": sum(1 for m in missions if m.date_fin and not m.en_cours),
        "Planifiées": sum(
            1
            for m in missions
            if not m.en_cours
            and not m.date_fin
            and m.date_debut > datetime.now().date()
        ),
    }

    return client_counts, status_counts


def _display_missions_by_client_and_status(client_counts, status_counts):
    """Affiche la répartition par client et statut."""
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


def _group_missions_by_year(missions):
    """Groupe les missions par année."""
    missions_by_year = {}
    for mission in missions:
        if mission.date_debut:
            year = mission.date_debut.year
            if year not in missions_by_year:
                missions_by_year[year] = []
            missions_by_year[year].append(mission)
    return missions_by_year


def _calculate_year_revenue(year_missions, year):
    """Calcule les revenus pour une année donnée."""
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
    return year_revenue


def _analyze_missions_by_year(missions):
    """Analyse temporelle des missions par année avec revenus."""
    st.markdown("#### 📈 Analyse temporelle")

    missions_by_year = _group_missions_by_year(missions)

    for year in sorted(missions_by_year.keys(), reverse=True):
        year_missions = missions_by_year[year]
        st.write(f"**{year} :** {len(year_missions)} mission(s)")

        year_revenue = _calculate_year_revenue(year_missions, year)
        if year_revenue > 0:
            st.write(f"**Revenus {year} :** {year_revenue:,.0f}€")


def show_missions_analysis(missions):
    """
    Affiche une analyse complète des missions d'un consultant.

    Analyse multi-dimensionnelle incluant :
    - Répartition par client
    - Répartition par statut (en cours/terminées/planifiées)
    - Analyse temporelle par année
    - Calcul des revenus par année

    Args:
        missions: Liste des objets Mission à analyser

    Note:
        Les analyses temporelles sont groupées par année
        avec calcul automatique des revenus estimés.
    """

    st.markdown("### 📊 Analyse des missions")

    if not missions:
        st.info("ℹ️ Aucune mission à analyser")
        return

    client_counts, status_counts = _calculate_mission_statistics(missions)
    _display_missions_by_client_and_status(client_counts, status_counts)
    _analyze_missions_by_year(missions)


def _calculate_mission_revenue(mission):
    """Calcule le revenu d'une mission."""
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

    return revenue


def _build_revenue_data(missions):
    """Construit les données de revenus pour toutes les missions."""
    revenue_data = []
    total_revenue = 0

    for mission in missions:
        revenue = _calculate_mission_revenue(mission)

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

    return revenue_data, total_revenue


def _display_revenue_statistics(missions, total_revenue):
    """Affiche les statistiques globales des revenus."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total revenus", f"{total_revenue:,.0f}€")

    with col2:
        tjm_missions = [m for m in missions if m.taux_journalier]
        if tjm_missions:
            avg_tjm = sum(m.taux_journalier for m in tjm_missions) / len(tjm_missions)
            st.metric("TJM moyen", f"{avg_tjm:,.0f}€")
        else:
            st.metric("TJM moyen", "N/A")

    with col3:
        active_missions = sum(1 for m in missions if m.en_cours)
        st.metric("Missions actives", active_missions)


def show_missions_revenues(missions):
    """
    Affiche l'analyse détaillée des revenus des missions.

    Présente un tableau complet avec :
    - Revenus par mission (calculés précisément)
    - TJM moyen global
    - Nombre de missions actives
    - Tri par revenus décroissants
    - Statistiques financières globales

    Args:
        missions: Liste des objets Mission pour l'analyse financière

    Note:
        Les revenus sont calculés en jours ouvrés (5 jours/semaine)
        pour les missions terminées et en cours.
        Utilise pandas pour la présentation tabulaire.
    """

    st.markdown("### 📈 Analyse des revenus")

    if not missions:
        st.info("ℹ️ Aucune mission pour analyser les revenus")
        return

    revenue_data, total_revenue = _build_revenue_data(missions)

    if revenue_data:
        import pandas as pd

        df = pd.DataFrame(revenue_data)

        # Trier par revenus décroissants
        df = df.sort_values("Revenus", ascending=False)

        # Formater les colonnes
        df["Revenus"] = df["Revenus"].apply(lambda x: f"{x:,.0f}€")
        df["TJM"] = df["TJM"].apply(lambda x: f"{x:,}€" if x > 0 else "N/A")

        st.dataframe(df, width="stretch", hide_index=True)

        _display_revenue_statistics(missions, total_revenue)

    else:
        st.info("ℹ️ Aucune donnée de revenus disponible")
