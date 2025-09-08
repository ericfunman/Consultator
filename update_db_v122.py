#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise à jour de la base de données pour la V1.2.2
Ajoute le champ TJM aux missions et améliore la gestion de disponibilité
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from sqlalchemy import text

from app.database.database import get_database_session


def update_database_v122():
    """Met à jour la base de données pour la V1.2.2"""

    print("🔄 Mise à jour de la base de données pour V1.2.2...")

    try:
        with get_database_session() as session:
            # Ajouter le champ TJM aux missions
            updates = [
                "ALTER TABLE missions ADD COLUMN tjm DECIMAL(10,2);",
                # Ajouter un commentaire pour clarifier le champ
                "COMMENT ON COLUMN missions.tjm IS 'Taux Journalier Moyen de la mission en euros';",
            ]

            for update_sql in updates:
                try:
                    session.execute(text(update_sql))
                    print(f"✅ Exécuté: {update_sql}")
                except Exception as e:
                    if (
                        "duplicate column name" in str(e).lower()
                        or "already exists" in str(e).lower()
                    ):
                        print(f"⚠️  Colonne déjà existante: {update_sql}")
                    elif "comment" in str(e).lower():
                        print(f"⚠️  Commentaire non supporté (SQLite): {update_sql}")
                    else:
                        print(f"❌ Erreur: {update_sql} - {e}")

            # Migrer les données existantes si le champ taux_journalier existe
            try:
                session.execute(
                    text(
                        "UPDATE missions SET tjm = taux_journalier WHERE taux_journalier IS NOT NULL AND tjm IS NULL;"
                    )
                )
                print("✅ Migration des données TJM existantes effectuée")
            except Exception as e:
                print(f"⚠️  Pas de migration des données TJM nécessaire: {e}")

            session.commit()
            print("✅ Base de données mise à jour avec succès pour V1.2.2!")

            # Vérifier les colonnes ajoutées
            result = session.execute(text("PRAGMA table_info(missions);"))
            columns = [row[1] for row in result.fetchall()]

            new_columns = ["tjm"]
            for col in new_columns:
                if col in columns:
                    print(f"✅ Colonne '{col}' présente dans la table missions")
                else:
                    print(f"❌ Colonne '{col}' manquante dans la table missions")

    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 CONSULTATOR V1.2.2 - MISE À JOUR BASE DE DONNÉES")
    print("=" * 60)

    success = update_database_v122()

    if success:
        print("\n🎉 Mise à jour terminée avec succès!")
        print("📋 Nouveaux champs ajoutés:")
        print("   - missions.tjm (Taux Journalier Moyen mission)")
        print("\n💡 Nouvelles propriétés calculées disponibles:")
        print("   - consultant.date_disponibilite (calculée automatiquement)")
        print("   - mission.tjm (taux journalier de la mission)")
        print("\n🎯 Ces améliorations permettent:")
        print("   - Meilleur suivi des TJM par mission")
        print("   - Calcul automatique de la date de disponibilité")
        print("   - Gestion intelligente ASAP vs dates futures")
    else:
        print("\n❌ Échec de la mise à jour!")
        sys.exit(1)
