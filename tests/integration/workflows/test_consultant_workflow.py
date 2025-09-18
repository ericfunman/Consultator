"""Tests d'intégration pour le workflow consultant complet"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from datetime import datetime, date

# Import des services principaux
from app.services.consultant_service import ConsultantService
from app.services.practice_service import PracticeService
from app.database.database import get_database_session
from app.database.models import (
    Consultant,
    Practice,
    Competence,
    ConsultantCompetence,
    Mission,
)


# Fixtures pour les tests d'intégration
@pytest.fixture
def sample_consultant_data():
    """Données de test pour un consultant"""
    return {
        "prenom": "Jean",
        "nom": "Dupont",
        "email": "jean.dupont@test.com",
        "telephone": "0123456789",
        "salaire_actuel": 55000,
        "practice_id": 1,
        "disponibilite": True,
        "notes": "Consultant test d'intégration",
        "societe": "TestCorp",
        "grade": "Senior",
        "type_contrat": "CDI",
    }


@pytest.fixture
def sample_competence_data():
    """Données de test pour une compétence"""
    return {
        "nom": "Python_Test_Integration_Unique",
        "type_competence": "technique",
        "categorie": "Backend",
        "niveau_maitrise": "expert",
        "annees_experience": 5.0,
    }


@pytest.fixture
def sample_mission_data():
    """Données de test pour une mission"""
    return {
        "nom_mission": "Développement API REST",
        "client": "Client Test",
        "description": "Développement d'une API REST en Python",
        "date_debut": date(2024, 1, 1),
        "date_fin": date(2024, 6, 30),
        "statut": "terminee",
        "technologies_utilisees": "Python, FastAPI, PostgreSQL",
        "revenus_generes": 45000,
    }


class TestConsultantWorkflowIntegration:
    """Tests d'intégration pour le workflow consultant complet"""

    def setup_method(self):
        """Configuration avant chaque test"""
        # S'assurer que nous avons une practice de test
        with get_database_session() as session:
            # Créer une practice de test si elle n'existe pas
            practice = (
                session.query(Practice).filter(Practice.nom == "Test Practice").first()
            )
            if not practice:
                practice = Practice(
                    nom="Test Practice",
                    description="Practice pour les tests d'intégration",
                )
                session.add(practice)
                session.commit()

    def test_complete_consultant_workflow(
        self, sample_consultant_data, sample_competence_data, sample_mission_data
    ):
        """Test du workflow complet consultant : création → modification → compétences → missions → suppression"""

        consultant_id = None

        try:
            # === PHASE 1: Création du consultant ===
            print("=== PHASE 1: Création du consultant ===")

            # Créer le consultant
            result = ConsultantService.create_consultant(sample_consultant_data)
            assert result is True, "La création du consultant devrait réussir"

            # Vérifier que le consultant a été créé
            consultant = ConsultantService.get_consultant_by_email(
                sample_consultant_data["email"]
            )
            assert (
                consultant is not None
            ), "Le consultant devrait exister après création"
            assert consultant.prenom == sample_consultant_data["prenom"]
            assert consultant.nom == sample_consultant_data["nom"]
            consultant_id = consultant.id
            print(f"✅ Consultant créé avec ID: {consultant_id}")

            # === PHASE 2: Modification du consultant ===
            print("=== PHASE 2: Modification du consultant ===")

            update_data = {
                "telephone": "0987654321",
                "salaire_actuel": 60000,
                "notes": "Consultant modifié lors du test d'intégration",
            }

            result = ConsultantService.update_consultant(consultant_id, update_data)
            assert result is True, "La modification devrait réussir"

            # Vérifier les modifications
            updated_consultant = ConsultantService.get_consultant_by_id(consultant_id)
            assert updated_consultant.telephone == "0987654321"
            assert updated_consultant.salaire_actuel == 60000
            print("✅ Consultant modifié avec succès")

            # === PHASE 3: Ajout de compétences ===
            print("=== PHASE 3: Ajout de compétences ===")

            # Vérifier si la compétence existe déjà, sinon la créer
            with get_database_session() as session:
                competence = (
                    session.query(Competence)
                    .filter(Competence.nom == sample_competence_data["nom"])
                    .first()
                )

                if not competence:
                    competence = Competence(
                        nom=sample_competence_data["nom"],
                        type_competence=sample_competence_data["type_competence"],
                        categorie=sample_competence_data["categorie"],
                    )
                    session.add(competence)
                    session.commit()

                competence_id = competence.id

            # Ajouter la compétence au consultant
            consultant_competence_data = {
                "consultant_id": consultant_id,
                "competence_id": competence_id,
                "niveau_maitrise": sample_competence_data["niveau_maitrise"],
                "annees_experience": sample_competence_data["annees_experience"],
            }

            with get_database_session() as session:
                consultant_competence = ConsultantCompetence(
                    **consultant_competence_data
                )
                session.add(consultant_competence)
                session.commit()

            # Vérifier que la compétence a été ajoutée
            consultant_with_stats = ConsultantService.get_consultant_with_stats(
                consultant_id
            )
            assert consultant_with_stats is not None
            assert len(consultant_with_stats["competences"]) > 0
            print("✅ Compétence ajoutée au consultant")

            # === PHASE 4: Ajout de missions ===
            print("=== PHASE 4: Ajout de missions ===")

            # Créer une mission pour le consultant
            mission_data = sample_mission_data.copy()
            mission_data["consultant_id"] = consultant_id

            with get_database_session() as session:
                mission = Mission(**mission_data)
                session.add(mission)
                session.commit()

            # Vérifier que la mission a été ajoutée
            consultant_with_stats = ConsultantService.get_consultant_with_stats(
                consultant_id
            )
            assert len(consultant_with_stats["missions"]) > 0
            assert (
                consultant_with_stats["missions"][0]["nom_mission"]
                == sample_mission_data["nom_mission"]
            )
            print("✅ Mission ajoutée au consultant")

            # === PHASE 5: Recherche et vérifications ===
            print("=== PHASE 5: Recherche et vérifications ===")

            # Rechercher le consultant
            search_results = ConsultantService.search_consultants("Jean")
            assert len(search_results) > 0
            found_consultant = next(
                (c for c in search_results if c.id == consultant_id), None
            )
            assert found_consultant is not None
            print("✅ Consultant trouvé via recherche")

            # Vérifier les statistiques
            stats = ConsultantService.get_consultant_summary_stats()
            assert stats["total_consultants"] > 0
            print("✅ Statistiques mises à jour")

            # === PHASE 6: Test de disponibilité ===
            print("=== PHASE 6: Test de disponibilité ===")

            # Rendre le consultant indisponible
            ConsultantService.update_consultant(consultant_id, {"disponibilite": False})

            # Vérifier qu'il n'est plus dans les disponibles
            available = ConsultantService.get_consultants_by_availability(True)
            consultant_ids = [c["id"] for c in available]
            assert consultant_id not in consultant_ids
            print("✅ Gestion de disponibilité fonctionnelle")

            print("🎉 WORKFLOW COMPLET RÉUSSI !")

        finally:
            # === NETTOYAGE ===
            if consultant_id:
                print("=== NETTOYAGE ===")
                try:
                    # Supprimer les missions
                    with get_database_session() as session:
                        missions = (
                            session.query(Mission)
                            .filter(Mission.consultant_id == consultant_id)
                            .all()
                        )
                        for mission in missions:
                            session.delete(mission)
                        session.commit()

                    # Supprimer les compétences du consultant
                    with get_database_session() as session:
                        consultant_competences = (
                            session.query(ConsultantCompetence)
                            .filter(ConsultantCompetence.consultant_id == consultant_id)
                            .all()
                        )
                        for cc in consultant_competences:
                            session.delete(cc)
                        session.commit()

                    # Supprimer la compétence de test si elle a été créée
                    with get_database_session() as session:
                        test_competence = (
                            session.query(Competence)
                            .filter(Competence.nom == sample_competence_data["nom"])
                            .first()
                        )
                        if test_competence:
                            # Vérifier qu'elle n'est pas utilisée par d'autres consultants
                            other_usage = (
                                session.query(ConsultantCompetence)
                                .filter(
                                    ConsultantCompetence.competence_id
                                    == test_competence.id,
                                    ConsultantCompetence.consultant_id != consultant_id,
                                )
                                .first()
                            )
                            if not other_usage:
                                session.delete(test_competence)
                        session.commit()

                    # Supprimer le consultant
                    result = ConsultantService.delete_consultant(consultant_id)
                    assert result is True, "La suppression devrait réussir"
                    print("✅ Consultant supprimé (nettoyage)")

                except Exception as e:
                    print(f"⚠️ Erreur lors du nettoyage: {e}")

    def test_consultant_search_and_filter_workflow(self):
        """Test du workflow de recherche et filtrage de consultants"""

        # Créer plusieurs consultants pour les tests
        consultants_data = [
            {
                "prenom": "Alice",
                "nom": "Martin",
                "email": "alice.martin@test.com",
                "salaire_actuel": 50000,
                "practice_id": 1,
                "disponibilite": True,
                "grade": "Senior",
                "societe": "TechCorp",
            },
            {
                "prenom": "Bob",
                "nom": "Dubois",
                "email": "bob.dubois@test.com",
                "salaire_actuel": 45000,
                "practice_id": 1,
                "disponibilite": False,
                "grade": "Junior",
                "societe": "TechCorp",
            },
            {
                "prenom": "Claire",
                "nom": "Garcia",
                "email": "claire.garcia@test.com",
                "salaire_actuel": 60000,
                "practice_id": 1,
                "disponibilite": True,
                "grade": "Expert",
                "societe": "DataCorp",
            },
        ]

        created_ids = []

        try:
            # Créer les consultants
            for data in consultants_data:
                result = ConsultantService.create_consultant(data)
                assert result is True
                consultant = ConsultantService.get_consultant_by_email(data["email"])
                created_ids.append(consultant.id)

            # Test de recherche par nom
            results = ConsultantService.search_consultants("Alice")
            assert len(results) == 1
            assert results[0].prenom == "Alice"

            # Test de recherche par société
            results = ConsultantService.search_consultants("TechCorp")
            assert len(results) == 2

            # Test de filtrage par disponibilité
            available = ConsultantService.get_consultants_by_availability(True)
            available_ids = [c["id"] for c in available]
            assert len(available_ids) == 2  # Alice et Claire

            unavailable = ConsultantService.get_consultants_by_availability(False)
            unavailable_ids = [c["id"] for c in unavailable]
            assert len(unavailable_ids) == 1  # Bob

            # Test des statistiques
            stats = ConsultantService.get_consultant_summary_stats()
            assert stats["total_consultants"] >= 3
            assert stats["available_consultants"] >= 2

            print("✅ Workflow de recherche et filtrage réussi")

        finally:
            # Nettoyage
            for consultant_id in created_ids:
                try:
                    ConsultantService.delete_consultant(consultant_id)
                except Exception:
                    pass

    def test_consultant_pagination_workflow(self):
        """Test du workflow de pagination des consultants"""

        # Créer plusieurs consultants pour tester la pagination
        consultants_data = []
        for i in range(10):
            consultants_data.append(
                {
                    "prenom": f"Test{i}",
                    "nom": f"User{i}",
                    "email": f"test{i}.user@test.com",
                    "salaire_actuel": 50000 + i * 1000,
                    "practice_id": 1,
                    "disponibilite": True,
                    "grade": "Senior",
                    "societe": "TestCorp",
                }
            )

        created_ids = []

        try:
            # Créer les consultants
            for data in consultants_data:
                result = ConsultantService.create_consultant(data)
                assert result is True
                consultant = ConsultantService.get_consultant_by_email(data["email"])
                created_ids.append(consultant.id)

            # Test de pagination - page 1
            page1 = ConsultantService.get_all_consultants(page=1, per_page=5)
            assert len(page1) == 5

            # Test de pagination - page 2
            page2 = ConsultantService.get_all_consultants(page=2, per_page=5)
            assert len(page2) == 5

            # Vérifier que les pages sont différentes
            page1_ids = [c["id"] for c in page1]
            page2_ids = [c["id"] for c in page2]
            assert set(page1_ids).isdisjoint(set(page2_ids))

            # Test de recherche avec pagination
            search_results = ConsultantService.search_consultants_optimized(
                "Test", page=1, per_page=3
            )
            assert len(search_results) >= 3

            print("✅ Workflow de pagination réussi")

        finally:
            # Nettoyage
            for consultant_id in created_ids:
                try:
                    ConsultantService.delete_consultant(consultant_id)
                except Exception:
                    pass
