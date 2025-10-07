"""Tests Phase 42: dashboard_page.py (11% → 15%+)"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestCollectWidgetSelections(unittest.TestCase):
    @patch("app.pages_modules.dashboard_page.st")
    @patch("app.pages_modules.dashboard_page.WidgetFactory")
    def test_collect_widget_selections_empty(self, mock_factory, mock_st):
        from app.pages_modules.dashboard_page import _collect_widget_selections
        
        # Mock no widgets
        mock_factory.get_widgets_by_category.return_value = {}
        
        result = _collect_widget_selections()
        
        self.assertIsInstance(result, list)

class TestIsWidgetAvailable(unittest.TestCase):
    def test_is_widget_available_true(self):
        from app.pages_modules.dashboard_page import _is_widget_available
        
        widget = {"id": "w1", "name": "Widget 1"}
        current_widgets = []
        
        result = _is_widget_available(widget, current_widgets)
        
        self.assertTrue(result)

class TestAddSelectedWidgetsToDashboard(unittest.TestCase):
    @patch("app.pages_modules.dashboard_page.DashboardService")
    def test_add_selected_widgets(self, mock_service):
        from app.pages_modules.dashboard_page import _add_selected_widgets_to_dashboard
        
        dashboard_id = 1
        selected_widgets = ["widget1", "widget2"]
        
        _add_selected_widgets_to_dashboard(dashboard_id, selected_widgets)
        
        # Vérifie que add_widget a été appelé
        self.assertEqual(mock_service.add_widget_to_dashboard.call_count, 2)

class TestProcessWidgetAddition(unittest.TestCase):
    @patch("app.pages_modules.dashboard_page.st")
    @patch("app.pages_modules.dashboard_page.DashboardService")
    def test_process_widget_addition_success(self, mock_service, mock_st):
        from app.pages_modules.dashboard_page import _process_widget_addition
        
        dashboard_config = {"id": 1, "nom": "Dashboard"}
        new_widgets = ["widget1"]
        
        try:
            _process_widget_addition(dashboard_config, new_widgets)
            # Si pas d'exception, le test passe
        except Exception as e:
            self.fail(f"_process_widget_addition a levé une exception: {e}")

class TestRenderDeleteButton(unittest.TestCase):
    @patch("app.pages_modules.dashboard_page.st")
    def test_render_delete_button(self, mock_st):
        from app.pages_modules.dashboard_page import _render_delete_button
        
        widget = {"id": 1, "widget_type": "metric"}
        mock_st.button.return_value = False
        
        _render_delete_button(widget)
        
        # Vérifie que button a été appelé
        mock_st.button.assert_called()

if __name__ == "__main__":
    unittest.main()
