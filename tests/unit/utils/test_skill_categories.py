"""
Tests pour les utilitaires de compétences
Tests unitaires pour skill_categories.py
"""

import pytest
from app.utils.skill_categories import (
    get_all_competences,
    get_competences_by_category,
    get_all_categories,
    search_competences,
    COMPETENCES_TECHNIQUES,
    COMPETENCES_FONCTIONNELLES,
    NIVEAUX_MAITRISE,
    NIVEAUX_REQUIS,
)


class TestSkillCategories:
    """Tests pour les fonctions de gestion des compétences"""

    def test_get_all_competences_structure(self):
        """Test que get_all_competences retourne la bonne structure"""
        result = get_all_competences()

        assert isinstance(result, dict)
        assert "techniques" in result
        assert "fonctionnelles" in result
        assert isinstance(result["techniques"], dict)
        assert isinstance(result["fonctionnelles"], dict)

    def test_get_all_competences_content(self):
        """Test que get_all_competences contient les bonnes données"""
        result = get_all_competences()

        # Vérifier que les données techniques sont présentes
        assert "Backend" in result["techniques"]
        assert "Frontend" in result["techniques"]
        assert "Python" in result["techniques"]["Backend"]
        assert "React" in result["techniques"]["Frontend"]

        # Vérifier que les données fonctionnelles sont présentes
        assert "Banque de Détail" in result["fonctionnelles"]
        assert "Marchés Financiers" in result["fonctionnelles"]

    def test_get_competences_by_category_techniques(self):
        """Test récupération des compétences techniques"""
        result = get_competences_by_category("techniques")

        assert isinstance(result, dict)
        assert "Backend" in result
        assert "Frontend" in result
        assert isinstance(result["Backend"], list)
        assert "Python" in result["Backend"]

    def test_get_competences_by_category_fonctionnelles(self):
        """Test récupération des compétences fonctionnelles"""
        result = get_competences_by_category("fonctionnelles")

        assert isinstance(result, dict)
        assert "Banque de Détail" in result
        assert "Marchés Financiers" in result
        assert isinstance(result["Banque de Détail"], list)

    def test_get_competences_by_category_invalid(self):
        """Test récupération avec catégorie invalide"""
        result = get_competences_by_category("invalid")

        assert isinstance(result, dict)
        assert len(result) == 0

    def test_get_all_categories_structure(self):
        """Test que get_all_categories retourne la bonne structure"""
        result = get_all_categories()

        assert isinstance(result, dict)
        assert "techniques" in result
        assert "fonctionnelles" in result
        assert isinstance(result["techniques"], list)
        assert isinstance(result["fonctionnelles"], list)

    def test_get_all_categories_content(self):
        """Test que get_all_categories contient les bonnes catégories"""
        result = get_all_categories()

        # Vérifier les catégories techniques
        assert "Backend" in result["techniques"]
        assert "Frontend" in result["techniques"]
        assert "Data & Analytics" in result["techniques"]

        # Vérifier les catégories fonctionnelles
        assert "Banque de Détail" in result["fonctionnelles"]
        assert "Marchés Financiers" in result["fonctionnelles"]

    def test_search_competences_exact_match(self):
        """Test recherche de compétences avec correspondance exacte"""
        result = search_competences("Python")

        assert isinstance(result, list)
        assert len(result) > 0

        # Vérifier qu'au moins un résultat contient Python
        python_found = any(r["nom"] == "Python" for r in result)
        assert python_found

    def test_search_competences_partial_match(self):
        """Test recherche de compétences avec correspondance partielle"""
        result = search_competences("React")

        assert isinstance(result, list)
        assert len(result) > 0

        # Vérifier que tous les résultats contiennent "React"
        for r in result:
            assert "react" in r["nom"].lower()

    def test_search_competences_case_insensitive(self):
        """Test que la recherche est insensible à la casse"""
        result_upper = search_competences("PYTHON")
        result_lower = search_competences("python")

        assert len(result_upper) == len(result_lower)

    def test_search_competences_by_category(self):
        """Test recherche dans une catégorie spécifique"""
        result = search_competences("Python", "techniques")

        assert isinstance(result, list)
        for r in result:
            assert r["type"] == "techniques"

    def test_search_competences_no_results(self):
        """Test recherche sans résultats"""
        result = search_competences("technologienonexistante")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_search_competences_empty_query(self):
        """Test recherche avec requête vide"""
        result = search_competences("")

        assert isinstance(result, list)
        # Une requête vide devrait retourner tous les résultats ou aucun
        # selon l'implémentation

    def test_competences_techniques_structure(self):
        """Test que COMPETENCES_TECHNIQUES a la bonne structure"""
        assert isinstance(COMPETENCES_TECHNIQUES, dict)

        for category, skills in COMPETENCES_TECHNIQUES.items():
            assert isinstance(category, str)
            assert isinstance(skills, list)
            assert len(skills) > 0

            for skill in skills:
                assert isinstance(skill, str)
                assert len(skill.strip()) > 0

    def test_competences_fonctionnelles_structure(self):
        """Test que COMPETENCES_FONCTIONNELLES a la bonne structure"""
        assert isinstance(COMPETENCES_FONCTIONNELLES, dict)

        for category, skills in COMPETENCES_FONCTIONNELLES.items():
            assert isinstance(category, str)
            assert isinstance(skills, list)
            assert len(skills) > 0

            for skill in skills:
                assert isinstance(skill, str)
                assert len(skill.strip()) > 0

    def test_niveaux_maitrise_content(self):
        """Test que NIVEAUX_MAITRISE contient les bonnes valeurs"""
        assert isinstance(NIVEAUX_MAITRISE, list)
        assert len(NIVEAUX_MAITRISE) == 4
        assert "Débutant" in NIVEAUX_MAITRISE
        assert "Expert" in NIVEAUX_MAITRISE

    def test_niveaux_requis_content(self):
        """Test que NIVEAUX_REQUIS contient les bonnes valeurs"""
        assert isinstance(NIVEAUX_REQUIS, list)
        assert len(NIVEAUX_REQUIS) == 5
        assert "Junior" in NIVEAUX_REQUIS
        assert "Architect" in NIVEAUX_REQUIS

    def test_search_competences_result_structure(self):
        """Test que les résultats de recherche ont la bonne structure"""
        result = search_competences("Python")

        for item in result:
            assert isinstance(item, dict)
            assert "nom" in item
            assert "categorie" in item
            assert "type" in item
            assert isinstance(item["nom"], str)
            assert isinstance(item["categorie"], str)
            assert isinstance(item["type"], str)
