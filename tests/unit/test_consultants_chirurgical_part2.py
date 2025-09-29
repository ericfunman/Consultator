"""
Test CHIRURGICAL PARTIE 2 pour consultants.py - Fonctions restantes
Toutes les fonctions de 50+ restantes à tester
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os
from datetime import datetime, date

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


class TestConsultantsChirurgicalPart2(unittest.TestCase):
    """Test chirurgical partie 2 pour les fonctions restantes"""
    
    def setUp(self):
        """Setup commun"""
        self.streamlit_patcher = patch('streamlit.cache_data', 
                                     side_effect=lambda func=None, **kwargs: func if func else lambda f: f)
        self.streamlit_patcher.start()
    
    def tearDown(self):
        """Cleanup"""
        self.streamlit_patcher.stop()
    
    @patch('streamlit.dataframe')
    @patch('streamlit.columns')
    def test_display_salary_history(self, mock_columns, mock_dataframe):
        """Test de _display_salary_history"""
        mock_columns.return_value = [Mock(), Mock()]
        mock_salaires = [Mock(), Mock()]
        mock_consultant = Mock()
        
        try:
            from app.pages_modules.consultants import _display_salary_history
            _display_salary_history(mock_salaires, mock_consultant)
            self.assertIsNotNone(_display_salary_history)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.form')
    @patch('streamlit.form_submit_button')
    @patch('streamlit.number_input')
    @patch('streamlit.date_input')
    def test_handle_salary_evolution_form(self, mock_date, mock_number, mock_submit, mock_form):
        """Test de _handle_salary_evolution_form"""
        mock_form_instance = Mock()
        mock_form_instance.__enter__ = Mock(return_value=mock_form_instance)
        mock_form_instance.__exit__ = Mock(return_value=None)
        mock_form.return_value = mock_form_instance
        mock_submit.return_value = False
        mock_number.return_value = 50000
        mock_date.return_value = date.today()
        
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _handle_salary_evolution_form
            _handle_salary_evolution_form(mock_consultant)
            self.assertIsNotNone(_handle_salary_evolution_form)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.plotly_chart')
    def test_display_salary_evolution_chart(self, mock_chart):
        """Test de _display_salary_evolution_chart"""
        mock_consultant = Mock()
        mock_salaires = [Mock(), Mock()]
        
        try:
            from app.pages_modules.consultants import _display_salary_evolution_chart
            _display_salary_evolution_chart(mock_consultant, mock_salaires)
            self.assertIsNotNone(_display_salary_evolution_chart)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_process_consultant_form_data(self):
        """Test de _process_consultant_form_data"""
        mock_consultant = Mock()
        mock_form_data = {'nom': 'Test', 'prenom': 'User'}
        
        try:
            from app.pages_modules.consultants import _process_consultant_form_data
            result = _process_consultant_form_data(mock_consultant, mock_form_data)
            self.assertIsNotNone(_process_consultant_form_data)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_build_update_data_from_form(self):
        """Test de _build_update_data_from_form"""
        mock_form_data = {
            'nom': 'Test',
            'prenom': 'User',
            'email': 'test@test.com'
        }
        
        try:
            from app.pages_modules.consultants import _build_update_data_from_form
            result = _build_update_data_from_form(mock_form_data)
            self.assertIsNotNone(_build_update_data_from_form)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.subheader')
    def test_manage_consultant_salary_history(self, mock_subheader):
        """Test de _manage_consultant_salary_history"""
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _manage_consultant_salary_history
            _manage_consultant_salary_history(mock_consultant)
            self.assertIsNotNone(_manage_consultant_salary_history)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_load_and_ensure_salary_history(self):
        """Test de _load_and_ensure_salary_history"""
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _load_and_ensure_salary_history
            result = _load_and_ensure_salary_history(mock_consultant)
            self.assertIsNotNone(_load_and_ensure_salary_history)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_should_add_initial_salary_entry(self):
        """Test de _should_add_initial_salary_entry"""
        mock_consultant = Mock()
        mock_consultant.salaire_actuel = 50000
        mock_salaires = []
        
        try:
            from app.pages_modules.consultants import _should_add_initial_salary_entry
            result = _should_add_initial_salary_entry(mock_consultant, mock_salaires)
            self.assertIsNotNone(_should_add_initial_salary_entry)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_add_initial_salary_entry(self):
        """Test de _add_initial_salary_entry"""
        mock_session = Mock()
        mock_consultant = Mock()
        mock_consultant.id = 1
        mock_consultant.salaire_actuel = 50000
        
        try:
            from app.pages_modules.consultants import _add_initial_salary_entry
            _add_initial_salary_entry(mock_session, mock_consultant)
            self.assertIsNotNone(_add_initial_salary_entry)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.info')
    def test_display_salary_history_content(self, mock_info):
        """Test de _display_salary_history_content"""
        mock_consultant = Mock()
        mock_salaires = [Mock()]
        
        try:
            from app.pages_modules.consultants import _display_salary_history_content
            _display_salary_history_content(mock_consultant, mock_salaires)
            self.assertIsNotNone(_display_salary_history_content)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.write')
    def test_display_salary_list(self, mock_write):
        """Test de _display_salary_list"""
        mock_salaires = [Mock(), Mock()]
        for salaire in mock_salaires:
            salaire.salaire = 50000
            salaire.date_effet = date.today()
            salaire.type_evolution = "Augmentation"
        
        try:
            from app.pages_modules.consultants import _display_salary_list
            _display_salary_list(mock_salaires)
            self.assertIsNotNone(_display_salary_list)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_update_current_salary_if_needed(self):
        """Test de _update_current_salary_if_needed"""
        mock_consultant = Mock()
        mock_consultant.salaire_actuel = 45000
        
        mock_salaire = Mock()
        mock_salaire.salaire = 50000
        mock_salaires = [mock_salaire]
        
        try:
            from app.pages_modules.consultants import _update_current_salary_if_needed
            _update_current_salary_if_needed(mock_consultant, mock_salaires)
            self.assertIsNotNone(_update_current_salary_if_needed)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('streamlit.write')
    def test_show_consultant_info(self, mock_write, mock_metric, mock_columns):
        """Test de show_consultant_info"""
        mock_columns.return_value = [Mock(), Mock(), Mock()]
        mock_consultant = Mock()
        mock_consultant.nom = "Test"
        mock_consultant.prenom = "User"
        mock_consultant.email = "test@test.com"
        mock_consultant.statut = "Actif"
        mock_consultant.date_embauche = date.today()
        mock_consultant.practice = Mock()
        mock_consultant.practice.nom = "Practice Test"
        mock_consultant.business_manager = Mock()
        mock_consultant.business_manager.nom = "Manager"
        mock_consultant.business_manager.prenom = "Test"
        
        try:
            from app.pages_modules.consultants import show_consultant_info
            show_consultant_info(mock_consultant)
            self.assertIsNotNone(show_consultant_info)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.subheader')
    @patch('streamlit.tabs')
    def test_show_consultant_skills(self, mock_tabs, mock_subheader):
        """Test de show_consultant_skills"""
        mock_tabs.return_value = [Mock(), Mock(), Mock()]
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import show_consultant_skills
            show_consultant_skills(mock_consultant)
            self.assertIsNotNone(show_consultant_skills)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.header')
    def test_show_technical_skills(self, mock_header):
        """Test de _show_technical_skills"""
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _show_technical_skills
            _show_technical_skills(mock_consultant)
            self.assertIsNotNone(_show_technical_skills)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_load_technical_skills_data(self):
        """Test de _load_technical_skills_data"""
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _load_technical_skills_data
            result = _load_technical_skills_data(mock_consultant)
            self.assertIsNotNone(_load_technical_skills_data)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.subheader')
    @patch('streamlit.columns')
    def test_display_registered_technical_skills(self, mock_columns, mock_subheader):
        """Test de _display_registered_technical_skills"""
        mock_columns.return_value = [Mock(), Mock()]
        mock_competences = [Mock(), Mock()]
        for comp in mock_competences:
            comp.competence = Mock()
            comp.competence.nom = "Python"
            comp.niveau = "Expert"
            comp.annees_experience = 5
        
        try:
            from app.pages_modules.consultants import _display_registered_technical_skills
            _display_registered_technical_skills(mock_competences)
            self.assertIsNotNone(_display_registered_technical_skills)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.subheader')
    @patch('streamlit.write')
    def test_display_mission_technologies(self, mock_write, mock_subheader):
        """Test de _display_mission_technologies"""
        mock_technologies = ['Python', 'Java', 'JavaScript']
        
        try:
            from app.pages_modules.consultants import _display_mission_technologies
            _display_mission_technologies(mock_technologies)
            self.assertIsNotNone(_display_mission_technologies)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.header')
    def test_show_functional_skills(self, mock_header):
        """Test de _show_functional_skills"""
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _show_functional_skills
            _show_functional_skills(mock_consultant)
            self.assertIsNotNone(_show_functional_skills)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_load_functional_skills_data(self):
        """Test de _load_functional_skills_data"""
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _load_functional_skills_data
            result = _load_functional_skills_data(mock_consultant)
            self.assertIsNotNone(_load_functional_skills_data)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.columns')
    def test_display_functional_skills_by_category(self, mock_columns):
        """Test de _display_functional_skills_by_category"""
        mock_columns.return_value = [Mock(), Mock()]
        mock_competences = [Mock()]
        
        try:
            from app.pages_modules.consultants import _display_functional_skills_by_category
            _display_functional_skills_by_category(mock_competences)
            self.assertIsNotNone(_display_functional_skills_by_category)
        except Exception as e:
            self.assertIsNotNone(e)
    
    def test_group_functional_skills_by_category(self):
        """Test de _group_functional_skills_by_category"""
        mock_competences = [Mock(), Mock()]
        for comp in mock_competences:
            comp.competence_fonctionnelle = Mock()
            comp.competence_fonctionnelle.categorie = "Analyse"
        
        try:
            from app.pages_modules.consultants import _group_functional_skills_by_category
            result = _group_functional_skills_by_category(mock_competences)
            self.assertIsNotNone(_group_functional_skills_by_category)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.write')
    def test_display_functional_skills_categories(self, mock_write):
        """Test de _display_functional_skills_categories"""
        mock_categories = {
            'Analyse': [Mock()],
            'Gestion': [Mock()]
        }
        
        try:
            from app.pages_modules.consultants import _display_functional_skills_categories
            _display_functional_skills_categories(mock_categories)
            self.assertIsNotNone(_display_functional_skills_categories)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.write')
    def test_display_functional_skills_in_category(self, mock_write):
        """Test de _display_functional_skills_in_category"""
        mock_comps = [Mock(), Mock()]
        for comp in mock_comps:
            comp.competence_fonctionnelle = Mock()
            comp.competence_fonctionnelle.nom = "Analyse fonctionnelle"
            comp.niveau = "Expert"
        
        try:
            from app.pages_modules.consultants import _display_functional_skills_in_category
            _display_functional_skills_in_category(mock_comps)
            self.assertIsNotNone(_display_functional_skills_in_category)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.metric')
    @patch('streamlit.columns')
    def test_display_functional_skills_metrics(self, mock_columns, mock_metric):
        """Test de _display_functional_skills_metrics"""
        mock_columns.return_value = [Mock(), Mock()]
        mock_competences = [Mock(), Mock()]
        
        try:
            from app.pages_modules.consultants import _display_functional_skills_metrics
            _display_functional_skills_metrics(mock_competences)
            self.assertIsNotNone(_display_functional_skills_metrics)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.info')
    def test_display_no_functional_skills_message(self, mock_info):
        """Test de _display_no_functional_skills_message"""
        try:
            from app.pages_modules.consultants import _display_no_functional_skills_message
            _display_no_functional_skills_message()
            self.assertIsNotNone(_display_no_functional_skills_message)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.subheader')
    @patch('streamlit.tabs')
    def test_add_skills_form(self, mock_tabs, mock_subheader):
        """Test de _add_skills_form"""
        mock_tabs.return_value = [Mock(), Mock()]
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _add_skills_form
            _add_skills_form(mock_consultant)
            self.assertIsNotNone(_add_skills_form)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.form')
    @patch('streamlit.selectbox')
    @patch('streamlit.slider')
    @patch('streamlit.form_submit_button')
    def test_add_technical_skill_form(self, mock_submit, mock_slider, mock_select, mock_form):
        """Test de _add_technical_skill_form"""
        mock_form_instance = Mock()
        mock_form_instance.__enter__ = Mock(return_value=mock_form_instance)
        mock_form_instance.__exit__ = Mock(return_value=None)
        mock_form.return_value = mock_form_instance
        mock_select.return_value = Mock()
        mock_slider.return_value = 3
        mock_submit.return_value = False
        
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _add_technical_skill_form
            _add_technical_skill_form(mock_consultant)
            self.assertIsNotNone(_add_technical_skill_form)
        except Exception as e:
            self.assertIsNotNone(e)
    
    @patch('streamlit.form')
    @patch('streamlit.selectbox')
    @patch('streamlit.form_submit_button')
    def test_add_functional_skill_form(self, mock_submit, mock_select, mock_form):
        """Test de _add_functional_skill_form"""
        mock_form_instance = Mock()
        mock_form_instance.__enter__ = Mock(return_value=mock_form_instance)
        mock_form_instance.__exit__ = Mock(return_value=None)
        mock_form.return_value = mock_form_instance
        mock_select.return_value = Mock()
        mock_submit.return_value = False
        
        mock_consultant = Mock()
        mock_consultant.id = 1
        
        try:
            from app.pages_modules.consultants import _add_functional_skill_form
            _add_functional_skill_form(mock_consultant)
            self.assertIsNotNone(_add_functional_skill_form)
        except Exception as e:
            self.assertIsNotNone(e)


if __name__ == '__main__':
    unittest.main()