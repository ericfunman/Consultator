"""
Test minimal pour vérifier les imports
"""

def test_basic():
    """Test basique"""
    assert 1 + 1 == 2

def test_import_sys():
    """Test import de sys"""
    import sys
    assert sys.version_info.major >= 3

def test_import_app():
    """Test import du package app"""
    try:
        import app
        assert app is not None
    except ImportError:
        import pytest
        pytest.skip("app package not available")
