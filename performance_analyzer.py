#!/usr/bin/env python3
"""
Analyseur de performance pour l'application Consultator
Mesure les temps de réponse des principales fonctions
"""

import os
import statistics
import sys
import time
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

# Ajouter le chemin app au PYTHONPATH
sys.path.insert(0, os.path.join(os.getcwd(), "app"))


def measure_time(func, *args, **kwargs):
    """Mesure le temps d'exécution d'une fonction"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


def analyze_consultant_service_performance():
    """Analyse les performances du service consultant"""

    print("🔍 ANALYSE DES PERFORMANCES - CONSULTATOR")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        from services.consultant_service import ConsultantService

        # Tests multiples pour statistiques fiables
        num_tests = 5

        # Test 1: get_all_consultants (pagination standard)
        print("📋 TEST 1: get_all_consultants (50 premiers)")
        times_get_all = []

        for i in range(num_tests):
            result, exec_time = measure_time(
                ConsultantService.get_all_consultants, 1, 50
            )
            times_get_all.append(exec_time)
            print(f"  Test {i+1}: {exec_time:.3f}s - {len(result)} consultants")

        avg_get_all = statistics.mean(times_get_all)
        min_get_all = min(times_get_all)
        max_get_all = max(times_get_all)

        print("  📊 Statistiques:")
        print(f"    • Moyenne: {avg_get_all:.3f}s")
        print(f"    • Min: {min_get_all:.3f}s")
        print(f"    • Max: {max_get_all:.3f}s")
        print()

        # Test 2: search_consultants_optimized (recherche simple)
        print("🔍 TEST 2: search_consultants_optimized ('Jean')")
        times_search = []

        for i in range(num_tests):
            result, exec_time = measure_time(
                ConsultantService.search_consultants_optimized, "Jean"
            )
            times_search.append(exec_time)
            print(f"  Test {i+1}: {exec_time:.3f}s - {len(result)} résultats")

        avg_search = statistics.mean(times_search)
        min_search = min(times_search)
        max_search = max(times_search)

        print("  📊 Statistiques:")
        print(f"    • Moyenne: {avg_search:.3f}s")
        print(f"    • Min: {min_search:.3f}s")
        print(f"    • Max: {max_search:.3f}s")
        print()

        # Test 3: get_all_consultants_objects (objets SQLAlchemy)
        print("🏗️ TEST 3: get_all_consultants_objects (objets bruts)")
        times_objects = []

        for i in range(num_tests):
            result, exec_time = measure_time(
                ConsultantService.get_all_consultants_objects, 1, 50
            )
            times_objects.append(exec_time)
            print(f"  Test {i+1}: {exec_time:.3f}s - {len(result)} objets")

        avg_objects = statistics.mean(times_objects)
        min_objects = min(times_objects)
        max_objects = max(times_objects)

        print("  📊 Statistiques:")
        print(f"    • Moyenne: {avg_objects:.3f}s")
        print(f"    • Min: {min_objects:.3f}s")
        print(f"    • Max: {max_objects:.3f}s")
        print()

        # Test 4: Recherche spécifique (Abdallah)
        print("🎯 TEST 4: search_consultants_optimized ('Abdallah')")
        times_specific = []

        for i in range(num_tests):
            result, exec_time = measure_time(
                ConsultantService.search_consultants_optimized, "Abdallah"
            )
            times_specific.append(exec_time)
            print(f"  Test {i+1}: {exec_time:.3f}s - {len(result)} résultats")

        avg_specific = statistics.mean(times_specific)
        min_specific = min(times_specific)
        max_specific = max(times_specific)

        print("  📊 Statistiques:")
        print(f"    • Moyenne: {avg_specific:.3f}s")
        print(f"    • Min: {min_specific:.3f}s")
        print(f"    • Max: {max_specific:.3f}s")
        print()

        # Test 5: Grande pagination (stress test)
        print("⚡ TEST 5: get_all_consultants (pagination large - 200)")
        times_large = []

        for i in range(3):  # Moins de tests car plus lourd
            result, exec_time = measure_time(
                ConsultantService.get_all_consultants, 1, 200
            )
            times_large.append(exec_time)
            print(f"  Test {i+1}: {exec_time:.3f}s - {len(result)} consultants")

        avg_large = statistics.mean(times_large)
        min_large = min(times_large)
        max_large = max(times_large)

        print("  📊 Statistiques:")
        print(f"    • Moyenne: {avg_large:.3f}s")
        print(f"    • Min: {min_large:.3f}s")
        print(f"    • Max: {max_large:.3f}s")
        print()

        # ANALYSE COMPARATIVE
        print("📈 ANALYSE COMPARATIVE")
        print("=" * 40)

        performance_data = [
            ("get_all_consultants (50)", avg_get_all, "Liste standard"),
            ("search_consultants ('Jean')", avg_search, "Recherche courante"),
            ("get_all_consultants_objects", avg_objects, "Objets bruts"),
            ("search_consultants ('Abdallah')", avg_specific, "Recherche spécifique"),
            ("get_all_consultants (200)", avg_large, "Pagination large"),
        ]

        # Trier par performance
        performance_data.sort(key=lambda x: x[1])

        print("🏆 CLASSEMENT PAR VITESSE:")
        for i, (test_name, avg_time, description) in enumerate(performance_data, 1):
            status = (
                "🚀"
                if avg_time < 0.1
                else "⚡"
                if avg_time < 0.5
                else "🐌"
                if avg_time > 1.0
                else "✅"
            )
            print(f"  {i}. {status} {test_name}: {avg_time:.3f}s ({description})")

        print()

        # RECOMMANDATIONS
        print("💡 RECOMMANDATIONS")
        print("=" * 40)

        if avg_get_all < 0.2:
            print("✅ Performance EXCELLENTE pour la liste standard")
        elif avg_get_all < 0.5:
            print("⚡ Performance BONNE pour la liste standard")
        else:
            print("⚠️ Performance à améliorer pour la liste standard")

        if avg_search < 0.3:
            print("✅ Recherche RAPIDE et optimisée")
        else:
            print("⚠️ Recherche pourrait être optimisée")

        if avg_large > 1.0:
            print("⚠️ Pagination large lente - considérer la limitation")
        else:
            print("✅ Pagination large acceptable")

        # Ratio performance
        search_vs_list = avg_search / avg_get_all
        objects_vs_dict = avg_objects / avg_get_all

        print("\n📊 RATIOS:")
        print(f"  • Recherche vs Liste: {search_vs_list:.2f}x")
        print(f"  • Objets vs Dictionnaires: {objects_vs_dict:.2f}x")

        if search_vs_list < 1.5:
            print("  ✅ Recherche bien optimisée par rapport à la liste")
        else:
            print("  ⚠️ Recherche plus lente que prévu")

        return {
            "get_all_avg": avg_get_all,
            "search_avg": avg_search,
            "objects_avg": avg_objects,
            "specific_avg": avg_specific,
            "large_avg": avg_large,
        }

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback

        traceback.print_exc()
        return None


def analyze_database_performance():
    """Analyse les performances de la base de données"""

    print("\n🗄️ ANALYSE BASE DE DONNÉES")
    print("=" * 40)

    try:
        from database.database import get_database_session
        from database.models import Consultant
        from database.models import Mission
        from database.models import Practice

        # Test connexion DB
        start_time = time.time()
        session = get_database_session()
        connection_time = time.time() - start_time

        print(f"🔌 Connexion DB: {connection_time:.3f}s")

        # Test count consultants
        start_time = time.time()
        count_consultants = session.query(Consultant).count()
        count_time = time.time() - start_time

        print(
            f"📊 Count consultants: {count_time:.3f}s ({count_consultants} consultants)"
        )

        # Test count missions
        start_time = time.time()
        count_missions = session.query(Mission).count()
        mission_count_time = time.time() - start_time

        print(
            f"📋 Count missions: {mission_count_time:.3f}s ({count_missions} missions)"
        )

        # Test requête avec JOIN
        start_time = time.time()
        consultants_with_practice = (  # noqa: F841
            session.query(Consultant)
            .join(Practice, Consultant.practice_id == Practice.id, isouter=True)
            .limit(10)
            .all()
        )
        join_time = time.time() - start_time

        print(f"🔗 Requête JOIN (10 résultats): {join_time:.3f}s")

        session.close()

        # Évaluation performance DB
        if connection_time < 0.05:
            print("✅ Connexion DB très rapide")
        elif connection_time < 0.1:
            print("⚡ Connexion DB acceptable")
        else:
            print("⚠️ Connexion DB lente")

        if count_time < 0.1:
            print("✅ Count très rapide")
        else:
            print("⚠️ Count pourrait être optimisé")

        return {
            "connection_time": connection_time,
            "count_time": count_time,
            "join_time": join_time,
            "total_consultants": count_consultants,
            "total_missions": count_missions,
        }

    except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
        print(f"❌ Erreur DB: {e}")
        return None


def main():
    """Fonction principale d'analyse"""

    service_perf = analyze_consultant_service_performance()
    db_perf = analyze_database_performance()

    print("\n🎯 RÉSUMÉ EXÉCUTIF")
    print("=" * 40)

    if service_perf and db_perf:
        # Score global
        avg_response = service_perf["get_all_avg"]

        if avg_response < 0.2:
            score = "A+ (EXCELLENT)"
            emoji = "🏆"
        elif avg_response < 0.5:
            score = "A (TRÈS BON)"
            emoji = "🥇"
        elif avg_response < 1.0:
            score = "B (BON)"
            emoji = "🥈"
        else:
            score = "C (À AMÉLIORER)"
            emoji = "🥉"

        print(f"{emoji} SCORE GLOBAL: {score}")
        print(f"📊 Temps de réponse moyen: {avg_response:.3f}s")
        print(f"👥 Base de données: {db_perf['total_consultants']} consultants")
        print(f"📋 Missions: {db_perf['total_missions']} missions")

        # Recommandations finales
        print("\n💎 RECOMMANDATIONS FINALES:")
        if avg_response < 0.3:
            print("  ✅ Application très performante - RAS")
        elif avg_response < 0.7:
            print("  ⚡ Performance correcte - monitoring recommandé")
        else:
            print("  ⚠️ Optimisations nécessaires:")
            print("    • Ajouter des index sur les colonnes de recherche")
            print("    • Implémenter un cache Redis")
            print("    • Optimiser les requêtes SQL")

    print(f"\n📝 Analyse terminée le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
