"""
Script de migration pour ajouter les practices
"""

import os
import sys

# Ajouter le dossier app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from database.database import get_database_session
from database.database import init_database
from database.models import Practice


def migrate_add_practices():
    """Ajoute les practices par dÃ©faut Ã  la base de donnÃ©es"""

    print("ð Migration : Ajout des practices...")

    # Initialiser la base de donnÃ©es (crÃ©era la nouvelle table Practice)
    init_database()

    try:
        with get_database_session() as session:
            # VÃ©rifier si les practices existent dÃ©jÃ
            existing_practices = session.query(Practice).all()

            if not existing_practices:
                # CrÃ©er les practices par dÃ©faut
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
                print(f"â¹ï¸ {len(existing_practices)} practice(s) dÃ©jÃ  existante(s)")
                for p in existing_practices:
                    print(f"   - {p.nom}")

    except Exception as e:
        print(f"â Erreur lors de la migration : {e}")
        return False

    print("â Migration terminÃ©e avec succÃ¨s")
    return True


if __name__ == "__main__":
    migrate_add_practices()
