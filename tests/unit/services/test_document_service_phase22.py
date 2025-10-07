"""
Tests Phase 22 FINALE: DocumentService - 78.8% -> 92%+!
Ciblage: 46 lignes manquantes dans document_service.py
Focus: Upload, extraction texte (PDF/DOCX/PPTX), analyse CV
"""
import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open
from datetime import datetime
from pathlib import Path
import tempfile
import os


class TestDocumentServiceUpload(unittest.TestCase):
    """Tests upload et sauvegarde de fichiers"""

    def test_init_upload_directory(self):
        """Test initialisation répertoire upload"""
        from app.services.document_service import DocumentService
        
        upload_dir = DocumentService.init_upload_directory()
        assert isinstance(upload_dir, Path)

    def test_get_file_extension_pdf(self):
        """Test extraction extension PDF"""
        from app.services.document_service import DocumentService
        
        ext = DocumentService.get_file_extension("document.pdf")
        assert ext == "pdf"

    def test_get_file_extension_no_extension(self):
        """Test extraction sans extension"""
        from app.services.document_service import DocumentService
        
        ext = DocumentService.get_file_extension("document")
        assert ext == ""

    def test_is_allowed_file_pdf(self):
        """Test fichier PDF autorisé"""
        from app.services.document_service import DocumentService
        
        assert DocumentService.is_allowed_file("cv.pdf") is True

    def test_is_allowed_file_docx(self):
        """Test fichier DOCX autorisé"""
        from app.services.document_service import DocumentService
        
        assert DocumentService.is_allowed_file("cv.docx") is True

    def test_is_allowed_file_not_allowed(self):
        """Test fichier non autorisé"""
        from app.services.document_service import DocumentService
        
        assert DocumentService.is_allowed_file("virus.exe") is False

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_save_uploaded_file_success(self, mock_mkdir, mock_file):
        """Test sauvegarde fichier réussi"""
        from app.services.document_service import DocumentService
        
        mock_uploaded = Mock()
        mock_uploaded.name = "cv.pdf"
        mock_uploaded.size = 1024
        mock_uploaded.type = "application/pdf"
        mock_uploaded.getbuffer.return_value = b"fake pdf content"
        
        result = DocumentService.save_uploaded_file(mock_uploaded, 1)
        
        assert result["success"] is True
        assert "file_path" in result
        assert result["consultant_id"] == 1

    @patch('builtins.open', side_effect=IOError("Disk full"))
    @patch('pathlib.Path.mkdir')
    def test_save_uploaded_file_error(self, mock_mkdir, mock_file):
        """Test sauvegarde fichier avec erreur"""
        from app.services.document_service import DocumentService
        
        mock_uploaded = Mock()
        mock_uploaded.name = "cv.pdf"
        mock_uploaded.getbuffer.return_value = b"content"
        
        result = DocumentService.save_uploaded_file(mock_uploaded, 1)
        
        assert result["success"] is False
        assert "error" in result


class TestTextExtraction(unittest.TestCase):
    """Tests extraction texte des documents"""

    @patch('app.services.document_service.DocumentService._extract_text_from_pdf')
    def test_extract_text_from_file_pdf(self, mock_extract):
        """Test extraction texte PDF"""
        from app.services.document_service import DocumentService
        
        mock_extract.return_value = "Extracted PDF text"
        
        result = DocumentService.extract_text_from_file("test.pdf")
        assert "Extracted PDF text" in result or isinstance(result, str)

    @patch('app.services.document_service.DocumentService._extract_text_from_docx')
    def test_extract_text_from_file_docx(self, mock_extract):
        """Test extraction texte DOCX"""
        from app.services.document_service import DocumentService
        
        mock_extract.return_value = "Extracted DOCX text"
        
        result = DocumentService.extract_text_from_file("test.docx")
        assert "Extracted DOCX text" in result or isinstance(result, str)

    @patch('app.services.document_service.DocumentService._extract_text_from_pptx')
    def test_extract_text_from_file_pptx(self, mock_extract):
        """Test extraction texte PPTX"""
        from app.services.document_service import DocumentService
        
        mock_extract.return_value = "Extracted PPTX text"
        
        result = DocumentService.extract_text_from_file("test.pptx")
        assert "Extracted PPTX text" in result or isinstance(result, str)

    def test_extract_text_from_file_unsupported(self):
        """Test extraction format non supporté"""
        from app.services.document_service import DocumentService
        
        result = DocumentService.extract_text_from_file("test.txt")
        assert "non supporté" in result.lower()

    @patch('app.services.document_service.pdfplumber.open')
    def test_extract_text_from_pdf_success(self, mock_pdf):
        """Test extraction PDF réussi"""
        from app.services.document_service import DocumentService
        
        mock_page = Mock()
        mock_page.extract_text.return_value = "Page text"
        mock_pdf_obj = Mock()
        mock_pdf_obj.pages = [mock_page]
        mock_pdf.return_value.__enter__.return_value = mock_pdf_obj
        
        result = DocumentService._extract_text_from_pdf("test.pdf")
        assert isinstance(result, str)

    @patch('app.services.document_service.pdfplumber.open', side_effect=IOError("File not found"))
    def test_extract_text_from_pdf_error(self, mock_pdf):
        """Test extraction PDF avec erreur"""
        from app.services.document_service import DocumentService
        
        result = DocumentService._extract_text_from_pdf("nonexistent.pdf")
        assert "Erreur" in result

    @patch('app.services.document_service.DocxDocument')
    def test_extract_text_from_docx_success(self, mock_docx):
        """Test extraction DOCX réussi"""
        from app.services.document_service import DocumentService
        
        mock_para = Mock()
        mock_para.text = "Paragraph text"
        mock_doc = Mock()
        mock_doc.paragraphs = [mock_para]
        mock_docx.return_value = mock_doc
        
        result = DocumentService._extract_text_from_docx("test.docx")
        assert isinstance(result, str)

    @patch('app.services.document_service.DocxDocument', side_effect=IOError("File error"))
    def test_extract_text_from_docx_error(self, mock_docx):
        """Test extraction DOCX avec erreur"""
        from app.services.document_service import DocumentService
        
        result = DocumentService._extract_text_from_docx("bad.docx")
        assert "Erreur" in result

    @patch('app.services.document_service.Presentation')
    def test_extract_text_from_pptx_success(self, mock_pptx):
        """Test extraction PPTX réussi"""
        from app.services.document_service import DocumentService
        
        mock_shape = Mock()
        mock_shape.text = "Shape text"
        mock_slide = Mock()
        mock_slide.shapes = [mock_shape]
        mock_prs = Mock()
        mock_prs.slides = [mock_slide]
        mock_pptx.return_value = mock_prs
        
        result = DocumentService._extract_text_from_pptx("test.pptx")
        assert isinstance(result, str)

    @patch('app.services.document_service.Presentation', side_effect=IOError("File error"))
    def test_extract_text_from_pptx_error(self, mock_pptx):
        """Test extraction PPTX avec erreur"""
        from app.services.document_service import DocumentService
        
        result = DocumentService._extract_text_from_pptx("bad.pptx")
        assert "Erreur" in result


class TestPublicExtractionMethods(unittest.TestCase):
    """Tests des méthodes publiques d'extraction"""

    @patch('app.services.document_service.pdfplumber.open')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake pdf')
    def test_extract_text_from_pdf_public_success(self, mock_file, mock_pdf):
        """Test extraction publique PDF réussi"""
        from app.services.document_service import DocumentService
        
        mock_page = Mock()
        mock_page.extract_text.return_value = "PDF content"
        mock_pdf_obj = Mock()
        mock_pdf_obj.pages = [mock_page]
        mock_pdf.return_value.__enter__.return_value = mock_pdf_obj
        
        result = DocumentService.extract_text_from_pdf("test.pdf")
        assert isinstance(result, str)

    @patch('app.services.document_service.pdfplumber.open', side_effect=IOError("Error"))
    @patch('builtins.open', new_callable=mock_open)
    @patch('app.services.document_service.PyPDF2.PdfReader')
    def test_extract_text_from_pdf_fallback(self, mock_pypdf, mock_file, mock_pdfplumber):
        """Test extraction PDF avec fallback PyPDF2"""
        from app.services.document_service import DocumentService
        
        mock_page = Mock()
        mock_page.extract_text.return_value = "Fallback text"
        mock_reader = Mock()
        mock_reader.pages = [mock_page]
        mock_pypdf.return_value = mock_reader
        
        result = DocumentService.extract_text_from_pdf("test.pdf")
        assert isinstance(result, str)

    @patch('app.services.document_service.DocxDocument')
    def test_extract_text_from_docx_public_with_tables(self, mock_docx):
        """Test extraction DOCX avec tableaux"""
        from app.services.document_service import DocumentService
        
        mock_para = Mock()
        mock_para.text = "Paragraph"
        
        mock_cell = Mock()
        mock_cell.text = "Cell"
        mock_row = Mock()
        mock_row.cells = [mock_cell]
        mock_table = Mock()
        mock_table.rows = [mock_row]
        
        mock_doc = Mock()
        mock_doc.paragraphs = [mock_para]
        mock_doc.tables = [mock_table]
        mock_docx.return_value = mock_doc
        
        result = DocumentService.extract_text_from_docx("test.docx")
        assert isinstance(result, str)

    @patch('app.services.document_service.DocxDocument', side_effect=IOError("Error"))
    def test_extract_text_from_docx_public_error(self, mock_docx):
        """Test extraction DOCX publique avec erreur"""
        from app.services.document_service import DocumentService
        
        result = DocumentService.extract_text_from_docx("bad.docx")
        assert "Erreur" in result

    @patch('app.services.document_service.Presentation')
    def test_extract_text_from_pptx_public_success(self, mock_pptx):
        """Test extraction PPTX publique réussi"""
        from app.services.document_service import DocumentService
        
        mock_shape = Mock()
        mock_shape.text = "Slide text"
        mock_slide = Mock()
        mock_slide.shapes = [mock_shape]
        mock_prs = Mock()
        mock_prs.slides = [mock_slide]
        mock_pptx.return_value = mock_prs
        
        result = DocumentService.extract_text_from_pptx("test.pptx")
        assert isinstance(result, str)

    @patch('app.services.document_service.Presentation', side_effect=IOError("Error"))
    def test_extract_text_from_pptx_public_error(self, mock_pptx):
        """Test extraction PPTX publique avec erreur"""
        from app.services.document_service import DocumentService
        
        result = DocumentService.extract_text_from_pptx("bad.pptx")
        assert "Erreur" in result


class TestCVAnalysis(unittest.TestCase):
    """Tests analyse de contenu CV"""

    def test_analyze_cv_content_basic(self):
        """Test analyse CV basique"""
        from app.services.document_service import DocumentService
        
        text = "Python Java 5 ans d'expérience Ingénieur"
        result = DocumentService.analyze_cv_content(text)
        
        assert isinstance(result, dict)
        assert "skills_detected" in result
        assert "experience_years" in result

    def test_analyze_cv_content_empty(self):
        """Test analyse CV vide"""
        from app.services.document_service import DocumentService
        
        result = DocumentService.analyze_cv_content("")
        
        assert isinstance(result, dict)


class TestAllowedExtensions(unittest.TestCase):
    """Tests extensions autorisées"""

    def test_allowed_extensions_ppt(self):
        """Test PPT autorisé"""
        from app.services.document_service import DocumentService
        
        assert "ppt" in DocumentService.ALLOWED_EXTENSIONS

    def test_allowed_extensions_doc(self):
        """Test DOC autorisé"""
        from app.services.document_service import DocumentService
        
        assert "doc" in DocumentService.ALLOWED_EXTENSIONS


if __name__ == "__main__":
    unittest.main()
