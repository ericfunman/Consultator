"""
Démonstration des améliorations de performance avec le cache
Compare les performances avec et sans cache
"""

import time
from app.services.cache_service import get_cache_service, cached
from app.services.consultant_service import ConsultantService


def benchmark_function(func, *args, **kwargs):
    """Mesure le temps d'exécution d'une fonction"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


def test_cache_performance():
    """Test des performances du cache"""
    print("🚀 TEST DES PERFORMANCES DU CACHE")
    print("=" * 50)

    cache_service = get_cache_service()

    # Test 1: Cache simple
    print("\n📋 Test 1: Cache simple (mémoire)")
    test_key = "test_key"
    test_data = {"message": "Hello World", "timestamp": time.time()}

    # Stocker dans le cache
    cache_service.set(test_key, test_data, ttl=60)
    print("✅ Données stockées dans le cache")

    # Récupérer du cache
    cached_data = cache_service.get(test_key)
    print(f"✅ Données récupérées: {cached_data is not None}")

    # Test 2: Comparaison avec et sans cache pour les stats
    print("\n📊 Test 2: Comparaison stats consultants")

    # Sans cache
    print("🔄 Sans cache:")
    result1, time1 = benchmark_function(ConsultantService.get_consultant_summary_stats)
    print(f"   Temps: {time1:.4f}s")
    print(f"   Résultat: {len(result1)} métriques")

    # Avec cache (2ème appel devrait être plus rapide)
    print("⚡ Avec cache (2ème appel):")
    result2, time2 = benchmark_function(ConsultantService.get_consultant_summary_stats)
    print(f"   Temps: {time2:.4f}s")
    print(f"   Résultat: {len(result2)} métriques")

    # Calcul de l'amélioration
    if time2 > 0:
        improvement = ((time1 - time2) / time1) * 100
        print(f"   Amélioration: {improvement:.1f}%")

    # Test 3: Recherche avec cache
    print("\n🔍 Test 3: Recherche avec cache")

    search_term = "Jean"
    print(f"🔄 Recherche '{search_term}' sans cache:")
    result3, time3 = benchmark_function(
        ConsultantService.search_consultants_optimized,
        search_term, 1, 50
    )
    print(f"   Temps: {time3:.4f}s")
    print(f"   Résultats: {len(result3)} consultants")

    print(f"⚡ Recherche '{search_term}' avec cache:")
    result4, time4 = benchmark_function(
        ConsultantService.search_consultants_optimized,
        search_term, 1, 50
    )
    print(f"   Temps: {time4:.4f}s")
    print(f"   Résultats: {len(result4)} consultants")

    if time4 > 0:
        improvement_search = ((time3 - time4) / time3) * 100
        print(f"   Amélioration: {improvement_search:.1f}%")

    # Test 4: Statistiques du cache
    print("\n📈 Test 4: Statistiques du cache")
    stats = cache_service.get_stats()
    print(f"📊 Entrées en cache mémoire: {stats['memory_cache']['entries']}")
    print(f"📏 Taille estimée: {stats['memory_cache']['estimated_size_kb']:.1f} KB")
    print(f"🔌 Redis connecté: {stats['redis']['connected']}")

    if not stats['redis']['connected']:
        print(f"   Raison: {stats['redis']['reason']}")

    print("\n✅ Tests terminés!")


@cached(ttl=30)  # Cache 30 secondes
def expensive_operation(param: str):
    """Fonction coûteuse simulée pour démonstration"""
    print(f"   🔄 Exécution coûteuse pour paramètre: {param}")
    time.sleep(0.1)  # Simulation d'une opération coûteuse
    return f"Résultat pour {param}: {time.time()}"


def test_decorator_cache():
    """Test du décorateur de cache"""
    print("\n🎯 Test 5: Décorateur @cached")

    param = "test_param"

    print("🔄 Premier appel (sans cache):")
    result1, time1 = benchmark_function(expensive_operation, param)
    print(f"   Temps: {time1:.4f}s")
    print(f"   Résultat: {result1}")

    print("⚡ Deuxième appel (avec cache):")
    result2, time2 = benchmark_function(expensive_operation, param)
    print(f"   Temps: {time2:.4f}s")
    print(f"   Résultat: {result2}")

    if time2 > 0:
        improvement = ((time1 - time2) / time1) * 100
        print(f"   Amélioration: {improvement:.1f}%")

    print("\n🎉 Démonstration terminée!")


if __name__ == "__main__":
    test_cache_performance()
    test_decorator_cache()
