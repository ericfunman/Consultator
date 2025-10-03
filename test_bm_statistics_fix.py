#!/usr/bin/env python3
"""
Script de test pour vérifier la correction des statistiques Business Managers
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import get_database_session
from app.database.models import BusinessManager, ConsultantBusinessManager
from sqlalchemy import func, and_

def test_statistics_queries():
    """Test des requêtes utilisées dans la section statistiques"""
    print("🧪 Test des requêtes de statistiques Business Managers...")
    
    try:
        with get_database_session() as session:
            # Test 1: Statistiques générales
            print("\n1️⃣ Test des statistiques générales...")
            total_bms = session.query(BusinessManager).count()
            total_active_bms = (
                session.query(BusinessManager).filter(BusinessManager.actif).count()
            )
            active_assignments = (
                session.query(ConsultantBusinessManager)
                .filter(ConsultantBusinessManager.date_fin.is_(None))
                .count()
            )
            
            print(f"   ✅ Total BMs: {total_bms}")
            print(f"   ✅ BMs Actifs: {total_active_bms}")
            print(f"   ✅ Assignations actives: {active_assignments}")
            
            # Test 2: Répartition par BM (requête corrigée)
            print("\n2️⃣ Test de la répartition par BM (requête corrigée)...")
            
            bm_stats = (
                session.query(
                    BusinessManager.prenom,
                    BusinessManager.nom,
                    func.count(ConsultantBusinessManager.id).label("consultants_count")
                ).outerjoin(
                    ConsultantBusinessManager,
                    and_(
                        BusinessManager.id == ConsultantBusinessManager.business_manager_id,
                        ConsultantBusinessManager.date_fin.is_(None)
                    )
                ).filter(BusinessManager.actif).group_by(
                    BusinessManager.id, BusinessManager.prenom, BusinessManager.nom
                ).all()
            )
            
            print(f"   ✅ Répartition par BM: {len(bm_stats)} BMs trouvés")
            for bm_prenom, bm_nom, count in bm_stats[:5]:  # Afficher les 5 premiers
                print(f"      - {bm_prenom} {bm_nom}: {count} consultants")
            
            # Test 3: Évolution mensuelle
            print("\n3️⃣ Test de l'évolution mensuelle...")
            from sqlalchemy import extract
            
            monthly_stats = (
                session.query(
                    extract("year", ConsultantBusinessManager.date_creation).label("year"),
                    extract("month", ConsultantBusinessManager.date_creation).label("month"),
                    func.count(ConsultantBusinessManager.id).label("count"),
                )
                .group_by("year", "month")
                .order_by("year", "month")
                .limit(12)
                .all()
            )
            
            print(f"   ✅ Évolution mensuelle: {len(monthly_stats)} mois trouvés")
            for year, month, count in monthly_stats[-3:]:  # Afficher les 3 derniers mois
                print(f"      - {int(year)}/{int(month):02d}: {count} assignations")
            
            print("\n🎉 Tous les tests sont passés avec succès !")
            print("✅ L'erreur 'int' object has no attribute 'label' est corrigée")
            
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 DIAGNOSTIC DES STATISTIQUES BUSINESS MANAGERS")
    print("=" * 60)
    
    success = test_statistics_queries()
    
    if success:
        print(f"\n✅ DIAGNOSTIC TERMINÉ - Correction réussie !")
        print("🚀 L'onglet Statistiques devrait maintenant fonctionner correctement")
    else:
        print(f"\n❌ DIAGNOSTIC ÉCHOUÉ - Des problèmes persistent")
        
    print("=" * 60)