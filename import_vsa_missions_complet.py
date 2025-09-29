"""
Script d'import complet des missions VSA depuis le fichier VSA Personnes.xlsx
Corrige le problème de mapping des user_ids
"""

import os
import sys
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.database.database import get_database_session
from app.database.models import Consultant
from app.database.models import Mission
from app.database.models import VsaMission

# Configuration
EXCEL_FILE = r"C:\Users\b302gja\Documents\VSA Personnes.xlsx"
SHEET_MISSION = "Mission"
SHEET_PERSONNE = "Personne"


def create_user_id_mapping():
    """
    Crée un mapping entre les user_ids du fichier VSA et les IDs des consultants en base
    basé sur l'email comme clé de correspondance
    """
    mapping = {}

    print("🔄 Création du mapping user_id -> consultant_id...")

    # Charger les données VSA Personnes
    df_personnes = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_PERSONNE)

    with get_database_session() as session:
        # Pour chaque personne VSA, chercher le consultant correspondant
        for _, row in df_personnes.iterrows():
            vsa_user_id = row.get("user_id")
            vsa_email = str(row.get("email", "")).strip().lower()

            if pd.notna(vsa_user_id) and vsa_email:
                # Chercher le consultant avec le même email
                consultant = (
                    session.query(Consultant)
                    .filter(Consultant.email == vsa_email)
                    .first()
                )

                if consultant:
                    mapping[vsa_user_id] = consultant.id
                    print(
                        f"✅ Mapping: user_id {vsa_user_id} -> consultant_id {consultant.id} ({consultant.prenom} {consultant.nom})"
                    )
                else:
                    print(
                        f"⚠️ Consultant non trouvé pour email: {vsa_email} (user_id: {vsa_user_id})"
                    )

    print(f"📊 Mapping créé: {len(mapping)} correspondances")
    return mapping


def validate_mission_data_vsa(row) -> Dict:
    """Valide et nettoie les données d'une mission VSA depuis le fichier complet"""
    mission_data = {}

    try:
        # user_id (sera remappé plus tard)
        user_id = row.get("user_id")
        if pd.isna(user_id):
            raise ValueError("user_id manquant")
        mission_data["user_id"] = int(user_id)

        # Code de mission (généré si manquant)
        code = str(row.get("code", "")).strip()
        if not code or code == "nan" or code == "N/A":
            # Générer un code unique basé sur user_id et order_id
            order_id = str(row.get("order_id", "UNK")).strip()
            code = f"VSA-{user_id}-{order_id}"
        mission_data["code"] = code

        # Order ID
        order_id = str(row.get("order_id", "")).strip()
        mission_data["orderid"] = (
            order_id if order_id and order_id != "nan" else f"ORDER-{user_id}"
        )

        # Nom du client
        client_name = str(row.get("name", "")).strip()
        if not client_name or client_name == "nan":
            client_name = "Client non spécifié"
        mission_data["client_name"] = client_name

        # Dates
        try:
            date_debut = pd.to_datetime(row.get("DateDebutMission"), errors="coerce")
            mission_data["date_debut"] = (
                date_debut.date() if pd.notna(date_debut) else None
            )
        except:
            mission_data["date_debut"] = None

        try:
            date_fin = pd.to_datetime(row.get("DateFinMission"), errors="coerce")
            mission_data["date_fin"] = date_fin.date() if pd.notna(date_fin) else None
        except:
            mission_data["date_fin"] = None

        # TJM et CJM
        try:
            mission_data["tjm"] = (
                float(row.get("TJM", 0)) if pd.notna(row.get("TJM")) else None
            )
        except (ValueError, TypeError):
            mission_data["tjm"] = None

        try:
            # Essayer CJM_f1 puis CJM_f2
            cjm = row.get("CJM_f1")
            if pd.isna(cjm):
                cjm = row.get("CJM_f2")
            mission_data["cjm"] = float(cjm) if pd.notna(cjm) else None
        except (ValueError, TypeError):
            mission_data["cjm"] = None

        # Description (combiner plusieurs champs si disponibles)
        description_parts = []
        for field in ["TITRE", "description_Entete", "RESUME", "Description"]:
            value = str(row.get(field, "")).strip()
            if value and value != "nan" and value not in description_parts:
                description_parts.append(value)

        mission_data["description"] = (
            " | ".join(description_parts) if description_parts else None
        )
        mission_data["statut"] = "active"

    except Exception as e:
        raise ValueError(f"Erreur de validation: {e}")

    return mission_data


def create_classic_missions_from_vsa():
    """
    Crée des missions classiques dans la table Mission à partir des données VSA
    Agrège par code mission (hors INT) et consultant
    """
    print("\n🔄 Création des missions classiques depuis les données VSA...")

    stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

    with get_database_session() as session:
        # Récupérer toutes les missions VSA dont le code ne commence pas par INT
        vsa_missions = (
            session.query(VsaMission).filter(~VsaMission.code.startswith("INT")).all()
        )

        print(f"📊 {len(vsa_missions)} missions VSA externes trouvées")

        # Regrouper par consultant et code mission
        mission_groups = {}
        for vsa_mission in vsa_missions:
            key = (vsa_mission.user_id, vsa_mission.code)
            if key not in mission_groups:
                mission_groups[key] = []
            mission_groups[key].append(vsa_mission)

        print(f"📊 {len(mission_groups)} groupes de missions à traiter")

        for (consultant_id, mission_code), vsa_missions_group in mission_groups.items():
            try:
                # Trier les missions VSA par date de début pour avoir la chronologie
                vsa_missions_group.sort(
                    key=lambda m: m.date_debut if m.date_debut else datetime.min.date()
                )

                # Calculer les agrégations
                dates_debut = [m.date_debut for m in vsa_missions_group if m.date_debut]
                dates_fin = [m.date_fin for m in vsa_missions_group if m.date_fin]

                if not dates_debut:
                    print(
                        f"⚠️ Pas de date de début pour {mission_code}, mission ignorée"
                    )
                    stats["skipped"] += 1
                    continue

                date_debut_mission = min(dates_debut)
                date_fin_mission = max(dates_fin) if dates_fin else None

                # Récupérer le dernier TJM et CJM de la période (chronologiquement)
                derniere_vsa = vsa_missions_group[
                    -1
                ]  # Dernière dans l'ordre chronologique
                tjm_final = derniere_vsa.tjm
                cjm_final = derniere_vsa.cjm

                # Nom de la mission = code VSA
                nom_mission = mission_code
                client_name = vsa_missions_group[
                    0
                ].client_name  # Prendre le client du premier

                # Vérifier si une mission classique existe déjà avec ce nom pour ce consultant
                existing_mission = (
                    session.query(Mission)
                    .filter(
                        Mission.consultant_id == consultant_id,
                        Mission.nom_mission == nom_mission,
                    )
                    .first()
                )

                # Récupérer le consultant pour affichage
                consultant = (
                    session.query(Consultant)
                    .filter(Consultant.id == consultant_id)
                    .first()
                )
                consultant_name = (
                    f"{consultant.prenom} {consultant.nom}"
                    if consultant
                    else f"ID:{consultant_id}"
                )

                if existing_mission:
                    # Mettre à jour la mission existante
                    existing_mission.client = client_name
                    existing_mission.date_debut = date_debut_mission
                    existing_mission.date_fin = date_fin_mission
                    existing_mission.tjm = tjm_final
                    existing_mission.taux_journalier = tjm_final  # Pour compatibilité
                    existing_mission.statut = (
                        "terminee" if date_fin_mission else "en_cours"
                    )

                    print(
                        f"🔄 Mission classique mise à jour: {nom_mission} ({consultant_name} -> {client_name})"
                    )
                    stats["updated"] += 1
                else:
                    # Créer une nouvelle mission classique
                    mission_data = {
                        "consultant_id": consultant_id,
                        "nom_mission": nom_mission,
                        "client": client_name,
                        "date_debut": date_debut_mission,
                        "date_fin": date_fin_mission,
                        "tjm": tjm_final,
                        "taux_journalier": tjm_final,  # Pour compatibilité
                        "statut": "terminee" if date_fin_mission else "en_cours",
                        "description": f"Mission créée automatiquement depuis VSA - Code: {mission_code}",
                    }

                    classic_mission = Mission(**mission_data)
                    session.add(classic_mission)

                    print(
                        f"✅ Mission classique créée: {nom_mission} ({consultant_name} -> {client_name})"
                    )
                    print(
                        f"   📅 Du {date_debut_mission} au {date_fin_mission or 'En cours'}"
                    )
                    if tjm_final:
                        print(f"   💰 TJM: {tjm_final:,.0f}€")

                    stats["created"] += 1

                # Commit périodique
                if (stats["created"] + stats["updated"]) % 50 == 0:
                    session.commit()

            except Exception as e:
                print(f"❌ Erreur création mission classique {mission_code}: {e}")
                stats["errors"] += 1
                continue

        # Commit final
        session.commit()

    print(f"\n🎉 Création missions classiques terminée:")
    print(f"   ✅ Nouvelles missions: {stats['created']}")
    print(f"   🔄 Missions mises à jour: {stats['updated']}")
    print(f"   ⚠️ Missions ignorées: {stats['skipped']}")
    print(f"   ❌ Erreurs: {stats['errors']}")

    return stats


def import_vsa_missions_complet():
    """
    Importe toutes les missions VSA depuis le fichier complet avec mapping correct
    """
    stats = {"imported": 0, "errors": 0, "skipped": 0, "updated": 0}

    print(f"🚀 Import des missions VSA depuis {EXCEL_FILE}")

    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Fichier non trouvé: {EXCEL_FILE}")
        return stats

    # Créer le mapping user_id -> consultant_id
    user_mapping = create_user_id_mapping()

    if not user_mapping:
        print("❌ Aucun mapping créé, arrêt de l'import")
        return stats

    # Charger les missions
    df_missions = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_MISSION)
    print(f"📊 {len(df_missions)} missions trouvées dans le fichier")

    with get_database_session() as session:
        for index, row in df_missions.iterrows():
            try:
                # Valider les données
                mission_data = validate_mission_data_vsa(row)
                vsa_user_id = mission_data["user_id"]

                # Vérifier si on a un mapping pour ce user_id
                if vsa_user_id not in user_mapping:
                    print(
                        f"⚠️ Pas de mapping pour user_id {vsa_user_id}, mission ignorée"
                    )
                    stats["skipped"] += 1
                    continue

                # Remapper l'user_id vers l'ID consultant
                mission_data["user_id"] = user_mapping[vsa_user_id]
                consultant_id = mission_data["user_id"]

                # Vérifier si la mission existe déjà (par code + user_id + date_debut pour éviter les doublons)
                existing_mission = (
                    session.query(VsaMission)
                    .filter(
                        VsaMission.code == mission_data["code"],
                        VsaMission.user_id == mission_data["user_id"],
                        VsaMission.date_debut == mission_data["date_debut"],
                    )
                    .first()
                )

                if existing_mission:
                    # Mettre à jour la mission existante
                    for key, value in mission_data.items():
                        if key != "id":  # Ne pas modifier l'ID
                            setattr(existing_mission, key, value)

                    consultant = (
                        session.query(Consultant)
                        .filter(Consultant.id == consultant_id)
                        .first()
                    )
                    consultant_name = (
                        f"{consultant.prenom} {consultant.nom}"
                        if consultant
                        else f"ID:{consultant_id}"
                    )

                    print(
                        f"🔄 Mission mise à jour: {mission_data['code']} ({consultant_name} -> {mission_data['client_name']})"
                    )
                    stats["updated"] += 1
                else:
                    # Créer une nouvelle mission
                    vsa_mission = VsaMission(**mission_data)
                    session.add(vsa_mission)

                    consultant = (
                        session.query(Consultant)
                        .filter(Consultant.id == consultant_id)
                        .first()
                    )
                    consultant_name = (
                        f"{consultant.prenom} {consultant.nom}"
                        if consultant
                        else f"ID:{consultant_id}"
                    )

                    print(
                        f"✅ Mission créée: {mission_data['code']} ({consultant_name} -> {mission_data['client_name']})"
                    )
                    stats["imported"] += 1

                # Commit périodique pour éviter les blocages
                if (stats["imported"] + stats["updated"]) % 100 == 0:
                    session.commit()

            except Exception as e:
                print(f"❌ Erreur mission ligne {index + 1}: {e}")
                stats["errors"] += 1
                continue

        # Commit final
        session.commit()

    print("🎉 Import terminé:")
    print(f"   ✅ Nouvelles missions: {stats['imported']}")
    print(f"   🔄 Missions mises à jour: {stats['updated']}")
    print(f"   ⚠️ Missions ignorées: {stats['skipped']}")
    print(f"   ❌ Erreurs: {stats['errors']}")

    # Créer les missions classiques depuis les données VSA
    classic_stats = create_classic_missions_from_vsa()

    return stats, classic_stats


if __name__ == "__main__":
    vsa_stats, classic_stats = import_vsa_missions_complet()
