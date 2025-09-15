"""
Tests pour le référentiel des technologies
Tests unitaires pour technologies_referentiel.py
"""

import pytest
from app.utils.technologies_referentiel import (
    get_all_technologies,
    get_technologies_by_category,
    search_technologies,
    add_custom_technology,
    TECHNOLOGIES_REFERENTIEL,
    TECHNOLOGIES_POPULAIRES,
)


class TestTechnologiesReferentiel:
    """Tests pour les fonctions du référentiel des technologies"""

    def test_get_all_technologies_returns_list(self):
        """Test que get_all_technologies retourne une liste"""
        result = get_all_technologies()

        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_all_technologies_unique_and_sorted(self):
        """Test que get_all_technologies retourne des éléments uniques et triés"""
        result = get_all_technologies()

        # Vérifier qu'il n'y a pas de doublons
        assert len(result) == len(set(result))

        # Vérifier que c'est trié
        assert result == sorted(result)

    def test_get_all_technologies_contains_popular_techs(self):
        """Test que get_all_technologies contient les technologies populaires"""
        result = get_all_technologies()

        # Vérifier que certaines technologies populaires sont présentes
        # (toutes ne sont pas forcément dans la liste complète)
        popular_found = 0
        for tech in TECHNOLOGIES_POPULAIRES:
            if tech in result:
                popular_found += 1

        # Au moins 50% des technologies populaires devraient être dans la liste
        assert popular_found >= len(TECHNOLOGIES_POPULAIRES) // 2

    def test_get_technologies_by_category_structure(self):
        """Test que get_technologies_by_category retourne la bonne structure"""
        result = get_technologies_by_category()

        assert isinstance(result, dict)
        assert len(result) > 0

        for category, techs in result.items():
            assert isinstance(category, str)
            assert isinstance(techs, list)
            assert len(techs) > 0

            for tech in techs:
                assert isinstance(tech, str)
                assert len(tech.strip()) > 0

    def test_get_technologies_by_category_matches_original(self):
        """Test que get_technologies_by_category retourne les mêmes données que TECHNOLOGIES_REFERENTIEL"""
        result = get_technologies_by_category()

        assert result == TECHNOLOGIES_REFERENTIEL

    def test_search_technologies_exact_match(self):
        """Test recherche de technologies avec correspondance exacte"""
        result = search_technologies("Python")

        assert isinstance(result, list)
        assert "Python" in result

    def test_search_technologies_partial_match(self):
        """Test recherche de technologies avec correspondance partielle"""
        result = search_technologies("React")

        assert isinstance(result, list)
        assert len(result) > 0

        # Vérifier que tous les résultats contiennent "React"
        for tech in result:
            assert "react" in tech.lower()

    def test_search_technologies_case_insensitive(self):
        """Test que la recherche est insensible à la casse"""
        result_upper = search_technologies("PYTHON")
        result_lower = search_technologies("python")

        assert len(result_upper) == len(result_lower)

        # Les résultats devraient être identiques
        assert set(result_upper) == set(result_lower)

    def test_search_technologies_no_results(self):
        """Test recherche sans résultats"""
        result = search_technologies("technologienonexistante12345")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_search_technologies_empty_query(self):
        """Test recherche avec requête vide"""
        result = search_technologies("")

        assert isinstance(result, list)
        # Une requête vide devrait retourner tous les résultats
        all_techs = get_all_technologies()
        assert len(result) == len(all_techs)

    def test_add_custom_technology_new_category(self):
        """Test ajout d'une technologie dans une nouvelle catégorie"""
        # Utiliser une catégorie qui n'existe pas
        test_category = "TestCategory123"
        test_tech = "TestTechnology123"

        # S'assurer que la catégorie n'existe pas au départ
        assert test_category not in TECHNOLOGIES_REFERENTIEL

        # Ajouter la technologie
        result = add_custom_technology(test_category, test_tech)

        assert result is True
        assert test_category in TECHNOLOGIES_REFERENTIEL
        assert test_tech in TECHNOLOGIES_REFERENTIEL[test_category]

        # Nettoyer après le test
        del TECHNOLOGIES_REFERENTIEL[test_category]

    def test_add_custom_technology_existing_category(self):
        """Test ajout d'une technologie dans une catégorie existante"""
        test_category = "Langages de programmation"
        test_tech = "TestLangage123"

        # S'assurer que la technologie n'existe pas
        assert test_tech not in TECHNOLOGIES_REFERENTIEL[test_category]

        # Ajouter la technologie
        result = add_custom_technology(test_category, test_tech)

        assert result is True
        assert test_tech in TECHNOLOGIES_REFERENTIEL[test_category]

        # Nettoyer après le test
        TECHNOLOGIES_REFERENTIEL[test_category].remove(test_tech)

    def test_add_custom_technology_duplicate(self):
        """Test ajout d'une technologie qui existe déjà"""
        test_category = "Langages de programmation"
        existing_tech = "Python"  # Existe déjà

        # Vérifier qu'elle existe
        assert existing_tech in TECHNOLOGIES_REFERENTIEL[test_category]

        # Tenter de l'ajouter à nouveau
        result = add_custom_technology(test_category, existing_tech)

        assert result is False

    def test_technologies_referentiel_structure(self):
        """Test que TECHNOLOGIES_REFERENTIEL a la bonne structure"""
        assert isinstance(TECHNOLOGIES_REFERENTIEL, dict)
        assert len(TECHNOLOGIES_REFERENTIEL) > 0

        for category, techs in TECHNOLOGIES_REFERENTIEL.items():
            assert isinstance(category, str)
            assert isinstance(techs, list)
            assert len(techs) > 0

            for tech in techs:
                assert isinstance(tech, str)
                assert len(tech.strip()) > 0

    def test_technologies_populaires_content(self):
        """Test que TECHNOLOGIES_POPULAIRES contient des technologies valides"""
        assert isinstance(TECHNOLOGIES_POPULAIRES, list)
        assert len(TECHNOLOGIES_POPULAIRES) > 0

        # Vérifier que les technologies populaires sont des chaînes non vides
        for popular_tech in TECHNOLOGIES_POPULAIRES:
            assert isinstance(popular_tech, str)
            assert len(popular_tech.strip()) > 0

        # Vérifier que certaines technologies populaires sont dans le référentiel complet
        all_techs = get_all_technologies()
        popular_found = sum(1 for popular_tech in TECHNOLOGIES_POPULAIRES if popular_tech in all_techs)

        # Au moins certaines technologies populaires devraient être dans la liste complète
        assert popular_found > 0

    def test_search_technologies_result_consistency(self):
        """Test que les résultats de recherche sont cohérents"""
        query = "Java"
        result = search_technologies(query)

        # Vérifier que tous les résultats contiennent la requête
        for tech in result:
            assert query.lower() in tech.lower()

        # Vérifier que les résultats sont uniques
        assert len(result) == len(set(result))

    def test_get_all_technologies_no_duplicates_from_categories(self):
        """Test qu'il n'y a pas de doublons entre catégories dans get_all_technologies"""
        result = get_all_technologies()

        # Compter les occurrences de chaque technologie
        tech_counts = {}
        for tech in result:
            tech_counts[tech] = tech_counts.get(tech, 0) + 1

        # Vérifier qu'aucune technologie n'apparaît plus d'une fois
        for tech, count in tech_counts.items():
            assert count == 1
