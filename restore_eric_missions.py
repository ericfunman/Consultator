#!/usr/bin/env python3
"""
Script pour restaurer les missions manquantes d'Eric LAPINA
"""

from datetime import datetime

import pandas as pd

from app.database.database import get_session
from app.database.models import Consultant
from app.database.models import Mission
from app.database.models import VSA_Mission


def restore_eric_missions():
    """Restaure les missions manquantes d'Eric depuis les fichiers VSA"""

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

            # Missions actuelles
            missions_actuelles = (
                session.query(Mission).filter(Mission.consultant_id == eric.id).all()
            )
            vsa_actuelles = (
                session.query(VSA_Mission).filter(VSA_Mission.user_id == eric.id).all()
            )

            print(
                f"📊 État actuel: {len(missions_actuelles)} missions classiques, {len(vsa_actuelles)} VSA"
            )

            # Lire le fichier VSA Missions
            try:
                df_missions = pd.read_excel(
                    "missions_vsa_example.xlsx", sheet_name="Mission"
                )
                print(f"📖 {len(df_missions)} missions trouvées dans le fichier Excel")

                # Filtrer pour Eric LAPINA (user_id = 190)
                eric_missions = df_missions[df_missions["user_id"] == eric.id]

                print(f"🎯 {len(eric_missions)} missions trouvées pour Eric LAPINA")

                missions_ajoutees = 0
                for _, row in eric_missions.iterrows():
                    code_mission = str(row.get("Code", ""))

                    # Éviter de dupliquer AFFAS263
                    if "AFFAS263" in code_mission:
                        continue

                    # Vérifier si cette mission existe déjà
                    mission_existante = (
                        session.query(Mission)
                        .filter(
                            Mission.consultant_id == eric.id,
                            Mission.nom_mission == code_mission,
                        )
                        .first()
                    )

                    if mission_existante:
                        continue

                        # Créer la mission
                        try:
                            date_debut = pd.to_datetime(
                                row.get("date_debut", ""), errors="coerce"
                            )
                            date_fin = pd.to_datetime(
                                row.get("date_fin", ""), errors="coerce"
                            )

                            if pd.isna(date_debut):
                                continue

                            mission = Mission(
                                consultant_id=eric.id,
                                nom_mission=code_mission,
                                client=str(row.get("name", "")),
                                date_debut=date_debut.date(),
                                date_fin=(
                                    date_fin.date() if not pd.isna(date_fin) else None
                                ),
                                taux_journalier=(
                                    float(row.get("TJM", 0))
                                    if pd.notna(row.get("TJM"))
                                    else None
                                ),
                                description="Mission importée depuis VSA",
                            )
                            session.add(mission)
                            missions_ajoutees += 1
                            print(
                                f"✅ Mission ajoutée: {code_mission} ({date_debut.date()} -> {date_fin.date() if not pd.isna(date_fin) else 'En cours'})"
                            )

                        except Exception as e:
                            print(f"⚠️ Erreur mission {code_mission}: {e}")
                            continue

                session.commit()
                print(f"💾 {missions_ajoutees} nouvelles missions sauvegardées")

                # Vérification finale
                missions_finales = (
                    session.query(Mission)
                    .filter(Mission.consultant_id == eric.id)
                    .all()
                )
                print(f"🎉 Eric a maintenant {len(missions_finales)} missions au total")

                return True

            except FileNotFoundError:
                print("❌ Fichier missions_vsa_example.xlsx non trouvé")
                return False

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


if __name__ == "__main__":
    print("🔧 Restauration des missions d'Eric LAPINA...")
    success = restore_eric_missions()
    if success:
        print("✅ Restauration terminée!")
    else:
        print("❌ Échec de la restauration")
