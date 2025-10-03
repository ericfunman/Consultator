"""
Tests unitaires pour le module consultants.py
Couvre les fonctions de base du module de gestion des consultants
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, date

# Import du module à tester
from app.pages_modules.consultants import (
    _display_consultant_header,
    _display_consultant_metrics,
    _show_consultant_not_found,
    _extract_business_manager_info,
    _get_current_practice_id,
    _build_update_data,
    _display_consultant_status,
)


class TestConsultants(unittest.TestCase):
    """Tests pour le module consultants"""

    def setUp(self):
        """Configuration des tests"""
        # Mock d'un consultant
        self.mock_consultant = MagicMock()
        self.mock_consultant.id = 1
        self.mock_consultant.prenom = "Jean"
        self.mock_consultant.nom = "DUPONT"
        self.mock_consultant.email = "jean.dupont@test.com"
        self.mock_consultant.telephone = "0123456789"
        self.mock_consultant.date_entree = date(2020, 1, 1)
        self.mock_consultant.societe = "Consultator"
        self.mock_consultant.actif = True
        self.mock_consultant.periode_essai_actif = False

        # Mock d'un business manager
        self.mock_business_manager = MagicMock()
        self.mock_business_manager.id = 1
        self.mock_business_manager.nom = "Manager"
        self.mock_business_manager.prenom = "Business"

        # Mock d'une practice
        self.mock_practice = MagicMock()
        self.mock_practice.id = 1
        self.mock_practice.nom = "Data Science"

        # Données de test pour les formulaires
        self.sample_form_data = {
            "prenom": "Pierre",
            "nom": "MARTIN",
            "email": "pierre.martin@test.com",
            "telephone": "0987654321",
            "societe": "NewCorp",
            "date_entree": date(2023, 1, 1),
            "date_sortie": None,
            "date_premiere_mission": None,
            "actif": True,
            "periode_essai_actif": False,
            "tjm_actuel": 500,
            "experience_avant_cgi": 3,
            "niveau_etude": "Master",
            "specialite": "Informatique",
            "salaire": 60000,
            "disponibilite": "Disponible",
            "notes": "Notes de test",
            "selected_practice_id": 1,
            "grade": "Senior",
            "type_contrat": "CDI",
        }

    @patch("app.pages_modules.consultants.st")
    def test_display_consultant_header(self, mock_st):
        """Test _display_consultant_header"""
        # Mock st.columns pour retourner 2 colonnes
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2]

        consultant_data = {
            "consultant": self.mock_consultant,
            "business_manager": self.mock_business_manager,
            "prenom": self.mock_consultant.prenom,
            "nom": self.mock_consultant.nom,
        }

        _display_consultant_header(consultant_data)

        # Vérifier que les informations sont affichées
        mock_st.title.assert_called()
        mock_st.columns.assert_called()

    @patch("app.pages_modules.consultants.st")
    def test_display_consultant_metrics(self, mock_st):
        """Test _display_consultant_metrics"""
        # Mock st.columns pour retourner 5 colonnes (comme attendu par la fonction)
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = MagicMock()
        mock_col5 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3, mock_col4, mock_col5]

        consultant_data = {
            "consultant": self.mock_consultant,
            "missions_count": 5,
            "competences_count": 10,
            "langues_count": 2,
            "salaire_actuel": 60000,
            "tjm_moyen": 500,
            "disponibilite": True,
            "date_creation": datetime.now(),
            "practice_name": "Data Science",
        }

        _display_consultant_metrics(consultant_data)

        # Vérifier que st.columns est appelé et que les métriques sont affichées
        mock_st.columns.assert_called()

    @patch("app.pages_modules.consultants.st")
    def test_show_consultant_not_found(self, mock_st):
        """Test _show_consultant_not_found"""
        _show_consultant_not_found()

        # Vérifier qu'un message d'erreur est affiché
        mock_st.error.assert_called()

    def test_extract_business_manager_info(self):
        """Test _extract_business_manager_info"""
        # Test avec business manager
        mock_consultant = MagicMock()
        mock_consultant.business_manager_actuel = self.mock_business_manager
        self.mock_business_manager.nom_complet = "Business Manager"
        self.mock_business_manager.email = "bm@test.com"

        nom_complet, email = _extract_business_manager_info(mock_consultant)

        self.assertEqual(nom_complet, "Business Manager")
        self.assertEqual(email, "bm@test.com")

        # Test sans business manager
        mock_consultant.business_manager_actuel = None
        nom_complet, email = _extract_business_manager_info(mock_consultant)

        self.assertIsNone(nom_complet)
        self.assertIsNone(email)

    def test_get_current_practice_id(self):
        """Test _get_current_practice_id"""
        # Test avec practice
        mock_consultant = MagicMock()
        mock_consultant.practice_id = 1

        result = _get_current_practice_id(mock_consultant)

        self.assertEqual(result, 1)

        # Test sans practice
        mock_consultant.practice_id = None
        result = _get_current_practice_id(mock_consultant)

        self.assertIsNone(result)

    def test_build_update_data(self):
        """Test _build_update_data"""
        result = _build_update_data(self.sample_form_data)

        # Vérifier que les données sont correctement transformées
        self.assertIn("prenom", result)
        self.assertIn("nom", result)
        self.assertIn("email", result)
        self.assertEqual(result["prenom"], "Pierre")
        self.assertEqual(result["nom"], "MARTIN")
        self.assertEqual(result["email"], "pierre.martin@test.com")

    @patch("app.pages_modules.consultants.st")
    def test_display_consultant_status_with_mission_date(self, mock_st):
        """Test _display_consultant_status avec date de première mission"""
        mock_consultant = MagicMock()
        mock_consultant.date_premiere_mission = date(2020, 1, 1)
        mock_consultant.experience_annees = 4

        _display_consultant_status(mock_consultant)

        # Vérifier que des informations sont affichées
        mock_st.markdown.assert_called()
        mock_st.info.assert_called()

    @patch("app.pages_modules.consultants.st")
    def test_display_consultant_status_without_mission_date(self, mock_st):
        """Test _display_consultant_status sans date de première mission"""
        mock_consultant = MagicMock()
        mock_consultant.date_premiere_mission = None

        _display_consultant_status(mock_consultant)

        # Vérifier que des informations sont affichées
        mock_st.markdown.assert_called()
        mock_st.info.assert_called()

    @patch("app.pages_modules.consultants.st")
    def test_display_consultant_status_calculation_error(self, mock_st):
        """Test _display_consultant_status avec erreur de calcul d'expérience"""
        mock_consultant = MagicMock()
        mock_consultant.date_premiere_mission = date(2020, 1, 1)
        # Simuler une erreur lors du calcul d'expérience
        mock_consultant.experience_annees.side_effect = AttributeError("Erreur")

        _display_consultant_status(mock_consultant)

        # Vérifier que des informations sont affichées malgré l'erreur
        mock_st.markdown.assert_called()
        mock_st.info.assert_called()


if __name__ == "__main__":
    unittest.main()
