"""
Dashboard Advanced Features - Phase 4
Fonctionnalités avancées : filtres temporels, exports, alertes, AI insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import io

# Imports optionnels pour exports
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

from app.services.dashboard_service import DashboardService, DashboardDataService
from app.database.database import get_database_session
from app.database.models import Consultant, Mission


class AdvancedDashboardFeatures:
    """
    Fonctionnalités avancées pour les dashboards
    """
    
    def __init__(self):
        self.data_service = DashboardDataService()
    
    def show_advanced_filters(self, context: str = "default") -> Dict[str, Any]:
        """
        Panneau de filtres avancés
        """
        st.sidebar.subheader("🔍 Filtres Avancés")
        
        filters = {}
        
        # Filtre temporel avancé
        with st.sidebar.expander("📅 Période", expanded=True):
            date_mode = st.radio(
                "Mode de sélection",
                options=["Prédéfini", "Personnalisé"],
                index=0,
                key=f"dashboard_date_mode_radio_{context}"
            )
            
            if date_mode == "Prédéfini":
                period = st.selectbox(
                    "Période",
                    options=["7 jours", "1 mois", "3 mois", "6 mois", "12 mois", "2 ans"],
                    index=2,
                    key=f"dashboard_period_selectbox_{context}"
                )
                filters['period_predefined'] = period
                
                # Conversion en dates
                period_map = {
                    "7 jours": 7,
                    "1 mois": 30,
                    "3 mois": 90,
                    "6 mois": 180,
                    "12 mois": 365,
                    "2 ans": 730
                }
                
                end_date = datetime.now()
                start_date = end_date - timedelta(days=period_map[period])
                
            else:
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input(
                        "Du",
                        value=datetime.now() - timedelta(days=90),
                        max_value=datetime.now(),
                        key=f"dashboard_start_date_input_{context}"
                    )
                
                with col2:
                    end_date = st.date_input(
                        "Au",
                        value=datetime.now(),
                        max_value=datetime.now(),
                        key=f"dashboard_end_date_input_{context}"
                    )
                
                start_date = datetime.combine(start_date, datetime.min.time())
                end_date = datetime.combine(end_date, datetime.max.time())
            
            filters['start_date'] = start_date
            filters['end_date'] = end_date
        
        # Filtres par entité/practice
        with st.sidebar.expander("🏢 Entités & Practices", expanded=False):
            # Récupérer les entités et practices disponibles
            available_entities = self._get_available_entities()
            available_practices = self._get_available_practices()
            
            if available_entities:
                selected_entities = st.multiselect(
                    "Entités",
                    options=available_entities,
                    default=available_entities,
                    key=f"dashboard_entities_multiselect_{context}"
                )
                filters['entities'] = selected_entities
            
            if available_practices:
                selected_practices = st.multiselect(
                    "Practices",
                    options=available_practices,
                    default=available_practices,
                    key=f"dashboard_practices_multiselect_{context}"
                )
                filters['practices'] = selected_practices
        
        # Filtres par Business Manager
        with st.sidebar.expander("👔 Business Managers", expanded=False):
            available_bms = self._get_available_business_managers()
            
            if available_bms:
                selected_bms = st.multiselect(
                    "Business Managers",
                    options=available_bms,
                    default=available_bms,
                    key=f"dashboard_bms_multiselect_{context}"
                )
                filters['business_managers'] = selected_bms
        
        # Filtres par statut consultant
        with st.sidebar.expander("👥 Statuts Consultants", expanded=False):
            consultant_statuses = ["Actif", "En mission", "Intercontrat", "Congés"]
            selected_statuses = st.multiselect(
                "Statuts",
                options=consultant_statuses,
                default=consultant_statuses,
                key=f"dashboard_status_multiselect_{context}"
            )
            filters['consultant_statuses'] = selected_statuses
        
        # Filtre par seuils
        with st.sidebar.expander("📊 Seuils & Alertes", expanded=False):
            filters['intercontrat_threshold'] = st.slider(
                "Seuil alerte intercontrat (%)",
                min_value=0, max_value=50, value=15, step=1,
                key=f"dashboard_intercontrat_slider_{context}"
            )
            
            filters['revenue_threshold'] = st.number_input(
                "Seuil minimum revenus (k€)",
                min_value=0, value=500, step=50,
                key=f"dashboard_revenue_number_input_{context}"
            )
        
        return filters
    
    def apply_filters_to_data(self, data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Applique les filtres aux données
        """
        filtered_data = data.copy()
        
        # Filtre temporel
        if 'start_date' in filters and 'end_date' in filters:
            if 'date' in filtered_data.columns:
                filtered_data = filtered_data[
                    (filtered_data['date'] >= filters['start_date']) &
                    (filtered_data['date'] <= filters['end_date'])
                ]
        
        # Filtres entités
        if 'entities' in filters and filters['entities']:
            if 'entite' in filtered_data.columns:
                filtered_data = filtered_data[
                    filtered_data['entite'].isin(filters['entities'])
                ]
        
        # Filtres practices
        if 'practices' in filters and filters['practices']:
            if 'practice' in filtered_data.columns:
                filtered_data = filtered_data[
                    filtered_data['practice'].isin(filters['practices'])
                ]
        
        # Filtres BM
        if 'business_managers' in filters and filters['business_managers']:
            if 'business_manager' in filtered_data.columns:
                filtered_data = filtered_data[
                    filtered_data['business_manager'].isin(filters['business_managers'])
                ]
        
        return filtered_data
    
    def show_export_options(self, dashboard_config: Dict):
        """
        Options d'export du dashboard
        """
        st.sidebar.subheader("📤 Export")
        
        export_format = st.sidebar.selectbox(
            "Format d'export",
            options=["PDF", "Excel", "PNG", "PowerPoint"]
        )
        
        if st.sidebar.button("📥 Exporter le dashboard"):
            self._export_dashboard(dashboard_config, export_format)
    
    def _export_dashboard(self, dashboard_config: Dict, format_type: str):
        """
        Exporte le dashboard dans le format choisi
        """
        try:
            if format_type == "PDF":
                self._export_to_pdf(dashboard_config)
            elif format_type == "Excel":
                self._export_to_excel(dashboard_config)
            elif format_type == "PNG":
                self._export_to_image(dashboard_config)
            elif format_type == "PowerPoint":
                self._export_to_powerpoint(dashboard_config)
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'export: {e}")
    
    def _export_to_pdf(self, dashboard_config: Dict):
        """
        Export PDF du dashboard
        """
        if not HAS_REPORTLAB:
            st.error("❌ ReportLab n'est pas installé. Exécutez: pip install reportlab")
            return
            
        # Créer le PDF
        buffer = io.BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
        
        # En-tête
        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(50, 800, f"Dashboard: {dashboard_config['nom']}")
        
        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(50, 780, f"Généré le: {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        
        # Récupérer les données pour chaque widget
        y_position = 750
        
        for widget in dashboard_config.get('widgets', []):
            widget_data = self._get_widget_export_data(widget)
            
            pdf_canvas.setFont("Helvetica-Bold", 14)
            pdf_canvas.drawString(50, y_position, widget_data['title'])
            y_position -= 30
            
            pdf_canvas.setFont("Helvetica", 10)
            for line in widget_data['summary'][:10]:  # Limiter à 10 lignes
                pdf_canvas.drawString(70, y_position, str(line))
                y_position -= 15
            
            y_position -= 20
            
            if y_position < 100:  # Nouvelle page si nécessaire
                pdf_canvas.showPage()
                y_position = 800
        
        pdf_canvas.save()
        buffer.seek(0)
        
        # Téléchargement
        st.download_button(
            label="📥 Télécharger le PDF",
            data=buffer.getvalue(),
            file_name=f"dashboard_{dashboard_config['nom']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )
    
    def _export_to_excel(self, dashboard_config: Dict):
        """
        Export Excel avec données détaillées
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Onglet sommaire
            summary_data = self._get_dashboard_summary_data(dashboard_config)
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Sommaire', index=False)
            
            # Onglet par widget
            for widget in dashboard_config.get('widgets', []):
                widget_data = self._get_widget_detailed_data(widget)
                if widget_data is not None:
                    sheet_name = widget['widget_type'][:30]  # Limite Excel
                    widget_data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        
        st.download_button(
            label="📥 Télécharger Excel",
            data=output.getvalue(),
            file_name=f"dashboard_{dashboard_config['nom']}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    def _export_to_image(self, dashboard_config: Dict):
        """
        Export PNG du dashboard
        """
        st.info("🔄 Export PNG - Fonctionnalité en cours de développement")
        # Cette fonctionnalité nécessiterait une capture d'écran
        # ou la génération d'images des graphiques Plotly
    
    def _export_to_powerpoint(self, dashboard_config: Dict):
        """
        Export PowerPoint
        """
        st.info("🔄 Export PowerPoint - Fonctionnalité en cours de développement")
        # Cette fonctionnalité nécessiterait python-pptx
    
    def show_alerts_panel(self, filters: Dict[str, Any]):
        """
        Panneau d'alertes et notifications
        """
        st.sidebar.subheader("🚨 Alertes")
        
        alerts = self._check_dashboard_alerts(filters)
        
        if not alerts:
            st.sidebar.success("✅ Aucune alerte")
            return
        
        for alert in alerts:
            alert_color = {
                'critical': 'error',
                'warning': 'warning',
                'info': 'info'
            }.get(alert['severity'], 'info')
            
            with st.sidebar.container():
                if alert_color == 'error':
                    st.error(f"🚨 {alert['title']}")
                elif alert_color == 'warning':
                    st.warning(f"⚠️ {alert['title']}")
                else:
                    st.info(f"ℹ️ {alert['title']}")
                
                st.caption(alert['description'])
    
    def _check_dashboard_alerts(self, filters: Dict[str, Any]) -> List[Dict]:
        """
        Vérifie les conditions d'alerte
        """
        alerts = []
        
        # Alerte taux intercontrat
        intercontrat_data = self.data_service.get_intercontrat_data()
        threshold = filters.get('intercontrat_threshold', 15)
        
        if intercontrat_data['taux_intercontrat'] > threshold:
            alerts.append({
                'severity': 'critical',
                'title': f"Taux intercontrat élevé: {intercontrat_data['taux_intercontrat']:.1f}%",
                'description': f"Seuil configuré: {threshold}%. {intercontrat_data['consultants_intercontrat']} consultants concernés."
            })
        
        # Alerte revenus
        revenue_data = self.data_service.get_revenue_by_bm_data()
        revenue_threshold = filters.get('revenue_threshold', 500) * 1000
        
        low_revenue_bms = [
            bm for bm in revenue_data.get('bm_revenues', [])
            if bm['ca_estime'] < revenue_threshold
        ]
        
        if low_revenue_bms:
            alerts.append({
                'severity': 'warning',
                'title': f"{len(low_revenue_bms)} BM(s) sous le seuil",
                'description': f"Revenus inférieurs à {revenue_threshold/1000:.0f}k€"
            })
        
        # Alerte missions récentes
        recent_missions = self._check_recent_mission_activity()
        if recent_missions['low_activity']:
            alerts.append({
                'severity': 'info',
                'title': "Activité missions ralentie",
                'description': f"Seulement {recent_missions['count']} nouvelles missions cette semaine"
            })
        
        return alerts
    
    def show_ai_insights(self, dashboard_config: Dict, filters: Dict[str, Any]):
        """
        Insights IA basés sur les données du dashboard
        """
        st.sidebar.subheader("🤖 Insights IA")
        
        if st.sidebar.button("🔮 Générer des insights"):
            with st.sidebar.spinner("Analyse en cours..."):
                insights = self._generate_ai_insights(dashboard_config, filters)
                
                for insight in insights:
                    with st.sidebar.expander(f"💡 {insight['title']}", expanded=False):
                        st.write(insight['description'])
                        
                        if insight.get('recommendation'):
                            st.info(f"💡 **Recommandation:** {insight['recommendation']}")
    
    def _generate_ai_insights(self, dashboard_config: Dict, filters: Dict[str, Any]) -> List[Dict]:
        """
        Génère des insights IA (simulation)
        """
        insights = []
        
        # Analyse du taux d'intercontrat
        intercontrat_data = self.data_service.get_intercontrat_data()
        
        if intercontrat_data['taux_intercontrat'] > 20:
            insights.append({
                'title': "Taux d'intercontrat préoccupant",
                'description': f"Le taux d'intercontrat actuel de {intercontrat_data['taux_intercontrat']:.1f}% est supérieur à la moyenne du secteur (15%).",
                'recommendation': "Intensifier la prospection commerciale et analyser les compétences disponibles pour mieux positionner les consultants."
            })
        
        # Analyse des revenus
        revenue_data = self.data_service.get_revenue_by_bm_data()
        bm_revenues = revenue_data.get('bm_revenues', [])
        avg_revenue = sum(bm['ca_estime'] for bm in bm_revenues) / len(bm_revenues) if bm_revenues else 0
        
        top_performer = max(bm_revenues, key=lambda x: x['ca_estime']) if bm_revenues else None
        bottom_performer = min(bm_revenues, key=lambda x: x['ca_estime']) if bm_revenues else None
        
        if top_performer and bottom_performer:
            ratio = top_performer['ca_estime'] / bottom_performer['ca_estime'] if bottom_performer['ca_estime'] > 0 else 0
            
            if ratio > 3:
                insights.append({
                    'title': "Disparité importante entre BM",
                    'description': f"Écart de {ratio:.1f}x entre le meilleur ({top_performer['bm_name']}: {top_performer['ca_estime']/1000:.0f}k€) et le moins performant BM.",
                    'recommendation': "Organiser des sessions de partage de bonnes pratiques et analyser les stratégies des top performers."
                })
        
        # Analyse temporelle
        trend_data = self._get_trend_analysis(filters)
        if trend_data['declining']:
            insights.append({
                'title': "Tendance à la baisse détectée",
                'description': "Les métriques montrent une tendance négative sur la période sélectionnée.",
                'recommendation': "Analyser les causes de cette baisse et mettre en place un plan d'action correctif."
            })
        
        # Insights par practice
        practice_insights = self._analyze_practice_performance()
        insights.extend(practice_insights)
        
        return insights[:5]  # Limiter à 5 insights
    
    def show_comparative_analysis(self):
        """
        Analyse comparative multi-périodes
        """
        st.subheader("📈 Analyse Comparative")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Période de référence", ["Même période année précédente", "Période précédente"], key="dashboard_comparison_period_selectbox")
        
        with col2:
            comparison_type = st.selectbox("Type de comparaison", ["Évolution %", "Différence absolue", "Les deux"], key="dashboard_comparison_type_selectbox")
        
        # Tableau comparatif
        comparison_data = self._get_comparison_data()
        
        if comparison_data is not None and not comparison_data.empty:
            st.dataframe(
                comparison_data,
                use_container_width=True,
                column_config={
                    "evolution": st.column_config.NumberColumn(
                        "Évolution",
                        format="%.1f%%"
                    )
                }
            )
    
    def show_forecasting(self):
        """
        Prévisions basées sur les données historiques
        """
        st.subheader("🔮 Prévisions")
        
        forecast_type = st.selectbox(
            "Métrique à prévoir",
            ["Taux d'intercontrat", "Revenus globaux", "Nombre de missions"],
            key="dashboard_forecast_type_selectbox"
        )
        
        forecast_period = st.slider("Horizon de prévision (mois)", 1, 12, 3, key="dashboard_forecast_period_slider")
        
        if st.button("📊 Générer la prévision"):
            forecast_data = self._generate_forecast(forecast_type, forecast_period)
            
            # Graphique de prévision
            fig = go.Figure()
            
            # Données historiques
            fig.add_trace(go.Scatter(
                x=forecast_data['historical']['dates'],
                y=forecast_data['historical']['values'],
                mode='lines+markers',
                name='Données historiques',
                line=dict(color='blue')
            ))
            
            # Prévisions
            fig.add_trace(go.Scatter(
                x=forecast_data['forecast']['dates'],
                y=forecast_data['forecast']['values'],
                mode='lines+markers',
                name='Prévision',
                line=dict(color='red', dash='dash')
            ))
            
            # Zone de confiance
            fig.add_trace(go.Scatter(
                x=forecast_data['forecast']['dates'] + forecast_data['forecast']['dates'][::-1],
                y=forecast_data['forecast']['upper'] + forecast_data['forecast']['lower'][::-1],
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Zone de confiance 95%'
            ))
            
            fig.update_layout(
                title=f"Prévision: {forecast_type}",
                xaxis_title="Date",
                yaxis_title=forecast_type,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Résumé de la prévision
            st.info(f"📊 **Prévision à {forecast_period} mois:** {forecast_data['summary']}")
    
    # Méthodes utilitaires pour récupérer les données
    
    def _get_available_entities(self) -> List[str]:
        """Récupère les entités disponibles"""
        try:
            with get_database_session() as session:
                entities = session.query(Consultant.entite).distinct().all()
                return [e[0] for e in entities if e[0]]
        except:
            return ["Quanteam", "Autre"]
    
    def _get_available_practices(self) -> List[str]:
        """Récupère les practices disponibles"""
        try:
            with get_database_session() as session:
                # Adapter selon votre modèle
                practices = ["Data & Analytics", "Cloud & DevOps", "Cybersécurité", "Digital"]
                return practices
        except:
            return []
    
    def _get_available_business_managers(self) -> List[str]:
        """Récupère les BM disponibles"""
        try:
            with get_database_session() as session:
                bms = session.query(Consultant.business_manager).distinct().all()
                return [bm[0] for bm in bms if bm[0]]
        except:
            return []
    
    def _get_widget_export_data(self, widget: Dict) -> Dict:
        """Récupère les données d'export pour un widget"""
        return {
            'title': widget['widget_type'],
            'summary': ['Données du widget...', 'Ligne 2', 'Ligne 3']
        }
    
    def _get_widget_detailed_data(self, widget: Dict) -> Optional[pd.DataFrame]:
        """Récupère les données détaillées pour export Excel"""
        return pd.DataFrame({'colonne1': [1, 2, 3], 'colonne2': ['A', 'B', 'C']})
    
    def _get_dashboard_summary_data(self, dashboard_config: Dict) -> List[Dict]:
        """Récupère les données de sommaire du dashboard"""
        return [
            {'Métrique': 'Nombre de widgets', 'Valeur': len(dashboard_config.get('widgets', []))},
            {'Métrique': 'Date de création', 'Valeur': dashboard_config.get('date_creation', 'N/A')}
        ]
    
    def _check_recent_mission_activity(self) -> Dict:
        """Vérifie l'activité récente des missions"""
        return {'low_activity': False, 'count': 5}
    
    def _get_trend_analysis(self, filters: Dict) -> Dict:
        """Analyse les tendances"""
        return {'declining': False}
    
    def _analyze_practice_performance(self) -> List[Dict]:
        """Analyse la performance par practice"""
        return []
    
    def _get_comparison_data(self) -> Optional[pd.DataFrame]:
        """Récupère les données de comparaison"""
        return pd.DataFrame({
            'Métrique': ['Revenus', 'Taux intercontrat', 'Nb missions'],
            'Actuel': [1000, 15.5, 45],
            'Précédent': [950, 12.3, 42],
            'evolution': [5.3, 26.0, 7.1]
        })
    
    def _generate_forecast(self, forecast_type: str, period_months: int) -> Dict:
        """Génère des prévisions (simulation)"""
        from datetime import datetime, timedelta
        import random
        
        # Données historiques simulées
        historical_dates = [datetime.now() - timedelta(days=30*i) for i in range(12, 0, -1)]
        historical_values = [random.randint(50, 100) for _ in range(12)]
        
        # Prévisions simulées
        forecast_dates = [datetime.now() + timedelta(days=30*i) for i in range(1, period_months+1)]
        forecast_values = [random.randint(45, 95) for _ in range(period_months)]
        
        return {
            'historical': {
                'dates': historical_dates,
                'values': historical_values
            },
            'forecast': {
                'dates': forecast_dates,
                'values': forecast_values,
                'upper': [v + 10 for v in forecast_values],
                'lower': [v - 10 for v in forecast_values]
            },
            'summary': f"Tendance stable avec une moyenne de {sum(forecast_values)/len(forecast_values):.1f}"
        }


# Instance globale des fonctionnalités avancées
advanced_features = AdvancedDashboardFeatures()