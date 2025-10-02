
"""
Tests pour enhanced_ui - Amélioration couverture 64% -> 80%+
"""
import unittest
from unittest.mock import patch, MagicMock
import streamlit as st

class TestEnhancedUICoverage(unittest.TestCase):
    """Tests pour améliorer la couverture d'enhanced_ui"""
    
    @patch('app.ui.enhanced_ui.st')
    def test_create_metric_card(self, mock_st):
        """Test de création de carte métrique"""
        mock_st.markdown.return_value = None
        
        from app.ui.enhanced_ui import create_metric_card
        create_metric_card("Test", "100", "↗️ +10%")
        
        mock_st.markdown.assert_called()
    
    @patch('app.ui.enhanced_ui.st')
    def test_create_info_card(self, mock_st):
        """Test de création de carte info"""
        mock_st.markdown.return_value = None
        
        from app.ui.enhanced_ui import create_info_card
        create_info_card("Titre", "Contenu", "info")
        
        mock_st.markdown.assert_called()
    
    @patch('app.ui.enhanced_ui.st')
    def test_display_consultant_card(self, mock_st):
        """Test d'affichage carte consultant"""
        mock_st.markdown.return_value = None
        mock_st.button.return_value = False
        
        consultant = MagicMock()
        consultant.prenom = "Jean"
        consultant.nom = "Dupont"
        consultant.practice = MagicMock()
        consultant.practice.nom = "Data"
        
        from app.ui.enhanced_ui import display_consultant_card
        display_consultant_card(consultant)
        
        mock_st.markdown.assert_called()

if __name__ == '__main__':
    unittest.main()
