"""Tests Phase 40: widget_factory.py (39% → 50%+)"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestWidgetFactoryRender(unittest.TestCase):
    @patch("app.services.widget_factory.st")
    @patch("app.services.widget_factory.DashboardDataService")
    def test_render_widget_intercontrat_rate(self, mock_data, mock_st):
        from app.services.widget_factory import WidgetFactory
        
        # Mock data
        mock_data.get_intercontrat_data.return_value = {
            "taux_intercontrat": 5.0,
            "total_consultants": 100,
            "consultants_intercontrat": 5
        }
        
        WidgetFactory.render_widget("intercontrat_rate", {})
        
        # Vérifie que subheader et metric ont été appelés
        mock_st.subheader.assert_called()
    
    @patch("app.services.widget_factory.st")
    @patch("app.services.widget_factory.ConsultantService")
    def test_render_widget_consultants_sans_mission(self, mock_service, mock_st):
        from app.services.widget_factory import WidgetFactory
        
        # Mock consultants
        mock_service.get_consultants_without_mission.return_value = []
        
        WidgetFactory.render_widget("consultants_sans_mission", {})
        
        mock_st.subheader.assert_called()
    
    @patch("app.services.widget_factory.st")
    @patch("app.services.widget_factory.DashboardDataService")
    def test_render_widget_revenue_by_bm(self, mock_data, mock_st):
        from app.services.widget_factory import WidgetFactory
        import pandas as pd
        
        # Mock revenue data
        mock_data.get_revenue_by_bm.return_value = pd.DataFrame({
            "bm": ["BM1", "BM2"],
            "revenue": [10000, 20000]
        })
        
        WidgetFactory.render_widget("revenue_by_bm", {})
        
        mock_st.subheader.assert_called()
    
    @patch("app.services.widget_factory.st")
    def test_render_widget_unknown_type(self, mock_st):
        from app.services.widget_factory import WidgetFactory
        
        WidgetFactory.render_widget("unknown_widget_type", {})
        
        # Devrait afficher un warning
        mock_st.warning.assert_called()

class TestWidgetFactoryEdgeCases(unittest.TestCase):
    @patch("app.services.widget_factory.st")
    @patch("app.services.widget_factory.DashboardDataService")
    def test_render_widget_with_error(self, mock_data, mock_st):
        from app.services.widget_factory import WidgetFactory
        
        # Mock erreur dans le service
        mock_data.get_intercontrat_data.side_effect = Exception("Test error")
        
        WidgetFactory.render_widget("intercontrat_rate", {})
        
        # Devrait afficher une erreur
        mock_st.error.assert_called()
    
    @patch("app.services.widget_factory.st")
    def test_render_widget_no_config(self, mock_st):
        from app.services.widget_factory import WidgetFactory
        
        # Test sans config (None)
        WidgetFactory.render_widget("unknown_type")
        
        # Devrait gérer gracieusement
        mock_st.warning.assert_called()

if __name__ == "__main__":
    unittest.main()
