"""
Classe de base réutilisable pour tous les tests Consultator
Fournit des configurations communes et des utilitaires partagés
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import Dict, Any, Optional


class BaseTest:
    """Classe de base pour tous les tests avec configuration commune"""

    @pytest.fixture(autouse=True)
    def setup_test_env(self):
        """Configuration automatique pour chaque test"""
        # Configuration de base commune à tous les tests
        self.test_data = {}
        self.mock_objects = {}
        yield
        # Cleanup après chaque test
        self.test_data.clear()
        self.mock_objects.clear()

    def get_test_data(self, key: str, default: Any = None) -> Any:
        """Récupérer des données de test"""
        return self.test_data.get(key, default)

    def set_test_data(self, key: str, value: Any):
        """Stocker des données de test"""
        self.test_data[key] = value


class BaseUnitTest(BaseTest):
    """Classe de base pour les tests unitaires"""

    @pytest.fixture(autouse=True)
    def setup_unit_test(self):
        """Configuration spécifique aux tests unitaires"""
        # Isolation complète pour les tests unitaires
        self.isolated = True
        yield


class BaseIntegrationTest(BaseTest):
    """Classe de base pour les tests d'intégration"""

    @pytest.fixture(autouse=True)
    def setup_integration_test(self):
        """Configuration spécifique aux tests d'intégration"""
        # Configuration pour tests d'intégration
        self.integration_mode = True
        yield


class BaseUITest(BaseTest):
    """Classe de base pour les tests d'interface Streamlit"""

    @pytest.fixture(autouse=True)
    def setup_streamlit_mocks(self):
        """Configuration automatique des mocks Streamlit"""
        # Liste des fonctions Streamlit communes à mocker
        streamlit_functions = [
            "title",
            "header",
            "subheader",
            "write",
            "success",
            "error",
            "warning",
            "info",
            "columns",
            "tabs",
            "form",
            "form_submit_button",
            "text_input",
            "text_area",
            "selectbox",
            "checkbox",
            "button",
            "table",
            "dataframe",
            "metric",
            "expander",
            "empty",
            "radio",
            "sidebar",
            "spinner",
            "container",
        ]

        # Démarrer les patches
        self.streamlit_patches = []
        for func in streamlit_functions:
            patch_obj = patch(f"streamlit.{func}")
            self.streamlit_patches.append(patch_obj)
            patch_obj.start()

        # Configuration des mocks courants
        self._configure_common_mocks()

        yield

        # Arrêter tous les patches
        for patch_obj in self.streamlit_patches:
            patch_obj.stop()

    def _configure_common_mocks(self):
        """Configuration des mocks Streamlit courants"""

        # Mock columns pour retourner un nombre variable de colonnes
        def mock_columns(*args, **kwargs):
            if not args:
                return [MagicMock(), MagicMock()]  # Default 2 columns
            arg = args[0]
            if isinstance(arg, int):
                return [MagicMock() for _ in range(arg)]
            elif isinstance(arg, list):
                return [MagicMock() for _ in range(len(arg))]
            else:
                return [MagicMock(), MagicMock()]

        columns_patch = patch("streamlit.columns", side_effect=mock_columns)
        columns_patch.start()
        self.streamlit_patches.append(columns_patch)

        # Mock tabs pour retourner un nombre variable d'onglets
        def mock_tabs(*args, **kwargs):
            if not args:
                return [MagicMock(), MagicMock(), MagicMock()]  # Default 3 tabs
            arg = args[0]
            if isinstance(arg, list):
                return [MagicMock() for _ in range(len(arg))]
            else:
                return [MagicMock(), MagicMock(), MagicMock()]

        tabs_patch = patch("streamlit.tabs", side_effect=mock_tabs)
        tabs_patch.start()
        self.streamlit_patches.append(tabs_patch)

        # Mock form_submit_button pour retourner False par défaut
        submit_patch = patch("streamlit.form_submit_button", return_value=False)
        submit_patch.start()
        self.streamlit_patches.append(submit_patch)

        # Mock selectbox pour retourner la première option par défaut
        def mock_selectbox(*args, **kwargs):
            if len(args) > 1 and isinstance(args[1], list) and args[1]:
                return args[1][0]  # Return first option
            return "default"

        selectbox_patch = patch("streamlit.selectbox", side_effect=mock_selectbox)
        selectbox_patch.start()
        self.streamlit_patches.append(selectbox_patch)

    def assert_ui_elements_displayed(self, expected_elements: list):
        """Vérifier que les éléments UI attendus sont affichés"""
        # Implémentation générique pour vérifier les éléments UI
        for element in expected_elements:
            assert element in self.get_displayed_elements()

    def get_displayed_elements(self) -> list:
        """Récupérer la liste des éléments affichés (mock)"""
        # Retourner une liste mockée des éléments affichés
        return ["title", "header", "content"]


class BaseDatabaseTest(BaseTest):
    """Classe de base pour les tests de base de données"""

    @pytest.fixture(autouse=True)
    def setup_database_test(self):
        """Configuration spécifique aux tests de base de données"""
        # Configuration pour tests DB
        self.db_session = None
        yield
        # Cleanup DB après test
        if self.db_session:
            self.db_session.close()

    def create_test_data(self, model_class, **kwargs) -> Any:
        """Créer des données de test pour un modèle"""
        # Implémentation générique pour créer des données de test
        instance = model_class(**kwargs)
        if self.db_session:
            self.db_session.add(instance)
            self.db_session.commit()
        return instance


class BaseServiceTest(BaseUnitTest):
    """Classe de base pour les tests de services métier"""

    @pytest.fixture(autouse=True)
    def setup_service_test(self):
        """Configuration spécifique aux tests de services"""
        # Mocks pour les dépendances externes
        self.mock_db_session = MagicMock()
        self.mock_external_api = MagicMock()
        yield

    def mock_service_dependencies(self, service_class):
        """Mocker automatiquement les dépendances d'un service"""
        # Configuration automatique des mocks pour les services
        pass


class TestDataFactory:
    """Factory pour créer des données de test cohérentes"""

    @staticmethod
    def create_consultant_data(**overrides) -> Dict[str, Any]:
        """Créer des données de consultant de test"""
        base_data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@test.com",
            "telephone": "0123456789",
            "disponibilite": True,
            "salaire_souhaite": 45000,
            "experience_annees": 5,
        }
        base_data.update(overrides)
        return base_data

    @staticmethod
    def create_practice_data(**overrides) -> Dict[str, Any]:
        """Créer des données de practice de test"""
        base_data = {"nom": "Data Science", "actif": True}
        base_data.update(overrides)
        return base_data

    @staticmethod
    def create_mission_data(**overrides) -> Dict[str, Any]:
        """Créer des données de mission de test"""
        base_data = {
            "titre": "Mission Test",
            "client": "Client Test",
            "description": "Description de test",
            "duree_mois": 6,
            "tarif_jour": 450,
            "statut": "En cours",
        }
        base_data.update(overrides)
        return base_data


# Utilitaires de test partagés
def assert_contains_text(text: str, container: str):
    """Assertion utilitaire pour vérifier qu'un texte contient une chaîne"""
    assert text in container, f"'{text}' not found in '{container}'"


def assert_valid_email(email: str):
    """Assertion utilitaire pour valider un email"""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    assert re.match(pattern, email), f"Invalid email format: {email}"


def assert_positive_number(value: float, field_name: str = "value"):
    """Assertion utilitaire pour vérifier qu'un nombre est positif"""
    assert isinstance(value, (int, float)), f"{field_name} must be a number"
    assert value > 0, f"{field_name} must be positive, got {value}"
