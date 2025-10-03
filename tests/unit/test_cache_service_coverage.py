"""
Tests unitaires pour le service de cache
Couvre les fonctionnalités de cache mémoire et Redis
"""

import json
import time
import unittest.mock
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import Mock
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

    def test_init_without_redis(self):
        """Test d'initialisation sans Redis disponible"""
        with patch("app.services.cache_service.REDIS_AVAILABLE", False):
            service = CacheService()
            assert service.redis_client is None
            assert service.default_ttl == 300
            assert isinstance(service.memory_cache, dict)

    def test_init_with_redis_success(self):
        """Test d'initialisation avec Redis disponible et connexion réussie"""
        mock_redis = Mock()
        mock_redis.ping.return_value = True

        with patch("app.services.cache_service.REDIS_AVAILABLE", True), patch(
            "app.services.cache_service.redis"
        ) as mock_redis_module:
            mock_redis_module.from_url.return_value = mock_redis

            service = CacheService(redis_url="redis://localhost:6379/0", default_ttl=600)

            assert service.redis_client is mock_redis
            assert service.default_ttl == 600
            mock_redis.ping.assert_called_once()

    def test_init_with_redis_failure(self):
        """Test d'initialisation avec Redis disponible mais connexion échouée"""
        with patch("app.services.cache_service.REDIS_AVAILABLE", True), patch(
            "app.services.cache_service.redis"
        ) as mock_redis_module:
            mock_redis_module.from_url.side_effect = Exception("Connection failed")

            service = CacheService()

            assert service.redis_client is None
            assert service.default_ttl == 300

    def test_generate_key(self):
        """Test de génération de clé de cache"""
        service = CacheService()

        # Test avec arguments simples
        key1 = service._generate_key("test_func", (1, 2), {"param": "value"})
        key2 = service._generate_key("test_func", (1, 2), {"param": "value"})
        key3 = service._generate_key("test_func", (2, 1), {"param": "value"})

        assert key1 == key2  # Même arguments = même clé
        assert key1 != key3  # Arguments différents = clé différente
        assert key1.startswith("consultator:test_func:")

    def test_generate_key_with_complex_args(self):
        """Test de génération de clé avec arguments complexes"""
        service = CacheService()

        # Test avec objets datetime et autres types complexes
        dt = datetime(2023, 1, 1)
        key = service._generate_key("complex_func", (dt, [1, 2, 3]), {"nested": {"key": "value"}})

        assert key.startswith("consultator:complex_func:")
        # Vérifier que c'est un hash SHA-256 (64 caractères hex)
        hash_part = key.split(":")[-1]
        assert len(hash_part) == 64
        assert hash_part.isalnum()

    def test_is_expired(self):
        """Test de vérification d'expiration"""
        service = CacheService()

        # Entrée non expirée
        future_time = time.time() + 100
        entry_valid = {"expires_at": future_time}
        assert not service._is_expired(entry_valid)

        # Entrée expirée
        past_time = time.time() - 100
        entry_expired = {"expires_at": past_time}
        assert service._is_expired(entry_expired)

    def test_get_from_memory_cache(self):
        """Test de récupération depuis le cache mémoire"""
        service = CacheService()
        service.redis_client = None  # Désactiver Redis

        # Test cache vide
        assert service.get("nonexistent") is None

        # Ajouter une entrée
        service.memory_cache["test_key"] = {
            "data": "test_value",
            "expires_at": time.time() + 100,
        }

        # Récupérer l'entrée
        result = service.get("test_key")
        assert result == "test_value"

    def test_get_expired_from_memory_cache(self):
        """Test de récupération d'une entrée expirée du cache mémoire"""
        service = CacheService()
        service.redis_client = None

        # Ajouter une entrée expirée
        service.memory_cache["expired_key"] = {
            "data": "expired_value",
            "expires_at": time.time() - 100,
        }

        # Récupérer devrait retourner None et supprimer l'entrée
        result = service.get("expired_key")
        assert result is None
        assert "expired_key" not in service.memory_cache

    def test_get_from_redis_cache(self):
        """Test de récupération depuis Redis"""
        service = CacheService()
        mock_redis = Mock()
        service.redis_client = mock_redis

        # Simuler Redis avec données
        mock_redis.get.return_value = json.dumps("redis_value")

        result = service.get("redis_key")
        assert result == "redis_value"
        mock_redis.get.assert_called_once_with("redis_key")

    def test_get_from_redis_with_error(self):
        """Test de récupération depuis Redis avec erreur"""
        service = CacheService()
        mock_redis = Mock()
        mock_redis.get.side_effect = Exception("Redis error")
        service.redis_client = mock_redis

        # Fallback vers cache mémoire vide
        service.memory_cache["memory_key"] = {
            "data": "memory_value",
            "expires_at": time.time() + 100,
        }

        # Redis échoue, fallback vers mémoire
        result = service.get("memory_key")
        assert result == "memory_value"

    def test_set_in_cache(self):
        """Test de stockage dans le cache"""
        service = CacheService()
        mock_redis = Mock()
        service.redis_client = mock_redis

        # Stocker une valeur
        result = service.set("test_key", "test_value", ttl=120)

        assert result is True
        assert "test_key" in service.memory_cache

        # Vérifier la structure de l'entrée mémoire
        entry = service.memory_cache["test_key"]
        assert entry["data"] == "test_value"
        assert entry["expires_at"] > time.time()
        assert entry["created_at"] <= time.time()

        # Vérifier l'appel Redis
        mock_redis.setex.assert_called_once_with("test_key", 120, '"test_value"')

    def test_set_with_default_ttl(self):
        """Test de stockage avec TTL par défaut"""
        service = CacheService(default_ttl=500)
        service.redis_client = None

        service.set("test_key", "test_value")

        entry = service.memory_cache["test_key"]
        expected_expiry = entry["created_at"] + 500
        assert abs(entry["expires_at"] - expected_expiry) < 1  # Tolérance d'1 seconde

    def test_delete_from_cache(self):
        """Test de suppression du cache"""
        service = CacheService()
        mock_redis = Mock()
        service.redis_client = mock_redis

        # Ajouter des données dans les deux caches
        service.memory_cache["test_key"] = {
            "data": "value",
            "expires_at": time.time() + 100,
        }
        mock_redis.delete.return_value = 1

        # Supprimer
        result = service.delete("test_key")

        assert result is True
        assert "test_key" not in service.memory_cache
        mock_redis.delete.assert_called_once_with("test_key")

    def test_delete_nonexistent_key(self):
        """Test de suppression d'une clé inexistante"""
        service = CacheService()
        mock_redis = Mock()
        service.redis_client = mock_redis

        mock_redis.delete.return_value = 0

        result = service.delete("nonexistent")

        assert result is True  # True car on considère que l'opération a réussi
        mock_redis.delete.assert_called_once_with("nonexistent")

    def test_clear_pattern(self):
        """Test de suppression par pattern"""
        service = CacheService()
        mock_redis = Mock()
        service.redis_client = mock_redis

        # Simuler des clés Redis
        mock_redis.keys.return_value = ["consultator:user:1", "consultator:user:2"]
        mock_redis.delete.return_value = 2

        # Ajouter des clés en mémoire
        service.memory_cache.update(
            {
                "consultator:user:1": {
                    "data": "value1",
                    "expires_at": time.time() + 100,
                },
                "consultator:post:1": {
                    "data": "value2",
                    "expires_at": time.time() + 100,
                },
                "consultator:user:2": {
                    "data": "value3",
                    "expires_at": time.time() + 100,
                },
            }
        )

        # Supprimer avec pattern
        deleted_count = service.clear_pattern("consultator:user:*")

        assert deleted_count == 4  # 2 de Redis + 2 de mémoire
        assert "consultator:user:1" not in service.memory_cache
        assert "consultator:user:2" not in service.memory_cache
        assert "consultator:post:1" in service.memory_cache  # Ne correspond pas au pattern

    def test_get_stats_without_redis(self):
        """Test des statistiques sans Redis"""
        service = CacheService()
        service.redis_client = None

        # Ajouter des données en mémoire
        service.memory_cache = {
            "key1": {"data": "value1", "expires_at": time.time() + 100},
            "key2": {"data": "value2", "expires_at": time.time() + 100},
        }

        stats = service.get_stats()

        assert stats["memory_cache"]["entries"] == 2
        assert stats["memory_cache"]["estimated_size_kb"] > 0
        assert stats["redis"]["connected"] is False
        assert "Redis non installé" in stats["redis"]["reason"]

    def test_get_stats_with_redis(self):
        """Test des statistiques avec Redis"""
        service = CacheService()
        mock_redis = Mock()
        mock_redis.info.return_value = {
            "used_memory_human": "1.2M",
            "connected_clients": 5,
            "uptime_in_days": 7,
        }
        service.redis_client = mock_redis

        service.memory_cache = {"key1": {"data": "value1", "expires_at": time.time() + 100}}

        stats = service.get_stats()

        assert stats["memory_cache"]["entries"] == 1
        assert stats["redis"]["connected"] is True
        assert stats["redis"]["used_memory_human"] == "1.2M"
        assert stats["redis"]["connected_clients"] == 5
        assert stats["redis"]["uptime_days"] == 7

    def test_get_stats_with_redis_error(self):
        """Test des statistiques avec erreur Redis"""
        service = CacheService()
        mock_redis = Mock()
        mock_redis.info.side_effect = Exception("Redis error")
        service.redis_client = mock_redis

        stats = service.get_stats()

        assert stats["redis"]["connected"] is False
        assert "Redis error" in stats["redis"]["error"]


class TestGlobalCacheService:
    """Tests pour les fonctions globales du service de cache"""

    def test_get_cache_service_singleton(self):
        """Test que get_cache_service retourne toujours la même instance"""
        # Reset global state
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service1 = get_cache_service()
        service2 = get_cache_service()

        assert service1 is service2
        assert isinstance(service1, CacheService)


class TestCacheDecorator:
    """Tests pour le décorateur cached"""

    def test_cached_decorator_basic(self):
        """Test du décorateur cached de base"""
        service = CacheService()
        service.redis_client = None

        call_count = 0

        @cached(ttl=60)
        def test_function(x, y=10):
            nonlocal call_count
            call_count += 1
            return x + y

        # Premier appel - devrait exécuter la fonction
        result1 = test_function(5, 15)
        assert result1 == 20
        assert call_count == 1

        # Deuxième appel avec mêmes arguments - devrait utiliser le cache
        result2 = test_function(5, 15)
        assert result2 == 20
        assert call_count == 1  # Fonction pas appelée à nouveau

        # Appel avec arguments différents - devrait exécuter la fonction
        result3 = test_function(10, 15)
        assert result3 == 25
        assert call_count == 2

    def test_cached_decorator_with_key_prefix(self):
        """Test du décorateur avec préfixe de clé"""
        # Reset global cache service
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service = get_cache_service()
        service.redis_client = None

        @cached(ttl=60, key_prefix="test")
        def test_function(x):
            return x * 2

        test_function(5)

        # Vérifier que la clé contient le préfixe
        cache_keys = list(service.memory_cache.keys())
        assert len(cache_keys) == 1
        assert cache_keys[0].startswith("consultator:test:test_function:")

    def test_cached_decorator_with_complex_args(self):
        """Test du décorateur avec arguments complexes"""
        service = CacheService()
        service.redis_client = None

        @cached(ttl=30)
        def complex_function(data, multiplier=1):
            return [x * multiplier for x in data]

        result1 = complex_function([1, 2, 3], multiplier=2)
        result2 = complex_function([1, 2, 3], multiplier=2)  # Cache hit

        assert result1 == [2, 4, 6]
        assert result2 == [2, 4, 6]


class TestCacheInvalidation:
    """Tests pour les fonctions d'invalidation de cache"""

    def test_invalidate_cache(self):
        """Test de la fonction invalidate_cache"""
        # Reset global cache service
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service = get_cache_service()
        service.redis_client = None

        # Ajouter des données
        service.memory_cache.update(
            {
                "consultator:user:1": {
                    "data": "user1",
                    "expires_at": time.time() + 100,
                },
                "consultator:user:2": {
                    "data": "user2",
                    "expires_at": time.time() + 100,
                },
                "consultator:post:1": {
                    "data": "post1",
                    "expires_at": time.time() + 100,
                },
            }
        )

        # Invalider avec pattern
        deleted = invalidate_cache("consultator:user:*")

        assert deleted == 2
        assert "consultator:user:1" not in service.memory_cache
        assert "consultator:user:2" not in service.memory_cache
        assert "consultator:post:1" in service.memory_cache

    def test_invalidate_consultant_cache_all(self):
        """Test d'invalidation de tout le cache consultant"""
        # Reset global cache service
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service = get_cache_service()
        service.redis_client = None

        service.memory_cache.update(
            {
                "consultator:get_consultant:1": {
                    "data": "consultant1",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_consultant:2": {
                    "data": "consultant2",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_mission:1": {
                    "data": "mission1",
                    "expires_at": time.time() + 100,
                },
            }
        )

        invalidate_consultant_cache()

        assert "consultator:get_consultant:1" not in service.memory_cache
        assert "consultator:get_consultant:2" not in service.memory_cache
        assert "consultator:get_mission:1" in service.memory_cache  # Ne devrait pas être supprimé

    def test_invalidate_consultant_cache_specific(self):
        """Test d'invalidation du cache pour un consultant spécifique"""
        # Reset global cache service
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service = get_cache_service()
        service.redis_client = None

        service.memory_cache.update(
            {
                "consultator:get_consultant:1:abc123": {
                    "data": "consultant1",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_consultant:2:def456": {
                    "data": "consultant2",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_mission:1:xyz789": {
                    "data": "mission1",
                    "expires_at": time.time() + 100,
                },
            }
        )

        invalidate_consultant_cache(consultant_id=1)

        assert "consultator:get_consultant:1:abc123" not in service.memory_cache
        assert "consultator:get_consultant:2:def456" in service.memory_cache
        assert "consultator:get_mission:1:xyz789" in service.memory_cache

    def test_invalidate_mission_cache(self):
        """Test d'invalidation du cache des missions"""
        # Reset global cache service
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service = get_cache_service()
        service.redis_client = None

        service.memory_cache.update(
            {
                "consultator:get_mission:1:abc123": {
                    "data": "mission1",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_mission:2:def456": {
                    "data": "mission2",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_consultant:1:xyz789": {
                    "data": "consultant1",
                    "expires_at": time.time() + 100,
                },
            }
        )

        invalidate_mission_cache()

        assert "consultator:get_mission:1:abc123" not in service.memory_cache
        assert "consultator:get_mission:2:def456" not in service.memory_cache
        assert "consultator:get_consultant:1:xyz789" in service.memory_cache

    def test_invalidate_practice_cache(self):
        """Test d'invalidation du cache des practices"""
        # Reset global cache service
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service = get_cache_service()
        service.redis_client = None

        service.memory_cache.update(
            {
                "consultator:get_practice:1": {
                    "data": "practice1",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_practice:2": {
                    "data": "practice2",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_consultant:1": {
                    "data": "consultant1",
                    "expires_at": time.time() + 100,
                },
            }
        )

        invalidate_practice_cache()

        assert "consultator:get_practice:1" not in service.memory_cache
        assert "consultator:get_practice:2" not in service.memory_cache
        assert "consultator:get_consultant:1" in service.memory_cache

    def test_invalidate_search_cache(self):
        """Test d'invalidation du cache de recherche"""
        # Reset global cache service
        import app.services.cache_service

        app.services.cache_service._cache_service = None

        service = get_cache_service()
        service.redis_client = None

        service.memory_cache.update(
            {
                "consultator:search_consultants:abc123": {
                    "data": "search1",
                    "expires_at": time.time() + 100,
                },
                "consultator:search_consultants:def456": {
                    "data": "search2",
                    "expires_at": time.time() + 100,
                },
                "consultator:get_consultant:1": {
                    "data": "consultant1",
                    "expires_at": time.time() + 100,
                },
            }
        )

        invalidate_search_cache()

        assert "consultator:search_consultants:abc123" not in service.memory_cache
        assert "consultator:search_consultants:def456" not in service.memory_cache
        assert "consultator:get_consultant:1" in service.memory_cache


class TestCachedFunctions:
    """Tests pour les fonctions mises en cache"""

    @patch("app.services.cache_service.get_cache_service")
    def test_get_cached_consultant_stats(self, mock_get_service):
        """Test de la fonction get_cached_consultant_stats"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service

        mock_stats = {"total": 100, "active": 80}
        mock_service.get.return_value = None  # Cache miss

        with patch(
            "app.services.consultant_service.ConsultantService.get_consultant_summary_stats"
        ) as mock_consultant_service:
            mock_consultant_service.return_value = mock_stats

            result = get_cached_consultant_stats()

            assert result == mock_stats
            mock_consultant_service.assert_called_once()

            # Deuxième appel - devrait utiliser le cache
            result2 = get_cached_consultant_stats()
            assert result2 == mock_stats
            mock_service.get.assert_called()

    @patch("app.services.cache_service.get_cache_service")
    def test_get_cached_consultants_list(self, mock_get_service):
        """Test de la fonction get_cached_consultants_list"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service

        mock_consultants = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
        mock_service.get.return_value = None  # Cache miss

        with patch(
            "app.services.consultant_service.ConsultantService.get_all_consultants_with_stats"
        ) as mock_consultant_service:
            mock_consultant_service.return_value = mock_consultants

            result = get_cached_consultants_list(page=1, per_page=50)

            assert result == mock_consultants
            mock_consultant_service.assert_called_once_with(1, 50)

    @patch("app.services.cache_service.get_cache_service")
    def test_get_cached_search_results(self, mock_get_service):
        """Test de la fonction get_cached_search_results"""
        mock_service = Mock()
        mock_get_service.return_value = mock_service

        mock_results = [{"id": 1, "name": "John Doe"}]
        mock_service.get.return_value = None  # Cache miss

        with patch("app.services.consultant_service.ConsultantService.search_consultants_optimized") as mock_search:
            mock_search.return_value = mock_results

            result = get_cached_search_results("John", page=1, per_page=20)

            assert result == mock_results
            mock_search.assert_called_once_with("John", 1, 20)


if __name__ == "__main__":
    pytest.main([__file__])
