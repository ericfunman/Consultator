"""Tests Phase 43: dashboard_builder.py (15% → 17%)"""
import unittest
from unittest.mock import Mock, patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestDashboardBuilderInit(unittest.TestCase):
    def test_dashboard_builder_initialization(self):
        from app.pages_modules.dashboard_builder import DashboardBuilder
        
        builder = DashboardBuilder()
        
        self.assertEqual(builder.grid_width, 12)
        self.assertEqual(builder.grid_height, 20)

class TestDashboardCanvas(unittest.TestCase):
    @patch("app.pages_modules.dashboard_builder.st")
    def test_show_dashboard_canvas_with_none_config(self, mock_st):
        from app.pages_modules.dashboard_builder import DashboardBuilder
        
        builder = DashboardBuilder()
        try:
            builder._show_dashboard_canvas(None)
            # Si pas d'exception, succès
        except Exception as e:
            self.fail(f"_show_dashboard_canvas a levé une exception: {e}")

if __name__ == "__main__":
    unittest.main()
