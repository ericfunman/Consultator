"""
Page de gestion des practices - VERSION FONCTIONNELLE
"""

import streamlit as st

try:
    import pandas as pd
except ImportError:
    pd = None

from services.practice_service import PracticeService

# Constantes
PRENOM_COLUMN = "Prénom"


def show():
    """Affiche la page de gestion des practices"""
    st.title("🏢 Gestion des Practices")

    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3 = st.tabs(
        ["📊 Vue d'ensemble", "👥 Consultants par Practice", "⚙️ Gestion des Practices"]
    )

    with tab1:
        show_practice_overview()

    with tab2:
        show_consultants_by_practice()

    with tab3:
        show_practice_management()


def show_practice_overview():
    """Affiche une vue d'ensemble des practices"""
    st.subheader("📊 Vue d'ensemble des Practices")

    try:
        # Récupérer les statistiques
        stats = PracticeService.get_practice_statistics()

        if stats:
            # Afficher les métriques principales
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Practices", stats.get("total_practices", 0))

            with col2:
                st.metric("Consultants assignés", stats.get("total_consultants", 0))

            with col3:
                st.metric("Practices actives", stats.get("active_practices", 0))

        # Afficher la liste des practices
        practices = PracticeService.get_all_practices()
        if practices:
            st.subheader("Liste des Practices")
            for practice in practices:
                with st.expander(f"🏢 {practice.nom}"):
                    st.write(
                        f"**Description:** {practice.description or 'Aucune description'}"
                    )
                    st.write(f"**Responsable:** {practice.responsable or 'Non défini'}")
                    st.write(
                        f"**Statut:** {'✅ Actif' if practice.actif else '❌ Inactif'}"
                    )

    except Exception as e:
        st.error(f"Erreur lors du chargement de la vue d'ensemble: {e}")


def show_consultants_by_practice():
    """Affiche les consultants par practice avec gestion avancée"""
    st.subheader("👥 Consultants par Practice")

    try:
        practices = PracticeService.get_all_practices()

        if practices:
            _display_practice_interface(practices)
        else:
            st.warning("Aucune practice trouvée.")

    except Exception as e:
        st.error(f"Erreur lors du chargement des consultants: {e}")
        st.exception(e)


def _display_practice_interface(practices):
    """Affiche l'interface de sélection et gestion des practices"""
    selected_practice = _render_practice_selector(practices)

    if selected_practice:
        _display_practice_tabs(selected_practice)


def _render_practice_selector(practices):
    """Affiche le sélecteur de practice"""
    col1, _ = st.columns([2, 1])

    with col1:
        return st.selectbox(
            "Sélectionner une practice:",
            options=practices,
            format_func=lambda x: x.nom,
            key="practice_selector",
        )

    return None


def _display_practice_tabs(selected_practice):
    """Affiche les onglets de gestion de la practice"""
    tab1, tab2, tab3 = st.tabs(
        ["📋 Liste des consultants", "➕ Affecter consultant", "⚙️ Actions"]
    )

    with tab1:
        _display_consultants_list_tab(selected_practice)

    with tab2:
        _display_assign_consultant_tab(selected_practice)

    with tab3:
        _display_practice_actions_tab(selected_practice)


def _display_consultants_list_tab(selected_practice):
    """Affiche l'onglet de la liste des consultants"""
    consultants_dict = PracticeService.get_consultants_by_practice(selected_practice.id)

    if consultants_dict:
        _render_consultants_table(consultants_dict, selected_practice)
    else:
        st.info("Aucun consultant assigné à cette practice.")


def _render_consultants_table(consultants_dict, selected_practice):
    """Affiche le tableau des consultants avec actions"""
    practice_name = list(consultants_dict.keys())[0]
    consultants = consultants_dict[practice_name]

    if consultants:
        st.write(
            f"**{len(consultants)} consultant(s) dans la practice {selected_practice.nom}**"
        )

        consultant_data = _prepare_consultants_table_data(consultants)
        _display_consultants_dataframe(consultant_data)
        _display_remove_consultant_section(consultants, selected_practice)
    else:
        st.info("Aucun consultant assigné à cette practice.")


def _prepare_consultants_table_data(consultants):
    """Prépare les données pour le tableau des consultants"""
    consultant_data = []
    for consultant in consultants:
        consultant_data.append(
            {
                "ID": consultant.id,
                "Nom": consultant.nom,
                PRENOM_COLUMN: consultant.prenom,
                "Email": consultant.email,
                "Grade": getattr(consultant, "grade", "Non défini"),
                "Disponible": (
                    "✅" if getattr(consultant, "disponibilite", False) else "❌"
                ),
                "Salaire": _format_consultant_salary(consultant),
            }
        )
    return consultant_data


def _format_consultant_salary(consultant):
    """Formate le salaire d'un consultant"""
    salaire = getattr(consultant, "salaire_actuel", None)
    if salaire:
        return f"{salaire:,.0f}€"
    return "Non défini"


def _display_consultants_dataframe(consultant_data):
    """Affiche le dataframe des consultants"""
    if not consultant_data:
        return

    if pd is not None:
        df = pd.DataFrame(consultant_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config=_get_column_config(),
        )
    else:
        _display_consultants_simple_list(consultant_data)


def _get_column_config():
    """Retourne la configuration des colonnes pour le dataframe"""
    return {
        "ID": st.column_config.NumberColumn("ID", width="small"),
        "Nom": st.column_config.TextColumn("Nom", width="medium"),
        PRENOM_COLUMN: st.column_config.TextColumn(PRENOM_COLUMN, width="medium"),
        "Email": st.column_config.TextColumn("Email", width="large"),
        "Grade": st.column_config.TextColumn("Grade", width="medium"),
        "Disponible": st.column_config.TextColumn("Disponible", width="small"),
        "Salaire": st.column_config.TextColumn("Salaire", width="medium"),
    }


def _display_consultants_simple_list(consultant_data):
    """Affiche la liste simple des consultants sans pandas"""
    for data in consultant_data:
        st.write(
            f"**{data[PRENOM_COLUMN]} {data['Nom']}** - {data['Grade']} - {data['Email']} - {data['Salaire']}"
        )


def _display_remove_consultant_section(consultants, selected_practice):
    """Affiche la section pour retirer un consultant"""
    st.write("**Retirer un consultant de la practice:**")
    consultant_to_remove = st.selectbox(
        "Choisir un consultant à retirer:",
        options=consultants,
        format_func=lambda x: f"{x.prenom} {x.nom}",
        key="consultant_to_remove",
    )

    if st.button("🗑️ Retirer de la practice", key="remove_consultant"):
        _handle_remove_consultant(consultant_to_remove, selected_practice)


def _handle_remove_consultant(consultant_to_remove, selected_practice):
    """Gère la suppression d'un consultant de la practice"""
    try:
        success = PracticeService.assign_consultant_to_practice(
            consultant_to_remove.id, None
        )
        if success:
            st.success(
                f"✅ {consultant_to_remove.prenom} {consultant_to_remove.nom} a été retiré de la practice {selected_practice.nom}"
            )
            st.rerun()
        else:
            st.error("❌ Erreur lors du retrait du consultant")
    except Exception as e:
        st.error(f"❌ Erreur: {e}")


def _display_assign_consultant_tab(selected_practice):
    """Affiche l'onglet d'affectation de consultant"""
    st.write("**Affecter un consultant à la practice:**")

    available_consultants = _get_available_consultants(selected_practice)

    if available_consultants:
        _display_consultant_assignment_interface(
            available_consultants, selected_practice
        )
    else:
        st.info("Tous les consultants sont déjà affectés à cette practice.")


def _get_available_consultants(selected_practice):
    """Récupère les consultants disponibles pour affectation"""
    from app.services.consultant_service import ConsultantService

    all_consultants = ConsultantService.get_all_consultants_objects(
        page=1, per_page=10000
    )

    return [
        c
        for c in all_consultants
        if not c.practice_id or c.practice_id != selected_practice.id
    ]


def _display_consultant_assignment_interface(available_consultants, selected_practice):
    """Affiche l'interface d'affectation de consultant"""
    consultant_to_add = st.selectbox(
        "Choisir un consultant à affecter:",
        options=available_consultants,
        format_func=lambda x: f"{x.prenom} {x.nom} - {getattr(x, 'grade', 'Grade non défini')}",
        key="consultant_to_add",
    )

    if consultant_to_add:
        _display_consultant_details(consultant_to_add)

    if st.button("➕ Affecter à la practice", key="add_consultant"):
        _handle_assign_consultant(consultant_to_add, selected_practice)


def _display_consultant_details(consultant):
    """Affiche les détails du consultant sélectionné"""
    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.write(f"**Email:** {consultant.email}")
        st.write(f"**Grade:** {getattr(consultant, 'grade', 'Non défini')}")

    with col_info2:
        current_practice = _get_consultant_current_practice(consultant)
        st.write(f"**Practice actuelle:** {current_practice}")
        st.write(f"**Salaire:** {getattr(consultant, 'salaire_actuel', 0):,.0f}€")


def _get_consultant_current_practice(consultant):
    """Récupère la practice actuelle du consultant"""
    if not consultant.practice_id:
        return "Aucune"

    current_practice_obj = PracticeService.get_practice_by_id(consultant.practice_id)
    return current_practice_obj.nom if current_practice_obj else "Aucune"


def _handle_assign_consultant(consultant_to_add, selected_practice):
    """Gère l'affectation d'un consultant à la practice"""
    try:
        success = PracticeService.assign_consultant_to_practice(
            consultant_to_add.id, selected_practice.id
        )
        if success:
            st.success(
                f"✅ {consultant_to_add.prenom} {consultant_to_add.nom} a été affecté à la practice {selected_practice.nom}"
            )
            st.rerun()
        else:
            st.error("❌ Erreur lors de l'affectation du consultant")
    except Exception as e:
        st.error(f"❌ Erreur: {e}")


def _display_practice_actions_tab(selected_practice):
    """Affiche l'onglet des actions sur la practice"""
    st.write("**Actions sur la practice:**")

    col_action1, col_action2 = st.columns(2)

    with col_action1:
        _display_practice_statistics(selected_practice)

    with col_action2:
        _display_practice_export_options(selected_practice)


def _display_practice_statistics(selected_practice):
    """Affiche les statistiques de la practice"""
    st.write("**Statistiques de la practice:**")
    try:
        stats = PracticeService.get_practice_statistics()
        practice_stats = next(
            (
                p
                for p in stats.get("practices_detail", [])
                if p["nom"] == selected_practice.nom
            ),
            None,
        )
        if practice_stats:
            st.metric("Total consultants", practice_stats["total_consultants"])
            st.metric("Consultants actifs", practice_stats["consultants_actifs"])
            st.write(f"**Responsable:** {practice_stats['responsable']}")
    except Exception as e:
        st.error(f"Erreur lors du chargement des statistiques: {e}")


def _display_practice_export_options(selected_practice):
    """Affiche les options d'export de la practice"""
    st.write("**Export des données:**")
    if st.button("📊 Exporter la liste (CSV)", key="export_csv"):
        _handle_csv_export(selected_practice)


def _handle_csv_export(selected_practice):
    """Gère l'export CSV de la practice"""
    try:
        consultants_dict = PracticeService.get_consultants_by_practice(
            selected_practice.id
        )
        if consultants_dict and pd is not None:
            _process_csv_export(consultants_dict, selected_practice)
    except Exception as e:
        st.error(f"❌ Erreur lors de l'export: {e}")


def _process_csv_export(consultants_dict, selected_practice):
    """Traite l'export CSV des consultants"""
    practice_name = list(consultants_dict.keys())[0]
    consultants = consultants_dict[practice_name]

    if consultants:
        export_data = _prepare_csv_export_data(consultants, selected_practice)
        _generate_csv_download(export_data, selected_practice)


def _prepare_csv_export_data(consultants, selected_practice):
    """Prépare les données pour l'export CSV"""
    export_data = []
    for consultant in consultants:
        export_data.append(
            {
                "ID": consultant.id,
                "Nom": consultant.nom,
                PRENOM_COLUMN: consultant.prenom,
                "Email": consultant.email,
                "Grade": getattr(consultant, "grade", ""),
                "Disponible": getattr(consultant, "disponibilite", False),
                "Salaire": getattr(consultant, "salaire_actuel", 0),
                "Practice": selected_practice.nom,
            }
        )
    return export_data


def _generate_csv_download(export_data, selected_practice):
    """Génère le téléchargement CSV"""
    df_export = pd.DataFrame(export_data)
    csv = df_export.to_csv(index=False)

    st.download_button(
        label="💾 Télécharger CSV",
        data=csv,
        file_name=f"consultants_{selected_practice.nom.replace(' ', '_')}.csv",
        mime="text/csv",
    )
    st.success("✅ Export prêt au téléchargement!")


def show_practice_management():
    """Interface de gestion des practices"""
    st.subheader("⚙️ Gestion des Practices")

    _display_practice_creation_form()
    _display_existing_practices_list()


def _display_practice_creation_form():
    """Affiche le formulaire de création de practice"""
    with st.expander("➕ Créer une nouvelle practice"):
        _render_practice_creation_form()


def _render_practice_creation_form():
    """Affiche le formulaire de création avec validation"""
    with st.form("create_practice_form"):
        nom = st.text_input("Nom de la practice*")
        description = st.text_area("Description")
        responsable = st.text_input("Responsable")

        if st.form_submit_button("Créer la practice"):
            _handle_practice_creation(nom, description, responsable)


def _handle_practice_creation(nom, description, responsable):
    """Gère la création d'une nouvelle practice"""
    if nom:
        _create_new_practice(nom, description, responsable)
    else:
        st.error("❌ Le nom de la practice est obligatoire.")


def _create_new_practice(nom, description, responsable):
    """Crée une nouvelle practice avec gestion d'erreur"""
    try:
        success = PracticeService.create_practice(
            nom=nom, description=description, responsable=responsable
        )
        if success:
            st.success(f"✅ Practice '{nom}' créée avec succès !")
            st.rerun()
        else:
            st.error("❌ Erreur lors de la création de la practice.")
    except Exception as e:
        st.error(f"❌ Erreur: {e}")


def _display_existing_practices_list():
    """Affiche la liste des practices existantes"""
    practices = PracticeService.get_all_practices()
    if practices:
        st.write("**Practices existantes:**")
        _render_practices_table(practices)


def _render_practices_table(practices):
    """Affiche le tableau des practices existantes"""
    for practice in practices:
        _render_single_practice_row(practice)


def _render_single_practice_row(practice):
    """Affiche une ligne pour une practice"""
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.write(f"🏢 {practice.nom}")

    with col2:
        if st.button("Modifier", key=f"edit_{practice.id}"):
            st.info("Fonction de modification en cours de développement")

    with col3:
        status = "✅ Actif" if practice.actif else "❌ Inactif"
        st.write(status)
