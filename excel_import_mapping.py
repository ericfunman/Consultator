"""
Script d'import Excel vers base de données Consultants
Mapping des colonnes Excel vers le modèle Consultant
"""

from datetime import date
from datetime import datetime

import pandas as pd

from database.database import get_database_session
from database.models import Consultant
from database.models import Practice


def analyze_excel_file():
    """Analyse le fichier Excel et affiche la structure"""
    print("📋 ANALYSE DU FICHIER EXCEL")
    print("=" * 50)

    try:
        # Lire le fichier Excel
        excel_file = pd.ExcelFile("Data Quanteam 1 ligne.xlsx")  # noqa: F841
        df = pd.read_excel("Data Quanteam 1 ligne.xlsx", sheet_name="Consultant")

        print(f"📊 Nombre de lignes: {len(df)}")
        print(f"📊 Nombre de colonnes: {len(df.columns)}")
        print()

        print("🔍 Colonnes Excel détectées:")
        for i, col in enumerate(df.columns, 1):
            sample_value = df[col].iloc[0] if len(df) > 0 else "N/A"
            print(f"  {i:2d}. {col:<20} | Exemple: {sample_value}")

        print()
        print("👁️ Aperçu des données:")
        print(df.head(3).to_string(max_cols=6))

        return df

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None


def get_mapping_proposal():
    """Propose un mapping entre colonnes Excel et champs DB"""

    mapping = {
        # MAPPING EXCEL -> BASE DE DONNÉES
        # Format: "Colonne Excel": "champ_db"
        # ✅ CORRESPONDANCES DIRECTES
        "Prenom": "prenom",
        "Nom": "nom",
        "email": "email",
        "Num Telephonne": "telephone",  # Note: typo dans Excel
        "Société": "societe",
        "Date Entree Société": "date_entree_societe",
        "Date Sortie société": "date_sortie_societe",
        "Date de naissance": None,  # Pas de champ correspondant en DB
        # 🔄 CORRESPONDANCES AVEC TRANSFORMATION
        "CJM": "salaire_actuel",  # CJM = Coût Journalier Moyen
        "Salaire": None,  # Doublon avec CJM, on garde CJM
        "contract_type_code": "type_contrat",  # CDI/CDD/etc.
        "UseActive": "disponibilite",  # Active/Inactive -> Boolean
        # ⚠️ CHAMPS DB NON FOURNIS DANS EXCEL
        # Ces champs devront être définis par défaut:
        # - grade (défaut: 'Junior')
        # - practice_id (défaut: None ou Practice par défaut)
        # - date_premiere_mission (défaut: None)
        # - notes (défaut: None)
    }

    return mapping


def show_mapping_proposal():
    """Affiche le mapping proposé de manière claire"""

    print("\n🎯 PROPOSITION DE MAPPING")
    print("=" * 50)

    mapping = get_mapping_proposal()

    print("✅ CORRESPONDANCES DIRECTES:")
    for excel_col, db_field in mapping.items():
        if db_field and not excel_col.startswith("~"):
            print(f"  📋 {excel_col:<25} → {db_field}")

    print("\n🔄 CORRESPONDANCES AVEC TRANSFORMATION:")
    transformations = {
        "CJM": "salaire_actuel (CJM = Coût Journalier Moyen)",
        "contract_type_code": "type_contrat (CDI/CDD/Stagiaire/etc.)",
        "UseActive": "disponibilite (Active → True, Inactive → False)",
    }

    for excel_col, description in transformations.items():
        print(f"  🔄 {excel_col:<25} → {description}")

    print("\n⚠️ COLONNES EXCEL NON UTILISÉES:")
    unused = ["Salaire", "Date de naissance"]
    for col in unused:
        print(f"  ❌ {col:<25} → (ignorée)")

    print("\n🆕 CHAMPS DB AVEC VALEURS PAR DÉFAUT:")
    defaults = {
        "grade": "'Junior'",
        "practice_id": "None (à assigner ultérieurement)",
        "date_premiere_mission": "None",
        "notes": "None",
        "date_creation": "datetime.now()",
        "derniere_maj": "datetime.now()",
    }

    for field, default_value in defaults.items():
        print(f"  🆕 {field:<25} → {default_value}")


def create_import_function():
    """Génère la fonction d'import basée sur le mapping"""

    print("\n📝 FONCTION D'IMPORT GÉNÉRÉE:")
    print("=" * 50)

    import_code = '''
def import_consultants_from_excel(excel_file_path='Data Quanteam 1 ligne.xlsx'):
    """
    Importe les consultants depuis le fichier Excel vers la base de données

    Args:
        excel_file_path: Chemin vers le fichier Excel

    Returns:
        dict: Résultats de l'import (succès, erreurs, statistiques)
    """

    results = {
        "total_lignes": 0,
        "importes": 0,
        "erreurs": [],
        "doublons": 0
    }

    try:
        # Lire le fichier Excel
        df = pd.read_excel(excel_file_path, sheet_name='Consultant')
        results["total_lignes"] = len(df)

        session = get_database_session()

        for index, row in df.iterrows():
            try:
                # Vérifier si le consultant existe déjà (par email)
                existing = session.query(Consultant).filter_by(email=row['email']).first()
                if existing:
                    results["doublons"] += 1
                    print(f"⚠️  Consultant {row['Prenom']} {row['Nom']} déjà existant (email: {row['email']})")
                    continue

                # Créer nouveau consultant
                consultant = Consultant(
                    # Correspondances directes
                    prenom=str(row['Prenom']).strip(),
                    nom=str(row['Nom']).strip(),
                    email=str(row['email']).strip(),
                    telephone=str(row['Num Telephonne']) if pd.notna(row['Num Telephonne']) else None,
                    societe=str(row['Société']).strip() if pd.notna(row['Société']) else 'Quanteam',

                    # Transformations
                    salaire_actuel=float(row['CJM']) if pd.notna(row['CJM']) else None,
                    type_contrat=str(row['contract_type_code']).strip() if pd.notna(row['contract_type_code']) else 'CDI',
                    disponibilite=str(row['UseActive']).strip().lower() == 'active' if pd.notna(row['UseActive']) else True,

                    # Dates avec gestion des erreurs
                    date_entree_societe=pd.to_datetime(row['Date Entree Société']).date() if pd.notna(row['Date Entree Société']) else None,
                    date_sortie_societe=pd.to_datetime(row['Date Sortie société']).date() if pd.notna(row['Date Sortie société']) else None,

                    # Valeurs par défaut
                    grade='Junior',
                    practice_id=None,  # À assigner manuellement plus tard
                    date_premiere_mission=None,
                    notes=f"Importé depuis Excel le {datetime.now().strftime('%d/%m/%Y')}"
                )

                session.add(consultant)
                results["importes"] += 1
                print(f"✅ {consultant.prenom} {consultant.nom} importé avec succès")

            except Exception as e:
                error_msg = f"Ligne {index + 2}: {str(e)}"
                results["erreurs"].append(error_msg)
                print(f"❌ Erreur ligne {index + 2}: {e}")

        # Sauvegarder en base
        session.commit()
        session.close()

        return results

    except Exception as e:
        results["erreurs"].append(f"Erreur globale: {str(e)}")
        return results


def show_import_summary(results):
    """Affiche un résumé de l'import"""
    print("\\n📊 RÉSUMÉ DE L'IMPORT")
    print("=" * 30)
    print(f"📋 Total lignes traitées: {results['total_lignes']}")
    print(f"✅ Consultants importés: {results['importes']}")
    print(f"⚠️  Doublons ignorés: {results['doublons']}")
    print(f"❌ Erreurs: {len(results['erreurs'])}")

    if results['erreurs']:
        print("\\n🔍 Détail des erreurs:")
        for error in results['erreurs']:
            print(f"  • {error}")


# UTILISATION:
# results = import_consultants_from_excel()
# show_import_summary(results)
'''

    print(import_code)

    return import_code


if __name__ == "__main__":
    # Analyser le fichier
    df = analyze_excel_file()

    if df is not None:
        # Proposer le mapping
        show_mapping_proposal()

        # Générer la fonction d'import
        create_import_function()

        print("\n🎯 PROCHAINES ÉTAPES:")
        print("1. Vérifier le mapping proposé")
        print("2. Adapter si nécessaire")
        print("3. Exécuter l'import avec: import_consultants_from_excel()")
        print("4. Assigner les practices manuellement après import")
