"""Tests d'intégration pour le workflow practice complet"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from datetime import datetime, date

# Import des services principaux
from app.services.practice_service import PracticeService
from app.services.consultant_service import ConsultantService
from app.database.database import get_database_session
from app.database.models import Practice, Consultant


# Fixtures pour les tests de practice
@pytest.fixture
def sample_practice_data():
    """Données de test pour une practice"""
    return {
        "nom": "Data Science & AI",
        "description": "Practice spécialisée dans la data science et l'intelligence artificielle",
        "responsable": "Dr. Marie Dubois",
    }


@pytest.fixture
def sample_consultants_for_practice():
    """Créer plusieurs consultants de test pour une practice"""
    consultants_data = [
        {
            "prenom": "Alice",
            "nom": "Data",
            "email": "alice.data@test.com",
            "salaire_actuel": 65000,
            "practice_id": 1,
            "disponibilite": True,
            "grade": "Expert",
            "societe": "DataCorp",
        },
        {
            "prenom": "Bob",
            "nom": "AI",
            "email": "bob.ai@test.com",
            "salaire_actuel": 60000,
            "practice_id": 1,
            "disponibilite": True,
            "grade": "Senior",
            "societe": "DataCorp",
        },
        {
            "prenom": "Claire",
            "nom": "ML",
            "email": "claire.ml@test.com",
            "salaire_actuel": 55000,
            "practice_id": 1,
            "disponibilite": False,
            "grade": "Senior",
            "societe": "DataCorp",
        },
    ]

    created_ids = []

    for data in consultants_data:
        result = ConsultantService.create_consultant(data)
        assert result is True
        consultant = ConsultantService.get_consultant_by_email(data["email"])
        created_ids.append(consultant.id)

    yield created_ids

    # Nettoyage
    for consultant_id in created_ids:
        try:
            ConsultantService.delete_consultant(consultant_id)
        except:
            pass


class TestPracticeWorkflowIntegration:
    """Tests d'intégration pour le workflow practice complet"""

    def test_complete_practice_workflow(
        self, sample_practice_data, sample_consultants_for_practice
    ):
        """Test du workflow complet practice : création → assignation → statistiques → suppression"""

        practice_id = None
        consultant_ids = sample_consultants_for_practice

        try:
            # === PHASE 1: Création de la practice ===
            print("=== PHASE 1: Création de la practice ===")

            with get_database_session() as session:
                practice = Practice(**sample_practice_data)
                session.add(practice)
                session.commit()
                practice_id = practice.id

            # Vérifier que la practice a été créée
            with get_database_session() as session:
                created_practice = (
                    session.query(Practice).filter(Practice.id == practice_id).first()
                )
                assert created_practice is not None
                assert created_practice.nom == sample_practice_data["nom"]
                assert (
                    created_practice.description == sample_practice_data["description"]
                )

            print(f"✅ Practice créée avec ID: {practice_id}")

            # === PHASE 2: Assignation des consultants ===
            print("=== PHASE 2: Assignation des consultants ===")

            for consultant_id in consultant_ids:
                result = ConsultantService.update_consultant(
                    consultant_id, {"practice_id": practice_id}
                )
                assert result is True

            # Vérifier les assignations
            with get_database_session() as session:
                consultants_in_practice = (
                    session.query(Consultant)
                    .filter(Consultant.practice_id == practice_id)
                    .all()
                )
                assert len(consultants_in_practice) == len(consultant_ids)

            print("✅ Consultants assignés à la practice")

            # === PHASE 3: Vérification des statistiques ===
            print("=== PHASE 3: Vérification des statistiques ===")

            # Vérifier les statistiques via ConsultantService
            all_consultants = ConsultantService.get_all_consultants_with_stats()
            practice_consultants = [
                c
                for c in all_consultants
                if c.get("practice_name") == sample_practice_data["nom"]
            ]

            assert len(practice_consultants) == len(consultant_ids)

            # Calculer les statistiques manuellement
            total_salary = sum(c["salaire_actuel"] for c in practice_consultants)
            available_count = sum(1 for c in practice_consultants if c["disponibilite"])
            unavailable_count = len(practice_consultants) - available_count

            print(
                f"📊 Statistiques practice: {len(practice_consultants)} consultants, "
                f"{available_count} disponibles, salaire total: {total_salary}€"
            )

            # === PHASE 4: Test de recherche par practice ===
            print("=== PHASE 4: Test de recherche par practice ===")

            # Rechercher les consultants de cette practice
            search_results = ConsultantService.search_consultants_optimized(
                "", page=1, per_page=50
            )
            practice_results = [
                c
                for c in search_results
                if c.get("practice_name") == sample_practice_data["nom"]
            ]

            assert len(practice_results) == len(consultant_ids)

            print("✅ Recherche par practice fonctionnelle")

            # === PHASE 5: Modification de la practice ===
            print("=== PHASE 5: Modification de la practice ===")

            with get_database_session() as session:
                practice = (
                    session.query(Practice).filter(Practice.id == practice_id).first()
                )
                practice.description = (
                    "Description mise à jour pour les tests d'intégration"
                )
                practice.responsable = "Dr. Jean Martin"
                session.commit()

            # Vérifier les modifications
            with get_database_session() as session:
                updated_practice = (
                    session.query(Practice).filter(Practice.id == practice_id).first()
                )
                assert (
                    updated_practice.description
                    == "Description mise à jour pour les tests d'intégration"
                )
                assert updated_practice.responsable == "Dr. Jean Martin"

            print("✅ Practice modifiée avec succès")

            print("🎉 WORKFLOW PRACTICE COMPLET RÉUSSI !")

        finally:
            # === NETTOYAGE ===
            print("=== NETTOYAGE PRACTICE ===")

            # Détacher les consultants de la practice
            for consultant_id in consultant_ids:
                try:
                    ConsultantService.update_consultant(
                        consultant_id, {"practice_id": None}
                    )
                except:
                    pass

            # Supprimer la practice
            if practice_id:
                try:
                    with get_database_session() as session:
                        practice = (
                            session.query(Practice)
                            .filter(Practice.id == practice_id)
                            .first()
                        )
                        if practice:
                            session.delete(practice)
                            session.commit()
                    print("✅ Practice supprimée (nettoyage)")
                except Exception as e:
                    print(f"⚠️ Erreur lors du nettoyage practice: {e}")

    def test_practice_statistics_workflow(self):
        """Test du workflow des statistiques de practice"""

        # Créer plusieurs practices avec des consultants
        practices_data = [
            {
                "nom": "Frontend Development",
                "description": "Développement frontend",
                "responsable": "Alice Frontend",
            },
            {
                "nom": "Backend Development",
                "description": "Développement backend",
                "responsable": "Bob Backend",
            },
        ]

        practice_ids = []
        all_consultant_ids = []

        try:
            # Créer les practices
            for practice_data in practices_data:
                with get_database_session() as session:
                    practice = Practice(**practice_data)
                    session.add(practice)
                    session.commit()
                    practice_ids.append(practice.id)

            # Créer des consultants pour chaque practice
            consultants_data = [
                # Frontend
                {
                    "prenom": "Anna",
                    "nom": "React",
                    "email": "anna.react@test.com",
                    "salaire_actuel": 55000,
                    "practice_id": practice_ids[0],
                    "disponibilite": True,
                },
                {
                    "prenom": "Ben",
                    "nom": "Vue",
                    "email": "ben.vue@test.com",
                    "salaire_actuel": 52000,
                    "practice_id": practice_ids[0],
                    "disponibilite": False,
                },
                # Backend
                {
                    "prenom": "Charlie",
                    "nom": "Python",
                    "email": "charlie.python@test.com",
                    "salaire_actuel": 60000,
                    "practice_id": practice_ids[1],
                    "disponibilite": True,
                },
                {
                    "prenom": "Diana",
                    "nom": "Java",
                    "email": "diana.java@test.com",
                    "salaire_actuel": 58000,
                    "practice_id": practice_ids[1],
                    "disponibilite": True,
                },
                {
                    "prenom": "Eve",
                    "nom": "Node",
                    "email": "eve.node@test.com",
                    "salaire_actuel": 54000,
                    "practice_id": practice_ids[1],
                    "disponibilite": False,
                },
            ]

            # Créer les consultants
            for data in consultants_data:
                result = ConsultantService.create_consultant(data)
                assert result is True
                consultant = ConsultantService.get_consultant_by_email(data["email"])
                all_consultant_ids.append(consultant.id)

            # Analyser les statistiques par practice
            all_consultants = ConsultantService.get_all_consultants_with_stats()

            frontend_consultants = [
                c
                for c in all_consultants
                if c.get("practice_name") == "Frontend Development"
            ]
            backend_consultants = [
                c
                for c in all_consultants
                if c.get("practice_name") == "Backend Development"
            ]

            # Vérifications Frontend
            assert len(frontend_consultants) == 2
            frontend_available = sum(
                1 for c in frontend_consultants if c["disponibilite"]
            )
            assert frontend_available == 1  # Anna disponible, Ben non disponible

            # Vérifications Backend
            assert len(backend_consultants) == 3
            backend_available = sum(
                1 for c in backend_consultants if c["disponibilite"]
            )
            assert backend_available == 2  # Charlie et Diana disponibles, Eve non

            # Calcul des salaires moyens
            frontend_avg_salary = sum(
                c["salaire_actuel"] for c in frontend_consultants
            ) / len(frontend_consultants)
            backend_avg_salary = sum(
                c["salaire_actuel"] for c in backend_consultants
            ) / len(backend_consultants)

            assert frontend_avg_salary == 53500  # (55000 + 52000) / 2
            assert backend_avg_salary == pytest.approx(
                57333.33, abs=0.01
            )  # (60000 + 58000 + 54000) / 3

            print("✅ Statistiques des practices calculées correctement")

        finally:
            # Nettoyage
            for consultant_id in all_consultant_ids:
                try:
                    ConsultantService.delete_consultant(consultant_id)
                except:
                    pass

            for practice_id in practice_ids:
                try:
                    with get_database_session() as session:
                        practice = (
                            session.query(Practice)
                            .filter(Practice.id == practice_id)
                            .first()
                        )
                        if practice:
                            session.delete(practice)
                            session.commit()
                except:
                    pass

    def test_practice_consultant_reassignment(self):
        """Test de réassignation de consultants entre practices"""

        # Créer deux practices
        practices_data = [
            {"nom": "Old Practice", "description": "Practice d'origine"},
            {"nom": "New Practice", "description": "Nouvelle practice"},
        ]

        practice_ids = []

        try:
            # Créer les practices
            for practice_data in practices_data:
                with get_database_session() as session:
                    practice = Practice(**practice_data)
                    session.add(practice)
                    session.commit()
                    practice_ids.append(practice.id)

            # Créer un consultant dans la première practice
            consultant_data = {
                "prenom": "Test",
                "nom": "Reassignment",
                "email": "test.reassignment@test.com",
                "salaire_actuel": 50000,
                "practice_id": practice_ids[0],
                "disponibilite": True,
                "grade": "Senior",
                "societe": "TestCorp",
            }

            result = ConsultantService.create_consultant(consultant_data)
            assert result is True
            consultant = ConsultantService.get_consultant_by_email(
                consultant_data["email"]
            )
            consultant_id = consultant.id

            # Vérifier l'assignation initiale
            consultant_with_stats = ConsultantService.get_consultant_with_stats(
                consultant_id
            )
            assert (
                consultant_with_stats["id"] is not None
            )  # Vérifier que le consultant existe

            # Réassigner à la nouvelle practice
            result = ConsultantService.update_consultant(
                consultant_id, {"practice_id": practice_ids[1]}
            )
            assert result is True

            # Vérifier la nouvelle assignation
            updated_consultant = ConsultantService.get_consultant_by_id(consultant_id)
            assert updated_consultant.practice_id == practice_ids[1]

            # Vérifier les statistiques des practices
            all_consultants = ConsultantService.get_all_consultants_with_stats()

            old_practice_consultants = [
                c for c in all_consultants if c.get("practice_name") == "Old Practice"
            ]
            new_practice_consultants = [
                c for c in all_consultants if c.get("practice_name") == "New Practice"
            ]

            assert (
                len(old_practice_consultants) == 0
            )  # Plus de consultants dans l'ancienne practice
            assert (
                len(new_practice_consultants) == 1
            )  # Un consultant dans la nouvelle practice

            print("✅ Réassignation de consultant entre practices réussie")

        finally:
            # Nettoyage
            if "consultant_id" in locals():
                try:
                    ConsultantService.delete_consultant(consultant_id)
                except:
                    pass

            for practice_id in practice_ids:
                try:
                    with get_database_session() as session:
                        practice = (
                            session.query(Practice)
                            .filter(Practice.id == practice_id)
                            .first()
                        )
                        if practice:
                            session.delete(practice)
                            session.commit()
                except:
                    pass
