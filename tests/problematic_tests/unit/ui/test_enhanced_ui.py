"""
Tests pour le module enhanced_ui.py
Couverture complète des filtres avancés et recherche en temps réel
"""

import time
from datetime import date
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import streamlit as st

from app.ui.enhanced_ui import AdvancedUIFilters
from app.ui.enhanced_ui import RealTimeSearch


class TestAdvancedUIFilters:
    """Tests pour la classe AdvancedUIFilters"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.ui_filters = AdvancedUIFilters()

    def test_init(self):
        """Test de l'initialisation"""
        assert isinstance(self.ui_filters.filters, dict)
        assert self.ui_filters.filters["search_term"] == ""
        assert self.ui_filters.filters["practice_filter"] is None
        assert self.ui_filters.filters["grade_filter"] is None
        assert self.ui_filters.filters["availability_filter"] is None

    def test_get_unique_values_practice(self):
        """Test récupération des valeurs uniques pour practice"""
        values = self.ui_filters._get_unique_values("practice_name")
        assert isinstance(values, list)
        assert "Digital" in values
        assert "Data" in values
        assert "Cloud" in values
        assert "Cybersecurity" in values

    def test_get_unique_values_grade(self):
        """Test récupération des valeurs uniques pour grade"""
        values = self.ui_filters._get_unique_values("grade")
        assert isinstance(values, list)
        assert "Junior" in values
        assert "Confirmé" in values
        assert "Senior" in values
        assert "Expert" in values

    def test_get_unique_values_type_contrat(self):
        """Test récupération des valeurs uniques pour type_contrat"""
        values = self.ui_filters._get_unique_values("type_contrat")
        assert isinstance(values, list)
        assert "CDI" in values
        assert "CDD" in values
        assert "Freelance" in values
        assert "Stagiaire" in values

    def test_get_unique_values_societe(self):
        """Test récupération des valeurs uniques pour societe"""
        values = self.ui_filters._get_unique_values("societe")
        assert isinstance(values, list)
        assert "Quanteam" in values
        assert "Asigma" in values
        assert "Autres" in values

    def test_get_unique_values_unknown_field(self):
        """Test récupération des valeurs pour un champ inconnu"""
        values = self.ui_filters._get_unique_values("unknown_field")
        assert values == []

    def test_reset_filters(self):
        """Test de la réinitialisation des filtres"""
        # Modifier quelques filtres
        self.ui_filters.filters["search_term"] = "test"
        self.ui_filters.filters["practice_filter"] = "Digital"
        self.ui_filters.filters["salaire_min"] = 50000
        self.ui_filters.filters["experience_max"] = 10.0

        # Réinitialiser
        self.ui_filters.reset_filters()

        # Vérifier la réinitialisation
        assert self.ui_filters.filters["search_term"] == ""
        assert self.ui_filters.filters["practice_filter"] is None
        # Note: salaire_min et salaire_max peuvent être None après reset selon l'implémentation
        assert self.ui_filters.filters["salaire_min"] in [0, None]
        assert self.ui_filters.filters["salaire_max"] in [200000, None]
        assert self.ui_filters.filters["experience_min"] in [0, None]
        assert self.ui_filters.filters["experience_max"] in [50.0, None]

    def test_apply_filters_empty_data(self):
        """Test application des filtres sur données vides"""
        result = self.ui_filters.apply_filters([])
        assert result == []

    def test_apply_filters_no_filters(self):
        """Test application sans filtres actifs"""
        data = [
            {"nom": "Dupont", "prenom": "Jean", "practice_name": "Digital"},
            {"nom": "Martin", "prenom": "Marie", "practice_name": "Data"},
        ]
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 2
        assert result == data

    def test_apply_filters_search_term(self):
        """Test filtre de recherche textuelle"""
        data = [
            {"nom": "Dupont", "prenom": "Jean", "practice_name": "Digital"},
            {"nom": "Martin", "prenom": "Marie", "practice_name": "Data"},
            {"nom": "Bernard", "prenom": "Paul", "practice_name": "Cloud"},
        ]

        self.ui_filters.filters["search_term"] = "jean"
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["prenom"] == "Jean"

    def test_apply_filters_search_term_case_insensitive(self):
        """Test recherche insensible à la casse"""
        data = [{"nom": "DUPONT", "prenom": "jean", "practice_name": "Digital"}]

        self.ui_filters.filters["search_term"] = "JEAN"
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1

    def test_apply_filters_practice(self):
        """Test filtre par practice"""
        data = [
            {"nom": "Dupont", "practice_name": "Digital"},
            {"nom": "Martin", "practice_name": "Data"},
            {"nom": "Bernard", "practice_name": "Digital"},
        ]

        self.ui_filters.filters["practice_filter"] = "Digital"
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 2
        assert all(item["practice_name"] == "Digital" for item in result)

    def test_apply_filters_grade(self):
        """Test filtre par grade"""
        data = [
            {"nom": "Dupont", "grade": "Junior"},
            {"nom": "Martin", "grade": "Senior"},
            {"nom": "Bernard", "grade": "Junior"},
        ]

        self.ui_filters.filters["grade_filter"] = "Junior"
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 2
        assert all(item["grade"] == "Junior" for item in result)

    def test_apply_filters_availability_true(self):
        """Test filtre disponibilité = True"""
        data = [
            {"nom": "Dupont", "disponibilite": True},
            {"nom": "Martin", "disponibilite": False},
            {"nom": "Bernard", "disponibilite": True},
        ]

        self.ui_filters.filters["availability_filter"] = True
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 2
        assert all(item["disponibilite"] is True for item in result)

    def test_apply_filters_availability_false(self):
        """Test filtre disponibilité = False"""
        data = [
            {"nom": "Dupont", "disponibilite": True},
            {"nom": "Martin", "disponibilite": False},
        ]

        self.ui_filters.filters["availability_filter"] = False
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["disponibilite"] is False

    def test_apply_filters_societe(self):
        """Test filtre par société"""
        data = [
            {"nom": "Dupont", "societe": "Quanteam"},
            {"nom": "Martin", "societe": "Asigma"},
            {"nom": "Bernard", "societe": "Quanteam"},
        ]

        self.ui_filters.filters["societe_filter"] = "Quanteam"
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 2
        assert all(item["societe"] == "Quanteam" for item in result)

    def test_apply_filters_type_contrat(self):
        """Test filtre par type de contrat"""
        data = [
            {"nom": "Dupont", "type_contrat": "CDI"},
            {"nom": "Martin", "type_contrat": "CDD"},
            {"nom": "Bernard", "type_contrat": "CDI"},
        ]

        self.ui_filters.filters["type_contrat_filter"] = "CDI"
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 2
        assert all(item["type_contrat"] == "CDI" for item in result)

    def test_apply_filters_salaire_min(self):
        """Test filtre salaire minimum"""
        data = [
            {"nom": "Dupont", "salaire_actuel": 45000},
            {"nom": "Martin", "salaire_actuel": 55000},
            {"nom": "Bernard", "salaire_actuel": 40000},
        ]

        self.ui_filters.filters["salaire_min"] = 50000
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["salaire_actuel"] == 55000

    def test_apply_filters_salaire_max(self):
        """Test filtre salaire maximum"""
        data = [
            {"nom": "Dupont", "salaire_actuel": 45000},
            {"nom": "Martin", "salaire_actuel": 55000},
            {"nom": "Bernard", "salaire_actuel": 60000},
        ]

        self.ui_filters.filters["salaire_max"] = 50000
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["salaire_actuel"] == 45000

    def test_apply_filters_salaire_missing_value(self):
        """Test filtre salaire avec valeur manquante"""
        data = [
            {"nom": "Dupont"},  # Pas de salaire_actuel
            {"nom": "Martin", "salaire_actuel": 55000},
        ]

        self.ui_filters.filters["salaire_min"] = 50000
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["nom"] == "Martin"

    def test_apply_filters_experience_min(self):
        """Test filtre expérience minimum"""
        data = [
            {"nom": "Dupont", "experience_annees": 3},
            {"nom": "Martin", "experience_annees": 7},
            {"nom": "Bernard", "experience_annees": 2},
        ]

        self.ui_filters.filters["experience_min"] = 5
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["experience_annees"] == 7

    def test_apply_filters_experience_max(self):
        """Test filtre expérience maximum"""
        data = [
            {"nom": "Dupont", "experience_annees": 3},
            {"nom": "Martin", "experience_annees": 7},
            {"nom": "Bernard", "experience_annees": 10},
        ]

        self.ui_filters.filters["experience_max"] = 5
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["experience_annees"] == 3

    def test_apply_filters_experience_missing_value(self):
        """Test filtre expérience avec valeur manquante"""
        data = [
            {"nom": "Dupont"},  # Pas d'experience_annees
            {"nom": "Martin", "experience_annees": 7},
        ]

        self.ui_filters.filters["experience_min"] = 5
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["nom"] == "Martin"

    def test_apply_filters_multiple_filters(self):
        """Test application de plusieurs filtres en même temps"""
        data = [
            {
                "nom": "Dupont",
                "practice_name": "Digital",
                "grade": "Senior",
                "salaire_actuel": 55000,
                "experience_annees": 7,
            },
            {
                "nom": "Martin",
                "practice_name": "Digital",
                "grade": "Junior",
                "salaire_actuel": 45000,
                "experience_annees": 3,
            },
            {
                "nom": "Bernard",
                "practice_name": "Data",
                "grade": "Senior",
                "salaire_actuel": 60000,
                "experience_annees": 8,
            },
        ]

        self.ui_filters.filters["practice_filter"] = "Digital"
        self.ui_filters.filters["grade_filter"] = "Senior"
        self.ui_filters.filters["salaire_min"] = 50000

        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"

    def test_apply_filters_search_with_none_values(self):
        """Test recherche avec des valeurs None"""
        data = [
            {"nom": "Dupont", "prenom": None, "practice_name": "Digital"},
            {"nom": None, "prenom": "Marie", "practice_name": "Data"},
        ]

        self.ui_filters.filters["search_term"] = "marie"
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["prenom"] == "Marie"

    @patch("streamlit.sidebar")
    def test_render_filters_sidebar_mock(self, mock_sidebar):
        """Test basique du rendu des filtres (avec mocks)"""
        # Configuration basique des mocks
        mock_sidebar.header = MagicMock()
        mock_sidebar.text_input = MagicMock(return_value="")
        mock_sidebar.markdown = MagicMock()
        mock_sidebar.subheader = MagicMock()
        mock_sidebar.columns = MagicMock(return_value=(MagicMock(), MagicMock()))
        mock_sidebar.selectbox = MagicMock(return_value=None)
        mock_sidebar.number_input = MagicMock(return_value=0)
        mock_sidebar.date_input = MagicMock(return_value=None)
        mock_sidebar.button = MagicMock(return_value=False)

        # Test du rendu
        filters = self.ui_filters.render_filters_sidebar()

        # Vérifications basiques
        assert isinstance(filters, dict)
        mock_sidebar.header.assert_called()
        mock_sidebar.text_input.assert_called()


class TestRealTimeSearch:
    """Tests pour la classe RealTimeSearch"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.real_time_search = RealTimeSearch()

    def test_init(self):
        """Test de l'initialisation"""
        assert self.real_time_search.last_search_time == 0
        assert self.real_time_search.search_debounce_ms == 300

    def test_should_search_first_time(self):
        """Test première recherche (doit retourner True)"""
        result = self.real_time_search.should_search()
        assert result is True

    def test_should_search_debounce(self):
        """Test debounce de recherche"""
        # Première recherche
        result1 = self.real_time_search.should_search()
        assert result1 is True

        # Deuxième recherche immédiate (doit être bloquée)
        result2 = self.real_time_search.should_search()
        assert result2 is False

    def test_should_search_after_delay(self):
        """Test recherche après délai suffisant"""
        # Première recherche
        self.real_time_search.should_search()

        # Simuler un délai supérieur au debounce
        original_time = self.real_time_search.last_search_time
        self.real_time_search.last_search_time = original_time - 400  # 400ms avant

        # Deuxième recherche (doit être autorisée)
        result = self.real_time_search.should_search()
        assert result is True

    def test_search_debounce_timing(self):
        """Test précis du timing du debounce"""
        start_time = time.time() * 1000

        # Première recherche
        self.real_time_search.should_search()

        # Modifier manuellement le last_search_time pour simuler un timing précis
        self.real_time_search.last_search_time = start_time

        # Test avec délai insuffisant (290ms)
        current_time = start_time + 290
        with patch("time.time", return_value=current_time / 1000):
            result = self.real_time_search.should_search()
            assert result is False

        # Test avec délai suffisant (310ms)
        current_time = start_time + 310
        with patch("time.time", return_value=current_time / 1000):
            result = self.real_time_search.should_search()
            assert result is True

    def test_custom_debounce_time(self):
        """Test avec un temps de debounce personnalisé"""
        # Modifier le temps de debounce
        self.real_time_search.search_debounce_ms = 500

        # Première recherche
        self.real_time_search.should_search()
        original_time = self.real_time_search.last_search_time

        # Test avec délai insuffisant (400ms)
        self.real_time_search.last_search_time = original_time - 400
        result = self.real_time_search.should_search()
        assert result is False

        # Test avec délai suffisant (600ms)
        self.real_time_search.last_search_time = original_time - 600
        result = self.real_time_search.should_search()
        assert result is True

    def test_multiple_searches_pattern(self):
        """Test pattern de recherches multiples"""
        results = []

        # Première recherche
        results.append(self.real_time_search.should_search())

        # Plusieurs recherches rapides (toutes bloquées sauf la première)
        for _ in range(5):
            results.append(self.real_time_search.should_search())

        # Vérifier le pattern
        assert results[0] is True  # Première autorisée
        assert all(not result for result in results[1:])  # Autres bloquées

    def test_search_timing_precision(self):
        """Test de la précision du timing"""
        # Utiliser un mock pour contrôler précisément le temps
        with patch("time.time") as mock_time:
            mock_time.return_value = 1000.0  # 1000 secondes

            # Première recherche
            result1 = self.real_time_search.should_search()
            assert result1 is True

            # 200ms plus tard (insuffisant)
            mock_time.return_value = 1000.2
            result2 = self.real_time_search.should_search()
            assert result2 is False

            # 400ms plus tard (suffisant)
            mock_time.return_value = 1000.4
            result3 = self.real_time_search.should_search()
            assert result3 is True


class TestIntegrationEnhancedUI:
    """Tests d'intégration pour les composants enhanced_ui"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.ui_filters = AdvancedUIFilters()
        self.real_time_search = RealTimeSearch()

    def test_integration_filters_and_search(self):
        """Test d'intégration filtres + recherche"""
        # Données de test
        data = [
            {
                "nom": "Dupont",
                "prenom": "Jean",
                "practice_name": "Digital",
                "grade": "Senior",
                "salaire_actuel": 55000,
            },
            {
                "nom": "Martin",
                "prenom": "Marie",
                "practice_name": "Data",
                "grade": "Junior",
                "salaire_actuel": 45000,
            },
        ]

        # Appliquer des filtres
        self.ui_filters.filters["practice_filter"] = "Digital"
        self.ui_filters.filters["search_term"] = "jean"

        # Vérifier que la recherche est autorisée
        search_allowed = self.real_time_search.should_search()
        assert search_allowed is True

        # Appliquer les filtres
        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"

    def test_complex_filtering_scenario(self):
        """Test de scénario complexe de filtrage"""
        # Données complexes
        data = [
            {
                "nom": "Dupont",
                "prenom": "Jean",
                "practice_name": "Digital",
                "grade": "Senior",
                "salaire_actuel": 65000,
                "experience_annees": 8,
                "societe": "Quanteam",
                "type_contrat": "CDI",
                "disponibilite": True,
            },
            {
                "nom": "Martin",
                "prenom": "Marie",
                "practice_name": "Digital",
                "grade": "Junior",
                "salaire_actuel": 45000,
                "experience_annees": 3,
                "societe": "Quanteam",
                "type_contrat": "CDI",
                "disponibilite": False,
            },
            {
                "nom": "Bernard",
                "prenom": "Paul",
                "practice_name": "Data",
                "grade": "Senior",
                "salaire_actuel": 70000,
                "experience_annees": 10,
                "societe": "Asigma",
                "type_contrat": "CDI",
                "disponibilite": True,
            },
        ]

        # Filtres complexes
        self.ui_filters.filters["practice_filter"] = "Digital"
        self.ui_filters.filters["availability_filter"] = True
        self.ui_filters.filters["salaire_min"] = 50000
        self.ui_filters.filters["experience_min"] = 5
        self.ui_filters.filters["societe_filter"] = "Quanteam"

        result = self.ui_filters.apply_filters(data)
        assert len(result) == 1
        assert result[0]["nom"] == "Dupont"

    def test_performance_large_dataset(self):
        """Test de performance sur un grand dataset"""
        # Générer un dataset plus important
        large_data = []
        for i in range(1000):
            large_data.append(
                {
                    "nom": f"Nom{i}",
                    "prenom": f"Prenom{i}",
                    "practice_name": "Digital" if i % 2 == 0 else "Data",
                    "grade": "Senior" if i % 3 == 0 else "Junior",
                    "salaire_actuel": 40000 + (i * 100),
                    "experience_annees": i % 20,
                }
            )

        # Mesurer le temps d'exécution des filtres
        start_time = time.time()

        self.ui_filters.filters["practice_filter"] = "Digital"
        self.ui_filters.filters["salaire_min"] = 60000

        result = self.ui_filters.apply_filters(large_data)

        end_time = time.time()
        execution_time = end_time - start_time

        # Vérifier que l'exécution est raisonnable (< 1 seconde)
        assert execution_time < 1.0

        # Vérifier que les résultats sont corrects
        assert len(result) > 0
        assert all(item["practice_name"] == "Digital" for item in result)
        assert all(item["salaire_actuel"] >= 60000 for item in result)
