"""
Script pour corriger la mission AFFAS263 manquante d'Eric LAPINA
Ajoute la mission du 21/08/2023 qui n'a pas été importée
"""

import pandas as pd

from app.database.database import get_database_session
from app.database.models import Consultant
from app.database.models import Mission
from app.database.models import VSA_Mission

EXCEL_FILE = r"C:\Users\b302gja\Documents\VSA Personnes.xlsx"


def fix_eric_lapina_mission():
    """Ajoute la mission AFFAS263 du 21/08/2023 manquante pour Eric LAPINA"""

    print("🔄 Correction de la mission AFFAS263 d'Eric LAPINA...")

    # Charger les données Excel
    df_missions = pd.read_excel(EXCEL_FILE, sheet_name="Mission")

    # Trouver la mission manquante
    mission_2023 = df_missions[
        (df_missions["code"] == "AFFAS263")
        & (df_missions["user_id"] == 5230.0)
        & (df_missions["DateDebutMission"] == "2023-08-21")
    ].iloc[0]

    print(f"📋 Mission trouvée: {mission_2023['code']} - {mission_2023['name']}")
    print(
        f"📅 Période: du {mission_2023['DateDebutMission']} au {mission_2023['DateFinMission']}"
    )

    with get_database_session() as session:
        # Trouver Eric LAPINA
        eric = (
            session.query(Consultant)
            .filter(Consultant.email == "eric.lapina@quanteam.fr")
            .first()
        )

        if not eric:
            print("❌ Eric LAPINA non trouvé dans la base")
            return

        print(f"✅ Eric LAPINA trouvé: {eric.prenom} {eric.nom} (ID: {eric.id})")

        # Vérifier si la mission existe déjà
        existing_vsa = (
            session.query(VSA_Mission)
            .filter(
                VSA_Mission.code == "AFFAS263",
                VSA_Mission.user_id == eric.id,
                VSA_Mission.date_debut == mission_2023["DateDebutMission"].date(),
            )
            .first()
        )

        if existing_vsa:
            print("ℹ️ Mission VSA déjà présente")
        else:
            # Créer la mission VSA
            vsa_mission_data = {
                "user_id": eric.id,
                "code": "AFFAS263",
                "orderid": str(int(mission_2023["order_id"])),
                "client_name": "GENERALI VIE",
                "date_debut": mission_2023["DateDebutMission"].date(),
                "date_fin": mission_2023["DateFinMission"].date(),
                "tjm": float(mission_2023["TJM"]),
                "cjm": 834.0,  # Valeur CJM d'Eric
                "description": "3000059886 | DSI Conformité",
                "statut": "active",
            }

            vsa_mission = VSA_Mission(**vsa_mission_data)
            session.add(vsa_mission)
            print("✅ Mission VSA ajoutée")

        # Maintenant, mettre à jour la mission classique
        classic_mission = (
            session.query(Mission)
            .filter(Mission.consultant_id == eric.id, Mission.nom_mission == "AFFAS263")
            .first()
        )

        if classic_mission:
            # Recalculer les dates avec la nouvelle mission VSA
            all_vsa_missions = (
                session.query(VSA_Mission)
                .filter(VSA_Mission.user_id == eric.id, VSA_Mission.code == "AFFAS263")
                .all()
            )

            # Trouver la date de début minimum et la date de fin maximum
            dates_debut = [m.date_debut for m in all_vsa_missions if m.date_debut]
            dates_fin = [m.date_fin for m in all_vsa_missions if m.date_fin]

            if dates_debut:
                new_date_debut = min(dates_debut)
                new_date_fin = max(dates_fin) if dates_fin else None

                print(
                    f"📅 Anciennes dates mission classique: du {classic_mission.date_debut} au {classic_mission.date_fin}"
                )

                # Mettre à jour la mission classique
                classic_mission.date_debut = new_date_debut
                classic_mission.date_fin = new_date_fin

                print(
                    f"📅 Nouvelles dates mission classique: du {new_date_debut} au {new_date_fin}"
                )
                print("✅ Mission classique mise à jour")

        session.commit()
        print("💾 Modifications sauvegardées")


if __name__ == "__main__":
    fix_eric_lapina_mission()
