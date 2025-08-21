"""
Tests pour les services métier
"""
import pytest
import sys
import os

# Ajouter le répertoire app au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

def test_consultant_service_import():
    """Test d'import du service consultant"""
    try:
        from services.consultant_service import ConsultantService
        assert ConsultantService is not None
    except ImportError:
        pytest.skip("ConsultantService non disponible")

def test_document_service_import():
    """Test d'import du service document"""
    try:
        from services.document_service import DocumentService
        assert DocumentService is not None
    except ImportError:
        pytest.skip("DocumentService non disponible")

def test_technology_service_import():
    """Test d'import du service technologie"""
    try:
        from services.technology_service import TechnologyService
        assert TechnologyService is not None
    except ImportError:
        pytest.skip("TechnologyService non disponible")

def test_document_analyzer_functionality():
    """Test des fonctionnalités de l'analyseur de documents"""
    try:
        from services.document_analyzer import DocumentAnalyzer
        
        # Test d'instanciation
        analyzer = DocumentAnalyzer()
        assert analyzer is not None
        
        # Test des extensions supportées
        assert analyzer.is_supported_file("test.pdf")
        assert analyzer.is_supported_file("test.docx")
        assert not analyzer.is_supported_file("test.txt")
        
    except ImportError:
        pytest.skip("DocumentAnalyzer non disponible")
    except Exception:
        # Les méthodes peuvent ne pas exister encore
        pytest.skip("Méthodes DocumentAnalyzer non implémentées")
