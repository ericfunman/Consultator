#!/usr/bin/env python3
"""
Ajout de missions de test pour Eric LAPINA
"""

import sys

sys.path.append(".")

from datetime import date
from datetime import datetime

from app.database.database import get_session
from app.database.models import Consultant
from app.database.models import Mission


def add_test_missions():
    """Ajoute des missions de test pour Eric"""

    try:
        with get_session() as session:
            # Recherche Eric
            eric = (
                session.query(Consultant)
                .filter(Consultant.email == "eric.lapina@quanteam.fr")
                .first()
            )

            if not eric:
                print("❌ Eric LAPINA non trouvé")
                return False

            print(f"✅ Eric trouvé: {eric.prenom} {eric.nom} (ID: {eric.id})")

            # Missions de test à ajouter
            missions_test = [
                {
                    "nom": "MISSION_BNP_2024",
                    "client": "BNP PARIBAS",
                    "debut": date(2024, 1, 15),
                    "fin": date(2024, 6, 30),
                    "tjm": 800,
                },
                {
                    "nom": "MISSION_SOCIETE_GENERALE",
                    "client": "SOCIETE GENERALE",
                    "debut": date(2024, 7, 1),
                    "fin": date(2024, 12, 31),
                    "tjm": 850,
                },
                {
                    "nom": "MISSION_CREDIT_AGRICOLE",
                    "client": "CREDIT AGRICOLE",
                    "debut": date(2025, 1, 1),
                    "fin": None,  # Mission en cours
                    "tjm": 900,
                },
            ]

            missions_ajoutees = 0

            for mission_data in missions_test:
                # Vérifier si la mission existe déjà
                existing = (
                    session.query(Mission)
                    .filter(
                        Mission.consultant_id == eric.id,
                        Mission.nom_mission == mission_data["nom"],
                    )
                    .first()
                )

                if not existing:
                    mission = Mission(
                        consultant_id=eric.id,
                        nom_mission=mission_data["nom"],
                        client=mission_data["client"],
                        date_debut=mission_data["debut"],
                        date_fin=mission_data["fin"],
                        taux_journalier=mission_data["tjm"],
                        description=f"Mission de test - {mission_data['client']}",
                    )

                    session.add(mission)
                    missions_ajoutees += 1

                    fin_str = (
                        mission_data["fin"].strftime("%d/%m/%Y")
                        if mission_data["fin"]
                        else "En cours"
                    )
                    print(
                        f"✅ Mission ajoutée: {mission_data['nom']} ({mission_data['debut'].strftime('%d/%m/%Y')} -> {fin_str})"
                    )
                else:
                    print(f"⚠️ Mission existe déjà: {mission_data['nom']}")

            session.commit()
            print(f"💾 {missions_ajoutees} nouvelles missions sauvegardées")

            # Vérification finale
            total_missions = (
                session.query(Mission).filter(Mission.consultant_id == eric.id).all()
            )
            print(f"\n📊 TOUTES LES MISSIONS D'ERIC ({len(total_missions)}):")
            for mission in total_missions:
                fin_str = (
                    mission.date_fin.strftime("%d/%m/%Y")
                    if mission.date_fin
                    else "En cours"
                )
                print(
                    f"  - {mission.nom_mission}: {mission.date_debut.strftime('%d/%m/%Y')} -> {fin_str} ({mission.client})"
                )

            return True

    except Exception as e:
        print(f"❌ Erreur lors de l'ajout: {e}")
        return False


if __name__ == "__main__":
    print("🔧 Ajout de missions de test pour Eric LAPINA...")
    success = add_test_missions()
    if success:
        print("✅ Ajout terminé!")
    else:
        print("❌ Échec de l'ajout")
