#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de mise a jour de la base de donnees pour la V1.2.1
Ajoute les champs grade et type_contrat pour les consultants
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from sqlalchemy import text

from app.database.database import get_database_session


def update_database_v121():
    """Met a jour la base de donnees pour la V1.2.1"""

    print("Mise a jour de la base de donnees pour V1.2.1...")

    try:
        with get_database_session() as session:
            # Ajouter les nouveaux champs a la table consultants
            updates = [
                "ALTER TABLE consultants ADD COLUMN grade VARCHAR(50) DEFAULT 'Junior';",
                "ALTER TABLE consultants ADD COLUMN type_contrat VARCHAR(20) DEFAULT 'CDI';",
            ]

            for update_sql in updates:
                try:
                    session.execute(text(update_sql))
                    print(f"Execute: {update_sql}")
                except Exception as e:
                    if (
                        "duplicate column name" in str(e).lower()
                        or "already exists" in str(e).lower()
                    ):
                        print(f"Colonne deja existante: {update_sql}")
                    else:
                        print(f"Erreur: {update_sql} - {e}")

            session.commit()
            print("Base de donnees mise a jour avec succes pour V1.2.1!")

            # Verifier les colonnes ajoutees
            result = session.execute(text("PRAGMA table_info(consultants);"))
            columns = [row[1] for row in result.fetchall()]

            new_columns = ["grade", "type_contrat"]
            for col in new_columns:
                if col in columns:
                    print(f"Colonne '{col}' presente")
                else:
                    print(f"Colonne '{col}' manquante")

    except Exception as e:
        print(f"Erreur lors de la mise a jour: {e}")
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("CONSULTATOR V1.2.1 - MISE A JOUR BASE DE DONNEES")
    print("=" * 60)

    success = update_database_v121()

    if success:
        print("\nMise a jour terminee avec succes!")
        print("Nouveaux champs ajoutes:")
        print(
            "   - grade (Junior, Confirme, Consultant Manager, Directeur de Practice)"
        )
        print("   - type_contrat (CDI, CDD, Stagiaire, Alternant, Independant)")
        print("\nCes champs sont maintenant disponibles dans l'interface consultant")
    else:
        print("\nEchec de la mise a jour!")
        sys.exit(1)
