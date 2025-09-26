"""
Tests pour le module technologies_referentiel.py
"""

import pytest

from app.utils.technologies_referentiel import TECHNOLOGIES_POPULAIRES
from app.utils.technologies_referentiel import TECHNOLOGIES_REFERENTIEL
from app.utils.technologies_referentiel import add_custom_technology
from app.utils.technologies_referentiel import get_all_technologies
from app.utils.technologies_referentiel import get_technologies_by_category
from app.utils.technologies_referentiel import search_technologies


class TestTechnologiesReferentiel:
    """Tests pour le référentiel des technologies"""

    def test_technologies_referentiel_structure(self):
        """Test que la structure du référentiel est correcte"""
        assert isinstance(TECHNOLOGIES_REFERENTIEL, dict)
        assert len(TECHNOLOGIES_REFERENTIEL) > 0

        # Vérifier qu'il y a au moins quelques catégories attendues
        expected_categories = [
            "Langages de programmation",
            "Frameworks Web",
            "Bases de données",
        ]
        for category in expected_categories:
            assert category in TECHNOLOGIES_REFERENTIEL
            assert isinstance(TECHNOLOGIES_REFERENTIEL[category], list)
            assert len(TECHNOLOGIES_REFERENTIEL[category]) > 0

    def test_technologies_populaires(self):
        """Test de la liste des technologies populaires"""
        assert isinstance(TECHNOLOGIES_POPULAIRES, list)
        assert len(TECHNOLOGIES_POPULAIRES) > 0

        # Vérifier que toutes les technologies populaires sont dans le référentiel
        all_techs = get_all_technologies()
        for tech in TECHNOLOGIES_POPULAIRES:
            assert tech in all_techs

    def test_get_all_technologies(self):
        """Test de la fonction get_all_technologies"""
        result = get_all_technologies()

        assert isinstance(result, list)
        assert len(result) > 0

        # Vérifier que c'est trié
        assert result == sorted(result)

        # Vérifier qu'il n'y a pas de doublons
        assert len(result) == len(set(result))

        # Vérifier que toutes les technologies sont des strings
        for tech in result:
            assert isinstance(tech, str)
            assert len(tech.strip()) > 0

    def test_get_technologies_by_category(self):
        """Test de la fonction get_technologies_by_category"""
        result = get_technologies_by_category()

        assert isinstance(result, dict)
        assert result == TECHNOLOGIES_REFERENTIEL

        # Vérifier que chaque catégorie a une liste
        for category, techs in result.items():
            assert isinstance(category, str)
            assert isinstance(techs, list)
            assert len(techs) > 0

    def test_search_technologies_exact_match(self):
        """Test de recherche avec correspondance exacte"""
        results = search_technologies("Python")

        assert isinstance(results, list)
        assert len(results) > 0
        assert "Python" in results

    def test_search_technologies_partial_match(self):
        """Test de recherche avec correspondance partielle"""
        results = search_technologies("Java")

        assert isinstance(results, list)
        assert len(results) > 0

        # Devrait contenir plusieurs variantes de Java
        java_variants = [tech for tech in results if "Java" in tech]
        assert len(java_variants) > 0

    def test_search_technologies_case_insensitive(self):
        """Test de recherche insensible à la casse"""
        results_upper = search_technologies("PYTHON")
        results_lower = search_technologies("python")

        assert len(results_upper) == len(results_lower)

        # Les résultats devraient être identiques
        assert set(results_upper) == set(results_lower)

    def test_search_technologies_no_results(self):
        """Test de recherche sans résultats"""
        results = search_technologies("technologie_inexistante_12345")

        assert isinstance(results, list)
        assert len(results) == 0

    def test_search_technologies_empty_query(self):
        """Test de recherche avec requête vide"""
        results = search_technologies("")

        assert isinstance(results, list)
        # Devrait retourner tous les résultats
        all_techs = get_all_technologies()
        assert len(results) == len(all_techs)

    def test_add_custom_technology_new_category(self):
        """Test d'ajout d'une technologie dans une nouvelle catégorie"""
        # Sauvegarder l'état initial
        initial_categories = list(TECHNOLOGIES_REFERENTIEL.keys())

        # Ajouter une technologie dans une nouvelle catégorie
        result = add_custom_technology("Test Category", "Test Technology")

        assert result is True
        assert "Test Category" in TECHNOLOGIES_REFERENTIEL
        assert "Test Technology" in TECHNOLOGIES_REFERENTIEL["Test Category"]

        # Nettoyer
        del TECHNOLOGIES_REFERENTIEL["Test Category"]

    def test_add_custom_technology_existing_category(self):
        """Test d'ajout d'une technologie dans une catégorie existante"""
        # Utiliser une catégorie existante
        category = list(TECHNOLOGIES_REFERENTIEL.keys())[0]
        initial_count = len(TECHNOLOGIES_REFERENTIEL[category])

        # Ajouter une technologie
        result = add_custom_technology(category, "Test Technology Unique")

        assert result is True
        assert len(TECHNOLOGIES_REFERENTIEL[category]) == initial_count + 1
        assert "Test Technology Unique" in TECHNOLOGIES_REFERENTIEL[category]

        # Nettoyer
        TECHNOLOGIES_REFERENTIEL[category].remove("Test Technology Unique")

    def test_add_custom_technology_duplicate(self):
        """Test d'ajout d'une technologie déjà existante"""
        # Utiliser une technologie existante
        category = list(TECHNOLOGIES_REFERENTIEL.keys())[0]
        existing_tech = TECHNOLOGIES_REFERENTIEL[category][0]

        # Essayer d'ajouter la même technologie
        result = add_custom_technology(category, existing_tech)

        assert result is False
        # Vérifier qu'elle n'a pas été ajoutée en double
        count = TECHNOLOGIES_REFERENTIEL[category].count(existing_tech)
        assert count == 1

    def test_technologies_data_integrity(self):
        """Test de l'intégrité des données de technologies"""
        all_techs = get_all_technologies()

        # Vérifier qu'il n'y a pas de doublons dans la liste complète
        unique_techs = set(all_techs)
        assert len(unique_techs) == len(all_techs)

        # Vérifier que toutes les technologies sont des strings non vides
        for tech in all_techs:
            assert isinstance(tech, str)
            assert len(tech.strip()) > 0

    def test_categories_data_integrity(self):
        """Test de l'intégrité des données de catégories"""
        # Vérifier que les clés de catégories sont des strings
        for category in TECHNOLOGIES_REFERENTIEL.keys():
            assert isinstance(category, str)
            assert len(category.strip()) > 0

        # Vérifier que chaque catégorie a au moins une technologie
        for category, techs in TECHNOLOGIES_REFERENTIEL.items():
            assert len(techs) > 0

    def test_popular_technologies_coverage(self):
        """Test que les technologies populaires sont bien couvertes"""
        all_techs = get_all_technologies()

        for popular_tech in TECHNOLOGIES_POPULAIRES:
            assert (
                popular_tech in all_techs
            ), f"Technologie populaire '{popular_tech}' manquante du référentiel"

    def test_search_technologies_special_characters(self):
        """Test de recherche avec caractères spéciaux"""
        # Tester avec des points, des espaces, etc.
        results = search_technologies("C#")
        assert len(results) > 0
        assert any("C#" in tech for tech in results)

        results = search_technologies("C++")
        assert len(results) > 0
        assert any("C++" in tech for tech in results)

    def test_search_technologies_numbers(self):
        """Test de recherche avec des numéros de version"""
        results = search_technologies("3.8")
        assert len(results) > 0
        assert any("3.8" in tech for tech in results)

    def test_get_all_technologies_no_duplicates_across_categories(self):
        """Test qu'il n'y a pas de doublons entre catégories différentes"""
        # Certaines technologies peuvent apparaître dans plusieurs catégories
        # mais get_all_technologies() doit les dédupliquer
        all_techs = get_all_technologies()

        # Vérifier qu'il n'y a pas de doublons dans le résultat final
        assert len(all_techs) == len(set(all_techs))

    def test_add_custom_technology_sorting(self):
        """Test que l'ajout maintient le tri alphabétique"""
        category = "Test Sort Category"
        add_custom_technology(category, "Z Technology")
        add_custom_technology(category, "A Technology")
        add_custom_technology(category, "M Technology")

        techs = TECHNOLOGIES_REFERENTIEL[category]
        assert techs == sorted(techs)

        # Nettoyer
        del TECHNOLOGIES_REFERENTIEL[category]
