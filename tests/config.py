"""
Configuration avancée pour les tests de couverture et non-régression

Ce fichier configure pytest avec des plugins et options spécifiques
pour maximiser la couverture de tests.
"""

# Configuration pytest pour les tests de régression
pytest_plugins = [
    "tests.fixtures.base_test",
    "tests.fixtures.database_fixtures",
]

# Markers personnalisés
pytest_markers = [
    "regression: Tests de non-régression critiques",
    "slow: Tests lents à exécuter",
    "integration: Tests d'intégration",
    "unit: Tests unitaires",
    "coverage: Tests pour améliorer la couverture",
    "import: Tests spécifiques à l'import VSA",
    "ui: Tests d'interface utilisateur",
    "performance: Tests de performance",
]

# Configuration de couverture
coverage_config = {
    "source": ["app"],
    "omit": [
        "app/main.py",  # Point d'entrée Streamlit
        "tests/*",
        "*/migrations/*",
        "*/venv/*",
        "*/.venv/*",
        "*/test_*",
    ],
    "exclude_lines": [
        "pragma: no cover",
        "def __repr__",
        "raise AssertionError",
        "raise NotImplementedError",
        "if __name__ == .__main__.:",
        "if TYPE_CHECKING:",
        "class .*Protocol.*:",
        "@abstract",
    ],
    "show_missing": True,
    "precision": 2,
    "fail_under": 80,  # Objectif 80% de couverture minimum
}

# Configuration des tests parallèles
parallel_config = {
    "workers": "auto",  # Utilise tous les cores disponibles
    "dist": "loadfile",  # Distribue par fichier
}

# Timeouts pour éviter les tests qui traînent
timeout_config = {
    "timeout": 300,  # 5 minutes max par test
    "timeout_method": "thread",
}

# Configuration des fixtures de base de données
database_config = {
    "test_database": ":memory:",  # SQLite en mémoire pour les tests
    "isolation_level": "SERIALIZABLE",
    "echo": False,  # True pour debug SQL
}

# Plugins de qualité de code
quality_plugins = [
    "pytest-cov",  # Couverture de code
    "pytest-xdist",  # Tests parallèles
    "pytest-timeout",  # Timeout des tests
    "pytest-mock",  # Mocking avancé
    "pytest-html",  # Rapports HTML
    "pytest-benchmark",  # Tests de performance
    "pytest-faker",  # Génération de données fake
]

# Configuration des rapports
reporting_config = {
    "html_report": "reports/pytest_report.html",
    "coverage_html": "reports/htmlcov",
    "junit_xml": "reports/junit.xml",
    "coverage_xml": "reports/coverage.xml",
}
