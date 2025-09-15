import pytest
from unittest.mock import patch, MagicMock
from tests.fixtures.base_test import BaseUITest

from app.pages_modules.practices import (
    show,
    show_practice_overview_optimized,
    show_consultants_by_practice_optimized,
    show_practice_consultants_optimized,
    show_practice_detailed_stats_cached,
    show_practice_management_optimized,
    show_create_practice_form_optimized,
    show_edit_practice_form_optimized,
    show_assign_consultant_form_optimized,
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
    },
    {
        "id": 4,
        "nom": "Frontend Development",
        "description": "Practice développement front-end",
        "responsable": "Sophie Durand",
        "actif": True,
        "date_creation": "2023-04-05"
    },
    {
        "id": 5,
        "nom": "Backend Development",
        "description": "Practice développement back-end",
        "responsable": "Marc Moreau",
        "actif": True,
        "date_creation": "2023-05-20"
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
    },
    {
        "id": 3,
        "nom": "Bernard",
        "prenom": "Pierre",
        "email": "pierre.bernard@email.com",
        "telephone": "0123456791",
        "salaire_actuel": 72000,
        "practice_nom": "Cloud & DevOps",
        "disponibilite": False,
        "nb_missions": 8,
        "nb_competences": 12,
        "experience_annees": 7
    },
    {
        "id": 4,
        "nom": "Durand",
        "prenom": "Sophie",
        "email": "sophie.durand@email.com",
        "telephone": "0123456792",
        "salaire_actuel": 55000,
        "practice_nom": "Frontend Development",
        "disponibilite": True,
        "nb_missions": 3,
        "nb_competences": 7,
        "experience_annees": 3
    },
    {
        "id": 5,
        "nom": "Moreau",
        "prenom": "Marc",
        "email": "marc.moreau@email.com",
        "telephone": "0123456793",
        "salaire_actuel": 68000,
        "practice_nom": "Backend Development",
        "disponibilite": True,
        "nb_missions": 6,
        "nb_competences": 9,
        "experience_annees": 6
    }
]

# Données de test pour les statistiques
SAMPLE_PRACTICE_STATS = {
    "total_practices": 5,
    "total_consultants": 15,
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
            "total_consultants": 2,
            "consultants_actifs": 1,
            "responsable": "Pierre Bernard"
        },
        {
            "nom": "Frontend Development",
            "total_consultants": 3,
            "consultants_actifs": 3,
            "responsable": "Sophie Durand"
        },
        {
            "nom": "Backend Development",
            "total_consultants": 3,
            "consultants_actifs": 2,
            "responsable": "Marc Moreau"
        }
    ]
}

# Données de test pour les statistiques détaillées
SAMPLE_DETAILED_STATS = {
    "total_consultants": 15,
    "disponibles": 11,
    "salaire_moyen": 63600,
    "total_missions": 26,
    "total_competences": 42
}

# Données de test pour les business managers
SAMPLE_BUSINESS_MANAGERS = [
    {
        "id": 1,
        "nom": "Dubois",
        "prenom": "Olivier",
        "email": "o.dubois@consultator.fr",
        "telephone": "0123456780"
    },
    {
        "id": 2,
        "nom": "Leroy",
        "prenom": "Catherine",
        "email": "c.leroy@consultator.fr",
        "telephone": "0123456781"
    }
]

# ===== FIXTURES =====

@pytest.fixture
def sample_practice_data():
    """Fixture pour les données de practice de test"""
    return SAMPLE_PRACTICES[0].copy()

@pytest.fixture
def sample_consultant_data():
    """Fixture pour les données de consultant de test"""
    return SAMPLE_CONSULTANTS[0].copy()

@pytest.fixture
def sample_practices_list():
    """Fixture pour la liste des practices de test"""
    return SAMPLE_PRACTICES.copy()

@pytest.fixture
def sample_consultants_list():
    """Fixture pour la liste des consultants de test"""
    return SAMPLE_CONSULTANTS.copy()

@pytest.fixture
def sample_practice_stats():
    """Fixture pour les statistiques de practice"""
    return SAMPLE_PRACTICE_STATS.copy()

@pytest.fixture
def sample_detailed_stats():
    """Fixture pour les statistiques détaillées"""
    return SAMPLE_DETAILED_STATS.copy()

@pytest.fixture
def sample_business_managers():
    """Fixture pour les business managers de test"""
    return SAMPLE_BUSINESS_MANAGERS.copy()


class TestShowFunction(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.time')
    def test_show_basic_display(self, mock_time, mock_st):
        """Test affichage de base de la fonction show"""
        # Setup
        mock_time.time.return_value = 1000.0

        # Mock session state
        class MockSessionState(dict):
            def __init__(self):
                super().__init__()

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")

            def __contains__(self, key):
                return key in dict.keys(self)

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state

        # Mock UI components with serializable return values
        mock_st.title = MagicMock()
        mock_st.tabs = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.caption = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.spinner = MagicMock()
        mock_st.metric = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.subheader = MagicMock()
        mock_st.dataframe = MagicMock()
        mock_st.bar_chart = MagicMock()
        mock_st.info = MagicMock()
        mock_st.selectbox = MagicMock()
        mock_st.button = MagicMock(return_value=False)

        # Configure selectbox to return different values based on call arguments
        selectbox_call_count = 0
        def selectbox_side_effect(*args, **kwargs):
            nonlocal selectbox_call_count
            selectbox_call_count += 1
            if "par page" in str(args):
                return 25
            elif "Filtrer par Practice" in str(args):
                return "Toutes"
            else:
                return "Data Engineering"

        mock_st.selectbox.side_effect = selectbox_side_effect

        # Mock PracticeServiceOptimized to return serializable data
        with patch('app.pages_modules.practices.PracticeServiceOptimized') as mock_service:
            mock_service.get_practice_statistics_optimized.return_value = {
                "total_practices": 2,
                "total_consultants": 10,
                "practices_detail": [
                    {"nom": "Data Engineering", "total_consultants": 5, "consultants_actifs": 4},
                    {"nom": "Data Science", "total_consultants": 5, "consultants_actifs": 3}
                ]
            }
            mock_service.get_all_practices_cached.return_value = SAMPLE_PRACTICES
            mock_service.get_consultants_by_practice_paginated.return_value = (SAMPLE_CONSULTANTS, len(SAMPLE_CONSULTANTS))

            # Execute
            show()

            # Verify
            mock_st.title.assert_called_once_with("🏢 Gestion des Practices")
            mock_st.tabs.assert_called_once()
            mock_st.caption.assert_called_once()

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.time')
    def test_show_with_session_state(self, mock_time, mock_st):
        """Test show avec session state existant"""
        # Setup
        mock_time.time.return_value = 1000.0

        class MockSessionState(dict):
            def __init__(self):
                super().__init__()
                self.practice_page = 2

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")

            def __contains__(self, key):
                return key in dict.keys(self)

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state

        mock_st.title = MagicMock()
        mock_st.tabs = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.caption = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.spinner = MagicMock()
        mock_st.metric = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.subheader = MagicMock()
        mock_st.dataframe = MagicMock()
        mock_st.bar_chart = MagicMock()
        mock_st.info = MagicMock()
        mock_st.selectbox = MagicMock()
        mock_st.button = MagicMock(return_value=False)

        # Configure selectbox to return different values based on call arguments
        selectbox_call_count = 0
        def selectbox_side_effect(*args, **kwargs):
            nonlocal selectbox_call_count
            selectbox_call_count += 1
            if "par page" in str(args):
                return 25
            elif "Filtrer par Practice" in str(args):
                return "Toutes"
            else:
                return "Data Engineering"

        mock_st.selectbox.side_effect = selectbox_side_effect

        # Mock PracticeServiceOptimized to return serializable data
        with patch('app.pages_modules.practices.PracticeServiceOptimized') as mock_service:
            mock_service.get_practice_statistics_optimized.return_value = {
                "total_practices": 2,
                "total_consultants": 10,
                "practices_detail": [
                    {"nom": "Data Engineering", "total_consultants": 5, "consultants_actifs": 4},
                    {"nom": "Data Science", "total_consultants": 5, "consultants_actifs": 3}
                ]
            }
            mock_service.get_all_practices_cached.return_value = SAMPLE_PRACTICES
            mock_service.get_consultants_by_practice_paginated.return_value = (SAMPLE_CONSULTANTS, len(SAMPLE_CONSULTANTS))

            # Execute
            show()

            # Verify session state is preserved
            assert mock_session_state.practice_page == 2


class TestShowPracticeOverviewOptimized(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_practice_overview_with_data(self, mock_service, mock_st):
        """Test vue d'ensemble avec données"""
        # Setup mock data
        mock_stats = SAMPLE_PRACTICE_STATS
        mock_service.get_practice_statistics_optimized.return_value = mock_stats

        # Mock UI components
        mock_st.spinner = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.metric = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.subheader = MagicMock()
        mock_st.dataframe = MagicMock()
        mock_st.bar_chart = MagicMock()
        mock_st.info = MagicMock()

        # Mock pandas and plotly
        with patch('app.pages_modules.practices.pd') as mock_pd, \
             patch('app.pages_modules.practices.px') as mock_px:

            mock_df = MagicMock()
            mock_pd.DataFrame.return_value = mock_df
            mock_df.rename.return_value = mock_df
            mock_df.__getitem__ = MagicMock(return_value=mock_df)
            mock_df.set_index.return_value = mock_df
            mock_df.__len__ = MagicMock(return_value=2)  # 2 practices in mock data

            mock_fig = MagicMock()
            mock_px.pie.return_value = mock_fig

            mock_st.plotly_chart = MagicMock()

            # Execute
            show_practice_overview_optimized()

            # Verify
            mock_service.get_practice_statistics_optimized.assert_called_once()
            assert mock_st.metric.call_count == 3  # 3 metrics in overview
            mock_st.dataframe.assert_called_once()
            mock_st.bar_chart.assert_called_once()
            mock_px.pie.assert_called_once()

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_practice_overview_empty_data(self, mock_service, mock_st):
        """Test vue d'ensemble sans données"""
        # Setup empty data
        mock_stats = {
            "total_practices": 0,
            "total_consultants": 0,
            "practices_detail": []
        }
        mock_service.get_practice_statistics_optimized.return_value = mock_stats

        mock_st.spinner = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.metric = MagicMock()
        mock_st.info = MagicMock()

        # Execute
        show_practice_overview_optimized()

        # Verify
        mock_st.info.assert_called_once()


class TestShowConsultantsByPracticeOptimized(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_consultants_with_data(self, mock_service, mock_st):
        """Test affichage consultants avec données"""
        # Setup mock data
        mock_practices = SAMPLE_PRACTICES
        mock_consultants = SAMPLE_CONSULTANTS

        mock_service.get_all_practices_cached.return_value = mock_practices
        mock_service.get_consultants_by_practice_paginated.return_value = (mock_consultants, len(mock_consultants))

        # Mock session state
        class MockSessionState(dict):
            def __init__(self):
                super().__init__()
                self.practice_page = 1

            def __setattr__(self, name, value):
                self[name] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError:
                    raise AttributeError(f"'MockSessionState' object has no attribute '{name}'")

            def __contains__(self, key):
                return key in dict.keys(self)

        mock_session_state = MockSessionState()
        mock_st.session_state = mock_session_state

        # Mock UI components
        mock_st.selectbox = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.spinner = MagicMock()
        mock_st.info = MagicMock()
        mock_st.markdown = MagicMock()
        mock_st.dataframe = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.metric = MagicMock()
        mock_st.code = MagicMock()
        mock_st.success = MagicMock()
        mock_st.warning = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])

        # Configure selectbox to return different values based on call arguments
        selectbox_call_count = 0
        def selectbox_side_effect(*args, **kwargs):
            nonlocal selectbox_call_count
            selectbox_call_count += 1
            if "par page" in str(args):
                return 25
            elif "Filtrer par Practice" in str(args):
                return "Toutes"
            else:
                return "Toutes"

        mock_st.selectbox.side_effect = selectbox_side_effect

        # Execute
        show_consultants_by_practice_optimized()

        # Verify
        mock_service.get_all_practices_cached.assert_called_once()
        mock_service.get_consultants_by_practice_paginated.assert_called_once()
        mock_st.info.assert_called_once()

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_consultants_empty_data(self, mock_service, mock_st):
        """Test affichage consultants sans données"""
        mock_service.get_all_practices_cached.return_value = []
        mock_service.get_consultants_by_practice_paginated.return_value = ([], 0)

        mock_st.selectbox = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.spinner = MagicMock()
        mock_st.info = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])

        # Configure selectbox to return different values based on call arguments
        selectbox_call_count = 0
        def selectbox_side_effect(*args, **kwargs):
            nonlocal selectbox_call_count
            selectbox_call_count += 1
            if "par page" in str(args):
                return 25
            elif "Filtrer par Practice" in str(args):
                return "Toutes"
            else:
                return "Toutes"

        mock_st.selectbox.side_effect = selectbox_side_effect

        # Execute
        show_consultants_by_practice_optimized()

        # Verify
        mock_st.info.assert_called_with("ℹ️ Aucun consultant trouvé pour cette practice.")


class TestShowPracticeConsultantsOptimized(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.pd')
    def test_show_practice_consultants_with_data(self, mock_pd, mock_st):
        """Test affichage consultants d'une practice avec données"""
        # Setup mock consultants
        consultants = SAMPLE_CONSULTANTS[:3]  # Prendre les 3 premiers consultants

        mock_df = MagicMock()
        mock_pd.DataFrame.return_value = mock_df

        mock_st.markdown = MagicMock()
        mock_st.dataframe = MagicMock()
        mock_st.expander = MagicMock()
        mock_st.button = MagicMock(return_value=False)
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.metric = MagicMock()

        # Execute
        show_practice_consultants_optimized("DevOps", consultants)

        # Verify
        mock_st.markdown.assert_called()
        mock_pd.DataFrame.assert_called_once()
        mock_st.dataframe.assert_called_once()

    @patch('app.pages_modules.practices.st')
    def test_show_practice_consultants_empty(self, mock_st):
        """Test affichage consultants d'une practice vide"""
        mock_st.markdown = MagicMock()
        mock_st.info = MagicMock()

        # Execute
        show_practice_consultants_optimized("DevOps", [])

        # Verify
        mock_st.info.assert_called_once_with("Aucun consultant dans cette practice")


class TestShowPracticeDetailedStatsCached(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_detailed_stats_with_data(self, mock_service, mock_st):
        """Test statistiques détaillées avec données"""
        # Setup mock stats
        mock_stats = SAMPLE_DETAILED_STATS
        mock_service.get_practice_detailed_stats_cached.return_value = mock_stats

        mock_st.subheader = MagicMock()
        mock_st.spinner = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock(), MagicMock()])
        mock_st.metric = MagicMock()

        # Execute
        show_practice_detailed_stats_cached("DevOps")

        # Verify
        mock_service.get_practice_detailed_stats_cached.assert_called_once_with("DevOps")
        assert mock_st.metric.call_count == 6  # 6 metrics displayed

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_detailed_stats_empty(self, mock_service, mock_st):
        """Test statistiques détaillées sans données"""
        mock_service.get_practice_detailed_stats_cached.return_value = None

        mock_st.subheader = MagicMock()
        mock_st.spinner = MagicMock()
        mock_st.info = MagicMock()

        # Execute
        show_practice_detailed_stats_cached("DevOps")

        # Verify
        mock_st.info.assert_called_once_with("Aucune donnée disponible")


class TestShowPracticeManagementOptimized(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_practice_management(self, mock_service, mock_st):
        """Test interface de gestion des practices"""
        mock_service.get_all_practices_cached.return_value = []

        mock_st.subheader = MagicMock()
        mock_st.tabs = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])

        # Mock ConsultantService to return serializable data
        with patch('app.pages_modules.practices.ConsultantService') as mock_consultant_service:
            mock_consultant_service.get_all_consultants.return_value = SAMPLE_CONSULTANTS

            # Mock selectbox for the assign form - configure to return different values
            selectbox_call_count = 0
            def selectbox_side_effect(*args, **kwargs):
                nonlocal selectbox_call_count
                selectbox_call_count += 1
                if "Sélectionner le consultant" in str(args):
                    return "Jean Dupont (jean.dupont@email.com)"
                elif "Nouvelle practice" in str(args):
                    return "Data Engineering"
                else:
                    return "Data Engineering"

            mock_st.selectbox.side_effect = selectbox_side_effect

            # Execute
            show_practice_management_optimized()

            # Verify
            mock_service.get_all_practices_cached.assert_called_once()
            mock_st.tabs.assert_called_once()


class TestShowCreatePracticeFormOptimized(BaseUITest):
    @patch('app.pages_modules.practices.st')
    def test_show_create_form_display(self, mock_st):
        """Test affichage formulaire de création"""
        mock_st.markdown = MagicMock()
        mock_st.form = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
        mock_st.text_input = MagicMock(return_value="")
        mock_st.text_area = MagicMock(return_value="")
        mock_st.form_submit_button = MagicMock(return_value=False)

        # Execute
        show_create_practice_form_optimized()

        # Verify
        mock_st.markdown.assert_called_once_with("#### ➕ Créer une nouvelle Practice")
        mock_st.form.assert_called_once()

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_create_form_success(self, mock_opt_service, mock_st):
        """Test création practice réussie"""
        with patch('services.practice_service.PracticeService') as mock_practice_service:
            mock_practice_service.create_practice.return_value = {"id": 1, "nom": "Test Practice"}

            mock_st.markdown = MagicMock()
            mock_st.form = MagicMock()
            mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
            mock_st.text_input = MagicMock(return_value="Test Practice")
            mock_st.text_area = MagicMock(return_value="Description test")
            mock_st.form_submit_button = MagicMock(return_value=True)
            mock_st.error = MagicMock()
            mock_st.rerun = MagicMock()

            # Execute
            show_create_practice_form_optimized()

            # Verify
            mock_practice_service.create_practice.assert_called_once()
            mock_opt_service.clear_practices_cache.assert_called_once()
            mock_st.rerun.assert_called_once()

    @patch('app.pages_modules.practices.st')
    def test_show_create_form_validation_error(self, mock_st):
        """Test validation formulaire de création"""
        mock_st.markdown = MagicMock()
        mock_st.form = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
        mock_st.text_input = MagicMock(return_value="")  # Empty name
        mock_st.text_area = MagicMock(return_value="")
        mock_st.form_submit_button = MagicMock(return_value=True)
        mock_st.error = MagicMock()

        # Execute
        show_create_practice_form_optimized()

        # Verify
        mock_st.error.assert_called_once_with("❌ Le nom de la practice est obligatoire")


class TestShowEditPracticeFormOptimized(BaseUITest):
    @patch('app.pages_modules.practices.st')
    def test_show_edit_form_no_practices(self, mock_st):
        """Test formulaire modification sans practices"""
        mock_st.markdown = MagicMock()
        mock_st.info = MagicMock()

        # Execute
        show_edit_practice_form_optimized([])

        # Verify
        mock_st.info.assert_called_once_with("Aucune practice à modifier")

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_edit_form_success(self, mock_opt_service, mock_st):
        """Test modification practice réussie"""
        practices = SAMPLE_PRACTICES[:2]  # Utiliser les 2 premières practices

        with patch('services.practice_service.PracticeService') as mock_practice_service:
            mock_practice_service.update_practice.return_value = True

            mock_st.markdown = MagicMock()
            mock_st.selectbox = MagicMock(return_value="Data Engineering")
            mock_st.form = MagicMock()
            mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
            mock_st.text_input = MagicMock(side_effect=["New DevOps", "New Responsable"])
            mock_st.text_area = MagicMock(return_value="New description")
            mock_st.checkbox = MagicMock(return_value=True)
            mock_st.form_submit_button = MagicMock(return_value=True)
            mock_st.error = MagicMock()
            mock_st.rerun = MagicMock()

            # Execute
            show_edit_practice_form_optimized(practices)

            # Verify
            mock_practice_service.update_practice.assert_called_once()
            mock_opt_service.clear_practices_cache.assert_called_once()


class TestShowAssignConsultantFormOptimized(BaseUITest):
    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.ConsultantService')
    def test_show_assign_form_no_consultants(self, mock_consultant_service, mock_st):
        """Test formulaire assignation sans consultants"""
        mock_consultant_service.get_all_consultants.return_value = []

        mock_st.markdown = MagicMock()
        mock_st.info = MagicMock()

        # Execute
        show_assign_consultant_form_optimized([])

        # Verify
        mock_st.info.assert_called_once_with("Aucun consultant trouvé")

    @patch('app.pages_modules.practices.st')
    @patch('app.pages_modules.practices.ConsultantService')
    @patch('app.pages_modules.practices.PracticeServiceOptimized')
    def test_show_assign_form_success(self, mock_opt_service, mock_consultant_service, mock_st):
        """Test assignation consultant réussie"""
        # Mock consultant
        mock_consultant = MagicMock()
        mock_consultant.id = SAMPLE_CONSULTANTS[0]["id"]
        mock_consultant.nom_complet = f"{SAMPLE_CONSULTANTS[0]['prenom']} {SAMPLE_CONSULTANTS[0]['nom']}"
        mock_consultant.email = SAMPLE_CONSULTANTS[0]["email"]
        mock_consultant.practice = None

        mock_consultant_service.get_all_consultants.return_value = [mock_consultant]

        practices = SAMPLE_PRACTICES[:2]  # Utiliser les 2 premières practices

        with patch('services.practice_service.PracticeService') as mock_practice_service:
            mock_practice_service.assign_consultant_to_practice.return_value = True

            mock_st.markdown = MagicMock()
            mock_st.selectbox = MagicMock(side_effect=["Jean Dupont (jean.dupont@email.com)", "Data Engineering"])
            mock_st.info = MagicMock()
            mock_st.button = MagicMock(return_value=True)
            mock_st.success = MagicMock()
            mock_st.error = MagicMock()
            mock_st.rerun = MagicMock()

            # Execute
            show_assign_consultant_form_optimized(practices)

            # Verify
            mock_practice_service.assign_consultant_to_practice.assert_called_once_with(1, 1)
            mock_st.success.assert_called_once_with("✅ Consultant assigné avec succès !")
            mock_opt_service.clear_practices_cache.assert_called_once()
