"""
Tests pour le module skill_categories.py
"""

import pytest
from app.utils.skill_categories import (
    COMPETENCES_TECHNIQUES,
    COMPETENCES_FONCTIONNELLES,
    NIVEAUX_MAITRISE,
    NIVEAUX_REQUIS,
    get_all_competences,
    get_competences_by_category,
    get_all_categories,
    search_competences,
)


class TestSkillCategories:
    """Tests pour les catégories de compétences"""

    def test_competences_techniques_structure(self):
        """Test que la structure des compétences techniques est correcte"""
        assert isinstance(COMPETENCES_TECHNIQUES, dict)
        assert len(COMPETENCES_TECHNIQUES) > 0

        # Vérifier qu'il y a au moins quelques catégories attendues
        expected_categories = ["Backend", "Frontend", "Data & Analytics"]
        for category in expected_categories:
            assert category in COMPETENCES_TECHNIQUES
            assert isinstance(COMPETENCES_TECHNIQUES[category], list)
            assert len(COMPETENCES_TECHNIQUES[category]) > 0

    def test_competences_fonctionnelles_structure(self):
        """Test que la structure des compétences fonctionnelles est correcte"""
        assert isinstance(COMPETENCES_FONCTIONNELLES, dict)
        assert len(COMPETENCES_FONCTIONNELLES) > 0

        # Vérifier qu'il y a au moins quelques catégories attendues
        expected_categories = ["Banque de Détail", "Marchés Financiers"]
        for category in expected_categories:
            assert category in COMPETENCES_FONCTIONNELLES
            assert isinstance(COMPETENCES_FONCTIONNELLES[category], list)
            assert len(COMPETENCES_FONCTIONNELLES[category]) > 0

    def test_niveaux_constantes(self):
        """Test des constantes de niveaux"""
        assert isinstance(NIVEAUX_MAITRISE, list)
        assert len(NIVEAUX_MAITRISE) == 4
        assert "Débutant" in NIVEAUX_MAITRISE
        assert "Expert" in NIVEAUX_MAITRISE

        assert isinstance(NIVEAUX_REQUIS, list)
        assert len(NIVEAUX_REQUIS) == 5
        assert "Junior" in NIVEAUX_REQUIS
        assert "Architect" in NIVEAUX_REQUIS

    def test_get_all_competences(self):
        """Test de la fonction get_all_competences"""
        result = get_all_competences()

        assert isinstance(result, dict)
        assert "techniques" in result
        assert "fonctionnelles" in result

        assert result["techniques"] == COMPETENCES_TECHNIQUES
        assert result["fonctionnelles"] == COMPETENCES_FONCTIONNELLES

    def test_get_competences_by_category(self):
        """Test de la fonction get_competences_by_category"""
        # Test catégorie techniques
        result = get_competences_by_category("techniques")
        assert result == COMPETENCES_TECHNIQUES

        # Test catégorie fonctionnelles
        result = get_competences_by_category("fonctionnelles")
        assert result == COMPETENCES_FONCTIONNELLES

        # Test catégorie invalide
        result = get_competences_by_category("invalide")
        assert result == {}

    def test_get_all_categories(self):
        """Test de la fonction get_all_categories"""
        result = get_all_categories()

        assert isinstance(result, dict)
        assert "techniques" in result
        assert "fonctionnelles" in result

        assert isinstance(result["techniques"], list)
        assert isinstance(result["fonctionnelles"], list)

        # Vérifier que les catégories correspondent
        assert set(result["techniques"]) == set(COMPETENCES_TECHNIQUES.keys())
        assert set(result["fonctionnelles"]) == set(COMPETENCES_FONCTIONNELLES.keys())

    def test_search_competences_exact_match(self):
        """Test de recherche avec correspondance exacte"""
        results = search_competences("Python")

        assert isinstance(results, list)
        assert len(results) > 0

        # Vérifier la structure du résultat
        for result in results:
            assert "nom" in result
            assert "categorie" in result
            assert "type" in result
            assert "Python" in result["nom"]

    def test_search_competences_partial_match(self):
        """Test de recherche avec correspondance partielle"""
        results = search_competences("Java")

        assert isinstance(results, list)
        assert len(results) > 0

        # Devrait trouver Java, JavaScript, etc.
        java_found = any("Java" in result["nom"] for result in results)
        assert java_found

    def test_search_competences_case_insensitive(self):
        """Test de recherche insensible à la casse"""
        results_upper = search_competences("PYTHON")
        results_lower = search_competences("python")

        assert len(results_upper) == len(results_lower)

        # Les résultats devraient être identiques
        upper_names = {r["nom"] for r in results_upper}
        lower_names = {r["nom"] for r in results_lower}
        assert upper_names == lower_names

    def test_search_competences_by_category(self):
        """Test de recherche dans une catégorie spécifique"""
        # Recherche dans techniques uniquement
        results = search_competences("Python", "techniques")

        assert isinstance(results, list)
        for result in results:
            assert result["type"] == "techniques"
            assert result["categorie"] in COMPETENCES_TECHNIQUES

    def test_search_competences_no_results(self):
        """Test de recherche sans résultats"""
        results = search_competences("competence_inexistante_12345")

        assert isinstance(results, list)
        assert len(results) == 0

    def test_search_competences_empty_query(self):
        """Test de recherche avec requête vide"""
        results = search_competences("")

        assert isinstance(results, list)
        # Devrait retourner tous les résultats ou aucun selon l'implémentation
        # Ici on teste juste que ça ne plante pas

    def test_search_competences_all_categories(self):
        """Test de recherche dans toutes les catégories"""
        results = search_competences("banque")

        assert isinstance(results, list)
        # Devrait trouver des compétences liées à la banque
        assert len(results) > 0

    def test_competences_data_integrity(self):
        """Test de l'intégrité des données de compétences"""
        all_competences = []

        # Collecter toutes les compétences
        for category_competences in COMPETENCES_TECHNIQUES.values():
            all_competences.extend(category_competences)

        for category_competences in COMPETENCES_FONCTIONNELLES.values():
            all_competences.extend(category_competences)

        # Vérifier qu'il n'y a pas de doublons
        unique_competences = set(all_competences)
        assert len(unique_competences) == len(all_competences)

        # Vérifier que toutes les compétences sont des strings non vides
        for competence in all_competences:
            assert isinstance(competence, str)
            assert len(competence.strip()) > 0

    def test_categories_data_integrity(self):
        """Test de l'intégrité des données de catégories"""
        # Vérifier que les clés de catégories sont des strings
        for category in COMPETENCES_TECHNIQUES.keys():
            assert isinstance(category, str)
            assert len(category.strip()) > 0

        for category in COMPETENCES_FONCTIONNELLES.keys():
            assert isinstance(category, str)
            assert len(category.strip()) > 0
