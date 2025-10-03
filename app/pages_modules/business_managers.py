from datetime import date
from datetime import datetime

import pandas as pd
import streamlit as st
from sqlalchemy import and_

from app.database.database import get_database_session
from app.database.models import BusinessManager
from app.database.models import Consultant
from app.database.models import ConsultantBusinessManager
from app.database.models import Mission
from app.services.business_manager_service import BusinessManagerService
from app.pages_modules.dashboard_page import show_dashboard_page

# Constantes pour éviter la duplication
TELEPHONE_LABEL = "Téléphone"
DATE_FORMAT = "%d/%m/%Y"
DUREE_LABEL = "Durée"

# Messages d'erreur fréquents
ERROR_INVALID_BM_ID = "❌ Erreur : ID du Business Manager invalide"
ERROR_GENERIC = "❌ Erreur : {}"
ERROR_ASSIGNMENT = "❌ Erreur lors de l'assignation : {}"
ERROR_PROFILE_LOADING = "❌ Erreur lors du chargement du profil : {}"
ERROR_UPDATE = "❌ Erreur lors de la mise à jour : {}"
ERROR_DELETE = "❌ Erreur lors de la suppression : {}"
ERROR_LIST_LOADING = "❌ Erreur lors du chargement de la liste : {}"
ERROR_CREATION = "❌ Erreur lors de la création : {}"
ERROR_STATISTICS = "❌ Erreur lors du calcul des statistiques : {}"

# Messages de succès fréquents
SUCCESS_BM_CREATED = "✅ Business Manager {} {} créé avec succès !"
SUCCESS_TRANSFER = "✅ Transfert réussi ! {} {} est maintenant assigné(e) à {} {}"
SUCCESS_ASSIGNMENT = "✅ Assignation créée ! {} {} est maintenant assigné(e) à {} {}"

# Messages d'information
INFO_ASSIGNMENT_CLOSE = "✅ En confirmant, l'assignation actuelle sera automatiquement clôturée et une nouvelle assignation sera créée."


def _validate_and_convert_bm_id(bm_id):
    """Valide et convertit l'ID du Business Manager en entier."""
    # S'assurer que bm_id est un entier
    if isinstance(bm_id, str):
        try:
            return int(bm_id)
        except ValueError as e:
            st.error(f"❌ Erreur : ID du Business Manager invalide ({bm_id})")
            print(
                f"Erreur de conversion d'ID dans show_bm_profile: {e}, valeur: {bm_id}, type: {type(bm_id)}"
            )
            return None
    elif not isinstance(bm_id, int):
        try:
            return int(str(bm_id))
        except (ValueError, TypeError) as e:
            st.error(f"❌ Erreur : ID du Business Manager invalide ({bm_id})")
            print(
                f"Erreur de conversion d'ID dans show_bm_profile: {e}, valeur: {bm_id}, type: {type(bm_id)}"
            )
            return None
    return bm_id


def _display_bm_header_and_info(bm):
    """Affiche l'en-tête et les informations générales du BM."""
    # En-tête avec bouton retour
    col1, col2 = st.columns([6, 1])

    with col1:
        st.title(f"👔 Profil de {bm.prenom} {bm.nom}")

    with col2:
        if st.button("← Retour", key="back_to_bm_list"):
            del st.session_state.view_bm_profile
            st.rerun()

    st.markdown("---")


def _display_bm_general_info(bm, session):
    """Affiche les informations générales et métriques du BM."""
    # Informations principales du BM
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Informations générales")
        st.write(f"**Nom complet :** {bm.prenom} {bm.nom}")
        st.write(f"**Email :** {bm.email}")
        st.write(f"**{TELEPHONE_LABEL} :** {bm.telephone or 'Non renseigné'}")
        st.write(
            f"**Date de création :** {bm.date_creation.strftime(DATE_FORMAT) if bm.date_creation else 'N/A'}"
        )
        st.write(f"**Statut :** {'🟢 Actif' if bm.actif else '🔴 Inactif'}")

    with col2:
        # Métriques
        consultants_count = (
            session.query(ConsultantBusinessManager)
            .filter(
                and_(
                    ConsultantBusinessManager.business_manager_id == bm.id,
                    ConsultantBusinessManager.date_fin.is_(None),
                )
            )
            .count()
        )

        st.metric("👥 Consultants actuels", consultants_count)

        # Actions sur le BM
        st.subheader("🔧 Actions")

        col_edit, col_delete = st.columns(2)

        with col_edit:
            if st.button("✏️ Modifier", width="stretch"):
                st.session_state.edit_bm_mode = True

        with col_delete:
            if st.button("🗑️ Supprimer", width="stretch", type="primary"):
                st.session_state.delete_bm_mode = True


def _handle_bm_form_actions(bm):
    """Gère l'affichage des formulaires de modification et suppression."""
    # Formulaire de modification
    if st.session_state.get("edit_bm_mode", False):
        show_edit_bm_form(bm)

    # Confirmation de suppression
    if st.session_state.get("delete_bm_mode", False):
        show_delete_bm_confirmation(bm)


def show():
    """
    Interface complète de gestion des Business Managers.

    Page principale offrant une navigation par onglets pour :
    - Consulter la liste des Business Managers
    - Créer un nouveau Business Manager
    - Visualiser les statistiques globales
    - Accéder aux profils détaillés individuels

    Cette fonction gère également l'état de session pour la navigation
    entre les différents profils de Business Managers.

    Raises:
        Exception: En cas d'erreur lors de l'initialisation de l'interface
    """
    st.title("👔 Gestion des Business Managers")

    # Vérifier si on doit afficher le profil d'un BM spécifique
    if "view_bm_profile" in st.session_state:
        show_bm_profile()
        return

    # Navigation par onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Liste des BMs", "➕ Nouveau BM", "📊 Statistiques", "📊 Dashboard"])

    with tab1:
        show_business_managers_list()

    with tab2:
        show_add_business_manager()

    with tab3:
        show_statistics()

    with tab4:
        show_dashboard_page()


def show_bm_profile():
    """
    Affiche le profil détaillé d'un Business Manager.

    Interface complète incluant :
    - Informations générales du BM (nom, email, téléphone, statut)
    - Métriques des consultants assignés
    - Actions de modification et suppression
    - Gestion des assignations de consultants
    - Historique des assignations

    La fonction récupère l'ID du BM depuis l'état de session
    et gère les erreurs de conversion d'ID.

    Raises:
        ValueError: Si l'ID du BM n'est pas convertible en entier
        Exception: Pour toute erreur lors de la récupération des données
    """
    bm_id = st.session_state.view_bm_profile

    # Valider et convertir l'ID
    validated_id = _validate_and_convert_bm_id(bm_id)
    if validated_id is None:
        del st.session_state.view_bm_profile
        st.rerun()
        return

    try:
        with get_database_session() as session:
            bm = (
                session.query(BusinessManager)
                .filter(BusinessManager.id == validated_id)
                .first()
            )

            if not bm:
                st.error("❌ Business Manager introuvable")
                del st.session_state.view_bm_profile
                st.rerun()
                return

            # Afficher l'en-tête et informations
            _display_bm_header_and_info(bm)
            _display_bm_general_info(bm, session)

            # Gestion des formulaires
            _handle_bm_form_actions(bm)

            st.markdown("---")

            # Gestion des assignations consultants
            show_bm_consultants_management(bm, session)

    except Exception as e:
        st.error(ERROR_PROFILE_LOADING.format(e))


def show_edit_bm_form(bm):
    """
    Formulaire de modification d'un Business Manager existant.

    Interface d'édition incluant :
    - Pré-remplissage des champs avec les données actuelles
    - Validation des modifications apportées
    - Gestion des champs optionnels (téléphone, notes)
    - Mise à jour automatique de la date de dernière modification
    - Gestion des erreurs et confirmation de succès

    Args:
        bm (BusinessManager): Instance du Business Manager à modifier

    Returns:
        None: Affiche directement le formulaire dans l'interface Streamlit

    Raises:
        Exception: En cas d'erreur lors de la mise à jour en base de données

    Note:
        La fonction utilise une session de base de données séparée
        pour éviter les conflits de transactions.
    """
    st.subheader("✏️ Modifier les informations")

    with st.form("edit_bm_form"):
        col1, col2 = st.columns(2)

        with col1:
            new_nom = st.text_input("Nom", value=bm.nom)
            new_email = st.text_input("Email", value=bm.email)
            new_actif = st.checkbox("Actif", value=bm.actif)

        with col2:
            new_prenom = st.text_input("Prénom", value=bm.prenom)
            new_telephone = st.text_input(TELEPHONE_LABEL, value=bm.telephone or "")

        new_notes = st.text_area("Notes", value=bm.notes or "", height=100)

        col_submit, col_cancel = st.columns(2)

        with col_submit:
            submitted = st.form_submit_button("💾 Mettre à jour", type="primary")

        with col_cancel:
            cancelled = st.form_submit_button("❌ Annuler")

        if cancelled:
            st.session_state.edit_bm_mode = False
            st.rerun()

        if submitted:
            try:
                with get_database_session() as session:
                    bm_to_update = session.query(BusinessManager).get(bm.id)
                    if bm_to_update:
                        bm_to_update.nom = new_nom.strip()
                        bm_to_update.prenom = new_prenom.strip()
                        bm_to_update.email = new_email.strip().lower()
                        bm_to_update.telephone = (
                            new_telephone.strip() if new_telephone else None
                        )
                        bm_to_update.actif = new_actif
                        bm_to_update.notes = new_notes.strip() if new_notes else None
                        bm_to_update.derniere_maj = datetime.now()

                        session.commit()
                        st.success("✅ Business Manager mis à jour avec succès !")
                        st.session_state.edit_bm_mode = False
                        st.rerun()

            except Exception as e:
                st.error(ERROR_UPDATE.format(e))


def show_delete_bm_confirmation(bm):
    """
    Interface de confirmation de suppression d'un Business Manager.

    Fonctionnalités incluses :
    - Vérification des assignations actives avant suppression
    - Affichage des conséquences de la suppression
    - Clôture automatique des assignations actives
    - Gestion des confirmations utilisateur
    - Messages d'avertissement et d'information

    Args:
        bm (BusinessManager): Instance du Business Manager à supprimer

    Returns:
        None: Affiche directement l'interface de confirmation

    Raises:
        Exception: En cas d'erreur lors de la suppression ou de la clôture des assignations

    Note:
        La suppression clôture automatiquement toutes les assignations actives
        avec un commentaire explicatif dans l'historique.
    """
    st.subheader("🗑️ Confirmer la suppression")

    # Vérifier les assignations
    try:
        with get_database_session() as session:
            assignments_count = (
                session.query(ConsultantBusinessManager)
                .filter(
                    and_(
                        ConsultantBusinessManager.business_manager_id == bm.id,
                        ConsultantBusinessManager.date_fin.is_(None),
                    )
                )
                .count()
            )

            total_assignments = (
                session.query(ConsultantBusinessManager)
                .filter(ConsultantBusinessManager.business_manager_id == bm.id)
                .count()
            )

            if assignments_count > 0:
                st.warning(
                    f"⚠️ Ce Business Manager a **{assignments_count}** consultant(s) actuellement assigné(s)."
                )
                st.info("La suppression clôturera automatiquement ces assignations.")

            if total_assignments > 0:
                st.info(f"📋 Historique total : **{total_assignments}** assignation(s)")

            st.error(
                f"🚨 **Êtes-vous sûr de vouloir supprimer {bm.prenom} {bm.nom} ?**"
            )
            st.write("Cette action est **irréversible**.")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🗑️ Oui, supprimer", type="primary", width="stretch"):
                    try:
                        # Clôturer les assignations actives
                        active_assignments = (
                            session.query(ConsultantBusinessManager)
                            .filter(
                                and_(
                                    ConsultantBusinessManager.business_manager_id
                                    == bm.id,
                                    ConsultantBusinessManager.date_fin.is_(None),
                                )
                            )
                            .all()
                        )

                        for assignment in active_assignments:
                            assignment.date_fin = datetime.now().date()
                            assignment.commentaire = (
                                f"BM supprimé le {datetime.now().strftime(DATE_FORMAT)}"
                            )

                        # Supprimer le BM - utiliser une nouvelle session pour éviter
                        # les conflits
                        with get_database_session() as delete_session:
                            # Récupérer le BM dans la nouvelle session
                            bm_to_delete = (
                                delete_session.query(BusinessManager)
                                .filter(BusinessManager.id == bm.id)
                                .first()
                            )
                            if bm_to_delete:
                                delete_session.delete(bm_to_delete)
                                delete_session.commit()

                        st.success(
                            f"✅ Business Manager {bm.prenom} {bm.nom} supprimé avec succès !"
                        )
                        del st.session_state.view_bm_profile
                        del st.session_state.delete_bm_mode
                        st.rerun()

                    except Exception as e:
                        st.error(ERROR_DELETE.format(e))

            with col2:
                if st.button("❌ Non, annuler", width="stretch"):
                    st.session_state.delete_bm_mode = False
                    st.rerun()

            with col3:
                st.write("")  # Espacement

    except Exception as e:
        st.error(f"❌ Erreur : {e}")


def show_bm_consultants_management(bm, session):
    """
    Interface complète de gestion des consultants assignés à un Business Manager.

    Organisation par onglets :
    - Consultants actuels : liste avec actions (terminer assignation, commentaires)
    - Nouvelle assignation : formulaire d'ajout avec gestion des transferts
    - Historique : vue complète de toutes les assignations passées

    Args:
        bm (BusinessManager): Instance du Business Manager
        session (Session): Session SQLAlchemy active

    Returns:
        None: Affiche directement l'interface de gestion

    Note:
        La fonction gère les transferts de consultants entre Business Managers
        en clôturant automatiquement les assignations précédentes.
    """
    st.subheader(f"👥 Consultants de {bm.prenom} {bm.nom}")

    # Onglets pour les consultants
    tab1, tab2, tab3 = st.tabs(
        ["👥 Consultants actuels", "➕ Nouvelle assignation", "📊 Historique"]
    )

    with tab1:
        show_current_bm_consultants(bm, session)

    with tab2:
        show_add_bm_assignment(bm, session)

    with tab3:
        show_bm_assignments_history(bm, session)


def _get_current_assignments(bm_id, session):
    """Récupère les assignations actuelles du Business Manager."""
    return (
        session.query(ConsultantBusinessManager, Consultant)
        .join(Consultant, ConsultantBusinessManager.consultant_id == Consultant.id)
        .filter(
            and_(
                ConsultantBusinessManager.business_manager_id == bm_id,
                ConsultantBusinessManager.date_fin.is_(None),
            )
        )
        .all()
    )


def _get_mission_data(consultant, session):
    """Récupère les données de mission pour un consultant."""
    mission_en_cours = (
        session.query(Mission)
        .filter(
            and_(
                Mission.consultant_id == consultant.id,
                Mission.statut == "en_cours",
            )
        )
        .order_by(Mission.date_debut.desc())
        .first()
    )

    # Préparer les données de mission
    client_mission = mission_en_cours.client if mission_en_cours else "N/A"
    role_mission = (
        mission_en_cours.role if mission_en_cours and mission_en_cours.role else "N/A"
    )

    # Extraire la logique de récupération du TJM
    tjm_mission = "N/A"
    if mission_en_cours:
        if mission_en_cours.tjm:
            tjm_mission = mission_en_cours.tjm
        elif mission_en_cours.taux_journalier:
            tjm_mission = mission_en_cours.taux_journalier

    date_debut_mission = (
        mission_en_cours.date_debut.strftime(DATE_FORMAT) if mission_en_cours else "N/A"
    )

    return {
        "client": client_mission,
        "role": role_mission,
        "tjm": tjm_mission,
        "date_debut": date_debut_mission,
    }


def _format_consultant_data(assignment, consultant, mission_data):
    """Formate les données d'un consultant pour le tableau."""
    # Formatage du TJM
    tjm_display = (
        f"{mission_data['tjm']}€"
        if isinstance(mission_data["tjm"], (int, float))
        else mission_data["tjm"]
    )

    # Formatage du salaire
    salaire_display = (
        f"{consultant.salaire_actuel}€" if consultant.salaire_actuel else "N/A"
    )

    return {
        "Consultant": f"{consultant.prenom} {consultant.nom}",
        "Email": consultant.email,
        "Type Contrat": consultant.type_contrat or "N/A",
        "Disponibilité": ("🟢 Disponible" if consultant.disponibilite else "🔴 Occupé"),
        "Client actuel": mission_data["client"],
        "Rôle mission": mission_data["role"],
        "TJM": tjm_display,
        "Salaire": salaire_display,
        "Début mission": mission_data["date_debut"],
        "Date assignation": assignment.date_debut.strftime(DATE_FORMAT),
        DUREE_LABEL: (
            (datetime.now().date() - assignment.date_debut).days
            if assignment.date_debut
            else 0
        ),
        "Commentaire": assignment.commentaire or "Aucun",
    }


def _handle_assignment_selection(current_assignments, data, session):
    """Gère la sélection et les actions sur les assignations."""
    # Affichage avec sélection
    event = st.dataframe(
        pd.DataFrame(data),
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
    )

    # Actions sur sélection
    if event.selection.rows:
        selected_row = event.selection.rows[0]
        # Convertir en entier au cas où c'est une chaîne (bug Streamlit)
        try:
            selected_row = int(selected_row)
        except (ValueError, TypeError):
            st.error("❌ Erreur : Index de ligne invalide")
            return

        selected_consultant_name = data[selected_row]["Consultant"]
        assignment_to_end = current_assignments[selected_row][0]

        st.success(f"✅ Consultant sélectionné : **{selected_consultant_name}**")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔚 Terminer l'assignation", type="primary"):
                _end_assignment(assignment_to_end, session)

        with col2:
            # Ajouter commentaire
            if st.button("📝 Ajouter un commentaire"):
                st.session_state.add_comment_assignment = assignment_to_end.id


def _end_assignment(assignment_to_end, session):
    """Termine une assignation."""
    try:
        assignment_to_end.date_fin = datetime.now().date()
        assignment_to_end.commentaire = (
            f"Assignation terminée le {datetime.now().strftime(DATE_FORMAT)}"
        )
        session.commit()
        st.success("✅ Assignation terminée avec succès !")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Erreur : {e}")


def _handle_comment_form(session):
    """Gère le formulaire d'ajout de commentaire."""
    if st.session_state.get("add_comment_assignment"):
        assignment_id = st.session_state.add_comment_assignment

        with st.form("comment_form"):
            comment = st.text_area("Commentaire", height=100)

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Ajouter"):
                    _add_comment_to_assignment(assignment_id, comment, session)

            with col2:
                if st.form_submit_button("❌ Annuler"):
                    del st.session_state.add_comment_assignment
                    st.rerun()


def _add_comment_to_assignment(assignment_id, comment, session):
    """Ajoute un commentaire à une assignation."""
    try:
        assignment = session.query(ConsultantBusinessManager).get(assignment_id)
        if assignment:
            existing_comment = assignment.commentaire or ""
            date_str = datetime.now().strftime(DATE_FORMAT)
            new_comment = (
                f"{existing_comment}\n{date_str}: {comment}"
                if existing_comment
                else f"{date_str}: {comment}"
            )
            assignment.commentaire = new_comment
            session.commit()
            st.success("✅ Commentaire ajouté !")
            del st.session_state.add_comment_assignment
            st.rerun()
    except Exception as e:
        st.error(f"❌ Erreur : {e}")


def show_current_bm_consultants(bm, session):
    """
    Affiche la liste des consultants actuellement assignés au Business Manager.

    Fonctionnalités incluses :
    - Liste détaillée avec informations de mission en cours
    - Sélection interactive de consultants
    - Actions sur les assignations (terminer, commenter)
    - Affichage des métriques de mission (client, rôle, TJM, salaire)
    - Gestion des commentaires sur les assignations

    Args:
        bm (BusinessManager): Instance du Business Manager
        session (Session): Session SQLAlchemy active

    Returns:
        None: Affiche directement la liste dans l'interface Streamlit

    Raises:
        Exception: En cas d'erreur lors des requêtes de base de données

    Note:
        La fonction récupère automatiquement les informations de mission
        en cours pour chaque consultant assigné.
    """
    try:
        # Récupérer les assignations actuelles
        current_assignments = _get_current_assignments(bm.id, session)

        if not current_assignments:
            st.info("👥 Aucun consultant actuellement assigné")
            return

        # Construire les données du tableau
        data = []
        for assignment, consultant in current_assignments:
            mission_data = _get_mission_data(consultant, session)
            consultant_data = _format_consultant_data(
                assignment, consultant, mission_data
            )
            data.append(consultant_data)

        # Gestion de la sélection et des actions
        _handle_assignment_selection(current_assignments, data, session)

        # Formulaire de commentaire
        _handle_comment_form(session)

    except Exception as e:
        st.error(f"❌ Erreur : {e}")


def _get_consultant_assignment_status(bm_id, session):
    """Récupère le statut d'assignation des consultants pour un BM."""
    # Récupérer les consultants déjà assignés à ce BM
    assigned_consultant_ids = [
        cbm.consultant_id
        for cbm in session.query(ConsultantBusinessManager)
        .filter(
            and_(
                ConsultantBusinessManager.business_manager_id == bm_id,
                ConsultantBusinessManager.date_fin.is_(None),
            )
        )
        .all()
    ]

    # Récupérer TOUS les consultants
    all_consultants = session.query(Consultant).all()

    # Séparer les consultants selon leur statut d'assignation
    available_consultants = []
    assigned_to_other_bm = []

    for consultant in all_consultants:
        if consultant.id in assigned_consultant_ids:
            continue  # Déjà assigné à ce BM

        # Vérifier s'il a une assignation active avec un autre BM
        existing_assignment = (
            session.query(ConsultantBusinessManager)
            .filter(
                and_(
                    ConsultantBusinessManager.consultant_id == consultant.id,
                    ConsultantBusinessManager.date_fin.is_(None),
                )
            )
            .first()
        )

        if existing_assignment:
            # Récupérer le BM actuel
            current_bm = (
                session.query(BusinessManager)
                .filter(BusinessManager.id == existing_assignment.business_manager_id)
                .first()
            )
            assigned_to_other_bm.append((consultant, current_bm, existing_assignment))
        else:
            available_consultants.append(consultant)

    return available_consultants, assigned_to_other_bm


def _build_consultant_options(available_consultants, assigned_to_other_bm):
    """Construit les options de sélection des consultants."""
    consultant_options = {}

    # Consultants disponibles (aucune assignation active)
    if available_consultants:
        st.write("**🟢 Consultants disponibles :**")
        for consultant in available_consultants:
            key = f"🟢 {consultant.prenom} {consultant.nom} ({consultant.email}) - DISPONIBLE"
            consultant_options[key] = {
                "consultant": consultant,
                "status": "available",
                "existing_assignment": None,
                "current_bm": None,
            }

    # Consultants assignés à d'autres BMs
    if assigned_to_other_bm:
        st.write("**🔄 Consultants assignés à d'autres BMs (nécessite transfert) :**")
        for consultant, current_bm, existing_assignment in assigned_to_other_bm:
            since_date = existing_assignment.date_debut.strftime(DATE_FORMAT)
            key = f"🔄 {consultant.prenom} {consultant.nom} ({consultant.email}) - Actuellement avec {current_bm.prenom} {current_bm.nom} depuis le {since_date}"
            consultant_options[key] = {
                "consultant": consultant,
                "status": "assigned",
                "existing_assignment": existing_assignment,
                "current_bm": current_bm,
            }

    return consultant_options


def _process_assignment_creation(
    bm, selected_consultant_data, date_debut, commentaire, session
):
    """Traite la création d'une nouvelle assignation."""
    consultant = selected_consultant_data["consultant"]
    status = selected_consultant_data["status"]
    existing_assignment = selected_consultant_data["existing_assignment"]
    current_bm = selected_consultant_data["current_bm"]

    # Si transfert nécessaire, clôturer l'assignation existante
    if status == "assigned" and existing_assignment:
        existing_assignment.date_fin = datetime.now().date()
        existing_assignment.commentaire = f"Transfert vers {bm.prenom} {bm.nom} le {datetime.now().strftime(DATE_FORMAT)}"

    # Créer la nouvelle assignation
    new_assignment = ConsultantBusinessManager(
        consultant_id=consultant.id,
        business_manager_id=bm.id,
        date_debut=date_debut or datetime.now().date(),
        commentaire=commentaire
        or (
            f"Transfert depuis {current_bm.prenom} {current_bm.nom}"
            if status == "assigned"
            else "Nouvelle assignation"
        ),
    )

    session.add(new_assignment)
    session.commit()

    success_message = (
        f"✅ {consultant.prenom} {consultant.nom} transféré depuis {current_bm.prenom} {current_bm.nom} vers {bm.prenom} {bm.nom} !"
        if status == "assigned"
        else f"✅ {consultant.prenom} {consultant.nom} assigné à {bm.prenom} {bm.nom} !"
    )

    return success_message


def show_add_bm_assignment(bm, session):
    """
    Formulaire d'ajout d'une nouvelle assignation consultant-Business Manager.

    Gestion intelligente des assignations :
    - Séparation des consultants disponibles et déjà assignés
    - Gestion des transferts depuis d'autres BMs
    - Validation des dates et commentaires
    - Clôture automatique des assignations précédentes lors de transferts

    Args:
        bm (BusinessManager): Business Manager cible de l'assignation
        session (Session): Session SQLAlchemy active

    Returns:
        None: Affiche directement le formulaire dans l'interface Streamlit

    Raises:
        Exception: En cas d'erreur lors de la création de l'assignation

    Note:
        La fonction gère automatiquement les transferts en clôturant
        les assignations existantes avec des commentaires explicatifs.
    """
    try:
        # Récupérer les consultants non assignés à ce BM
        assigned_consultant_ids = [
            cbm.consultant_id
            for cbm in session.query(ConsultantBusinessManager)
            .filter(
                and_(
                    ConsultantBusinessManager.business_manager_id == bm.id,
                    ConsultantBusinessManager.date_fin.is_(None),
                )
            )
            .all()
        ]

        # Récupérer TOUS les consultants (pas seulement les disponibles)
        all_consultants = session.query(Consultant).all()

        # Séparer les consultants selon leur statut d'assignation
        available_consultants, assigned_to_other_bm = _separate_consultants_by_status(
            all_consultants, assigned_consultant_ids, session
        )

        with st.form("add_bm_assignment_form"):
            st.write(f"**Assigner un consultant à {bm.prenom} {bm.nom}**")

            # Construire les options selon le statut
            consultant_options = _build_consultant_options_for_assignment(
                available_consultants, assigned_to_other_bm
            )

            if not consultant_options:
                st.info(
                    "👥 Tous les consultants sont déjà assignés à ce Business Manager"
                )
                st.form_submit_button("Fermer", disabled=True)
                return

            # Sélection consultant
            selected_consultant_key = st.selectbox(
                "Consultant à assigner", list(consultant_options.keys())
            )

            # Date de début (optionnelle)
            date_debut = st.date_input("Date de début", value=datetime.now().date())

            # Commentaire optionnel
            commentaire = st.text_area("Commentaire (optionnel)", height=80)

            selected_data = consultant_options[selected_consultant_key]

            # Afficher un avertissement si le consultant est déjà assigné
            cloture_comment = None
            if selected_data["status"] == "assigned":
                st.warning(
                    f"⚠️ **ATTENTION :** Ce consultant est actuellement assigné à {selected_data['current_bm'].prenom} {selected_data['current_bm'].nom}"
                )
                st.info(INFO_ASSIGNMENT_CLOSE)

                # Commentaire pour la clôture de l'ancienne assignation
                cloture_comment = st.text_input(
                    "Raison du transfert (optionnel)",
                    placeholder="Ex: Changement d'équipe, réorganisation...",
                    help="Ce commentaire sera ajouté à l'ancienne assignation lors de sa clôture",
                )

                submit_text = "🔄 Confirmer le transfert"
                submit_type = "primary"
            else:
                submit_text = "🔗 Créer l'assignation"
                submit_type = "secondary"

            submitted = st.form_submit_button(submit_text, type=submit_type)

            if submitted:
                consultant = selected_data["consultant"]

                try:
                    # Si le consultant est déjà assigné, clôturer l'ancienne assignation
                    if selected_data["status"] == "assigned":
                        _handle_assignment_transfer(
                            selected_data, date_debut, bm, cloture_comment
                        )

                    # Créer la nouvelle assignation
                    _create_new_assignment(
                        consultant, bm, date_debut, commentaire, session
                    )
                    session.commit()

                    # Afficher le message de succès approprié
                    _display_assignment_success_message(selected_data, consultant, bm)

                except Exception as e:
                    st.error(f"❌ Erreur lors de l'assignation : {e}")
                    session.rollback()

    except Exception as e:
        st.error(f"❌ Erreur : {e}")


def show_bm_assignments_history(bm, session):
    """
    Affiche l'historique complet des assignations d'un Business Manager.

    Vue historique incluant :
    - Toutes les assignations (actives et terminées)
    - Durée des assignations calculée automatiquement
    - Statut visuel (actif/terminé)
    - Commentaires associés aux assignations
    - Métriques globales (total, actives, terminées)

    Args:
        bm (BusinessManager): Instance du Business Manager
        session (Session): Session SQLAlchemy active

    Returns:
        None: Affiche directement l'historique dans l'interface Streamlit

    Raises:
        Exception: En cas d'erreur lors des requêtes de base de données

    Note:
        L'historique est trié par date de début décroissante
        pour afficher les assignations les plus récentes en premier.
    """
    try:
        # Toutes les assignations (actives et terminées)
        all_assignments = (
            session.query(ConsultantBusinessManager, Consultant)
            .join(Consultant, ConsultantBusinessManager.consultant_id == Consultant.id)
            .filter(ConsultantBusinessManager.business_manager_id == bm.id)
            .order_by(ConsultantBusinessManager.date_debut.desc())
            .all()
        )

        if not all_assignments:
            st.info("📊 Aucun historique d'assignation")
            return

        # Tableau de l'historique
        data = []
        for assignment, consultant in all_assignments:
            statut = "🟢 Active" if assignment.date_fin is None else "🔴 Terminée"
            duree = (
                "En cours"
                if assignment.date_fin is None
                else f"{(assignment.date_fin - assignment.date_debut).days} jours"
            )

            data.append(
                {
                    "Consultant": f"{consultant.prenom} {consultant.nom}",
                    "Début": assignment.date_debut.strftime(DATE_FORMAT),
                    "Fin": (
                        assignment.date_fin.strftime(DATE_FORMAT)
                        if assignment.date_fin
                        else "-"
                    ),
                    DUREE_LABEL: duree,
                    "Statut": statut,
                    "Commentaire": assignment.commentaire or "-",
                }
            )

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "Consultant": st.column_config.TextColumn("Consultant", width="large"),
                "Début": st.column_config.TextColumn("Date début", width="medium"),
                "Fin": st.column_config.TextColumn("Date fin", width="medium"),
                DUREE_LABEL: st.column_config.TextColumn(DUREE_LABEL, width="medium"),
                "Statut": st.column_config.TextColumn("Statut", width="small"),
                "Commentaire": st.column_config.TextColumn(
                    "Commentaire", width="large"
                ),
            },
        )

        # Statistiques de l'historique
        actives = len([a for a, c in all_assignments if a.date_fin is None])
        terminees = len(all_assignments) - actives

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📊 Total assignations", len(all_assignments))

        with col2:
            st.metric("🟢 Assignations actives", actives)

        with col3:
            st.metric("🔴 Assignations terminées", terminees)

    except Exception as e:
        st.error(f"❌ Erreur : {e}")


def show_business_managers_list():
    """
    Affiche la liste complète des Business Managers avec fonctionnalités de recherche et filtrage.

    Fonctionnalités incluses :
    - Affichage en tableau avec colonnes configurables
    - Recherche par nom, email ou statut
    - Filtrage par statut d'activité
    - Tri par colonnes
    - Pagination pour la performance
    - Actions rapides (voir, modifier, supprimer)
    - Métriques globales (nombre total, actifs, inactifs)

    La fonction utilise st.dataframe pour un affichage interactif
    et gère les états de chargement avec st.spinner.

    Returns:
        None: Affiche directement dans l'interface Streamlit

    Note:
        La fonction est optimisée pour les grandes listes avec pagination
        et utilise le cache Streamlit pour les données fréquemment consultées.
    """

    # Champ de recherche en temps réel
    search_term = st.text_input(
        "🔍 Rechercher un Business Manager",
        placeholder="Tapez un prénom, nom ou email pour filtrer...",
        help="La liste se filtre automatiquement pendant que vous tapez",
        key="bm_search",
    )

    try:
        # Utiliser la recherche si un terme est saisi, sinon afficher tous les BMs
        if search_term and search_term.strip():
            bms_data_from_service = BusinessManagerService.search_business_managers(
                search_term.strip()
            )
            if bms_data_from_service:
                st.info(
                    f"🔍 {len(bms_data_from_service)} Business Manager(s) trouvé(s) pour '{search_term}'"
                )
            else:
                st.warning(f"❌ Aucun Business Manager trouvé pour '{search_term}'")
                return
        else:
            bms_data_from_service = BusinessManagerService.get_all_business_managers()

        if not bms_data_from_service:
            st.info("📝 Aucun Business Manager enregistré")
            st.markdown(
                "💡 Utilisez l'onglet **Nouveau BM** pour créer votre premier Business Manager"
            )
            return

        # Préparer les données pour le tableau à partir du service
        bms_data = _build_bm_data_table(bms_data_from_service)

        # Afficher le tableau avec noms cliquables
        df = pd.DataFrame(bms_data)

        # Forcer le type de la colonne ID en entier
        if not df.empty:
            df["ID"] = df["ID"].astype(int)

        # En-tête du tableau
        st.markdown("### 📋 Liste des Business Managers")

        # CSS pour styliser les boutons comme des liens hypertextes
        _apply_bm_list_css()

        # En-tête du tableau
        _display_bm_table_header()

        # Lignes de données
        for i, row in enumerate(bms_data):
            _display_bm_table_row(row, i, len(bms_data))

        # Métriques générales
        _display_bm_metrics(bms_data_from_service, bms_data)

    except Exception as e:
        st.error(ERROR_LIST_LOADING.format(e))


def show_add_business_manager():
    """
    Formulaire d'ajout d'un nouveau Business Manager avec validation complète.

    Interface de création incluant :
    - Champs obligatoires : nom, prénom, email
    - Champs optionnels : téléphone, notes
    - Validation en temps réel des données saisies
    - Vérification d'unicité de l'email
    - Gestion des erreurs et messages utilisateur
    - Confirmation visuelle de succès

    Le formulaire utilise st.form pour une soumission atomique
    et gère les erreurs de validation côté client et serveur.

    Args:
        None

    Returns:
        None: Affiche directement le formulaire dans l'interface Streamlit

    Raises:
        Exception: En cas d'erreur lors de la création en base de données

    Note:
        La fonction valide l'unicité de l'email avant création
        et rafraîchit automatiquement la page après succès.
    """
    st.subheader("➕ Nouveau Business Manager")

    with st.form("add_bm_form"):
        col1, col2 = st.columns(2)

        with col1:
            nom = st.text_input("Nom *", placeholder="Dupont")
            email = st.text_input("Email *", placeholder="john.dupont@company.com")
            actif = st.checkbox("✅ Actif", value=True)

        with col2:
            prenom = st.text_input("Prénom *", placeholder="Jean")
            telephone = st.text_input(TELEPHONE_LABEL, placeholder="01 23 45 67 89")

        notes = st.text_area(
            "Notes (optionnel)",
            height=100,
            placeholder="Notes sur le Business Manager...",
        )

        submitted = st.form_submit_button("💾 Créer le Business Manager")

        if submitted:
            # Validation
            if not nom or not prenom or not email:
                st.error("❌ Les champs Nom, Prénom et Email sont obligatoires")
                return

            if "@" not in email:
                st.error("❌ Format d'email invalide")
                return

            try:
                with get_database_session() as session:
                    # Vérifier si l'email existe déjà
                    existing = (
                        session.query(BusinessManager)
                        .filter(BusinessManager.email == email.strip().lower())
                        .first()
                    )

                    if existing:
                        st.error(
                            f"❌ Un Business Manager avec l'email {email} existe déjà"
                        )
                        return

                    # Créer le nouveau BM
                    new_bm = BusinessManager(
                        nom=nom.strip(),
                        prenom=prenom.strip(),
                        email=email.strip().lower(),
                        telephone=telephone.strip() if telephone else None,
                        actif=actif,
                        notes=notes.strip() if notes else None,
                        date_creation=datetime.now(),
                    )

                    session.add(new_bm)
                    session.commit()

                    st.success(SUCCESS_BM_CREATED.format(prenom, nom))
                    st.balloons()

                    # Rafraîchir la page pour mettre à jour la liste
                    st.rerun()

            except Exception as e:
                st.error(ERROR_CREATION.format(e))


def show_statistics():
    """
    Affiche les statistiques globales et détaillées des Business Managers.

    Métriques calculées :
    - Nombre total de Business Managers
    - Nombre de BMs actifs/inactifs
    - Nombre d'assignations actives/totales
    - Moyenne de consultants par BM actif
    - Répartition des consultants par BM (graphique en barres)
    - Évolution mensuelle des assignations (graphique linéaire)

    La fonction utilise des requêtes SQL optimisées avec SQLAlchemy
    et affiche les résultats avec les composants Streamlit appropriés.

    Args:
        None

    Returns:
        None: Affiche directement les statistiques dans l'interface Streamlit

    Raises:
        Exception: En cas d'erreur lors des requêtes de base de données

    Note:
        Les statistiques sont calculées en temps réel à partir de la base de données.
        Les graphiques utilisent les composants natifs de Streamlit pour la visualisation.
    """
    st.subheader("📊 Statistiques des Business Managers")

    try:
        from sqlalchemy import func
        
        with get_database_session() as session:
            # Statistiques générales
            total_bms = session.query(BusinessManager).count()
            total_active_bms = (
                session.query(BusinessManager).filter(BusinessManager.actif).count()
            )
            active_assignments = (
                session.query(ConsultantBusinessManager)
                .filter(ConsultantBusinessManager.date_fin.is_(None))
                .count()
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.write(f"**👔 Total BMs:** {total_bms}")

            with col2:
                st.write(f"**🟢 BMs Actifs:** {total_active_bms}")

            with col3:
                st.write(f"**🔗 Assignations actives:** {active_assignments}")

            with col4:
                avg_consultants = (
                    active_assignments / total_active_bms if total_active_bms > 0 else 0
                )
                st.write(f"**📊 Moyenne consultants/BM:** {avg_consultants:.1f}")

            # Répartition par BM
            st.subheader("� Répartition des consultants par BM")

            bm_stats_query = session.query(
                BusinessManager.prenom,
                BusinessManager.nom,
                func.count(ConsultantBusinessManager.id).label("consultants_count")
            ).outerjoin(
                ConsultantBusinessManager,
                and_(
                    BusinessManager.id == ConsultantBusinessManager.business_manager_id,
                    ConsultantBusinessManager.date_fin.is_(None)
                )
            ).filter(BusinessManager.actif).group_by(
                BusinessManager.id, BusinessManager.prenom, BusinessManager.nom
            )

            bm_stats = bm_stats_query.all()

            if bm_stats:
                data = []
                for bm_prenom, bm_nom, count in bm_stats:
                    data.append(
                        {
                            "Business Manager": f"{bm_prenom} {bm_nom}",
                            "Consultants actifs": count,
                        }
                    )

                df = pd.DataFrame(data)

                if not df.empty:
                    st.bar_chart(df.set_index("Business Manager"))
                else:
                    st.info("📊 Aucune donnée à afficher")

            # Évolution des assignations
            st.subheader("📅 Évolution des assignations")

            # Assignations par mois (derniers 12 mois)
            import calendar
            from sqlalchemy import extract

            monthly_stats = (
                session.query(
                    extract("year", ConsultantBusinessManager.date_creation).label(
                        "year"
                    ),
                    extract("month", ConsultantBusinessManager.date_creation).label(
                        "month"
                    ),
                    func.count(ConsultantBusinessManager.id).label("count"),
                )
                .group_by("year", "month")
                .order_by("year", "month")
                .limit(12)
                .all()
            )

            if monthly_stats:
                monthly_data = []
                for year, month, count in monthly_stats:
                    month_name = calendar.month_name[int(month)]
                    monthly_data.append(
                        {
                            "Mois": f"{month_name} {int(year)}",
                            "Nouvelles assignations": count,
                        }
                    )

                df_monthly = pd.DataFrame(monthly_data)
                st.line_chart(df_monthly.set_index("Mois"))

    except Exception as e:
        st.error(ERROR_STATISTICS.format(e))


# Helper methods pour show_add_bm_assignment()


def _separate_consultants_by_status(all_consultants, assigned_consultant_ids, session):
    """Sépare les consultants entre disponibles et assignés à d'autres BMs."""
    available_consultants = []
    assigned_to_other_bm = []

    for consultant in all_consultants:
        if consultant.id in assigned_consultant_ids:
            continue  # Déjà assigné à ce BM

        # Vérifier s'il a une assignation active avec un autre BM
        existing_assignment = (
            session.query(ConsultantBusinessManager)
            .filter(
                and_(
                    ConsultantBusinessManager.consultant_id == consultant.id,
                    ConsultantBusinessManager.date_fin.is_(None),
                )
            )
            .first()
        )

        if existing_assignment:
            # Récupérer le BM actuel
            current_bm = (
                session.query(BusinessManager)
                .filter(BusinessManager.id == existing_assignment.business_manager_id)
                .first()
            )
            assigned_to_other_bm.append((consultant, current_bm, existing_assignment))
        else:
            available_consultants.append(consultant)

    return available_consultants, assigned_to_other_bm


def _build_consultant_options_for_assignment(
    available_consultants, assigned_to_other_bm
):
    """Construit les options de consultants pour le selectbox d'assignation."""
    consultant_options = {}

    # Consultants disponibles (aucune assignation active)
    if available_consultants:
        st.write("**🟢 Consultants disponibles :**")
        for consultant in available_consultants:
            key = f"🟢 {consultant.prenom} {consultant.nom} ({consultant.email}) - DISPONIBLE"
            consultant_options[key] = {
                "consultant": consultant,
                "status": "available",
                "existing_assignment": None,
                "current_bm": None,
            }

    # Consultants assignés à d'autres BMs
    if assigned_to_other_bm:
        st.write("**🔄 Consultants assignés à d'autres BMs (nécessite transfert) :**")
        for consultant, current_bm, existing_assignment in assigned_to_other_bm:
            since_date = existing_assignment.date_debut.strftime(DATE_FORMAT)
            key = f"🔄 {consultant.prenom} {consultant.nom} ({consultant.email}) - Actuellement avec {current_bm.prenom} {current_bm.nom} depuis le {since_date}"
            consultant_options[key] = {
                "consultant": consultant,
                "status": "assigned",
                "existing_assignment": existing_assignment,
                "current_bm": current_bm,
            }

    return consultant_options


def _handle_assignment_transfer(selected_data, date_debut, bm, cloture_comment):
    """Gère le transfert d'un consultant d'un BM à un autre."""
    existing_assignment = selected_data["existing_assignment"]
    existing_assignment.date_fin = date_debut  # Fin = début de la nouvelle assignation

    # Ajouter le commentaire de clôture
    existing_comment = existing_assignment.commentaire or ""
    new_comment = (
        f"Transfert vers {bm.prenom} {bm.nom} le {date_debut.strftime(DATE_FORMAT)}"
    )
    if cloture_comment:
        new_comment += f" - Raison: {cloture_comment}"

    if existing_comment:
        existing_assignment.commentaire = f"{existing_comment}\n{new_comment}"
    else:
        existing_assignment.commentaire = new_comment

    # Message de confirmation du transfert
    old_bm_name = (
        selected_data["current_bm"].prenom + " " + selected_data["current_bm"].nom
    )
    st.info(f"🔄 Assignation avec {old_bm_name} clôturée automatiquement")


def _create_new_assignment(consultant, bm, date_debut, commentaire, session):
    """Crée une nouvelle assignation consultant-BM."""
    assignment = ConsultantBusinessManager(
        consultant_id=consultant.id,
        business_manager_id=bm.id,
        date_debut=date_debut,
        date_creation=datetime.now(),
        commentaire=commentaire.strip() if commentaire else None,
    )
    session.add(assignment)
    return assignment


def _display_assignment_success_message(selected_data, consultant, bm):
    """Affiche le message de succès approprié après création d'assignation."""
    if selected_data["status"] == "assigned":
        st.success(
            SUCCESS_TRANSFER.format(
                consultant.prenom, consultant.nom, bm.prenom, bm.nom
            )
        )
    else:
        st.success(
            SUCCESS_ASSIGNMENT.format(
                consultant.prenom, consultant.nom, bm.prenom, bm.nom
            )
        )
    st.balloons()
    st.rerun()


# Helper methods pour show_business_managers_list()


def _apply_bm_list_css():
    """Applique le CSS pour styliser les boutons comme des liens hypertextes."""
    st.markdown(
        """
    <style>
    /* Style pour transformer les boutons en liens hypertextes - sélecteurs très spécifiques */
    .stButton button,
    .stButton > div > button,
    div[data-testid="column"] button,
    div[data-testid="column"] > div button,
    div[data-testid="column"] > div > div button,
    div[data-testid="column"] > div > div > div button,
    div[data-testid="column"] > div > div > div > div button {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #1f77b4 !important;
        text-decoration: underline !important;
        cursor: pointer !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        text-align: left !important;
        box-shadow: none !important;
        min-height: auto !important;
        height: auto !important;
        width: auto !important;
        border-width: 0 !important;
        outline: none !important;
    }

    .stButton button:hover,
    .stButton > div > button:hover,
    div[data-testid="column"] button:hover,
    div[data-testid="column"] > div button:hover,
    div[data-testid="column"] > div > div button:hover,
    div[data-testid="column"] > div > div > div button:hover,
    div[data-testid="column"] > div > div > div > div button:hover {
        color: #0d47a1 !important;
        text-decoration: underline !important;
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    .stButton button:focus,
    .stButton > div > button:focus,
    div[data-testid="column"] button:focus,
    div[data-testid="column"] > div button:focus,
    div[data-testid="column"] > div > div button:focus,
    div[data-testid="column"] > div > div > div button:focus,
    div[data-testid="column"] > div > div > div > div button:focus {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: 1px dotted #1f77b4 !important;
    }

    .stButton button:active,
    .stButton > div > button:active,
    div[data-testid="column"] button:active,
    div[data-testid="column"] > div button:active,
    div[data-testid="column"] > div > div button:active,
    div[data-testid="column"] > div > div > div button:active,
    div[data-testid="column"] > div > div > div > div button:active {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #0d47a1 !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def _build_bm_data_table(bms_data_from_service):
    """Construit les données du tableau à partir du service BM."""
    bms_data = []
    for bm_dict in bms_data_from_service:
        # Calculer le total des assignations avec une nouvelle session
        with get_database_session() as session:
            total_assignments = (
                session.query(ConsultantBusinessManager)
                .filter(ConsultantBusinessManager.business_manager_id == bm_dict["id"])
                .count()
            )

        bms_data.append(
            {
                "ID": int(bm_dict["id"]),  # Force la conversion en entier
                "Prénom": bm_dict["prenom"],
                "Nom": bm_dict["nom"],
                "Email": bm_dict["email"],
                TELEPHONE_LABEL: bm_dict["telephone"] or "N/A",
                "Consultants actuels": bm_dict["consultants_count"],
                "Total assignations": total_assignments,
                "Statut": "🟢 Actif" if bm_dict["actif"] else "🔴 Inactif",
                "Créé le": (
                    bm_dict["date_creation"].strftime(DATE_FORMAT)
                    if bm_dict["date_creation"]
                    else "N/A"
                ),
            }
        )
    return bms_data


def _display_bm_table_header():
    """Affiche l'en-tête du tableau des Business Managers."""
    # En-tête avec colonnes
    header_cols = st.columns([1, 3, 3, 2, 2, 2, 2])
    with header_cols[0]:
        st.markdown("**ID**")
    with header_cols[1]:
        st.markdown("**👤 Nom complet**")
    with header_cols[2]:
        st.markdown("**Email**")
    with header_cols[3]:
        st.markdown(f"**📱 {TELEPHONE_LABEL}**")
    with header_cols[4]:
        st.markdown("**👥 Consultants**")
    with header_cols[5]:
        st.markdown("**📊 Total**")
    with header_cols[6]:
        st.markdown("**🔄 Statut**")

    st.markdown("---")


def _display_bm_table_row(row, i, total_rows):
    """Affiche une ligne du tableau des Business Managers."""
    cols = st.columns([1, 3, 3, 2, 2, 2, 2])

    with cols[0]:
        st.write(f"`{row['ID']}`")

    with cols[1]:
        # Nom comme vrai lien hypertexte HTML + bouton invisible pour la navigation
        nom_complet = f"{row['Prénom']} {row['Nom']}"

        # Nom comme lien hypertexte cliquable
        if st.button(
            f"👤 {nom_complet}",
            key=f"btn_bm_{row['ID']}",
            help=f"Voir le profil de {nom_complet}",
        ):
            try:
                # S'assurer que l'ID est un entier valide
                bm_id = row["ID"]
                if isinstance(bm_id, str):
                    bm_id = int(bm_id)
                elif not isinstance(bm_id, int):
                    bm_id = int(str(bm_id))

                st.session_state.view_bm_profile = bm_id
                st.rerun()
            except (ValueError, TypeError) as e:
                st.error(f"❌ Erreur : ID du Business Manager invalide ({row['ID']})")
                print(
                    f"Erreur de conversion d'ID: {e}, valeur: {row['ID']}, type: {type(row['ID'])}"
                )

    with cols[2]:
        # Email simple non cliquable (utilisation du HTML pour éviter la détection automatique)
        st.markdown(
            f"""
        <div style="color: #262730; font-size: 14px;">
            {row['Email']}
        </div>
        """,
            unsafe_allow_html=True,
        )

    with cols[3]:
        st.write(row[TELEPHONE_LABEL])

    with cols[4]:
        st.write(f"**{row['Consultants actuels']}**")

    with cols[5]:
        st.write(f"{row['Total assignations']}")

    with cols[6]:
        st.write(row["Statut"])

    # Ligne de séparation subtile
    if i < total_rows - 1:
        st.markdown(
            "<hr style='margin: 0.5rem 0; border: 0; border-top: 1px solid #eee;'>",
            unsafe_allow_html=True,
        )


def _display_bm_metrics(bms_data_from_service, bms_data):
    """Affiche les métriques générales des Business Managers."""
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write(f"**👔 Total BMs:** {len(bms_data_from_service)}")

    with col2:
        actifs = len([bm for bm in bms_data_from_service if bm["actif"]])
        st.write(f"**🟢 Actifs:** {actifs}")

    with col3:
        total_consultants = sum(bm_data["Consultants actuels"] for bm_data in bms_data)
        st.write(f"**👥 Total consultants gérés:** {total_consultants}")

    with col4:
        avg_consultants = (
            total_consultants / len(bms_data_from_service)
            if len(bms_data_from_service) > 0
            else 0
        )
        st.write(f"**📊 Moyenne consultants/BM:** {avg_consultants:.1f}")
