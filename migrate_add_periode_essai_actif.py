"""
Script de migration pour ajouter les nouveaux champs période d'essai et statut actif
Version 1.2.3 - Septembre 2025
"""

import sqlite3
import sys
from pathlib import Path

# Chemin vers la base de données
DB_PATH = "test_consultator.db"


def migrate_add_periode_essai_and_actif():
    """Ajoute les nouvelles colonnes à la table consultants"""

    print("🔄 Migration base de données v1.2.3")
    print("➕ Ajout des champs période d'essai et statut actif")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Vérifier si les colonnes existent déjà
        cursor.execute("PRAGMA table_info(consultants)")
        columns = [column[1] for column in cursor.fetchall()]

        # Ajouter etat_periode_essai si elle n'existe pas
        if "etat_periode_essai" not in columns:
            cursor.execute(
                """
                ALTER TABLE consultants 
                ADD COLUMN etat_periode_essai VARCHAR(50)
            """
            )
            print("✅ Colonne 'etat_periode_essai' ajoutée")
        else:
            print("⚠️ Colonne 'etat_periode_essai' existe déjà")

        # Ajouter fin_periode_essai si elle n'existe pas
        if "fin_periode_essai" not in columns:
            cursor.execute(
                """
                ALTER TABLE consultants 
                ADD COLUMN fin_periode_essai DATE
            """
            )
            print("✅ Colonne 'fin_periode_essai' ajoutée")
        else:
            print("⚠️ Colonne 'fin_periode_essai' existe déjà")

        # Ajouter actif si elle n'existe pas
        if "actif" not in columns:
            cursor.execute(
                """
                ALTER TABLE consultants 
                ADD COLUMN actif BOOLEAN DEFAULT 1
            """
            )
            print("✅ Colonne 'actif' ajoutée")

            # Mettre tous les consultants existants comme actifs par défaut
            cursor.execute(
                """
                UPDATE consultants 
                SET actif = 1 
                WHERE actif IS NULL
            """
            )
            print("✅ Consultants existants mis à jour (actif=True par défaut)")
        else:
            print("⚠️ Colonne 'actif' existe déjà")

        conn.commit()
        conn.close()

        print("🎉 Migration v1.2.3 terminée avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        if "conn" in locals():
            conn.rollback()
            conn.close()


if __name__ == "__main__":
    migrate_add_periode_essai_and_actif()
