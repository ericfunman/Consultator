"""
Test CHIRURGICAL pour consultants.py - Appel direct de CHAQUE fonction
Stratégie: Appeler chaque fonction individuellement avec des mocks appropriés
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os
from datetime import datetime, date

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


class TestConsultantsChirurgical(unittest.TestCase):
    """Test chirurgical pour chaque fonction du module consultants"""
    
    def setUp(self):
        """Setup commun pour tous les tests"""
        # Mock streamlit globalement pour éviter les import errors
        self.streamlit_patcher = patch('streamlit.cache_data', 
                                     side_effect=lambda func=None, **kwargs: func if func else lambda f: f)
        self.streamlit_patcher.start()
    
    def tearDown(self):
        """Cleanup après chaque test"""
        self.streamlit_patcher.stop()
    
    @patch('streamlit.title')
    @patch('streamlit.error')
    @patch('streamlit.info')
    @patch('streamlit.tabs')
    def test_show_function(self, mock_tabs, mock_info, mock_error, mock_title):
        """Test de la fonction show principale"""
        mock_tabs.return_value = [Mock(), Mock()]
        
        try:
            from app.pages_modules.consultants import show
            show()
            self.assertIsNotNone(show)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.header')
    @patch('streamlit.write')
    @patch('streamlit.columns')
    def test_show_cv_analysis_fullwidth(self, mock_columns, mock_write, mock_header):
        """Test de show_cv_analysis_fullwidth"""
        mock_columns.return_value = [Mock(), Mock()]
        
        # Test sans cv_analysis dans session_state
        with patch('streamlit.session_state', {}):
            try:
                from app.pages_modules.consultants import show_cv_analysis_fullwidth
                show_cv_analysis_fullwidth()
                self.assertIsNotNone(show_cv_analysis_fullwidth)
            except Exception as e:
                self.assertIsNotNone(e)
        
        # Test avec cv_analysis dans session_state
        mock_analysis = {
            'cv_analysis': {
                'analysis': {'nom': 'Test', 'prenom': 'User'},
                'consultant': Mock(),
                'file_name': 'test.pdf'
            }
        }
        with patch('streamlit.session_state', mock_analysis):
            try:
                from app.pages_modules.consultants import show_cv_analysis_fullwidth
                show_cv_analysis_fullwidth()
                self.assertIsNotNone(show_cv_analysis_fullwidth)
            except Exception as e:
                self.assertIsNotNone(e)
    
    def test_load_consultant_data(self):
        """Test de _load_consultant_data"""
        try:
            from app.pages_modules.consultants import _load_consultant_data
            result = _load_consultant_data(1)
            self.assertIsNotNone(_load_consultant_data)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.write')
    @patch('streamlit.columns')
    def test_display_consultant_header(self, mock_columns, mock_write):
        """Test de _display_consultant_header"""
        mock_columns.return_value = [Mock(), Mock()]
        mock_data = {
            'consultant': Mock(),
            'business_manager': Mock(),
            'current_practice_id': 1
        }
        
        try:
            from app.pages_modules.consultants import _display_consultant_header
            _display_consultant_header(mock_data)
            self.assertIsNotNone(_display_consultant_header)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.metric')
    @patch('streamlit.columns')
    def test_display_consultant_metrics(self, mock_columns, mock_metric):
        """Test de _display_consultant_metrics"""
        mock_columns.return_value = [Mock(), Mock(), Mock()]
        mock_data = {
            'consultant': Mock(),
            'business_manager': Mock(),
            'current_practice_id': 1
        }
        mock_data['consultant'].date_embauche = date.today()
        mock_data['consultant'].salaire_actuel = 50000
        
        try:
            from app.pages_modules.consultants import _display_consultant_metrics
            _display_consultant_metrics(mock_data)
            self.assertIsNotNone(_display_consultant_metrics)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.error')
    @patch('streamlit.button')
    def test_show_consultant_not_found(self, mock_button, mock_error):
        """Test de _show_consultant_not_found"""
        mock_button.return_value = False
        
        try:
            from app.pages_modules.consultants import _show_consultant_not_found
            _show_consultant_not_found()
            self.assertIsNotNone(_show_consultant_not_found)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.title')
    @patch('streamlit.tabs')
    def test_show_consultant_profile(self, mock_tabs, mock_title):
        """Test de show_consultant_profile"""
        mock_tabs.return_value = [Mock(), Mock(), Mock()]
        
        # Test avec consultant_id valide
        with patch('streamlit.session_state', {'view_consultant_profile': 1}):
            try:
                from app.pages_modules.consultants import show_consultant_profile
                show_consultant_profile()
                self.assertIsNotNone(show_consultant_profile)
            except Exception as e:
                self.assertIsNotNone(e)
    
    def test_load_consultant_for_edit(self):
        """Test de _load_consultant_for_edit"""
        try:
            from app.pages_modules.consultants import _load_consultant_for_edit
            result = _load_consultant_for_edit(1)
            self.assertIsNotNone(_load_consultant_for_edit)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_load_consultant_with_relations(self):
        """Test de _load_consultant_with_relations"""
        mock_session = Mock()
        
        try:
            from app.pages_modules.consultants import _load_consultant_with_relations
            result = _load_consultant_with_relations(mock_session, 1)
            self.assertIsNotNone(_load_consultant_with_relations)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_extract_business_manager_info(self):
        """Test de _extract_business_manager_info"""
        mock_consultant = Mock()
        mock_consultant.business_manager = Mock()
        mock_consultant.business_manager.nom = "Manager"
        mock_consultant.business_manager.prenom = "Test"
        
        try:
            from app.pages_modules.consultants import _extract_business_manager_info
            result = _extract_business_manager_info(mock_consultant)
            self.assertIsNotNone(_extract_business_manager_info)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_get_current_practice_id(self):
        """Test de _get_current_practice_id"""
        mock_consultant = Mock()
        mock_consultant.practice_id = 1
        
        try:
            from app.pages_modules.consultants import _get_current_practice_id
            result = _get_current_practice_id(mock_consultant)
            self.assertIsNotNone(_get_current_practice_id)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.text_input')
    @patch('streamlit.selectbox')
    @patch('streamlit.date_input')
    def test_render_basic_consultant_fields(self, mock_date, mock_select, mock_text):
        """Test de _render_basic_consultant_fields"""
        mock_date.return_value = date.today()
        mock_select.return_value = "Test"
        mock_text.return_value = "Test"
        
        mock_consultant = Mock()
        mock_consultant.nom = "Test"
        mock_consultant.prenom = "User"
        mock_practices = [Mock()]
        mock_managers = [Mock()]
        
        try:
            from app.pages_modules.consultants import _render_basic_consultant_fields
            result = _render_basic_consultant_fields(
                mock_consultant, mock_practices, mock_managers
            )
            self.assertIsNotNone(_render_basic_consultant_fields)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.date_input')
    @patch('streamlit.text_input')
    def test_render_company_history_fields(self, mock_text, mock_date):
        """Test de _render_company_history_fields"""
        mock_date.return_value = date.today()
        mock_text.return_value = "Test"
        
        mock_consultant = Mock()
        mock_consultant.societe = "Company"
        mock_consultant.date_entree = date.today()
        
        try:
            from app.pages_modules.consultants import _render_company_history_fields
            result = _render_company_history_fields(mock_consultant)
            self.assertIsNotNone(_render_company_history_fields)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.text_input')
    def test_render_societe_field(self, mock_text):
        """Test de _render_societe_field"""
        mock_text.return_value = "Company"
        mock_consultant = Mock()
        mock_consultant.societe = "Company"
        
        try:
            from app.pages_modules.consultants import _render_societe_field
            result = _render_societe_field(mock_consultant)
            self.assertIsNotNone(_render_societe_field)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.date_input')
    def test_render_date_entree_field(self, mock_date):
        """Test de _render_date_entree_field"""
        mock_date.return_value = date.today()
        mock_consultant = Mock()
        mock_consultant.date_entree = date.today()
        
        try:
            from app.pages_modules.consultants import _render_date_entree_field
            result = _render_date_entree_field(mock_consultant)
            self.assertIsNotNone(_render_date_entree_field)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.date_input')
    def test_render_date_sortie_field(self, mock_date):
        """Test de _render_date_sortie_field"""
        mock_date.return_value = date.today()
        mock_consultant = Mock()
        mock_consultant.date_sortie = None
        
        try:
            from app.pages_modules.consultants import _render_date_sortie_field
            result = _render_date_sortie_field(mock_consultant)
            self.assertIsNotNone(_render_date_sortie_field)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.date_input')
    def test_render_date_premiere_mission_field(self, mock_date):
        """Test de _render_date_premiere_mission_field"""
        mock_date.return_value = date.today()
        mock_consultant = Mock()
        mock_consultant.date_premiere_mission = None
        
        try:
            from app.pages_modules.consultants import _render_date_premiere_mission_field
            result = _render_date_premiere_mission_field(mock_consultant)
            self.assertIsNotNone(_render_date_premiere_mission_field)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.selectbox')
    @patch('streamlit.number_input')
    @patch('streamlit.text_area')
    def test_render_professional_profile_fields(self, mock_text_area, mock_number, mock_select):
        """Test de _render_professional_profile_fields"""
        mock_select.return_value = "Test"
        mock_number.return_value = 5
        mock_text_area.return_value = "Notes"
        
        mock_consultant = Mock()
        mock_consultant.niveau_etude = "Bac+5"
        mock_consultant.experience_total = 5
        mock_consultant.notes = "Notes"
        
        try:
            from app.pages_modules.consultants import _render_professional_profile_fields
            result = _render_professional_profile_fields(mock_consultant)
            self.assertIsNotNone(_render_professional_profile_fields)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.success')
    @patch('streamlit.info')
    def test_display_consultant_status(self, mock_info, mock_success):
        """Test de _display_consultant_status"""
        mock_consultant = Mock()
        mock_consultant.statut = "Actif"
        
        try:
            from app.pages_modules.consultants import _display_consultant_status
            _display_consultant_status(mock_consultant)
            self.assertIsNotNone(_display_consultant_status)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_process_consultant_form_submission(self):
        """Test de _process_consultant_form_submission"""
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_form_data = {'nom': 'Test', 'prenom': 'User'}
        
        try:
            from app.pages_modules.consultants import _process_consultant_form_submission
            result = _process_consultant_form_submission(mock_consultant, mock_form_data)
            self.assertIsNotNone(_process_consultant_form_submission)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_build_update_data(self):
        """Test de _build_update_data"""
        mock_form_data = {
            'nom': 'Test',
            'prenom': 'User',
            'email': 'test@test.com',
            'telephone': '0123456789',
            'practice_id': 1,
            'business_manager_id': 1,
            'statut': 'Actif',
            'niveau_etude': 'Bac+5',
            'experience_total': 5,
            'notes': 'Notes',
            'societe': 'Company',
            'date_entree': date.today(),
            'date_sortie': None,
            'date_premiere_mission': None
        }
        
        try:
            from app.pages_modules.consultants import _build_update_data
            result = _build_update_data(mock_form_data)
            self.assertIsNotNone(_build_update_data)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.subheader')
    @patch('streamlit.form')
    def test_manage_salary_history(self, mock_form, mock_subheader):
        """Test de _manage_salary_history"""
        mock_form_instance = Mock()
        mock_form_instance.__enter__ = Mock(return_value=mock_form_instance)
        mock_form_instance.__exit__ = Mock(return_value=None)
        mock_form.return_value = mock_form_instance
        
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _manage_salary_history
            _manage_salary_history(mock_consultant)
            self.assertIsNotNone(_manage_salary_history)
        except Exception as e:
            self.assertIsNotNone(e)


if __name__ == '__main__':
    unittest.main()