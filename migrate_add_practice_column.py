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
    """Ajoute la colonne practice_id Ã  la table consultants et crÃ©e les practices par dÃ©faut"""

    print("ð Migration : Ajout de la colonne practice_id...")

    # Connecter directement Ã  SQLite pour la migration
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # VÃ©rifier si la colonne practice_id existe dÃ©jÃ
        cursor.execute("PRAGMA table_info(consultants)")
        columns = [column[1] for column in cursor.fetchall()]

        if "practice_id" not in columns:
            print("â Ajout de la colonne practice_id Ã  la table consultants...")
            cursor.execute("ALTER TABLE consultants ADD COLUMN practice_id INTEGER")
            conn.commit()
            print("â Colonne practice_id ajoutÃ©e")
        else:
            print("â¹ï¸ La colonne practice_id existe dÃ©jÃ ")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"â Erreur lors de l'ajout de la colonne : {e}")
        return False

    # Initialiser la base de donnÃ©es pour crÃ©er la table practices si elle n'existe pas
    print("ð Initialisation de la base de donnÃ©es...")
    init_database()

    # CrÃ©er les practices par dÃ©faut
    try:
        with get_database_session() as session:
            # VÃ©rifier si les practices existent dÃ©jÃ
            existing_practices = session.query(Practice).all()

            if not existing_practices:
                print("â CrÃ©ation des practices par dÃ©faut...")

                practices_default = [
                    Practice(
                        nom="Data",
                        description="Practice spÃ©cialisÃ©e dans les donnÃ©es, analytics, BI et data science",
                        responsable="",
                        actif=True,
                    ),
                    Practice(
                        nom="Quant",
                        description="Practice spÃ©cialisÃ©e dans l'analyse quantitative et le risk management",
                        responsable="",
                        actif=True,
                    ),
                ]

                for practice in practices_default:
                    session.add(practice)

                session.commit()
                print("â Practices par dÃ©faut crÃ©Ã©es : Data et Quant")
            else:
                print(
                    f"â¹ï¸ {len(existing_practices)} practice(s) dÃ©jÃ  existante(s) :"
                )
                for p in existing_practices:
                    print(f"   - {p.nom}")

    except Exception as e:
        print(f"â Erreur lors de la crÃ©ation des practices : {e}")
        return False

    print("â Migration terminÃ©e avec succÃ¨s")
    return True


def check_migration_needed():
    """VÃ©rifie si la migration est nÃ©cessaire"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # VÃ©rifier si la colonne practice_id existe
        cursor.execute("PRAGMA table_info(consultants)")
        columns = [column[1] for column in cursor.fetchall()]

        cursor.close()
        conn.close()

        return "practice_id" not in columns

    except Exception as e:
        print(f"Erreur lors de la vÃ©rification : {e}")
        return True  # En cas d'erreur, on assume qu'il faut migrer


if __name__ == "__main__":
    if check_migration_needed():
        print("ð Migration nÃ©cessaire dÃ©tectÃ©e")
        migrate_add_practice_column()
    else:
        print("â Aucune migration nÃ©cessaire - La base est Ã  jour")
