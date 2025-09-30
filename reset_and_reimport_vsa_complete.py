#!/usr/bin/env python3
"""
Script pour vider et recréer complètement les données VSA avec les bonnes relations
"""

from datetime import datetime
import pandas as pd
from app.database.database import get_database_session, reset_database, init_database
from app.database.models import BusinessManager, Consultant, ConsultantBusinessManager, Practice


def classify_person_by_job_title(job_title: str) -> str:
    """
    Classifie une personne comme Business Manager ou Consultant selon son job_title
    MISE À JOUR: Inclut Laurence Oziel comme Business Manager
    """
    if pd.isna(job_title):
        return "consultant"

    job_lower = job_title.lower()

    # Patterns pour identifier les Business Managers
    bm_patterns = [
        "business manager",
        "senior business manager",
    ]

    # Exception spéciale : Directeur de Practice est considéré comme consultant
    if "directeur de practice" in job_lower:
        return "consultant"

    if any(pattern in job_lower for pattern in bm_patterns):
        return "bm"

    return "consultant"


def is_laurence_oziel(firstname: str, lastname: str, email: str) -> bool:
    """
    Identifie spécifiquement Laurence Oziel pour la forcer comme Business Manager
    """
    if pd.isna(firstname) or pd.isna(lastname):
        return False
    
    return (
        firstname.strip().lower() == "laurence" and 
        lastname.strip().lower() == "oziel"
    ) or (
        pd.notna(email) and 
        email.strip().lower() == "laurence.oziel@quanteam.fr"
    )


def reset_and_reimport_vsa_data(excel_path: str):
    """
    Vide complètement la base et reimporte toutes les données VSA avec les bonnes relations
    """
    print("🗑️ ÉTAPE 1: Suppression complète de la base de données...")
    
    # Reset complet de la base
    reset_database()
    print("✅ Base de données vidée")
    
    print("🏗️ ÉTAPE 2: Recréation des tables...")
    init_database()
    print("✅ Tables recréées")
    
    print("📊 ÉTAPE 3: Lecture du fichier Excel...")
    try:
        df = pd.read_excel(excel_path, sheet_name=0)
        print(f"📋 {len(df)} lignes lues depuis Excel")
    except Exception as e:
        print(f"❌ Erreur lecture Excel: {e}")
        return False
    
    print("🔍 ÉTAPE 4: Analyse et classification...")
    
    # Forcer Laurence Oziel comme Business Manager
    def classify_with_laurence_override(row):
        if is_laurence_oziel(row["firstname"], row["lastname"], row.get("email", "")):
            return "bm"
        return classify_person_by_job_title(row["job_title"])
    
    df["classification"] = df.apply(classify_with_laurence_override, axis=1)
    
    classifications = df["classification"].value_counts()
    print(f"👥 Classification: {classifications.get('consultant', 0)} consultants, {classifications.get('bm', 0)} business managers")
    
    # Identifier les BM qui ont des consultants (incluant Laurence)
    bm_with_consultants = set()
    for _, row in df.iterrows():
        if row["classification"] == "consultant":
            manager_name = row["ManagerName"]
            if pd.notna(manager_name):
                bm_with_consultants.add(manager_name.strip())
    
    # Ajouter Laurence même si elle n'a pas de consultants dans ManagerName
    laurence_row = df[df.apply(lambda x: is_laurence_oziel(x["firstname"], x["lastname"], x.get("email", "")), axis=1)]
    if not laurence_row.empty:
        laurence_name = f"{laurence_row.iloc[0]['firstname']} {laurence_row.iloc[0]['lastname']}".strip()
        bm_with_consultants.add(laurence_name)
        print(f"🎯 Laurence Oziel forcée comme Business Manager: {laurence_name}")
    
    print(f"🎯 {len(bm_with_consultants)} Business Managers identifiés")
    
    print("👤 ÉTAPE 5: Création des Business Managers...")
    created_bms = {}
    bm_count = 0
    
    with get_database_session() as session:
        for _, row in df.iterrows():
            if row["classification"] == "bm":
                manager_name = f"{row['firstname']} {row['lastname']}".strip()
                
                # Créer tous les BM identifiés (y compris Laurence)
                if manager_name not in bm_with_consultants and not is_laurence_oziel(row["firstname"], row["lastname"], row.get("email", "")):
                    continue
                
                # Créer le BM
                bm = BusinessManager(
                    nom=row["lastname"].strip(),
                    prenom=row["firstname"].strip(),
                    email=row["email"].strip().lower() if pd.notna(row["email"]) else f"{row['firstname'].lower()}.{row['lastname'].lower()}@quanteam.fr",
                    telephone=row["mobile_number"] if pd.notna(row["mobile_number"]) else None,
                    actif=True,
                    date_creation=datetime.now(),
                )
                
                session.add(bm)
                session.flush()
                created_bms[manager_name] = bm.id
                bm_count += 1
                
                if is_laurence_oziel(row["firstname"], row["lastname"], row.get("email", "")):
                    print(f"✅ Laurence Oziel créée comme BM (ID: {bm.id})")
        
        session.commit()
    
    print(f"✅ {bm_count} Business Managers créés")
    
    print("👥 ÉTAPE 6: Création des consultants avec relations BM...")
    consultant_count = 0
    relations_count = 0
    
    with get_database_session() as session:
        for _, row in df.iterrows():
            if row["classification"] != "consultant":
                continue
            
            # Trouver le BM
            bm_id = None
            manager_name = row["ManagerName"]
            if pd.notna(manager_name):
                bm_id = created_bms.get(manager_name.strip())
                if bm_id:
                    print(f"🔗 Consultant {row['firstname']} {row['lastname']} -> BM {manager_name}")
            
            # Créer le consultant
            consultant = Consultant(
                nom=row["lastname"].strip(),
                prenom=row["firstname"].strip(),
                email=row["email"].strip().lower() if pd.notna(row["email"]) else f"{row['firstname'].lower()}.{row['lastname'].lower()}@quanteam.fr",
                telephone=row["mobile_number"] if pd.notna(row["mobile_number"]) else None,
                salaire_actuel=float(row["Salaire"]) if pd.notna(row["Salaire"]) else None,
                disponibilite=row["UseActive"].strip().lower() == "active" if pd.notna(row["UseActive"]) else True,
                date_entree_societe=pd.to_datetime(row["contract_date"]).date() if pd.notna(row["contract_date"]) else None,
                type_contrat="cdi",  # Par défaut
                societe=row["EntiteCollab"].strip() if pd.notna(row["EntiteCollab"]) else "Quanteam",
                entite=row["EntiteCollab"].strip() if pd.notna(row["EntiteCollab"]) else None,
                actif=row["UseActive"].strip().lower() == "active" if pd.notna(row["UseActive"]) else True,
                date_creation=datetime.now(),
            )
            
            session.add(consultant)
            session.flush()
            
            # Créer la relation BM-consultant
            if bm_id:
                cbm = ConsultantBusinessManager(
                    consultant_id=consultant.id,
                    business_manager_id=bm_id,
                    date_debut=pd.to_datetime(row["contract_date"]).date() if pd.notna(row["contract_date"]) else datetime.now().date(),
                    date_creation=datetime.now(),
                )
                session.add(cbm)
                relations_count += 1
            
            consultant_count += 1
        
        session.commit()
    
    print(f"✅ {consultant_count} consultants créés")
    print(f"🔗 {relations_count} relations BM-consultant établies")
    
    print("📊 ÉTAPE 7: Vérification finale...")
    with get_database_session() as session:
        # Vérifier Laurence
        laurence_bm = session.query(BusinessManager).filter(
            BusinessManager.prenom.ilike('%laurence%'),
            BusinessManager.nom.ilike('%oziel%')
        ).first()
        
        if laurence_bm:
            # Compter ses consultants
            consultants_managed = session.query(ConsultantBusinessManager).filter(
                ConsultantBusinessManager.business_manager_id == laurence_bm.id
            ).count()
            
            print(f"✅ Laurence Oziel (BM ID: {laurence_bm.id}) manage {consultants_managed} consultants")
        else:
            print("❌ Laurence Oziel non trouvée!")
        
        total_bm = session.query(BusinessManager).count()
        total_consultants = session.query(Consultant).count()
        total_relations = session.query(ConsultantBusinessManager).count()
        
        print(f"📊 RÉSUMÉ FINAL:")
        print(f"   - Business Managers: {total_bm}")
        print(f"   - Consultants: {total_consultants}")
        print(f"   - Relations BM-Consultant: {total_relations}")
    
    return True


if __name__ == "__main__":
    print("🔄 RESET ET RÉIMPORT COMPLET DES DONNÉES VSA")
    print("=" * 60)
    
    excel_file = r"C:\Users\b302gja\Documents\VSA Personnes.xlsx"
    
    try:
        success = reset_and_reimport_vsa_data(excel_file)
        if success:
            print("\n🎉 REIMPORT TERMINÉ AVEC SUCCÈS!")
            print("💡 Laurence Oziel est maintenant Business Manager avec ses consultants rattachés")
        else:
            print("\n❌ Erreur lors du réimport")
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        raise