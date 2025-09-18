"""
Tests unitaires pour le service de documents
Couvre les fonctionnalités d'upload, extraction de texte et analyse de CV
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.services.document_service import DocumentService


class TestDocumentService:
    """Tests pour la classe DocumentService"""

    def setup_method(self):
        """Configuration avant chaque test"""
        # Créer un répertoire temporaire pour les tests
        self.temp_dir = tempfile.mkdtemp()
        self.original_upload_dir = DocumentService.UPLOAD_DIR
        DocumentService.UPLOAD_DIR = Path(self.temp_dir) / "uploads"

    def teardown_method(self):
        """Nettoyage après chaque test"""
        # Restaurer le répertoire original
        DocumentService.UPLOAD_DIR = self.original_upload_dir

        # Supprimer le répertoire temporaire
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_upload_directory(self):
        """Test d'initialisation du répertoire d'upload"""
        upload_dir = DocumentService.init_upload_directory()
        assert upload_dir.exists()
        assert upload_dir.is_dir()

    def test_get_file_extension(self):
        """Test de récupération d'extension de fichier"""
        assert DocumentService.get_file_extension("test.pdf") == "pdf"
        assert DocumentService.get_file_extension("test.PDF") == "pdf"
        assert DocumentService.get_file_extension("test.docx") == "docx"
        assert DocumentService.get_file_extension("test") == ""
        assert DocumentService.get_file_extension("") == ""

    def test_is_allowed_file(self):
        """Test de vérification de fichier autorisé"""
        assert DocumentService.is_allowed_file("test.pdf") is True
        assert DocumentService.is_allowed_file("test.docx") is True
        assert DocumentService.is_allowed_file("test.pptx") is True
        assert DocumentService.is_allowed_file("test.txt") is False
        assert DocumentService.is_allowed_file("test.exe") is False

    def test_save_uploaded_file_success(self):
        """Test de sauvegarde de fichier uploadé avec succès"""
        # Mock d'un fichier uploadé Streamlit
        mock_file = MagicMock()
        mock_file.name = "test_document.pdf"
        mock_file.size = 1024
        mock_file.type = "application/pdf"
        mock_file.getbuffer.return_value = b"test content"

        result = DocumentService.save_uploaded_file(mock_file, consultant_id=1)

        assert result["success"] is True
        assert "file_path" in result
        assert result["filename"].endswith("_test_document.pdf")
        assert result["original_name"] == "test_document.pdf"
        assert result["size"] == 1024
        assert result["type"] == "application/pdf"
        assert result["extension"] == "pdf"
        assert result["consultant_id"] == 1
        assert "upload_date" in result

        # Vérifier que le fichier a été créé
        assert Path(result["file_path"]).exists()

    def test_save_uploaded_file_error(self):
        """Test de sauvegarde de fichier avec erreur"""
        mock_file = MagicMock()
        mock_file.name = "test.pdf"
        mock_file.getbuffer.side_effect = OSError("Disk full")

        result = DocumentService.save_uploaded_file(mock_file, consultant_id=1)

        assert result["success"] is False
        assert "error" in result

    def test_extract_text_from_file_pdf(self):
        """Test d'extraction de texte depuis un PDF"""
        # Créer un fichier PDF temporaire simulé
        pdf_path = Path(self.temp_dir) / "test.pdf"
        pdf_path.write_text("dummy pdf content")

        with patch.object(DocumentService, "_extract_text_from_pdf") as mock_extract:
            mock_extract.return_value = "Extracted PDF text"

            result = DocumentService.extract_text_from_file(str(pdf_path))
            assert result == "Extracted PDF text"
            mock_extract.assert_called_once_with(str(pdf_path))

    def test_extract_text_from_file_docx(self):
        """Test d'extraction de texte depuis un DOCX"""
        docx_path = Path(self.temp_dir) / "test.docx"

        with patch.object(DocumentService, "_extract_text_from_docx") as mock_extract:
            mock_extract.return_value = "Extracted DOCX text"

            result = DocumentService.extract_text_from_file(str(docx_path))
            assert result == "Extracted DOCX text"
            mock_extract.assert_called_once_with(str(docx_path))

    def test_extract_text_from_file_unsupported(self):
        """Test d'extraction de texte depuis un format non supporté"""
        txt_path = Path(self.temp_dir) / "test.txt"

        result = DocumentService.extract_text_from_file(str(txt_path))
        assert result == "Format txt non supporté"

    def test_extract_text_from_file_error(self):
        """Test d'extraction de texte avec erreur"""
        pdf_path = Path(self.temp_dir) / "test.pdf"

        with patch.object(DocumentService, "_extract_text_from_pdf") as mock_extract:
            mock_extract.side_effect = OSError("File corrupted")

            result = DocumentService.extract_text_from_file(str(pdf_path))
            assert result == "Erreur d'extraction: File corrupted"

    @patch("app.services.document_service.pdfplumber")
    def test_extract_text_from_pdf_success(self, mock_pdfplumber):
        """Test d'extraction de texte PDF avec succès"""
        # Mock pdfplumber
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Page content"
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf

        pdf_path = Path(self.temp_dir) / "test.pdf"
        result = DocumentService.extract_text_from_pdf(str(pdf_path))

        assert result == "Page content"
        mock_pdfplumber.open.assert_called_once_with(str(pdf_path))

    @patch("app.services.document_service.DocxDocument")
    def test_extract_text_from_docx_success(self, mock_docx):
        """Test d'extraction de texte DOCX avec succès"""
        # Mock docx
        mock_para1 = MagicMock()
        mock_para1.text = "Paragraph 1"
        mock_para2 = MagicMock()
        mock_para2.text = "Paragraph 2"
        mock_doc = MagicMock()
        mock_doc.paragraphs = [mock_para1, mock_para2]
        mock_doc.tables = []
        mock_docx.return_value = mock_doc

        docx_path = Path(self.temp_dir) / "test.docx"
        result = DocumentService.extract_text_from_docx(str(docx_path))

        assert result == "Paragraph 1\nParagraph 2"
        mock_docx.assert_called_once_with(str(docx_path))

    @patch("app.services.document_service.DocxDocument")
    def test_extract_text_from_docx_with_tables(self, mock_docx):
        """Test d'extraction de texte DOCX avec tableaux"""
        # Mock docx avec tableaux
        mock_para = MagicMock()
        mock_para.text = "Content"

        mock_cell = MagicMock()
        mock_cell.text = "Cell content"
        mock_row = MagicMock()
        mock_row.cells = [mock_cell]
        mock_table = MagicMock()
        mock_table.rows = [mock_row]

        mock_doc = MagicMock()
        mock_doc.paragraphs = [mock_para]
        mock_doc.tables = [mock_table]
        mock_docx.return_value = mock_doc

        docx_path = Path(self.temp_dir) / "test.docx"
        result = DocumentService.extract_text_from_docx(str(docx_path))

        assert "Content" in result
        assert "Cell content" in result

    @patch("app.services.document_service.Presentation")
    def test_extract_text_from_pptx_success(self, mock_pptx):
        """Test d'extraction de texte PPTX avec succès"""
        # Mock pptx
        mock_shape = MagicMock()
        mock_shape.text = "Slide content"
        mock_slide = MagicMock()
        mock_slide.shapes = [mock_shape]
        mock_prs = MagicMock()
        mock_prs.slides = [mock_slide]
        mock_pptx.return_value = mock_prs

        pptx_path = Path(self.temp_dir) / "test.pptx"
        result = DocumentService.extract_text_from_pptx(str(pptx_path))

        assert result == "Slide content"
        mock_pptx.assert_called_once_with(str(pptx_path))

    def test_analyze_cv_content_basic(self):
        """Test d'analyse basique du contenu CV"""
        cv_text = """
        John Doe
        Python Developer with 5 years of experience

        Skills: Python, JavaScript, React, SQL, Docker
        Languages: Français, Anglais

        Experience: 5 years in software development
        """

        result = DocumentService.analyze_cv_content(cv_text)

        assert "skills_detected" in result
        assert len(result["skills_detected"]) > 0
        assert any(skill["skill"] == "Python" for skill in result["skills_detected"])
        assert "languages" in result
        assert "Français" in result["languages"]
        assert "Anglais" in result["languages"]
        assert result["experience_years"]["total"] == 5
        assert "summary" in result

    def test_analyze_cv_content_empty(self):
        """Test d'analyse de CV vide"""
        result = DocumentService.analyze_cv_content("")

        assert result["skills_detected"] == []
        assert result["experience_years"] == {}
        assert result["languages"] == []
        assert result["education"] == []
        assert result["contact_info"] == {}
        assert result["summary"] == "..."

    def test_analyze_cv_content_no_matches(self):
        """Test d'analyse de CV sans correspondances"""
        cv_text = "This is a simple text without any technical skills mentioned."

        result = DocumentService.analyze_cv_content(cv_text)

        assert result["skills_detected"] == []
        assert result["experience_years"] == {}
        assert result["languages"] == []

    def test_get_consultant_documents(self):
        """Test de récupération des documents d'un consultant"""
        # Créer une structure de répertoires simulée
        consultant_dir = DocumentService.UPLOAD_DIR / "consultant_1"
        consultant_dir.mkdir(parents=True, exist_ok=True)

        # Créer des fichiers de test
        test_file1 = consultant_dir / "20231201_120000_cv.pdf"
        test_file1.write_text("dummy content")
        test_file2 = consultant_dir / "20231202_130000_resume.docx"
        test_file2.write_text("dummy content")

        documents = DocumentService.get_consultant_documents(1)

        assert len(documents) == 2
        # Vérifier que c'est trié par date (plus récent en premier)
        assert documents[0]["filename"] == "20231202_130000_resume.docx"
        assert documents[1]["filename"] == "20231201_120000_cv.pdf"

        # Vérifier les propriétés
        doc = documents[0]
        assert "filename" in doc
        assert "path" in doc
        assert "size" in doc
        assert "size_mb" in doc
        assert "modified" in doc
        assert "extension" in doc
        assert "type" in doc

    def test_get_consultant_documents_no_directory(self):
        """Test de récupération de documents quand le répertoire n'existe pas"""
        documents = DocumentService.get_consultant_documents(999)
        assert documents == []

    def test_get_file_type_name(self):
        """Test de récupération du nom du type de fichier"""
        assert DocumentService.get_file_type_name("test.pdf") == "PDF"
        assert DocumentService.get_file_type_name("test.docx") == "Word (DOCX)"
        assert DocumentService.get_file_type_name("test.doc") == "Word (DOC)"
        assert DocumentService.get_file_type_name("test.pptx") == "PowerPoint (PPTX)"
        assert DocumentService.get_file_type_name("test.ppt") == "PowerPoint (PPT)"
        assert DocumentService.get_file_type_name("test.unknown") == "Inconnu"

    def test_delete_document_success(self):
        """Test de suppression de document avec succès"""
        # Créer un fichier temporaire
        test_file = Path(self.temp_dir) / "test_to_delete.pdf"
        test_file.write_text("content")

        assert test_file.exists()

        result = DocumentService.delete_document(str(test_file))
        assert result is True
        assert not test_file.exists()

    def test_delete_document_error(self):
        """Test de suppression de document avec erreur"""
        non_existent_file = Path(self.temp_dir) / "non_existent.pdf"

        result = DocumentService.delete_document(str(non_existent_file))
        assert result is False

    @patch("app.services.document_service.get_database_session")
    def test_get_all_consultants_for_selection(self, mock_get_session):
        """Test de récupération de tous les consultants pour sélection"""
        # Mock de la session et des consultants
        mock_consultant1 = MagicMock()
        mock_consultant1.id = 1
        mock_consultant1.prenom = "John"
        mock_consultant1.nom = "Doe"
        mock_consultant1.email = "john.doe@example.com"

        mock_consultant2 = MagicMock()
        mock_consultant2.id = 2
        mock_consultant2.prenom = "Jane"
        mock_consultant2.nom = "Smith"
        mock_consultant2.email = "jane.smith@example.com"

        mock_session = MagicMock()
        mock_session.query.return_value.all.return_value = [
            mock_consultant1,
            mock_consultant2,
        ]
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = DocumentService.get_all_consultants_for_selection()

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["name"] == "John Doe"
        assert result[0]["email"] == "john.doe@example.com"
        assert result[0]["display"] == "John Doe (john.doe@example.com)"

        assert result[1]["id"] == 2
        assert result[1]["name"] == "Jane Smith"
        assert result[1]["email"] == "jane.smith@example.com"
        assert result[1]["display"] == "Jane Smith (jane.smith@example.com)"

    @patch("app.services.document_service.get_database_session")
    def test_get_all_consultants_for_selection_error(self, mock_get_session):
        """Test de récupération de consultants avec erreur DB"""
        from sqlalchemy.exc import SQLAlchemyError

        mock_session = MagicMock()
        mock_session.query.side_effect = SQLAlchemyError("DB connection failed")
        mock_get_session.return_value.__enter__.return_value = mock_session

        result = DocumentService.get_all_consultants_for_selection()
        assert result == []
