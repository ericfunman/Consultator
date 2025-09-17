#!/usr/bin/env python3
"""
Script de mise à jour de la base de données pour la V1.2
Ajoute les nouveaux champs pour l'historique société des consultants
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from sqlalchemy import text

from app.database.database import get_database_session


def update_database_v12():
    """Met à jour la base de données pour la V1.2"""

    print("🔄 Mise à jour de la base de données pour V1.2...")

    try:
        with get_database_session() as session:
            # Ajouter les nouveaux champs à la table consultants
            updates = [
                "ALTER TABLE consultants ADD COLUMN date_entree_societe DATE;",
                "ALTER TABLE consultants ADD COLUMN date_sortie_societe DATE;",
                "ALTER TABLE consultants ADD COLUMN societe VARCHAR(50) DEFAULT 'Quanteam';",
                "ALTER TABLE consultants ADD COLUMN date_premiere_mission DATE;",
            ]

            for update_sql in updates:
                try:
                    session.execute(text(update_sql))
                    print(f"✅ Exécuté: {update_sql}")
                except Exception as exc:
                    if (
                        "duplicate column name" in str(exc).lower()
                        or "already exists" in str(exc).lower()
                    ):
                        print(f"⚠️  Colonne déjà existante: {update_sql}")
                    else:
                        print(f"❌ Erreur: {update_sql} - {exc}")

            session.commit()
            print("✅ Base de données mise à jour avec succès pour V1.2!")

            # Vérifier les colonnes ajoutées
            result = session.execute(text("PRAGMA table_info(consultants);"))
            columns = [row[1] for row in result.fetchall()]

            new_columns = [
                "date_entree_societe",
                "date_sortie_societe",
                "societe",
                "date_premiere_mission",
            ]
            for col in new_columns:
                if col in columns:
                    print(f"✅ Colonne '{col}' présente")
                else:
                    print(f"❌ Colonne '{col}' manquante")

    except Exception as exc:
        print(f"❌ Erreur lors de la mise à jour: {exc}")
        return False

    return True


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 CONSULTATOR V1.2 - MISE À JOUR BASE DE DONNÉES")
    print("=" * 50)

    success = update_database_v12()

    if success:
        print("\n🎉 Mise à jour terminée avec succès!")
        print("📋 Nouveaux champs ajoutés:")
        print("   - date_entree_societe (Date d'entrée)")
        print("   - date_sortie_societe (Date de sortie)")
        print("   - societe (Quanteam/Asigma)")
        print("   - date_premiere_mission (Première mission)")
        print("\n💡 Propriétés calculées disponibles:")
        print("   - experience_annees (calculée automatiquement)")
        print("   - statut_societe (En poste/Parti/Départ prévu)")
    else:
        print("\n❌ Échec de la mise à jour!")
        sys.exit(1)
