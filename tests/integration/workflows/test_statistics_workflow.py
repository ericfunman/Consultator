"""Tests d'intégration pour le workflow de statistiques et tableaux de bord"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from datetime import datetime, date, timedelta
import pandas as pd

# Import des services principaux
from app.services.consultant_service import ConsultantService
from app.services.practice_service import PracticeService
from app.database.database import get_database_session
from app.database.models import Practice, Consultant, Mission


# Fixtures pour les tests de statistiques
@pytest.fixture
def statistics_test_data():
    """Créer un jeu de données complet pour les tests de statistiques"""

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
    ]

    practice_ids = []

    for practice_data in practices_data:
        with get_database_session() as session:
            practice = Practice(**practice_data)
            session.add(practice)
            session.commit()
            practice_ids.append(practice.id)

    # Créer des consultants avec diversité de salaires et grades
    consultants_data = [
        # Data Science - hauts salaires
        {
            "prenom": "Alice",
            "nom": "Expert",
            "email": "alice.expert@test.com",
            "salaire_actuel": 75000,
            "practice_id": practice_ids[0],
            "disponibilite": True,
            "grade": "Expert",
            "societe": "DataCorp",
        },
        {
            "prenom": "Bob",
            "nom": "Senior",
            "email": "bob.senior@test.com",
            "salaire_actuel": 65000,
            "practice_id": practice_ids[0],
            "disponibilite": True,
            "grade": "Senior",
            "societe": "DataCorp",
        },
        {
            "prenom": "Claire",
            "nom": "Senior",
            "email": "claire.senior@test.com",
            "salaire_actuel": 62000,
            "practice_id": practice_ids[0],
            "disponibilite": False,
            "grade": "Senior",
            "societe": "DataCorp",
        },
        {
            "prenom": "David",
            "nom": "Junior",
            "email": "david.junior@test.com",
            "salaire_actuel": 45000,
            "practice_id": practice_ids[0],
            "disponibilite": True,
            "grade": "Junior",
            "societe": "DataCorp",
        },
        # Frontend - salaires moyens
        {
            "prenom": "Emma",
            "nom": "Expert",
            "email": "emma.expert@test.com",
            "salaire_actuel": 68000,
            "practice_id": practice_ids[1],
            "disponibilite": True,
            "grade": "Expert",
            "societe": "WebCorp",
        },
        {
            "prenom": "Felix",
            "nom": "Senior",
            "email": "felix.senior@test.com",
            "salaire_actuel": 58000,
            "practice_id": practice_ids[1],
            "disponibilite": True,
            "grade": "Senior",
            "societe": "WebCorp",
        },
        {
            "prenom": "Grace",
            "nom": "Senior",
            "email": "grace.senior@test.com",
            "salaire_actuel": 55000,
            "practice_id": practice_ids[1],
            "disponibilite": False,
            "grade": "Senior",
            "societe": "WebCorp",
        },
        {
            "prenom": "Henry",
            "nom": "Junior",
            "email": "henry.junior@test.com",
            "salaire_actuel": 42000,
            "practice_id": practice_ids[1],
            "disponibilite": True,
            "grade": "Junior",
            "societe": "WebCorp",
        },
        # Backend - salaires variés
        {
            "prenom": "Iris",
            "nom": "Expert",
            "email": "iris.expert@test.com",
            "salaire_actuel": 72000,
            "practice_id": practice_ids[2],
            "disponibilite": False,
            "grade": "Expert",
            "societe": "BackendCorp",
        },
        {
            "prenom": "Jack",
            "nom": "Senior",
            "email": "jack.senior@test.com",
            "salaire_actuel": 60000,
            "practice_id": practice_ids[2],
            "disponibilite": True,
            "grade": "Senior",
            "societe": "BackendCorp",
        },
        {
            "prenom": "Kate",
            "nom": "Senior",
            "email": "kate.senior@test.com",
            "salaire_actuel": 57000,
            "practice_id": practice_ids[2],
            "disponibilite": True,
            "grade": "Senior",
            "societe": "BackendCorp",
        },
        {
            "prenom": "Leo",
            "nom": "Junior",
            "email": "leo.junior@test.com",
            "salaire_actuel": 44000,
            "practice_id": practice_ids[2],
            "disponibilite": True,
            "grade": "Junior",
            "societe": "BackendCorp",
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


class TestStatisticsWorkflowIntegration:
    """Tests d'intégration pour le workflow de statistiques et tableaux de bord"""

    def test_basic_statistics_workflow(self, statistics_test_data):
        """Test du workflow de statistiques de base"""

        print("=== TEST STATISTIQUES DE BASE ===")

        # Récupérer tous les consultants avec stats
        all_consultants = ConsultantService.get_all_consultants_with_stats()
        assert len(all_consultants) == len(statistics_test_data["consultant_ids"])

        # Calculer les métriques de base
        total_consultants = len(all_consultants)
        available_consultants = sum(1 for c in all_consultants if c["disponibilite"])
        unavailable_consultants = total_consultants - available_consultants
        availability_rate = (
            (available_consultants / total_consultants) * 100
            if total_consultants > 0
            else 0
        )

        total_salary = sum(c["salaire_actuel"] for c in all_consultants)
        avg_salary = total_salary / total_consultants if total_consultants > 0 else 0

        print(f"📊 Métriques globales:")
        print(f"   - Total consultants: {total_consultants}")
        print(f"   - Disponibles: {available_consultants} ({availability_rate:.1f}%)")
        print(f"   - Non disponibles: {unavailable_consultants}")
        print(f"   - Salaire total: {total_salary:,}€")
        print(f"   - Salaire moyen: {avg_salary:,.0f}€")

        # Vérifications
        assert total_consultants == 12
        assert available_consultants == 9  # 9 disponibles, 3 non disponibles
        assert unavailable_consultants == 3
        assert 70 <= availability_rate <= 80  # ~75%
        assert avg_salary > 55000  # Salaire moyen élevé

        print("✅ Statistiques de base calculées correctement")

    def test_practice_statistics_workflow(self, statistics_test_data):
        """Test du workflow de statistiques par practice"""

        print("=== TEST STATISTIQUES PAR PRACTICE ===")

        all_consultants = ConsultantService.get_all_consultants_with_stats()

        # Statistiques par practice
        practice_stats = {}
        for practice_name in ["Data Science", "Frontend", "Backend"]:
            practice_consultants = [
                c for c in all_consultants if c.get("practice_name") == practice_name
            ]
            if practice_consultants:
                total = len(practice_consultants)
                available = sum(1 for c in practice_consultants if c["disponibilite"])
                unavailable = total - available
                availability_rate = (available / total) * 100 if total > 0 else 0
                total_salary = sum(c["salaire_actuel"] for c in practice_consultants)
                avg_salary = total_salary / total if total > 0 else 0

                practice_stats[practice_name] = {
                    "total": total,
                    "available": available,
                    "unavailable": unavailable,
                    "availability_rate": availability_rate,
                    "total_salary": total_salary,
                    "avg_salary": avg_salary,
                }

                print(f"📊 {practice_name}:")
                print(f"   - Consultants: {total}")
                print(f"   - Disponibles: {available} ({availability_rate:.1f}%)")
                print(f"   - Salaire moyen: {avg_salary:,.0f}€")

        # Vérifications spécifiques
        ds_stats = practice_stats["Data Science"]
        assert ds_stats["total"] == 4
        assert ds_stats["available"] == 3  # Alice, Bob, David
        assert ds_stats["unavailable"] == 1  # Claire

        frontend_stats = practice_stats["Frontend"]
        assert frontend_stats["total"] == 4
        assert frontend_stats["available"] == 3  # Emma, Felix, Henry
        assert frontend_stats["unavailable"] == 1  # Grace

        backend_stats = practice_stats["Backend"]
        assert backend_stats["total"] == 4
        assert backend_stats["available"] == 3  # Jack, Kate, Leo
        assert backend_stats["unavailable"] == 1  # Iris

        print("✅ Statistiques par practice calculées correctement")

    def test_grade_statistics_workflow(self, statistics_test_data):
        """Test du workflow de statistiques par grade"""

        print("=== TEST STATISTIQUES PAR GRADE ===")

        all_consultants = ConsultantService.get_all_consultants_with_stats()

        # Statistiques par grade
        grade_stats = {}
        for grade in ["Expert", "Senior", "Junior"]:
            grade_consultants = [c for c in all_consultants if c.get("grade") == grade]
            if grade_consultants:
                total = len(grade_consultants)
                available = sum(1 for c in grade_consultants if c["disponibilite"])
                availability_rate = (available / total) * 100 if total > 0 else 0
                total_salary = sum(c["salaire_actuel"] for c in grade_consultants)
                avg_salary = total_salary / total if total > 0 else 0

                grade_stats[grade] = {
                    "total": total,
                    "available": available,
                    "availability_rate": availability_rate,
                    "total_salary": total_salary,
                    "avg_salary": avg_salary,
                }

                print(f"📊 Grade {grade}:")
                print(f"   - Consultants: {total}")
                print(f"   - Disponibles: {available} ({availability_rate:.1f}%)")
                print(f"   - Salaire moyen: {avg_salary:,.0f}€")

        # Vérifications
        expert_stats = grade_stats["Expert"]
        assert expert_stats["total"] == 3  # Alice, Emma, Iris
        assert expert_stats["available"] == 2  # Alice, Emma (Iris non disponible)

        senior_stats = grade_stats["Senior"]
        assert senior_stats["total"] == 6  # Bob, Claire, Felix, Grace, Jack, Kate
        assert senior_stats["available"] == 4  # Bob, Felix, Jack, Kate

        junior_stats = grade_stats["Junior"]
        assert junior_stats["total"] == 3  # David, Henry, Leo
        assert junior_stats["available"] == 3  # Tous disponibles

        # Vérifier la progression salariale
        assert (
            expert_stats["avg_salary"]
            > senior_stats["avg_salary"]
            > junior_stats["avg_salary"]
        )

        print("✅ Statistiques par grade calculées correctement")

    def test_salary_distribution_workflow(self, statistics_test_data):
        """Test du workflow de distribution des salaires"""

        print("=== TEST DISTRIBUTION SALARIALE ===")

        all_consultants = ConsultantService.get_all_consultants_with_stats()
        salaries = [c["salaire_actuel"] for c in all_consultants]

        # Calculer les quartiles
        salaries_sorted = sorted(salaries)
        q1 = salaries_sorted[len(salaries_sorted) // 4]
        q2 = salaries_sorted[len(salaries_sorted) // 2]  # Médiane
        q3 = salaries_sorted[3 * len(salaries_sorted) // 4]

        print(f"📊 Distribution salariale:")
        print(f"   - Minimum: {min(salaries):,}€")
        print(f"   - Q1 (25%): {q1:,}€")
        print(f"   - Médiane: {q2:,}€")
        print(f"   - Q3 (75%): {q3:,}€")
        print(f"   - Maximum: {max(salaries):,}€")

        # Vérifications
        assert min(salaries) >= 40000  # Salaire minimum raisonnable
        assert max(salaries) <= 80000  # Salaire maximum raisonnable
        assert q2 > 50000  # Médiane > 50k€
        assert q3 > q1  # Q3 > Q1 (distribution logique)

        # Calculer l'écart interquartile
        iqr = q3 - q1
        print(f"   - Écart interquartile: {iqr:,}€")

        # Vérifier la répartition par tranches
        salary_ranges = {
            "40k-50k": sum(1 for s in salaries if 40000 <= s < 50000),
            "50k-60k": sum(1 for s in salaries if 50000 <= s < 60000),
            "60k-70k": sum(1 for s in salaries if 60000 <= s < 70000),
            "70k-80k": sum(1 for s in salaries if 70000 <= s < 80000),
        }

        print(f"📊 Répartition par tranches:")
        for range_name, count in salary_ranges.items():
            print(f"   - {range_name}: {count} consultants")

        # Vérifications de répartition
        assert salary_ranges["40k-50k"] == 3  # Juniors
        assert salary_ranges["50k-60k"] == 3  # Certains seniors
        assert salary_ranges["60k-70k"] == 4  # Seniors et experts
        assert salary_ranges["70k-80k"] == 2  # Experts

        print("✅ Distribution salariale analysée correctement")

    def test_dashboard_metrics_workflow(self, statistics_test_data):
        """Test du workflow des métriques pour tableau de bord"""

        print("=== TEST MÉTRIQUES TABLEAU DE BORD ===")

        all_consultants = ConsultantService.get_all_consultants_with_stats()

        # Métriques clés pour le dashboard
        dashboard_metrics = {
            "total_consultants": len(all_consultants),
            "available_consultants": sum(
                1 for c in all_consultants if c["disponibilite"]
            ),
            "total_practices": len(
                set(
                    c.get("practice_name")
                    for c in all_consultants
                    if c.get("practice_name")
                )
            ),
            "total_salary_cost": sum(c["salaire_actuel"] for c in all_consultants),
            "avg_salary": sum(c["salaire_actuel"] for c in all_consultants)
            / len(all_consultants),
            "availability_rate": (
                sum(1 for c in all_consultants if c["disponibilite"])
                / len(all_consultants)
            )
            * 100,
        }

        # Métriques par practice pour le dashboard
        practice_dashboard = {}
        for practice_name in ["Data Science", "Frontend", "Backend"]:
            practice_consultants = [
                c for c in all_consultants if c.get("practice_name") == practice_name
            ]
            if practice_consultants:
                practice_dashboard[practice_name] = {
                    "count": len(practice_consultants),
                    "available": sum(
                        1 for c in practice_consultants if c["disponibilite"]
                    ),
                    "avg_salary": sum(c["salaire_actuel"] for c in practice_consultants)
                    / len(practice_consultants),
                    "availability_rate": (
                        sum(1 for c in practice_consultants if c["disponibilite"])
                        / len(practice_consultants)
                    )
                    * 100,
                }

        # Afficher les métriques du dashboard
        print("📊 MÉTRIQUES PRINCIPALES:")
        print(f"   - 👥 Total consultants: {dashboard_metrics['total_consultants']}")
        print(f"   - ✅ Disponibles: {dashboard_metrics['available_consultants']}")
        print(f"   - 🏢 Practices: {dashboard_metrics['total_practices']}")
        print(f"   - 💰 Coût total: {dashboard_metrics['total_salary_cost']:,}€")
        print(f"   - 📈 Salaire moyen: {dashboard_metrics['avg_salary']:,.0f}€")
        print(
            f"   - 📊 Taux disponibilité: {dashboard_metrics['availability_rate']:.1f}%"
        )

        print("\n📊 MÉTRIQUES PAR PRACTICE:")
        for practice, metrics in practice_dashboard.items():
            print(f"   - {practice}:")
            print(f"     • Consultants: {metrics['count']}")
            print(
                f"     • Disponibles: {metrics['available']} ({metrics['availability_rate']:.1f}%)"
            )
            print(f"     • Salaire moyen: {metrics['avg_salary']:,.0f}€")

        # Vérifications des métriques
        assert dashboard_metrics["total_consultants"] == 12
        assert dashboard_metrics["available_consultants"] == 9
        assert dashboard_metrics["total_practices"] == 3
        assert dashboard_metrics["total_salary_cost"] > 650000  # > 650k€
        assert 55000 <= dashboard_metrics["avg_salary"] <= 60000
        assert 70 <= dashboard_metrics["availability_rate"] <= 80

        print("✅ Métriques du tableau de bord calculées correctement")

    def test_statistics_export_workflow(self, statistics_test_data):
        """Test du workflow d'export des statistiques"""

        print("=== TEST EXPORT STATISTIQUES ===")

        all_consultants = ConsultantService.get_all_consultants_with_stats()

        # Créer un DataFrame pandas pour l'export
        df = pd.DataFrame(all_consultants)

        # Vérifications du DataFrame
        assert len(df) == len(all_consultants)
        assert "prenom" in df.columns
        assert "nom" in df.columns
        assert "salaire_actuel" in df.columns
        assert "practice_name" in df.columns
        assert "grade" in df.columns
        assert "disponibilite" in df.columns

        # Statistiques descriptives
        salary_stats = df["salaire_actuel"].describe()
        print(f"📊 Statistiques descriptives des salaires:")
        print(f"   - Count: {salary_stats['count']}")
        print(f"   - Mean: {salary_stats['mean']:,.0f}€")
        print(f"   - Std: {salary_stats['std']:,.0f}€")
        print(f"   - Min: {salary_stats['min']:,.0f}€")
        print(f"   - 25%: {salary_stats['25%']:,.0f}€")
        print(f"   - 50%: {salary_stats['50%']:,.0f}€")
        print(f"   - 75%: {salary_stats['75%']:,.0f}€")
        print(f"   - Max: {salary_stats['max']:,.0f}€")

        # Groupement par practice
        practice_group = df.groupby("practice_name").agg(
            {
                "salaire_actuel": ["count", "mean", "min", "max"],
                "disponibilite": "sum",  # Nombre de disponibles
            }
        )

        print(f"\n📊 Statistiques par practice (DataFrame):")
        for practice in practice_group.index:
            stats = practice_group.loc[practice]
            count = stats["salaire_actuel"]["count"]
            mean_salary = stats["salaire_actuel"]["mean"]
            available = stats["disponibilite"]["sum"]
            print(
                f"   - {practice}: {count} consultants, {available} disponibles, salaire moyen: {mean_salary:,.0f}€"
            )

        # Groupement par grade
        grade_group = df.groupby("grade").agg(
            {"salaire_actuel": ["count", "mean"], "disponibilite": "sum"}
        )

        print(f"\n📊 Statistiques par grade (DataFrame):")
        for grade in grade_group.index:
            stats = grade_group.loc[grade]
            count = stats["salaire_actuel"]["count"]
            mean_salary = stats["salaire_actuel"]["mean"]
            available = stats["disponibilite"]["sum"]
            print(
                f"   - {grade}: {count} consultants, {available} disponibles, salaire moyen: {mean_salary:,.0f}€"
            )

        # Simulation d'export CSV
        csv_content = df.to_csv(index=False)
        assert len(csv_content) > 0
        assert "prenom,nom" in csv_content

        print("✅ Export des statistiques simulé avec succès")
