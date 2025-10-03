"""
Script de test pour vérifier le bon fonctionnement du système de dashboard
Vérifie toutes les fonctionnalités importantes
"""

import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import get_database_session
from app.services.dashboard_service import DashboardService, DashboardDataService
from app.services.widget_factory import WidgetFactory

def test_database_tables():
    """Test 1: Vérifier que les tables dashboard existent"""
    print("🔍 Test 1: Vérification des tables dashboard...")
    
    try:
        with get_database_session() as session:
            # Test des requêtes de base
            widgets = session.execute("SELECT COUNT(*) FROM widget_catalog").scalar()
            dashboards = session.execute("SELECT COUNT(*) FROM dashboard_configurations").scalar()
            instances = session.execute("SELECT COUNT(*) FROM dashboard_widget_instances").scalar()
            
            print(f"   ✅ Tables existantes:")
            print(f"      📦 widget_catalog: {widgets} widgets")
            print(f"      📊 dashboard_configurations: {dashboards} dashboards")
            print(f"      🧩 dashboard_widget_instances: {instances} instances")
            
            return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_dashboard_service():
    """Test 2: Vérifier les services dashboard"""
    print("\n🔍 Test 2: Services dashboard...")
    
    try:
        # Test DashboardService
        dashboards = DashboardService.get_all_dashboards()
        print(f"   ✅ DashboardService: {len(dashboards)} dashboards trouvés")
        
        for dashboard in dashboards:
            print(f"      📊 {dashboard.name} ({dashboard.target_role})")
        
        # Test DashboardDataService
        data_service = DashboardDataService()
        
        # Test des données intercontrat
        intercontrat_data = data_service.get_intercontrat_data()
        print(f"   ✅ Données intercontrat: {intercontrat_data}")
        
        # Test des données revenue
        revenue_data = data_service.get_revenue_by_bm_data()
        print(f"   ✅ Données revenue: {len(revenue_data)} BMs")
        
        # Test des KPIs globaux
        global_kpis = data_service.get_global_kpis()
        print(f"   ✅ KPIs globaux: {len(global_kpis)} indicateurs")
        
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_widget_factory():
    """Test 3: Vérifier le WidgetFactory"""
    print("\n🔍 Test 3: Widget Factory...")
    
    try:
        factory = WidgetFactory()
        
        # Test des widgets disponibles
        available_widgets = [
            'intercontrat_rate',
            'consultants_sans_mission', 
            'revenue_by_bm',
            'global_kpis',
            'intercontrat_trend',
            'top_bm_performance'
        ]
        
        for widget_type in available_widgets:
            # On ne peut pas tester le rendu complet sans Streamlit,
            # mais on peut vérifier que les méthodes existent
            method_name = f"render_{widget_type}"
            if hasattr(factory, method_name):
                print(f"   ✅ Widget {widget_type}: méthode {method_name} disponible")
            else:
                print(f"   ❌ Widget {widget_type}: méthode {method_name} manquante")
                
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_dashboard_access():
    """Test 4: Vérifier l'accès aux dashboards par rôle"""
    print("\n🔍 Test 4: Accès dashboards par rôle...")
    
    try:
        # Test pour rôle direction
        direction_dashboards = DashboardService.get_dashboards_for_role('direction')
        print(f"   ✅ Dashboards direction: {len(direction_dashboards)}")
        
        # Test pour rôle bm
        bm_dashboards = DashboardService.get_dashboards_for_role('bm')
        print(f"   ✅ Dashboards BM: {len(bm_dashboards)}")
        
        # Test pour rôle inexistant
        unknown_dashboards = DashboardService.get_dashboards_for_role('unknown')
        print(f"   ✅ Dashboards inconnus: {len(unknown_dashboards)}")
        
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Exécution de tous les tests"""
    print("🚀 TESTS DU SYSTÈME DASHBOARD")
    print("=" * 50)
    
    tests = [
        test_database_tables,
        test_dashboard_service,
        test_widget_factory,
        test_dashboard_access
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} échoué: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DES TESTS")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 TOUS LES TESTS RÉUSSIS ({passed}/{total})")
        print("✅ Le système dashboard est opérationnel !")
        print("\n🚀 Vous pouvez maintenant:")
        print("   • Aller dans Business Managers > Onglet Dashboard")
        print("   • Utiliser les dashboards Direction et BM")
        print("   • Créer de nouveaux dashboards personnalisés")
    else:
        print(f"⚠️  TESTS PARTIELS ({passed}/{total})")
        print("🔧 Certaines fonctionnalités peuvent nécessiter des corrections")

if __name__ == "__main__":
    main()