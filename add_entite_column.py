"""
Migration pour ajouter le champ entite à la table consultants
"""

from app.database.database import get_database_session
from sqlalchemy import text

def add_entite_column():
    """Ajoute la colonne entite à la table consultants"""

    with get_database_session() as session:
        try:
            # Vérifier si la colonne existe déjà
            result = session.execute(text("""
                PRAGMA table_info(consultants)
            """)).fetchall()

            column_names = [row[1] for row in result]  # row[1] contient le nom de la colonne

            if 'entite' not in column_names:
                # Ajouter la colonne entite
                session.execute(text("""
                    ALTER TABLE consultants
                    ADD COLUMN entite VARCHAR(100)
                """))
                session.commit()
                print("✅ Colonne 'entite' ajoutée à la table consultants")
            else:
                print("ℹ️ La colonne 'entite' existe déjà")

        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de la colonne: {e}")
            session.rollback()
            raise

if __name__ == "__main__":
    add_entite_column()