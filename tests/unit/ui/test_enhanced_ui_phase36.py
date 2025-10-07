"""Tests Phase 36: enhanced_ui.py (mode accéléré)"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestCreateMetricCard(unittest.TestCase):
    @patch("app.ui.enhanced_ui.st")
    def test_create_metric_card_basic(self, mock_st):
        from app.ui.enhanced_ui import create_metric_card
        create_metric_card("Test", 100)
        mock_st.metric.assert_called_once()
    
    @patch("app.ui.enhanced_ui.st")
    def test_create_metric_card_with_delta(self, mock_st):
        from app.ui.enhanced_ui import create_metric_card
        create_metric_card("Test", 100, delta=10)
        mock_st.metric.assert_called_once()

class TestCreateInfoCard(unittest.TestCase):
    @patch("app.ui.enhanced_ui.st")
    def test_create_info_card_basic(self, mock_st):
        from app.ui.enhanced_ui import create_info_card
        create_info_card("Title", "Content")
        mock_st.markdown.assert_called()

class TestDisplayConsultantCard(unittest.TestCase):
    @patch("app.ui.enhanced_ui.st")
    def test_display_consultant_card(self, mock_st):
        from app.ui.enhanced_ui import display_consultant_card
        c = Mock(prenom="Jean", nom="Dupont", email="jean@test.com", practice=Mock(nom="Data"))
        # Mock columns as context managers
        col1 = MagicMock()
        col2 = MagicMock()
        col1.__enter__ = Mock(return_value=col1)
        col1.__exit__ = Mock(return_value=None)
        col2.__enter__ = Mock(return_value=col2)
        col2.__exit__ = Mock(return_value=None)
        mock_st.columns.return_value = [col1, col2]
        display_consultant_card(c)
        mock_st.markdown.assert_called()

if __name__ == "__main__":
    unittest.main()
