
"""
Tests supplémentaires pour consultants.py - Amélioration couverture 61% -> 75%+
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import date

class TestConsultantsCoverageBoost(unittest.TestCase):
    """Tests pour améliorer significativement la couverture de consultants.py"""
    
    @patch('app.pages_modules.consultants.st')
    def test_render_availability_field(self, mock_st):
        """Test du champ disponibilité"""
        mock_st.radio.return_value = "Disponible"
        
        from app.pages_modules.consultants import _render_availability_field
        result = _render_availability_field(MagicMock())
        
        self.assertEqual(result, "Disponible")
        mock_st.radio.assert_called_once()
    
    @patch('app.pages_modules.consultants.st')
    def test_render_practice_field(self, mock_st):
        """Test du champ practice"""
        mock_st.selectbox.return_value = 1
        
        from app.pages_modules.consultants import _render_practice_field
        result = _render_practice_field([MagicMock()], None)
        
        self.assertEqual(result, 1)
        mock_st.selectbox.assert_called_once()
    
    @patch('app.pages_modules.consultants.st')
    def test_render_manager_field(self, mock_st):
        """Test du champ manager"""
        mock_st.selectbox.return_value = 1
        
        from app.pages_modules.consultants import _render_manager_field
        result = _render_manager_field([MagicMock()], None)
        
        self.assertEqual(result, 1)
        mock_st.selectbox.assert_called_once()
    
    def test_validate_consultant_data_valid(self):
        """Test de validation avec données valides"""
        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@test.com",
            "telephone": "0123456789"
        }
        
        from app.pages_modules.consultants import _validate_consultant_data
        errors = _validate_consultant_data(data)
        
        self.assertEqual(len(errors), 0)
    
    def test_validate_consultant_data_missing_required(self):
        """Test de validation avec données manquantes"""
        data = {
            "prenom": "",
            "nom": "Dupont",
            "email": "invalid-email",
            "telephone": "123"
        }
        
        from app.pages_modules.consultants import _validate_consultant_data
        errors = _validate_consultant_data(data)
        
        self.assertGreater(len(errors), 0)
    
    def test_format_consultant_display_name(self):
        """Test de formatage du nom d'affichage"""
        consultant = MagicMock()
        consultant.prenom = "Jean"
        consultant.nom = "Dupont"
        
        from app.pages_modules.consultants import _format_consultant_display_name
        result = _format_consultant_display_name(consultant)
        
        self.assertEqual(result, "Jean DUPONT")
    
    def test_calculate_experience_years(self):
        """Test de calcul des années d'expérience"""
        from app.pages_modules.consultants import _calculate_experience_years
        
        # Test avec date d'entrée
        result = _calculate_experience_years(date(2020, 1, 1), None)
        self.assertGreater(result, 3)
        
        # Test avec date de sortie
        result = _calculate_experience_years(date(2020, 1, 1), date(2023, 1, 1))
        self.assertEqual(result, 3)
    
    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_status_active(self, mock_st):
        """Test d'affichage statut consultant actif"""
        mock_st.success.return_value = None
        
        consultant = MagicMock()
        consultant.date_sortie = None
        
        from app.pages_modules.consultants import _display_consultant_status
        _display_consultant_status(consultant)
        
        mock_st.success.assert_called_once()
    
    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_status_inactive(self, mock_st):
        """Test d'affichage statut consultant inactif"""
        mock_st.warning.return_value = None
        
        consultant = MagicMock()
        consultant.date_sortie = date(2023, 12, 31)
        
        from app.pages_modules.consultants import _display_consultant_status
        _display_consultant_status(consultant)
        
        mock_st.warning.assert_called_once()

if __name__ == '__main__':
    unittest.main()
