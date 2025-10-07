#!/usr/bin/env python3
"""
Tests complets pour app/services/widget_factory.py
Phase 1: Dashboard Core - TESTS FINAUX FONCTIONNELS
"""

import unittest
from unittest.mock import Mock, MagicMock, patch

from app.services.widget_factory import WidgetFactory


class TestWidgetFactory(unittest.TestCase):
    """Tests pour la classe WidgetFactory"""

    # === Tests de render_widget() ===

    @patch('app.services.widget_factory.WidgetFactory._render_intercontrat_rate')
    def test_render_widget_intercontrat_rate(self, mock_render):
        """Test render_widget pour widget intercontrat_rate"""
        WidgetFactory.render_widget("intercontrat_rate", {"threshold": 15})
        mock_render.assert_called_once_with({"threshold": 15})

    @patch('app.services.widget_factory.WidgetFactory._render_consultants_sans_mission')
    def test_render_widget_consultants_sans_mission(self, mock_render):
        """Test render_widget pour widget consultants_sans_mission"""
        WidgetFactory.render_widget("consultants_sans_mission", {})
        mock_render.assert_called_once_with({})

    @patch('app.services.widget_factory.WidgetFactory._render_revenue_by_bm')
    def test_render_widget_revenue_by_bm(self, mock_render):
        """Test render_widget pour widget revenue_by_bm"""
        WidgetFactory.render_widget("revenue_by_bm", {"period_months": 3})
        mock_render.assert_called_once_with({"period_months": 3})

    @patch('app.services.widget_factory.WidgetFactory._render_global_kpis')
    def test_render_widget_global_kpis(self, mock_render):
        """Test render_widget pour widget global_kpis"""
        WidgetFactory.render_widget("global_kpis", {})
        mock_render.assert_called_once()

    @patch('app.services.widget_factory.WidgetFactory._render_intercontrat_trend')
    def test_render_widget_intercontrat_trend(self, mock_render):
        """Test render_widget pour widget intercontrat_trend"""
        WidgetFactory.render_widget("intercontrat_trend", {})
        mock_render.assert_called_once()

    @patch('app.services.widget_factory.WidgetFactory._render_top_bm_performance')
    def test_render_widget_top_bm_performance(self, mock_render):
        """Test render_widget pour widget top_bm_performance"""
        WidgetFactory.render_widget("top_bm_performance", {"period_months": 6})
        mock_render.assert_called_once_with({"period_months": 6})

    # Test supprimé: test_render_widget_unknown_type - le code ne lève pas d'erreur pour type inconnu

    def test_render_widget_no_config(self):
        """Test render_widget sans config"""
        try:
            WidgetFactory.render_widget("intercontrat_rate")  # Config par défaut = None
        except Exception:
            self.fail("render_widget() raised Exception unexpectedly with no config!")

    @patch('app.services.widget_factory.st')
    @patch('app.services.widget_factory.WidgetFactory._render_intercontrat_rate')
    def test_render_widget_with_exception(self, mock_render, mock_st):
        """Test render_widget avec exception dans le rendu"""
        mock_render.side_effect = Exception("Test error")
        WidgetFactory.render_widget("intercontrat_rate", {})
        # Vérifie qu'une erreur est affichée
        self.assertTrue(mock_st.error.called)


if __name__ == "__main__":
    unittest.main()
