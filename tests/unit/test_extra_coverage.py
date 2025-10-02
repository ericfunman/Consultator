"""
Tests focused sur les modules à faible couverture pour passer de 76% à 80%+
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import date

class TestConsultantFormsTargeted(unittest.TestCase):
    """Tests ciblés pour consultant_forms (69% -> 80%+)"""
    
    @patch('app.pages_modules.consultant_forms.st')
    def test_create_consultant_form_basic(self, mock_st):
        """Test création formulaire consultant de base"""
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.text_input.return_value = "Test"
        mock_st.selectbox.return_value = "Option"
        mock_st.number_input.return_value = 50000
        mock_st.form_submit_button.return_value = False
        
        from app.pages_modules.consultant_forms import create_consultant_form
        result = create_consultant_form()
        
        self.assertIsNotNone(result)
    
    @patch('app.pages_modules.consultant_forms.st')
    def test_update_consultant_form_basic(self, mock_st):
        """Test formulaire mise à jour consultant"""
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "test@test.com"
        
        mock_st.form.return_value.__enter__ = MagicMock()
        mock_st.form.return_value.__exit__ = MagicMock()
        mock_st.text_input.return_value = "Test"
        mock_st.form_submit_button.return_value = False
        
        from app.pages_modules.consultant_forms import update_consultant_form
        result = update_consultant_form(mock_consultant)
        
        self.assertIsNotNone(result)
    
    def test_validate_form_data_valid(self):
        """Test validation données formulaire valides"""
        data = {
            "prenom": "Jean",
            "nom": "Dupont", 
            "email": "jean.dupont@test.com",
            "telephone": "0123456789"
        }
        
        from app.pages_modules.consultant_forms import validate_form_data
        errors = validate_form_data(data)
        
        self.assertEqual(len(errors), 0)
    
    def test_validate_form_data_errors(self):
        """Test validation avec erreurs"""
        data = {
            "prenom": "",
            "nom": "",
            "email": "invalid-email",
            "telephone": "123"
        }
        
        from app.pages_modules.consultant_forms import validate_form_data
        errors = validate_form_data(data)
        
        self.assertGreater(len(errors), 0)

class TestConsultantLanguagesTargeted(unittest.TestCase):
    """Tests ciblés pour consultant_languages (67% -> 80%+)"""
    
    @patch('app.pages_modules.consultant_languages.st')
    def test_show_consultant_languages_basic(self, mock_st):
        """Test affichage langues consultant de base"""
        mock_st.subheader.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.selectbox.return_value = "Français"
        mock_st.button.return_value = False
        
        consultant = MagicMock()
        consultant.id = 1
        
        from app.pages_modules.consultant_languages import show_consultant_languages
        show_consultant_languages(consultant)
        
        mock_st.subheader.assert_called()
    
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_add_language_to_consultant(self, mock_session):
        """Test ajout langue à consultant"""
        mock_session_obj = mock_session.return_value.__enter__.return_value
        
        from app.pages_modules.consultant_languages import add_language_to_consultant
        result = add_language_to_consultant(1, "Français", "Courant")
        
        mock_session_obj.add.assert_called_once()
        mock_session_obj.commit.assert_called_once()
    
    @patch('app.pages_modules.consultant_languages.get_database_session')
    def test_get_consultant_languages(self, mock_session):
        """Test récupération langues consultant"""
        mock_session_obj = mock_session.return_value.__enter__.return_value
        mock_session_obj.query.return_value.filter.return_value.all.return_value = []
        
        from app.pages_modules.consultant_languages import get_consultant_languages
        result = get_consultant_languages(1)
        
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()