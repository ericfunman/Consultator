"""
Script d'import des consultants depuis Excel vers la base de données
Fichier: Data Quanteam 1 ligne.xlsx - Onglet: Consultant
"""

import os
import sys
from datetime import datetime

import pandas as pd

# Ajouter le chemin vers les modules
current_dir = os.path.dirname(__file__)
app_dir = os.path.join(current_dir, "app")
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from database.database import get_database_session
from database.models import Consultant
from database.models import Practice


def import_consultants_from_excel(
    excel_file_path="Data Quanteam 1 ligne.xlsx", dry_run=False
):
    """
    Importe les consultants depuis le fichier Excel vers la base de données

    Args:
        excel_file_path: Chemin vers le fichier Excel
        dry_run: Si True, affiche ce qui serait importé sans sauvegarder

    Returns:
        dict: Résultats de l'import (succès, erreurs, statistiques)
    """

    results = {
        "total_lignes": 0,
        "importes": 0,
        "erreurs": [],
        "doublons": 0,
        "consultants_crees": [],
    }

    print(f"🚀 IMPORT DES CONSULTANTS DEPUIS {excel_file_path}")
    print("=" * 60)
    print(f"Mode: {'🔍 SIMULATION (dry-run)' if dry_run else '💾 IMPORT RÉEL'}")
    print()

    try:
        # Lire le fichier Excel
        print("📖 Lecture du fichier Excel...")
        df = pd.read_excel(excel_file_path, sheet_name="Consultant")
        results["total_lignes"] = len(df)
        print(f"✅ {len(df)} ligne(s) trouvée(s)")
        print()

        # Afficher les colonnes détectées
        print("🔍 Colonnes détectées:")
        for col in df.columns:
            print(f"  • {col}")
        print()

        if not dry_run:
            session = get_database_session()

        for index, row in df.iterrows():
            try:
                print(f"📋 Traitement ligne {index + 2}: {row['Prenom']} {row['Nom']}")

                # Vérifier si le consultant existe déjà (par email)
                if not dry_run:
                    existing = (
                        session.query(Consultant).filter_by(email=row["email"]).first()
                    )
                    if existing:
                        results["doublons"] += 1
                        print(f"  ⚠️  Consultant déjà existant (email: {row['email']})")
                        continue

                # Préparer les données du consultant
                consultant_data = {
                    # Correspondances directes
                    "prenom": str(row["Prenom"]).strip(),
                    "nom": str(row["Nom"]).strip().upper(),  # Nom en majuscules
                    "email": str(row["email"]).strip().lower(),  # Email en minuscules
                    "telephone": (
                        str(row["Num Telephonne"]).strip()
                        if pd.notna(row["Num Telephonne"])
                        else None
                    ),
                    "societe": (
                        str(row["Société"]).strip()
                        if pd.notna(row["Société"])
                        else "Quanteam"
                    ),
                    # Transformations
                    "salaire_actuel": (
                        float(row["CJM"])
                        if pd.notna(row["CJM"]) and row["CJM"] != 0
                        else None
                    ),
                    "type_contrat": (
                        str(row["contract_type_code"]).strip()
                        if pd.notna(row["contract_type_code"])
                        else "CDI"
                    ),
                    "disponibilite": (
                        str(row["UseActive"]).strip().lower() == "active"
                        if pd.notna(row["UseActive"])
                        else True
                    ),
                    # Valeurs par défaut
                    "grade": "Junior",
                    "practice_id": None,  # À assigner manuellement plus tard
                    "date_premiere_mission": None,
                    "notes": f"Importé depuis Excel le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
                }

                # Gestion des dates avec validation
                try:
                    if pd.notna(row["Date Entree Société"]):
                        consultant_data["date_entree_societe"] = pd.to_datetime(
                            row["Date Entree Société"]
                        ).date()
                except:
                    consultant_data["date_entree_societe"] = None
                    print(f"  ⚠️  Date d'entrée invalide, ignorée")

                try:
                    if pd.notna(row["Date Sortie société"]):
                        consultant_data["date_sortie_societe"] = pd.to_datetime(
                            row["Date Sortie société"]
                        ).date()
                except:
                    consultant_data["date_sortie_societe"] = None

                # Afficher les données qui seront importées
                print(f"  📝 Données à importer:")
                for key, value in consultant_data.items():
                    if value is not None:
                        print(f"    • {key}: {value}")

                if dry_run:
                    # Mode simulation - juste afficher
                    results["importes"] += 1
                    results["consultants_crees"].append(
                        f"{consultant_data['prenom']} {consultant_data['nom']}"
                    )
                    print(f"  ✅ [SIMULATION] Consultant prêt pour import")
                else:
                    # Mode réel - créer en base
                    consultant = Consultant(**consultant_data)
                    session.add(consultant)
                    results["importes"] += 1
                    results["consultants_crees"].append(
                        f"{consultant.prenom} {consultant.nom}"
                    )
                    print(f"  ✅ Consultant créé en base")

                print()

            except Exception as e:
                error_msg = f"Ligne {index + 2} ({row.get('Prenom', '?')} {row.get('Nom', '?')}): {str(e)}"
                results["erreurs"].append(error_msg)
                print(f"  ❌ Erreur: {e}")
                print()

        # Sauvegarder en base (mode réel uniquement)
        if not dry_run and results["importes"] > 0:
            print("💾 Sauvegarde en base de données...")
            session.commit()
            session.close()
            print("✅ Sauvegarde terminée")
        elif not dry_run:
            session.close()

        return results

    except Exception as e:
        results["erreurs"].append(f"Erreur globale: {str(e)}")
        print(f"❌ Erreur globale: {e}")
        return results


def show_import_summary(results):
    """Affiche un résumé de l'import"""
    print("\n📊 RÉSUMÉ DE L'IMPORT")
    print("=" * 40)
    print(f"📋 Total lignes traitées: {results['total_lignes']}")
    print(f"✅ Consultants importés: {results['importes']}")
    print(f"⚠️  Doublons ignorés: {results['doublons']}")
    print(f"❌ Erreurs: {len(results['erreurs'])}")

    if results["consultants_crees"]:
        print(f"\n👥 Consultants traités:")
        for consultant in results["consultants_crees"]:
            print(f"  • {consultant}")

    if results["erreurs"]:
        print(f"\n🔍 Détail des erreurs:")
        for error in results["erreurs"]:
            print(f"  • {error}")

    print(f"\n🎯 Prochaines étapes après import:")
    print(f"  1. Assigner les practices aux consultants")
    print(f"  2. Vérifier/ajuster les grades si nécessaire")
    print(f"  3. Ajouter les compétences et langues")
    print(f"  4. Ajouter les missions historiques")


if __name__ == "__main__":
    # Faire d'abord une simulation
    print("🔍 SIMULATION D'IMPORT (dry-run)")
    print("=" * 40)
    results = import_consultants_from_excel(dry_run=True)
    show_import_summary(results)

    # Demander confirmation pour l'import réel
    if results["importes"] > 0 and len(results["erreurs"]) == 0:
        print(f"\n❓ Voulez-vous procéder à l'import réel ? (o/n)")
        # response = input().lower()
        # if response == 'o':
        #     print(f"\n💾 IMPORT RÉEL")
        #     print("=" * 20)
        #     real_results = import_consultants_from_excel(dry_run=False)
        #     show_import_summary(real_results)
    else:
        print(f"\n⚠️  Import non recommandé - Corrigez les erreurs d'abord")
