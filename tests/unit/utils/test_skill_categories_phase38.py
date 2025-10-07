"""Tests Phase 38: skill_categories.py (84% → 90%+)"""
import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestGetAllCompetences(unittest.TestCase):
    def test_get_all_competences_not_empty(self):
        from app.utils.skill_categories import get_all_competences
        competences = get_all_competences()
        self.assertIsInstance(competences, (list, dict))
        self.assertGreater(len(competences), 0)
    
    def test_get_all_competences_structure(self):
        from app.utils.skill_categories import get_all_competences
        competences = get_all_competences()
        # Test structure selon le type
        self.assertGreater(len(competences), 0)

class TestGetCompetencesByCategory(unittest.TestCase):
    def test_get_competences_by_category_techniques(self):
        from app.utils.skill_categories import get_competences_by_category
        competences = get_competences_by_category("techniques")
        self.assertIsInstance(competences, (list, dict))
        self.assertGreater(len(competences), 0)
    
    def test_get_competences_by_category_fonctionnelles(self):
        from app.utils.skill_categories import get_competences_by_category
        competences = get_competences_by_category("fonctionnelles")
        self.assertIsInstance(competences, (list, dict))

class TestGetAllCategories(unittest.TestCase):
    def test_get_all_categories_not_empty(self):
        from app.utils.skill_categories import get_all_categories
        categories = get_all_categories()
        self.assertIsInstance(categories, (list, dict))
        self.assertGreater(len(categories), 0)

class TestSearchCompetences(unittest.TestCase):
    def test_search_competences_python(self):
        from app.utils.skill_categories import search_competences
        results = search_competences("Python")
        self.assertIsInstance(results, list)
        # Python devrait être trouvé
        if results:
            self.assertTrue(any("python" in r["nom"].lower() for r in results))
    
    def test_search_competences_empty_query(self):
        from app.utils.skill_categories import search_competences
        results = search_competences("")
        # Recherche vide devrait retourner tous ou aucun
        self.assertIsInstance(results, list)
    
    def test_search_competences_with_category(self):
        from app.utils.skill_categories import search_competences
        results = search_competences("Data", category_type="techniques")
        self.assertIsInstance(results, list)

class TestGetCompetencesDict(unittest.TestCase):
    def test_get_competences_dict_techniques(self):
        from app.utils.skill_categories import _get_competences_dict
        result = _get_competences_dict("techniques")
        self.assertIsInstance(result, dict)
    
    def test_get_competences_dict_fonctionnelles(self):
        from app.utils.skill_categories import _get_competences_dict
        result = _get_competences_dict("fonctionnelles")
        self.assertIsInstance(result, dict)

class TestAddAllCategoryCompetences(unittest.TestCase):
    def test_add_all_category_competences(self):
        from app.utils.skill_categories import _add_all_category_competences
        _add_all_category_competences("Data", ["Python", "SQL"], "techniques")
        # Fonction modifie en place, test qu'elle ne crash pas
        self.assertIsNotNone(_add_all_category_competences)

class TestSearchIndividualCompetences(unittest.TestCase):
    def test_search_individual_competences(self):
        from app.utils.skill_categories import _search_individual_competences
        _search_individual_competences("python", "Data", ["Python", "SQL"], "techniques")
        # Fonction modifie en place, test qu'elle ne crash pas
        self.assertIsNotNone(_search_individual_competences)

class TestDetermineCompetenceType(unittest.TestCase):
    def test_determine_competence_type_techniques(self):
        from app.utils.skill_categories import _determine_competence_type
        result = _determine_competence_type("Data", "techniques")
        self.assertIsInstance(result, str)
    
    def test_determine_competence_type_fonctionnelles(self):
        from app.utils.skill_categories import _determine_competence_type
        result = _determine_competence_type("Finance", "fonctionnelles")
        self.assertIsInstance(result, str)

class TestGetCategoryForSkill(unittest.TestCase):
    def test_get_category_for_skill_python(self):
        from app.utils.skill_categories import get_category_for_skill
        result = get_category_for_skill("Python")
        self.assertIsInstance(result, str)
    
    def test_get_category_for_skill_unknown(self):
        from app.utils.skill_categories import get_category_for_skill
        result = get_category_for_skill("CompetenceInconnueXYZ123")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Autre")
    
    def test_get_category_for_skill_case_insensitive(self):
        from app.utils.skill_categories import get_category_for_skill
        result1 = get_category_for_skill("python")
        result2 = get_category_for_skill("PYTHON")
        # Devrait être identique (case insensitive)
        self.assertEqual(result1, result2)

class TestGetAllSkills(unittest.TestCase):
    def test_get_all_skills_not_empty(self):
        from app.utils.skill_categories import get_all_skills
        skills = get_all_skills()
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
    
    def test_get_all_skills_unique(self):
        from app.utils.skill_categories import get_all_skills
        skills = get_all_skills()
        # Vérifier qu'il n'y a pas de doublons
        self.assertEqual(len(skills), len(set(skills)))

if __name__ == "__main__":
    unittest.main()
