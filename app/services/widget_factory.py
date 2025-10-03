"""
Factory pattern pour les widgets de dashboard
Centralise la création et le rendu des différents types de widgets
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional
from datetime import datetime, date

from app.services.dashboard_service import DashboardDataService


class WidgetFactory:
    """
    Factory pour créer et rendre les widgets de dashboard
    """

    @staticmethod
    def render_widget(widget_type: str, config: Dict[str, Any] = None) -> None:
        """
        Rend un widget selon son type

        Args:
            widget_type: Type du widget à rendre
            config: Configuration spécifique du widget
        """
        config = config or {}

        # Mapping des types de widgets vers leurs fonctions de rendu
        widget_renderers = {
            "intercontrat_rate": WidgetFactory._render_intercontrat_rate,
            "consultants_sans_mission": WidgetFactory._render_consultants_sans_mission,
            "revenue_by_bm": WidgetFactory._render_revenue_by_bm,
            "global_kpis": WidgetFactory._render_global_kpis,
            "intercontrat_trend": WidgetFactory._render_intercontrat_trend,
            "top_bm_performance": WidgetFactory._render_top_bm_performance,
        }

        renderer = widget_renderers.get(widget_type)
        if renderer:
            try:
                renderer(config)
            except Exception as e:
                st.error(f"❌ Erreur dans le widget {widget_type}: {e}")
        else:
            st.warning(f"⚠️ Widget type '{widget_type}' non reconnu")

    @staticmethod
    def _render_intercontrat_rate(config: Dict) -> None:
        """
        Widget: Taux d'intercontrat global
        """
        st.subheader("⏰ Taux d'Intercontrat")

        bm_filter = config.get("bm_filter")
        data = DashboardDataService.get_intercontrat_data(bm_filter)

        taux = data["taux_intercontrat"]
        total = data["total_consultants"]
        intercontrat = data["consultants_intercontrat"]

        # Couleur selon le seuil
        if taux > 15:
            color = "red"
            status = "🔴 Critique"
        elif taux > 10:
            color = "orange"
            status = "🟠 Attention"
        else:
            color = "green"
            status = "🟢 Normal"

        # Métriques principales
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Taux d'intercontrat", f"{taux}%", help="Pourcentage de consultants sans mission en cours")

        with col2:
            st.metric(
                "Consultants concernés",
                f"{intercontrat}/{total}",
                help="Nombre de consultants en intercontrat sur le total",
            )

        with col3:
            st.write(f"**Statut:** {status}")

        # Graphique en gauge si possible, sinon barre de progression
        if taux > 0:
            # Barre de progression colorée
            progress_html = f"""
            <div style="
                background-color: #f0f0f0;
                border-radius: 10px;
                padding: 5px;
                margin: 10px 0;
            ">
                <div style="
                    background-color: {color};
                    width: {min(taux, 25)}%;
                    height: 20px;
                    border-radius: 5px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                ">
                    {taux}%
                </div>
            </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)

    @staticmethod
    def _render_consultants_sans_mission(config: Dict) -> None:
        """
        Widget: Liste des consultants sans mission
        """
        st.subheader("👥 Consultants en Intercontrat")

        bm_filter = config.get("bm_filter")
        data = DashboardDataService.get_intercontrat_data(bm_filter)

        consultants = data["consultants_sans_mission"]

        if not consultants:
            st.success("🎉 Aucun consultant en intercontrat !")
            return

        # Tableau des consultants
        df_consultants = pd.DataFrame(consultants)

        # Configuration du tableau
        st.dataframe(
            df_consultants,
            column_config={
                "nom": st.column_config.TextColumn("Consultant", width="large"),
                "email": st.column_config.TextColumn("Email", width="large"),
                "derniere_mission": st.column_config.TextColumn("Dernière mission", width="medium"),
            },
            hide_index=True,
            use_container_width=True,
        )

        # Résumé
        st.caption(f"📊 **{len(consultants)}** consultant(s) en intercontrat")

    @staticmethod
    def _render_revenue_by_bm(config: Dict) -> None:
        """
        Widget: Revenus par Business Manager
        """
        st.subheader("💰 Revenus par Business Manager")

        period_months = config.get("period_months", 3)
        data = DashboardDataService.get_revenue_by_bm_data(period_months)

        bm_revenues = data["bm_revenues"]

        if not bm_revenues:
            st.info("📊 Aucune donnée de revenus disponible")
            return

        # Création du DataFrame
        df = pd.DataFrame(bm_revenues)

        # Graphique en barres
        fig = px.bar(
            df,
            x="bm_name",
            y="ca_estime",
            title=f"CA Estimé ({period_months} derniers mois)",
            labels={"bm_name": "Business Manager", "ca_estime": "CA Estimé (€)"},
            color="ca_estime",
            color_continuous_scale="Viridis",
        )

        fig.update_layout(xaxis_tickangle=-45, height=400, showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

        # Métriques résumées
        col1, col2, col3 = st.columns(3)

        with col1:
            total_ca = sum(bm["ca_estime"] for bm in bm_revenues)
            st.metric("CA Total", f"{total_ca:,.0f} €")

        with col2:
            avg_tjm = sum(bm["tjm_moyen"] for bm in bm_revenues) / len(bm_revenues) if bm_revenues else 0
            st.metric("TJM Moyen", f"{avg_tjm:.0f} €")

        with col3:
            total_missions = sum(bm["missions_count"] for bm in bm_revenues)
            st.metric("Total Missions", f"{total_missions}")

    @staticmethod
    def _render_global_kpis(config: Dict) -> None:
        """
        Widget: KPIs globaux
        """
        st.subheader("📊 KPIs Globaux")

        # Données d'intercontrat
        intercontrat_data = DashboardDataService.get_intercontrat_data()

        # Données de revenus
        revenue_data = DashboardDataService.get_revenue_by_bm_data(1)  # 1 mois

        # Affichage en colonnes
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Total Consultants",
                intercontrat_data["total_consultants"],
                help="Nombre total de consultants actifs",
            )

        with col2:
            st.metric(
                "⏰ Taux Intercontrat",
                f"{intercontrat_data['taux_intercontrat']}%",
                delta=(
                    f"-{intercontrat_data['taux_intercontrat'] - 12:.1f}%"
                    if intercontrat_data["taux_intercontrat"] > 12
                    else None
                ),
                delta_color="inverse",
                help="Pourcentage de consultants sans mission",
            )

        with col3:
            total_missions = sum(bm["missions_count"] for bm in revenue_data["bm_revenues"])
            st.metric("🎯 Missions Actives", total_missions, help="Nombre de missions en cours ce mois")

        with col4:
            ca_mensuel = sum(bm["ca_estime"] for bm in revenue_data["bm_revenues"])
            st.metric("💰 CA Mensuel", f"{ca_mensuel:,.0f} €", help="Chiffre d'affaires estimé du mois")

    @staticmethod
    def _render_intercontrat_trend(config: Dict) -> None:
        """
        Widget: Tendance d'évolution de l'intercontrat
        """
        st.subheader("📈 Évolution Intercontrat")

        # Pour cette démo, on simule des données de tendance
        # Dans la vraie implémentation, on irait chercher l'historique
        current_data = DashboardDataService.get_intercontrat_data()

        dates = pd.date_range(start="2025-07-01", end="2025-10-01", freq="M")
        taux_simules = [8.5, 12.2, 15.1, current_data["taux_intercontrat"]]

        df_trend = pd.DataFrame({"Date": dates[: len(taux_simules)], "Taux": taux_simules[: len(dates)]})

        fig = px.line(df_trend, x="Date", y="Taux", title="Évolution du Taux d'Intercontrat", markers=True)

        # Ligne de seuil critique à 15%
        fig.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="Seuil critique (15%)")

        fig.update_layout(yaxis_title="Taux d'Intercontrat (%)", height=300)

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def _render_top_bm_performance(config: Dict) -> None:
        """
        Widget: Top des Business Managers par performance
        """
        st.subheader("🏆 Top Business Managers")

        period_months = config.get("period_months", 3)
        data = DashboardDataService.get_revenue_by_bm_data(period_months)

        bm_revenues = data["bm_revenues"]

        if not bm_revenues:
            st.info("📊 Aucune donnée disponible")
            return

        # Tri par CA estimé décroissant
        top_bms = sorted(bm_revenues, key=lambda x: x["ca_estime"], reverse=True)[:5]

        # Affichage du top 5
        for i, bm in enumerate(top_bms, 1):
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 3, 2, 2])

                with col1:
                    # Médaille pour le podium
                    if i == 1:
                        medal = "🥇"
                    elif i == 2:
                        medal = "🥈"
                    elif i == 3:
                        medal = "🥉"
                    else:
                        medal = f"{i}️⃣"
                    st.write(f"### {medal}")

                with col2:
                    st.write(f"**{bm['bm_name']}**")

                with col3:
                    st.write(f"💰 {bm['ca_estime']:,.0f} €")

                with col4:
                    st.write(f"🎯 {bm['missions_count']} missions")

                if i < len(top_bms):
                    st.divider()


class WidgetCatalogManager:
    """
    Gestionnaire du catalogue de widgets
    """

    @staticmethod
    def initialize_widget_catalog():
        """
        Initialise le catalogue de widgets avec les widgets de base
        """
        from app.database.database import get_database_session
        from app.database.models import WidgetCatalog

        widgets_to_create = [
            {
                "name": "intercontrat_rate",
                "category": "intercontrat",
                "display_name": "Taux d'Intercontrat",
                "description": "Affiche le pourcentage de consultants sans mission",
                "icon": "⏰",
                "render_function": "intercontrat_rate",
                "config_schema": {"bm_filter": "integer"},
            },
            {
                "name": "consultants_sans_mission",
                "category": "intercontrat",
                "display_name": "Consultants en Intercontrat",
                "description": "Liste détaillée des consultants sans mission",
                "icon": "👥",
                "render_function": "consultants_sans_mission",
                "config_schema": {"bm_filter": "integer"},
            },
            {
                "name": "revenue_by_bm",
                "category": "financial",
                "display_name": "Revenus par BM",
                "description": "Graphique des revenus par Business Manager",
                "icon": "💰",
                "render_function": "revenue_by_bm",
                "config_schema": {"period_months": "integer"},
            },
            {
                "name": "global_kpis",
                "category": "management",
                "display_name": "KPIs Globaux",
                "description": "Indicateurs de performance globaux",
                "icon": "📊",
                "render_function": "global_kpis",
                "config_schema": {},
            },
            {
                "name": "intercontrat_trend",
                "category": "intercontrat",
                "display_name": "Tendance Intercontrat",
                "description": "Évolution du taux d'intercontrat dans le temps",
                "icon": "📈",
                "render_function": "intercontrat_trend",
                "config_schema": {},
            },
            {
                "name": "top_bm_performance",
                "category": "management",
                "display_name": "Top BM Performance",
                "description": "Classement des meilleurs Business Managers",
                "icon": "🏆",
                "render_function": "top_bm_performance",
                "config_schema": {"period_months": "integer"},
            },
        ]

        try:
            with get_database_session() as session:
                for widget_data in widgets_to_create:
                    # Vérifier si le widget existe déjà
                    existing = session.query(WidgetCatalog).filter(WidgetCatalog.name == widget_data["name"]).first()

                    if not existing:
                        widget = WidgetCatalog(**widget_data)
                        session.add(widget)

                session.commit()
                print("✅ Catalogue de widgets initialisé avec succès")

        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation du catalogue: {e}")

    @staticmethod
    def get_widgets_by_category():
        """
        Récupère les widgets organisés par catégorie
        """
        from app.services.dashboard_service import DashboardService

        widgets = DashboardService.get_available_widgets()

        categories = {}
        for widget in widgets:
            category = widget["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(widget)

        return categories
