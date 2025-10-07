"""Tests Phase 46: widget_factory.py (51% → 52%)"""
import unittest
from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestWidgetFactory(unittest.TestCase):
    @patch("app.services.widget_factory.st")
    def test_render_widget_unknown_type(self, mock_st):
        from app.services.widget_factory import WidgetFactory
        
        # Widget type inconnu - test ne devrait pas crasher
        WidgetFactory.render_widget("unknown_widget_type", {})
        # Si arrive ici, pas de crash = succès

if __name__ == "__main__":
    unittest.main()
