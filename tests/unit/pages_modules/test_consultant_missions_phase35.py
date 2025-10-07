"""Tests unitaires pour consultant_missions.py - Phase 35"""
import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import date
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestDisplayMissionPeriod(unittest.TestCase):
    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_period_complete(self, mock_st):
        from app.pages_modules.consultant_missions import _display_mission_period
        mission = Mock(date_debut=date(2024,1,1), date_fin=date(2024,12,31), en_cours=False)
        _display_mission_period(mission)
        mock_st.markdown.assert_called()
    
    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_period_en_cours(self, mock_st):
        from app.pages_modules.consultant_missions import _display_mission_period
        mission = Mock(date_debut=date(2024,1,1), date_fin=None, en_cours=True)
        _display_mission_period(mission)
        mock_st.write.assert_called()

class TestDisplayMissionClient(unittest.TestCase):
    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_client_with_secteur(self, mock_st):
        from app.pages_modules.consultant_missions import _display_mission_client
        mission = Mock(client=Mock(nom="ClientA", secteur="Banque"))
        _display_mission_client(mission)
        self.assertEqual(mock_st.write.call_count, 2)
    
    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_client_no_secteur(self, mock_st):
        from app.pages_modules.consultant_missions import _display_mission_client
        mission = Mock(client=Mock(nom="ClientB", secteur=None))
        _display_mission_client(mission)
        mock_st.write.assert_called_once()

class TestDisplayMissionRemuneration(unittest.TestCase):
    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_remuneration_tjm(self, mock_st):
        from app.pages_modules.consultant_missions import _display_mission_remuneration
        mission = Mock(tjm=500, taux_journalier=None, salaire_mensuel=None)
        _display_mission_remuneration(mission)
        mock_st.markdown.assert_called()
    
    @patch("app.pages_modules.consultant_missions.st")
    def test_display_mission_remuneration_old_taux(self, mock_st):
        from app.pages_modules.consultant_missions import _display_mission_remuneration
        mission = Mock(tjm=None, taux_journalier=450, salaire_mensuel=5000)
        _display_mission_remuneration(mission)
        self.assertGreater(mock_st.write.call_count, 0)

class TestValidateMissionForm(unittest.TestCase):
    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_valid(self, mock_st):
        from app.pages_modules.consultant_missions import validate_mission_form
        result = validate_mission_form("Titre", 1, date(2024,1,1), False, date(2024,12,31))
        self.assertTrue(result)
    
    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_no_title(self, mock_st):
        from app.pages_modules.consultant_missions import validate_mission_form
        result = validate_mission_form("", 1, date(2024,1,1), True, None)
        self.assertFalse(result)
    
    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_no_client(self, mock_st):
        from app.pages_modules.consultant_missions import validate_mission_form
        result = validate_mission_form("Titre", None, date(2024,1,1), True, None)
        self.assertFalse(result)
    
    @patch("app.pages_modules.consultant_missions.st")
    def test_validate_mission_form_date_fin_before_debut(self, mock_st):
        from app.pages_modules.consultant_missions import validate_mission_form
        result = validate_mission_form("Titre", 1, date(2024,12,31), False, date(2024,1,1))
        self.assertFalse(result)

class TestCreateMission(unittest.TestCase):
    @patch("app.pages_modules.consultant_missions.get_database_session")
    @patch("app.pages_modules.consultant_missions.st")
    def test_create_mission_exception(self, mock_st, mock_get_session):
        from app.pages_modules.consultant_missions import create_mission
        mock_get_session.side_effect = Exception("DB error")
        result = create_mission(1, {})
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
