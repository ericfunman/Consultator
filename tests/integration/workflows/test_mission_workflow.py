"""Tests d'intégration pour le workflow mission complet"""

from datetime import date
from datetime import datetime
from datetime import timedelta
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
import streamlit as st

from app.database.database import get_database_session
from app.database.models import Consultant
from app.database.models import Mission
from app.database.models import Practice

# Import des services principaux
from app.services.consultant_service import ConsultantService


# Fixtures pour les tests de mission
@pytest.fixture
def sample_mission_data():
    """Données de test pour une mission"""
    return {
        "nom_mission": "Développement Application Web",
        "client": "Entreprise ABC",
        "description": "Développement complet d'une application web responsive",
        "date_debut": date.today(),
        "date_fin": date.today() + timedelta(days=90),
        "statut": "en_cours",
        "technologies_utilisees": "React, Node.js, MongoDB",
        "revenus_generes": 0,
        "role": "Développeur Full-Stack",
    }


@pytest.fixture
def sample_consultant_for_mission():
    """Créer un consultant de test pour les missions"""
    import uuid

    unique_id = str(uuid.uuid4())[:8]

    data = {
        "prenom": "Marie",
        "nom": f"Leroy_{unique_id}",
        "email": f"marie.leroy.{unique_id}@test.com",
        "telephone": "0123456789",
        "salaire_actuel": 55000,
        "practice_id": 1,
        "disponibilite": True,
        "notes": "Consultant pour tests missions",
        "societe": "TestCorp",
        "grade": "Senior",
        "type_contrat": "CDI",
    }

    result = ConsultantService.create_consultant(data)
    assert result is True

    consultant = ConsultantService.get_consultant_by_email(data["email"])
    yield consultant.id

    # Nettoyage
    try:
        ConsultantService.delete_consultant(consultant.id)
    except:
        pass


class TestMissionWorkflowIntegration:
    """Tests d'intégration pour le workflow mission complet"""

    def test_complete_mission_lifecycle(
        self, sample_consultant_for_mission, sample_mission_data
    ):
        """Test du cycle de vie complet d'une mission"""

        consultant_id = sample_consultant_for_mission
        mission_id = None

        try:
            # === PHASE 1: Création de la mission ===
            print("=== PHASE 1: Création de la mission ===")

            mission_data = sample_mission_data.copy()
            mission_data["consultant_id"] = consultant_id

            with get_database_session() as session:
                mission = Mission(**mission_data)
                session.add(mission)
                session.commit()
                mission_id = mission.id

            # Vérifier que la mission a été créée
            with get_database_session() as session:
                created_mission = (
                    session.query(Mission).filter(Mission.id == mission_id).first()
                )
                assert created_mission is not None
                assert created_mission.nom_mission == sample_mission_data["nom_mission"]
                assert created_mission.client == sample_mission_data["client"]
                assert created_mission.statut == "en_cours"

            print(f"✅ Mission créée avec ID: {mission_id}")

            # === PHASE 2: Modification de la mission ===
            print("=== PHASE 2: Modification de la mission ===")

            with get_database_session() as session:
                mission = (
                    session.query(Mission).filter(Mission.id == mission_id).first()
                )
                mission.description = "Description mise à jour pour le test"
                mission.technologies_utilisees = "React, Node.js, MongoDB, Docker"
                mission.role = "Lead Développeur"
                session.commit()

            # Vérifier les modifications
            with get_database_session() as session:
                updated_mission = (
                    session.query(Mission).filter(Mission.id == mission_id).first()
                )
                assert (
                    updated_mission.description
                    == "Description mise à jour pour le test"
                )
                assert updated_mission.role == "Lead Développeur"

            print("✅ Mission modifiée avec succès")

            # === PHASE 3: Clôture de la mission ===
            print("=== PHASE 3: Clôture de la mission ===")

            with get_database_session() as session:
                mission = (
                    session.query(Mission).filter(Mission.id == mission_id).first()
                )
                mission.statut = "terminee"
                mission.date_fin = date.today() + timedelta(days=85)  # Fin anticipée
                mission.revenus_generes = 45000
                session.commit()

            # Vérifier la clôture
            with get_database_session() as session:
                closed_mission = (
                    session.query(Mission).filter(Mission.id == mission_id).first()
                )
                assert closed_mission.statut == "terminee"
                assert closed_mission.revenus_generes == 45000

            print("✅ Mission clôturée avec succès")

            # === PHASE 4: Vérification des impacts ===
            print("=== PHASE 4: Vérification des impacts ===")

            # Vérifier que le consultant a la mission dans son historique
            consultant_with_stats = ConsultantService.get_consultant_with_stats(
                consultant_id
            )
            assert len(consultant_with_stats["missions"]) > 0

            mission_in_profile = next(
                (m for m in consultant_with_stats["missions"] if m["id"] == mission_id),
                None,
            )
            assert mission_in_profile is not None
            assert mission_in_profile["statut"] == "terminee"
            assert mission_in_profile["revenus_generes"] == 45000

            print("✅ Impacts vérifiés dans le profil consultant")

            print("🎉 CYCLE DE VIE MISSION RÉUSSI !")

        finally:
            # === NETTOYAGE ===
            if mission_id:
                print("=== NETTOYAGE MISSION ===")
                try:
                    with get_database_session() as session:
                        mission = (
                            session.query(Mission)
                            .filter(Mission.id == mission_id)
                            .first()
                        )
                        if mission:
                            session.delete(mission)
                            session.commit()
                    print("✅ Mission supprimée (nettoyage)")
                except Exception as e:
                    print(f"⚠️ Erreur lors du nettoyage mission: {e}")

    def test_multiple_missions_workflow(self, sample_consultant_for_mission):
        """Test de gestion de plusieurs missions pour un consultant"""

        consultant_id = sample_consultant_for_mission
        mission_ids = []

        try:
            # Créer plusieurs missions
            missions_data = [
                {
                    "nom_mission": "Mission 1 - API Development",
                    "client": "Client A",
                    "description": "Développement API REST",
                    "date_debut": date.today() - timedelta(days=30),
                    "date_fin": date.today() + timedelta(days=30),
                    "statut": "en_cours",
                    "technologies_utilisees": "Python, FastAPI",
                    "revenus_generes": 0,
                    "consultant_id": consultant_id,
                },
                {
                    "nom_mission": "Mission 2 - Frontend Development",
                    "client": "Client B",
                    "description": "Développement interface utilisateur",
                    "date_debut": date.today() - timedelta(days=60),
                    "date_fin": date.today() - timedelta(days=10),
                    "statut": "terminee",
                    "technologies_utilisees": "React, TypeScript",
                    "revenus_generes": 35000,
                    "consultant_id": consultant_id,
                },
                {
                    "nom_mission": "Mission 3 - Database Design",
                    "client": "Client C",
                    "description": "Conception base de données",
                    "date_debut": date.today() - timedelta(days=90),
                    "date_fin": date.today() - timedelta(days=20),
                    "statut": "terminee",
                    "technologies_utilisees": "PostgreSQL, MongoDB",
                    "revenus_generes": 28000,
                    "consultant_id": consultant_id,
                },
            ]

            # Créer les missions
            for mission_data in missions_data:
                with get_database_session() as session:
                    mission = Mission(**mission_data)
                    session.add(mission)
                    session.commit()
                    mission_ids.append(mission.id)

            # Vérifier que toutes les missions sont créées
            with get_database_session() as session:
                missions = (
                    session.query(Mission)
                    .filter(Mission.consultant_id == consultant_id)
                    .all()
                )
                assert len(missions) == 3

            # Vérifier les statistiques du consultant
            consultant_with_stats = ConsultantService.get_consultant_with_stats(
                consultant_id
            )
            assert len(consultant_with_stats["missions"]) == 3

            # Calculer les revenus totaux
            total_revenus = sum(
                m["revenus_generes"] for m in consultant_with_stats["missions"]
            )
            assert total_revenus == 63000  # 0 + 35000 + 28000

            # Vérifier le nombre de missions terminées
            completed_missions = [
                m
                for m in consultant_with_stats["missions"]
                if m["statut"] == "terminee"
            ]
            assert len(completed_missions) == 2

            # Vérifier qu'il y a une mission en cours
            active_missions = [
                m
                for m in consultant_with_stats["missions"]
                if m["statut"] == "en_cours"
            ]
            assert len(active_missions) == 1

            print("✅ Gestion de plusieurs missions réussie")

        finally:
            # Nettoyage
            for mission_id in mission_ids:
                try:
                    with get_database_session() as session:
                        mission = (
                            session.query(Mission)
                            .filter(Mission.id == mission_id)
                            .first()
                        )
                        if mission:
                            session.delete(mission)
                            session.commit()
                except:
                    pass

    def test_mission_status_transitions(self, sample_consultant_for_mission):
        """Test des transitions d'état des missions"""

        consultant_id = sample_consultant_for_mission
        mission_id = None

        try:
            # Créer une mission
            mission_data = {
                "nom_mission": "Test Status Transitions",
                "client": "Test Client",
                "description": "Test des transitions d'état",
                "date_debut": date.today(),
                "date_fin": date.today() + timedelta(days=60),
                "statut": "en_cours",
                "technologies_utilisees": "Python",
                "revenus_generes": 0,
                "consultant_id": consultant_id,
            }

            with get_database_session() as session:
                mission = Mission(**mission_data)
                session.add(mission)
                session.commit()
                mission_id = mission.id

            # Test des transitions d'état
            status_transitions = [
                ("en_cours", "Mission en cours"),
                ("suspendue", "Mission suspendue temporairement"),
                ("terminee", "Mission terminée avec succès"),
                ("annulee", "Mission annulée"),
            ]

            for status, description in status_transitions:
                with get_database_session() as session:
                    mission = (
                        session.query(Mission).filter(Mission.id == mission_id).first()
                    )
                    mission.statut = status
                    if status == "terminee":
                        mission.revenus_generes = 30000
                    session.commit()

                # Vérifier le changement d'état
                with get_database_session() as session:
                    updated_mission = (
                        session.query(Mission).filter(Mission.id == mission_id).first()
                    )
                    assert updated_mission.statut == status

                print(f"✅ Transition vers '{status}' réussie")

            # Vérifier l'impact sur les statistiques du consultant
            consultant_with_stats = ConsultantService.get_consultant_with_stats(
                consultant_id
            )
            missions = consultant_with_stats["missions"]
            assert len(missions) == 1

            final_mission = missions[0]
            assert final_mission["statut"] == "annulee"  # Dernier état

            print("✅ Transitions d'état des missions réussies")

        finally:
            # Nettoyage
            if mission_id:
                try:
                    with get_database_session() as session:
                        mission = (
                            session.query(Mission)
                            .filter(Mission.id == mission_id)
                            .first()
                        )
                        if mission:
                            session.delete(mission)
                            session.commit()
                except:
                    pass

    def test_mission_date_management(self, sample_consultant_for_mission):
        """Test de la gestion des dates dans les missions"""

        consultant_id = sample_consultant_for_mission
        mission_id = None

        try:
            # Créer une mission avec des dates
            base_date = date.today()
            mission_data = {
                "nom_mission": "Test Date Management",
                "client": "Test Client",
                "description": "Test de gestion des dates",
                "date_debut": base_date,
                "date_fin": base_date + timedelta(days=30),
                "statut": "en_cours",
                "technologies_utilisees": "Python",
                "revenus_generes": 0,
                "consultant_id": consultant_id,
            }

            with get_database_session() as session:
                mission = Mission(**mission_data)
                session.add(mission)
                session.commit()
                mission_id = mission.id

            # Test de modification des dates
            new_start_date = base_date + timedelta(days=5)
            new_end_date = base_date + timedelta(days=45)

            with get_database_session() as session:
                mission = (
                    session.query(Mission).filter(Mission.id == mission_id).first()
                )
                mission.date_debut = new_start_date
                mission.date_fin = new_end_date
                session.commit()

            # Vérifier les nouvelles dates
            with get_database_session() as session:
                updated_mission = (
                    session.query(Mission).filter(Mission.id == mission_id).first()
                )
                assert updated_mission.date_debut == new_start_date
                assert updated_mission.date_fin == new_end_date

            # Test de calcul de durée
            duration_days = (updated_mission.date_fin - updated_mission.date_debut).days
            assert duration_days == 40

            print("✅ Gestion des dates des missions réussie")

        finally:
            # Nettoyage
            if mission_id:
                try:
                    with get_database_session() as session:
                        mission = (
                            session.query(Mission)
                            .filter(Mission.id == mission_id)
                            .first()
                        )
                        if mission:
                            session.delete(mission)
                            session.commit()
                except:
                    pass
