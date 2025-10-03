#!/usr/bin/env python3
"""
Script d'initialisation des dashboards
Crée les tables de dashboard et initialise les données par défaut
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import init_database, get_database_session
from app.database.models import DashboardConfiguration, DashboardWidgetInstance, WidgetCatalog
from app.services.widget_factory import WidgetCatalogManager
from app.pages_modules.dashboard_page import create_default_dashboards


def initialize_dashboard_system():
    """
    Initialise complètement le système de dashboard
    """
    print("🚀 Initialisation du système de dashboard...")
    print("=" * 50)

    try:
        # 1. Initialiser/mettre à jour la base de données
        print("1️⃣ Mise à jour de la base de données...")
        init_database()
        print("   ✅ Base de données mise à jour")

        # 2. Initialiser le catalogue de widgets
        print("\n2️⃣ Initialisation du catalogue de widgets...")
        WidgetCatalogManager.initialize_widget_catalog()
        print("   ✅ Catalogue de widgets initialisé")

        # 3. Créer les dashboards par défaut
        print("\n3️⃣ Création des dashboards par défaut...")
        create_default_dashboards()
        print("   ✅ Dashboards par défaut créés")

        # 4. Vérification finale
        print("\n4️⃣ Vérification du système...")
        with get_database_session() as session:
            # Compter les widgets disponibles
            widget_count = session.query(WidgetCatalog).filter(WidgetCatalog.is_active == True).count()
            print(f"   📊 {widget_count} widgets disponibles")

            # Compter les dashboards
            dashboard_count = session.query(DashboardConfiguration).count()
            print(f"   📋 {dashboard_count} dashboards configurés")

            # Compter les instances de widgets
            widget_instance_count = session.query(DashboardWidgetInstance).count()
            print(f"   🧩 {widget_instance_count} widgets installés")

        print("\n🎉 Système de dashboard initialisé avec succès !")
        print("🚀 Vous pouvez maintenant utiliser l'onglet Dashboard dans Business Managers")

    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()


def show_dashboard_info():
    """
    Affiche les informations sur le système de dashboard
    """
    print("\n📊 SYSTÈME DE DASHBOARD - INFORMATIONS")
    print("=" * 50)

    try:
        with get_database_session() as session:
            # Widgets disponibles
            widgets = session.query(WidgetCatalog).filter(WidgetCatalog.is_active == True).all()
            
            print(f"\n🧩 WIDGETS DISPONIBLES ({len(widgets)}):")
            for widget in widgets:
                print(f"   {widget.icon} {widget.display_name} ({widget.category})")
                print(f"      {widget.description}")

            # Dashboards configurés
            dashboards = session.query(DashboardConfiguration).all()
            
            print(f"\n📋 DASHBOARDS CONFIGURÉS ({len(dashboards)}):")
            for dashboard in dashboards:
                widget_count = len(dashboard.widget_instances)
                template_str = " [TEMPLATE]" if dashboard.is_template else ""
                print(f"   📊 {dashboard.nom}{template_str}")
                print(f"      👥 Accès: {dashboard.role_access} | 🧩 {widget_count} widgets")
                if dashboard.description:
                    print(f"      📝 {dashboard.description}")

    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--info":
        show_dashboard_info()
    else:
        initialize_dashboard_system()
        show_dashboard_info()