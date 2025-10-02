"""
Tests unitaires pour consultants.py - Version optimisée pour la couverture
Tests simples et fonctionnels sans complexité excessive
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import date, datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))


class MockSessionState:
    """Mock de st.session_state simple"""
    def __init__(self):
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def __getitem__(self, key):
        return self.data.get(key)
    
    def __setitem__(self, key, value):
        self.data[key] = value


class TestConsultantsOptimizedCoverage(unittest.TestCase):
    """Tests optimisés pour la couverture maximale"""

    def setUp(self):
        """Setup des mocks communs"""
        self.mock_session_state = MockSessionState()
        self.mock_consultant = MagicMock()
        self.mock_consultant.date_entree = date(2022, 1, 1)
        self.mock_consultant.date_sortie = date(2023, 12, 31)
        self.mock_consultant.date_premiere_mission = date(2022, 1, 15)
        self.mock_consultant.id = 1
        self.mock_consultant.prenom = "Jean"
        self.mock_consultant.nom = "Dupont"
        self.mock_consultant.email = "jean.dupont@test.com"
        self.mock_consultant.telephone = "0123456789"
        self.mock_consultant.salaire_actuel = 50000
        self.mock_consultant.disponibilite = "Disponible"
        self.mock_consultant.notes = "Notes test"
        self.mock_consultant.practice_id = 1
        self.mock_consultant.business_manager_actuel = None
        
        # Mock column
        self.mock_col = MagicMock()
        self.mock_col.__enter__ = Mock(return_value=self.mock_col)
        self.mock_col.__exit__ = Mock(return_value=None)

    def test_build_update_data_complete(self):
        """Test _build_update_data avec toutes les données"""
        form_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@test.com",
            "telephone": "0123456789",
            "salaire": 55000,
            "disponibilite": "Disponible",
            "notes": "Notes test",
            "selected_practice_id": 1,
            "societe": "France",
            "date_entree": date.today(),
            "date_sortie": None,
            "date_premiere_mission": None,
            "grade": "Senior",
            "type_contrat": "CDI"
        }

        from app.pages_modules.consultants import _build_update_data
        result = _build_update_data(form_data)

        # Vérifications
        self.assertIsInstance(result, dict)
        self.assertEqual(result["prenom"], "Jean")
        self.assertEqual(result["nom"], "Dupont")
        self.assertEqual(result["email"], "jean.dupont@test.com")
        self.assertEqual(result["salaire_actuel"], 55000)

    @patch('app.pages_modules.consultants.st.columns')
    @patch('app.pages_modules.consultants.st.title')
    @patch('app.pages_modules.consultants.st.markdown')
    def test_display_consultant_header(self, mock_markdown, mock_title, mock_columns):
        """Test _display_consultant_header"""
        mock_columns.return_value = (self.mock_col, self.mock_col)
        consultant_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "practice_name": "Practice Test"
        }

        from app.pages_modules.consultants import _display_consultant_header
        _display_consultant_header(consultant_data)

        # Vérifications
        mock_columns.assert_called_once_with([6, 1])
        mock_title.assert_called()

    def test_extract_business_manager_info_with_manager(self):
        """Test _extract_business_manager_info avec business manager"""
        mock_bm = MagicMock()
        mock_bm.nom_complet = "Marie Martin"
        mock_bm.email = "marie.martin@test.com"
        self.mock_consultant.business_manager_actuel = mock_bm

        from app.pages_modules.consultants import _extract_business_manager_info
        result = _extract_business_manager_info(self.mock_consultant)

        # Vérifications
        self.assertIsNotNone(result)
        bm_nom_complet, bm_email = result
        self.assertEqual(bm_nom_complet, "Marie Martin")
        self.assertEqual(bm_email, "marie.martin@test.com")

    def test_extract_business_manager_info_without_manager(self):
        """Test _extract_business_manager_info sans business manager"""
        self.mock_consultant.business_manager_actuel = None

        from app.pages_modules.consultants import _extract_business_manager_info
        result = _extract_business_manager_info(self.mock_consultant)

        # Vérifications
        bm_nom_complet, bm_email = result
        self.assertIsNone(bm_nom_complet)
        self.assertIsNone(bm_email)

    def test_get_current_practice_id_with_practice(self):
        """Test _get_current_practice_id avec practice"""
        self.mock_consultant.practice_id = 5

        from app.pages_modules.consultants import _get_current_practice_id
        result = _get_current_practice_id(self.mock_consultant)

        # Vérifications
        self.assertEqual(result, 5)

    def test_get_current_practice_id_without_practice(self):
        """Test _get_current_practice_id sans practice"""
        delattr(self.mock_consultant, 'practice_id')

        from app.pages_modules.consultants import _get_current_practice_id
        result = _get_current_practice_id(self.mock_consultant)

        # Vérifications
        self.assertIsNone(result)

    def test_should_add_initial_salary_entry_true(self):
        """Test _should_add_initial_salary_entry retourne True"""
        mock_consultant = MagicMock()
        mock_consultant.salaire_actuel = 50000
        salaires = []

        from app.pages_modules.consultants import _should_add_initial_salary_entry
        result = _should_add_initial_salary_entry(mock_consultant, salaires)

        # Vérifications
        self.assertTrue(result)

    def test_should_add_initial_salary_entry_false_no_salary(self):
        """Test _should_add_initial_salary_entry retourne False sans salaire"""
        mock_consultant = MagicMock()
        mock_consultant.salaire_actuel = None
        salaires = []

        from app.pages_modules.consultants import _should_add_initial_salary_entry
        result = _should_add_initial_salary_entry(mock_consultant, salaires)

        # Vérifications
        self.assertFalse(result)

    @patch('app.pages_modules.consultants.st.date_input')
    def test_render_date_entree_field(self, mock_date):
        """Test _render_date_entree_field"""
        mock_date.return_value = date.today()
        # Mock consultant avec vraie date
        self.mock_consultant.date_entree = date(2022, 1, 1)

        from app.pages_modules.consultants import _render_date_entree_field
        result = _render_date_entree_field(self.mock_consultant)

        # Vérifications
        mock_date.assert_called()
        self.assertEqual(result, date.today())

    @patch('app.pages_modules.consultants.st.date_input')
    def test_render_date_sortie_field(self, mock_date):
        """Test _render_date_sortie_field"""
        mock_date.return_value = date.today()
        # Mock consultant avec vraie date
        self.mock_consultant.date_sortie = date(2023, 12, 31)

        from app.pages_modules.consultants import _render_date_sortie_field
        result = _render_date_sortie_field(self.mock_consultant)

        # Vérifications
        mock_date.assert_called()
        self.assertEqual(result, date.today())

    @patch('app.pages_modules.consultants.st.date_input')
    def test_render_date_premiere_mission_field(self, mock_date):
        """Test _render_date_premiere_mission_field"""
        mock_date.return_value = date.today()
        # Mock consultant avec vraie date
        self.mock_consultant.date_premiere_mission = date(2022, 1, 15)

        from app.pages_modules.consultants import _render_date_premiere_mission_field
        result = _render_date_premiere_mission_field(self.mock_consultant)

        # Vérifications
        mock_date.assert_called()
        self.assertEqual(result, date.today())

    @patch('app.pages_modules.consultants.st.selectbox')
    def test_render_societe_field(self, mock_select):
        """Test _render_societe_field"""
        mock_select.return_value = "France"

        from app.pages_modules.consultants import _render_societe_field
        result = _render_societe_field(self.mock_consultant)

        # Vérifications
        mock_select.assert_called()
        self.assertEqual(result, "France")

    def test_consultant_module_functions_exist(self):
        """Test que les principales fonctions du module existent"""
        from app.pages_modules import consultants
        
        # Test l'existence des fonctions principales
        required_functions = [
            '_build_update_data',
            '_extract_business_manager_info',
            '_get_current_practice_id',
            '_should_add_initial_salary_entry'
        ]
        
        for func_name in required_functions:
            self.assertTrue(hasattr(consultants, func_name), 
                          f"Fonction {func_name} manquante")


if __name__ == '__main__':
    unittest.main()