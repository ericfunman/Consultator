#!/usr/bin/env python3
"""
Script de vérification de l'initialisation de la base de données pour CI/CD
Teste que toutes les tables sont créées correctement
"""

import os
import sys

# Ajouter le répertoire app au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))


def verify_database_setup():
    """Vérifie que la base de données peut être initialisée correctement"""
    try:
        print("🔍 Vérification de l'initialisation de la base de données...")

        # Import des modèles
        from sqlalchemy import inspect

        from app.database.database import get_database_engine
        from app.database.database import init_database
        from app.database.models import CV
        from app.database.models import Base
        from app.database.models import Competence
        from app.database.models import Consultant
        from app.database.models import ConsultantCompetence
        from app.database.models import Mission
        from app.database.models import Practice

        print(f"✅ Modèles importés: {len(Base.metadata.tables)} tables")

        # Lister les tables définies
        table_names = list(Base.metadata.tables.keys())
        print(f"📋 Tables définies: {', '.join(table_names)}")

        # Force l'initialisation
        init_database()

        # Vérifier que les tables existent dans la base
        engine = get_database_engine()
        inspector = inspect(engine)
        actual_tables = inspector.get_table_names()

        print(f"🗄️ Tables créées: {', '.join(actual_tables)}")

        # Vérifications
        missing_tables = set(table_names) - set(actual_tables)
        if missing_tables:
            print(f"❌ Tables manquantes: {', '.join(missing_tables)}")
            return False

        print("✅ Toutes les tables sont correctement créées")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_database_setup()
    sys.exit(0 if success else 1)
