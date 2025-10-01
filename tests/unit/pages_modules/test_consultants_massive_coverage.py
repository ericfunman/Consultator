"""
Tests de coverage massif pour consultants.py
Objectif: Augmenter le coverage du module consultants de 50% vers 80%+
"""

import unittest
from unittest.mock import patch, MagicMock, Mock
from datetime import date
import pytest
import streamlit as st


class TestConsultantsMassiveCoverage(unittest.TestCase):
    """Tests de coverage massif pour le module consultants"""

    def setUp(self):
        """Setup pour chaque test"""
        self.mock_consultant = MagicMock()
        self.mock_consultant.id = 1
        self.mock_consultant.prenom = "Jean"
        self.mock_consultant.nom = "Dupont"
        self.mock_consultant.email = "jean.dupont@test.com"
        self.mock_consultant.telephone = "0123456789"
        self.mock_consultant.salaire_actuel = 50000
        self.mock_consultant.disponibilite = True
        self.mock_consultant.societe = "Quanteam"
        self.mock_consultant.grade = "Junior"
        self.mock_consultant.type_contrat = "CDI"
        self.mock_consultant.date_entree = date.today()
        self.mock_consultant.date_sortie = None
        self.mock_consultant.date_premiere_mission = date.today()
        self.mock_consultant.experience_annees = 5

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.imports_ok', False)
    def test_show_imports_not_ok(self, mock_st):
        """Test show() avec imports_ok = False"""
        mock_st.title.return_value = None
        mock_st.error.return_value = None
        mock_st.info.return_value = None
        
        from app.pages_modules.consultants import show
        show()
        
        # Vérifications
        mock_st.title.assert_called_once_with("👥 Gestion des consultants")
        mock_st.error.assert_called_once_with("❌ Les services de base ne sont pas disponibles")
        mock_st.info.assert_called_once_with("Vérifiez que tous les modules sont correctement installés")

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.imports_ok', True)
    @patch('app.pages_modules.consultants.show_consultant_profile')
    def test_show_with_view_consultant_profile_session(self, mock_show_profile, mock_st):
        """Test show() avec view_consultant_profile dans session_state"""
        mock_st.title.return_value = None
        mock_st.session_state = {"view_consultant_profile": True}
        mock_show_profile.return_value = None
        
        from app.pages_modules.consultants import show
        show()
        
        # Vérifications
        mock_st.title.assert_called_once_with("👥 Gestion des consultants")
        mock_show_profile.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.imports_ok', True)
    @patch('app.pages_modules.consultants._show_consultants_list')
    @patch('app.pages_modules.consultants._show_add_consultant_form')
    def test_show_main_tabs(self, mock_add_form, mock_list, mock_st):
        """Test show() avec les onglets principaux"""
        mock_st.title.return_value = None
        mock_st.session_state = {}
        mock_st.tabs.return_value = [MagicMock(), MagicMock()]
        mock_list.return_value = None
        mock_add_form.return_value = None
        
        from app.pages_modules.consultants import show
        show()
        
        # Vérifications
        mock_st.title.assert_called_once_with("👥 Gestion des consultants")
        mock_st.tabs.assert_called_once_with([" Consultants", "➕ Ajouter un consultant"])
        mock_list.assert_called_once()
        mock_add_form.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.ConsultantService')
    def test_show_consultants_list_basic(self, mock_service, mock_st):
        """Test _show_consultants_list fonctionnement de base"""
        # Setup
        mock_st.header.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.text_input.return_value = ""
        mock_st.selectbox.return_value = "Tous"
        mock_st.number_input.return_value = 20
        mock_st.checkbox.return_value = False
        mock_st.button.return_value = False
        mock_service.get_all_consultants_paginated.return_value = ([], 0)
        mock_service.count_all_consultants.return_value = 0
        mock_st.info.return_value = None
        
        from app.pages_modules.consultants import _show_consultants_list
        _show_consultants_list()
        
        # Vérifications
        mock_st.header.assert_called_once_with("📋 Liste des consultants")
        mock_service.get_all_consultants_paginated.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.ConsultantService')
    def test_show_consultants_list_with_search(self, mock_service, mock_st):
        """Test _show_consultants_list avec recherche"""
        # Setup
        mock_st.header.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.text_input.return_value = "Jean"  # Terme de recherche
        mock_st.selectbox.return_value = "Tous"
        mock_st.number_input.return_value = 20
        mock_st.checkbox.return_value = False
        mock_st.button.return_value = False
        mock_service.search_consultants.return_value = ([], 0)
        mock_st.info.return_value = None
        
        from app.pages_modules.consultants import _show_consultants_list
        _show_consultants_list()
        
        # Vérifications
        mock_service.search_consultants.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.ConsultantService')
    def test_show_consultants_list_with_results(self, mock_service, mock_st):
        """Test _show_consultants_list avec des résultats"""
        # Setup
        mock_st.header.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.text_input.return_value = ""
        mock_st.selectbox.return_value = "Tous"
        mock_st.number_input.return_value = 20
        mock_st.checkbox.return_value = False
        mock_st.button.return_value = False
        
        # Mock consultants
        consultants = [self.mock_consultant]
        mock_service.get_all_consultants_paginated.return_value = (consultants, 1)
        mock_service.count_all_consultants.return_value = 1
        
        # Mock pour l'affichage
        mock_st.subheader.return_value = None
        mock_st.dataframe.return_value = None
        
        from app.pages_modules.consultants import _show_consultants_list
        _show_consultants_list()
        
        # Vérifications
        mock_st.subheader.assert_called()
        mock_st.dataframe.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.PracticeService')
    def test_show_add_consultant_form_basic(self, mock_practice_service, mock_st):
        """Test _show_add_consultant_form fonctionnement de base"""
        # Setup
        mock_st.header.return_value = None
        mock_st.form.return_value.__enter__ = Mock()
        mock_st.form.return_value.__exit__ = Mock()
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.text_input.side_effect = ["Jean", "Dupont", "jean.dupont@test.com", "0123456789"]
        mock_st.number_input.return_value = 50000
        mock_st.selectbox.side_effect = ["Practice 1", "Junior", "CDI", "Quanteam"]
        mock_st.date_input.side_effect = [date.today(), None, date.today()]
        mock_st.checkbox.return_value = True
        mock_st.form_submit_button.return_value = False  # Pas de soumission
        
        # Mock service
        mock_practice_service.get_all_practices.return_value = []
        
        from app.pages_modules.consultants import _show_add_consultant_form
        _show_add_consultant_form()
        
        # Vérifications
        mock_st.header.assert_called_once_with("👤 Ajouter un nouveau consultant")

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.PracticeService')
    @patch('app.pages_modules.consultants.ConsultantService')
    def test_show_add_consultant_form_submit_success(self, mock_consultant_service, mock_practice_service, mock_st):
        """Test _show_add_consultant_form avec soumission réussie"""
        # Setup
        mock_st.header.return_value = None
        mock_st.form.return_value.__enter__ = Mock()
        mock_st.form.return_value.__exit__ = Mock()
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.text_input.side_effect = ["Jean", "Dupont", "jean.dupont@test.com", "0123456789"]
        mock_st.number_input.return_value = 50000
        mock_st.selectbox.side_effect = ["Practice 1", "Junior", "CDI", "Quanteam"]
        mock_st.date_input.side_effect = [date.today(), None, date.today()]
        mock_st.checkbox.return_value = True
        mock_st.form_submit_button.return_value = True  # Soumission
        mock_st.success.return_value = None
        mock_st.rerun.return_value = None
        
        # Mock services
        mock_practice_service.get_all_practices.return_value = []
        mock_practice_service.get_practice_by_name.return_value = MagicMock(id=1)
        mock_consultant_service.create_consultant.return_value = True
        
        from app.pages_modules.consultants import _show_add_consultant_form
        _show_add_consultant_form()
        
        # Vérifications
        mock_consultant_service.create_consultant.assert_called_once()
        mock_st.success.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.ConsultantService')
    def test_show_consultant_profile_not_found(self, mock_service, mock_st):
        """Test show_consultant_profile avec consultant non trouvé"""
        # Setup
        mock_st.session_state = {"consultant_id": 999}
        mock_service.get_consultant_by_id.return_value = None
        mock_st.error.return_value = None
        mock_st.button.return_value = False
        
        from app.pages_modules.consultants import show_consultant_profile
        show_consultant_profile()
        
        # Vérifications
        mock_service.get_consultant_by_id.assert_called_once_with(999)
        mock_st.error.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants.ConsultantService')
    @patch('app.pages_modules.consultants._display_consultant_header')
    @patch('app.pages_modules.consultants._display_consultant_metrics')
    def test_show_consultant_profile_found(self, mock_metrics, mock_header, mock_service, mock_st):
        """Test show_consultant_profile avec consultant trouvé"""
        # Setup
        mock_st.session_state = {"consultant_id": 1}
        mock_service.get_consultant_by_id.return_value = self.mock_consultant
        mock_st.button.return_value = False
        mock_st.tabs.return_value = [MagicMock() for _ in range(7)]
        mock_header.return_value = None
        mock_metrics.return_value = None
        
        from app.pages_modules.consultants import show_consultant_profile
        show_consultant_profile()
        
        # Vérifications
        mock_service.get_consultant_by_id.assert_called_once_with(1)
        mock_header.assert_called_once()
        mock_metrics.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_header_basic(self, mock_st):
        """Test _display_consultant_header"""
        # Setup
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.markdown.return_value = None
        
        from app.pages_modules.consultants import _display_consultant_header
        _display_consultant_header(self.mock_consultant)
        
        # Vérifications
        mock_st.columns.assert_called_once_with([3, 1])
        mock_st.markdown.assert_called()

    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_metrics_basic(self, mock_st):
        """Test _display_consultant_metrics"""
        # Setup
        mock_st.columns.return_value = [MagicMock() for _ in range(5)]
        mock_st.metric.return_value = None
        
        from app.pages_modules.consultants import _display_consultant_metrics
        _display_consultant_metrics(self.mock_consultant)
        
        # Vérifications
        mock_st.columns.assert_called_once_with(5)
        # Vérifier que st.metric est appelé 5 fois
        self.assertEqual(mock_st.metric.call_count, 5)

    @patch('app.pages_modules.consultants.st')
    def test_render_societe_field_basic(self, mock_st):
        """Test _render_societe_field"""
        # Setup
        mock_st.selectbox.return_value = "Quanteam"
        
        from app.pages_modules.consultants import _render_societe_field
        result = _render_societe_field(self.mock_consultant)
        
        # Vérifications
        self.assertEqual(result, "Quanteam")
        mock_st.selectbox.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_render_date_entree_field_basic(self, mock_st):
        """Test _render_date_entree_field"""
        # Setup
        mock_st.date_input.return_value = date.today()
        
        from app.pages_modules.consultants import _render_date_entree_field
        result = _render_date_entree_field(self.mock_consultant)
        
        # Vérifications
        self.assertEqual(result, date.today())
        mock_st.date_input.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_render_date_sortie_field_basic(self, mock_st):
        """Test _render_date_sortie_field"""
        # Setup
        mock_st.date_input.return_value = None
        
        from app.pages_modules.consultants import _render_date_sortie_field
        result = _render_date_sortie_field(self.mock_consultant)
        
        # Vérifications
        self.assertEqual(result, None)
        mock_st.date_input.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_render_date_premiere_mission_field_basic(self, mock_st):
        """Test _render_date_premiere_mission_field"""
        # Setup
        mock_st.date_input.return_value = date.today()
        
        from app.pages_modules.consultants import _render_date_premiere_mission_field
        result = _render_date_premiere_mission_field(self.mock_consultant)
        
        # Vérifications
        self.assertEqual(result, date.today())
        mock_st.date_input.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_render_skill_level_fields_basic(self, mock_st):
        """Test _render_skill_level_fields"""
        # Setup
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.selectbox.return_value = "Confirmé"
        mock_st.number_input.return_value = 3
        
        from app.pages_modules.consultants import _render_skill_level_fields
        niveau, experience = _render_skill_level_fields()
        
        # Vérifications
        self.assertEqual(niveau, "Confirmé")
        self.assertEqual(experience, 3)
        mock_st.columns.assert_called_once_with(2)

    @patch('app.pages_modules.consultants.st')
    def test_display_no_functional_skills_message_basic(self, mock_st):
        """Test _display_no_functional_skills_message"""
        # Setup
        mock_st.info.return_value = None
        mock_st.write.return_value = None
        
        from app.pages_modules.consultants import _display_no_functional_skills_message
        _display_no_functional_skills_message()
        
        # Vérifications
        mock_st.info.assert_called_once_with("📝 Aucune compétence fonctionnelle enregistrée")
        mock_st.write.assert_called_once()


if __name__ == "__main__":
    unittest.main()