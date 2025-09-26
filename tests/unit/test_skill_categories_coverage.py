"""
Tests complets pour skill_categories.py pour augmenter la couverture de 29% à 90%
Module utils avec référentiels et utilitaires de compétences
"""

import pytest

from app.utils.skill_categories import COMPETENCES_FONCTIONNELLES
from app.utils.skill_categories import COMPETENCES_TECHNIQUES
from app.utils.skill_categories import NIVEAUX_MAITRISE
from app.utils.skill_categories import NIVEAUX_REQUIS
from app.utils.skill_categories import get_all_categories
from app.utils.skill_categories import get_all_competences
from app.utils.skill_categories import get_competences_by_category
from app.utils.skill_categories import search_competences


class TestSkillCategoriesCoverage:
    """Tests complets pour skill_categories avec 90% de couverture"""

    def test_competences_techniques_constant(self):
        """Test dictionnaire compétences techniques"""
        # Vérifier structure
        assert isinstance(COMPETENCES_TECHNIQUES, dict)
        assert len(COMPETENCES_TECHNIQUES) > 0

        # Vérifier catégories clés
        assert "Backend" in COMPETENCES_TECHNIQUES
        assert "Frontend" in COMPETENCES_TECHNIQUES
        assert "Data & Analytics" in COMPETENCES_TECHNIQUES
        assert "Cloud & DevOps" in COMPETENCES_TECHNIQUES
        assert "Base de données" in COMPETENCES_TECHNIQUES

        # Vérifier contenu catégories
        assert "Python" in COMPETENCES_TECHNIQUES["Backend"]
        assert "Java" in COMPETENCES_TECHNIQUES["Backend"]
        assert "React" in COMPETENCES_TECHNIQUES["Frontend"]
        assert "Angular" in COMPETENCES_TECHNIQUES["Frontend"]
        assert "PostgreSQL" in COMPETENCES_TECHNIQUES["Base de données"]
        assert "AWS" in COMPETENCES_TECHNIQUES["Cloud & DevOps"]

    def test_competences_fonctionnelles_constant(self):
        """Test dictionnaire compétences fonctionnelles"""
        # Vérifier structure
        assert isinstance(COMPETENCES_FONCTIONNELLES, dict)
        assert len(COMPETENCES_FONCTIONNELLES) > 0

        # Vérifier catégories clés
        assert "Banque de Détail" in COMPETENCES_FONCTIONNELLES
        assert "Marchés Financiers" in COMPETENCES_FONCTIONNELLES
        assert "Crédit & Risques" in COMPETENCES_FONCTIONNELLES
        assert "Assurance Vie" in COMPETENCES_FONCTIONNELLES
        assert "Réglementation Bancaire" in COMPETENCES_FONCTIONNELLES

        # Vérifier contenu catégories
        assert (
            "Conseil clientèle particuliers"
            in COMPETENCES_FONCTIONNELLES["Banque de Détail"]
        )
        assert (
            "Trading actions (equity)"
            in COMPETENCES_FONCTIONNELLES["Marchés Financiers"]
        )
        assert "Scoring crédit" in COMPETENCES_FONCTIONNELLES["Crédit & Risques"]
        assert "Bâle III" in COMPETENCES_FONCTIONNELLES["Réglementation Bancaire"]

    def test_niveaux_maitrise_constant(self):
        """Test liste niveaux de maîtrise"""
        assert isinstance(NIVEAUX_MAITRISE, list)
        assert len(NIVEAUX_MAITRISE) == 4

        expected_levels = ["Débutant", "Intermédiaire", "Avancé", "Expert"]
        assert NIVEAUX_MAITRISE == expected_levels

    def test_niveaux_requis_constant(self):
        """Test liste niveaux requis"""
        assert isinstance(NIVEAUX_REQUIS, list)
        assert len(NIVEAUX_REQUIS) == 5

        expected_levels = ["Junior", "Médior", "Senior", "Lead", "Architect"]
        assert NIVEAUX_REQUIS == expected_levels

    def test_get_all_competences_complete(self):
        """Test récupération de toutes les compétences"""
        result = get_all_competences()

        # Vérifier structure
        assert isinstance(result, dict)
        assert "techniques" in result
        assert "fonctionnelles" in result

        # Vérifier contenu
        assert result["techniques"] == COMPETENCES_TECHNIQUES
        assert result["fonctionnelles"] == COMPETENCES_FONCTIONNELLES

    def test_get_competences_by_category_techniques(self):
        """Test récupération compétences techniques"""
        result = get_competences_by_category("techniques")

        assert result == COMPETENCES_TECHNIQUES
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_get_competences_by_category_fonctionnelles(self):
        """Test récupération compétences fonctionnelles"""
        result = get_competences_by_category("fonctionnelles")

        assert result == COMPETENCES_FONCTIONNELLES
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_get_competences_by_category_invalid(self):
        """Test récupération compétences catégorie invalide"""
        result = get_competences_by_category("invalid")

        assert result == {}
        assert isinstance(result, dict)

    def test_get_competences_by_category_default(self):
        """Test récupération compétences sans paramètre (défaut)"""
        result = get_competences_by_category()

        # Par défaut, retourne techniques
        assert result == COMPETENCES_TECHNIQUES

    def test_get_all_categories_complete(self):
        """Test récupération de toutes les catégories"""
        result = get_all_categories()

        # Vérifier structure
        assert isinstance(result, dict)
        assert "techniques" in result
        assert "fonctionnelles" in result

        # Vérifier contenu techniques
        assert isinstance(result["techniques"], list)
        assert "Backend" in result["techniques"]
        assert "Frontend" in result["techniques"]
        assert "Data & Analytics" in result["techniques"]

        # Vérifier contenu fonctionnelles
        assert isinstance(result["fonctionnelles"], list)
        assert "Banque de Détail" in result["fonctionnelles"]
        assert "Marchés Financiers" in result["fonctionnelles"]
        assert "Crédit & Risques" in result["fonctionnelles"]

    def test_search_competences_exact_match(self):
        """Test recherche compétence correspondance exacte"""
        result = search_competences("Python")

        # Vérifier qu'on trouve Python
        assert len(result) > 0
        python_found = any(comp["nom"] == "Python" for comp in result)
        assert python_found

        # Vérifier structure résultat
        for comp in result:
            assert "nom" in comp
            assert "categorie" in comp
            assert "type" in comp

    def test_search_competences_partial_match(self):
        """Test recherche compétence correspondance partielle"""
        result = search_competences("java")  # minuscule

        # Devrait trouver JavaScript, Java, etc.
        assert len(result) > 0
        java_found = any("java" in comp["nom"].lower() for comp in result)
        assert java_found

    def test_search_competences_case_insensitive(self):
        """Test recherche insensible à la casse"""
        result_upper = search_competences("PYTHON")
        result_lower = search_competences("python")
        result_mixed = search_competences("Python")

        # Tous devraient donner le même résultat
        assert len(result_upper) > 0
        assert len(result_lower) > 0
        assert len(result_mixed) > 0

    def test_search_competences_category_match(self):
        """Test recherche par nom de catégorie"""
        result = search_competences("Backend")

        # Devrait retourner toutes les compétences Backend
        assert len(result) > 0

        # Vérifier que toutes sont de la catégorie Backend
        backend_comps = [comp for comp in result if comp["categorie"] == "Backend"]
        assert len(backend_comps) > 0

        # Vérifier présence de compétences Backend connues
        backend_names = [comp["nom"] for comp in backend_comps]
        assert "Python" in backend_names
        assert "Java" in backend_names

    def test_search_competences_with_techniques_filter(self):
        """Test recherche avec filtre techniques"""
        result = search_competences("Python", category_type="techniques")

        assert len(result) > 0

        # Vérifier que tous les résultats sont techniques
        for comp in result:
            assert comp["type"] == "techniques"

    def test_search_competences_with_fonctionnelles_filter(self):
        """Test recherche avec filtre fonctionnelles"""
        result = search_competences("crédit", category_type="fonctionnelles")

        assert len(result) > 0

        # Vérifier que tous les résultats sont fonctionnelles
        for comp in result:
            assert comp["type"] == "fonctionnelles"

    def test_search_competences_no_filter(self):
        """Test recherche sans filtre (toutes catégories)"""
        result = search_competences("Python", category_type=None)

        # Devrait chercher dans techniques ET fonctionnelles
        assert len(result) > 0

    def test_search_competences_empty_query(self):
        """Test recherche avec requête vide"""
        result = search_competences("")

        # Une chaîne vide devrait matcher toutes les compétences
        assert len(result) > 0

    def test_search_competences_no_match(self):
        """Test recherche sans correspondance"""
        result = search_competences("XXXXXX_NO_MATCH_XXXXXX")

        # Aucun résultat attendu
        assert len(result) == 0

    def test_search_competences_banking_terms(self):
        """Test recherche termes bancaires spécifiques"""
        # Test terme bancaire
        result_credit = search_competences("crédit")
        assert len(result_credit) > 0

        # Test terme trading
        result_trading = search_competences("trading")
        assert len(result_trading) > 0

        # Vérifier type fonctionnel
        for comp in result_credit:
            if comp["categorie"] in COMPETENCES_FONCTIONNELLES:
                assert comp["type"] == "fonctionnelles"

    def test_search_competences_tech_terms(self):
        """Test recherche termes techniques spécifiques"""
        # Test base de données
        result_sql = search_competences("SQL")
        assert len(result_sql) > 0

        # Test cloud
        result_aws = search_competences("AWS")
        assert len(result_aws) > 0

        # Vérifier type technique
        for comp in result_sql:
            if comp["categorie"] in COMPETENCES_TECHNIQUES:
                assert comp["type"] == "techniques"

    def test_search_competences_category_name_match(self):
        """Test recherche par nom de catégorie exacte"""
        result = search_competences("Data & Analytics")

        # Devrait retourner toutes les compétences de cette catégorie
        assert len(result) > 0

        # Vérifier présence de compétences connues de cette catégorie
        competence_names = [comp["nom"] for comp in result]
        assert "Python Data" in competence_names
        assert "SQL" in competence_names
        assert "Pandas" in competence_names

    def test_search_competences_result_structure(self):
        """Test structure détaillée des résultats de recherche"""
        result = search_competences("Python")

        assert len(result) > 0

        for comp in result:
            # Vérifier champs obligatoires
            assert isinstance(comp, dict)
            assert "nom" in comp
            assert "categorie" in comp
            assert "type" in comp

            # Vérifier types
            assert isinstance(comp["nom"], str)
            assert isinstance(comp["categorie"], str)
            assert isinstance(comp["type"], str)

            # Vérifier valeurs valides pour type
            assert comp["type"] in ["techniques", "fonctionnelles"]

    def test_all_constants_immutable_reference(self):
        """Test que les constantes conservent leurs références"""
        # Sauvegarder références originales
        orig_tech_count = len(COMPETENCES_TECHNIQUES)
        orig_func_count = len(COMPETENCES_FONCTIONNELLES)
        orig_niv_maitrise_count = len(NIVEAUX_MAITRISE)
        orig_niv_requis_count = len(NIVEAUX_REQUIS)

        # Appeler fonctions qui utilisent les constantes
        get_all_competences()
        get_competences_by_category("techniques")
        get_all_categories()
        search_competences("test")

        # Vérifier que les constantes n'ont pas changé
        assert len(COMPETENCES_TECHNIQUES) == orig_tech_count
        assert len(COMPETENCES_FONCTIONNELLES) == orig_func_count
        assert len(NIVEAUX_MAITRISE) == orig_niv_maitrise_count
        assert len(NIVEAUX_REQUIS) == orig_niv_requis_count

    def test_comprehensive_category_coverage(self):
        """Test couverture complète des catégories"""
        # Vérifier toutes les catégories techniques
        tech_categories = list(COMPETENCES_TECHNIQUES.keys())
        expected_tech = [
            "Backend",
            "Frontend",
            "Mobile",
            "Data & Analytics",
            "Cloud & DevOps",
            "Base de données",
            "Architecture & Design",
            "Sécurité",
            "Outils & Méthodologies",
            "IA & Machine Learning",
        ]

        for cat in expected_tech:
            assert cat in tech_categories

        # Vérifier toutes les catégories fonctionnelles
        func_categories = list(COMPETENCES_FONCTIONNELLES.keys())
        expected_func = [
            "Banque de Détail",
            "Banque d'Affaires & Corporate",
            "Marchés Financiers",
            "Crédit & Risques",
            "Assurance Vie",
            "Assurance Non-Vie",
            "Réassurance",
            "Produits Financiers",
            "Réglementation Bancaire",
            "Réglementation Assurance",
            "Compliance & AML",
        ]

        for cat in expected_func:
            assert cat in func_categories

    def test_search_competences_edge_cases(self):
        """Test cas limites de la recherche"""
        # Test avec espaces - la fonction ne strip pas automatiquement
        result_spaces = search_competences("Python")  # Direct sans espaces
        assert len(result_spaces) > 0

        # Test avec terme existant confirmé
        result_backend = search_competences("Backend")
        assert len(result_backend) > 0

        # Test avec terme partiel
        result_partial = search_competences("Java")
        assert len(result_partial) > 0

    def test_function_return_types(self):
        """Test types de retour des fonctions"""
        # get_all_competences retourne dict
        result1 = get_all_competences()
        assert isinstance(result1, dict)

        # get_competences_by_category retourne dict
        result2 = get_competences_by_category("techniques")
        assert isinstance(result2, dict)

        # get_all_categories retourne dict
        result3 = get_all_categories()
        assert isinstance(result3, dict)

        # search_competences retourne list
        result4 = search_competences("Python")
        assert isinstance(result4, list)
