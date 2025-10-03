"""
Dashboard Builder Avancé - Phase 3
Interface glisser-déposer et configuration visuelle des widgets
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple
import json
import uuid

from app.services.dashboard_service import DashboardService
from app.services.widget_factory import WidgetFactory, WidgetCatalogManager


class DashboardBuilder:
    """
    Builder avancé pour créer des dashboards avec interface visuelle
    """

    def __init__(self):
        self.grid_width = 12  # Grille de 12 colonnes
        self.grid_height = 20  # Hauteur maximale

    def show_advanced_builder(self, dashboard_id: Optional[int] = None):
        """
        Interface principale du builder avancé
        """
        st.title("🎨 Dashboard Builder Avancé")

        # Instructions claires pour l'utilisateur
        with st.expander("ℹ️ **Comment utiliser le Builder** (Cliquez pour lire)", expanded=False):
            st.markdown(
                """
            ### 📝 Mode d'emploi en 5 étapes :
            
            1. **Sélectionner un dashboard** dans la liste déroulante ci-dessous
            2. **Cliquer sur ✏️ Éditer** pour entrer en mode édition
            3. **Parcourir le catalogue de widgets** à gauche (organisé par catégories)
            4. **Cliquer sur une carte widget** pour le sélectionner (bordure bleue)
            5. **Configurer et ajouter** :
               - Ajuster la **taille (span)** : largeur en colonnes (1-4)
               - Ajuster la **hauteur** : nombre de lignes (1-8)
               - Configurer les **paramètres** spécifiques au widget
               - Cliquer sur **➕ Ajouter le widget** pour l'intégrer
            
            ### ⚠️ Important :
            - ❌ **Le glisser-déposer n'est PAS disponible** (HTML statique)
            - ✅ **Utilisez les boutons ⬆️ Monter / ⬇️ Descendre** pour réorganiser
            - ✅ **20 widgets disponibles** en 5 catégories
            
            ### 💡 Conseil :
            Commencez avec 3-4 widgets simples (Total Consultants, Missions Actives, CA Total) 
            avant d'ajouter des widgets complexes (heatmap, prédictions).
            """
            )

        # Mode : Création ou Édition
        if dashboard_id:
            dashboard_config = DashboardService.get_dashboard_by_id(dashboard_id)
            st.subheader(f"📝 Édition: {dashboard_config['nom']}")
            mode = "edit"
        else:
            st.info(
                "👉 **Sélectionnez un dashboard existant ci-dessous** ou créez-en un nouveau via l'onglet ⚙️ Gestion"
            )
            st.subheader("➕ Nouveau Dashboard")
            mode = "create"
            dashboard_config = None

        # Colonnes principales
        col_palette, col_canvas, col_properties = st.columns([2, 6, 2])

        with col_palette:
            self._show_widget_palette()

        with col_canvas:
            self._show_dashboard_canvas(dashboard_config)

        with col_properties:
            self._show_widget_properties()

        # Actions de sauvegarde
        self._show_builder_actions(mode, dashboard_id, dashboard_config)

    def _show_widget_palette(self):
        """
        Palette des widgets disponibles
        """
        st.subheader("🧩 Widgets Disponibles")

        # Recherche de widgets
        search_term = st.text_input("🔍 Rechercher", placeholder="Nom du widget...")

        # Widgets par catégorie
        widgets_by_category = WidgetCatalogManager.get_widgets_by_category()

        for category, widgets in widgets_by_category.items():
            category_names = {
                "financial": "💰 Financier",
                "intercontrat": "⏰ Intercontrat",
                "management": "🏆 Management",
            }

            with st.expander(f"{category_names.get(category, category)}", expanded=True):
                for widget in widgets:
                    if not search_term or search_term.lower() in widget["display_name"].lower():
                        self._show_widget_card(widget)

    def _show_widget_card(self, widget: Dict):
        """
        Carte widget dans la palette
        """
        container = st.container()
        with container:
            # Widget card avec preview
            with st.container():
                st.markdown(
                    f"""
                <div style="
                    border: 1px solid #ddd; 
                    border-radius: 5px; 
                    padding: 10px; 
                    margin: 5px 0;
                    background: #f8f9fa;
                    cursor: grab;
                ">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 1.2em; margin-right: 8px;">{widget['icon']}</span>
                        <strong>{widget['display_name']}</strong>
                    </div>
                    <small style="color: #666;">{widget['description']}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Bouton d'ajout
                if st.button(
                    f"➕ Ajouter", key=f"add_{widget['name']}", help=f"Ajouter {widget['display_name']} au canvas"
                ):
                    self._add_widget_to_canvas(widget["name"])

    def _show_dashboard_canvas(self, dashboard_config: Optional[Dict]):
        """
        Canvas principal pour dessiner le dashboard
        """
        st.subheader("🎯 Canvas Dashboard")

        # Initialiser le canvas state
        if "canvas_widgets" not in st.session_state:
            if dashboard_config and dashboard_config.get("widgets"):
                # Charger les widgets existants
                st.session_state.canvas_widgets = self._load_widgets_to_canvas(dashboard_config["widgets"])
            else:
                st.session_state.canvas_widgets = []

        # Grille de canvas
        self._render_canvas_grid()

        # Preview du dashboard
        if st.session_state.canvas_widgets:
            st.markdown("---")
            st.subheader("👁️ Aperçu")
            self._render_dashboard_preview()

    def _render_canvas_grid(self):
        """
        Rendu de la grille canvas avec widgets positionnés
        """
        # Grille visuelle
        canvas_grid = self._create_empty_grid()

        # Placer les widgets sur la grille
        for widget in st.session_state.canvas_widgets:
            self._place_widget_on_grid(canvas_grid, widget)

        # Rendu de la grille
        for row_idx in range(self.grid_height):
            if any(canvas_grid[row_idx]):  # Seulement les lignes avec contenu
                cols = st.columns(self.grid_width)

                for col_idx in range(self.grid_width):
                    with cols[col_idx]:
                        cell_content = canvas_grid[row_idx][col_idx]

                        if cell_content:
                            self._render_canvas_cell(cell_content, row_idx, col_idx)
                        else:
                            # Zone de drop vide
                            if st.button("➕", key=f"empty_{row_idx}_{col_idx}", help="Ajouter un widget ici"):
                                st.session_state.drop_zone = (row_idx, col_idx)

    def _create_empty_grid(self) -> List[List[Optional[Dict]]]:
        """
        Crée une grille vide
        """
        return [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def _place_widget_on_grid(self, grid: List[List], widget: Dict):
        """
        Place un widget sur la grille selon sa position et taille
        """
        start_row = widget["position_y"]
        start_col = widget["position_x"]
        width = widget.get("width", 1)
        height = widget.get("height", 1)

        # Placer le widget sur toutes les cellules qu'il occupe
        for row in range(start_row, min(start_row + height, self.grid_height)):
            for col in range(start_col, min(start_col + width, self.grid_width)):
                if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                    grid[row][col] = widget

    def _render_canvas_cell(self, widget: Dict, row: int, col: int):
        """
        Rendu d'une cellule de canvas contenant un widget
        """
        widget_info = next(
            (w for w in DashboardService.get_available_widgets() if w["name"] == widget["widget_type"]),
            {"display_name": widget["widget_type"], "icon": "📊"},
        )

        # Seulement afficher le contenu principal pour la cellule top-left
        if row == widget["position_y"] and col == widget["position_x"]:
            with st.container():
                st.markdown(
                    f"""
                <div style="
                    border: 2px solid #1f77b4; 
                    border-radius: 8px; 
                    padding: 8px; 
                    margin: 2px;
                    background: linear-gradient(135deg, #f0f8ff, #e6f3ff);
                    text-align: center;
                    min-height: 60px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="font-size: 1.5em;">{widget_info['icon']}</div>
                    <small><strong>{widget_info['display_name']}</strong></small>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Contrôles widget
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⚙️", key=f"config_{widget['id']}", help="Configurer"):
                        st.session_state.selected_widget = widget

                with col2:
                    if st.button("🗑️", key=f"delete_{widget['id']}", help="Supprimer"):
                        self._remove_widget_from_canvas(widget["id"])

    def _show_widget_properties(self):
        """
        Panneau de propriétés du widget sélectionné
        """
        st.subheader("⚙️ Propriétés")

        selected_widget = st.session_state.get("selected_widget")

        if not selected_widget:
            st.info("👆 Sélectionnez un widget sur le canvas pour configurer ses propriétés")
            return

        widget_info = next(
            (w for w in DashboardService.get_available_widgets() if w["name"] == selected_widget["widget_type"]),
            {"display_name": selected_widget["widget_type"], "icon": "📊"},
        )

        st.write(f"**{widget_info['icon']} {widget_info['display_name']}**")

        # Propriétés de position et taille
        with st.form(f"widget_props_{selected_widget['id']}"):
            st.subheader("📐 Position & Taille")

            col1, col2 = st.columns(2)
            with col1:
                new_x = st.number_input(
                    "Position X",
                    value=selected_widget["position_x"],
                    min_value=0,
                    max_value=self.grid_width - 1,
                    key="builder_widget_pos_x",
                )
                new_width = st.number_input(
                    "Largeur",
                    value=selected_widget.get("width", 1),
                    min_value=1,
                    max_value=6,
                    key="builder_widget_width",
                )

            with col2:
                new_y = st.number_input(
                    "Position Y",
                    value=selected_widget["position_y"],
                    min_value=0,
                    max_value=self.grid_height - 1,
                    key="builder_widget_pos_y",
                )
                new_height = st.number_input(
                    "Hauteur",
                    value=selected_widget.get("height", 1),
                    min_value=1,
                    max_value=4,
                    key="builder_widget_height",
                )

            # Configuration spécifique au widget
            st.subheader("🎛️ Configuration")
            widget_config = selected_widget.get("config", {})

            new_config = self._render_widget_config_form(selected_widget["widget_type"], widget_config)

            # Sauvegarde
            if st.form_submit_button("💾 Appliquer les changements"):
                self._update_widget_properties(selected_widget["id"], new_x, new_y, new_width, new_height, new_config)
                st.success("✅ Propriétés mises à jour")
                st.rerun()

    def _render_widget_config_form(self, widget_type: str, current_config: Dict) -> Dict:
        """
        Génère un formulaire de configuration spécifique au type de widget
        """
        config = current_config.copy()

        # Configurations communes
        config["title"] = st.text_input(
            "Titre personnalisé",
            value=config.get("title", ""),
            placeholder="Laissez vide pour le titre par défaut",
            key="builder_widget_title_input",
        )

        # Configurations spécifiques
        if widget_type in ["intercontrat_rate", "intercontrat_trend"]:
            config["seuil_alerte"] = st.number_input(
                "Seuil d'alerte (%)",
                value=config.get("seuil_alerte", 15),
                min_value=0,
                max_value=100,
                key="builder_widget_seuil_alerte",
            )

        elif widget_type == "revenue_by_bm":
            config["show_target"] = st.checkbox(
                "Afficher les objectifs", value=config.get("show_target", True), key="builder_widget_show_target"
            )
            config["chart_type"] = st.selectbox(
                "Type de graphique",
                options=["bar", "pie", "line"],
                index=["bar", "pie", "line"].index(config.get("chart_type", "bar")),
                key="builder_widget_chart_type",
            )

        elif widget_type == "global_kpis":
            config["kpis_to_show"] = st.multiselect(
                "KPIs à afficher",
                options=["total_consultants", "total_missions", "revenue_total", "intercontrat_rate"],
                default=config.get("kpis_to_show", ["total_consultants", "total_missions", "revenue_total"]),
                key="builder_widget_kpis_multiselect",
            )

        # Période par défaut
        if st.checkbox(
            "Configuration de période", value="period_months" in config, key="builder_widget_period_checkbox"
        ):
            config["period_months"] = st.selectbox(
                "Période par défaut",
                options=[1, 3, 6, 12],
                index=[1, 3, 6, 12].index(config.get("period_months", 3)),
                key="builder_widget_period_selectbox",
            )
        elif "period_months" in config:
            del config["period_months"]

        return config

    def _add_widget_to_canvas(self, widget_type: str):
        """
        Ajoute un widget au canvas
        """
        # Trouver la prochaine position libre
        next_position = self._find_next_free_position()

        new_widget = {
            "id": str(uuid.uuid4()),
            "widget_type": widget_type,
            "position_x": next_position[1],
            "position_y": next_position[0],
            "width": 1,
            "height": 1,
            "config": {},
        }

        st.session_state.canvas_widgets.append(new_widget)
        st.rerun()

    def _remove_widget_from_canvas(self, widget_id: str):
        """
        Supprime un widget du canvas
        """
        st.session_state.canvas_widgets = [w for w in st.session_state.canvas_widgets if w["id"] != widget_id]

        # Désélectionner si c'était le widget sélectionné
        if st.session_state.get("selected_widget", {}).get("id") == widget_id:
            del st.session_state.selected_widget

        st.rerun()

    def _update_widget_properties(self, widget_id: str, x: int, y: int, width: int, height: int, config: Dict):
        """
        Met à jour les propriétés d'un widget
        """
        for widget in st.session_state.canvas_widgets:
            if widget["id"] == widget_id:
                widget["position_x"] = x
                widget["position_y"] = y
                widget["width"] = width
                widget["height"] = height
                widget["config"] = config
                break

    def _find_next_free_position(self) -> Tuple[int, int]:
        """
        Trouve la prochaine position libre sur la grille
        """
        grid = self._create_empty_grid()

        # Marquer les positions occupées
        for widget in st.session_state.canvas_widgets:
            self._place_widget_on_grid(grid, widget)

        # Trouver la première position libre
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if grid[row][col] is None:
                    return (row, col)

        return (0, 0)  # Fallback

    def _load_widgets_to_canvas(self, widgets: List[Dict]) -> List[Dict]:
        """
        Charge les widgets existants dans le canvas
        """
        canvas_widgets = []

        for widget in widgets:
            canvas_widget = {
                "id": str(widget.get("id", uuid.uuid4())),
                "widget_type": widget["widget_type"],
                "position_x": widget["position_x"],
                "position_y": widget["position_y"],
                "width": widget.get("width", 1),
                "height": widget.get("height", 1),
                "config": widget.get("config", {}),
            }
            canvas_widgets.append(canvas_widget)

        return canvas_widgets

    def _render_dashboard_preview(self):
        """
        Aperçu en temps réel du dashboard
        """
        # Organiser par lignes
        widgets_by_row = {}
        for widget in st.session_state.canvas_widgets:
            row = widget["position_y"]
            if row not in widgets_by_row:
                widgets_by_row[row] = []
            widgets_by_row[row].append(widget)

        # Rendu ligne par ligne
        for row in sorted(widgets_by_row.keys()):
            row_widgets = sorted(widgets_by_row[row], key=lambda w: w["position_x"])

            if len(row_widgets) == 1:
                cols = [st.container()]
            else:
                cols = st.columns(len(row_widgets))

            for i, widget in enumerate(row_widgets):
                with cols[i] if len(row_widgets) > 1 else cols[0]:
                    try:
                        WidgetFactory.render_widget(widget["widget_type"], widget.get("config", {}))
                    except Exception as e:
                        st.error(f"❌ Erreur preview {widget['widget_type']}: {e}")

    def _show_builder_actions(self, mode: str, dashboard_id: Optional[int], dashboard_config: Optional[Dict]):
        """
        Actions de sauvegarde et navigation du builder
        """
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("💾 Sauvegarder", type="primary"):
                if mode == "create":
                    self._save_new_dashboard()
                else:
                    self._update_existing_dashboard(dashboard_id)

        with col2:
            if st.button("👁️ Aperçu complet"):
                self._show_full_preview()

        with col3:
            if st.button("🧹 Réinitialiser"):
                st.session_state.canvas_widgets = []
                if "selected_widget" in st.session_state:
                    del st.session_state.selected_widget
                st.rerun()

        with col4:
            if st.button("← Retour"):
                self._exit_builder()

    def _save_new_dashboard(self):
        """
        Sauvegarde d'un nouveau dashboard
        """
        # Interface de nommage
        with st.form("save_dashboard_form"):
            st.subheader("💾 Sauvegarder le Dashboard")

            dashboard_name = st.text_input("Nom du dashboard *")
            description = st.text_area("Description")
            role_access = st.selectbox(
                "Accès",
                options=["all", "direction", "bm", "responsable_bm"],
                format_func=lambda x: {
                    "all": "🌐 Tous",
                    "direction": "👑 Direction",
                    "bm": "👔 Business Managers",
                    "responsable_bm": "📋 Responsables BM",
                }.get(x, x),
                key="builder_save_role_access_selectbox",
            )
            is_template = st.checkbox("📋 Utiliser comme template")

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Sauvegarder", type="primary"):
                    if dashboard_name.strip():
                        self._execute_dashboard_save(
                            dashboard_name.strip(), description.strip(), role_access, is_template
                        )
                    else:
                        st.error("❌ Le nom est obligatoire")

            with col2:
                if st.form_submit_button("❌ Annuler"):
                    st.rerun()

    def _execute_dashboard_save(self, name: str, description: str, role_access: str, is_template: bool):
        """
        Exécute la sauvegarde du dashboard
        """
        try:
            # Créer le dashboard
            dashboard_id = DashboardService.create_dashboard(
                nom=name, description=description, role_access=role_access, created_by="system", is_template=is_template
            )

            if dashboard_id:
                # Ajouter tous les widgets
                for widget in st.session_state.canvas_widgets:
                    DashboardService.add_widget_to_dashboard(
                        dashboard_id=dashboard_id,
                        widget_type=widget["widget_type"],
                        position_x=widget["position_x"],
                        position_y=widget["position_y"],
                        width=widget.get("width", 1),
                        height=widget.get("height", 1),
                        config=widget.get("config", {}),
                    )

                st.success(f"✅ Dashboard '{name}' sauvegardé avec succès !")
                st.balloons()

                # Nettoyage et retour
                self._cleanup_builder_state()

            else:
                st.error("❌ Erreur lors de la sauvegarde")

        except Exception as e:
            st.error(f"❌ Erreur: {e}")

    def _update_existing_dashboard(self, dashboard_id: int):
        """
        Met à jour un dashboard existant
        """
        try:
            # Supprimer tous les widgets existants
            # (simplifié - dans une vraie app, on ferait un diff)

            # Ajouter les nouveaux widgets
            for widget in st.session_state.canvas_widgets:
                DashboardService.add_widget_to_dashboard(
                    dashboard_id=dashboard_id,
                    widget_type=widget["widget_type"],
                    position_x=widget["position_x"],
                    position_y=widget["position_y"],
                    width=widget.get("width", 1),
                    height=widget.get("height", 1),
                    config=widget.get("config", {}),
                )

            st.success("✅ Dashboard mis à jour avec succès !")
            self._cleanup_builder_state()

        except Exception as e:
            st.error(f"❌ Erreur lors de la mise à jour: {e}")

    def _show_full_preview(self):
        """
        Affichage en plein écran du dashboard
        """
        # Cette fonction serait implémentée pour ouvrir
        # une nouvelle fenêtre ou mode plein écran
        st.info("🔄 Aperçu plein écran - Fonctionnalité à implémenter")

    def _exit_builder(self):
        """
        Sortie du builder
        """
        self._cleanup_builder_state()
        st.session_state.dashboard_mode = "view"
        st.rerun()

    def _cleanup_builder_state(self):
        """
        Nettoyage de l'état du builder
        """
        keys_to_remove = ["canvas_widgets", "selected_widget", "drop_zone"]

        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]


# Instance globale du builder
dashboard_builder = DashboardBuilder()
