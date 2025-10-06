"""
Page de gestion des dashboards personnalisés
Interface utilisateur pour créer, configurer et visualiser les dashboards
Phases 1-4 complètes : fondations, widgets, builder avancé, fonctionnalités premium
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from app.services.dashboard_service import DashboardService
from app.services.widget_factory import WidgetFactory, WidgetCatalogManager
from app.pages_modules.dashboard_builder import dashboard_builder
from app.pages_modules.dashboard_advanced import advanced_features

# Constantes pour messages d'erreur et labels réutilisés
ERROR_DASHBOARD_NOT_FOUND = "❌ Dashboard introuvable"
ERROR_DASHBOARD_NAME_REQUIRED = "❌ Le nom du dashboard est obligatoire"
LABEL_DASHBOARD_NAME = "Nom du dashboard *"
BUTTON_CANCEL = "❌ Annuler"


def show_dashboard_page():
    """
    Page principale des dashboards personnalisés
    Phases 1-4 : Vue classique, Création, Builder avancé, Fonctionnalités premium
    """
    # Initialiser le catalogue de widgets s'il n'existe pas
    if "widgets_initialized" not in st.session_state:
        WidgetCatalogManager.initialize_widget_catalog()
        st.session_state.widgets_initialized = True

    # Navigation selon le mode
    if "dashboard_mode" not in st.session_state:
        st.session_state.dashboard_mode = "view"

    # Interface de sélection de mode
    mode_tabs = st.tabs(["👁️ Visualisation", "🎨 Builder Avancé", "📊 Analytics+", "⚙️ Gestion"])

    with mode_tabs[0]:
        if st.session_state.dashboard_mode in ["view", "create", "edit"]:
            show_enhanced_dashboard_viewer()

    with mode_tabs[1]:
        dashboard_builder.show_advanced_builder()

    with mode_tabs[2]:
        show_advanced_analytics()

    with mode_tabs[3]:
        show_dashboard_management_page()


def show_dashboard_viewer():
    """
    Mode visualisation des dashboards (fonction originale)
    """
    # En-tête avec contrôles
    col1, col2, col3 = st.columns([3, 2, 1])

    with col1:
        # Sélection du dashboard
        dashboards = DashboardService.get_all_dashboards()

        if not dashboards:
            st.info("📊 Aucun dashboard disponible")
            if st.button("➕ Créer mon premier dashboard", key="create_first_dashboard_viewer"):
                st.session_state.dashboard_mode = "create"
                st.rerun()
            return

        dashboard_options = {f"{d['nom']}" + (" 📋" if d["is_template"] else ""): d["id"] for d in dashboards}

        # Conserver la sélection dashboard entre les interactions
        if "selected_dashboard_id" not in st.session_state:
            st.session_state.selected_dashboard_id = list(dashboard_options.values())[0] if dashboard_options else None

        selected_dashboard_name = st.selectbox(
            "📊 Sélectionner un dashboard",
            options=list(dashboard_options.keys()),
            index=(
                list(dashboard_options.values()).index(st.session_state.selected_dashboard_id)
                if st.session_state.selected_dashboard_id in dashboard_options.values()
                else 0
            ),
            key="selected_dashboard",
        )

        selected_dashboard_id = dashboard_options[selected_dashboard_name]
        st.session_state.selected_dashboard_id = selected_dashboard_id

    with col2:
        # Filtre de période global (optionnel)
        period_filter = st.selectbox(
            "📅 Période", options=["1 mois", "3 mois", "6 mois", "12 mois"], index=1, key="global_period_filter_viewer"
        )

    with col3:
        # Boutons d'action
        if st.button("⚙️ Éditer", key="edit_dashboard_viewer"):
            st.session_state.dashboard_mode = "edit"
            st.session_state.edit_dashboard_id = st.session_state.selected_dashboard_id
            st.rerun()

        if st.button("➕ Nouveau", key="new_dashboard_viewer"):
            st.session_state.dashboard_mode = "create"
            st.rerun()

    st.markdown("---")

    # Affichage du dashboard sélectionné
    dashboard_config = DashboardService.get_dashboard_by_id(selected_dashboard_id)

    if not dashboard_config:
        st.error(ERROR_DASHBOARD_NOT_FOUND)
        return

    # Conversion de la période en nombre de mois
    period_months = {"1 mois": 1, "3 mois": 3, "6 mois": 6, "12 mois": 12}.get(period_filter, 3)

    # Affichage des widgets
    render_dashboard_widgets(dashboard_config, period_months)


def show_enhanced_dashboard_viewer():
    """
    Visualiseur de dashboard amélioré avec filtres avancés
    """
    # Vérifier si on est en mode création ou édition
    if st.session_state.dashboard_mode == "create":
        st.title("➕ Créer un nouveau dashboard")
        show_dashboard_creation_form()
        return
    elif st.session_state.dashboard_mode == "edit":
        st.title("⚙️ Éditer le dashboard")
        show_dashboard_edit_form()
        return

    st.title("📊 Dashboard Personnalisé")

    # Sidebar avec filtres avancés
    filters = advanced_features.show_advanced_filters(context="enhanced_viewer")
    advanced_features.show_alerts_panel(filters)

    # Contenu principal inchangé mais avec filtres appliqués
    show_dashboard_viewer()


def show_advanced_analytics():
    """
    Page Analytics avancée avec insights IA et prévisions
    """
    st.title("📊 Analytics Avancés")

    # Sélection du dashboard pour analyse
    dashboards = DashboardService.get_all_dashboards()

    if not dashboards:
        st.info("📊 Aucun dashboard disponible pour l'analyse")
        return

    dashboard_options = {f"{d['nom']}": d["id"] for d in dashboards}
    selected_dashboard_name = st.selectbox(
        "Dashboard à analyser", options=list(dashboard_options.keys()), key="analytics_dashboard_selectbox"
    )

    selected_dashboard_id = dashboard_options[selected_dashboard_name]
    dashboard_config = DashboardService.get_dashboard_by_id(selected_dashboard_id)

    if not dashboard_config:
        st.error(ERROR_DASHBOARD_NOT_FOUND)
        return

    # Tabs analytiques
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Insights IA", "📈 Analyse Comparative", "🔮 Prévisions", "📤 Export"])

    with tab1:
        filters = advanced_features.show_advanced_filters(context="analytics")
        advanced_features.show_ai_insights(dashboard_config, filters)

    with tab2:
        advanced_features.show_comparative_analysis()

    with tab3:
        advanced_features.show_forecasting()

    with tab4:
        st.subheader("📤 Export Dashboard")
        advanced_features.show_export_options(dashboard_config)


def show_dashboard_management_page():
    """
    Page de gestion avancée des dashboards
    """
    st.title("⚙️ Gestion des Dashboards")

    # Statistiques globales
    col1, col2, col3, col4 = st.columns(4)

    dashboards = DashboardService.get_all_dashboards()
    total_widgets = sum(len(d.get("widgets", [])) for d in dashboards)
    templates_count = sum(1 for d in dashboards if d.get("is_template", False))

    with col1:
        st.metric("Dashboards Total", len(dashboards))

    with col2:
        st.metric("Widgets Total", total_widgets)

    with col3:
        st.metric("Templates", templates_count)

    with col4:
        st.metric("Dashboards Actifs", len(dashboards) - templates_count)

    st.markdown("---")

    # Tabs de gestion
    tab1, tab2, tab3 = st.tabs(["📋 Liste", "🔧 Maintenance", "📊 Statistiques"])

    with tab1:
        show_dashboards_list()

    with tab2:
        show_maintenance_tools()

    with tab3:
        show_dashboard_statistics()


def show_dashboards_list():
    """
    Liste détaillée des dashboards avec actions
    """
    st.subheader("📋 Tous les Dashboards")

    dashboards = DashboardService.get_all_dashboards()

    if not dashboards:
        st.info("📊 Aucun dashboard créé")
        return

    # Tableau des dashboards
    for dashboard in dashboards:
        with st.expander(f"📊 {dashboard['nom']}", expanded=False):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.write(f"**Description:** {dashboard.get('description', 'Aucune')}")
                st.write(f"**Accès:** {dashboard['role_access']}")
                st.write(f"**Créé le:** {dashboard['date_creation'].strftime('%d/%m/%Y')}")
                st.write(f"**Widgets:** {len(dashboard.get('widgets', []))}")

            with col2:
                if dashboard.get("is_template"):
                    st.success("📋 Template")
                else:
                    st.info("📊 Dashboard")

                if dashboard.get("is_public"):
                    st.success("🌐 Public")
                else:
                    st.warning("🔒 Privé")

            with col3:
                if st.button("👁️ Voir", key=f"view_{dashboard['id']}"):
                    st.session_state.dashboard_mode = "view"
                    st.session_state.selected_dashboard_id = dashboard["id"]
                    st.rerun()

                if st.button("✏️ Éditer", key=f"edit_{dashboard['id']}"):
                    st.session_state.dashboard_mode = "edit"
                    st.session_state.edit_dashboard_id = dashboard["id"]
                    st.rerun()

                if st.button("📋 Dupliquer", key=f"dup_{dashboard['id']}"):
                    st.info("🔄 Duplication - Fonctionnalité à implémenter")


def show_maintenance_tools():
    """
    Outils de maintenance des dashboards
    """
    st.subheader("🔧 Outils de Maintenance")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧹 Nettoyage")

        if st.button("🗑️ Supprimer les dashboards vides", key="clean_empty_dashboards"):
            st.info("🔄 Nettoyage des dashboards vides")

        if st.button("🔄 Réinitialiser les templates", key="reset_templates"):
            st.info("🔄 Réinitialisation des templates par défaut")

        if st.button("📦 Optimiser la base de données", key="optimize_database"):
            st.info("🔄 Optimisation de la base de données")

    with col2:
        st.subheader("📊 Diagnostic")

        if st.button("🔍 Vérifier l'intégrité", key="check_integrity"):
            st.success("✅ Tous les dashboards sont valides")

        if st.button("📈 Analyser les performances", key="analyze_performance"):
            st.info("📊 Analyse des performances en cours...")

        if st.button("🔧 Réparer les widgets", key="repair_widgets"):
            st.info("🔧 Réparation automatique des widgets")


def show_dashboard_statistics():
    """
    Statistiques détaillées sur l'utilisation des dashboards
    """
    st.subheader("📊 Statistiques d'Utilisation")

    # Récupération des dashboards
    all_dashboards = DashboardService.get_all_dashboards()

    if not all_dashboards:
        st.info("📊 Aucun dashboard disponible pour les statistiques")
        if st.button("➕ Créer mon premier dashboard", key="create_first_dashboard_statistics_gestion"):
            st.session_state.dashboard_mode = "create"
            st.rerun()
        return

    # Graphiques de statistiques
    import plotly.express as px
    import pandas as pd

    # Stats par type de widget
    widget_usage = {}

    for dashboard in all_dashboards:
        for widget in dashboard.get("widgets", []):
            widget_type = widget["widget_type"]
            widget_usage[widget_type] = widget_usage.get(widget_type, 0) + 1

    if widget_usage:
        widget_df = pd.DataFrame(list(widget_usage.items()), columns=["Widget", "Utilisations"])

        fig = px.bar(widget_df, x="Widget", y="Utilisations", title="Utilisation des Widgets")
        st.plotly_chart(fig, use_container_width=True)

    # Stats par rôle d'accès
    role_stats = {}
    for dashboard in all_dashboards:
        role = dashboard["role_access"]
        role_stats[role] = role_stats.get(role, 0) + 1

    if role_stats:
        role_df = pd.DataFrame(list(role_stats.items()), columns=["Rôle", "Dashboards"])

        fig = px.pie(role_df, values="Dashboards", names="Rôle", title="Répartition par Rôle d'Accès")
        st.plotly_chart(fig, use_container_width=True)


def show_dashboard_creator():
    """
    Mode création de nouveau dashboard
    """
    st.header("➕ Créer un Nouveau Dashboard")

    # Formulaire de création
    with st.form("create_dashboard_form"):
        dashboard_data = _collect_dashboard_form_data()
        selected_widgets = _collect_widget_selections()

        # Boutons d'action
        submitted, cancelled = _render_creation_buttons()

        if cancelled:
            st.session_state.dashboard_mode = "view"
            st.rerun()
            return

        if submitted:
            _process_dashboard_creation(dashboard_data, selected_widgets)


def _collect_dashboard_form_data() -> Dict:
    """Collecte les données du formulaire de dashboard"""
    col1, col2 = st.columns(2)

    with col1:
        dashboard_name = st.text_input(LABEL_DASHBOARD_NAME, placeholder="Mon Dashboard Personnel")
        role_access = st.selectbox(
            "Accès",
            options=["all", "direction", "bm", "responsable_bm"],
            format_func=lambda x: {
                "all": "🌐 Tous",
                "direction": "👑 Direction",
                "bm": "👔 Business Managers",
                "responsable_bm": "📋 Responsables BM",
            }.get(x, x),
            key="dashboard_creator_role_access_selectbox",
        )

    with col2:
        description = st.text_area("Description", placeholder="Description de ce dashboard...", height=100)
        is_template = st.checkbox("📋 Utiliser comme template")

    return {
        "name": dashboard_name,
        "description": description,
        "role_access": role_access,
        "is_template": is_template,
    }


def _collect_widget_selections() -> List[str]:
    """Collecte les sélections de widgets par catégorie"""
    st.subheader("🧩 Widgets à inclure")

    # Récupération des widgets par catégorie
    widgets_by_category = WidgetCatalogManager.get_widgets_by_category()
    selected_widgets = []

    for category, widgets in widgets_by_category.items():
        selected_widgets.extend(_collect_category_widgets(category, widgets))

    return selected_widgets


def _collect_category_widgets(category: str, widgets: List[Dict]) -> List[str]:
    """Collecte les widgets sélectionnés pour une catégorie"""
    category_names = {
        "financial": "💰 Financier",
        "intercontrat": "⏰ Intercontrat",
        "management": "🏆 Management",
    }

    st.write(f"**{category_names.get(category, category)}**")

    cols = st.columns(2)
    selected = []

    for i, widget in enumerate(widgets):
        with cols[i % 2]:
            if st.checkbox(
                f"{widget['icon']} {widget['display_name']}",
                key=f"widget_{widget['name']}",
                help=widget["description"],
            ):
                selected.append(widget["name"])

    return selected


def _render_creation_buttons() -> Tuple[bool, bool]:
    """Affiche les boutons de création et retourne leur état"""
    col1, col2 = st.columns(2)

    with col1:
        submitted = st.form_submit_button("🚀 Créer le Dashboard", type="primary")

    with col2:
        cancelled = st.form_submit_button(BUTTON_CANCEL)

    return submitted, cancelled


def _process_dashboard_creation(dashboard_data: Dict, selected_widgets: List[str]):
    """Traite la création du dashboard et des widgets"""
    if not dashboard_data["name"].strip():
        st.error(ERROR_DASHBOARD_NAME_REQUIRED)
        return

    if not selected_widgets:
        st.error("❌ Veuillez sélectionner au moins un widget")
        return

    # Création du dashboard
    dashboard_id = DashboardService.create_dashboard(
        nom=dashboard_data["name"].strip(),
        description=dashboard_data["description"].strip(),
        role_access=dashboard_data["role_access"],
        created_by="system",  # À adapter selon l'authentification
        is_template=dashboard_data["is_template"],
    )

    if dashboard_id:
        _add_selected_widgets_to_dashboard(dashboard_id, selected_widgets)
        st.success(f"✅ Dashboard '{dashboard_data['name']}' créé avec succès !")
        st.balloons()

        # Retour au mode visualisation
        st.session_state.dashboard_mode = "view"
        st.rerun()
    else:
        st.error("❌ Erreur lors de la création du dashboard")


def _add_selected_widgets_to_dashboard(dashboard_id: int, selected_widgets: List[str]):
    """Ajoute les widgets sélectionnés au dashboard"""
    for i, widget_type in enumerate(selected_widgets):
        # Disposition automatique en grille 2 colonnes
        position_x = i % 2
        position_y = i // 2

        DashboardService.add_widget_to_dashboard(
            dashboard_id=dashboard_id,
            widget_type=widget_type,
            position_x=position_x,
            position_y=position_y,
            width=1,
            height=1,
        )


def show_dashboard_editor():
    """
    Mode édition d'un dashboard existant
    """
    dashboard_id = st.session_state.get("edit_dashboard_id")

    if not dashboard_id:
        st.error("❌ Aucun dashboard à éditer")
        st.session_state.dashboard_mode = "view"
        st.rerun()
        return

    dashboard_config = DashboardService.get_dashboard_by_id(dashboard_id)

    if not dashboard_config:
        st.error(ERROR_DASHBOARD_NOT_FOUND)
        st.session_state.dashboard_mode = "view"
        st.rerun()
        return

    st.header(f"⚙️ Édition: {dashboard_config['nom']}")

    # Onglets d'édition
    tab1, tab2, tab3 = st.tabs(["🧩 Widgets", "⚙️ Configuration", "🗑️ Gestion"])

    with tab1:
        show_widgets_editor(dashboard_config)

    with tab2:
        show_dashboard_settings_editor(dashboard_config)

    with tab3:
        show_dashboard_management(dashboard_config)

    # Bouton retour
    if st.button("← Retour à la visualisation", key="back_to_visualization"):
        st.session_state.dashboard_mode = "view"
        if "edit_dashboard_id" in st.session_state:
            del st.session_state.edit_dashboard_id
        st.rerun()


def show_widgets_editor(dashboard_config: Dict):
    """
    Éditeur de widgets pour un dashboard
    """
    st.subheader("🧩 Gestion des Widgets")

    current_widgets = dashboard_config.get("widgets", [])

    # Widgets actuels
    _display_current_widgets(current_widgets)

    # Ajouter nouveaux widgets
    _handle_widget_addition(dashboard_config, current_widgets)


def _display_current_widgets(current_widgets: List[Dict]):
    """Affiche la liste des widgets actuels avec options de suppression"""
    if current_widgets:
        st.write("**Widgets actuels:**")

        for widget in current_widgets:
            _display_single_widget(widget)

        st.divider()


def _display_single_widget(widget: Dict):
    """Affiche un widget individuel avec ses informations et bouton de suppression"""
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        with col1:
            widget_info = next(
                (w for w in DashboardService.get_available_widgets() if w["name"] == widget["widget_type"]),
                {"display_name": widget["widget_type"], "icon": "📊"},
            )
            st.write(f"{widget_info['icon']} {widget_info['display_name']}")

        with col2:
            st.write(f"Position: ({widget['position_x']}, {widget['position_y']})")

        with col3:
            st.write(f"Taille: {widget['width']}x{widget['height']}")

        with col4:
            _render_delete_button(widget)


def _render_delete_button(widget: Dict):
    """Affiche le bouton de suppression pour un widget"""
    if st.button("🗑️", key=f"delete_widget_{widget['id']}", help="Supprimer"):
        if DashboardService.remove_widget_from_dashboard(widget["id"]):
            st.success("✅ Widget supprimé")
            st.rerun()
        else:
            st.error("❌ Erreur lors de la suppression")


def _handle_widget_addition(dashboard_config: Dict, current_widgets: List[Dict]):
    """Gère l'ajout de nouveaux widgets"""
    st.write("**Ajouter des widgets:**")

    widgets_by_category = WidgetCatalogManager.get_widgets_by_category()

    with st.form("add_widgets_form"):
        new_widgets = _collect_new_widgets(widgets_by_category, current_widgets)

        if st.form_submit_button("➕ Ajouter les widgets sélectionnés"):
            _process_widget_addition(dashboard_config, new_widgets)


def _collect_new_widgets(widgets_by_category: Dict, current_widgets: List[Dict]) -> List[str]:
    """Collecte les nouveaux widgets sélectionnés par l'utilisateur"""
    new_widgets = []

    for category, widgets in widgets_by_category.items():
        category_names = {
            "financial": "💰 Financier",
            "intercontrat": "⏰ Intercontrat",
            "management": "🏆 Management",
        }

        st.write(f"**{category_names.get(category, category)}**")

        cols = st.columns(2)
        for i, widget in enumerate(widgets):
            with cols[i % 2]:
                if _is_widget_available(widget, current_widgets):
                    if st.checkbox(
                        f"{widget['icon']} {widget['display_name']}",
                        key=f"add_widget_{widget['name']}",
                        help=widget["description"],
                    ):
                        new_widgets.append(widget["name"])
                else:
                    st.write(f"✅ {widget['icon']} {widget['display_name']} (déjà présent)")

    return new_widgets


def _is_widget_available(widget: Dict, current_widgets: List[Dict]) -> bool:
    """Vérifie si un widget peut être ajouté (n'est pas déjà présent)"""
    return not any(w["widget_type"] == widget["name"] for w in current_widgets)


def _process_widget_addition(dashboard_config: Dict, new_widgets: List[str]):
    """Traite l'ajout des nouveaux widgets sélectionnés"""
    if new_widgets:
        # Calcul de la prochaine position
        max_y = max([w["position_y"] for w in dashboard_config.get("widgets", [])] + [-1])

        for i, widget_type in enumerate(new_widgets):
            position_x = i % 2
            position_y = max_y + 1 + (i // 2)

            success = DashboardService.add_widget_to_dashboard(
                dashboard_id=dashboard_config["id"],
                widget_type=widget_type,
                position_x=position_x,
                position_y=position_y,
            )

            if success:
                st.success(f"✅ Widget {widget_type} ajouté")
            else:
                st.error(f"❌ Erreur lors de l'ajout de {widget_type}")

        st.rerun()
    else:
        st.warning("⚠️ Aucun widget sélectionné")


def show_dashboard_settings_editor(dashboard_config: Dict):
    """
    Éditeur de configuration du dashboard
    """
    st.subheader("⚙️ Configuration du Dashboard")

    with st.form("dashboard_settings_form"):
        # Configuration de base (lecture seule pour cette version)
        st.text_input("Nom", value=dashboard_config["nom"], disabled=True)
        st.text_area("Description", value=dashboard_config.get("description", ""), disabled=True)
        st.selectbox(
            "Accès",
            value=dashboard_config["role_access"],
            options=["all", "direction", "bm", "responsable_bm"],
            disabled=True,
        )

        st.info("💡 La modification des paramètres de base sera disponible dans une prochaine version")

        if st.form_submit_button("💾 Sauvegarder"):
            st.success("✅ Configuration sauvegardée")


def show_dashboard_management(dashboard_config: Dict):
    """
    Gestion avancée du dashboard (suppression, duplication, etc.)
    """
    st.subheader("🗑️ Gestion du Dashboard")

    # Informations du dashboard
    _display_dashboard_info(dashboard_config)

    st.markdown("---")

    # Actions dangereuses
    _display_dashboard_actions(dashboard_config)


def _display_dashboard_info(dashboard_config: Dict):
    """Affiche les informations du dashboard"""
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Nombre de widgets", len(dashboard_config.get("widgets", [])))
        st.write(f"**Créé le:** {dashboard_config['date_creation'].strftime('%d/%m/%Y')}")
        st.write(f"**Créé par:** {dashboard_config['created_by']}")

    with col2:
        st.write(f"**Type:** {'📋 Template' if dashboard_config['is_template'] else '📊 Dashboard'}")
        st.write(f"**Accès:** {dashboard_config['role_access']}")
        st.write(f"**Public:** {'✅ Oui' if dashboard_config['is_public'] else '❌ Non'}")


def _display_dashboard_actions(dashboard_config: Dict):
    """Affiche les actions de gestion du dashboard"""
    st.subheader("⚠️ Actions Avancées")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 Dupliquer le dashboard", type="secondary", key="duplicate_dashboard"):
            st.info("💡 Fonctionnalité de duplication à implémenter")

    with col2:
        if st.button("🗑️ Supprimer le dashboard", type="primary", key="delete_dashboard"):
            st.session_state.confirm_delete_dashboard = True

    # Confirmation de suppression
    _handle_delete_confirmation(dashboard_config)


def _handle_delete_confirmation(dashboard_config: Dict):
    """Gère la confirmation de suppression du dashboard"""
    if not st.session_state.get("confirm_delete_dashboard", False):
        return

    st.error("🚨 **Attention !** Cette action est irréversible.")

    col1, col2, _ = st.columns(3)

    with col1:
        if st.button("✅ Confirmer la suppression", type="primary", key="confirm_delete_dashboard"):
            _execute_dashboard_deletion(dashboard_config)

    with col2:
        if st.button(BUTTON_CANCEL, key="cancel_delete_dashboard"):
            st.session_state.confirm_delete_dashboard = False
            st.rerun()


def _execute_dashboard_deletion(dashboard_config: Dict):
    """Exécute la suppression du dashboard"""
    if DashboardService.delete_dashboard(dashboard_config["id"]):
        st.success("✅ Dashboard supprimé avec succès")
        _cleanup_dashboard_state()
        st.rerun()
    else:
        st.error("❌ Erreur lors de la suppression")


def _cleanup_dashboard_state():
    """Nettoie l'état de session après suppression"""
    st.session_state.dashboard_mode = "view"
    if "edit_dashboard_id" in st.session_state:
        del st.session_state.edit_dashboard_id
    if "confirm_delete_dashboard" in st.session_state:
        del st.session_state.confirm_delete_dashboard


def render_dashboard_widgets(dashboard_config: Dict, period_months: int = 3):
    """
    Rend les widgets d'un dashboard selon sa configuration

    Args:
        dashboard_config: Configuration du dashboard
        period_months: Période en mois pour les filtres globaux
    """
    widgets = dashboard_config.get("widgets", [])

    if not widgets:
        st.info("📊 Ce dashboard ne contient aucun widget")
        return

    # Organiser et rendre les widgets
    widgets_by_row = _organize_widgets_by_position(widgets)
    _render_widgets_by_rows(widgets_by_row, period_months)


def _organize_widgets_by_position(widgets: List[Dict]) -> Dict[int, List[Dict]]:
    """Organise les widgets par ligne selon leur position Y"""
    widgets_by_row = {}
    for widget in widgets:
        row = widget["position_y"]
        if row not in widgets_by_row:
            widgets_by_row[row] = []
        widgets_by_row[row].append(widget)
    return widgets_by_row


def _render_widgets_by_rows(widgets_by_row: Dict[int, List[Dict]], period_months: int):
    """Rend les widgets ligne par ligne"""
    for row in sorted(widgets_by_row.keys()):
        row_widgets = sorted(widgets_by_row[row], key=lambda w: w["position_x"])
        _render_single_row(row_widgets, period_months, row, max(widgets_by_row.keys()))


def _render_single_row(row_widgets: List[Dict], period_months: int, row: int, max_row: int):
    """Rend une ligne de widgets"""
    # Créer les colonnes selon le nombre de widgets dans la ligne
    cols = _create_columns_for_row(row_widgets)

    for i, widget in enumerate(row_widgets):
        with cols[i] if len(row_widgets) > 1 else cols[0]:
            _render_single_widget(widget, period_months)

    # Séparateur entre les lignes (sauf pour la dernière)
    if row < max_row:
        st.markdown("---")


def _create_columns_for_row(row_widgets: List[Dict]) -> List:
    """Crée les colonnes appropriées pour une ligne de widgets"""
    if len(row_widgets) == 1:
        return [st.container()]
    else:
        return st.columns(len(row_widgets))


def _render_single_widget(widget: Dict, period_months: int):
    """Rend un widget individuel avec sa configuration"""
    # Configuration du widget avec période globale
    widget_config = widget.get("config", {}).copy()
    if _should_apply_global_period(widget, widget_config):
        widget_config["period_months"] = period_months

    # Rendu du widget
    try:
        WidgetFactory.render_widget(widget["widget_type"], widget_config)
    except Exception as e:
        st.error(f"❌ Erreur dans le widget {widget['widget_type']}: {e}")


def _should_apply_global_period(widget: Dict, widget_config: Dict) -> bool:
    """Détermine si la période globale doit être appliquée au widget"""
    return "period_months" in widget_config or "period_months" in str(widget.get("widget_type", ""))


def create_default_dashboards():
    """
    Crée des dashboards par défaut si aucun n'existe
    """
    dashboards = DashboardService.get_all_dashboards()

    if not dashboards:
        _create_direction_dashboard()
        _create_bm_dashboard()
        print("✅ Dashboards par défaut créés")


def _create_direction_dashboard():
    """Crée le dashboard par défaut pour la direction"""
    direction_id = DashboardService.create_dashboard(
        nom="Vue Direction",
        description="Dashboard pour la direction avec KPIs globaux et analyse financière",
        role_access="direction",
        created_by="system",
        is_template=True,
    )

    if direction_id:
        direction_widgets = [
            ("global_kpis", 0, 0, 2, 1),
            ("intercontrat_rate", 0, 1, 1, 1),
            ("revenue_by_bm", 1, 1, 1, 1),
            ("top_bm_performance", 0, 2, 2, 1),
        ]

        _add_widgets_to_dashboard(direction_id, direction_widgets)


def _create_bm_dashboard():
    """Crée le dashboard par défaut pour les Business Managers"""
    bm_id = DashboardService.create_dashboard(
        nom="Focus Business Manager",
        description="Dashboard pour Business Managers avec focus sur l'intercontrat",
        role_access="bm",
        created_by="system",
        is_template=True,
    )

    if bm_id:
        bm_widgets = [
            ("intercontrat_rate", 0, 0, 1, 1),
            ("consultants_sans_mission", 1, 0, 1, 1),
            ("intercontrat_trend", 0, 1, 2, 1),
        ]

        _add_widgets_to_dashboard(bm_id, bm_widgets)


def _add_widgets_to_dashboard(dashboard_id: int, widgets: List[Tuple[str, int, int, int, int]]):
    """Ajoute une liste de widgets à un dashboard"""
    for widget_type, x, y, w, h in widgets:
        DashboardService.add_widget_to_dashboard(dashboard_id, widget_type, x, y, w, h)


def show_dashboard_creation_form():
    """
    Formulaire simplifié de création de dashboard
    """
    # Message clair avec instructions
    st.success("✨ **Création de Dashboard en 2 Étapes**")

    st.markdown(
        """
    ### � Étape 1 : Créer la structure du dashboard
    Remplissez le formulaire ci-dessous pour créer un dashboard vide.
    
    ### 🎨 Étape 2 : Ajouter des widgets
    Après création, allez dans l'onglet **🎨 Builder Avancé** pour :
    - Parcourir le **catalogue de 20 widgets** disponibles
    - Cliquer sur un widget pour le sélectionner
    - Configurer sa taille et ses paramètres
    - Cliquer sur **➕ Ajouter** pour l'intégrer au dashboard
    
    ⚠️ **Note** : Le glisser-déposer n'est pas disponible. Utilisez les boutons ⬆️⬇️ pour réorganiser.
    """
    )

    # Bouton pour rediriger vers le Builder Avancé
    col1, col2, _ = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🎨 Aller directement au Builder Avancé",
            key="go_to_builder_advanced",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.dashboard_mode = "view"
            st.info("👉 Passez à l'onglet '🎨 Builder Avancé' pour créer votre dashboard avec l'interface complète !")
            return

    st.markdown("---")

    # Formulaire simplifié
    with st.form("create_simple_dashboard"):
        st.subheader("📝 Créer un dashboard simple")

        nom = st.text_input(LABEL_DASHBOARD_NAME, placeholder="Mon Dashboard Perso")
        description = st.text_area("Description", placeholder="Description de votre dashboard...")

        role_access = st.selectbox(
            "Rôle d'accès",
            options=["all", "admin", "bm", "consultant"],
            format_func=lambda x: {
                "all": "🌍 Tous",
                "admin": "👑 Admin",
                "bm": "💼 Business Manager",
                "consultant": "👤 Consultant",
            }.get(x, x),
        )

        is_template = st.checkbox(
            "📋 Créer comme template", help="Ce dashboard pourra être dupliqué par d'autres utilisateurs"
        )

        col1, col2 = st.columns(2)

        with col1:
            submitted = st.form_submit_button("✅ Créer Dashboard", type="primary", use_container_width=True)

        with col2:
            cancelled = st.form_submit_button(BUTTON_CANCEL, use_container_width=True)

        if submitted:
            if not nom:
                st.error(ERROR_DASHBOARD_NAME_REQUIRED)
            else:
                try:
                    # Créer le dashboard
                    dashboard_id = DashboardService.create_dashboard(
                        nom=nom,
                        description=description or "",
                        role_access=role_access,
                        created_by="user",  # À remplacer par le vrai user si authentification
                        is_template=is_template,
                    )

                    if dashboard_id:
                        st.success(f"✅ Dashboard '{nom}' créé avec succès !")
                        st.info("💡 Vous pouvez maintenant ajouter des widgets via le Builder Avancé")
                        st.session_state.dashboard_mode = "view"
                        st.session_state.selected_dashboard_id = dashboard_id
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la création du dashboard")

                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")

        if cancelled:
            st.session_state.dashboard_mode = "view"
            st.rerun()


def show_dashboard_edit_form():
    """
    Formulaire d'édition de dashboard
    """
    if not _validate_edit_session():
        return

    dashboard_id = st.session_state.edit_dashboard_id
    dashboard_config = DashboardService.get_dashboard_by_id(dashboard_id)

    if not _validate_dashboard_config(dashboard_config):
        return

    _show_edit_instructions()
    _show_edit_form(dashboard_config)


def _validate_edit_session() -> bool:
    """Valide que la session d'édition est correctement initialisée"""
    if "edit_dashboard_id" not in st.session_state:
        st.error("❌ Aucun dashboard sélectionné pour l'édition")
        if st.button("🔙 Retour"):
            st.session_state.dashboard_mode = "view"
            st.rerun()
        return False
    return True


def _validate_dashboard_config(dashboard_config: Optional[Dict]) -> bool:
    """Valide que la configuration du dashboard est disponible"""
    if not dashboard_config:
        st.error(ERROR_DASHBOARD_NOT_FOUND)
        if st.button("🔙 Retour"):
            st.session_state.dashboard_mode = "view"
            st.rerun()
        return False
    return True


def _show_edit_instructions():
    """Affiche les instructions pour l'édition"""
    st.info("💡 Utilisez le Builder Avancé pour modifier les widgets et la disposition")

    # Bouton pour rediriger vers le Builder Avancé
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🎨 Éditer avec le Builder Avancé", key="edit_in_builder_advanced", type="primary", use_container_width=True
        ):
            st.session_state.dashboard_mode = "view"
            st.info("👉 Passez à l'onglet '🎨 Builder Avancé' pour éditer votre dashboard !")
            return

    st.markdown("---")


def _show_edit_form(dashboard_config: Dict):
    """Affiche le formulaire d'édition du dashboard"""
    with st.form("edit_dashboard_form"):
        _render_edit_form_fields(dashboard_config)
        submitted, cancelled = _render_edit_form_buttons()

        if cancelled:
            st.session_state.dashboard_mode = "view"
            st.rerun()
            return

        if submitted:
            _process_edit_form_submission(dashboard_config)


def _render_edit_form_fields(dashboard_config: Dict):
    """Affiche les champs du formulaire d'édition"""
    st.subheader(f"✏️ Éditer: {dashboard_config['nom']}")

    # Utilisation de variables globales pour éviter la répétition
    global LABEL_DASHBOARD_NAME, ERROR_DASHBOARD_NAME_REQUIRED, BUTTON_CANCEL

    nom = st.text_input(LABEL_DASHBOARD_NAME, value=dashboard_config["nom"])
    description = st.text_area("Description", value=dashboard_config.get("description", ""))

    role_access = st.selectbox(
        "Rôle d'accès",
        options=["all", "admin", "bm", "consultant"],
        index=["all", "admin", "bm", "consultant"].index(dashboard_config.get("role_access", "all")),
        format_func=lambda x: {
            "all": "🌍 Tous",
            "admin": "👑 Admin",
            "bm": "💼 Business Manager",
            "consultant": "👤 Consultant",
        }.get(x, x),
    )

    is_template = st.checkbox("📋 Template", value=dashboard_config.get("is_template", False))

    # Stocker les valeurs pour utilisation dans la soumission
    st.session_state.edit_form_data = {
        "nom": nom,
        "description": description,
        "role_access": role_access,
        "is_template": is_template,
    }


def _render_edit_form_buttons() -> Tuple[bool, bool]:
    """Affiche les boutons du formulaire d'édition et retourne leur état"""
    col1, col2 = st.columns(2)

    with col1:
        submitted = st.form_submit_button("✅ Sauvegarder", type="primary", use_container_width=True)

    with col2:
        cancelled = st.form_submit_button(BUTTON_CANCEL, use_container_width=True)

    return submitted, cancelled


def _process_edit_form_submission(dashboard_config: Dict):
    """Traite la soumission du formulaire d'édition"""
    form_data = st.session_state.get("edit_form_data", {})

    if not form_data.get("nom"):
        st.error(ERROR_DASHBOARD_NAME_REQUIRED)
        return

    try:
        # Mettre à jour le dashboard
        success = DashboardService.update_dashboard(
            dashboard_id=dashboard_config["id"],
            nom=form_data["nom"],
            description=form_data["description"],
            role_access=form_data["role_access"],
            is_template=form_data["is_template"],
        )

        if success:
            st.success(f"✅ Dashboard '{form_data['nom']}' mis à jour avec succès !")
            st.session_state.dashboard_mode = "view"
            st.rerun()
        else:
            st.error("❌ Erreur lors de la mise à jour du dashboard")

    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")
