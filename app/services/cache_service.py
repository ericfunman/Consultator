"""
Service de cache avancé pour Consultator
Système de cache multi-niveaux avec Redis et cache en mémoire
Optimisé pour les requêtes fréquentes de consultants et missions
"""

import hashlib
import json
import time
from datetime import datetime
from datetime import timedelta
from functools import wraps
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None


class CacheService:
    """Service de cache multi-niveaux pour optimiser les performances"""

    def __init__(self, redis_url: str = "redis://localhost:6379/0", default_ttl: int = 300):
        """
        Initialise le service de cache

        Args:
            redis_url: URL de connexion Redis
            default_ttl: TTL par défaut en secondes (5 minutes)
        """
        self.default_ttl = default_ttl
        self.redis_client = None
        self.memory_cache: Dict[str, Dict[str, Any]] = {}

        # Initialiser Redis si disponible
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(redis_url)
                # Test de connexion
                self.redis_client.ping()
                print("✅ Redis connecté avec succès")
            except Exception as e:
                print(f"⚠️ Redis non disponible: {e}")
                self.redis_client = None
        else:
            print("ℹ️ Redis non installé, utilisation du cache mémoire uniquement")

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Génère une clé de cache unique basée sur la fonction et ses arguments"""
        # Convertir les arguments en string JSON
        args_str = json.dumps(args, default=str, sort_keys=True)
        kwargs_str = json.dumps(kwargs, default=str, sort_keys=True)

        # Créer un hash unique avec SHA-256 (plus sécurisé que MD5)
        key_content = f"{func_name}:{args_str}:{kwargs_str}"
        key_hash = hashlib.sha256(key_content.encode()).hexdigest()

        return f"consultator:{func_name}:{key_hash}"

    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """Vérifie si une entrée de cache a expiré"""
        return time.time() > cache_entry.get("expires_at", 0)

    def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        # Essayer Redis d'abord
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                print(f"⚠️ Erreur Redis GET: {e}")

        # Fallback vers le cache mémoire
        if key in self.memory_cache:
            cache_entry = self.memory_cache[key]
            if not self._is_expired(cache_entry):
                return cache_entry["data"]
            else:
                # Supprimer l'entrée expirée
                del self.memory_cache[key]

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Stocke une valeur dans le cache"""
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl

        cache_entry = {
            "data": value,
            "expires_at": expires_at,
            "created_at": time.time(),
        }

        # Stocker dans Redis
        if self.redis_client:
            try:
                self.redis_client.setex(key, ttl, json.dumps(value, default=str))
            except Exception as e:
                print(f"⚠️ Erreur Redis SET: {e}")

        # Stocker dans le cache mémoire
        self.memory_cache[key] = cache_entry

        return True

    def delete(self, key: str) -> bool:
        """Supprime une clé du cache"""
        deleted = False

        # Supprimer de Redis
        if self.redis_client:
            try:
                self.redis_client.delete(key)
                deleted = True
            except Exception as e:
                print(f"⚠️ Erreur Redis DELETE: {e}")

        # Supprimer du cache mémoire
        if key in self.memory_cache:
            del self.memory_cache[key]
            deleted = True

        return deleted

    def clear_pattern(self, pattern: str) -> int:
        """Supprime toutes les clés correspondant à un pattern"""
        deleted_count = 0

        # Supprimer de Redis
        if self.redis_client:
            try:
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
                    deleted_count += len(keys)
            except Exception as e:
                print(f"⚠️ Erreur Redis CLEAR: {e}")

        # Supprimer du cache mémoire
        import fnmatch

        keys_to_delete = [k for k in self.memory_cache.keys() if fnmatch.fnmatch(k, pattern)]
        for key in keys_to_delete:
            del self.memory_cache[key]
            deleted_count += 1

        return deleted_count

    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        memory_entries = len(self.memory_cache)
        memory_size = sum(len(str(entry)) for entry in self.memory_cache.values())

        stats = {
            "memory_cache": {
                "entries": memory_entries,
                "estimated_size_kb": memory_size / 1024,
                "hit_rate": 0,  # À implémenter avec des compteurs
            }
        }

        if self.redis_client:
            try:
                redis_info = self.redis_client.info()
                stats["redis"] = {
                    "connected": True,
                    "used_memory_human": redis_info.get("used_memory_human", "N/A"),
                    "connected_clients": redis_info.get("connected_clients", 0),
                    "uptime_days": redis_info.get("uptime_in_days", 0),
                }
            except Exception as e:
                stats["redis"] = {"connected": False, "error": str(e)}
        else:
            stats["redis"] = {"connected": False, "reason": "Redis non installé"}

        return stats


# Instance globale du service de cache
_cache_service = None


def get_cache_service() -> CacheService:
    """Retourne l'instance globale du service de cache"""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service


def cached(ttl: Optional[int] = None, key_prefix: str = ""):
    """
    Décorateur pour mettre en cache le résultat d'une fonction

    Args:
        ttl: Time To Live en secondes (utilise la valeur par défaut si None)
        key_prefix: Préfixe pour la clé de cache
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_service = get_cache_service()

            # Générer la clé de cache
            func_name = f"{key_prefix}:{func.__name__}" if key_prefix else func.__name__
            cache_key = cache_service._generate_key(func_name, args, kwargs)

            # Essayer de récupérer du cache
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Exécuter la fonction
            result = func(*args, **kwargs)

            # Mettre en cache le résultat
            cache_service.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator


def invalidate_cache(pattern: str):
    """Invalide toutes les clés de cache correspondant à un pattern"""
    cache_service = get_cache_service()
    return cache_service.clear_pattern(pattern)


# Fonctions utilitaires pour l'invalidation de cache
def invalidate_consultant_cache(consultant_id: Optional[int] = None):
    """Invalide le cache des consultants"""
    if consultant_id:
        invalidate_cache(f"consultator:*consultant*{consultant_id}*")
    else:
        invalidate_cache("consultator:*consultant*")


def invalidate_mission_cache(consultant_id: Optional[int] = None):
    """Invalide le cache des missions"""
    if consultant_id:
        invalidate_cache(f"consultator:*mission*{consultant_id}*")
    else:
        invalidate_cache("consultator:*mission*")


def invalidate_practice_cache():
    """Invalide le cache des practices"""
    invalidate_cache("consultator:*practice*")


def invalidate_search_cache():
    """Invalide le cache des recherches"""
    invalidate_cache("consultator:*search*")


# Cache pour les statistiques globales
@cached(ttl=60)  # Cache 1 minute pour les stats
def get_cached_consultant_stats():
    """Cache les statistiques des consultants"""
    from app.services.consultant_service import ConsultantService

    return ConsultantService.get_consultant_summary_stats()


@cached(ttl=300)  # Cache 5 minutes pour les listes
def get_cached_consultants_list(page: int = 1, per_page: int = 50):
    """Cache la liste des consultants"""
    from app.services.consultant_service import ConsultantService

    return ConsultantService.get_all_consultants_with_stats(page, per_page)


@cached(ttl=60)  # Cache 1 minute pour les recherches
def get_cached_search_results(search_term: str, page: int = 1, per_page: int = 50):
    """Cache les résultats de recherche"""
    from app.services.consultant_service import ConsultantService

    return ConsultantService.search_consultants_optimized(search_term, page, per_page)
