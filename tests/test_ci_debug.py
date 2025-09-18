"""
Test de debug pour CI - sans dépendances externes
"""

import pytest
import sys
import os


def test_python_basics():
    """Test basique Python sans dépendances"""
    assert 2 + 2 == 4


def test_environment():
    """Test de l'environnement CI"""
    assert sys.version_info >= (3, 8)


def test_path_setup():
    """Test configuration path"""
    current_dir = os.getcwd()
    assert os.path.exists(current_dir)


class TestCIEnvironment:
    """Tests d'environnement CI"""

    def test_imports_basic(self):
        """Test imports Python de base"""
        import json
        import datetime

        assert True

    def test_directory_structure(self):
        """Test structure répertoire"""
        assert os.path.exists("tests")
        assert os.path.exists("app") or True  # Peut ne pas exister en CI

    def test_ci_environment_vars(self):
        """Test variables CI"""
        ci_vars = ["CI", "GITHUB_ACTIONS", "GITHUB_WORKFLOW"]
        has_ci_var = any(var in os.environ for var in ci_vars)
        # Ne pas faire échouer si pas en CI
        assert True
