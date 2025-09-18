"""Tests d'intégration pour le workflow de recherche et filtrage"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from datetime import datetime, date

# Import des services principaux
from app.services.consultant_service import ConsultantService
from app.services.practice_service import PracticeService
from app.database.database import get_database_session
from app.database.models import Practice, Consultant


# Fixtures pour les tests de recherche
@pytest.fixture
def search_test_data():
    """Créer un jeu de données complet pour les tests de recherche"""

    # Créer des practices
    practices_data = [
        {
            "nom": "Data Science",
            "description": "Data Science & AI",
            "responsable": "Dr. Marie Dubois",
        },
        {
            "nom": "Frontend",
            "description": "Développement frontend",
            "responsable": "Alice Frontend",
        },
        {
            "nom": "Backend",
            "description": "Développement backend",
            "responsable": "Bob Backend",
        },
        {
            "nom": "DevOps",
            "description": "Infrastructure & DevOps",
            "responsable": "Charlie DevOps",
        },
    ]

    practice_ids = []

    for practice_data in practices_data:
        with get_database_session() as session:
            practice = Practice(**practice_data)
            session.add(practice)
            session.commit()
            practice_ids.append(practice.id)

    # Créer des consultants avec diversité
    consultants_data = [
        # Data Science
        {
            "prenom": "Alice",
            "nom": "Data",
            "email": "alice.data@test.com",
            "salaire_actuel": 65000,
            "practice_id": practice_ids[0],
            "disponibilite": True,
            "grade": "Expert",
            "societe": "DataCorp",
        },
        {
            "prenom": "Bob",
            "nom": "AI",
            "email": "bob.ai@test.com",
            "salaire_actuel": 60000,
            "practice_id": practice_ids[0],
            "disponibilite": False,
            "grade": "Senior",
            "societe": "DataCorp",
        },
        {
            "prenom": "Claire",
            "nom": "ML",
            "email": "claire.ml@test.com",
            "salaire_actuel": 55000,
            "practice_id": practice_ids[0],
            "disponibilite": True,
            "grade": "Senior",
            "societe": "DataCorp",
        },
        # Frontend
        {
            "prenom": "David",
            "nom": "React",
            "email": "david.react@test.com",
            "salaire_actuel": 55000,
            "practice_id": practice_ids[1],
            "disponibilite": True,
            "grade": "Senior",
            "societe": "WebCorp",
        },
        {
            "prenom": "Emma",
            "nom": "Vue",
            "email": "emma.vue@test.com",
            "salaire_actuel": 50000,
            "practice_id": practice_ids[1],
            "disponibilite": True,
            "grade": "Junior",
            "societe": "WebCorp",
        },
        {
            "prenom": "Felix",
            "nom": "Angular",
            "email": "felix.angular@test.com",
            "salaire_actuel": 52000,
            "practice_id": practice_ids[1],
            "disponibilite": False,
            "grade": "Senior",
            "societe": "WebCorp",
        },
        # Backend
        {
            "prenom": "Grace",
            "nom": "Python",
            "email": "grace.python@test.com",
            "salaire_actuel": 60000,
            "practice_id": practice_ids[2],
            "disponibilite": True,
            "grade": "Expert",
            "societe": "BackendCorp",
        },
        {
            "prenom": "Henry",
            "nom": "Java",
            "email": "henry.java@test.com",
            "salaire_actuel": 58000,
            "practice_id": practice_ids[2],
            "disponibilite": True,
            "grade": "Senior",
            "societe": "BackendCorp",
        },
        {
            "prenom": "Iris",
            "nom": "Node",
            "email": "iris.node@test.com",
            "salaire_actuel": 54000,
            "practice_id": practice_ids[2],
            "disponibilite": False,
            "grade": "Senior",
            "societe": "BackendCorp",
        },
        # DevOps
        {
            "prenom": "Jack",
            "nom": "Docker",
            "email": "jack.docker@test.com",
            "salaire_actuel": 62000,
            "practice_id": practice_ids[3],
            "disponibilite": True,
            "grade": "Expert",
            "societe": "InfraCorp",
        },
        {
            "prenom": "Kate",
            "nom": "Kubernetes",
            "email": "kate.kubernetes@test.com",
            "salaire_actuel": 59000,
            "practice_id": practice_ids[3],
            "disponibilite": True,
            "grade": "Senior",
            "societe": "InfraCorp",
        },
    ]

    consultant_ids = []

    for data in consultants_data:
        result = ConsultantService.create_consultant(data)
        assert result is True
        consultant = ConsultantService.get_consultant_by_email(data["email"])
        consultant_ids.append(consultant.id)

    yield {
        "practice_ids": practice_ids,
        "consultant_ids": consultant_ids,
        "practices_data": practices_data,
        "consultants_data": consultants_data,
    }

    # Nettoyage
    for consultant_id in consultant_ids:
        try:
            ConsultantService.delete_consultant(consultant_id)
        except:
            pass

    for practice_id in practice_ids:
        try:
            with get_database_session() as session:
                practice = (
                    session.query(Practice).filter(Practice.id == practice_id).first()
                )
                if practice:
                    session.delete(practice)
                    session.commit()
        except:
            pass


class TestSearchWorkflowIntegration:
    """Tests d'intégration pour le workflow de recherche et filtrage"""

    def test_basic_search_workflow(self, search_test_data):
        """Test du workflow de recherche basique"""

        print("=== TEST RECHERCHE BASIQUE ===")

        # Recherche sans filtre
        all_results = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=50
        )
        assert len(all_results) == len(search_test_data["consultant_ids"])

        # Recherche par prénom
        alice_results = ConsultantService.search_consultants_optimized(
            "Alice", page=1, per_page=50
        )
        assert len(alice_results) == 1
        assert alice_results[0]["prenom"] == "Alice"

        # Recherche par nom
        data_results = ConsultantService.search_consultants_optimized(
            "Data", page=1, per_page=50
        )
        assert (
            len(data_results) == 3
        )  # Alice Data (nom), Bob AI (societe=DataCorp), Claire ML (societe=DataCorp)
        # Vérifier qu'Alice Data est dans les résultats
        alice_in_results = any(
            r["nom"] == "Data" and r["prenom"] == "Alice" for r in data_results
        )
        assert alice_in_results

        # Recherche par société
        webcorp_results = ConsultantService.search_consultants_optimized(
            "WebCorp", page=1, per_page=50
        )
        assert len(webcorp_results) == 3  # David, Emma, Felix

        print("✅ Recherche basique fonctionnelle")

    def test_advanced_filter_workflow(self, search_test_data):
        """Test du workflow de filtrage avancé"""

        print("=== TEST FILTRAGE AVANCÉ ===")

        # Filtre par practice
        data_science_results = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=50, practice_filter="Data Science"
        )
        assert len(data_science_results) == 3  # Alice, Bob, Claire

        frontend_results = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=50, practice_filter="Frontend"
        )
        assert len(frontend_results) == 3  # David, Emma, Felix

        # Filtre par grade
        expert_results = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=50, grade_filter="Expert"
        )
        assert len(expert_results) == 3  # Alice, Grace, Jack

        senior_results = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=50, grade_filter="Senior"
        )
        assert len(senior_results) == 7  # Bob, Claire, David, Felix, Henry, Iris, Kate

        # Filtre par disponibilité
        available_results = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=50, availability_filter=True
        )
        assert len(available_results) == 8  # Tous sauf Bob et Felix et Iris

        unavailable_results = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=50, availability_filter=False
        )
        assert len(unavailable_results) == 3  # Bob, Felix, Iris

        print("✅ Filtrage avancé fonctionnel")

    def test_combined_filters_workflow(self, search_test_data):
        """Test du workflow avec filtres combinés"""

        print("=== TEST FILTRES COMBINÉS ===")

        # Practice + Grade
        data_science_senior = ConsultantService.search_consultants_optimized(
            "",
            page=1,
            per_page=50,
            practice_filter="Data Science",
            grade_filter="Senior",
        )
        assert len(data_science_senior) == 2  # Bob, Claire

        # Practice + Disponibilité
        frontend_available = ConsultantService.search_consultants_optimized(
            "",
            page=1,
            per_page=50,
            practice_filter="Frontend",
            availability_filter=True,
        )
        assert len(frontend_available) == 2  # David, Emma (Felix n'est pas disponible)

        # Grade + Disponibilité
        senior_available = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=50, grade_filter="Senior", availability_filter=True
        )
        assert len(senior_available) == 4  # Claire, David, Emma, Henry, Kate

        # Tous les filtres
        complex_filter = ConsultantService.search_consultants_optimized(
            "",
            page=1,
            per_page=50,
            practice_filter="Backend",
            grade_filter="Senior",
            availability_filter=True,
        )
        assert len(complex_filter) == 1  # Henry

        print("✅ Filtres combinés fonctionnels")

    def test_search_with_text_and_filters(self, search_test_data):
        """Test de recherche textuelle avec filtres"""

        print("=== TEST RECHERCHE TEXTUELLE + FILTRES ===")

        # Recherche "Python" dans Backend
        python_backend = ConsultantService.search_consultants_optimized(
            "Python", page=1, per_page=50, practice_filter="Backend"
        )
        assert len(python_backend) == 1
        assert python_backend[0]["prenom"] == "Grace"

        # Recherche "React" dans Frontend disponibles
        react_frontend_available = ConsultantService.search_consultants_optimized(
            "React",
            page=1,
            per_page=50,
            practice_filter="Frontend",
            availability_filter=True,
        )
        assert len(react_frontend_available) == 1
        assert react_frontend_available[0]["prenom"] == "David"

        # Recherche "Corp" dans Experts
        corp_experts = ConsultantService.search_consultants_optimized(
            "Corp", page=1, per_page=50, grade_filter="Expert"
        )
        assert len(corp_experts) == 3  # Alice, Grace, Jack

        print("✅ Recherche textuelle avec filtres fonctionnelle")

    def test_pagination_workflow(self, search_test_data):
        """Test du workflow de pagination"""

        print("=== TEST PAGINATION ===")

        # Test pagination avec 2 par page
        page1 = ConsultantService.search_consultants_optimized("", page=1, per_page=2)
        page2 = ConsultantService.search_consultants_optimized("", page=2, per_page=2)
        page3 = ConsultantService.search_consultants_optimized("", page=3, per_page=2)

        assert len(page1) == 2
        assert len(page2) == 2
        assert len(page3) == 2

        # Vérifier que les résultats sont différents
        page1_ids = {r["id"] for r in page1}
        page2_ids = {r["id"] for r in page2}
        page3_ids = {r["id"] for r in page3}

        assert page1_ids.isdisjoint(page2_ids)
        assert page1_ids.isdisjoint(page3_ids)
        assert page2_ids.isdisjoint(page3_ids)

        # Test pagination avec filtres
        frontend_page1 = ConsultantService.search_consultants_optimized(
            "", page=1, per_page=2, practice_filter="Frontend"
        )
        frontend_page2 = ConsultantService.search_consultants_optimized(
            "", page=2, per_page=2, practice_filter="Frontend"
        )

        assert len(frontend_page1) == 2
        assert (
            len(frontend_page2) == 1
        )  # 3 consultants frontend, donc page 2 a 1 résultat

        print("✅ Pagination fonctionnelle")

    def test_statistics_with_filters_workflow(self, search_test_data):
        """Test des statistiques avec différents filtres"""

        print("=== TEST STATISTIQUES AVEC FILTRES ===")

        # Statistiques générales
        all_consultants = ConsultantService.get_all_consultants_with_stats()
        assert len(all_consultants) == len(search_test_data["consultant_ids"])

        # Calculer les statistiques manuellement pour vérification
        total_consultants = len(all_consultants)
        available_count = sum(1 for c in all_consultants if c["disponibilite"])
        total_salary = sum(c["salaire_actuel"] for c in all_consultants)
        avg_salary = total_salary / total_consultants if total_consultants > 0 else 0

        print(
            f"📊 Stats générales: {total_consultants} consultants, "
            f"{available_count} disponibles, salaire moyen: {avg_salary:.0f}€"
        )

        # Statistiques par practice
        for practice_name in ["Data Science", "Frontend", "Backend", "DevOps"]:
            practice_consultants = [
                c for c in all_consultants if c.get("practice_name") == practice_name
            ]
            if practice_consultants:
                practice_available = sum(
                    1 for c in practice_consultants if c["disponibilite"]
                )
                practice_avg_salary = sum(
                    c["salaire_actuel"] for c in practice_consultants
                ) / len(practice_consultants)
                print(
                    f"📊 {practice_name}: {len(practice_consultants)} consultants, "
                    f"{practice_available} disponibles, salaire moyen: {practice_avg_salary:.0f}€"
                )

        # Statistiques par grade
        for grade in ["Expert", "Senior", "Junior"]:
            grade_consultants = [c for c in all_consultants if c.get("grade") == grade]
            if grade_consultants:
                grade_available = sum(
                    1 for c in grade_consultants if c["disponibilite"]
                )
                grade_avg_salary = sum(
                    c["salaire_actuel"] for c in grade_consultants
                ) / len(grade_consultants)
                print(
                    f"📊 {grade}: {len(grade_consultants)} consultants, "
                    f"{grade_available} disponibles, salaire moyen: {grade_avg_salary:.0f}€"
                )

        print("✅ Statistiques avec filtres fonctionnelles")

    def test_search_performance_workflow(self, search_test_data):
        """Test des performances de recherche"""

        print("=== TEST PERFORMANCES RECHERCHE ===")

        import time

        # Test performance recherche simple
        start_time = time.time()
        for _ in range(10):
            results = ConsultantService.search_consultants_optimized(
                "", page=1, per_page=50
            )
        simple_search_time = (time.time() - start_time) / 10

        # Test performance avec filtres
        start_time = time.time()
        for _ in range(10):
            results = ConsultantService.search_consultants_optimized(
                "",
                page=1,
                per_page=50,
                practice_filter="Data Science",
                grade_filter="Senior",
                availability_filter=True,
            )
        filtered_search_time = (time.time() - start_time) / 10

        print(f"⏱️ Performance recherche simple: {simple_search_time:.4f}s")
        print(f"⏱️ Performance recherche filtrée: {filtered_search_time:.4f}s")

        # Les recherches filtrées peuvent être plus lentes mais pas excessivement
        assert simple_search_time < 1.0  # Moins d'1 seconde pour une recherche simple
        assert (
            filtered_search_time < 2.0
        )  # Moins de 2 secondes pour une recherche filtrée

        print("✅ Performances de recherche acceptables")
