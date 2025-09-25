"""
Script de création de la table VSA_Mission
Ajoute la table vsa_missions à la base de données existante
"""

import os
import sys
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Float, Text, DateTime, Index
from sqlalchemy.sql import text

# Ajouter les chemins nécessaires
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.database.database import DATABASE_URL

def create_vsa_missions_table():
    """Crée la table vsa_missions dans la base de données"""

    # Obtenir l'URL de la base de données
    database_url = DATABASE_URL

    # Créer le moteur SQLAlchemy
    engine = create_engine(database_url)

    try:
        with engine.connect() as conn:
            # Vérifier si la table existe déjà
            result = conn.execute(text("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='vsa_missions'
            """))

            if result.fetchone():
                print("✅ La table vsa_missions existe déjà")
                return

            # Créer la table
            create_table_sql = """
            CREATE TABLE vsa_missions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                code VARCHAR(100) NOT NULL,
                orderid VARCHAR(100) NOT NULL,
                client_name VARCHAR(200) NOT NULL,
                date_debut DATE,
                date_fin DATE,
                tjm FLOAT,
                cjm FLOAT,
                description TEXT,
                statut VARCHAR(50) DEFAULT 'active',
                date_import DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """

            conn.execute(text(create_table_sql))

            # Créer les index
            index_sqls = [
                "CREATE INDEX idx_vsa_mission_user_id ON vsa_missions(user_id)",
                "CREATE INDEX idx_vsa_mission_code ON vsa_missions(code)",
                "CREATE INDEX idx_vsa_mission_orderid ON vsa_missions(orderid)",
                "CREATE INDEX idx_vsa_mission_client ON vsa_missions(client_name)",
                "CREATE INDEX idx_vsa_mission_dates ON vsa_missions(date_debut, date_fin)",
            ]

            for index_sql in index_sqls:
                conn.execute(text(index_sql))

            # Commit des changements
            conn.commit()

            print("✅ Table vsa_missions créée avec succès")
            print("✅ Index créés avec succès")

    except Exception as e:
        print(f"❌ Erreur lors de la création de la table: {e}")
        raise

if __name__ == "__main__":
    create_vsa_missions_table()