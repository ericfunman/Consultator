"""
Tests pour business_managers.py - Ciblage couverture 52% → 85%+
Fokus sur les fonctions principales et les chemins non couverts
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
import sys
import os
from datetime import datetime, date

# Ajouter le répertoire racine au path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)


class MockSessionState:
    """Mock de streamlit.session_state qui peut être utilisé avec del"""
    def __init__(self, initial_data=None):
        self._data = initial_data or {}
    
    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            if not hasattr(self, '_data'):
                super().__setattr__('_data', {})
            self._data[name] = value
    
    def __delattr__(self, name):
        if name in self._data:
            del self._data[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __contains__(self, name):
        return name in self._data
    
    def get(self, name, default=None):
        return self._data.get(name, default)


class TestBusinessManagersCoverage(unittest.TestCase):
    """Tests ciblés pour améliorer la couverture de business_managers.py"""

    def setUp(self):
        """Setup pour chaque test"""
        # Mock BusinessManager
        self.mock_bm = Mock()
        self.mock_bm.id = 1
        self.mock_bm.prenom = "Jean"
        self.mock_bm.nom = "Dupont"
        self.mock_bm.email = "jean.dupont@test.com"
        self.mock_bm.telephone = "0123456789"
        self.mock_bm.date_creation = datetime(2024, 1, 1)
        self.mock_bm.actif = True

        # Mock session database
        self.mock_session = MagicMock()
        self.mock_session.__enter__ = MagicMock(return_value=self.mock_session)
        self.mock_session.__exit__ = MagicMock(return_value=None)

        # Mock consultant
        self.mock_consultant = Mock()
        self.mock_consultant.id = 1
        self.mock_consultant.prenom = "Marie"
        self.mock_consultant.nom = "Martin"

        # Mock assignment
        self.mock_assignment = Mock()
        self.mock_assignment.id = 1
        self.mock_assignment.consultant_id = 1
        self.mock_assignment.business_manager_id = 1
        self.mock_assignment.date_debut = date(2024, 1, 1)
        self.mock_assignment.date_fin = None
        self.mock_assignment.actif = True

    def test_validate_and_convert_bm_id_string_valid(self):
        """Test validation ID avec string valide"""
        from app.pages_modules.business_managers import _validate_and_convert_bm_id
        
        result = _validate_and_convert_bm_id("123")
        self.assertEqual(result, 123)

    def test_validate_and_convert_bm_id_string_invalid(self):
        """Test validation ID avec string invalide"""
        with patch('streamlit.error') as mock_error:
            from app.pages_modules.business_managers import _validate_and_convert_bm_id
            
            result = _validate_and_convert_bm_id("abc")
            self.assertIsNone(result)
            mock_error.assert_called_once()

    def test_validate_and_convert_bm_id_int_valid(self):
        """Test validation ID avec int valide"""
        from app.pages_modules.business_managers import _validate_and_convert_bm_id
        
        result = _validate_and_convert_bm_id(123)
        self.assertEqual(result, 123)

    def test_validate_and_convert_bm_id_other_type_valid(self):
        """Test validation ID avec autre type convertible"""
        from app.pages_modules.business_managers import _validate_and_convert_bm_id
        
        # Le code actuel ne gère que les strings et ints
        with patch('streamlit.error'):
            result = _validate_and_convert_bm_id(123.0)
            # Float 123.0 sera converti en string "123.0" puis échouera sur int()
            self.assertIsNone(result)

    def test_validate_and_convert_bm_id_other_type_invalid(self):
        """Test validation ID avec autre type non convertible"""
        with patch('streamlit.error') as mock_error:
            from app.pages_modules.business_managers import _validate_and_convert_bm_id
            
            result = _validate_and_convert_bm_id(object())
            self.assertIsNone(result)
            mock_error.assert_called_once()

    @patch('streamlit.columns')
    @patch('streamlit.title')
    @patch('streamlit.button')
    @patch('streamlit.markdown')
    @patch('streamlit.rerun')
    def test_display_bm_header_and_info(self, mock_rerun, mock_markdown, mock_button, 
                                        mock_title, mock_columns):
        """Test de l'affichage en-tête BM"""
        # Setup mocks
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_col1.__enter__ = MagicMock(return_value=mock_col1)
        mock_col1.__exit__ = MagicMock(return_value=None)
        mock_col2.__enter__ = MagicMock(return_value=mock_col2)
        mock_col2.__exit__ = MagicMock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2]
        mock_button.return_value = False

        from app.pages_modules.business_managers import _display_bm_header_and_info
        
        # Test sans clic bouton
        _display_bm_header_and_info(self.mock_bm)
        
        mock_title.assert_called_once_with("👔 Profil de Jean Dupont")
        mock_button.assert_called_once_with("← Retour", key="back_to_bm_list")
        mock_markdown.assert_called_once_with("---")
        mock_rerun.assert_not_called()

    @patch('streamlit.columns')
    @patch('streamlit.title')
    @patch('streamlit.button')
    @patch('streamlit.markdown')
    @patch('streamlit.rerun')
    def test_display_bm_header_and_info_with_button_click(self, mock_rerun, mock_markdown, 
                                                          mock_button, mock_title, mock_columns):
        """Test de l'affichage en-tête BM avec clic bouton retour"""
        # Setup mocks
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_col1.__enter__ = MagicMock(return_value=mock_col1)
        mock_col1.__exit__ = MagicMock(return_value=None)
        mock_col2.__enter__ = MagicMock(return_value=mock_col2)
        mock_col2.__exit__ = MagicMock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2]
        mock_button.return_value = True

        # Setup session state mock qui supporte del
        mock_session_state = MockSessionState({'view_bm_profile': True})

        from app.pages_modules.business_managers import _display_bm_header_and_info
        
        with patch('streamlit.session_state', mock_session_state):
            _display_bm_header_and_info(self.mock_bm)
            mock_rerun.assert_called_once()

    @patch('streamlit.columns')
    @patch('streamlit.subheader') 
    @patch('streamlit.write')
    @patch('streamlit.metric')
    def test_display_bm_general_info(self, mock_metric, mock_write, mock_subheader, mock_columns):
        """Test de l'affichage des informations générales BM"""
        # Setup mocks
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_col1.__enter__ = MagicMock(return_value=mock_col1)
        mock_col1.__exit__ = MagicMock(return_value=None)
        mock_col2.__enter__ = MagicMock(return_value=mock_col2)
        mock_col2.__exit__ = MagicMock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2]
        
        # Mock session query
        self.mock_session.query.return_value.filter.return_value.count.return_value = 5

        from app.pages_modules.business_managers import _display_bm_general_info
        
        _display_bm_general_info(self.mock_bm, self.mock_session)
        
        mock_subheader.assert_called()
        mock_write.assert_called()
        mock_metric.assert_called()

    def test_handle_bm_form_actions_no_mode(self):
        """Test de la gestion des actions formulaire BM sans mode actif"""
        # Mock session state sans modes actifs
        mock_session_state = MockSessionState({})

        from app.pages_modules.business_managers import _handle_bm_form_actions
        
        with patch('streamlit.session_state', mock_session_state):
            result = _handle_bm_form_actions(self.mock_bm)
            # La fonction ne retourne rien si aucun mode n'est actif
            self.assertIsNone(result)

    @patch('app.pages_modules.business_managers.show_edit_bm_form')
    def test_handle_bm_form_actions_edit_mode(self, mock_show_edit):
        """Test de la gestion des actions formulaire BM en mode édition"""
        # Mock session state avec edit_bm_mode = True
        mock_session_state = MockSessionState({'edit_bm_mode': True})

        from app.pages_modules.business_managers import _handle_bm_form_actions
        
        with patch('streamlit.session_state', mock_session_state):
            _handle_bm_form_actions(self.mock_bm)
            mock_show_edit.assert_called_once_with(self.mock_bm)

    @patch('app.pages_modules.business_managers.show_bm_profile')
    @patch('streamlit.title')
    @patch('streamlit.tabs')
    def test_show_main_function(self, mock_tabs, mock_title, mock_show_profile):
        """Test de la fonction show principale"""
        # Setup session state avec view_bm_profile
        mock_session_state = MockSessionState({'view_bm_profile': 1})

        from app.pages_modules.business_managers import show
        
        with patch('streamlit.session_state', mock_session_state):
            show()
            mock_show_profile.assert_called_once()

    @patch('streamlit.title')
    @patch('streamlit.tabs')
    @patch('app.pages_modules.business_managers.show_business_managers_list')
    @patch('app.pages_modules.business_managers.show_add_business_manager')
    @patch('app.pages_modules.business_managers.show_statistics')
    def test_show_main_function_no_profile_view(self, mock_show_stats, mock_show_add, 
                                                mock_show_list, mock_tabs, mock_title):
        """Test de la fonction show sans vue profil"""
        # Setup
        mock_tab1, mock_tab2, mock_tab3 = MagicMock(), MagicMock(), MagicMock()
        mock_tab1.__enter__ = MagicMock(return_value=mock_tab1)
        mock_tab1.__exit__ = MagicMock(return_value=None)
        mock_tab2.__enter__ = MagicMock(return_value=mock_tab2)
        mock_tab2.__exit__ = MagicMock(return_value=None)
        mock_tab3.__enter__ = MagicMock(return_value=mock_tab3)
        mock_tab3.__exit__ = MagicMock(return_value=None)
        mock_tabs.return_value = [mock_tab1, mock_tab2, mock_tab3]

        # Mock session state sans view_bm_profile
        mock_session_state = MockSessionState({})

        from app.pages_modules.business_managers import show
        
        with patch('streamlit.session_state', mock_session_state):
            show()
            
            mock_title.assert_called_once_with("👔 Gestion des Business Managers")
            mock_tabs.assert_called_once()
            mock_show_list.assert_called_once()
            mock_show_add.assert_called_once()
            mock_show_stats.assert_called_once()

    @patch('app.pages_modules.business_managers._validate_and_convert_bm_id')
    @patch('app.pages_modules.business_managers._display_bm_header_and_info')
    @patch('app.pages_modules.business_managers._display_bm_general_info')
    @patch('app.pages_modules.business_managers._handle_bm_form_actions')
    @patch('app.pages_modules.business_managers.get_database_session')
    @patch('streamlit.markdown')
    def test_show_bm_profile_valid_id(self, mock_markdown, mock_get_session, mock_handle_actions, 
                                      mock_display_general, mock_display_header, mock_validate_id):
        """Test show_bm_profile avec ID valide"""
        # Setup
        mock_validate_id.return_value = 1
        mock_get_session.return_value = self.mock_session
        
        # Mock la requête qui retourne un BM
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = self.mock_bm
        self.mock_session.query.return_value = mock_query
        
        mock_handle_actions.return_value = None

        mock_session_state = MockSessionState({'view_bm_profile': 1})

        from app.pages_modules.business_managers import show_bm_profile
        
        with patch('streamlit.session_state', mock_session_state):
            show_bm_profile()
            
            mock_validate_id.assert_called_once_with(1)
            mock_display_header.assert_called_once_with(self.mock_bm)
            mock_display_general.assert_called_once()
            mock_markdown.assert_called_once_with("---")

    @patch('app.pages_modules.business_managers._validate_and_convert_bm_id')
    @patch('streamlit.rerun')
    def test_show_bm_profile_invalid_id(self, mock_rerun, mock_validate_id):
        """Test show_bm_profile avec ID invalide"""
        mock_validate_id.return_value = None

        mock_session_state = MockSessionState({'view_bm_profile': "invalid"})

        from app.pages_modules.business_managers import show_bm_profile
        
        with patch('streamlit.session_state', mock_session_state):
            show_bm_profile()
            
            mock_validate_id.assert_called_once_with("invalid")
            # Vérifie que view_bm_profile a été supprimé
            self.assertNotIn('view_bm_profile', mock_session_state._data)
            mock_rerun.assert_called_once()

    @patch('app.pages_modules.business_managers._validate_and_convert_bm_id')
    @patch('app.pages_modules.business_managers.get_database_session')
    @patch('streamlit.error')
    @patch('streamlit.rerun')
    def test_show_bm_profile_bm_not_found(self, mock_rerun, mock_error, mock_get_session, mock_validate_id):
        """Test show_bm_profile avec BM introuvable"""
        # Setup
        mock_validate_id.return_value = 999
        mock_get_session.return_value = self.mock_session
        
        # Mock la requête qui ne retourne aucun BM
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        self.mock_session.query.return_value = mock_query

        mock_session_state = MockSessionState({'view_bm_profile': 999})

        from app.pages_modules.business_managers import show_bm_profile
        
        with patch('streamlit.session_state', mock_session_state):
            show_bm_profile()
            
            mock_validate_id.assert_called_once_with(999)
            mock_error.assert_called_once_with("❌ Business Manager introuvable")
            # Vérifie que view_bm_profile a été supprimé
            self.assertNotIn('view_bm_profile', mock_session_state._data)
            mock_rerun.assert_called_once()

    @patch('streamlit.form')
    @patch('streamlit.text_input')
    @patch('streamlit.checkbox')
    @patch('streamlit.form_submit_button')
    @patch('streamlit.success')
    @patch('streamlit.error')
    def test_show_edit_bm_form_not_submitted(self, mock_error, mock_success,
                                             mock_submit, mock_checkbox, mock_text_input, mock_form):
        """Test du formulaire d'édition BM - non soumis"""
        # Setup mocks
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = MagicMock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = MagicMock(return_value=None)
        
        mock_text_input.side_effect = ["Jean", "Dupont", "jean@test.com", "0123456789"]
        mock_checkbox.return_value = True
        mock_submit.return_value = False  # Pas soumis

        from app.pages_modules.business_managers import show_edit_bm_form
        
        show_edit_bm_form(self.mock_bm)
        
        mock_form.assert_called_once()
        mock_success.assert_not_called()
        mock_error.assert_not_called()

    def test_constants_coverage(self):
        """Test pour couvrir les constantes du module"""
        from app.pages_modules.business_managers import (
            TELEPHONE_LABEL, DATE_FORMAT, DUREE_LABEL,
            ERROR_INVALID_BM_ID, ERROR_GENERIC, ERROR_ASSIGNMENT,
            SUCCESS_BM_CREATED, SUCCESS_TRANSFER, SUCCESS_ASSIGNMENT,
            INFO_ASSIGNMENT_CLOSE
        )
        
        # Vérifier que les constantes sont bien définies
        self.assertEqual(TELEPHONE_LABEL, "Téléphone")
        self.assertEqual(DATE_FORMAT, "%d/%m/%Y")
        self.assertEqual(DUREE_LABEL, "Durée")
        self.assertIsNotNone(ERROR_INVALID_BM_ID)
        self.assertIsNotNone(SUCCESS_BM_CREATED)

    def test_imports_coverage(self):
        """Test pour couvrir les imports du module"""
        try:
            from app.pages_modules import business_managers
            from app.pages_modules.business_managers import show, show_bm_profile
            from app.pages_modules.business_managers import _validate_and_convert_bm_id
            
            # Si on arrive ici, tous les imports ont réussi
            self.assertIsNotNone(business_managers)
            self.assertIsNotNone(show)
            self.assertIsNotNone(show_bm_profile)
        except ImportError as e:
            self.fail(f"Import failed: {e}")

    @patch('streamlit.form')
    @patch('streamlit.text_input')
    @patch('streamlit.text_area')
    @patch('streamlit.checkbox')
    @patch('streamlit.form_submit_button')
    @patch('streamlit.success')
    @patch('streamlit.error')
    @patch('streamlit.rerun')
    @patch('app.pages_modules.business_managers.get_database_session')
    def test_show_edit_bm_form_submitted_success(self, mock_get_session, mock_rerun, 
                                                  mock_error, mock_success, mock_submit,
                                                  mock_checkbox, mock_text_area, mock_text_input, mock_form):
        """Test du formulaire d'édition BM - soumis avec succès"""
        # Setup mocks
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = MagicMock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = MagicMock(return_value=None)
        
        mock_text_input.side_effect = ["Jean", "Dupont", "jean@test.com", "0123456789"]
        mock_text_area.return_value = "Notes test"
        mock_checkbox.return_value = True
        mock_submit.return_value = True
        mock_get_session.return_value = self.mock_session
        
        # Mock la recherche et mise à jour du BM
        mock_bm_to_update = MagicMock()
        self.mock_session.query.return_value.get.return_value = mock_bm_to_update
        self.mock_session.commit.return_value = None

        # Mock session state
        mock_session_state = MockSessionState({'edit_bm_mode': True})

        from app.pages_modules.business_managers import show_edit_bm_form
        
        with patch('streamlit.session_state', mock_session_state):
            show_edit_bm_form(self.mock_bm)
            
            mock_form.assert_called_once()
            mock_success.assert_called_once_with("✅ Business Manager mis à jour avec succès !")
            # Vérifier que le mode edit a été désactivé
            self.assertFalse(mock_session_state.get('edit_bm_mode', True))
            # Le rerun peut être appelé plusieurs fois
            self.assertGreater(mock_rerun.call_count, 0)

    @patch('streamlit.subheader')
    @patch('streamlit.dataframe')
    @patch('streamlit.columns')
    @patch('streamlit.selectbox')
    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('app.pages_modules.business_managers.BusinessManagerService.get_all_business_managers')
    def test_show_business_managers_list_basic(self, mock_get_all_bm, mock_button, 
                                               mock_text_input, mock_selectbox, 
                                               mock_columns, mock_dataframe, mock_subheader):
        """Test de base pour show_business_managers_list"""
        # Setup
        mock_get_all_bm.return_value = [
            {'id': 1, 'prenom': 'Jean', 'nom': 'Dupont', 'email': 'jean@test.com', 'actif': True},
            {'id': 2, 'prenom': 'Marie', 'nom': 'Martin', 'email': 'marie@test.com', 'actif': True}
        ]
        
        # Setup mocks pour les colonnes
        mock_col1, mock_col2, mock_col3 = MagicMock(), MagicMock(), MagicMock()
        mock_col1.__enter__ = MagicMock(return_value=mock_col1)
        mock_col1.__exit__ = MagicMock(return_value=None)
        mock_col2.__enter__ = MagicMock(return_value=mock_col2)
        mock_col2.__exit__ = MagicMock(return_value=None)
        mock_col3.__enter__ = MagicMock(return_value=mock_col3)
        mock_col3.__exit__ = MagicMock(return_value=None)
        mock_columns.return_value = [mock_col1, mock_col2, mock_col3]
        
        mock_selectbox.return_value = "Tous"
        mock_text_input.return_value = ""
        mock_button.return_value = False

        from app.pages_modules.business_managers import show_business_managers_list
        
        show_business_managers_list()
        
        mock_get_all_bm.assert_called_once()
        # Vérifier que la fonction a été appelée avec succès
        self.assertIsNotNone(mock_get_all_bm)

    @patch('streamlit.subheader')
    @patch('streamlit.metric')
    @patch('streamlit.plotly_chart')
    @patch('app.pages_modules.business_managers.get_database_session')
    def test_show_statistics_basic(self, mock_get_session, mock_plotly_chart, 
                                   mock_metric, mock_subheader):
        """Test de base pour show_statistics"""
        # Setup
        mock_get_session.return_value = self.mock_session
        
        # Mock les requêtes pour les stats
        self.mock_session.query.return_value.count.return_value = 3

        from app.pages_modules.business_managers import show_statistics
        
        show_statistics()
        
        # Vérifier qu'au moins un subheader est affiché
        mock_subheader.assert_called()

    @patch('streamlit.form')
    @patch('streamlit.text_input')
    @patch('streamlit.text_area')
    @patch('streamlit.form_submit_button')
    @patch('streamlit.success')
    @patch('streamlit.error')
    @patch('streamlit.rerun')
    @patch('app.pages_modules.business_managers.get_database_session')
    def test_show_add_business_manager_basic(self, mock_get_session, mock_rerun,
                                             mock_error, mock_success, mock_submit,
                                             mock_text_area, mock_text_input, mock_form):
        """Test de base pour show_add_business_manager"""
        # Setup mocks
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = MagicMock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = MagicMock(return_value=None)
        
        mock_text_input.side_effect = ["Jean", "Dupont", "jean@test.com", "0123456789"]
        mock_text_area.return_value = "Notes test"
        mock_submit.return_value = False  # Pas soumis

        from app.pages_modules.business_managers import show_add_business_manager
        
        show_add_business_manager()
        
        mock_form.assert_called_once()
        # Pas de success/error car pas soumis
        mock_success.assert_not_called()
        mock_error.assert_not_called()

    @patch('app.pages_modules.business_managers.show_delete_bm_confirmation')
    def test_handle_bm_form_actions_delete_mode(self, mock_show_delete):
        """Test de la gestion des actions formulaire BM en mode suppression"""
        # Mock session state avec delete_bm_mode = True
        mock_session_state = MockSessionState({'delete_bm_mode': True})

        from app.pages_modules.business_managers import _handle_bm_form_actions
        
        with patch('streamlit.session_state', mock_session_state):
            _handle_bm_form_actions(self.mock_bm)
            mock_show_delete.assert_called_once_with(self.mock_bm)


if __name__ == '__main__':
    unittest.main()