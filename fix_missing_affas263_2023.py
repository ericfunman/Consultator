"""
Script pour corriger la mission AFFAS263 manquante du 21/08/2023 pour Eric LAPINA
"""

import sys
from datetime import date
from datetime import datetime

import pandas as pd

# Ajouter le chemin de l'app
sys.path.append("app")

from database.database import get_session
from database.models import Consultant
from database.models import Mission
from database.models import VSA_Mission
from import_vsa_missions_complet import validate_mission_data_vsa


def fix_missing_mission():
    """Ajoute la mission manquante et recrée la mission classique"""

    excel_file = r"C:\Users\b302gja\Documents\VSA Personnes.xlsx"

    try:
        # 1. Lire la ligne manquante depuis Excel
        print("🔍 Lecture de la mission manquante depuis Excel...")
        df_missions = pd.read_excel(excel_file, sheet_name="Mission")

        missing_mission = df_missions[
            (df_missions["user_id"] == 5230)
            & (df_missions["order_id"] == 1909)
            & (df_missions["code"] == "AFFAS263")
        ]

        if len(missing_mission) == 0:
            print("❌ Mission non trouvée dans Excel")
            return

        mission_data = missing_mission.iloc[0]
        print(
            f"✅ Mission trouvée: {mission_data['DateDebutMission']} → {mission_data['DateFinMission']}"
        )

        # 2. Valider les données
        print("\n📋 Validation des données...")
        try:
            validated_data = validate_mission_data_vsa(mission_data)
            print("✅ Données validées")
        except Exception as e:
            print(f"❌ Erreur de validation: {e}")
            return

        # 3. Ajouter la mission VSA manquante
        session = get_session()
        try:
            # Vérifier si elle existe déjà
            existing = (
                session.query(VSA_Mission)
                .filter(
                    VSA_Mission.user_id == 190,  # Eric LAPINA
                    VSA_Mission.code == "AFFAS263",
                    VSA_Mission.date_debut == date(2023, 8, 21),
                )
                .first()
            )

            if existing:
                print("⚠️ Mission VSA 2023 existe déjà")
            else:
                # Créer la nouvelle mission VSA
                print("\n➕ Ajout de la mission VSA manquante...")
                new_vsa_mission = VSA_Mission(
                    user_id=190,  # Eric LAPINA dans notre DB
                    code=validated_data["code"],
                    orderid=str(validated_data["orderid"]),
                    client_name=validated_data["client_name"],
                    date_debut=validated_data["date_debut"],
                    date_fin=validated_data["date_fin"],
                    tjm=validated_data["tjm"],
                    cjm=validated_data.get("cjm"),
                    description=validated_data.get("description"),
                    date_import=datetime.now(),
                )

                session.add(new_vsa_mission)
                session.commit()
                print("✅ Mission VSA ajoutée")

            # 4. Recréer la mission classique AFFAS263 avec les bonnes dates
            print("\n🔄 Mise à jour de la mission classique...")

            # Supprimer l'ancienne mission classique AFFAS263
            old_classic = (
                session.query(Mission)
                .filter(Mission.consultant_id == 190, Mission.nom_mission == "AFFAS263")
                .first()
            )

            if old_classic:
                session.delete(old_classic)
                print("🗑️ Ancienne mission classique supprimée")

            # Récupérer toutes les missions VSA AFFAS263 d'Eric
            all_vsa_affas = (
                session.query(VSA_Mission)
                .filter(VSA_Mission.user_id == 190, VSA_Mission.code == "AFFAS263")
                .order_by(VSA_Mission.date_debut)
                .all()
            )

            if all_vsa_affas:
                # Calculer les vraies dates (de la première à la dernière)
                date_debut_min = min(
                    m.date_debut for m in all_vsa_affas if m.date_debut
                )
                date_fin_max = max(m.date_fin for m in all_vsa_affas if m.date_fin)

                # TJM le plus récent
                tjm_recent = all_vsa_affas[-1].tjm

                print(
                    f"📅 Nouvelle mission classique: {date_debut_min} → {date_fin_max}"
                )
                print(f"💰 TJM: {tjm_recent}€")

                # Créer la nouvelle mission classique
                new_classic_mission = Mission(
                    consultant_id=190,
                    nom_mission="AFFAS263",
                    client="GENERALI VIE",
                    date_debut=date_debut_min,
                    date_fin=date_fin_max,
                    tjm=tjm_recent,
                    statut="en_cours" if date_fin_max >= date.today() else "terminee",
                )

                session.add(new_classic_mission)
                session.commit()
                print("✅ Nouvelle mission classique créée")

            session.close()
            print("\n🎉 Correction terminée avec succès !")

        except Exception as e:
            session.rollback()
            session.close()
            print(f"❌ Erreur base de données: {e}")

    except Exception as e:
        print(f"❌ Erreur générale: {e}")


if __name__ == "__main__":
    fix_missing_mission()
