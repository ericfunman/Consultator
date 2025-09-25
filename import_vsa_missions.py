"""
Script d'import des missions VSA depuis Excel
Importe les missions depuis l'onglet Mission du fichier Excel VSA
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import argparse

import pandas as pd

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.database.database import get_database_session
from app.database.models import Consultant, VSA_Mission

# Configuration
EXCEL_FILE = "Data Quanteam 1 ligne.xlsx"  # À modifier selon le fichier réel
SHEET_NAME = "Mission"  # Nom de l'onglet contenant les missions

# Mapping des colonnes Excel vers les champs du modèle
COLUMN_MAPPING = {
    'user_id': 'user_id',  # ID du consultant
    'Code': 'code',  # Clé unique de la mission
    'Orderid': 'orderid',  # Numéro de commande
    'name': 'client_name',  # Nom du client
    'date_debut': 'date_debut',  # Date de début
    'date_fin': 'date_fin',  # Date de fin
    'TJM': 'tjm',  # Taux Journalier Moyen
    'CJM': 'cjm',  # Coût Journalier Moyen
    'description': 'description',  # Description optionnelle
}

# Constantes pour les messages
MSG_FICHIER_NON_TROUVE = "❌ Fichier Excel non trouvé: {}"
MSG_ONGLET_NON_TROUVE = "❌ Onglet '{}' non trouvé dans le fichier Excel"
MSG_AUCUNE_MISSION = "ℹ️ Aucune mission trouvée dans le fichier"
MSG_MISSION_IMPORTEE = "✅ Mission importée: {} (Consultant: {}, Client: {})"
MSG_ERREUR_IMPORT = "❌ Erreur lors de l'import de la mission {}: {}"
MSG_CONSULTANT_NON_TROUVE = "⚠️ Consultant avec user_id {} non trouvé, mission ignorée: {}"
MSG_MISSION_DUPLIQUEE = "⚠️ Mission avec code {} déjà existante, ignorée"
MSG_IMPORT_TERMINE = "🎉 Import terminé: {} missions importées, {} erreurs, {} ignorées"
MSG_DEBUT_IMPORT = "🚀 Début de l'import des missions VSA depuis {}"


def parse_date(date_value) -> Optional[datetime.date]:
    """Parse une date depuis différentes formats Excel"""
    if pd.isna(date_value):
        return None

    try:
        if isinstance(date_value, str):
            # Essayer différents formats de date
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                try:
                    return datetime.strptime(date_value, fmt).date()
                except ValueError:
                    continue
        elif isinstance(date_value, datetime):
            return date_value.date()
        elif isinstance(date_value, pd.Timestamp):
            return date_value.date()
    except Exception:
        pass

    return None


def validate_mission_data(row: pd.Series) -> Dict:
    """Valide et nettoie les données d'une mission"""
    mission_data = {}

    try:
        # Champs obligatoires
        mission_data['user_id'] = int(row.get('user_id', 0))
        mission_data['code'] = str(row.get('Code', '')).strip()
        mission_data['orderid'] = str(row.get('Orderid', '')).strip()
        mission_data['client_name'] = str(row.get('name', '')).strip()

        # Validation des champs obligatoires
        if not mission_data['user_id'] or mission_data['user_id'] <= 0:
            raise ValueError("user_id invalide")
        if not mission_data['code']:
            raise ValueError("Code de mission manquant")
        if not mission_data['orderid']:
            raise ValueError("Numéro de commande manquant")
        if not mission_data['client_name']:
            raise ValueError("Nom du client manquant")

        # Champs optionnels
        mission_data['date_debut'] = parse_date(row.get('date_debut'))
        mission_data['date_fin'] = parse_date(row.get('date_fin'))

        # Champs numériques
        try:
            mission_data['tjm'] = float(row.get('TJM', 0)) if pd.notna(row.get('TJM')) else None
        except (ValueError, TypeError):
            mission_data['tjm'] = None

        try:
            mission_data['cjm'] = float(row.get('CJM', 0)) if pd.notna(row.get('CJM')) else None
        except (ValueError, TypeError):
            mission_data['cjm'] = None

        # Description
        description = str(row.get('description', '')).strip()
        mission_data['description'] = description if description else None

        # Statut par défaut
        mission_data['statut'] = 'active'

    except Exception as e:
        raise ValueError(f"Erreur de validation: {e}")

    return mission_data


def import_vsa_missions(excel_file: str = EXCEL_FILE, sheet_name: str = SHEET_NAME) -> Dict[str, int]:
    """
    Importe les missions VSA depuis un fichier Excel

    Args:
        excel_file: Chemin vers le fichier Excel
        sheet_name: Nom de l'onglet contenant les missions

    Returns:
        Dict avec les statistiques d'import
    """
    stats = {'imported': 0, 'errors': 0, 'skipped': 0}

    print(MSG_DEBUT_IMPORT.format(excel_file))

    # Vérifier que le fichier existe
    if not os.path.exists(excel_file):
        print(MSG_FICHIER_NON_TROUVE.format(excel_file))
        return stats

    try:
        # Charger le fichier Excel
        xl = pd.ExcelFile(excel_file)

        # Vérifier que l'onglet existe
        if sheet_name not in xl.sheet_names:
            print(MSG_ONGLET_NON_TROUVE.format(sheet_name))
            print(f"Onglets disponibles: {xl.sheet_names}")
            return stats

        # Charger les données
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"📊 {len(df)} lignes trouvées dans l'onglet {sheet_name}")

        if df.empty:
            print(MSG_AUCUNE_MISSION)
            return stats

        # Traiter chaque ligne
        with get_database_session() as session:
            for index, row in df.iterrows():
                try:
                    # Valider les données
                    mission_data = validate_mission_data(row)

                    # Vérifier si le consultant existe
                    consultant = session.query(Consultant).filter(
                        Consultant.id == mission_data['user_id']
                    ).first()

                    if not consultant:
                        print(MSG_CONSULTANT_NON_TROUVE.format(
                            mission_data['user_id'], mission_data['code']
                        ))
                        stats['skipped'] += 1
                        continue

                    # Vérifier si la mission existe déjà
                    existing_mission = session.query(VSA_Mission).filter(
                        VSA_Mission.code == mission_data['code']
                    ).first()

                    if existing_mission:
                        print(MSG_MISSION_DUPLIQUEE.format(mission_data['code']))
                        stats['skipped'] += 1
                        continue

                    # Créer la mission VSA
                    vsa_mission = VSA_Mission(**mission_data)
                    session.add(vsa_mission)

                    print(MSG_MISSION_IMPORTEE.format(
                        mission_data['code'],
                        f"{consultant.prenom} {consultant.nom}",
                        mission_data['client_name']
                    ))
                    stats['imported'] += 1

                except Exception as e:
                    print(MSG_ERREUR_IMPORT.format(index + 2, str(e)))
                    stats['errors'] += 1
                    continue

            # Commit des changements
            session.commit()

    except Exception as e:
        print(f"❌ Erreur générale lors de l'import: {e}")
        stats['errors'] += 1

    print(MSG_IMPORT_TERMINE.format(stats['imported'], stats['errors'], stats['skipped']))
    return stats


def show_import_summary(stats: Dict[str, int]) -> None:
    """Affiche un résumé de l'import"""
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DE L'IMPORT DES MISSIONS VSA")
    print("="*50)
    print(f"✅ Missions importées: {stats['imported']}")
    print(f"❌ Erreurs: {stats['errors']}")
    print(f"⚠️ Ignorées: {stats['skipped']}")
    print(f"📈 Taux de succès: {(stats['imported'] / max(stats['imported'] + stats['errors'] + stats['skipped'], 1) * 100):.1f}%")


if __name__ == "__main__":
    # Parser les arguments de ligne de commande
    parser = argparse.ArgumentParser(description='Import des missions VSA depuis Excel')
    parser.add_argument('--file', '-f', default=EXCEL_FILE,
                       help=f'Fichier Excel à importer (défaut: {EXCEL_FILE})')
    parser.add_argument('--sheet', '-s', default=SHEET_NAME,
                       help=f'Onglet Excel contenant les missions (défaut: {SHEET_NAME})')

    args = parser.parse_args()

    # Exécuter l'import
    stats = import_vsa_missions(excel_file=args.file, sheet_name=args.sheet)
    show_import_summary(stats)