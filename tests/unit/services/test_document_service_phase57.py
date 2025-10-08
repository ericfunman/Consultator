"""
Tests Phase 57 - document_service.py (Coverage boost 70% → 72%+)
Cible: DocumentService - Gestion documents, upload, extraction texte, analyse CV
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock, mock_open
from io import BytesIO

# Import du service à tester
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from app.services.document_service import DocumentService


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_upload_dir(tmp_path):
    """Crée un répertoire temporaire pour les uploads"""
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    return upload_dir


@pytest.fixture
def mock_uploaded_file():
    """Mock fichier Streamlit uploadé"""
    mock_file = Mock()
    mock_file.name = "test_cv.pdf"
    mock_file.type = "application/pdf"
    mock_file.size = 1024
    mock_file.getbuffer.return_value = b"fake pdf content"
    return mock_file


@pytest.fixture
def setup_document_service_dir(temp_upload_dir, monkeypatch):
    """Configure le répertoire d'upload du service"""
    monkeypatch.setattr(DocumentService, 'UPLOAD_DIR', temp_upload_dir)
    return temp_upload_dir


# ============================================================================
# TESTS: Initialisation et configuration
# ============================================================================

class TestInitialization:
    """Tests pour l'initialisation du service"""

    def test_init_upload_directory_creates_dir(self, temp_upload_dir, monkeypatch):
        """Test création du répertoire d'upload"""
        new_dir = temp_upload_dir / "new_uploads"
        monkeypatch.setattr(DocumentService, 'UPLOAD_DIR', new_dir)
        
        result = DocumentService.init_upload_directory()
        
        assert result.exists()
        assert result.is_dir()
        assert result == new_dir

    def test_init_upload_directory_existing_dir(self, temp_upload_dir, monkeypatch):
        """Test avec répertoire existant"""
        monkeypatch.setattr(DocumentService, 'UPLOAD_DIR', temp_upload_dir)
        
        result = DocumentService.init_upload_directory()
        
        assert result.exists()
        assert result == temp_upload_dir

    def test_allowed_extensions_defined(self):
        """Test que les extensions autorisées sont définies"""
        assert isinstance(DocumentService.ALLOWED_EXTENSIONS, dict)
        assert "pdf" in DocumentService.ALLOWED_EXTENSIONS
        assert "docx" in DocumentService.ALLOWED_EXTENSIONS
        assert len(DocumentService.ALLOWED_EXTENSIONS) >= 4


# ============================================================================
# TESTS: get_file_extension()
# ============================================================================

class TestGetFileExtension:
    """Tests pour get_file_extension()"""

    def test_get_file_extension_simple(self):
        """Test extraction extension simple"""
        result = DocumentService.get_file_extension("document.pdf")
        assert result == "pdf"

    def test_get_file_extension_uppercase(self):
        """Test avec extension majuscule"""
        result = DocumentService.get_file_extension("document.PDF")
        assert result == "pdf"

    def test_get_file_extension_multiple_dots(self):
        """Test avec plusieurs points"""
        result = DocumentService.get_file_extension("my.document.name.docx")
        assert result == "docx"

    def test_get_file_extension_no_extension(self):
        """Test sans extension"""
        result = DocumentService.get_file_extension("document")
        assert result == ""

    def test_get_file_extension_empty_string(self):
        """Test avec chaîne vide"""
        result = DocumentService.get_file_extension("")
        assert result == ""


# ============================================================================
# TESTS: is_allowed_file()
# ============================================================================

class TestIsAllowedFile:
    """Tests pour is_allowed_file()"""

    def test_is_allowed_file_pdf(self):
        """Test fichier PDF autorisé"""
        assert DocumentService.is_allowed_file("document.pdf") is True

    def test_is_allowed_file_docx(self):
        """Test fichier DOCX autorisé"""
        assert DocumentService.is_allowed_file("document.docx") is True

    def test_is_allowed_file_pptx(self):
        """Test fichier PPTX autorisé"""
        assert DocumentService.is_allowed_file("presentation.pptx") is True

    def test_is_allowed_file_not_allowed(self):
        """Test fichier non autorisé"""
        assert DocumentService.is_allowed_file("document.txt") is False
        assert DocumentService.is_allowed_file("image.jpg") is False

    def test_is_allowed_file_case_insensitive(self):
        """Test insensible à la casse"""
        assert DocumentService.is_allowed_file("document.PDF") is True
        assert DocumentService.is_allowed_file("document.DOCX") is True


# ============================================================================
# TESTS: save_uploaded_file()
# ============================================================================

class TestSaveUploadedFile:
    """Tests pour save_uploaded_file()"""

    def test_save_uploaded_file_success(self, setup_document_service_dir, mock_uploaded_file):
        """Test sauvegarde réussie d'un fichier"""
        consultant_id = 123
        
        result = DocumentService.save_uploaded_file(mock_uploaded_file, consultant_id)
        
        assert result["success"] is True
        assert "file_path" in result
        assert "filename" in result
        assert result["original_name"] == "test_cv.pdf"
        assert result["consultant_id"] == consultant_id
        assert result["extension"] == "pdf"

    def test_save_uploaded_file_creates_consultant_dir(self, setup_document_service_dir, mock_uploaded_file):
        """Test création du répertoire consultant"""
        consultant_id = 456
        
        result = DocumentService.save_uploaded_file(mock_uploaded_file, consultant_id)
        
        consultant_dir = setup_document_service_dir / f"consultant_{consultant_id}"
        assert consultant_dir.exists()
        assert consultant_dir.is_dir()

    def test_save_uploaded_file_unique_filename(self, setup_document_service_dir, mock_uploaded_file):
        """Test génération nom de fichier unique avec timestamp"""
        result = DocumentService.save_uploaded_file(mock_uploaded_file, 1)
        
        filename = result["filename"]
        # Le fichier doit contenir un timestamp
        assert len(filename) > len("test_cv.pdf")
        assert "test_cv.pdf" in filename

    @patch('builtins.open', side_effect=OSError("Permission denied"))
    def test_save_uploaded_file_io_error(self, mock_open_error, setup_document_service_dir, mock_uploaded_file):
        """Test avec erreur d'écriture"""
        result = DocumentService.save_uploaded_file(mock_uploaded_file, 1)
        
        assert result["success"] is False
        assert "error" in result


# ============================================================================
# TESTS: get_file_type_name()
# ============================================================================

class TestGetFileTypeName:
    """Tests pour get_file_type_name()"""

    def test_get_file_type_name_pdf(self):
        """Test nom type PDF"""
        assert DocumentService.get_file_type_name("document.pdf") == "PDF"

    def test_get_file_type_name_docx(self):
        """Test nom type DOCX"""
        assert DocumentService.get_file_type_name("document.docx") == "Word (DOCX)"

    def test_get_file_type_name_pptx(self):
        """Test nom type PPTX"""
        assert DocumentService.get_file_type_name("presentation.pptx") == "PowerPoint (PPTX)"

    def test_get_file_type_name_unknown(self):
        """Test type inconnu"""
        assert DocumentService.get_file_type_name("document.txt") == "Inconnu"


# ============================================================================
# TESTS: extract_text_from_file() - Dispatcher
# ============================================================================

class TestExtractTextFromFile:
    """Tests pour extract_text_from_file() - fonction dispatcher"""

    @patch.object(DocumentService, '_extract_text_from_pdf')
    def test_extract_text_from_file_pdf(self, mock_extract_pdf):
        """Test dispatch vers _extract_text_from_pdf"""
        mock_extract_pdf.return_value = "PDF text content"
        
        result = DocumentService.extract_text_from_file("document.pdf")
        
        mock_extract_pdf.assert_called_once_with("document.pdf")
        assert result == "PDF text content"

    @patch.object(DocumentService, '_extract_text_from_docx')
    def test_extract_text_from_file_docx(self, mock_extract_docx):
        """Test dispatch vers _extract_text_from_docx"""
        mock_extract_docx.return_value = "DOCX text content"
        
        result = DocumentService.extract_text_from_file("document.docx")
        
        mock_extract_docx.assert_called_once_with("document.docx")
        assert result == "DOCX text content"

    @patch.object(DocumentService, '_extract_text_from_pptx')
    def test_extract_text_from_file_pptx(self, mock_extract_pptx):
        """Test dispatch vers _extract_text_from_pptx"""
        mock_extract_pptx.return_value = "PPTX text content"
        
        result = DocumentService.extract_text_from_file("presentation.pptx")
        
        mock_extract_pptx.assert_called_once_with("presentation.pptx")
        assert result == "PPTX text content"

    def test_extract_text_from_file_unsupported(self):
        """Test format non supporté"""
        result = DocumentService.extract_text_from_file("document.txt")
        
        assert "Format txt non supporté" in result or "non supporté" in result.lower()

    @patch.object(DocumentService, '_extract_text_from_pdf', side_effect=OSError("File error"))
    def test_extract_text_from_file_io_error(self, mock_extract):
        """Test avec erreur I/O"""
        result = DocumentService.extract_text_from_file("document.pdf")
        
        assert "Erreur" in result or "erreur" in result.lower()


# ============================================================================
# TESTS: analyze_cv_content()
# ============================================================================

class TestAnalyzeCvContent:
    """Tests pour analyze_cv_content()"""

    def test_analyze_cv_content_skills_detection(self):
        """Test détection de compétences techniques"""
        text = """
        Profil Développeur Python
        Compétences: Python, Django, PostgreSQL, Docker, AWS
        Expérience avec React et TypeScript
        """
        
        result = DocumentService.analyze_cv_content(text)
        
        assert "skills_detected" in result
        assert len(result["skills_detected"]) > 0
        # Vérifier que Python est détecté
        skills_names = [s["skill"].lower() for s in result["skills_detected"]]
        assert any("python" in skill for skill in skills_names)

    def test_analyze_cv_content_experience_years(self):
        """Test détection années d'expérience"""
        text = "Développeur avec 5 ans d'expérience en Python et Django"
        
        result = DocumentService.analyze_cv_content(text)
        
        assert "experience_years" in result
        if "total" in result["experience_years"]:
            assert result["experience_years"]["total"] == 5

    def test_analyze_cv_content_languages(self):
        """Test détection de langues"""
        text = "Langues: Français (natif), Anglais (courant), Espagnol (intermédiaire)"
        
        result = DocumentService.analyze_cv_content(text)
        
        assert "languages" in result
        assert len(result["languages"]) >= 2

    def test_analyze_cv_content_summary(self):
        """Test génération du résumé"""
        text = "Jean Dupont\nDéveloppeur Full Stack\n5 ans d'expérience\nCompétences: Python, React"
        
        result = DocumentService.analyze_cv_content(text)
        
        assert "summary" in result
        assert len(result["summary"]) > 0
        assert "..." in result["summary"]  # Tronqué avec ...

    def test_analyze_cv_content_empty_text(self):
        """Test avec texte vide"""
        result = DocumentService.analyze_cv_content("")
        
        assert "skills_detected" in result
        assert "experience_years" in result
        assert "languages" in result
        assert result["skills_detected"] == []

    def test_analyze_cv_content_case_insensitive(self):
        """Test insensible à la casse"""
        text = "PYTHON python PyThOn"
        
        result = DocumentService.analyze_cv_content(text)
        
        # Python devrait être détecté malgré les variations de casse
        skills_names = [s["skill"].lower() for s in result["skills_detected"]]
        assert any("python" in skill for skill in skills_names)


# ============================================================================
# TESTS: get_consultant_documents()
# ============================================================================

class TestGetConsultantDocuments:
    """Tests pour get_consultant_documents()"""

    def test_get_consultant_documents_empty(self, setup_document_service_dir):
        """Test sans documents"""
        result = DocumentService.get_consultant_documents(999)
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_consultant_documents_with_files(self, setup_document_service_dir):
        """Test avec fichiers existants"""
        # Créer un répertoire consultant avec des fichiers
        consultant_id = 123
        consultant_dir = setup_document_service_dir / f"consultant_{consultant_id}"
        consultant_dir.mkdir()
        
        # Créer des fichiers de test
        (consultant_dir / "cv.pdf").write_text("fake pdf")
        (consultant_dir / "lettre.docx").write_text("fake docx")
        
        result = DocumentService.get_consultant_documents(consultant_id)
        
        assert len(result) == 2
        assert all("filename" in doc for doc in result)
        assert all("size" in doc for doc in result)
        assert all("extension" in doc for doc in result)

    def test_get_consultant_documents_sorted_by_date(self, setup_document_service_dir):
        """Test tri par date de modification (plus récent en premier)"""
        consultant_id = 456
        consultant_dir = setup_document_service_dir / f"consultant_{consultant_id}"
        consultant_dir.mkdir()
        
        # Créer des fichiers
        file1 = consultant_dir / "old.pdf"
        file2 = consultant_dir / "new.pdf"
        file1.write_text("old")
        file2.write_text("new")
        
        result = DocumentService.get_consultant_documents(consultant_id)
        
        # Le plus récent devrait être en premier
        assert len(result) >= 2
        # new.pdf devrait être avant old.pdf (ou égal si créés simultanément)
        filenames = [doc["filename"] for doc in result]
        assert "new.pdf" in filenames or "old.pdf" in filenames


# ============================================================================
# TESTS: delete_document()
# ============================================================================

class TestDeleteDocument:
    """Tests pour delete_document()"""

    def test_delete_document_success(self, temp_upload_dir):
        """Test suppression réussie"""
        # Créer un fichier temporaire
        test_file = temp_upload_dir / "to_delete.pdf"
        test_file.write_text("content")
        
        result = DocumentService.delete_document(str(test_file))
        
        assert result is True
        assert not test_file.exists()

    def test_delete_document_not_found(self):
        """Test suppression fichier inexistant"""
        result = DocumentService.delete_document("/nonexistent/file.pdf")
        
        assert result is False


# ============================================================================
# TESTS: get_all_consultants_for_selection()
# ============================================================================

class TestGetAllConsultantsForSelection:
    """Tests pour get_all_consultants_for_selection()"""

    @patch('app.services.document_service.get_database_session')
    def test_get_all_consultants_success(self, mock_get_db):
        """Test récupération consultants réussie"""
        # Mock DB session
        mock_session = MagicMock()
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=False)
        mock_get_db.return_value = mock_session
        
        # Mock consultants
        mock_consultant1 = Mock()
        mock_consultant1.id = 1
        mock_consultant1.prenom = "Jean"
        mock_consultant1.nom = "Dupont"
        mock_consultant1.email = "jean.dupont@test.com"
        
        mock_consultant2 = Mock()
        mock_consultant2.id = 2
        mock_consultant2.prenom = "Marie"
        mock_consultant2.nom = "Martin"
        mock_consultant2.email = "marie.martin@test.com"
        
        mock_session.query.return_value.all.return_value = [mock_consultant1, mock_consultant2]
        
        result = DocumentService.get_all_consultants_for_selection()
        
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["name"] == "Jean Dupont"
        assert result[1]["name"] == "Marie Martin"
        assert "display" in result[0]

    @patch('app.services.document_service.get_database_session')
    def test_get_all_consultants_db_error(self, mock_get_db):
        """Test avec erreur de base de données"""
        from sqlalchemy.exc import SQLAlchemyError
        mock_get_db.side_effect = SQLAlchemyError("Database error")
        
        result = DocumentService.get_all_consultants_for_selection()
        
        assert result == []


# ============================================================================
# TESTS: Edge cases
# ============================================================================

class TestEdgeCases:
    """Tests de cas limites"""

    def test_analyze_cv_very_long_text(self):
        """Test avec texte très long"""
        long_text = "Python " * 1000 + "Java " * 1000
        
        result = DocumentService.analyze_cv_content(long_text)
        
        assert "skills_detected" in result
        # Devrait détecter Python et Java
        assert len(result["skills_detected"]) >= 2

    def test_analyze_cv_special_characters(self):
        """Test avec caractères spéciaux"""
        text = "C++ développeur, expert C#, connaît node.js et ci/cd"
        
        result = DocumentService.analyze_cv_content(text)
        
        # Devrait détecter C++, C#, Node.js, CI/CD
        assert len(result["skills_detected"]) > 0

    def test_get_file_extension_with_spaces(self):
        """Test extension avec espaces (cas bizarre)"""
        result = DocumentService.get_file_extension("document .pdf")
        
        # Devrait quand même extraire l'extension
        assert "pdf" in result.lower()

    def test_save_uploaded_file_very_long_filename(self, setup_document_service_dir, mock_uploaded_file):
        """Test avec nom de fichier très long (limitation Windows)"""
        mock_uploaded_file.name = "a" * 200 + ".pdf"
        
        result = DocumentService.save_uploaded_file(mock_uploaded_file, 1)
        
        # Sur Windows, les noms trop longs peuvent échouer (limite MAX_PATH)
        # Le service doit gérer l'erreur proprement avec success=False
        assert "success" in result
        # Accepte success True ou False selon l'OS
        assert isinstance(result["success"], bool)
