"""
Tests unitaires pour le service de cache
Couvre toutes les fonctionnalités du CacheService
"""

import json
import time
import unittest.mock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.services.cache_service import CacheService
from app.services.cache_service import cached
from app.services.cache_service import get_cache_service
from app.services.cache_service import get_cached_consultant_stats
from app.services.cache_service import get_cached_consultants_list
from app.services.cache_service import get_cached_search_results
from app.services.cache_service import invalidate_cache
from app.services.cache_service import invalidate_consultant_cache
from app.services.cache_service import invalidate_mission_cache
from app.services.cache_service import invalidate_practice_cache
from app.services.cache_service import invalidate_search_cache


class TestCacheService:
    """Tests pour la classe CacheService"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.cache_service = CacheService(default_ttl=60)

    def test_init_without_redis(self):
        """Test d'initialisation sans Redis"""
        with patch("app.services.cache_service.REDIS_AVAILABLE", False):
            cache = CacheService()
            assert cache.redis_client is None
            assert cache.default_ttl == 300
            assert isinstance(cache.memory_cache, dict)

    def test_init_with_redis_success(self):
        """Test d'initialisation avec Redis disponible"""
        mock_redis = MagicMock()
        with patch("app.services.cache_service.REDIS_AVAILABLE", True), patch(
            "app.services.cache_service.redis"
        ) as mock_redis_module:
            mock_redis_module.from_url.return_value = mock_redis
            mock_redis.ping.return_value = True

            cache = CacheService(redis_url="redis://test:6379/0", default_ttl=120)

            assert cache.redis_client == mock_redis
            assert cache.default_ttl == 120
            mock_redis_module.from_url.assert_called_once_with("redis://test:6379/0")
            mock_redis.ping.assert_called_once()

    def test_init_with_redis_connection_error(self):
        """Test d'initialisation avec erreur de connexion Redis"""
        with patch("app.services.cache_service.REDIS_AVAILABLE", True), patch(
            "app.services.cache_service.redis"
        ) as mock_redis_module:
            mock_redis_module.from_url.side_effect = Exception("Connection failed")

            cache = CacheService()

            assert cache.redis_client is None

    def test_generate_key(self):
        """Test de génération de clé de cache"""
        key = self.cache_service._generate_key("test_func", (1, 2), {"param": "value"})

        # Vérifier le format de la clé
        assert key.startswith("consultator:test_func:")
        assert len(key) == len("consultator:test_func:") + 64  # SHA-256 hex = 64 chars

        # Vérifier que la même entrée génère la même clé
        key2 = self.cache_service._generate_key("test_func", (1, 2), {"param": "value"})
        assert key == key2

        # Vérifier que des arguments différents génèrent des clés différentes
        key3 = self.cache_service._generate_key("test_func", (1, 3), {"param": "value"})
        assert key != key3

    def test_is_expired(self):
        """Test de vérification d'expiration"""
        # Entrée non expirée
        future_time = time.time() + 100
        entry = {"expires_at": future_time}
        assert not self.cache_service._is_expired(entry)

        # Entrée expirée
        past_time = time.time() - 100
        entry = {"expires_at": past_time}
        assert self.cache_service._is_expired(entry)

        # Entrée sans expires_at
        entry = {}
        assert self.cache_service._is_expired(entry)

    def test_get_from_memory_cache(self):
        """Test de récupération depuis le cache mémoire"""
        key = "test_key"
        value = {"data": "test_value"}
        self.cache_service.memory_cache[key] = {
            "data": value,
            "expires_at": time.time() + 100,
        }

        result = self.cache_service.get(key)
        assert result == value

    def test_get_expired_from_memory_cache(self):
        """Test de récupération d'une entrée expirée du cache mémoire"""
        key = "test_key"
        self.cache_service.memory_cache[key] = {
            "data": "test_value",
            "expires_at": time.time() - 100,
        }

        result = self.cache_service.get(key)
        assert result is None
        # Vérifier que l'entrée a été supprimée
        assert key not in self.cache_service.memory_cache

    def test_get_from_redis_cache(self):
        """Test de récupération depuis Redis"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis
        mock_redis.get.return_value = json.dumps({"data": "redis_value"})

        result = self.cache_service.get("test_key")
        assert result == {"data": "redis_value"}
        mock_redis.get.assert_called_once_with("test_key")

    def test_get_from_redis_with_error(self):
        """Test de récupération depuis Redis avec erreur"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis
        mock_redis.get.side_effect = Exception("Redis error")

        # Devrait retourner None et logger l'erreur
        result = self.cache_service.get("test_key")
        assert result is None

    def test_set_in_memory_cache(self):
        """Test de stockage dans le cache mémoire"""
        key = "test_key"
        value = "test_value"

        result = self.cache_service.set(key, value, ttl=30)
        assert result is True

        # Vérifier que l'entrée a été créée
        assert key in self.cache_service.memory_cache
        entry = self.cache_service.memory_cache[key]
        assert entry["data"] == value
        assert entry["expires_at"] > time.time()
        assert entry["created_at"] <= time.time()

    def test_set_in_redis_cache(self):
        """Test de stockage dans Redis"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis

        key = "test_key"
        value = {"complex": "data"}

        result = self.cache_service.set(key, value, ttl=120)
        assert result is True

        # Vérifier l'appel Redis
        mock_redis.setex.assert_called_once_with(key, 120, json.dumps(value, default=str))

    def test_set_in_redis_with_error(self):
        """Test de stockage dans Redis avec erreur"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis
        mock_redis.setex.side_effect = Exception("Redis error")

        result = self.cache_service.set("test_key", "value")
        # Devrait quand même réussir (stockage en mémoire)
        assert result is True

    def test_delete_from_memory_cache(self):
        """Test de suppression du cache mémoire"""
        key = "test_key"
        self.cache_service.memory_cache[key] = {
            "data": "value",
            "expires_at": time.time() + 100,
        }

        result = self.cache_service.delete(key)
        assert result is True
        assert key not in self.cache_service.memory_cache

    def test_delete_from_redis_cache(self):
        """Test de suppression de Redis"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis
        mock_redis.delete.return_value = 1

        result = self.cache_service.delete("test_key")
        assert result is True
        mock_redis.delete.assert_called_once_with("test_key")

    def test_delete_from_both_caches(self):
        """Test de suppression des deux caches"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis
        mock_redis.delete.return_value = 1

        key = "test_key"
        self.cache_service.memory_cache[key] = {
            "data": "value",
            "expires_at": time.time() + 100,
        }

        result = self.cache_service.delete(key)
        assert result is True
        assert key not in self.cache_service.memory_cache
        mock_redis.delete.assert_called_once_with(key)

    def test_clear_pattern_memory_only(self):
        """Test de suppression par pattern (mémoire uniquement)"""
        # Créer des clés de test
        self.cache_service.memory_cache = {
            "consultator:user:1": {"data": "user1"},
            "consultator:user:2": {"data": "user2"},
            "consultator:post:1": {"data": "post1"},
        }

        result = self.cache_service.clear_pattern("consultator:user:*")
        assert result == 2  # 2 clés supprimées
        assert "consultator:user:1" not in self.cache_service.memory_cache
        assert "consultator:user:2" not in self.cache_service.memory_cache
        assert "consultator:post:1" in self.cache_service.memory_cache

    def test_clear_pattern_with_redis(self):
        """Test de suppression par pattern avec Redis"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis
        mock_redis.keys.return_value = ["key1", "key2"]

        result = self.cache_service.clear_pattern("pattern:*")
        assert result == 2
        mock_redis.keys.assert_called_once_with("pattern:*")
        mock_redis.delete.assert_called_once_with("key1", "key2")

    def test_get_stats_without_redis(self):
        """Test des statistiques sans Redis"""
        # Ajouter des données de test
        self.cache_service.memory_cache = {
            "key1": {"data": "value1"},
            "key2": {"data": "value2"},
        }

        stats = self.cache_service.get_stats()

        assert stats["memory_cache"]["entries"] == 2
        assert stats["memory_cache"]["estimated_size_kb"] > 0
        assert stats["redis"]["connected"] is False
        assert "reason" in stats["redis"]

    def test_get_stats_with_redis(self):
        """Test des statistiques avec Redis"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis
        mock_redis.info.return_value = {
            "used_memory_human": "1.2M",
            "connected_clients": 5,
            "uptime_in_days": 10,
        }

        stats = self.cache_service.get_stats()

        assert stats["redis"]["connected"] is True
        assert stats["redis"]["used_memory_human"] == "1.2M"
        assert stats["redis"]["connected_clients"] == 5
        assert stats["redis"]["uptime_days"] == 10

    def test_get_stats_redis_error(self):
        """Test des statistiques avec erreur Redis"""
        mock_redis = MagicMock()
        self.cache_service.redis_client = mock_redis
        mock_redis.info.side_effect = Exception("Redis error")

        stats = self.cache_service.get_stats()

        assert stats["redis"]["connected"] is False
        assert "error" in stats["redis"]


class TestGlobalCacheFunctions:
    """Tests pour les fonctions globales du cache"""

    def test_get_cache_service_singleton(self):
        """Test du pattern singleton pour get_cache_service"""
        # Reset global state
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service1 = get_cache_service()
        service2 = get_cache_service()

        assert service1 is service2
        assert isinstance(service1, CacheService)

    def test_cached_decorator(self):
        """Test du décorateur @cached"""
        # Reset global state
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        call_count = 0

        @cached(ttl=30)
        def test_function(x, y=10):
            nonlocal call_count
            call_count += 1
            return x + y

        # Premier appel - devrait exécuter la fonction
        result1 = test_function(5, y=15)
        assert result1 == 20
        assert call_count == 1

        # Deuxième appel avec mêmes arguments - devrait utiliser le cache
        result2 = test_function(5, y=15)
        assert result2 == 20
        assert call_count == 1  # Fonction pas appelée à nouveau

        # Appel avec arguments différents - devrait exécuter la fonction
        result3 = test_function(10, y=15)
        assert result3 == 25
        assert call_count == 2

    def test_cached_decorator_with_prefix(self):
        """Test du décorateur @cached avec préfixe"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        @cached(ttl=30, key_prefix="test")
        def test_function(x):
            return x * 2

        result = test_function(5)
        assert result == 10

        # Vérifier que la clé contient le préfixe
        cache_service = get_cache_service()
        # La clé devrait commencer par "consultator:test:test_function:"
        cache_keys = list(cache_service.memory_cache.keys())
        assert len(cache_keys) == 1
        assert cache_keys[0].startswith("consultator:test:test_function:")

    def test_invalidate_cache(self):
        """Test de la fonction invalidate_cache"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        cache_service = get_cache_service()
        # Ajouter des données de test
        cache_service.memory_cache = {
            "consultator:user:1": {"data": "user1"},
            "consultator:post:1": {"data": "post1"},
        }

        result = invalidate_cache("consultator:user:*")
        assert result == 1
        assert "consultator:user:1" not in cache_service.memory_cache
        assert "consultator:post:1" in cache_service.memory_cache

    def test_invalidate_consultant_cache_all(self):
        """Test d'invalidation du cache consultant (tous)"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        cache_service = get_cache_service()
        cache_service.memory_cache = {
            "consultator:get_consultants:abc": {"data": "consultants"},
            "consultator:get_user:123": {"data": "user"},
        }

        invalidate_consultant_cache()

        # Vérifier que seules les clés consultant ont été supprimées
        assert len(cache_service.memory_cache) == 1
        assert "consultator:get_user:123" in cache_service.memory_cache

    def test_invalidate_consultant_cache_specific(self):
        """Test d'invalidation du cache consultant (spécifique)"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        cache_service = get_cache_service()
        cache_service.memory_cache = {
            "consultator:get_consultant_123:abc": {"data": "consultant123"},
            "consultator:get_consultant_456:def": {"data": "consultant456"},
            "consultator:get_user:123": {"data": "user"},
        }

        invalidate_consultant_cache(123)

        assert "consultator:get_consultant_123:abc" not in cache_service.memory_cache
        assert "consultator:get_consultant_456:def" in cache_service.memory_cache
        assert "consultator:get_user:123" in cache_service.memory_cache

    def test_invalidate_mission_cache(self):
        """Test d'invalidation du cache mission"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        cache_service = get_cache_service()
        cache_service.memory_cache = {
            "consultator:get_missions_123:abc": {"data": "missions123"},
            "consultator:get_other:def": {"data": "other"},
        }

        invalidate_mission_cache(123)

        assert "consultator:get_missions_123:abc" not in cache_service.memory_cache
        assert "consultator:get_other:def" in cache_service.memory_cache

    def test_invalidate_practice_cache(self):
        """Test d'invalidation du cache practice"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        cache_service = get_cache_service()
        cache_service.memory_cache = {
            "consultator:get_practices:abc": {"data": "practices"},
            "consultator:get_other:def": {"data": "other"},
        }

        invalidate_practice_cache()

        assert "consultator:get_practices:abc" not in cache_service.memory_cache
        assert "consultator:get_other:def" in cache_service.memory_cache

    def test_invalidate_search_cache(self):
        """Test d'invalidation du cache recherche"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        cache_service = get_cache_service()
        cache_service.memory_cache = {
            "consultator:search_consultants:abc": {"data": "search_results"},
            "consultator:get_other:def": {"data": "other"},
        }

        invalidate_search_cache()

        assert "consultator:search_consultants:abc" not in cache_service.memory_cache
        assert "consultator:get_other:def" in cache_service.memory_cache


class TestCachedFunctions:
    """Tests pour les fonctions mises en cache"""

    def test_get_cached_consultant_stats(self):
        """Test de la fonction get_cached_consultant_stats"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        with patch("app.services.consultant_service.ConsultantService") as mock_service:
            mock_service.get_consultant_summary_stats.return_value = {"total": 100}

            # Premier appel
            stats1 = get_cached_consultant_stats()
            assert stats1 == {"total": 100}
            mock_service.get_consultant_summary_stats.assert_called_once()

            # Deuxième appel - devrait utiliser le cache
            stats2 = get_cached_consultant_stats()
            assert stats2 == {"total": 100}
            # La fonction ne devrait pas être appelée une deuxième fois
            mock_service.get_consultant_summary_stats.assert_called_once()

    def test_get_cached_consultants_list(self):
        """Test de la fonction get_cached_consultants_list"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        with patch("app.services.consultant_service.ConsultantService") as mock_service:
            mock_service.get_all_consultants_with_stats.return_value = [{"id": 1, "name": "Test"}]

            # Test avec paramètres par défaut
            result = get_cached_consultants_list()
            assert result == [{"id": 1, "name": "Test"}]
            mock_service.get_all_consultants_with_stats.assert_called_once_with(1, 50)

    def test_get_cached_search_results(self):
        """Test de la fonction get_cached_search_results"""
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        with patch("app.services.consultant_service.ConsultantService") as mock_service:
            mock_service.search_consultants_optimized.return_value = [{"id": 1, "name": "John"}]

            result = get_cached_search_results("John", page=2, per_page=10)
            assert result == [{"id": 1, "name": "John"}]
            mock_service.search_consultants_optimized.assert_called_once_with("John", 2, 10)
