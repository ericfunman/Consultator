"""
Script de migration pour ajouter les practices
"""

import sys
import os

# Ajouter le dossier app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database.database import init_database, get_database_session
from database.models import Practice

def migrate_add_practices():
    """Ajoute les practices par défaut à la base de données"""
    
    print("🔄 Migration : Ajout des practices...")
    
    # Initialiser la base de données (créera la nouvelle table Practice)
    init_database()
    
    try:
        with get_database_session() as session:
            # Vérifier si les practices existent déjà
            existing_practices = session.query(Practice).all()
            
            if not existing_practices:
                # Créer les practices par défaut
                practices_default = [
                    Practice(
                        nom="Data",
                        description="Practice spécialisée dans les données, analytics, BI et data science",
                        responsable="",
                        actif=True
                    ),
                    Practice(
                        nom="Quant",
                        description="Practice spécialisée dans l'analyse quantitative et le risk management", 
                        responsable="",
                        actif=True
                    )
                ]
                
                for practice in practices_default:
                    session.add(practice)
                
                session.commit()
                print("✅ Practices par défaut créées : Data et Quant")
            else:
                print(f"ℹ️ {len(existing_practices)} practice(s) déjà existante(s)")
                for p in existing_practices:
                    print(f"   - {p.nom}")
    
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        return False
    
    print("✅ Migration terminée avec succès")
    return True

if __name__ == "__main__":
    migrate_add_practices()
