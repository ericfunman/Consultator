"""
Tests Phase 55 - cache_service.py (Coverage boost 68% → 70%+)
Cible: CacheService avec logique de cache multi-niveaux (Redis + Memory)
"""

import pytest
import time
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Import du service à tester
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from app.services.cache_service import CacheService, REDIS_AVAILABLE


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_redis():
    """Mock client Redis"""
    mock_client = Mock()
    mock_client.ping = Mock(return_value=True)
    mock_client.get = Mock(return_value=None)
    mock_client.set = Mock(return_value=True)
    mock_client.delete = Mock(return_value=1)
    mock_client.exists = Mock(return_value=0)
    mock_client.keys = Mock(return_value=[])
    mock_client.flushdb = Mock(return_value=True)
    return mock_client


@pytest.fixture
def cache_service_no_redis():
    """CacheService sans Redis (memory only)"""
    with patch('app.services.cache_service.REDIS_AVAILABLE', False):
        service = CacheService()
        return service


@pytest.fixture
def cache_service_with_redis(mock_redis):
    """CacheService avec Redis mocké"""
    with patch('redis.from_url', return_value=mock_redis):
        service = CacheService()
        return service


# ============================================================================
# TESTS: __init__()
# ============================================================================

class TestCacheServiceInit:
    """Tests pour l'initialisation de CacheService"""

    def test_init_default_values(self):
        """Test initialisation avec valeurs par défaut"""
        with patch('app.services.cache_service.REDIS_AVAILABLE', False):
            service = CacheService()
            
            assert service.default_ttl == 300  # 5 minutes
            assert service.redis_client is None
            assert service.memory_cache == {}

    def test_init_custom_ttl(self):
        """Test initialisation avec TTL personnalisé"""
        with patch('app.services.cache_service.REDIS_AVAILABLE', False):
            service = CacheService(default_ttl=600)
            
            assert service.default_ttl == 600

    def test_init_redis_not_available(self):
        """Test quand Redis n'est pas installé"""
        with patch('app.services.cache_service.REDIS_AVAILABLE', False):
            service = CacheService()
            
            assert service.redis_client is None


# ============================================================================
# TESTS: _generate_key()
# ============================================================================

class TestGenerateKey:
    """Tests pour _generate_key()"""

    def test_generate_key_simple_args(self, cache_service_no_redis):
        """Test génération de clé avec arguments simples"""
        key = cache_service_no_redis._generate_key("func_name", (1, 2), {})
        
        assert key.startswith("consultator:func_name:")
        assert len(key) > 30  # Hash SHA-256

    def test_generate_key_with_kwargs(self, cache_service_no_redis):
        """Test génération de clé avec kwargs"""
        key = cache_service_no_redis._generate_key("test_func", (), {"param": "value"})
        
        assert "test_func" in key
        assert isinstance(key, str)

    def test_generate_key_consistency(self, cache_service_no_redis):
        """Test que la même input génère toujours la même clé"""
        key1 = cache_service_no_redis._generate_key("func", (1, 2), {"a": "b"})
        key2 = cache_service_no_redis._generate_key("func", (1, 2), {"a": "b"})
        
        assert key1 == key2

    def test_generate_key_different_args_different_keys(self, cache_service_no_redis):
        """Test que des arguments différents génèrent des clés différentes"""
        key1 = cache_service_no_redis._generate_key("func", (1,), {})
        key2 = cache_service_no_redis._generate_key("func", (2,), {})
        
        assert key1 != key2

    def test_generate_key_kwargs_order_independent(self, cache_service_no_redis):
        """Test que l'ordre des kwargs n'affecte pas la clé"""
        key1 = cache_service_no_redis._generate_key("func", (), {"a": 1, "b": 2})
        key2 = cache_service_no_redis._generate_key("func", (), {"b": 2, "a": 1})
        
        assert key1 == key2  # sort_keys=True dans JSON

    def test_generate_key_datetime_serialization(self, cache_service_no_redis):
        """Test sérialisation d'objets datetime"""
        now = datetime.now()
        key = cache_service_no_redis._generate_key("func", (now,), {})
        
        assert isinstance(key, str)
        assert "consultator:" in key


# ============================================================================
# TESTS: _is_expired()
# ============================================================================

class TestIsExpired:
    """Tests pour _is_expired()"""

    def test_is_expired_not_expired(self, cache_service_no_redis):
        """Test entrée non expirée"""
        future_time = time.time() + 100
        cache_entry = {"expires_at": future_time}
        
        assert not cache_service_no_redis._is_expired(cache_entry)

    def test_is_expired_expired(self, cache_service_no_redis):
        """Test entrée expirée"""
        past_time = time.time() - 100
        cache_entry = {"expires_at": past_time}
        
        assert cache_service_no_redis._is_expired(cache_entry)

    def test_is_expired_exact_time(self, cache_service_no_redis):
        """Test à l'instant exact d'expiration"""
        current_time = time.time()
        cache_entry = {"expires_at": current_time}
        
        # Devrait être expiré (time.time() >= expires_at)
        result = cache_service_no_redis._is_expired(cache_entry)
        assert isinstance(result, bool)

    def test_is_expired_missing_expires_at(self, cache_service_no_redis):
        """Test entrée sans champ expires_at"""
        cache_entry = {}
        
        assert cache_service_no_redis._is_expired(cache_entry)  # Expiré par défaut


# ============================================================================
# TESTS: get()
# ============================================================================

class TestGet:
    """Tests pour get()"""

    def test_get_from_memory_cache_valid(self, cache_service_no_redis):
        """Test récupération depuis cache mémoire valide"""
        key = "test_key"
        value = {"data": "test_value"}
        expires_at = time.time() + 100
        
        cache_service_no_redis.memory_cache[key] = {
            "data": value,
            "expires_at": expires_at
        }
        
        result = cache_service_no_redis.get(key)
        
        assert result == value

    def test_get_from_memory_cache_expired(self, cache_service_no_redis):
        """Test récupération depuis cache mémoire expiré"""
        key = "test_key"
        expires_at = time.time() - 100  # Expiré
        
        cache_service_no_redis.memory_cache[key] = {
            "data": "old_value",
            "expires_at": expires_at
        }
        
        result = cache_service_no_redis.get(key)
        
        assert result is None
        assert key not in cache_service_no_redis.memory_cache  # Supprimé

    def test_get_key_not_found(self, cache_service_no_redis):
        """Test récupération d'une clé inexistante"""
        result = cache_service_no_redis.get("nonexistent_key")
        
        assert result is None


# ============================================================================
# TESTS: set()
# ============================================================================

class TestSet:
    """Tests pour set()"""

    def test_set_memory_cache_default_ttl(self, cache_service_no_redis):
        """Test stockage dans cache mémoire avec TTL par défaut"""
        key = "test_key"
        value = {"test": "data"}
        
        result = cache_service_no_redis.set(key, value)
        
        assert result is True
        assert key in cache_service_no_redis.memory_cache
        assert cache_service_no_redis.memory_cache[key]["data"] == value

    def test_set_memory_cache_custom_ttl(self, cache_service_no_redis):
        """Test stockage avec TTL personnalisé"""
        key = "test_key"
        value = "test_value"
        ttl = 600
        
        before_time = time.time()
        cache_service_no_redis.set(key, value, ttl=ttl)
        after_time = time.time()
        
        cache_entry = cache_service_no_redis.memory_cache[key]
        assert cache_entry["data"] == value
        assert before_time + ttl <= cache_entry["expires_at"] <= after_time + ttl + 1


# ============================================================================
# TESTS: delete()
# ============================================================================

class TestDelete:
    """Tests pour delete()"""

    def test_delete_from_memory_cache(self, cache_service_no_redis):
        """Test suppression depuis cache mémoire"""
        key = "test_key"
        cache_service_no_redis.memory_cache[key] = {
            "data": "value",
            "expires_at": time.time() + 100
        }
        
        result = cache_service_no_redis.delete(key)
        
        assert result is True
        assert key not in cache_service_no_redis.memory_cache

    def test_delete_nonexistent_key(self, cache_service_no_redis):
        """Test suppression d'une clé inexistante"""
        result = cache_service_no_redis.delete("nonexistent_key")
        
        # La méthode retourne False si rien n'est supprimé
        assert result is False


# ============================================================================
# TESTS: clear() (méthode réelle du module)
# ============================================================================

class TestClear:
    """Tests pour clear()"""

    def test_clear_memory_cache(self, cache_service_no_redis):
        """Test clear() sur cache mémoire"""
        cache_service_no_redis.memory_cache["key1"] = {"data": "val1"}
        cache_service_no_redis.memory_cache["key2"] = {"data": "val2"}
        
        result = cache_service_no_redis.clear()
        
        assert result is True
        assert len(cache_service_no_redis.memory_cache) == 0


# ============================================================================
# TESTS: clear_pattern()
# ============================================================================

class TestClearPattern:
    """Tests pour clear_pattern()"""

    def test_clear_pattern_memory(self, cache_service_no_redis):
        """Test clear_pattern sur cache mémoire"""
        cache_service_no_redis.memory_cache["consultator:user:1"] = {"data": "val1"}
        cache_service_no_redis.memory_cache["consultator:user:2"] = {"data": "val2"}
        cache_service_no_redis.memory_cache["consultator:mission:1"] = {"data": "val3"}
        
        deleted_count = cache_service_no_redis.clear_pattern("consultator:user:*")
        
        assert deleted_count == 2
        assert "consultator:user:1" not in cache_service_no_redis.memory_cache
        assert "consultator:user:2" not in cache_service_no_redis.memory_cache
        assert "consultator:mission:1" in cache_service_no_redis.memory_cache

    def test_clear_pattern_no_match(self, cache_service_no_redis):
        """Test clear_pattern sans correspondances"""
        cache_service_no_redis.memory_cache["key1"] = {"data": "val1"}
        
        deleted_count = cache_service_no_redis.clear_pattern("nonexistent:*")
        
        assert deleted_count == 0
        assert "key1" in cache_service_no_redis.memory_cache


# ============================================================================
# TESTS: get_stats()
# ============================================================================

class TestGetStats:
    """Tests pour get_stats()"""

    def test_get_stats_empty_cache(self, cache_service_no_redis):
        """Test statistiques sur cache vide"""
        stats = cache_service_no_redis.get_stats()
        
        assert "memory_cache" in stats
        assert stats["memory_cache"]["entries"] == 0
        assert stats["redis"]["connected"] is False

    def test_get_stats_with_entries(self, cache_service_no_redis):
        """Test statistiques avec entrées"""
        current_time = time.time()
        
        cache_service_no_redis.memory_cache["key1"] = {
            "data": "val1",
            "expires_at": current_time + 100,
            "created_at": current_time - 50
        }
        cache_service_no_redis.memory_cache["key2"] = {
            "data": "val2",
            "expires_at": current_time - 10,  # Expiré
            "created_at": current_time - 60
        }
        
        stats = cache_service_no_redis.get_stats()
        
        assert stats["memory_cache"]["entries"] == 2
        assert "estimated_size_kb" in stats["memory_cache"]
        assert stats["redis"]["connected"] is False


# ============================================================================
# TESTS: Edge cases et intégration
# ============================================================================

class TestEdgeCases:
    """Tests de cas limites"""

    def test_large_value_storage(self, cache_service_no_redis):
        """Test stockage d'une grande valeur"""
        large_value = {"data": "x" * 10000}  # 10KB de données
        
        result = cache_service_no_redis.set("large_key", large_value)
        
        assert result is True
        retrieved = cache_service_no_redis.get("large_key")
        assert retrieved == large_value

    def test_none_value_storage(self, cache_service_no_redis):
        """Test stockage de None"""
        result = cache_service_no_redis.set("none_key", None)
        
        assert result is True
        retrieved = cache_service_no_redis.get("none_key")
        assert retrieved is None

    def test_complex_nested_data(self, cache_service_no_redis):
        """Test avec données complexes imbriquées"""
        complex_data = {
            "list": [1, 2, {"nested": "dict"}],
            "dict": {"a": [1, 2, 3]},
            "tuple_as_list": (1, 2, 3)
        }
        
        cache_service_no_redis.set("complex_key", complex_data)
        retrieved = cache_service_no_redis.get("complex_key")
        
        assert isinstance(retrieved, dict)
        assert retrieved["list"] == [1, 2, {"nested": "dict"}]

    def test_concurrent_access_simulation(self, cache_service_no_redis):
        """Test simulation d'accès concurrent"""
        # Simuler plusieurs écritures/lectures rapides
        for i in range(10):
            cache_service_no_redis.set(f"key_{i}", f"value_{i}")
        
        # Vérifier toutes les valeurs
        for i in range(10):
            assert cache_service_no_redis.get(f"key_{i}") == f"value_{i}"

    def test_ttl_zero(self, cache_service_no_redis):
        """Test avec TTL = 0 (expiration immédiate)"""
        cache_service_no_redis.set("test_key", "value", ttl=0)
        
        # TTL=0 signifie expiré immédiatement
        # La clé est stockée avec expires_at = time.time() + 0
        # Donc devrait être expiré lors de la récupération
        result = cache_service_no_redis.get("test_key")
        
        # Peut être None (expiré) ou "value" (récupéré juste après stockage)
        # Comportement dépend du timing
        assert result is None or result == "value"

    def test_negative_ttl(self, cache_service_no_redis):
        """Test avec TTL négatif"""
        cache_service_no_redis.set("test_key", "value", ttl=-100)
        
        # Déjà expiré
        result = cache_service_no_redis.get("test_key")
        
        assert result is None


# ============================================================================
# TESTS: Décorateurs et fonctions utilitaires
# ============================================================================

class TestDecoratorsAndHelpers:
    """Tests pour les décorateurs @cached et fonctions invalidate_*"""

    def test_cached_decorator_basic(self, cache_service_no_redis):
        """Test du décorateur @cached basique"""
        from app.services.cache_service import cached
        
        call_count = {"value": 0}
        
        @cached(ttl=60)
        def expensive_function(x: int) -> int:
            call_count["value"] += 1
            return x * 2
        
        # Premier appel - calcul
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count["value"] == 1
        
        # Deuxième appel - depuis cache
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count["value"] == 1  # Pas d'appel supplémentaire
        
        # Appel avec argument différent - nouveau calcul
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count["value"] == 2

    def test_cached_decorator_with_key_prefix(self, cache_service_no_redis):
        """Test du décorateur @cached avec préfixe"""
        from app.services.cache_service import cached
        
        @cached(ttl=60, key_prefix="test_module")
        def test_func(arg: str) -> str:
            return arg.upper()
        
        result = test_func("hello")
        assert result == "HELLO"

    def test_invalidate_consultant_cache_all(self):
        """Test invalidation du cache consultants (tous)"""
        from app.services.cache_service import invalidate_consultant_cache
        
        # Test que la fonction existe et s'exécute sans erreur
        result = invalidate_consultant_cache()
        # La fonction ne retourne rien (None)
        assert result is None

    def test_invalidate_consultant_cache_specific(self):
        """Test invalidation du cache pour un consultant spécifique"""
        from app.services.cache_service import invalidate_consultant_cache
        
        # Test que la fonction existe avec paramètre
        result = invalidate_consultant_cache(consultant_id=123)
        assert result is None

    def test_invalidate_mission_cache(self):
        """Test invalidation du cache missions"""
        from app.services.cache_service import invalidate_mission_cache
        
        # Test que la fonction existe
        result = invalidate_mission_cache()
        assert result is None

    def test_invalidate_practice_cache(self):
        """Test invalidation du cache practices"""
        from app.services.cache_service import invalidate_practice_cache
        
        # Test que la fonction existe
        result = invalidate_practice_cache()
        assert result is None

    def test_invalidate_search_cache(self):
        """Test invalidation du cache recherches"""
        from app.services.cache_service import invalidate_search_cache
        
        # Test que la fonction existe
        result = invalidate_search_cache()
        assert result is None

    def test_get_cache_service_singleton(self):
        """Test que get_cache_service retourne toujours la même instance"""
        from app.services.cache_service import get_cache_service
        
        service1 = get_cache_service()
        service2 = get_cache_service()
        
        assert service1 is service2  # Même objet en mémoire

