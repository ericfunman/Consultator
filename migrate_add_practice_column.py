"""
Script de migration pour ajouter la colonne practice_id aux consultants
"""

import os
import sqlite3
import sys

# Ajouter le dossier app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from database.database import DATABASE_PATH
from database.database import get_database_session
from database.database import init_database
from database.models import Practice


def migrate_add_practice_column():
    """Ajoute la colonne practice_id à la table consultants et crée les practices par défaut"""

    print("🔄 Migration : Ajout de la colonne practice_id...")

    # Connecter directement à SQLite pour la migration
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Vérifier si la colonne practice_id existe déjà
        cursor.execute("PRAGMA table_info(consultants)")
        columns = [column[1] for column in cursor.fetchall()]

        if "practice_id" not in columns:
            print("➕ Ajout de la colonne practice_id à la table consultants...")
            cursor.execute("ALTER TABLE consultants ADD COLUMN practice_id INTEGER")
            conn.commit()
            print("✅ Colonne practice_id ajoutée")
        else:
            print("ℹ️ La colonne practice_id existe déjà")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de la colonne : {e}")
        return False

    # Initialiser la base de données pour créer la table practices si elle n'existe pas
    print("🔄 Initialisation de la base de données...")
    init_database()

    # Créer les practices par défaut
    try:
        with get_database_session() as session:
            # Vérifier si les practices existent déjà
            existing_practices = session.query(Practice).all()

            if not existing_practices:
                print("➕ Création des practices par défaut...")

                practices_default = [
                    Practice(
                        nom="Data",
                        description="Practice spécialisée dans les données, analytics, BI et data science",
                        responsable="",
                        actif=True,
                    ),
                    Practice(
                        nom="Quant",
                        description="Practice spécialisée dans l'analyse quantitative et le risk management",
                        responsable="",
                        actif=True,
                    ),
                ]

                for practice in practices_default:
                    session.add(practice)

                session.commit()
                print("✅ Practices par défaut créées : Data et Quant")
            else:
                print(f"ℹ️ {len(existing_practices)} practice(s) déjà existante(s) :")
                for p in existing_practices:
                    print(f"   - {p.nom}")

    except Exception as e:
        print(f"❌ Erreur lors de la création des practices : {e}")
        return False

    print("✅ Migration terminée avec succès")
    return True


def check_migration_needed():
    """Vérifie si la migration est nécessaire"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Vérifier si la colonne practice_id existe
        cursor.execute("PRAGMA table_info(consultants)")
        columns = [column[1] for column in cursor.fetchall()]

        cursor.close()
        conn.close()

        return "practice_id" not in columns

    except Exception as e:
        print(f"Erreur lors de la vérification : {e}")
        return True  # En cas d'erreur, on assume qu'il faut migrer


if __name__ == "__main__":
    if check_migration_needed():
        print("🚀 Migration nécessaire détectée")
        migrate_add_practice_column()
    else:
        print("✅ Aucune migration nécessaire - La base est à jour")
