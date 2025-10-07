"""
Tests unitaires pour le module consultant_info.py - Phase 26
Coverage target: 77.3% → 85%+ (gain estimé +7-8%)

Stratégie:
- Fonctions de calcul et traitement de données (70% du module)
- Fonctions d'affichage secondaires avec peu de Streamlit
- Validation des formulaires
- Génération de rapports

Fonctions clés à tester:
- _calculate_availability_status (logique métier)
- _display_identity_info, _display_affectation_info, _display_financial_info
- _display_vsa_missions, _display_vsa_missions_stats, _display_vsa_missions_table
- validate_info_form (validation pure)
- update_consultant_info (CRUD avec DB)
- generate_consultant_report (génération de contenu)
- show_salary_history, show_detailed_salary_history
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open
from datetime import datetime, date, timedelta
import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestCalculateAvailabilityStatus(unittest.TestCase):
    """Tests pour _calculate_availability_status"""

    def setUp(self):
        from app.pages_modules.consultant_info import _calculate_availability_status

        self.func = _calculate_availability_status

    def test_no_missions_available(self):
        """Test consultant sans missions = disponible"""
        consultant = Mock(missions=[])
        result = self.func(consultant)
        self.assertEqual(result, "✅ Disponible")

    def test_all_past_missions_available(self):
        """Test toutes missions passées = disponible"""
        past_mission = Mock(date_fin=date.today() - timedelta(days=10))
        consultant = Mock(missions=[past_mission])
        result = self.func(consultant)
        self.assertEqual(result, "✅ Disponible")

    def test_mission_ending_today_available(self):
        """Test mission se terminant aujourd'hui = disponible"""
        today_mission = Mock(date_fin=date.today())
        consultant = Mock(missions=[today_mission])
        result = self.func(consultant)
        self.assertIn("Disponible", result)

    def test_mission_ending_soon_days_countdown(self):
        """Test mission se terminant bientôt = compte à rebours"""
        future_mission = Mock(date_fin=date.today() + timedelta(days=30))
        consultant = Mock(missions=[future_mission])
        result = self.func(consultant)
        self.assertIn("30 jours", result)

    def test_mission_ending_far_future_unavailable(self):
        """Test mission lointaine = non disponible"""
        far_future_mission = Mock(date_fin=date.today() + timedelta(days=180))
        consultant = Mock(missions=[far_future_mission])
        result = self.func(consultant)
        self.assertEqual(result, "❌ Non disponible")

    def test_multiple_missions_latest_end_date(self):
        """Test multiples missions = prend la date la plus lointaine"""
        mission1 = Mock(date_fin=date.today() + timedelta(days=30))
        mission2 = Mock(date_fin=date.today() + timedelta(days=60))
        mission3 = Mock(date_fin=date.today() - timedelta(days=10))
        consultant = Mock(missions=[mission1, mission2, mission3])
        result = self.func(consultant)
        self.assertIn("60 jours", result)

    def test_mission_with_none_date_fin_ignored(self):
        """Test missions avec date_fin None = ignorées"""
        mission_none = Mock(date_fin=None)
        consultant = Mock(missions=[mission_none])
        result = self.func(consultant)
        self.assertEqual(result, "✅ Disponible")


class TestDisplayIdentityInfo(unittest.TestCase):
    """Tests pour _display_identity_info"""

    @patch("app.pages_modules.consultant_info.st")
    def test_display_identity_info_full(self, mock_st):
        """Test affichage identité complète"""
        from app.pages_modules.consultant_info import _display_identity_info

        consultant = Mock(prenom="Jean", nom="Dupont", email="jean.dupont@test.com", telephone="0123456789")

        _display_identity_info(consultant)

        # Vérifier les appels
        mock_st.markdown.assert_called()
        self.assertGreaterEqual(mock_st.write.call_count, 3)

    @patch("app.pages_modules.consultant_info.st")
    def test_display_identity_info_no_phone(self, mock_st):
        """Test affichage identité sans téléphone"""
        from app.pages_modules.consultant_info import _display_identity_info

        consultant = Mock(prenom="Marie", nom="Martin", email="marie@test.com", telephone=None)

        _display_identity_info(consultant)

        mock_st.markdown.assert_called()
        # Téléphone non affiché si None


class TestDisplayAffectationInfo(unittest.TestCase):
    """Tests pour _display_affectation_info"""

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info._calculate_availability_status")
    def test_display_affectation_with_practice(self, mock_calc_status, mock_st):
        """Test affichage affectation avec practice"""
        from app.pages_modules.consultant_info import _display_affectation_info

        mock_calc_status.return_value = "✅ Disponible"

        # Mock st.columns pour retourner des colonnes mockées
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = MagicMock()
        mock_st.columns.side_effect = [[mock_col1, mock_col2], [mock_col3, mock_col4]]

        practice = Mock(nom="Data")
        consultant = Mock(
            practice=practice,
            entite="Paris",
            type_contrat="CDI",
            etat_periode_essai="Validée",
            fin_periode_essai=date(2024, 12, 31),
            actif=True,
            statut_societe="En poste",
            date_creation=date(2024, 1, 1),
            missions=[],
        )

        _display_affectation_info(consultant)

        mock_st.markdown.assert_called()
        mock_calc_status.assert_called_once_with(consultant)

    @patch("app.pages_modules.consultant_info.st")
    @patch("app.pages_modules.consultant_info._calculate_availability_status")
    def test_display_affectation_no_practice(self, mock_calc_status, mock_st):
        """Test affichage affectation sans practice"""
        from app.pages_modules.consultant_info import _display_affectation_info

        mock_calc_status.return_value = "✅ Disponible"

        # Mock st.columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_col4 = MagicMock()
        mock_st.columns.side_effect = [[mock_col1, mock_col2], [mock_col3, mock_col4]]

        consultant = Mock(
            practice=None,
            entite="Lyon",
            type_contrat="Freelance",
            actif=False,
            statut_societe="Départ prévu",
            date_creation=None,
            missions=[],
        )

        _display_affectation_info(consultant)

        mock_st.markdown.assert_called()


class TestDisplayFinancialInfo(unittest.TestCase):
    """Tests pour _display_financial_info"""

    @patch("app.pages_modules.consultant_info.st")
    def test_display_financial_info_with_salary(self, mock_st):
        """Test affichage infos financières avec salaire"""
        from app.pages_modules.consultant_info import _display_financial_info

        # Mock st.columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        consultant = Mock(salaire_actuel=50000)

        _display_financial_info(consultant)

        mock_st.markdown.assert_called()
        # 3 métriques: salaire, CJM, TJM
        self.assertEqual(mock_st.metric.call_count, 3)

    @patch("app.pages_modules.consultant_info.st")
    def test_display_financial_info_no_salary(self, mock_st):
        """Test affichage infos financières sans salaire"""
        from app.pages_modules.consultant_info import _display_financial_info

        # Mock st.columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        consultant = Mock(salaire_actuel=None)

        _display_financial_info(consultant)

        mock_st.markdown.assert_called()
        self.assertEqual(mock_st.metric.call_count, 3)


class TestDisplayNotesSection(unittest.TestCase):
    """Tests pour _display_notes_section"""

    @patch("app.pages_modules.consultant_info.st")
    def test_display_notes_with_content(self, mock_st):
        """Test affichage notes avec contenu"""
        from app.pages_modules.consultant_info import _display_notes_section

        consultant = Mock(id=1, notes="Excellent consultant Python")

        _display_notes_section(consultant)

        mock_st.markdown.assert_called()
        mock_st.text_area.assert_called_once()

    @patch("app.pages_modules.consultant_info.st")
    def test_display_notes_no_content(self, mock_st):
        """Test affichage notes sans contenu = rien affiché"""
        from app.pages_modules.consultant_info import _display_notes_section

        consultant = Mock(id=2, notes=None)

        _display_notes_section(consultant)

        # Rien ne devrait être affiché
        mock_st.markdown.assert_not_called()
        mock_st.text_area.assert_not_called()


class TestDisplayVsaMissions(unittest.TestCase):
    """Tests pour _display_vsa_missions"""

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_display_vsa_missions_external(self, mock_st, mock_session):
        """Test affichage missions VSA externes (filtre décoché)"""
        from app.pages_modules.consultant_info import _display_vsa_missions
        from database.models import VsaMission

        # Mock session et données
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        mission1 = Mock(code="PROJ001", est_active=True, tjm=500, cjm=400, orderid="CMD001", client_name="Client A", date_debut=date(2024, 1, 1), date_fin=date(2024, 12, 31), duree_jours=200)
        mission2 = Mock(code="INT002", est_active=False, tjm=0, cjm=0, orderid="CMD002", client_name="Interne", date_debut=date(2024, 1, 1), date_fin=None, duree_jours=None)

        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [mission1, mission2]

        # Simuler checkbox décochée (missions externes)
        mock_st.checkbox.return_value = False

        consultant = Mock(id=1)

        _display_vsa_missions(consultant)

        mock_st.markdown.assert_called()
        mock_st.checkbox.assert_called_once()
        # Filtrage externe = 1 mission PROJ001

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_display_vsa_missions_internal(self, mock_st, mock_session):
        """Test affichage missions VSA internes (filtre coché)"""
        from app.pages_modules.consultant_info import _display_vsa_missions

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        mission = Mock(code="INT001", est_active=True)
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [mission]

        # Simuler checkbox cochée (missions internes)
        mock_st.checkbox.return_value = True

        consultant = Mock(id=2)

        _display_vsa_missions(consultant)

        mock_st.checkbox.assert_called_once()


class TestDisplayVsaMissionsStats(unittest.TestCase):
    """Tests pour _display_vsa_missions_stats"""

    @patch("app.pages_modules.consultant_info.st")
    def test_display_vsa_missions_stats(self, mock_st):
        """Test affichage stats missions VSA"""
        from app.pages_modules.consultant_info import _display_vsa_missions_stats

        # Mock st.columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        missions = [
            Mock(est_active=True, tjm=500),
            Mock(est_active=True, tjm=600),
            Mock(est_active=False, tjm=None),
        ]

        _display_vsa_missions_stats(missions)

        # 3 métriques: total, actives, TJM moyen
        self.assertEqual(mock_st.metric.call_count, 3)

    @patch("app.pages_modules.consultant_info.st")
    def test_display_vsa_missions_stats_no_tjm(self, mock_st):
        """Test stats missions VSA sans TJM"""
        from app.pages_modules.consultant_info import _display_vsa_missions_stats

        # Mock st.columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        missions = [Mock(est_active=True, tjm=None), Mock(est_active=False, tjm=None)]

        _display_vsa_missions_stats(missions)

        self.assertEqual(mock_st.metric.call_count, 3)


class TestValidateInfoForm(unittest.TestCase):
    """Tests pour validate_info_form"""

    @patch("app.pages_modules.consultant_info.st")
    def test_validate_info_form_valid(self, mock_st):
        """Test validation formulaire valide"""
        from app.pages_modules.consultant_info import validate_info_form

        result = validate_info_form("Jean", "Dupont", "jean.dupont@test.com")
        self.assertTrue(result)
        mock_st.error.assert_not_called()

    @patch("app.pages_modules.consultant_info.st")
    def test_validate_info_form_missing_prenom(self, mock_st):
        """Test validation prénom manquant"""
        from app.pages_modules.consultant_info import validate_info_form

        result = validate_info_form("", "Dupont", "jean@test.com")
        self.assertFalse(result)
        mock_st.error.assert_called()

    @patch("app.pages_modules.consultant_info.st")
    def test_validate_info_form_missing_nom(self, mock_st):
        """Test validation nom manquant"""
        from app.pages_modules.consultant_info import validate_info_form

        result = validate_info_form("Jean", "", "jean@test.com")
        self.assertFalse(result)
        mock_st.error.assert_called()

    @patch("app.pages_modules.consultant_info.st")
    def test_validate_info_form_invalid_email(self, mock_st):
        """Test validation email invalide"""
        from app.pages_modules.consultant_info import validate_info_form

        result = validate_info_form("Jean", "Dupont", "invalid-email")
        self.assertFalse(result)
        mock_st.error.assert_called()

    @patch("app.pages_modules.consultant_info.st")
    def test_validate_info_form_whitespace_only(self, mock_st):
        """Test validation avec espaces seulement"""
        from app.pages_modules.consultant_info import validate_info_form

        result = validate_info_form("   ", "Dupont", "jean@test.com")
        self.assertFalse(result)
        mock_st.error.assert_called()


class TestUpdateConsultantInfo(unittest.TestCase):
    """Tests pour update_consultant_info"""

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_update_consultant_info_success(self, mock_st, mock_session):
        """Test mise à jour infos consultant réussie"""
        from app.pages_modules.consultant_info import update_consultant_info, ConsultantSalaire

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        consultant = Mock(id=1, salaire_actuel=50000)
        
        # Premier appel: récupération du consultant
        # Deuxième appel: vérification email unique (aucun doublon)
        mock_db.query.return_value.filter.return_value.first.side_effect = [consultant, None]

        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "jean.dupont@test.com",
            "telephone": "0123456789",
            "salaire_actuel": 55000,
            "disponibilite": True,
            "notes": "Bon consultant",
            "commentaire": "Augmentation annuelle",
        }

        result = update_consultant_info(1, data)
        self.assertTrue(result)
        mock_db.commit.assert_called_once()

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_update_consultant_info_not_found(self, mock_st, mock_session):
        """Test mise à jour consultant introuvable"""
        from app.pages_modules.consultant_info import update_consultant_info

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None

        data = {"prenom": "Jean", "nom": "Dupont", "email": "jean@test.com", "salaire_actuel": 50000, "disponibilite": True}

        result = update_consultant_info(999, data)
        self.assertFalse(result)
        mock_st.error.assert_called()

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_update_consultant_info_duplicate_email(self, mock_st, mock_session):
        """Test mise à jour avec email en double"""
        from app.pages_modules.consultant_info import update_consultant_info

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        consultant = Mock(id=1, salaire_actuel=50000)
        existing = Mock(id=2, email="duplicate@test.com")

        # Premier appel: consultant à modifier
        # Deuxième appel: email déjà utilisé
        mock_db.query.return_value.filter.return_value.first.side_effect = [consultant, existing]

        data = {
            "prenom": "Jean",
            "nom": "Dupont",
            "email": "duplicate@test.com",
            "salaire_actuel": 50000,
            "disponibilite": True,
        }

        result = update_consultant_info(1, data)
        self.assertFalse(result)
        mock_st.error.assert_called()


class TestGenerateConsultantReport(unittest.TestCase):
    """Tests pour generate_consultant_report"""

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_generate_consultant_report_success(self, mock_st, mock_session):
        """Test génération rapport consultant réussie"""
        from app.pages_modules.consultant_info import generate_consultant_report

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Simuler comptages
        mock_db.query.return_value.filter.return_value.count.return_value = 5

        practice = Mock(nom="Data")
        consultant = Mock(
            id=1,
            prenom="Jean",
            nom="Dupont",
            email="jean@test.com",
            practice=practice,
            disponibilite=True,
            salaire_actuel=60000,
        )

        generate_consultant_report(consultant)

        mock_st.markdown.assert_called()
        mock_st.success.assert_called_once()

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_generate_consultant_report_no_practice(self, mock_st, mock_session):
        """Test génération rapport sans practice"""
        from app.pages_modules.consultant_info import generate_consultant_report

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.count.return_value = 0

        consultant = Mock(id=2, prenom="Marie", nom="Martin", email="marie@test.com", practice=None, disponibilite=False, salaire_actuel=None)

        generate_consultant_report(consultant)

        mock_st.markdown.assert_called()
        mock_st.success.assert_called_once()


class TestShowSalaryHistory(unittest.TestCase):
    """Tests pour show_salary_history"""

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_show_salary_history_with_data(self, mock_st, mock_session):
        """Test affichage historique salaires avec données"""
        from app.pages_modules.consultant_info import show_salary_history

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        salary1 = Mock(date_debut=date(2024, 1, 1), salaire=50000, commentaire="Embauche")
        salary2 = Mock(date_debut=date(2023, 1, 1), salaire=45000, commentaire="Ancien")

        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [salary1, salary2]

        show_salary_history(1)

        mock_st.markdown.assert_called()
        mock_st.dataframe.assert_called_once()

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_show_salary_history_no_data(self, mock_st, mock_session):
        """Test affichage historique salaires sans données"""
        from app.pages_modules.consultant_info import show_salary_history

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = []

        show_salary_history(2)

        # Rien ne devrait être affiché si pas de données
        mock_st.markdown.assert_not_called()


class TestShowDetailedSalaryHistory(unittest.TestCase):
    """Tests pour show_detailed_salary_history"""

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_show_detailed_salary_history_with_data(self, mock_st, mock_session):
        """Test affichage historique détaillé avec données"""
        from app.pages_modules.consultant_info import show_detailed_salary_history

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db

        # Mock st.columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_col3 = MagicMock()
        mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]

        salary1 = Mock(date_debut=date(2024, 1, 1), salaire=60000, commentaire="Augmentation")
        salary2 = Mock(date_debut=date(2023, 1, 1), salaire=50000, commentaire="Embauche")

        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [salary1, salary2]

        show_detailed_salary_history(1)

        mock_st.markdown.assert_called()
        # 3 métriques: actuel, min, max
        self.assertEqual(mock_st.metric.call_count, 3)
        mock_st.dataframe.assert_called_once()
        mock_st.button.assert_called_once()

    @patch("app.pages_modules.consultant_info.get_database_session")
    @patch("app.pages_modules.consultant_info.st")
    def test_show_detailed_salary_history_no_data(self, mock_st, mock_session):
        """Test affichage historique détaillé sans données"""
        from app.pages_modules.consultant_info import show_detailed_salary_history

        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

        show_detailed_salary_history(2)

        mock_st.markdown.assert_called()
        mock_st.info.assert_called_once()


if __name__ == "__main__":
    unittest.main()
