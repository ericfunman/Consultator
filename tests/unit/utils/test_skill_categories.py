"""
Tests pour le module skill_categories.py
"""

import pytest

from app.utils.skill_categories import COMPETENCES_FONCTIONNELLES
from app.utils.skill_categories import COMPETENCES_TECHNIQUES
from app.utils.skill_categories import NIVEAUX_MAITRISE
from app.utils.skill_categories import NIVEAUX_REQUIS
from app.utils.skill_categories import get_all_categories
from app.utils.skill_categories import get_all_competences
from app.utils.skill_categories import get_all_skills
from app.utils.skill_categories import get_category_for_skill
from app.utils.skill_categories import get_competences_by_category
from app.utils.skill_categories import search_competences


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


class TestGetCategoryForSkill:
    """Tests pour la fonction get_category_for_skill"""

    def test_get_category_for_skill_backend(self):
        """Test catégorie pour compétence Backend"""
        assert get_category_for_skill("Python") == "Backend"
        assert get_category_for_skill("Java") == "Backend"
        assert get_category_for_skill("Spring Boot") == "Backend"

    def test_get_category_for_skill_frontend(self):
        """Test catégorie pour compétence Frontend"""
        assert get_category_for_skill("React") == "Frontend"
        assert get_category_for_skill("Angular") == "Frontend"
        assert get_category_for_skill("Vue.js") == "Frontend"

    def test_get_category_for_skill_mobile(self):
        """Test catégorie pour compétence Mobile"""
        assert get_category_for_skill("React Native") == "Mobile"
        assert get_category_for_skill("Flutter") == "Mobile"

    def test_get_category_for_skill_data(self):
        """Test catégorie pour compétence Data"""
        assert get_category_for_skill("SQL") == "Data & Analytics"
        assert get_category_for_skill("Pandas") == "Data & Analytics"

    def test_get_category_for_skill_cloud(self):
        """Test catégorie pour compétence Cloud"""
        assert get_category_for_skill("AWS") == "Cloud & DevOps"
        assert get_category_for_skill("Docker") == "Cloud & DevOps"

    def test_get_category_for_skill_database(self):
        """Test catégorie pour compétence Base de données"""
        assert get_category_for_skill("PostgreSQL") == "Base de données"
        assert get_category_for_skill("MongoDB") == "Base de données"

    def test_get_category_for_skill_fonctionnelle(self):
        """Test catégorie pour compétence fonctionnelle"""
        result = get_category_for_skill("Crédit immobilier")
        assert result == "Banque de Détail"

    def test_get_category_for_skill_case_insensitive(self):
        """Test insensibilité à la casse"""
        assert get_category_for_skill("python") == "Backend"
        assert get_category_for_skill("PYTHON") == "Backend"
        assert get_category_for_skill("PyThOn") == "Backend"

    def test_get_category_for_skill_not_found(self):
        """Test compétence non trouvée"""
        assert get_category_for_skill("CompétenceInexistante") == "Autre"
        assert get_category_for_skill("XYZ123") == "Autre"

    def test_get_category_for_skill_empty(self):
        """Test avec chaîne vide"""
        assert get_category_for_skill("") == "Autre"

    def test_get_category_for_skill_none(self):
        """Test avec None"""
        assert get_category_for_skill(None) == "Autre"

    def test_get_category_for_skill_whitespace(self):
        """Test avec espaces"""
        result = get_category_for_skill("React Native")
        assert result == "Mobile"


class TestGetAllSkills:
    """Tests pour la fonction get_all_skills"""

    def test_get_all_skills_returns_list(self):
        """Test que la fonction retourne une liste"""
        result = get_all_skills()
        assert isinstance(result, list)

    def test_get_all_skills_not_empty(self):
        """Test que la liste n'est pas vide"""
        result = get_all_skills()
        assert len(result) > 0

    def test_get_all_skills_contains_techniques(self):
        """Test que la liste contient des compétences techniques"""
        result = get_all_skills()
        
        assert "Python" in result
        assert "Java" in result
        assert "React" in result
        assert "Docker" in result

    def test_get_all_skills_contains_fonctionnelles(self):
        """Test que la liste contient des compétences fonctionnelles"""
        result = get_all_skills()
        
        # Vérifier au moins une compétence fonctionnelle
        has_functional = any(
            skill in result 
            for category_skills in COMPETENCES_FONCTIONNELLES.values() 
            for skill in category_skills
        )
        assert has_functional

    def test_get_all_skills_sorted(self):
        """Test que la liste est triée"""
        result = get_all_skills()
        assert result == sorted(result)

    def test_get_all_skills_no_duplicates(self):
        """Test absence de doublons"""
        result = get_all_skills()
        assert len(result) == len(set(result))

    def test_get_all_skills_all_strings(self):
        """Test que tous les éléments sont des strings"""
        result = get_all_skills()
        
        for skill in result:
            assert isinstance(skill, str)
            assert len(skill) > 0

    def test_get_all_skills_count(self):
        """Test nombre total approximatif de compétences"""
        result = get_all_skills()
        
        # Compter manuellement (approximatif)
        manual_count = sum(len(skills) for skills in COMPETENCES_TECHNIQUES.values())
        manual_count += sum(len(skills) for skills in COMPETENCES_FONCTIONNELLES.values())
        
        # Le résultat peut être <= au compte manuel (doublons éliminés)
        assert len(result) <= manual_count
        assert len(result) > 0


class TestIntegration:
    """Tests d'intégration entre les fonctions"""

    def test_all_skills_have_categories(self):
        """Test que toutes les compétences ont une catégorie"""
        all_skills = get_all_skills()
        
        # Tester un échantillon
        for skill in all_skills[:20]:
            category = get_category_for_skill(skill)
            # Ne devrait pas être "Autre" pour les compétences du référentiel
            assert category != "Autre"

    def test_search_and_get_category_consistency(self):
        """Test cohérence entre search et get_category"""
        search_results = search_competences("Python")
        
        for result in search_results:
            if result["nom"] == "Python":
                category_from_search = result["categorie"]
                category_from_get = get_category_for_skill("Python")
                assert category_from_search == category_from_get
                break

    def test_get_all_and_get_category(self):
        """Test cohérence entre get_all_skills et get_category"""
        all_skills = get_all_skills()
        
        # Prendre quelques compétences et vérifier leur catégorie
        sample_skills = all_skills[:10]
        
        for skill in sample_skills:
            category = get_category_for_skill(skill)
            # Doit être une catégorie valide
            assert isinstance(category, str)
            assert len(category) > 0
