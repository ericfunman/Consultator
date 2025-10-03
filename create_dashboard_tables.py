#!/usr/bin/env python3
"""
Script de création forcée des tables dashboard
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import get_database_session, get_database_engine
from app.database.models import Base, DashboardConfiguration, DashboardWidgetInstance, WidgetCatalog


def create_dashboard_tables():
    """
    Crée explicitement les tables dashboard
    """
    print("🔨 Création des tables dashboard...")
    
    try:
        # Créer toutes les tables définies dans Base
        engine = get_database_engine()
        Base.metadata.create_all(engine)
        print("✅ Toutes les tables créées avec succès")
        
        # Vérifier que les tables existent
        with get_database_session() as session:
            # Test de chaque table
            try:
                session.query(WidgetCatalog).count()
                print("✅ Table widget_catalog créée")
            except Exception as e:
                print(f"❌ Erreur table widget_catalog: {e}")
            
            try:
                session.query(DashboardConfiguration).count()
                print("✅ Table dashboard_configurations créée")
            except Exception as e:
                print(f"❌ Erreur table dashboard_configurations: {e}")
            
            try:
                session.query(DashboardWidgetInstance).count()
                print("✅ Table dashboard_widget_instances créée")
            except Exception as e:
                print(f"❌ Erreur table dashboard_widget_instances: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Création des tables dashboard")
    print("=" * 40)
    
    success = create_dashboard_tables()
    
    if success:
        print("\n🎉 Tables dashboard créées avec succès !")
        print("Vous pouvez maintenant exécuter: python init_dashboard_system.py")
    else:
        print("\n❌ Échec de la création des tables")