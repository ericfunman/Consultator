"""
Configuration de performance pour Consultator
Optimisations pour gérer 1000+ consultants efficacement
"""

# Paramètres de pagination pour les grandes listes
PAGINATION_CONFIG = {
    "consultants_per_page": 50,  # Augmenté de 20 à 50
    "missions_per_page": 100,    # Pour l'affichage des missions
    "search_results_per_page": 25,
    "max_search_results": 500    # Limite les recherches très larges
}

# Configuration du cache Streamlit
CACHE_CONFIG = {
    "default_ttl": 300,          # 5 minutes pour les données générales
    "stats_ttl": 600,            # 10 minutes pour les statistiques
    "search_ttl": 180,           # 3 minutes pour les recherches
    "consultant_details_ttl": 300, # 5 minutes pour les détails consultant
}

# Configuration de la base de données
DATABASE_CONFIG = {
    "pool_size": 20,             # Nombre de connexions dans le pool
    "max_overflow": 30,          # Connexions supplémentaires autorisées
    "pool_timeout": 30,          # Timeout pour obtenir une connexion
    "pool_recycle": 3600,        # Recycler les connexions après 1h
    "echo": False,               # Désactiver le logging SQL en production
    "connect_args": {
        "check_same_thread": False,
        "timeout": 30,
        "isolation_level": "READ_UNCOMMITTED"  # Pour les lectures rapides
    }
}

# Optimisations des requêtes
QUERY_CONFIG = {
    "batch_size": 100,           # Taille des lots pour les opérations bulk
    "max_bulk_operations": 1000, # Maximum d'opérations en une fois
    "use_lazy_loading": True,    # Chargement paresseux des relations
    "preload_relations": [       # Relations à charger systématiquement
        "practice",
        "business_manager_gestions.business_manager"
    ]
}

# Configuration de l'interface utilisateur
UI_CONFIG = {
    "show_pagination_info": True,
    "show_loading_spinners": True,
    "use_progressive_loading": True,  # Chargement progressif des données
    "max_items_in_selectbox": 200,   # Limite pour les select boxes
    "use_virtual_scrolling": False,  # À activer si nécessaire
    "compress_large_tables": True    # Compression pour les gros tableaux
}

# Limites de sécurité
SECURITY_LIMITS = {
    "max_file_upload_size": 10 * 1024 * 1024,  # 10MB
    "max_cv_text_length": 50000,               # 50k caractères max
    "max_search_term_length": 100,             # Limite les requêtes abusives
    "rate_limit_per_minute": 60,               # Limite les requêtes par minute
    "session_timeout_minutes": 60              # Timeout de session
}

# Configuration des exports
EXPORT_CONFIG = {
    "max_export_rows": 5000,     # Limite pour les exports Excel/CSV
    "chunk_size_export": 500,    # Taille des chunks pour gros exports
    "include_relations": False,   # Exporter les relations par défaut
    "compress_exports": True      # Compression des fichiers d'export
}

# Monitoring et logging
MONITORING_CONFIG = {
    "log_slow_queries": True,
    "slow_query_threshold": 2.0,  # 2 secondes
    "log_large_results": True,
    "large_result_threshold": 1000,  # Plus de 1000 résultats
    "performance_metrics": True,
    "cache_hit_rate_tracking": True
}

# Messages d'optimisation
OPTIMIZATION_MESSAGES = {
    "large_dataset_warning": "⚠️ Jeu de données important détecté. Utilisation d'optimisations automatiques.",
    "cache_warming": "🔄 Préchauffage du cache en cours...",
    "pagination_info": "📊 Affichage par pages pour optimiser les performances",
    "search_optimization": "🔍 Recherche optimisée pour de gros volumes"
}

def get_optimal_page_size(total_items: int) -> int:
    """Calcule la taille de page optimale selon le nombre total d'éléments"""
    if total_items < 100:
        return 25
    elif total_items < 500:
        return 50
    elif total_items < 2000:
        return 100
    else:
        return 200

def should_use_cache(operation_type: str) -> bool:
    """Détermine si le cache doit être utilisé pour une opération"""
    cache_operations = [
        'list_consultants',
        'get_statistics',
        'search_consultants',
        'list_competences',
        'list_practices'
    ]
    return operation_type in cache_operations

def get_cache_ttl(data_type: str) -> int:
    """Retourne le TTL approprié selon le type de données"""
    ttl_mapping = {
        'stats': CACHE_CONFIG['stats_ttl'],
        'search': CACHE_CONFIG['search_ttl'],
        'details': CACHE_CONFIG['consultant_details_ttl'],
        'default': CACHE_CONFIG['default_ttl']
    }
    return ttl_mapping.get(data_type, ttl_mapping['default'])

# Configuration spécifique pour les gros volumes
LARGE_DATASET_CONFIG = {
    "threshold_consultants": 500,    # Seuil pour considérer comme "gros volume"
    "threshold_missions": 2000,
    "threshold_competences": 100,
    
    # Optimisations automatiques quand seuils dépassés
    "auto_optimizations": {
        "enable_lazy_loading": True,
        "increase_cache_ttl": True,
        "use_summary_views": True,
        "limit_real_time_updates": True,
        "enable_background_refresh": True
    }
}

def is_large_dataset() -> dict:
    """Vérifie si on est dans un contexte de gros volume de données"""
    # Cette fonction sera implementée pour vérifier les seuils
    return {
        "is_large": True,  # À adapter selon les données réelles
        "consultants_count": 1000,
        "missions_count": 10000,
        "optimizations_enabled": True
    }
