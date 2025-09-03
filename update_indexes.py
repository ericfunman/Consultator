"""
Script de mise à jour des index de base de données
Ajoute les nouveaux index de performance sans recréer la base
"""

import os
import sys
from sqlalchemy import create_engine, text

# Configuration
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app.database.database import DATABASE_URL

def add_performance_indexes():
    """Ajoute les nouveaux index de performance à la base existante"""

    engine = create_engine(DATABASE_URL, echo=True)

    with engine.connect() as conn:
        try:
            print("🔄 Ajout des index de performance...")

            # Index pour Consultant
            print("📊 Index Consultant...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_consultant_salaire
                ON consultants (salaire_actuel)
            """))

            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_consultant_recherche
                ON consultants (nom, prenom, email)
            """))

            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_consultant_dispo_practice
                ON consultants (disponibilite, practice_id)
            """))

            # Index pour Mission
            print("📊 Index Mission...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_mission_consultant_statut
                ON missions (consultant_id, statut)
            """))

            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_mission_client_consultant
                ON missions (client, consultant_id)
            """))

            # Index pour Competence
            print("📊 Index Competence...")
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_competence_nom
                ON competences (nom)
            """))

            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_competence_categorie
                ON competences (categorie)
            """))

            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_competence_type
                ON competences (type_competence)
            """))

            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_competence_nom_categorie
                ON competences (nom, categorie)
            """))

            conn.commit()
            print("✅ Tous les index ont été ajoutés avec succès !")

        except Exception as e:
            print(f"❌ Erreur lors de l'ajout des index: {e}")
            conn.rollback()

if __name__ == "__main__":
    add_performance_indexes()
