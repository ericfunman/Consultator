"""
Tests Phase 54 - document_analyzer.py extraction functions
Coverage 69% → 80%+ (cible: lignes 250-453)
Focus: extract_text_from_file, PDF/DOCX/PPTX extraction methods
"""

import pytest
from unittest.mock import Mock, patch, mock_open, MagicMock
import sys
import os
from pathlib import Path

# Import du module à tester
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from app.services.document_analyzer import DocumentAnalyzer


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_pdf_file():
    """Mock d'un fichier PDF"""
    return "/tmp/test_cv.pdf"


@pytest.fixture
def mock_docx_file():
    """Mock d'un fichier DOCX"""
    return "/tmp/test_cv.docx"


@pytest.fixture
def mock_pptx_file():
    """Mock d'un fichier PowerPoint"""
    return "/tmp/presentation.pptx"


# ============================================================================
# TESTS: extract_text_from_file() - Main entry point
# ============================================================================

class TestExtractTextFromFile:
    """Tests pour la fonction extract_text_from_file()"""

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_text_from_pdf')
    @patch('streamlit.error')
    def test_extract_text_pdf_success(self, mock_st_error, mock_extract_pdf, mock_pdf_file):
        """Test extraction réussie d'un PDF"""
        mock_extract_pdf.return_value = "Contenu du PDF extrait"
        
        result = DocumentAnalyzer.extract_text_from_file(mock_pdf_file)
        
        assert result == "Contenu du PDF extrait"
        mock_extract_pdf.assert_called_once_with(mock_pdf_file)
        mock_st_error.assert_not_called()

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_text_from_docx')
    @patch('streamlit.error')
    def test_extract_text_docx_success(self, mock_st_error, mock_extract_docx, mock_docx_file):
        """Test extraction réussie d'un DOCX"""
        mock_extract_docx.return_value = "Contenu du DOCX extrait"
        
        result = DocumentAnalyzer.extract_text_from_file(mock_docx_file)
        
        assert result == "Contenu du DOCX extrait"
        mock_extract_docx.assert_called_once_with(mock_docx_file)

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_text_from_pptx')
    @patch('streamlit.error')
    def test_extract_text_pptx_success(self, mock_st_error, mock_extract_pptx, mock_pptx_file):
        """Test extraction réussie d'un PPTX"""
        mock_extract_pptx.return_value = "Contenu du PPTX extrait"
        
        result = DocumentAnalyzer.extract_text_from_file(mock_pptx_file)
        
        assert result == "Contenu du PPTX extrait"
        mock_extract_pptx.assert_called_once_with(mock_pptx_file)

    @patch('streamlit.error')
    def test_extract_text_unsupported_format(self, mock_st_error):
        """Test avec format non supporté"""
        result = DocumentAnalyzer.extract_text_from_file("/tmp/file.txt")
        
        assert result == ""
        mock_st_error.assert_called_once()

    @patch('streamlit.error')
    def test_extract_text_doc_extension(self, mock_st_error):
        """Test avec extension .doc (Word ancien format)"""
        with patch.object(DocumentAnalyzer, '_extract_text_from_docx') as mock_docx:
            mock_docx.return_value = "Texte extrait"
            
            result = DocumentAnalyzer.extract_text_from_file("/tmp/old_doc.doc")
            
            assert result == "Texte extrait"
            mock_docx.assert_called_once()

    @patch('streamlit.error')
    def test_extract_text_ppt_extension(self, mock_st_error):
        """Test avec extension .ppt (PowerPoint ancien format)"""
        with patch.object(DocumentAnalyzer, '_extract_text_from_pptx') as mock_pptx:
            mock_pptx.return_value = "Texte slides"
            
            result = DocumentAnalyzer.extract_text_from_file("/tmp/old_pres.ppt")
            
            assert result == "Texte slides"
            mock_pptx.assert_called_once()

    @patch('streamlit.error')
    def test_extract_text_case_insensitive_extension(self, mock_st_error):
        """Test avec extension majuscule"""
        with patch.object(DocumentAnalyzer, '_extract_text_from_pdf') as mock_pdf:
            mock_pdf.return_value = "PDF content"
            
            result = DocumentAnalyzer.extract_text_from_file("/tmp/FILE.PDF")
            
            assert result == "PDF content"

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_text_from_pdf')
    @patch('streamlit.error')
    def test_extract_text_oserror(self, mock_st_error, mock_extract_pdf):
        """Test gestion OSError"""
        mock_extract_pdf.side_effect = OSError("File not found")
        
        result = DocumentAnalyzer.extract_text_from_file("/tmp/missing.pdf")
        
        assert result == ""
        mock_st_error.assert_called_once()

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_text_from_pdf')
    @patch('streamlit.error')
    def test_extract_text_valueerror(self, mock_st_error, mock_extract_pdf):
        """Test gestion ValueError"""
        mock_extract_pdf.side_effect = ValueError("Invalid format")
        
        result = DocumentAnalyzer.extract_text_from_file("/tmp/corrupt.pdf")
        
        assert result == ""
        mock_st_error.assert_called_once()


# ============================================================================
# TESTS: _extract_text_from_pdf() - PDF extraction main
# ============================================================================

class TestExtractTextFromPdf:
    """Tests pour _extract_text_from_pdf()"""

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_pdf_with_pdfplumber')
    @patch('streamlit.success')
    def test_extract_pdf_pdfplumber_success(self, mock_st_success, mock_pdfplumber, mock_pdf_file):
        """Test extraction PDF avec pdfplumber réussie"""
        mock_pdfplumber.return_value = ["Page 1 content", "Page 2 content"]
        
        result = DocumentAnalyzer._extract_text_from_pdf(mock_pdf_file)
        
        assert "Page 1 content" in result
        assert "Page 2 content" in result
        mock_st_success.assert_called_once()
        assert "pdfplumber" in mock_st_success.call_args[0][0]

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_pdf_with_pdfplumber')
    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_pdf_with_pypdf2')
    @patch('streamlit.success')
    def test_extract_pdf_fallback_to_pypdf2(self, mock_st_success, mock_pypdf2, mock_pdfplumber, mock_pdf_file):
        """Test fallback vers PyPDF2 si pdfplumber échoue"""
        mock_pdfplumber.return_value = []  # Échec pdfplumber
        mock_pypdf2.return_value = ["Page 1", "Page 2"]
        
        result = DocumentAnalyzer._extract_text_from_pdf(mock_pdf_file)
        
        assert "Page 1" in result
        mock_pypdf2.assert_called_once()
        assert "PyPDF2" in mock_st_success.call_args[0][0]

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_pdf_with_pdfplumber')
    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_pdf_with_pypdf2')
    @patch('streamlit.error')
    def test_extract_pdf_both_methods_fail(self, mock_st_error, mock_pypdf2, mock_pdfplumber, mock_pdf_file):
        """Test échec des deux méthodes d'extraction"""
        mock_pdfplumber.return_value = []
        mock_pypdf2.return_value = []
        
        result = DocumentAnalyzer._extract_text_from_pdf(mock_pdf_file)
        
        assert result == ""
        mock_st_error.assert_called_once()
        assert "Aucun texte" in mock_st_error.call_args[0][0]

    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_pdf_with_pdfplumber')
    @patch('streamlit.error')
    def test_extract_pdf_exception(self, mock_st_error, mock_pdfplumber, mock_pdf_file):
        """Test gestion d'exception lors de l'extraction"""
        mock_pdfplumber.side_effect = OSError("Cannot open file")
        
        result = DocumentAnalyzer._extract_text_from_pdf(mock_pdf_file)
        
        assert result == ""
        mock_st_error.assert_called_once()


# ============================================================================
# TESTS: _extract_pdf_with_pdfplumber()
# ============================================================================

class TestExtractPdfWithPdfplumber:
    """Tests pour _extract_pdf_with_pdfplumber()"""

    @patch('pdfplumber.open')
    @patch('streamlit.info')
    def test_extract_pdfplumber_single_page(self, mock_st_info, mock_pdfplumber_open, mock_pdf_file):
        """Test extraction d'un PDF 1 page avec pdfplumber"""
        mock_page = Mock()
        mock_page.extract_text.return_value = "Page content"
        mock_page.extract_tables.return_value = []
        
        mock_pdf = Mock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__ = Mock(return_value=mock_pdf)
        mock_pdf.__exit__ = Mock(return_value=False)
        
        mock_pdfplumber_open.return_value = mock_pdf
        
        result = DocumentAnalyzer._extract_pdf_with_pdfplumber(mock_pdf_file)
        
        assert len(result) == 1
        assert "Page content" in result[0]
        assert "PAGE 1" in result[0]

    @patch('pdfplumber.open')
    @patch('streamlit.info')
    @patch('streamlit.warning')
    def test_extract_pdfplumber_with_tables(self, mock_st_warning, mock_st_info, mock_pdfplumber_open, mock_pdf_file):
        """Test extraction avec tableaux"""
        mock_page = Mock()
        mock_page.extract_text.return_value = "Text content"
        mock_page.extract_tables.return_value = [
            [["Header1", "Header2"], ["Value1", "Value2"]]
        ]
        
        mock_pdf = Mock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__ = Mock(return_value=mock_pdf)
        mock_pdf.__exit__ = Mock(return_value=False)
        
        mock_pdfplumber_open.return_value = mock_pdf
        
        result = DocumentAnalyzer._extract_pdf_with_pdfplumber(mock_pdf_file)
        
        assert len(result) == 2  # Texte + tableau
        assert "TABLEAU" in result[1]

    @patch('pdfplumber.open')
    @patch('streamlit.info')
    @patch('streamlit.warning')
    def test_extract_pdfplumber_page_error(self, mock_st_warning, mock_st_info, mock_pdfplumber_open, mock_pdf_file):
        """Test gestion d'erreur sur une page"""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1"
        mock_page1.extract_tables.return_value = []
        
        mock_page2 = Mock()
        mock_page2.extract_text.side_effect = ValueError("Corrupt page")
        
        mock_pdf = Mock()
        mock_pdf.pages = [mock_page1, mock_page2]
        mock_pdf.__enter__ = Mock(return_value=mock_pdf)
        mock_pdf.__exit__ = Mock(return_value=False)
        
        mock_pdfplumber_open.return_value = mock_pdf
        
        result = DocumentAnalyzer._extract_pdf_with_pdfplumber(mock_pdf_file)
        
        # Devrait avoir extrait page 1 seulement
        assert len(result) >= 1
        mock_st_warning.assert_called_once()

    @patch('pdfplumber.open')
    @patch('streamlit.info')
    def test_extract_pdfplumber_multiple_pages(self, mock_st_info, mock_pdfplumber_open, mock_pdf_file):
        """Test extraction multi-pages"""
        mock_pages = []
        for i in range(3):
            mock_page = Mock()
            mock_page.extract_text.return_value = f"Page {i+1} content"
            mock_page.extract_tables.return_value = []
            mock_pages.append(mock_page)
        
        mock_pdf = Mock()
        mock_pdf.pages = mock_pages
        mock_pdf.__enter__ = Mock(return_value=mock_pdf)
        mock_pdf.__exit__ = Mock(return_value=False)
        
        mock_pdfplumber_open.return_value = mock_pdf
        
        result = DocumentAnalyzer._extract_pdf_with_pdfplumber(mock_pdf_file)
        
        assert len(result) == 3
        for i in range(3):
            assert f"PAGE {i+1}" in result[i]


# ============================================================================
# TESTS: _extract_pdf_with_pypdf2()
# ============================================================================

class TestExtractPdfWithPypdf2:
    """Tests pour _extract_pdf_with_pypdf2()"""

    @patch('builtins.open', new_callable=mock_open, read_data=b'PDF content')
    @patch('pypdf.PdfReader')
    @patch('streamlit.info')
    def test_extract_pypdf2_single_page(self, mock_st_info, mock_pdfreader, mock_file, mock_pdf_file):
        """Test extraction avec PyPDF2 une page"""
        mock_page = Mock()
        mock_page.extract_text.return_value = "Page text"
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page]
        mock_pdfreader.return_value = mock_reader
        
        result = DocumentAnalyzer._extract_pdf_with_pypdf2(mock_pdf_file)
        
        assert len(result) == 1
        assert "PAGE 1" in result[0]
        assert "Page text" in result[0]

    @patch('builtins.open', new_callable=mock_open, read_data=b'PDF content')
    @patch('pypdf.PdfReader')
    @patch('streamlit.info')
    @patch('streamlit.warning')
    def test_extract_pypdf2_page_error(self, mock_st_warning, mock_st_info, mock_pdfreader, mock_file, mock_pdf_file):
        """Test gestion d'erreur extraction page"""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1"
        
        mock_page2 = Mock()
        mock_page2.extract_text.side_effect = ValueError("Error")
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2]
        mock_pdfreader.return_value = mock_reader
        
        result = DocumentAnalyzer._extract_pdf_with_pypdf2(mock_pdf_file)
        
        # Devrait avoir page 1 seulement
        assert len(result) >= 1
        mock_st_warning.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data=b'PDF content')
    @patch('pypdf.PdfReader')
    @patch('streamlit.info')
    def test_extract_pypdf2_empty_page(self, mock_st_info, mock_pdfreader, mock_file, mock_pdf_file):
        """Test page vide"""
        mock_page = Mock()
        mock_page.extract_text.return_value = ""
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page]
        mock_pdfreader.return_value = mock_reader
        
        result = DocumentAnalyzer._extract_pdf_with_pypdf2(mock_pdf_file)
        
        # Page vide non ajoutée
        assert len(result) == 0


# ============================================================================
# TESTS: _extract_text_from_docx()
# ============================================================================

class TestExtractTextFromDocx:
    """Tests pour _extract_text_from_docx()"""

    @patch('app.services.document_analyzer.Document')
    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_docx_paragraphs')
    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_docx_tables')
    @patch('streamlit.info')
    @patch('streamlit.success')
    def test_extract_docx_success(self, mock_st_success, mock_st_info, mock_tables, mock_paragraphs, mock_document, mock_docx_file):
        """Test extraction DOCX réussie"""
        mock_doc = Mock()
        mock_document.return_value = mock_doc
        mock_paragraphs.return_value = ["Paragraph 1", "Paragraph 2"]
        mock_tables.return_value = ["Table data"]
        
        result = DocumentAnalyzer._extract_text_from_docx(mock_docx_file)
        
        assert "Paragraph 1" in result
        assert "Paragraph 2" in result

    @patch('app.services.document_analyzer.Document')
    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_docx_paragraphs')
    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_docx_tables')
    @patch('streamlit.info')
    @patch('streamlit.success')
    def test_extract_docx_empty(self, mock_st_success, mock_st_info, mock_tables, mock_paragraphs, mock_document, mock_docx_file):
        """Test DOCX vide"""
        mock_doc = Mock()
        mock_document.return_value = mock_doc
        mock_paragraphs.return_value = []
        mock_tables.return_value = []
        
        result = DocumentAnalyzer._extract_text_from_docx(mock_docx_file)
        
        assert result == ""

    @patch('app.services.document_analyzer.Document')
    @patch('streamlit.error')
    def test_extract_docx_error(self, mock_st_error, mock_document, mock_docx_file):
        """Test erreur extraction DOCX"""
        mock_document.side_effect = OSError("Cannot open")
        
        result = DocumentAnalyzer._extract_text_from_docx(mock_docx_file)
        
        assert result == ""
        mock_st_error.assert_called_once()


# ============================================================================
# TESTS: _extract_text_from_pptx()
# ============================================================================

class TestExtractTextFromPptx:
    """Tests pour _extract_text_from_pptx()"""

    @patch('app.services.document_analyzer.Presentation')
    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_slide_content')
    @patch('streamlit.info')
    @patch('streamlit.success')
    def test_extract_pptx_success(self, mock_st_success, mock_st_info, mock_slide_content, mock_presentation, mock_pptx_file):
        """Test extraction PPTX réussie"""
        mock_slide1 = Mock()
        mock_slide2 = Mock()
        
        mock_prs = Mock()
        mock_prs.slides = [mock_slide1, mock_slide2]
        mock_presentation.return_value = mock_prs
        
        mock_slide_content.side_effect = [["Title"], ["Content"]]
        
        result = DocumentAnalyzer._extract_text_from_pptx(mock_pptx_file)
        
        assert "Title" in result
        assert "Content" in result

    @patch('app.services.document_analyzer.Presentation')
    @patch('app.services.document_analyzer.DocumentAnalyzer._extract_slide_content')
    @patch('streamlit.info')
    @patch('streamlit.success')
    def test_extract_pptx_no_text(self, mock_st_success, mock_st_info, mock_slide_content, mock_presentation, mock_pptx_file):
        """Test PPTX sans texte"""
        mock_slide = Mock()
        
        mock_prs = Mock()
        mock_prs.slides = [mock_slide]
        mock_presentation.return_value = mock_prs
        
        mock_slide_content.return_value = []
        
        result = DocumentAnalyzer._extract_text_from_pptx(mock_pptx_file)
        
        assert result == ""

    @patch('app.services.document_analyzer.Presentation')
    @patch('streamlit.error')
    def test_extract_pptx_error(self, mock_st_error, mock_presentation, mock_pptx_file):
        """Test erreur extraction PPTX"""
        mock_presentation.side_effect = ValueError("File corrupt")
        
        result = DocumentAnalyzer._extract_text_from_pptx(mock_pptx_file)
        
        assert result == ""
        mock_st_error.assert_called_once()


# ============================================================================
# TESTS: Edge cases
# ============================================================================

class TestEdgeCases:
    """Tests des cas limites"""

    @patch('streamlit.error')
    def test_extract_none_path(self, mock_st_error):
        """Test avec chemin None"""
        result = DocumentAnalyzer.extract_text_from_file(None)
        
        assert result == ""
        mock_st_error.assert_called_once()

    @patch('streamlit.error')
    def test_extract_empty_path(self, mock_st_error):
        """Test avec chemin vide"""
        result = DocumentAnalyzer.extract_text_from_file("")
        
        assert result == ""
        mock_st_error.assert_called_once()

    @patch('pdfplumber.open')
    @patch('streamlit.info')
    def test_extract_pdfplumber_none_text(self, mock_st_info, mock_pdfplumber_open):
        """Test page PDF avec texte None"""
        mock_page = Mock()
        mock_page.extract_text.return_value = None
        mock_page.extract_tables.return_value = []
        
        mock_pdf = Mock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__ = Mock(return_value=mock_pdf)
        mock_pdf.__exit__ = Mock(return_value=False)
        
        mock_pdfplumber_open.return_value = mock_pdf
        
        result = DocumentAnalyzer._extract_pdf_with_pdfplumber("/tmp/test.pdf")
        
        # Page avec None non ajoutée
        assert len(result) == 0
