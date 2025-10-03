"""
Tests unitaires pour le service SimpleDocumentAnalyzer
"""

import tempfile
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from app.services.simple_analyzer import SimpleDocumentAnalyzer


class TestSimpleDocumentAnalyzer:
    """Tests pour SimpleDocumentAnalyzer"""

    def test_extract_text_from_txt_file(self):
        """Test extraction depuis fichier TXT"""
        test_content = "Ceci est un contenu de test pour le CV."

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = SimpleDocumentAnalyzer.extract_text_from_file("test.txt")

        assert result == test_content

    def test_extract_text_from_pdf_file(self):
        """Test extraction depuis fichier PDF"""
        # Mock pypdf
        mock_pdf_reader = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Contenu PDF"
        mock_pdf_reader.pages = [mock_page]

        with patch("pypdf.PdfReader") as mock_pdf_reader_class:
            mock_pdf_reader_class.return_value = mock_pdf_reader

            with patch("builtins.open", mock_open()):
                result = SimpleDocumentAnalyzer.extract_text_from_file("test.pdf")

        assert result == "Contenu PDF"

    def test_extract_text_from_pdf_error(self):
        """Test extraction PDF avec erreur"""
        with patch("pypdf.PdfReader", side_effect=OSError("PDF error")):
            with patch("builtins.open", mock_open()):
                result = SimpleDocumentAnalyzer.extract_text_from_file("test.pdf")

        assert "Erreur lors de l'extraction PDF" in result

    def test_extract_text_from_docx_file(self):
        """Test extraction depuis fichier DOCX"""
        # Mock docx
        mock_doc = MagicMock()
        mock_paragraph1 = MagicMock()
        mock_paragraph1.text = "Paragraphe 1"
        mock_paragraph2 = MagicMock()
        mock_paragraph2.text = "Paragraphe 2"
        mock_doc.paragraphs = [mock_paragraph1, mock_paragraph2]

        with patch("docx.Document") as mock_document:
            mock_document.return_value = mock_doc

            result = SimpleDocumentAnalyzer.extract_text_from_file("test.docx")

        assert result == "Paragraphe 1\nParagraphe 2"

    def test_extract_text_from_docx_error(self):
        """Test extraction DOCX avec erreur"""
        with patch("docx.Document", side_effect=OSError("DOCX error")):
            result = SimpleDocumentAnalyzer.extract_text_from_file("test.docx")

        assert "Erreur lors de l'extraction DOCX" in result

    def test_extract_text_from_pptx_file(self):
        """Test extraction depuis fichier PPTX"""
        # Mock pptx
        mock_prs = MagicMock()
        mock_slide = MagicMock()
        mock_shape = MagicMock()
        mock_shape.text = "Contenu slide"
        mock_slide.shapes = [mock_shape]
        mock_prs.slides = [mock_slide]

        with patch("pptx.Presentation") as mock_presentation:
            mock_presentation.return_value = mock_prs

            result = SimpleDocumentAnalyzer.extract_text_from_file("test.pptx")

        assert result == "Contenu slide"

    def test_extract_text_from_pptx_error(self):
        """Test extraction PPTX avec erreur"""
        with patch("pptx.Presentation", side_effect=OSError("PPTX error")):
            result = SimpleDocumentAnalyzer.extract_text_from_file("test.pptx")

        assert "Erreur lors de l'extraction PowerPoint" in result

    def test_extract_text_from_unsupported_format(self):
        """Test format non supporté"""
        result = SimpleDocumentAnalyzer.extract_text_from_file("test.xyz")
        assert result == "Format de fichier non supporté"

    def test_extract_text_file_error(self):
        """Test erreur générale d'ouverture de fichier"""
        with patch("builtins.open", side_effect=OSError("File error")):
            result = SimpleDocumentAnalyzer.extract_text_from_file("test.txt")

        assert "Erreur d'extraction: File error" in result

    @patch("app.services.simple_analyzer.st")
    def test_analyze_cv_content_basic(self, mock_st):
        """Test analyse basique du contenu CV"""
        text = """
        CV de Jean Dupont
        Technologies: Python, Java, SQL, Docker
        Expérience chez BNP Paribas et Société Générale
        Compétences en Business Intelligence et Data
        """

        result = SimpleDocumentAnalyzer.analyze_cv_content(text, "Jean Dupont")

        # Vérifications de base
        assert result["consultant"] == "Jean Dupont"
        assert "Python" in result["langages_techniques"]
        assert "Java" in result["langages_techniques"]
        assert "SQL" in result["langages_techniques"]
        assert "Docker" in result["langages_techniques"]
        assert len(result["missions"]) > 0
        assert result["missions"][0]["client"] in ["BNP Paribas", "Société Générale"]
        assert "Business Intelligence" in result["competences_fonctionnelles"]
        assert "Analyse de données" in result["competences_fonctionnelles"]
        assert "informations_generales" in result
        assert result["informations_generales"]["technologies_detectees"] > 0

    @patch("app.services.simple_analyzer.st")
    def test_analyze_cv_content_empty_text(self, mock_st):
        """Test analyse avec texte vide"""
        result = SimpleDocumentAnalyzer.analyze_cv_content("", "Test")

        assert result["consultant"] == "Test"
        assert result["langages_techniques"] == []
        assert result["missions"] == []
        assert result["competences_fonctionnelles"] == []
        assert result["informations_generales"]["technologies_detectees"] == 0

    @patch("app.services.simple_analyzer.st")
    def test_analyze_cv_content_no_matches(self, mock_st):
        """Test analyse sans correspondances"""
        text = "Texte sans technologies ni clients connus"
        result = SimpleDocumentAnalyzer.analyze_cv_content(text, "Test")

        assert result["langages_techniques"] == []
        assert result["missions"] == []
        assert result["competences_fonctionnelles"] == []
        assert result["informations_generales"]["technologies_detectees"] == 0
        assert result["informations_generales"]["clients_detectes"] == 0

    @patch("app.services.simple_analyzer.st")
    def test_analyze_cv_content_case_insensitive(self, mock_st):
        """Test recherche insensible à la casse"""
        text = "python, JAVASCRIPT, bnp paribas"
        result = SimpleDocumentAnalyzer.analyze_cv_content(text, "Test")

        assert "Python" in result["langages_techniques"]
        assert "JavaScript" in result["langages_techniques"]
        assert len(result["missions"]) > 0

    @patch("app.services.simple_analyzer.st")
    def test_analyze_cv_content_limit_results(self, mock_st):
        """Test limitation du nombre de résultats"""
        # Créer un texte avec beaucoup de technologies
        techs = SimpleDocumentAnalyzer.TECHNOLOGIES[:20]  # Plus de 15
        text = ", ".join(techs)

        result = SimpleDocumentAnalyzer.analyze_cv_content(text, "Test")

        # Vérifier que seules les 15 premières sont gardées
        assert len(result["langages_techniques"]) <= 15

    @patch("app.services.simple_analyzer.st")
    def test_analyze_cv_content_with_error(self, mock_st):
        """Test gestion d'erreur pendant l'analyse"""
        # Simuler une erreur en patchant une partie du code
        with patch.object(SimpleDocumentAnalyzer, "TECHNOLOGIES", side_effect=Exception("Test error")):
            result = SimpleDocumentAnalyzer.analyze_cv_content("test", "Test")

        # Le résultat devrait quand même être retourné avec les valeurs par défaut
        assert result["consultant"] == "Test"
        assert result["langages_techniques"] == []
        assert result["missions"] == []
        assert result["competences_fonctionnelles"] == []

    def test_technologies_list(self):
        """Test que la liste des technologies est correctement définie"""
        assert len(SimpleDocumentAnalyzer.TECHNOLOGIES) > 0
        assert "Python" in SimpleDocumentAnalyzer.TECHNOLOGIES
        assert "Java" in SimpleDocumentAnalyzer.TECHNOLOGIES
        assert "SQL" in SimpleDocumentAnalyzer.TECHNOLOGIES

    def test_clients_list(self):
        """Test que la liste des clients est correctement définie"""
        assert len(SimpleDocumentAnalyzer.CLIENTS) > 0
        assert "BNP Paribas" in SimpleDocumentAnalyzer.CLIENTS
        assert "Société Générale" in SimpleDocumentAnalyzer.CLIENTS
        assert "Quanteam" in SimpleDocumentAnalyzer.CLIENTS
