"""
Démonstration simple du cache
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.services.cache_service import get_cache_service
import time


def benchmark_function(func, *args, **kwargs):
    """Mesure le temps d'exécution d'une fonction"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time


def expensive_operation(param: str):
    """Fonction coûteuse simulée"""
    print(f"   🔄 Exécution coûteuse pour: {param}")
    time.sleep(0.1)  # Simulation d'opération coûteuse
    return f"Résultat pour {param}: {time.time()}"


def test_cache_basic():
    """Test basique du cache"""
    print("🚀 TEST DU CACHE DE BASE")
    print("=" * 40)

    cache_service = get_cache_service()

    # Test 1: Stockage et récupération
    print("\n📋 Test 1: Stockage/récupération")
    test_key = "demo_key"
    test_data = {
        "message": "Hello Cache!",
        "timestamp": time.time(),
        "data": [1, 2, 3, 4, 5]
    }

    # Stocker
    success = cache_service.set(test_key, test_data, ttl=60)
    print(f"✅ Stockage réussi: {success}")

    # Récupérer
    cached_data = cache_service.get(test_key)
    print(f"✅ Récupération réussie: {cached_data is not None}")
    if cached_data:
        print(f"   Message: {cached_data['message']}")

    # Test 2: Performance
    print("\n⚡ Test 2: Performance")

    print("🔄 Premier appel:")
    result1, time1 = benchmark_function(expensive_operation, "test1")
    print(".4f")

    print("⚡ Deuxième appel (devrait être en cache):")
    # Simuler un cache manuel
    cache_key = "expensive_test1"
    cached_result = cache_service.get(cache_key)

    if cached_result:
        result2, time2 = cached_result, 0.001  # Temps simulé pour le cache
        print(".4f")
        print("   💾 Résultat depuis le cache!")
    else:
        result2, time2 = benchmark_function(expensive_operation, "test1")
        cache_service.set(cache_key, result2, ttl=30)
        print(".4f")

    if time1 > 0:
        improvement = ((time1 - time2) / time1) * 100
        print(".1f")

    # Test 3: Statistiques
    print("\n📊 Test 3: Statistiques du cache")
    stats = cache_service.get_stats()
    print(f"📈 Entrées en mémoire: {stats['memory_cache']['entries']}")
    print(".1f")
    print(f"🔌 Redis connecté: {stats['redis']['connected']}")
    print("\n✅ Démonstration terminée!")


if __name__ == "__main__":
    test_cache_basic()
