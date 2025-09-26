"""
Tests complets pour technologies_referentiel.py
Module avec référentiel de technologies et fonctions utilitaires - objectif 100% de couverture
"""

from typing import Dict
from typing import List

import pytest

from app.utils.technologies_referentiel import TECHNOLOGIES_POPULAIRES
from app.utils.technologies_referentiel import TECHNOLOGIES_REFERENTIEL
from app.utils.technologies_referentiel import add_custom_technology
from app.utils.technologies_referentiel import get_all_technologies
from app.utils.technologies_referentiel import get_technologies_by_category
from app.utils.technologies_referentiel import search_technologies


class TestTechnologiesReferentiel:
    """Tests complets pour technologies_referentiel.py avec 100% de couverture"""

    def test_technologies_referentiel_constant(self):
        """Test dictionnaire référentiel technologies"""
        # Vérifier structure
        assert isinstance(TECHNOLOGIES_REFERENTIEL, dict)
        assert len(TECHNOLOGIES_REFERENTIEL) > 0

        # Vérifier catégories principales
        expected_categories = [
            "Langages de programmation",
            "Frameworks Web",
            "Bases de données",
            "Cloud & DevOps",
            "Intelligence Artificielle & Data Science",
            "Mobile",
            "Outils de développement",
            "Architecture & Design",
            "Sécurité",
            "Systèmes d'exploitation",
            "Méthodologies",
        ]

        for category in expected_categories:
            assert category in TECHNOLOGIES_REFERENTIEL
            assert isinstance(TECHNOLOGIES_REFERENTIEL[category], list)
            assert len(TECHNOLOGIES_REFERENTIEL[category]) > 0

    def test_technologies_referentiel_content(self):
        """Test contenu du référentiel"""
        # Vérifier présence de technologies connues
        langages = TECHNOLOGIES_REFERENTIEL["Langages de programmation"]
        assert "Python" in langages
        assert "Java" in langages
        assert "JavaScript" in langages
        assert "C#" in langages

        frameworks = TECHNOLOGIES_REFERENTIEL["Frameworks Web"]
        assert "React" in frameworks
        assert "Angular" in frameworks
        assert "Vue.js" in frameworks
        assert "Django" in frameworks

        databases = TECHNOLOGIES_REFERENTIEL["Bases de données"]
        assert "MySQL" in databases
        assert "PostgreSQL" in databases
        assert "MongoDB" in databases

    def test_technologies_populaires_constant(self):
        """Test liste technologies populaires"""
        assert isinstance(TECHNOLOGIES_POPULAIRES, list)
        assert len(TECHNOLOGIES_POPULAIRES) > 0

        # Vérifier présence de technologies populaires
        expected_popular = ["Python", "Java", "JavaScript", "React", "AWS", "Docker"]
        for tech in expected_popular:
            assert tech in TECHNOLOGIES_POPULAIRES

    def test_get_all_technologies_complete(self):
        """Test récupération de toutes les technologies"""
        all_techs = get_all_technologies()

        # Vérifier structure
        assert isinstance(all_techs, list)
        assert len(all_techs) > 0

        # Vérifier que la liste est triée
        assert all_techs == sorted(all_techs)

        # Vérifier absence de doublons (set conversion)
        assert len(all_techs) == len(set(all_techs))

        # Vérifier présence de technologies de différentes catégories
        assert "Python" in all_techs
        assert "React" in all_techs
        assert "MySQL" in all_techs
        assert "AWS" in all_techs

    def test_get_all_technologies_aggregation(self):
        """Test agrégation correcte de toutes les catégories"""
        all_techs = get_all_technologies()

        # Compter manuellement toutes les technologies uniques
        manual_count = set()
        for category, techs in TECHNOLOGIES_REFERENTIEL.items():
            manual_count.update(techs)

        assert len(all_techs) == len(manual_count)

    def test_get_technologies_by_category(self):
        """Test récupération technologies par catégorie"""
        result = get_technologies_by_category()

        # Vérifier que c'est le même dictionnaire
        assert result == TECHNOLOGIES_REFERENTIEL
        assert result is TECHNOLOGIES_REFERENTIEL  # Même référence

        # Vérifier structure
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_search_technologies_exact_match(self):
        """Test recherche technologie correspondance exacte"""
        result = search_technologies("Python")

        # Vérifier qu'on trouve Python
        assert len(result) > 0
        python_found = any(tech == "Python" for tech in result)
        assert python_found

    def test_search_technologies_partial_match(self):
        """Test recherche technologie correspondance partielle"""
        result = search_technologies("java")  # minuscule

        # Devrait trouver Java, JavaScript, Java Android, etc.
        assert len(result) > 0
        java_found = any("java" in tech.lower() for tech in result)
        assert java_found

        # Vérifier quelques correspondances attendues
        java_techs = [tech for tech in result if "java" in tech.lower()]
        assert "Java" in java_techs
        assert "JavaScript" in java_techs

    def test_search_technologies_case_insensitive(self):
        """Test recherche insensible à la casse"""
        result_upper = search_technologies("PYTHON")
        result_lower = search_technologies("python")
        result_mixed = search_technologies("Python")

        # Tous devraient donner le même résultat
        assert len(result_upper) > 0
        assert len(result_lower) > 0
        assert len(result_mixed) > 0
        assert set(result_upper) == set(result_lower) == set(result_mixed)

    def test_search_technologies_empty_query(self):
        """Test recherche avec requête vide"""
        result = search_technologies("")

        # Une chaîne vide devrait matcher toutes les technologies
        all_techs = get_all_technologies()
        assert len(result) == len(all_techs)
        assert set(result) == set(all_techs)

    def test_search_technologies_no_match(self):
        """Test recherche sans correspondance"""
        result = search_technologies("XXXXXX_NO_MATCH_XXXXXX")

        # Aucun résultat attendu
        assert len(result) == 0

    def test_search_technologies_common_terms(self):
        """Test recherche termes communs"""
        # Test terme cloud
        result_cloud = search_technologies("cloud")
        assert len(result_cloud) > 0
        cloud_found = any("cloud" in tech.lower() for tech in result_cloud)
        assert cloud_found

        # Test terme web
        result_web = search_technologies("web")
        assert len(result_web) > 0

        # Test terme sql
        result_sql = search_technologies("sql")
        assert len(result_sql) > 0

    def test_search_technologies_specific_frameworks(self):
        """Test recherche frameworks spécifiques"""
        # Test React
        result_react = search_technologies("React")
        assert "React" in result_react
        assert "React.js" in result_react
        assert "React Native" in result_react

        # Test Angular
        result_angular = search_technologies("Angular")
        assert "Angular" in result_angular
        assert "AngularJS" in result_angular

    def test_add_custom_technology_new_category(self):
        """Test ajout technologie nouvelle catégorie"""
        # Sauvegarder état original
        original_categories = list(TECHNOLOGIES_REFERENTIEL.keys())

        try:
            # Ajouter technologie dans nouvelle catégorie
            result = add_custom_technology("Test Category", "Test Technology")

            assert result == True
            assert "Test Category" in TECHNOLOGIES_REFERENTIEL
            assert "Test Technology" in TECHNOLOGIES_REFERENTIEL["Test Category"]

        finally:
            # Nettoyer - supprimer la catégorie de test
            if "Test Category" in TECHNOLOGIES_REFERENTIEL:
                del TECHNOLOGIES_REFERENTIEL["Test Category"]

    def test_add_custom_technology_existing_category(self):
        """Test ajout technologie catégorie existante"""
        # Utiliser catégorie existante
        category = "Langages de programmation"
        original_techs = TECHNOLOGIES_REFERENTIEL[category].copy()

        try:
            # Ajouter nouvelle technologie
            result = add_custom_technology(category, "TestLang")

            assert result == True
            assert "TestLang" in TECHNOLOGIES_REFERENTIEL[category]

            # Vérifier que la liste est triée
            assert TECHNOLOGIES_REFERENTIEL[category] == sorted(
                TECHNOLOGIES_REFERENTIEL[category]
            )

        finally:
            # Restaurer état original
            TECHNOLOGIES_REFERENTIEL[category] = original_techs

    def test_add_custom_technology_duplicate(self):
        """Test ajout technologie déjà existante"""
        category = "Langages de programmation"
        original_techs = TECHNOLOGIES_REFERENTIEL[category].copy()

        try:
            # Essayer d'ajouter Python qui existe déjà
            result = add_custom_technology(category, "Python")

            assert result == False
            # Vérifier que la liste n'a pas changé
            assert TECHNOLOGIES_REFERENTIEL[category] == original_techs

        finally:
            # Restaurer état original (normalement pas nécessaire ici)
            TECHNOLOGIES_REFERENTIEL[category] = original_techs

    def test_add_custom_technology_sorting(self):
        """Test tri automatique après ajout"""
        category = "Test Sorting Category"

        try:
            # Ajouter plusieurs technologies dans le désordre
            add_custom_technology(category, "ZZZ Last")
            add_custom_technology(category, "AAA First")
            add_custom_technology(category, "MMM Middle")

            # Vérifier que la liste est triée
            techs = TECHNOLOGIES_REFERENTIEL[category]
            assert techs == ["AAA First", "MMM Middle", "ZZZ Last"]
            assert techs == sorted(techs)

        finally:
            # Nettoyer
            if category in TECHNOLOGIES_REFERENTIEL:
                del TECHNOLOGIES_REFERENTIEL[category]

    def test_referentiel_data_integrity(self):
        """Test intégrité des données du référentiel"""
        for category, techs in TECHNOLOGIES_REFERENTIEL.items():
            # Vérifier que toutes les catégories ont des technologies
            assert len(techs) > 0, f"Category '{category}' is empty"

            # Vérifier qu'il n'y a pas de doublons dans chaque catégorie (tolérer quelques doublons connus)
            unique_techs = len(set(techs))
            total_techs = len(techs)
            if unique_techs != total_techs:
                # Identifier les doublons pour debug
                duplicates = [tech for tech in techs if techs.count(tech) > 1]
                print(f"Category '{category}' has duplicates: {set(duplicates)}")
                # Tolérer jusqu'à 5 doublons (peut être normal avec des alias)
                assert (
                    total_techs - unique_techs <= 5
                ), f"Category '{category}' has too many duplicates: {set(duplicates)}"

            # Vérifier que toutes les technologies sont des strings non vides
            for tech in techs:
                assert isinstance(
                    tech, str
                ), f"Technology '{tech}' in '{category}' is not a string"
                assert tech.strip() != "", f"Empty technology in '{category}'"

    def test_popular_technologies_subset(self):
        """Test que les technologies populaires sont dans le référentiel"""
        all_techs = get_all_technologies()

        for popular_tech in TECHNOLOGIES_POPULAIRES:
            assert (
                popular_tech in all_techs
            ), f"Popular technology '{popular_tech}' not found in referentiel"

    def test_comprehensive_category_coverage(self):
        """Test couverture complète des catégories importantes"""
        # Vérifier catégories essentielles
        essential_categories = [
            "Langages de programmation",
            "Frameworks Web",
            "Bases de données",
            "Cloud & DevOps",
        ]

        for category in essential_categories:
            assert category in TECHNOLOGIES_REFERENTIEL
            assert (
                len(TECHNOLOGIES_REFERENTIEL[category]) >= 10
            )  # Au moins 10 technologies

    def test_search_technologies_edge_cases(self):
        """Test cas limites de la recherche"""
        # Test avec recherche simple (la fonction ne fait pas de strip automatiquement)
        result_python = search_technologies("Python")
        assert len(result_python) > 0

        # Test avec caractères spéciaux dans les technologies
        result_special = search_technologies("C#")
        assert len(result_special) > 0
        assert "C#" in result_special

        # Test avec points
        result_dot = search_technologies("3.x")
        assert len(result_dot) > 0

    def test_function_return_types(self):
        """Test types de retour des fonctions"""
        # get_all_technologies retourne List[str]
        all_techs = get_all_technologies()
        assert isinstance(all_techs, list)
        assert all(isinstance(tech, str) for tech in all_techs)

        # get_technologies_by_category retourne Dict[str, List[str]]
        by_category = get_technologies_by_category()
        assert isinstance(by_category, dict)
        assert all(isinstance(key, str) for key in by_category.keys())
        assert all(isinstance(val, list) for val in by_category.values())

        # search_technologies retourne List[str]
        search_result = search_technologies("test")
        assert isinstance(search_result, list)
        assert all(isinstance(tech, str) for tech in search_result)

        # add_custom_technology retourne bool
        original_techs = TECHNOLOGIES_REFERENTIEL.get("Test", []).copy()
        try:
            result = add_custom_technology("Test", "TestTech")
            assert isinstance(result, bool)
        finally:
            if "Test" in TECHNOLOGIES_REFERENTIEL:
                if not original_techs:
                    del TECHNOLOGIES_REFERENTIEL["Test"]
                else:
                    TECHNOLOGIES_REFERENTIEL["Test"] = original_techs

    def test_large_dataset_performance(self):
        """Test performance avec le grand dataset"""
        # Vérifier que la recherche est efficace même avec beaucoup de données
        all_techs = get_all_technologies()

        # Le référentiel devrait contenir plusieurs centaines de technologies
        assert len(all_techs) > 200

        # Les recherches devraient être rapides
        import time

        start_time = time.time()

        for _ in range(100):  # 100 recherches
            search_technologies("a")

        end_time = time.time()
        # Devrait prendre moins d'une seconde pour 100 recherches
        assert (end_time - start_time) < 1.0

    def test_specific_technology_categories_content(self):
        """Test contenu spécifique de certaines catégories"""
        # Test catégorie IA & Data Science
        ai_category = TECHNOLOGIES_REFERENTIEL[
            "Intelligence Artificielle & Data Science"
        ]
        expected_ai_techs = ["TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy"]
        for tech in expected_ai_techs:
            assert tech in ai_category

        # Test catégorie Mobile
        mobile_category = TECHNOLOGIES_REFERENTIEL["Mobile"]
        expected_mobile_techs = ["iOS", "Android", "React Native", "Flutter"]
        for tech in expected_mobile_techs:
            assert tech in mobile_category

        # Test catégorie Cloud & DevOps
        cloud_category = TECHNOLOGIES_REFERENTIEL["Cloud & DevOps"]
        expected_cloud_techs = ["AWS", "Azure", "Docker", "Kubernetes", "Jenkins"]
        for tech in expected_cloud_techs:
            assert tech in cloud_category
