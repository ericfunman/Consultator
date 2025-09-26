"""
Script d'import des données VSA Personnes depuis Excel
Importe les consultants et business managers depuis le fichier Excel
"""

from datetime import datetime

import pandas as pd

from app.database.database import get_database_session
from app.database.models import BusinessManager
from app.database.models import Consultant
from app.database.models import ConsultantBusinessManager
from app.database.models import Practice


def classify_person_by_job_title(job_title: str) -> str:
    """
    Classifie une personne comme Business Manager ou Consultant selon son job_title

    Args:
        job_title (str): Le titre du poste

    Returns:
        str: 'bm' pour Business Manager, 'consultant' pour Consultant
    """
    if pd.isna(job_title):
        return "consultant"

    job_lower = job_title.lower()

    # Patterns pour identifier les Business Managers
    bm_patterns = [
        "business manager",
        "senior business manager",
        # 'directeur' retiré car un Directeur de Practice est d'abord un consultant
    ]

    # Exception spéciale : Directeur de Practice est considéré comme consultant
    if "directeur de practice" in job_lower:
        return "consultant"

    if any(pattern in job_lower for pattern in bm_patterns):
        return "bm"

    return "consultant"


def map_contract_type(contract_code: str) -> str:
    """
    Mappe le type de contrat Excel vers une catégorie simple

    Args:
        contract_code (str): Code du contrat dans Excel

    Returns:
        str: 'cdi', 'cdd', 'stage', 'apprentissage', 'autre'
    """
    if pd.isna(contract_code):
        return "autre"

    code_lower = contract_code.lower()

    if "cdi" in code_lower:
        return "cdi"
    elif "cdd" in code_lower:
        return "cdd"
    elif "stage" in code_lower:
        return "stage"
    elif "apprentissage" in code_lower:
        return "apprentissage"
    else:
        return "autre"


def import_vsa_personnes_data(excel_path: str, practice_mapping: dict = None):
    """
    Importe les données depuis le fichier Excel VSA Personnes

    Args:
        excel_path (str): Chemin vers le fichier Excel
        practice_mapping (dict): Mapping EntiteCollab -> Practice ID (optionnel)
    """
    print("🚀 Début de l'import des données VSA Personnes")

    try:
        # Lire le fichier Excel
        df = pd.read_excel(excel_path, sheet_name=0)
        print(f"📊 {len(df)} lignes lues depuis Excel")

        # Statistiques de classification
        classifications = (
            df["job_title"].apply(classify_person_by_job_title).value_counts()
        )
        print(
            f"👥 Classification: {classifications.get('consultant', 0)} consultants, {classifications.get('bm', 0)} business managers"
        )

        # Première passe: Identifier les BM qui ont des consultants
        bm_with_consultants = set()
        for _, row in df.iterrows():
            if classify_person_by_job_title(row["job_title"]) == "consultant":
                manager_name = row["ManagerName"]
                if pd.notna(manager_name):
                    bm_with_consultants.add(manager_name.strip())

        print(f"🎯 {len(bm_with_consultants)} Business Managers ont des consultants")

        # Créer les BM qui ont des consultants
        created_bms = {}
        bm_count = 0

        with get_database_session() as session:
            for _, row in df.iterrows():
                if classify_person_by_job_title(row["job_title"]) == "bm":
                    manager_name = f"{row['firstname']} {row['lastname']}".strip()

                    # Ne créer que les BM qui ont des consultants
                    if manager_name not in bm_with_consultants:
                        continue

                    # Vérifier si le BM existe déjà
                    existing_bm = (
                        session.query(BusinessManager)
                        .filter(BusinessManager.email == row["email"].strip().lower())
                        .first()
                    )

                    if existing_bm:
                        created_bms[manager_name] = existing_bm.id
                        continue

                    # Créer le BM
                    bm = BusinessManager(
                        nom=row["lastname"].strip(),
                        prenom=row["firstname"].strip(),
                        email=row["email"].strip().lower(),
                        telephone=(
                            row["mobile_number"]
                            if pd.notna(row["mobile_number"])
                            else None
                        ),
                        actif=True,  # Tous les BM sont actifs
                        date_creation=datetime.now(),
                    )

                    session.add(bm)
                    session.flush()  # Pour obtenir l'ID
                    created_bms[manager_name] = bm.id
                    bm_count += 1

            session.commit()

        print(f"✅ {bm_count} Business Managers créés")

        # Deuxième passe: Les practices seront créées manuellement par l'utilisateur
        # On ne fait rien ici, l'utilisateur nous donnera la liste

        # Troisième passe: Créer les consultants
        consultant_count = 0
        skipped_count = 0

        with get_database_session() as session:
            for _, row in df.iterrows():
                if classify_person_by_job_title(row["job_title"]) != "consultant":
                    continue

                # Vérifier si le consultant existe déjà
                existing_consultant = (
                    session.query(Consultant)
                    .filter(Consultant.email == row["email"].strip().lower())
                    .first()
                )

                if existing_consultant:
                    skipped_count += 1
                    continue

                # Trouver le BM
                bm_id = None
                manager_name = row["ManagerName"]
                if pd.notna(manager_name):
                    bm_id = created_bms.get(manager_name.strip())

                # Créer le consultant
                consultant = Consultant(
                    nom=row["lastname"].strip(),
                    prenom=row["firstname"].strip(),
                    email=row["email"].strip().lower(),
                    telephone=(
                        row["mobile_number"] if pd.notna(row["mobile_number"]) else None
                    ),
                    salaire_actuel=(
                        float(row["Salaire"]) if pd.notna(row["Salaire"]) else None
                    ),
                    disponibilite=(
                        row["UseActive"].strip().lower() == "active"
                        if pd.notna(row["UseActive"])
                        else True
                    ),
                    date_entree_societe=(
                        pd.to_datetime(row["contract_date"]).date()
                        if pd.notna(row["contract_date"])
                        else None
                    ),
                    # practice_id sera défini quand l'utilisateur nous donnera le mapping
                    type_contrat=(
                        map_contract_type(row["contract_type_code"])
                        if pd.notna(row["contract_type_code"])
                        else "cdi"
                    ),
                    societe=(
                        row["EntiteCollab"].strip()
                        if pd.notna(row["EntiteCollab"])
                        else "Quanteam"
                    ),
                    entite=(
                        row["EntiteCollab"].strip()
                        if pd.notna(row["EntiteCollab"])
                        else None
                    ),
                    # Nouveaux champs période d'essai et statut actif
                    etat_periode_essai=(
                        row["Etat P.Test"].strip()
                        if pd.notna(row["Etat P.Test"])
                        else None
                    ),
                    fin_periode_essai=(
                        pd.to_datetime(row["Fin P.Test"]).date()
                        if pd.notna(row["Fin P.Test"])
                        else None
                    ),
                    actif=(
                        row["UseActive"].strip().lower() == "active"
                        if pd.notna(row["UseActive"])
                        else True
                    ),
                    date_creation=datetime.now(),
                )

                session.add(consultant)
                session.flush()  # Pour obtenir l'ID du consultant

                # Créer la relation BM-consultant si nécessaire
                if bm_id:
                    cbm = ConsultantBusinessManager(
                        consultant_id=consultant.id,
                        business_manager_id=bm_id,
                        date_debut=(
                            pd.to_datetime(row["contract_date"]).date()
                            if pd.notna(row["contract_date"])
                            else datetime.now().date()
                        ),
                        date_creation=datetime.now(),
                    )
                    session.add(cbm)

                consultant_count += 1

            session.commit()

        print(f"✅ {consultant_count} consultants créés")
        if skipped_count > 0:
            print(f"⏭️ {skipped_count} consultants déjà existants (ignorés)")

        print("🎉 Import terminé avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        raise


if __name__ == "__main__":
    # Chemin vers le fichier Excel
    excel_file = r"C:\Users\b302gja\Documents\VSA Personnes.xlsx"

    # Lancer l'import
    import_vsa_personnes_data(excel_file)
