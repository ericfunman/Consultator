import pytest
from unittest.mock import patch, MagicMock
from tests.fixtures.base_test import BaseUITest

from app.pages_modules.practices import (
    show,
    show_practice_overview,
    show_consultants_by_practice,
    show_practice_management,
)


# ===== DONNÉES DE TEST =====

# Données de test pour les practices
SAMPLE_PRACTICES = [
    {
        "id": 1,
        "nom": "Data Engineering",
        "description": "Practice spécialisée en ingénierie de données",
        "responsable": "Jean Dupont",
        "actif": True,
        "date_creation": "2023-01-15"
    },
    {
        "id": 2,
        "nom": "Data Science",
        "description": "Practice d'analyse et science des données",
        "responsable": "Marie Martin",
        "actif": True,
        "date_creation": "2023-02-01"
    },
    {
        "id": 3,
        "nom": "Cloud & DevOps",
        "description": "Practice cloud et automatisation",
        "responsable": "Pierre Bernard",
        "actif": True,
        "date_creation": "2023-03-10"
    }
]

# Données de test pour les consultants
SAMPLE_CONSULTANTS = [
    {
        "id": 1,
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@email.com",
        "telephone": "0123456789",
        "salaire_actuel": 65000,
        "practice_nom": "Data Engineering",
        "disponibilite": True,
        "nb_missions": 5,
        "nb_competences": 8,
        "experience_annees": 5
    },
    {
        "id": 2,
        "nom": "Martin",
        "prenom": "Marie",
        "email": "marie.martin@email.com",
        "telephone": "0123456790",
        "salaire_actuel": 58000,
        "practice_nom": "Data Science",
        "disponibilite": True,
        "nb_missions": 4,
        "nb_competences": 6,
        "experience_annees": 4
    }
]

# Données de test pour les statistiques
SAMPLE_PRACTICE_STATS = {
    "total_practices": 3,
    "total_consultants": 10,
    "active_practices": 3,
    "practices_detail": [
        {
            "nom": "Data Engineering",
            "total_consultants": 3,
            "consultants_actifs": 2,
            "responsable": "Jean Dupont"
        },
        {
            "nom": "Data Science",
            "total_consultants": 4,
            "consultants_actifs": 3,
            "responsable": "Marie Martin"
        },
        {
            "nom": "Cloud & DevOps",
            "total_consultants": 3,
            "consultants_actifs": 2,
            "responsable": "Pierre Bernard"
        }
    ]
}


class TestShowFunction(BaseUITest):
    @patch('app.pages_modules.practices.st')
    def test_show_basic_display(self, mock_st):
        """Test affichage de base de la fonction show"""
        
        # Mock UI components
        mock_st.title = MagicMock()
        mock_st.tabs = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])

        # Mock PracticeService to return serializable data
        with patch('app.pages_modules.practices.PracticeService') as mock_service:
            mock_service.get_practice_statistics.return_value = {
                "total_practices": 2,
                "total_consultants": 10,
                "active_practices": 2
            }
            mock_service.get_all_practices.return_value = []

            # Execute
            show()

            # Verify
            mock_st.title.assert_called_once_with("🏢 Gestion des Practices")
            mock_st.tabs.assert_called_once()


class TestShowPracticeOverview(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeService')
    def test_show_practice_overview_with_data(self, mock_service, mock_st):
        """Test vue d'ensemble avec données"""
        # Setup mock data
        mock_stats = SAMPLE_PRACTICE_STATS
        mock_service.get_practice_statistics.return_value = mock_stats

        # Create mock practice objects
        class MockPractice:
            def __init__(self, data):
                for k, v in data.items():
                    setattr(self, k, v)

        mock_practices = [MockPractice(p) for p in SAMPLE_PRACTICES]
        mock_service.get_all_practices.return_value = mock_practices

        # Mock UI components
        mock_st.subheader = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.metric = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.write = MagicMock()
        mock_st.error = MagicMock()

        # Execute
        show_practice_overview()

        # Verify
        mock_service.get_practice_statistics.assert_called_once()
        mock_service.get_all_practices.assert_called_once()
        assert mock_st.metric.call_count == 3  # 3 metrics in overview
        mock_st.subheader.assert_called()

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeService')
    def test_show_practice_overview_error(self, mock_service, mock_st):
        """Test vue d'ensemble avec erreur"""
        # Setup error
        mock_service.get_practice_statistics.side_effect = Exception("Test error")

        mock_st.subheader = MagicMock()
        mock_st.error = MagicMock()

        # Execute
        show_practice_overview()

        # Verify
        mock_st.error.assert_called_once()


class TestShowConsultantsByPractice(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeService')
    def test_show_consultants_with_data(self, mock_service, mock_st):
        """Test affichage consultants avec données"""
        
        # Create mock practice and consultant objects
        class MockPractice:
            def __init__(self, data):
                for k, v in data.items():
                    setattr(self, k, v)

        class MockConsultant:
            def __init__(self, data):
                for k, v in data.items():
                    setattr(self, k, v)

        mock_practices = [MockPractice(p) for p in SAMPLE_PRACTICES]
        mock_consultants = [MockConsultant(c) for c in SAMPLE_CONSULTANTS]

        mock_service.get_all_practices.return_value = mock_practices
        mock_service.get_consultants_by_practice.return_value = mock_consultants

        # Mock UI components
        mock_st.subheader = MagicMock()
        mock_st.selectbox = MagicMock(return_value=mock_practices[0])
        mock_st.write = MagicMock()
        mock_st.info = MagicMock()
        mock_st.warning = MagicMock()
        mock_st.error = MagicMock()

        # Execute
        show_consultants_by_practice()

        # Verify
        mock_service.get_all_practices.assert_called_once()
        mock_service.get_consultants_by_practice.assert_called_once()
        mock_st.selectbox.assert_called_once()

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeService')
    def test_show_consultants_no_practices(self, mock_service, mock_st):
        """Test affichage consultants sans practices"""
        mock_service.get_all_practices.return_value = []

        mock_st.subheader = MagicMock()
        mock_st.warning = MagicMock()
        mock_st.error = MagicMock()

        # Execute
        show_consultants_by_practice()

        # Verify
        mock_st.warning.assert_called_once_with("Aucune practice trouvée.")

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeService')
    def test_show_consultants_error(self, mock_service, mock_st):
        """Test affichage consultants avec erreur"""
        mock_service.get_all_practices.side_effect = Exception("Test error")

        mock_st.subheader = MagicMock()
        mock_st.error = MagicMock()

        # Execute
        show_consultants_by_practice()

        # Verify
        mock_st.error.assert_called_once()


class TestShowPracticeManagement(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeService')
    def test_show_practice_management(self, mock_service, mock_st):
        """Test interface de gestion des practices"""
        
        # Create mock practice objects
        class MockPractice:
            def __init__(self, data):
                for k, v in data.items():
                    setattr(self, k, v)

        mock_practices = [MockPractice(p) for p in SAMPLE_PRACTICES[:2]]
        mock_service.get_all_practices.return_value = mock_practices

        # Mock UI components
        mock_st.subheader = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.form = MagicMock()
        mock_st.text_input = MagicMock(return_value="")
        mock_st.text_area = MagicMock(return_value="")
        mock_st.form_submit_button = MagicMock(return_value=False)
        mock_st.write = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.button = MagicMock(return_value=False)

        # Execute
        show_practice_management()

        # Verify
        mock_st.subheader.assert_called_once_with("⚙️ Gestion des Practices")
        mock_st.expander.assert_called_once()
        mock_service.get_all_practices.assert_called_once()

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeService')
    def test_show_practice_management_create_success(self, mock_service, mock_st):
        """Test création practice réussie"""
        mock_service.create_practice.return_value = True
        mock_service.get_all_practices.return_value = []

        # Mock UI components
        mock_st.subheader = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.form = MagicMock()
        mock_st.text_input = MagicMock(return_value="Test Practice")
        mock_st.text_area = MagicMock(return_value="Description test")
        mock_st.form_submit_button = MagicMock(return_value=True)
        mock_st.success = MagicMock()
        mock_st.error = MagicMock()
        mock_st.rerun = MagicMock()
        mock_st.write = MagicMock()

        # Execute
        show_practice_management()

        # Verify
        mock_service.create_practice.assert_called_once()
        mock_st.success.assert_called_once()
        mock_st.rerun.assert_called_once()

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeService')
    def test_show_practice_management_create_validation_error(self, mock_service, mock_st):
        """Test validation formulaire de création"""
        mock_service.get_all_practices.return_value = []

        # Mock UI components
        mock_st.subheader = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.form = MagicMock()
        mock_st.text_input = MagicMock(return_value="")  # Empty name
        mock_st.text_area = MagicMock(return_value="")
        mock_st.form_submit_button = MagicMock(return_value=True)
        mock_st.error = MagicMock()
        mock_st.write = MagicMock()

        # Execute
        show_practice_management()

        # Verify
        mock_st.error.assert_called_with("❌ Le nom de la practice est obligatoire.")