"""
Tests unitaires pour widget_factory.py (Phase 50 - Couverture 80%)
Objectif: Tester WidgetFactory et WidgetCatalogManager
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
import pandas as pd

from app.services.widget_factory import WidgetFactory, WidgetCatalogManager


class TestWidgetFactoryRenderWidget:
    """Tests pour la méthode render_widget"""

    @patch("app.services.widget_factory.WidgetFactory._render_intercontrat_rate")
    def test_render_widget_intercontrat_rate(self, mock_render):
        """Test rendu du widget intercontrat_rate"""
        config = {"bm_filter": 1}
        WidgetFactory.render_widget("intercontrat_rate", config)
        
        mock_render.assert_called_once_with(config)

    @patch("app.services.widget_factory.WidgetFactory._render_consultants_sans_mission")
    def test_render_widget_consultants_sans_mission(self, mock_render):
        """Test rendu du widget consultants_sans_mission"""
        config = {"bm_filter": 2}
        WidgetFactory.render_widget("consultants_sans_mission", config)
        
        mock_render.assert_called_once_with(config)

    @patch("app.services.widget_factory.WidgetFactory._render_revenue_by_bm")
    def test_render_widget_revenue_by_bm(self, mock_render):
        """Test rendu du widget revenue_by_bm"""
        config = {"period_months": 3}
        WidgetFactory.render_widget("revenue_by_bm", config)
        
        mock_render.assert_called_once_with(config)

    @patch("app.services.widget_factory.WidgetFactory._render_global_kpis")
    def test_render_widget_global_kpis(self, mock_render):
        """Test rendu du widget global_kpis"""
        WidgetFactory.render_widget("global_kpis", {})
        
        mock_render.assert_called_once_with({})

    @patch("app.services.widget_factory.WidgetFactory._render_intercontrat_trend")
    def test_render_widget_intercontrat_trend(self, mock_render):
        """Test rendu du widget intercontrat_trend"""
        WidgetFactory.render_widget("intercontrat_trend")
        
        mock_render.assert_called_once()

    @patch("app.services.widget_factory.WidgetFactory._render_top_bm_performance")
    def test_render_widget_top_bm_performance(self, mock_render):
        """Test rendu du widget top_bm_performance"""
        config = {"period_months": 6}
        WidgetFactory.render_widget("top_bm_performance", config)
        
        mock_render.assert_called_once_with(config)

    @patch("streamlit.warning")
    def test_render_widget_unknown_type(self, mock_warning):
        """Test widget type inconnu"""
        WidgetFactory.render_widget("unknown_widget_type", {})
        
        mock_warning.assert_called_once_with("⚠️ Widget type 'unknown_widget_type' non reconnu")

    @patch("streamlit.error")
    @patch("app.services.widget_factory.WidgetFactory._render_intercontrat_rate")
    def test_render_widget_exception_handling(self, mock_render, mock_error):
        """Test gestion d'exception lors du rendu"""
        mock_render.side_effect = Exception("Test error")
        
        WidgetFactory.render_widget("intercontrat_rate", {})
        
        mock_error.assert_called_once()
        assert "Test error" in str(mock_error.call_args[0][0])

    def test_render_widget_config_none_default(self):
        """Test config None transformé en dict vide"""
        with patch("app.services.widget_factory.WidgetFactory._render_global_kpis") as mock_render:
            WidgetFactory.render_widget("global_kpis", None)
            
            mock_render.assert_called_once_with({})


class TestRenderIntercontratRate:
    """Tests pour _render_intercontrat_rate"""

    @patch("streamlit.plotly_chart")
    @patch("streamlit.markdown")
    @patch("streamlit.write")
    @patch("streamlit.metric")
    @patch("streamlit.columns")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_intercontrat_rate_critical(self, mock_data, mock_subheader, mock_cols, 
                                               mock_metric, mock_write, mock_markdown, mock_chart):
        """Test widget avec taux critique (>15%)"""
        mock_data.return_value = {
            "taux_intercontrat": 18.5,
            "total_consultants": 100,
            "consultants_intercontrat": 18,
            "consultants_sans_mission": []
        }
        
        col1, col2, col3 = Mock(), Mock(), Mock()
        col1.__enter__ = Mock(return_value=col1)
        col1.__exit__ = Mock(return_value=False)
        col2.__enter__ = Mock(return_value=col2)
        col2.__exit__ = Mock(return_value=False)
        col3.__enter__ = Mock(return_value=col3)
        col3.__exit__ = Mock(return_value=False)
        mock_cols.return_value = [col1, col2, col3]
        
        WidgetFactory._render_intercontrat_rate({"bm_filter": 1})
        
        mock_data.assert_called_once_with(1)
        mock_subheader.assert_called_once_with("⏰ Taux d'Intercontrat")
        assert mock_markdown.called
        # Vérifier couleur rouge dans le HTML
        html_call = mock_markdown.call_args[0][0]
        assert "red" in html_call

    @patch("streamlit.markdown")
    @patch("streamlit.write")
    @patch("streamlit.metric")
    @patch("streamlit.columns")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_intercontrat_rate_warning(self, mock_data, mock_subheader, mock_cols,
                                              mock_metric, mock_write, mock_markdown):
        """Test widget avec taux attention (>10% et <=15%)"""
        mock_data.return_value = {
            "taux_intercontrat": 12.0,
            "total_consultants": 50,
            "consultants_intercontrat": 6,
            "consultants_sans_mission": []
        }
        
        col1, col2, col3 = Mock(), Mock(), Mock()
        for col in [col1, col2, col3]:
            col.__enter__ = Mock(return_value=col)
            col.__exit__ = Mock(return_value=False)
        mock_cols.return_value = [col1, col2, col3]
        
        WidgetFactory._render_intercontrat_rate({})
        
        html_call = mock_markdown.call_args[0][0]
        assert "orange" in html_call

    @patch("streamlit.markdown")
    @patch("streamlit.write")
    @patch("streamlit.metric")
    @patch("streamlit.columns")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_intercontrat_rate_normal(self, mock_data, mock_subheader, mock_cols,
                                             mock_metric, mock_write, mock_markdown):
        """Test widget avec taux normal (<=10%)"""
        mock_data.return_value = {
            "taux_intercontrat": 5.0,
            "total_consultants": 80,
            "consultants_intercontrat": 4,
            "consultants_sans_mission": []
        }
        
        col_mocks = [Mock(), Mock(), Mock()]
        mock_cols.return_value = col_mocks
        
        WidgetFactory._render_intercontrat_rate({})
        
        html_call = mock_markdown.call_args[0][0]
        assert "green" in html_call

    @patch("streamlit.markdown")
    @patch("streamlit.write")
    @patch("streamlit.metric")
    @patch("streamlit.columns")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_intercontrat_rate_zero(self, mock_data, mock_subheader, mock_cols,
                                           mock_metric, mock_write, mock_markdown):
        """Test widget avec taux à 0% (pas de HTML)"""
        mock_data.return_value = {
            "taux_intercontrat": 0.0,
            "total_consultants": 50,
            "consultants_intercontrat": 0,
            "consultants_sans_mission": []
        }
        
        col_mocks = [Mock(), Mock(), Mock()]
        mock_cols.return_value = col_mocks
        
        WidgetFactory._render_intercontrat_rate({})
        
        # Pas de HTML si taux = 0
        assert not mock_markdown.called


class TestRenderConsultantsSansMission:
    """Tests pour _render_consultants_sans_mission"""

    @patch("streamlit.success")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_consultants_sans_mission_empty(self, mock_data, mock_subheader, mock_success):
        """Test sans consultants en intercontrat"""
        mock_data.return_value = {
            "consultants_sans_mission": [],
            "taux_intercontrat": 0.0,
            "total_consultants": 50,
            "consultants_intercontrat": 0
        }
        
        WidgetFactory._render_consultants_sans_mission({})
        
        mock_success.assert_called_once_with("🎉 Aucun consultant en intercontrat !")

    @patch("streamlit.caption")
    @patch("streamlit.dataframe")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_consultants_sans_mission_with_data(self, mock_data, mock_subheader, 
                                                        mock_dataframe, mock_caption):
        """Test avec consultants en intercontrat"""
        mock_data.return_value = {
            "consultants_sans_mission": [
                {"nom": "Dupont Jean", "email": "jean@test.com", "derniere_mission": "2024-01-01"},
                {"nom": "Martin Marie", "email": "marie@test.com", "derniere_mission": "2024-02-15"}
            ],
            "taux_intercontrat": 4.0,
            "total_consultants": 50,
            "consultants_intercontrat": 2
        }
        
        WidgetFactory._render_consultants_sans_mission({"bm_filter": 3})
        
        mock_data.assert_called_once_with(3)
        mock_dataframe.assert_called_once()
        mock_caption.assert_called_once()
        # Vérifier le caption
        caption_text = mock_caption.call_args[0][0]
        assert "2" in caption_text


class TestRenderRevenueByBm:
    """Tests pour _render_revenue_by_bm"""

    @patch("streamlit.info")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_revenue_by_bm_data")
    def test_render_revenue_by_bm_no_data(self, mock_data, mock_subheader, mock_info):
        """Test sans données de revenus"""
        mock_data.return_value = {"bm_revenues": []}
        
        WidgetFactory._render_revenue_by_bm({"period_months": 3})
        
        mock_info.assert_called_once_with("📊 Aucune donnée de revenus disponible")

    @patch("streamlit.metric")
    @patch("streamlit.columns")
    @patch("streamlit.plotly_chart")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_revenue_by_bm_data")
    def test_render_revenue_by_bm_with_data(self, mock_data, mock_subheader, mock_chart,
                                            mock_cols, mock_metric):
        """Test avec données de revenus"""
        mock_data.return_value = {
            "bm_revenues": [
                {"bm_name": "BM 1", "ca_estime": 50000, "tjm_moyen": 500, "missions_count": 5},
                {"bm_name": "BM 2", "ca_estime": 30000, "tjm_moyen": 450, "missions_count": 3}
            ]
        }
        
        col_mocks = [Mock(), Mock(), Mock()]
        mock_cols.return_value = col_mocks
        
        WidgetFactory._render_revenue_by_bm({"period_months": 6})
        
        mock_data.assert_called_once_with(6)
        mock_chart.assert_called_once()
        assert mock_metric.call_count == 3

    @patch("streamlit.metric")
    @patch("streamlit.columns")
    @patch("streamlit.plotly_chart")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_revenue_by_bm_data")
    def test_render_revenue_by_bm_default_period(self, mock_data, mock_subheader, mock_chart,
                                                  mock_cols, mock_metric):
        """Test avec période par défaut (3 mois)"""
        mock_data.return_value = {
            "bm_revenues": [
                {"bm_name": "BM 1", "ca_estime": 10000, "tjm_moyen": 400, "missions_count": 1}
            ]
        }
        
        col_mocks = [Mock(), Mock(), Mock()]
        mock_cols.return_value = col_mocks
        
        WidgetFactory._render_revenue_by_bm({})
        
        mock_data.assert_called_once_with(3)


class TestRenderGlobalKpis:
    """Tests pour _render_global_kpis"""

    @patch("streamlit.metric")
    @patch("streamlit.columns")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_revenue_by_bm_data")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_global_kpis_normal(self, mock_intercontrat, mock_revenue, mock_subheader,
                                       mock_cols, mock_metric):
        """Test rendu des KPIs globaux"""
        mock_intercontrat.return_value = {
            "total_consultants": 100,
            "taux_intercontrat": 8.0,
            "consultants_intercontrat": 8,
            "consultants_sans_mission": []
        }
        
        mock_revenue.return_value = {
            "bm_revenues": [
                {"ca_estime": 25000, "missions_count": 5},
                {"ca_estime": 15000, "missions_count": 3}
            ]
        }
        
        col_mocks = [Mock(), Mock(), Mock(), Mock()]
        mock_cols.return_value = col_mocks
        
        WidgetFactory._render_global_kpis({})
        
        mock_intercontrat.assert_called_once()
        mock_revenue.assert_called_once_with(1)
        assert mock_metric.call_count == 4


class TestRenderIntercontratTrend:
    """Tests pour _render_intercontrat_trend"""

    @patch("streamlit.plotly_chart")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_intercontrat_trend(self, mock_data, mock_subheader, mock_chart):
        """Test rendu de la tendance intercontrat"""
        mock_data.return_value = {
            "taux_intercontrat": 10.5,
            "total_consultants": 50,
            "consultants_intercontrat": 5,
            "consultants_sans_mission": []
        }
        
        WidgetFactory._render_intercontrat_trend({})
        
        mock_data.assert_called_once()
        mock_chart.assert_called_once()


class TestRenderTopBmPerformance:
    """Tests pour _render_top_bm_performance"""

    @patch("streamlit.info")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_revenue_by_bm_data")
    def test_render_top_bm_no_data(self, mock_data, mock_subheader, mock_info):
        """Test sans données"""
        mock_data.return_value = {"bm_revenues": []}
        
        WidgetFactory._render_top_bm_performance({"period_months": 3})
        
        mock_info.assert_called_once_with("📊 Aucune donnée disponible")

    @patch("streamlit.divider")
    @patch("streamlit.write")
    @patch("streamlit.columns")
    @patch("streamlit.container")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_revenue_by_bm_data")
    def test_render_top_bm_with_podium(self, mock_data, mock_subheader, mock_container,
                                       mock_cols, mock_write, mock_divider):
        """Test avec top 3 (podium complet)"""
        mock_data.return_value = {
            "bm_revenues": [
                {"bm_name": "BM 1", "ca_estime": 100000, "missions_count": 10},
                {"bm_name": "BM 2", "ca_estime": 80000, "missions_count": 8},
                {"bm_name": "BM 3", "ca_estime": 60000, "missions_count": 6},
                {"bm_name": "BM 4", "ca_estime": 40000, "missions_count": 4}
            ]
        }
        
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock()
        col_mocks = [Mock(), Mock(), Mock(), Mock()]
        mock_cols.return_value = col_mocks
        
        WidgetFactory._render_top_bm_performance({})
        
        # Vérifier que les 4 BM sont affichés (limité à top 5)
        assert mock_container.call_count == 4

    @patch("streamlit.write")
    @patch("streamlit.columns")
    @patch("streamlit.container")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_revenue_by_bm_data")
    def test_render_top_bm_more_than_five(self, mock_data, mock_subheader, mock_container,
                                          mock_cols, mock_write):
        """Test avec plus de 5 BM (seulement top 5 affichés)"""
        mock_data.return_value = {
            "bm_revenues": [
                {"bm_name": f"BM {i}", "ca_estime": 10000 * (10 - i), "missions_count": 10 - i}
                for i in range(10)
            ]
        }
        
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock()
        col_mocks = [Mock(), Mock(), Mock(), Mock()]
        mock_cols.return_value = col_mocks
        
        WidgetFactory._render_top_bm_performance({"period_months": 12})
        
        # Seulement top 5 affichés
        assert mock_container.call_count == 5


class TestWidgetCatalogManager:
    """Tests pour WidgetCatalogManager"""

    @patch("app.services.widget_factory.get_database_session")
    def test_initialize_widget_catalog_success(self, mock_session):
        """Test initialisation réussie du catalogue"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with patch("builtins.print") as mock_print:
            WidgetCatalogManager.initialize_widget_catalog()
            
            # Vérifier que commit a été appelé
            mock_db.commit.assert_called_once()
            # Vérifier message de succès
            mock_print.assert_called_once()
            assert "✅" in str(mock_print.call_args[0][0])

    @patch("app.services.widget_factory.get_database_session")
    def test_initialize_widget_catalog_existing_widgets(self, mock_session):
        """Test avec widgets existants (pas de duplication)"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Simuler qu'un widget existe déjà
        mock_db.query.return_value.filter.return_value.first.return_value = Mock()
        
        WidgetCatalogManager.initialize_widget_catalog()
        
        # Vérifier qu'aucun add n'a été fait (widgets existants)
        assert mock_db.add.call_count == 0

    @patch("app.services.widget_factory.get_database_session")
    def test_initialize_widget_catalog_error(self, mock_session):
        """Test gestion d'erreur lors de l'initialisation"""
        mock_session.return_value.__enter__.side_effect = Exception("DB Error")
        
        with patch("builtins.print") as mock_print:
            WidgetCatalogManager.initialize_widget_catalog()
            
            # Vérifier message d'erreur
            error_call = str(mock_print.call_args[0][0])
            assert "❌" in error_call
            assert "DB Error" in error_call

    @patch("app.services.widget_factory.DashboardService.get_available_widgets")
    def test_get_widgets_by_category(self, mock_get_widgets):
        """Test récupération des widgets par catégorie"""
        mock_get_widgets.return_value = [
            {"name": "widget1", "category": "intercontrat"},
            {"name": "widget2", "category": "financial"},
            {"name": "widget3", "category": "intercontrat"},
            {"name": "widget4", "category": "management"}
        ]
        
        result = WidgetCatalogManager.get_widgets_by_category()
        
        assert len(result) == 3  # 3 catégories
        assert len(result["intercontrat"]) == 2
        assert len(result["financial"]) == 1
        assert len(result["management"]) == 1

    @patch("app.services.widget_factory.DashboardService.get_available_widgets")
    def test_get_widgets_by_category_empty(self, mock_get_widgets):
        """Test avec aucun widget"""
        mock_get_widgets.return_value = []
        
        result = WidgetCatalogManager.get_widgets_by_category()
        
        assert result == {}


class TestEdgeCases:
    """Tests de cas limites et d'intégration"""

    @patch("streamlit.error")
    @patch("app.services.widget_factory.WidgetFactory._render_intercontrat_rate")
    def test_widget_exception_with_custom_message(self, mock_render, mock_error):
        """Test exception avec message personnalisé"""
        mock_render.side_effect = ValueError("Invalid BM filter")
        
        WidgetFactory.render_widget("intercontrat_rate", {"bm_filter": -1})
        
        error_msg = mock_error.call_args[0][0]
        assert "intercontrat_rate" in error_msg
        assert "Invalid BM filter" in error_msg

    @patch("streamlit.plotly_chart")
    @patch("streamlit.markdown")
    @patch("streamlit.write")
    @patch("streamlit.metric")
    @patch("streamlit.columns")
    @patch("streamlit.subheader")
    @patch("app.services.widget_factory.DashboardDataService.get_intercontrat_data")
    def test_render_intercontrat_rate_edge_15_percent(self, mock_data, mock_subheader, 
                                                       mock_cols, mock_metric, mock_write, 
                                                       mock_markdown, mock_chart):
        """Test taux exactement à 15% (limite critique)"""
        mock_data.return_value = {
            "taux_intercontrat": 15.0,
            "total_consultants": 100,
            "consultants_intercontrat": 15,
            "consultants_sans_mission": []
        }
        
        col_mocks = [Mock(), Mock(), Mock()]
        mock_cols.return_value = col_mocks
        
        WidgetFactory._render_intercontrat_rate({})
        
        html_call = mock_markdown.call_args[0][0]
        # 15% exactement = critique (orange, pas rouge car pas >15)
        assert "orange" in html_call

    @patch("app.services.widget_factory.get_database_session")
    def test_initialize_catalog_partial_commit(self, mock_session):
        """Test commit avec seulement nouveaux widgets"""
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Premier widget existe, les autres non
        first_call = True
        def mock_first():
            nonlocal first_call
            if first_call:
                first_call = False
                return Mock()  # Widget existe
            return None  # Autres widgets n'existent pas
        
        mock_db.query.return_value.filter.return_value.first.side_effect = mock_first
        
        WidgetCatalogManager.initialize_widget_catalog()
        
        # Commit appelé une fois même si seulement certains widgets sont nouveaux
        assert mock_db.commit.call_count == 1
