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
        mock_columns.return_value = [self.mock_col, self.mock_col, self.mock_col, self.mock_col, self.mock_col]  # Corrigé: 5 colonnes
        consultant_data = {
            "salaire_actuel": 50000,
            "nb_missions": 5,
            "grade": "Senior",
            "disponibilite": "Disponible",  # Ajouté: requis par la fonction
            "date_creation": datetime.now(),  # Ajouté: requis par la fonction
            "practice_name": "Practice Test"  # Ajouté: requis par la fonction
        }

        from app.pages_modules.consultants import _display_consultant_metrics
        _display_consultant_metrics(consultant_data)

        # Vérifications
        mock_columns.assert_called_once_with(5)  # Corrigé: la fonction utilise 5 colonnes
        mock_metric.assert_called()

    def test_extract_business_manager_info_with_manager(self):
        """Test _extract_business_manager_info avec business manager"""
        mock_consultant = MagicMock()
        mock_bm = MagicMock()
        mock_bm.nom_complet = "Marie Martin"
        mock_bm.email = "marie.martin@test.com"
        mock_consultant.business_manager_actuel = mock_bm  # Corrigé: business_manager_actuel

        from app.pages_modules.consultants import _extract_business_manager_info
        result = _extract_business_manager_info(mock_consultant)

        # Vérifications - la fonction retourne un tuple (nom_complet, email)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Marie Martin")  # nom_complet
        self.assertEqual(result[1], "marie.martin@test.com")  # email

    def test_extract_business_manager_info_without_manager(self):
        """Test _extract_business_manager_info sans business manager"""
        mock_consultant = MagicMock()
        mock_consultant.business_manager_actuel = None  # Corrigé: business_manager_actuel

        from app.pages_modules.consultants import _extract_business_manager_info
        result = _extract_business_manager_info(mock_consultant)

        # Vérifications - la fonction retourne un tuple (None, None)
        self.assertIsNotNone(result)  # Le tuple existe
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

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
            "nom": "Dupont",
            "email": "jean.dupont@test.com",  # Ajouté: requis par la fonction
            "telephone": "",
            "salaire": 0,
            "disponibilite": "Disponible",
            "notes": "",
            "selected_practice_id": None,
            "societe": "Quanteam",
            "manager_id": None,
            "entite": "",
            "teletravail": "Non",
            "date_entree": None,
            "date_premiere_mission": None,
            "date_sortie": None,
            "salaire_souhaite": None,
            "commentaires_rh": "",
            "date_derniere_augmentation": None,
            "commentaires_manager": "",
            "seuil_vigilance": "Vert",
            "taux_prod_percent": 0,
            "statut_periode_essai": "Non",
            "periode_essai_active": False,
            "grade": "",
            "type_contrat": ""
        }

        from app.pages_modules.consultants import _build_update_data
        result = _build_update_data(form_data)

        # Vérifications
        self.assertIsInstance(result, dict)
        self.assertEqual(result["prenom"], "Jean")
        self.assertEqual(result["nom"], "Dupont")
        # Les champs vides doivent être traités correctement
        self.assertEqual(result["email"], "jean.dupont@test.com")

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

    @patch('app.pages_modules.consultants.st')
    def test_render_basic_consultant_fields(self, mock_st):
        """Test de la fonction _render_basic_consultant_fields"""
        # Données de test
        mock_consultant = MagicMock()
        mock_consultant.prenom = "Jean"
        mock_consultant.nom = "Dupont"
        mock_consultant.email = "jean.dupont@test.com"
        mock_consultant.telephone = "0123456789"
        mock_consultant.salaire_actuel = 50000
        mock_consultant.disponibilite = True
        
        practice_options = {"Practice 1": 1, "Practice 2": 2}
        current_practice_id = 1
        bm_nom_complet = "Manager Test"
        bm_email = "manager@test.com"
        
        # Configuration des mocks
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        # 5 appels st.text_input : prenom, email, BM, nom, telephone
        mock_st.text_input.side_effect = ["Jean", "jean.dupont@test.com", "Manager Test (manager@test.com)", "Dupont", "0123456789"]
        mock_st.number_input.return_value = 50000
        mock_st.info.return_value = None
        mock_st.selectbox.return_value = "Practice 1"
        mock_st.checkbox.return_value = True
        
        # Test
        from app.pages_modules.consultants import _render_basic_consultant_fields
        result = _render_basic_consultant_fields(
            mock_consultant,
            practice_options,
            current_practice_id,
            bm_nom_complet,
            bm_email
        )
        
        # Vérifications
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 7)
        self.assertEqual(result[0], "Jean")  # prenom
        self.assertEqual(result[1], "Dupont")  # nom  
        self.assertEqual(result[2], "jean.dupont@test.com")  # email
        self.assertEqual(result[3], "0123456789")  # telephone
        self.assertEqual(result[4], 50000)  # salaire
        self.assertEqual(result[5], True)  # disponibilite
        self.assertEqual(result[6], 1)  # selected_practice_id
        
        # Vérifier les appels
        mock_st.columns.assert_called_once_with(2)
        self.assertEqual(mock_st.text_input.call_count, 5)
        mock_st.number_input.assert_called_once()
        mock_st.selectbox.assert_called_once()
        mock_st.checkbox.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_render_company_history_fields(self, mock_st):
        """Test _render_company_history_fields"""
        # Setup des mocks
        mock_st.markdown.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.selectbox.return_value = "Quanteam"
        mock_st.date_input.side_effect = [date.today(), date.today(), date.today()]
        
        from app.pages_modules.consultants import _render_company_history_fields
        result = _render_company_history_fields(self.mock_consultant)

        # Vérifications
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], "Quanteam")  # societe
        # Les 3 autres éléments sont des dates
        for i in range(1, 4):
            self.assertIsInstance(result[i], date)
        
        # Vérifier les appels
        mock_st.columns.assert_called_once_with(2)
        mock_st.selectbox.assert_called_once()
        self.assertEqual(mock_st.date_input.call_count, 3)

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

    @patch('app.pages_modules.consultants.st')
    def test_render_professional_profile_fields(self, mock_st):
        """Test _render_professional_profile_fields"""
        # Setup des mocks
        mock_st.markdown.return_value = None
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.selectbox.side_effect = ["Junior", "CDI"]
        
        from app.pages_modules.consultants import _render_professional_profile_fields
        result = _render_professional_profile_fields(self.mock_consultant)

        # Vérifications
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Junior")  # grade
        self.assertEqual(result[1], "CDI")     # type_contrat
        
        # Vérifier les appels
        mock_st.columns.assert_called_once_with(2)
        self.assertEqual(mock_st.selectbox.call_count, 2)

    @patch('app.pages_modules.consultants.st')
    def test_display_consultant_status(self, mock_st):
        """Test _display_consultant_status"""
        # Setup du mock consultant avec date_premiere_mission
        self.mock_consultant.date_premiere_mission = date.today()
        self.mock_consultant.experience_annees = 5
        
        # Setup des mocks
        mock_st.markdown.return_value = None
        mock_st.info.return_value = None
        
        from app.pages_modules.consultants import _display_consultant_status
        _display_consultant_status(self.mock_consultant)
        
        # Vérifications
        mock_st.markdown.assert_called_once_with("---")
        mock_st.info.assert_called_once()
        
        # Vérifier le contenu du message
        call_args = mock_st.info.call_args[0][0]
        self.assertIn("Expérience calculée", call_args)
        self.assertIn("5 années", call_args)

    @patch('app.pages_modules.consultants.st')
    def test_display_functional_skills_metrics(self, mock_st):
        """Test _display_functional_skills_metrics"""
        # Données de test
        competences_func = [
            MagicMock(),
            MagicMock(),
            MagicMock()
        ]
        
        # Setup des mocks
        mock_st.metric.return_value = None
        
        from app.pages_modules.consultants import _display_functional_skills_metrics
        _display_functional_skills_metrics(competences_func)
        
        # Vérifications
        mock_st.metric.assert_called_once_with("🏦 Total compétences fonctionnelles", 3)

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
        mock_competence1 = MagicMock()
        mock_competence1.nom = "Gestion projet"
        mock_competence1.categorie = "Management"
        
        mock_competence2 = MagicMock()
        mock_competence2.nom = "Analyse business"
        mock_competence2.categorie = "Analyse"
        
        mock_competence3 = MagicMock()
        mock_competence3.nom = "Leadership"
        mock_competence3.categorie = "Management"
        
        mock_consultant_comp1 = MagicMock()
        mock_consultant_comp2 = MagicMock()
        mock_consultant_comp3 = MagicMock()
        
        # La fonction attend des tuples (consultant_comp, competence)
        competences_func = [
            (mock_consultant_comp1, mock_competence1),
            (mock_consultant_comp2, mock_competence2),
            (mock_consultant_comp3, mock_competence3)
        ]

        from app.pages_modules.consultants import _group_functional_skills_by_category
        result = _group_functional_skills_by_category(competences_func)

        # Vérifications
        self.assertIsInstance(result, dict)
        self.assertIn("Management", result)
        self.assertIn("Analyse", result)
        self.assertEqual(len(result["Management"]), 2)
        self.assertEqual(len(result["Analyse"]), 1)

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants._save_consultant_competence')
    def test_add_technical_skill_form_success(self, mock_save, mock_st):
        """Test _add_technical_skill_form avec soumission réussie"""
        # Setup des mocks - utiliser vraies catégories
        mock_st.selectbox.side_effect = ["Backend", "Python", "Confirmé"]
        mock_st.number_input.return_value = 3
        mock_st.text_input.return_value = "Certification Python"
        mock_st.text_area.return_value = "Projets Python"
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.form_submit_button.return_value = True
        mock_st.success.return_value = None
        mock_st.error.return_value = None
        mock_save.return_value = None
        
        from app.pages_modules.consultants import _add_technical_skill_form
        _add_technical_skill_form(self.mock_consultant)
        
        # Vérifications
        self.assertEqual(mock_st.selectbox.call_count, 3)  # catégorie + compétence + niveau
        mock_st.number_input.assert_called_once()
        mock_st.form_submit_button.assert_called_once()
        mock_save.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    def test_add_technical_skill_form_no_submit(self, mock_st):
        """Test _add_technical_skill_form sans soumission"""
        # Setup des mocks - utiliser vraies catégories
        mock_st.selectbox.side_effect = ["Backend", "Python", "Confirmé"]
        mock_st.number_input.return_value = 3
        mock_st.text_input.return_value = "Certification Python"
        mock_st.text_area.return_value = "Projets Python"
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.form_submit_button.return_value = False  # Pas de soumission
        
        from app.pages_modules.consultants import _add_technical_skill_form
        _add_technical_skill_form(self.mock_consultant)
        
        # Vérifications
        self.assertEqual(mock_st.selectbox.call_count, 3)  # catégorie + compétence + niveau
        mock_st.number_input.assert_called_once()
        mock_st.form_submit_button.assert_called_once()

    @patch('app.pages_modules.consultants.st')
    @patch('app.pages_modules.consultants._save_consultant_competence')
    def test_add_functional_skill_form_success(self, mock_save, mock_st):
        """Test _add_functional_skill_form avec soumission réussie"""
        # Setup des mocks
        mock_st.selectbox.side_effect = ["Banque de Détail", "Conseil clientèle particuliers", "Confirmé"]
        mock_st.number_input.return_value = 3
        mock_st.text_input.return_value = "Certification test"
        mock_st.text_area.return_value = "Projets test"
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.form_submit_button.return_value = True
        mock_st.success.return_value = None
        mock_st.error.return_value = None
        mock_save.return_value = None
        
        from app.pages_modules.consultants import _add_functional_skill_form
        _add_functional_skill_form(self.mock_consultant)
        
        # Vérifications
        self.assertEqual(mock_st.selectbox.call_count, 3)  # catégorie + compétence + niveau
        mock_st.number_input.assert_called_once()
        mock_st.form_submit_button.assert_called_once()
        mock_save.assert_called_once()


if __name__ == '__main__':
    unittest.main()