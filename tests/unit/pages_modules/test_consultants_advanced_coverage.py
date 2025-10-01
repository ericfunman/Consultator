"""
Tests d'amélioration de couverture pour le module consultants.py
Objectif: Améliorer de 19% vers 60%+ en ciblant les fonctions principales non couvertes
Focus: Fonctions avec le plus fort impact et facilité de test
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os
import pandas as pd
from datetime import datetime, date

# Ajouter le répertoire racine au path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)


class MockSessionState:
    """Mock de streamlit.session_state pour les tests"""
    def __init__(self):
        self._data = {}

    def __contains__(self, key):
        return key in self._data

    def __getattr__(self, key):
        if key == '_data':
            return super().__getattribute__(key)
        return self._data.get(key, MagicMock())

    def __setattr__(self, key, value):
        if key == '_data':
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def __delattr__(self, key):
        if key in self._data:
            del self._data[key]

    def get(self, key, default=None):
        return self._data.get(key, default)


class TestConsultantsModuleAdvancedCoverage(unittest.TestCase):
    """Tests avancés pour améliorer la couverture de consultants.py"""

    def setUp(self):
        """Setup pour chaque test"""
        self.mock_consultant = MagicMock()
        self.mock_consultant.id = 1
        self.mock_consultant.prenom = "Jean"
        self.mock_consultant.nom = "Dupont"
        self.mock_consultant.salaire_actuel = 50000
        self.mock_consultant.practice = MagicMock()
        self.mock_consultant.practice.nom = "Practice Test"

        self.mock_col = MagicMock()
        self.mock_col.__enter__ = MagicMock(return_value=self.mock_col)
        self.mock_col.__exit__ = MagicMock(return_value=None)

    @patch('app.pages_modules.consultants.get_database_session')
    def test_load_consultant_data_success(self, mock_get_session):
        """Test _load_consultant_data avec succès"""
        consultant_id = 1

        # Setup mock session et query
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.options.return_value.filter.return_value.first.return_value = self.mock_consultant

        from app.pages_modules.consultants import _load_consultant_data
        result = _load_consultant_data(consultant_id)

        # Vérifications
        mock_session.query.assert_called_once()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    @patch('app.pages_modules.consultants.get_database_session')
    def test_load_consultant_data_not_found(self, mock_get_session):
        """Test _load_consultant_data consultant non trouvé"""
        consultant_id = 999

        # Setup mock session et query
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.options.return_value.filter.return_value.first.return_value = None

        from app.pages_modules.consultants import _load_consultant_data
        result = _load_consultant_data(consultant_id)

        # Vérifications
        mock_session.query.assert_called_once()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (None, None))

    @patch('streamlit.columns')
    @patch('streamlit.button')
    @patch('streamlit.title')
    def test_display_consultant_header(self, mock_title, mock_button, mock_columns):
        """Test _display_consultant_header"""
        mock_columns.return_value = [self.mock_col, self.mock_col]
        mock_button.return_value = False
        consultant_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "practice_name": "Practice Test"
        }

        from app.pages_modules.consultants import _display_consultant_header
        _display_consultant_header(consultant_data)

        # Vérifications
        mock_columns.assert_called_once_with([6, 1])  # Corrigé: [6, 1] au lieu de [1, 3]
        mock_title.assert_called_once()
        mock_button.assert_called_once()

    @patch('streamlit.columns')
    @patch('streamlit.metric')
    def test_display_consultant_metrics(self, mock_metric, mock_columns):
        """Test _display_consultant_metrics"""
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col]
        consultant_data = {
            "salaire_actuel": 50000,
            "nb_missions": 5,
            "grade": "Senior"
        }

        from app.pages_modules.consultants import _display_consultant_metrics
        _display_consultant_metrics(consultant_data)

        # Vérifications
        mock_columns.assert_called_once_with(3)
        self.assertEqual(mock_metric.call_count, 3)

    def test_extract_business_manager_info_with_manager(self):
        """Test _extract_business_manager_info avec business manager"""
        mock_consultant = MagicMock()
        mock_consultant.business_manager = MagicMock()
        mock_consultant.business_manager.prenom = "Marie"
        mock_consultant.business_manager.nom = "Martin"

        from app.pages_modules.consultants import _extract_business_manager_info
        result = _extract_business_manager_info(mock_consultant)

        # Vérifications
        self.assertIsNotNone(result)
        self.assertEqual(result["prenom"], "Marie")
        self.assertEqual(result["nom"], "Martin")

    def test_extract_business_manager_info_without_manager(self):
        """Test _extract_business_manager_info sans business manager"""
        mock_consultant = MagicMock()
        mock_consultant.business_manager = None

        from app.pages_modules.consultants import _extract_business_manager_info
        result = _extract_business_manager_info(mock_consultant)

        # Vérifications
        self.assertIsNone(result)

    def test_get_current_practice_id_with_practice(self):
        """Test _get_current_practice_id avec practice"""
        mock_consultant = MagicMock()
        mock_consultant.practice_id = 5  # Corrigé: utilise practice_id directement

        from app.pages_modules.consultants import _get_current_practice_id
        result = _get_current_practice_id(mock_consultant)

        # Vérifications
        self.assertEqual(result, 5)

    def test_get_current_practice_id_without_practice(self):
        """Test _get_current_practice_id sans practice"""
        mock_consultant = MagicMock()
        # Simuler l'absence de practice_id
        mock_consultant.practice_id = None

        from app.pages_modules.consultants import _get_current_practice_id
        result = _get_current_practice_id(mock_consultant)

        # Vérifications
        self.assertIsNone(result)

    def test_build_update_data_complete(self):
        """Test _build_update_data avec toutes les données"""
        form_data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@test.com",
            "telephone": "0123456789",
            "salaire": 55000,  # Corrigé: "salaire" au lieu de "salaire_actuel"
            "grade": "Senior",
            "type_contrat": "CDI",
            "disponibilite": "Disponible",
            "notes": "Notes test",
            "selected_practice_id": 1,
            "societe": "Quanteam",
            "manager_id": 1,
            "entite": "Data",
            "teletravail": "Hybride",
            "date_entree": "2023-01-01",
            "date_premiere_mission": "2023-02-01",
            "date_sortie": None,
            "salaire_souhaite": 60000,
            "commentaires_rh": "Commentaires test",
            "date_derniere_augmentation": "2023-06-01",
            "commentaires_manager": "Commentaires manager",
            "seuil_vigilance": "Vert",
            "taux_prod_percent": 80,
            "statut_periode_essai": "Non",
            "periode_essai_active": False
        }

        from app.pages_modules.consultants import _build_update_data
        result = _build_update_data(form_data)

        # Vérifications
        self.assertIsInstance(result, dict)
        self.assertEqual(result["prenom"], "Jean")
        self.assertEqual(result["nom"], "Dupont")
        self.assertEqual(result["email"], "jean.dupont@test.com")
        self.assertEqual(result["salaire_actuel"], 55000)

    def test_build_update_data_partial(self):
        """Test _build_update_data avec données partielles"""
        form_data = {
            "prenom": "Jean",
            "nom": "Dupont"
        }

        from app.pages_modules.consultants import _build_update_data
        result = _build_update_data(form_data)

        # Vérifications
        self.assertIsInstance(result, dict)
        self.assertEqual(result["prenom"], "Jean")
        self.assertEqual(result["nom"], "Dupont")
        # Les autres champs ne doivent pas être présents
        self.assertNotIn("email", result)

    def test_should_add_initial_salary_entry_true(self):
        """Test _should_add_initial_salary_entry retourne True"""
        mock_consultant = MagicMock()
        mock_consultant.salaire_actuel = 50000
        salaires = []  # Aucun historique de salaire

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

    def test_should_add_initial_salary_entry_false_with_history(self):
        """Test _should_add_initial_salary_entry retourne False avec historique année courante"""
        from datetime import date
        mock_consultant = MagicMock()
        mock_consultant.salaire_actuel = 50000
        
        # Créer un mock de salaire pour l'année courante
        mock_salaire = MagicMock()
        mock_salaire.date_debut.year = date.today().year
        salaires = [mock_salaire]  # Historique pour l'année courante

        from app.pages_modules.consultants import _should_add_initial_salary_entry
        result = _should_add_initial_salary_entry(mock_consultant, salaires)

        # Vérifications
        self.assertFalse(result)

    @patch('streamlit.container')
    @patch('streamlit.columns')
    @patch('streamlit.text_input')
    @patch('streamlit.selectbox')
    @patch('streamlit.number_input')
    def test_render_basic_consultant_fields(self, mock_number, mock_select, mock_text, mock_columns, mock_container):
        """Test _render_basic_consultant_fields"""
        # Setup
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock()
        mock_columns.return_value = [self.mock_col, self.mock_col]
        mock_text.side_effect = ["Jean", "Dupont", "jean.dupont@test.com", "0123456789"]
        mock_select.side_effect = ["Senior", "CDI", "Disponible"]
        mock_number.return_value = 50000

        with patch('app.services.practice_service.PracticeService') as mock_practice_service:
            mock_practice_service.get_all_practices.return_value = []
            
            from app.pages_modules.consultants import _render_basic_consultant_fields
            result = _render_basic_consultant_fields(
                self.mock_consultant, 
                None,  # business_manager_data
                None   # current_practice_id
            )

            # Vérifications
            self.assertIsInstance(result, dict)
            self.assertIn("prenom", result)
            self.assertIn("nom", result)

    @patch('streamlit.date_input')
    @patch('streamlit.selectbox')  
    def test_render_company_history_fields(self, mock_select, mock_date):
        """Test _render_company_history_fields"""
        mock_select.return_value = "France"
        mock_date.return_value = date.today()

        from app.pages_modules.consultants import _render_company_history_fields
        result = _render_company_history_fields(self.mock_consultant)

        # Vérifications
        self.assertIsInstance(result, dict)
        mock_select.assert_called()
        mock_date.assert_called()

    @patch('streamlit.selectbox')
    def test_render_societe_field(self, mock_select):
        """Test _render_societe_field"""
        mock_select.return_value = "France"

        from app.pages_modules.consultants import _render_societe_field
        result = _render_societe_field(self.mock_consultant)

        # Vérifications
        self.assertEqual(result, "France")
        mock_select.assert_called_once()

    @patch('streamlit.date_input')
    def test_render_date_entree_field(self, mock_date):
        """Test _render_date_entree_field"""
        test_date = date.today()
        mock_date.return_value = test_date

        from app.pages_modules.consultants import _render_date_entree_field
        result = _render_date_entree_field(self.mock_consultant)

        # Vérifications
        self.assertEqual(result, test_date)
        mock_date.assert_called_once()

    @patch('streamlit.date_input')
    def test_render_date_sortie_field(self, mock_date):
        """Test _render_date_sortie_field"""
        test_date = date.today()
        mock_date.return_value = test_date

        from app.pages_modules.consultants import _render_date_sortie_field
        result = _render_date_sortie_field(self.mock_consultant)

        # Vérifications
        self.assertEqual(result, test_date)
        mock_date.assert_called_once()

    @patch('streamlit.date_input')
    def test_render_date_premiere_mission_field(self, mock_date):
        """Test _render_date_premiere_mission_field"""
        test_date = date.today()
        mock_date.return_value = test_date

        from app.pages_modules.consultants import _render_date_premiere_mission_field
        result = _render_date_premiere_mission_field(self.mock_consultant)

        # Vérifications
        self.assertEqual(result, test_date)
        mock_date.assert_called_once()

    @patch('streamlit.container')
    @patch('streamlit.text_area')
    def test_render_professional_profile_fields(self, mock_text_area, mock_container):
        """Test _render_professional_profile_fields"""
        mock_container.return_value.__enter__ = Mock()
        mock_container.return_value.__exit__ = Mock()
        mock_text_area.side_effect = ["Formation", "Expérience", "Certifications"]

        from app.pages_modules.consultants import _render_professional_profile_fields
        result = _render_professional_profile_fields(self.mock_consultant)

        # Vérifications
        self.assertIsInstance(result, dict)
        self.assertEqual(mock_text_area.call_count, 3)

    @patch('streamlit.expander')
    @patch('streamlit.markdown')
    def test_display_consultant_status(self, mock_markdown, mock_expander):
        """Test _display_consultant_status"""
        mock_expander.return_value.__enter__ = Mock()
        mock_expander.return_value.__exit__ = Mock()

        from app.pages_modules.consultants import _display_consultant_status
        _display_consultant_status(self.mock_consultant)

        # Vérifications
        mock_expander.assert_called()
        mock_markdown.assert_called()

    @patch('streamlit.columns')
    @patch('streamlit.metric')
    def test_display_functional_skills_metrics(self, mock_metric, mock_columns):
        """Test _display_functional_skills_metrics"""
        mock_columns.return_value = [self.mock_col, self.mock_col]
        competences_func = [MagicMock(), MagicMock(), MagicMock()]

        from app.pages_modules.consultants import _display_functional_skills_metrics
        _display_functional_skills_metrics(competences_func)

        # Vérifications
        mock_columns.assert_called_once_with(2)
        self.assertEqual(mock_metric.call_count, 2)

    @patch('streamlit.info')
    def test_display_no_functional_skills_message(self, mock_info):
        """Test _display_no_functional_skills_message"""
        from app.pages_modules.consultants import _display_no_functional_skills_message
        _display_no_functional_skills_message()

        # Vérifications
        mock_info.assert_called_once()

    def test_group_functional_skills_by_category(self):
        """Test _group_functional_skills_by_category"""
        # Mock competences avec différentes catégories
        comp1 = MagicMock()
        comp1.competence_fonctionnelle.nom = "Gestion projet"
        comp1.competence_fonctionnelle.categorie = "Management"
        
        comp2 = MagicMock()
        comp2.competence_fonctionnelle.nom = "Analyse business"
        comp2.competence_fonctionnelle.categorie = "Analyse"
        
        comp3 = MagicMock()
        comp3.competence_fonctionnelle.nom = "Leadership"
        comp3.competence_fonctionnelle.categorie = "Management"
        
        competences_func = [comp1, comp2, comp3]

        from app.pages_modules.consultants import _group_functional_skills_by_category
        result = _group_functional_skills_by_category(competences_func)

        # Vérifications
        self.assertIsInstance(result, dict)
        self.assertIn("Management", result)
        self.assertIn("Analyse", result)
        self.assertEqual(len(result["Management"]), 2)
        self.assertEqual(len(result["Analyse"]), 1)

    @patch('streamlit.form')
    @patch('streamlit.selectbox')
    @patch('streamlit.slider')
    @patch('streamlit.form_submit_button')
    @patch('streamlit.success')
    def test_add_technical_skill_form_success(self, mock_success, mock_submit, mock_slider, mock_select, mock_form):
        """Test _add_technical_skill_form avec succès"""
        # Setup
        mock_form.return_value.__enter__ = Mock()
        mock_form.return_value.__exit__ = Mock()
        mock_select.return_value = "Python"
        mock_slider.return_value = 3
        mock_submit.return_value = True

        with patch('app.services.consultant_service.ConsultantService') as mock_service, \
             patch('app.services.technology_service.TechnologyService') as mock_tech_service:
            
            mock_tech_service.get_all_technologies.return_value = []
            mock_service.add_technical_skill_to_consultant.return_value = True

            from app.pages_modules.consultants import _add_technical_skill_form
            _add_technical_skill_form(self.mock_consultant)

            # Vérifications
            mock_form.assert_called()
            mock_submit.assert_called_once()
            mock_success.assert_called_once()

    @patch('streamlit.form')
    @patch('streamlit.selectbox')
    @patch('streamlit.slider')
    @patch('streamlit.form_submit_button')
    def test_add_technical_skill_form_no_submit(self, mock_submit, mock_slider, mock_select, mock_form):
        """Test _add_technical_skill_form sans soumission"""
        # Setup
        mock_form.return_value.__enter__ = Mock()
        mock_form.return_value.__exit__ = Mock()
        mock_select.return_value = "Python"
        mock_slider.return_value = 3
        mock_submit.return_value = False

        with patch('app.services.technology_service.TechnologyService') as mock_tech_service:
            mock_tech_service.get_all_technologies.return_value = []

            from app.pages_modules.consultants import _add_technical_skill_form
            _add_technical_skill_form(self.mock_consultant)

            # Vérifications
            mock_form.assert_called()
            mock_submit.assert_called_once()

    @patch('streamlit.form')
    @patch('streamlit.selectbox')
    @patch('streamlit.slider')
    @patch('streamlit.form_submit_button')
    @patch('streamlit.success')
    def test_add_functional_skill_form_success(self, mock_success, mock_submit, mock_slider, mock_select, mock_form):
        """Test _add_functional_skill_form avec succès"""
        # Setup
        mock_form.return_value.__enter__ = Mock()
        mock_form.return_value.__exit__ = Mock()
        mock_select.return_value = "Gestion projet"
        mock_slider.return_value = 4
        mock_submit.return_value = True

        with patch('app.services.consultant_service.ConsultantService') as mock_service:
            mock_service.get_functional_skills.return_value = []
            mock_service.add_functional_skill_to_consultant.return_value = True

            from app.pages_modules.consultants import _add_functional_skill_form
            _add_functional_skill_form(self.mock_consultant)

            # Vérifications
            mock_form.assert_called()
            mock_submit.assert_called_once()
            mock_success.assert_called_once()


if __name__ == '__main__':
    unittest.main()