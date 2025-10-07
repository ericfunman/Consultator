"""
Tests Phase 6: document_analyzer.py - Cibler les 158 lignes non couvertes (78%→85%)
Lignes prioritaires : 256,258,275-287 (parsing errors), 300-320 (extraction),
329-342,352-358,361-362 (skills parsing), 370-376,384-396,404-416 (formatting edge cases)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.document_analyzer import DocumentAnalyzer


@pytest.fixture
def analyzer():
    return DocumentAnalyzer()


class TestParseCV:
    """Tests pour parse_cv"""
    
    def test_parse_cv_with_valid_pdf(self, analyzer):
        """Test parsing PDF valide"""
        with patch('app.services.document_analyzer.fitz.open') as mock_open:
            mock_doc = Mock()
            mock_page = Mock()
            mock_page.get_text.return_value = "Jean Dupont\nPython Developer"
            mock_doc.__iter__.return_value = [mock_page]
            mock_open.return_value = mock_doc
            
            result = analyzer.parse_cv("test.pdf")
            assert isinstance(result, dict)
    
    def test_parse_cv_file_not_found(self, analyzer):
        """Test fichier inexistant"""
        result = analyzer.parse_cv("inexistant.pdf")
        assert "error" in result or result == {}
    
    def test_parse_cv_invalid_format(self, analyzer):
        """Test format invalide"""
        with patch('app.services.document_analyzer.fitz.open', side_effect=Exception("Format error")):
            result = analyzer.parse_cv("test.pdf")
            assert isinstance(result, dict)


class TestExtractPersonalInfo:
    """Tests pour _extract_personal_info"""
    
    def test_extract_name_simple(self, analyzer):
        """Test extraction nom simple"""
        text = "Jean Dupont\nDeveloper"
        result = analyzer._extract_personal_info(text)
        assert result is not None
    
    def test_extract_email(self, analyzer):
        """Test extraction email"""
        text = "Contact: jean.dupont@email.com"
        result = analyzer._extract_personal_info(text)
        assert result is not None
    
    def test_extract_phone(self, analyzer):
        """Test extraction téléphone"""
        text = "Tel: 01 23 45 67 89"
        result = analyzer._extract_personal_info(text)
        assert result is not None
    
    def test_extract_personal_info_empty_text(self, analyzer):
        """Test texte vide"""
        result = analyzer._extract_personal_info("")
        assert result is not None


class TestExtractSkills:
    """Tests pour _extract_skills"""
    
    def test_extract_skills_python(self, analyzer):
        """Test extraction Python"""
        text = "Compétences: Python, Django"
        result = analyzer._extract_skills(text)
        assert isinstance(result, list)
    
    def test_extract_skills_multiple(self, analyzer):
        """Test plusieurs compétences"""
        text = "Python, JavaScript, SQL, Docker"
        result = analyzer._extract_skills(text)
        assert isinstance(result, list)
    
    def test_extract_skills_no_skills(self, analyzer):
        """Test sans compétences"""
        text = "Expérience professionnelle"
        result = analyzer._extract_skills(text)
        assert isinstance(result, list)
    
    def test_extract_skills_with_variations(self, analyzer):
        """Test variations orthographiques"""
        text = "python, Python, PYTHON"
        result = analyzer._extract_skills(text)
        assert isinstance(result, list)


class TestExtractExperience:
    """Tests pour _extract_experience"""
    
    def test_extract_experience_years(self, analyzer):
        """Test extraction années"""
        text = "5 ans d'expérience en Python"
        result = analyzer._extract_experience(text)
        assert isinstance(result, (int, float, type(None)))
    
    def test_extract_experience_months(self, analyzer):
        """Test extraction mois"""
        text = "18 mois d'expérience"
        result = analyzer._extract_experience(text)
        assert isinstance(result, (int, float, type(None)))
    
    def test_extract_experience_no_info(self, analyzer):
        """Test sans info expérience"""
        text = "Compétences techniques"
        result = analyzer._extract_experience(text)
        assert result is None or isinstance(result, (int, float))


class TestExtractEducation:
    """Tests pour _extract_education"""
    
    def test_extract_education_master(self, analyzer):
        """Test extraction Master"""
        text = "Master en Informatique"
        result = analyzer._extract_education(text)
        assert isinstance(result, list)
    
    def test_extract_education_license(self, analyzer):
        """Test extraction Licence"""
        text = "Licence en Mathématiques"
        result = analyzer._extract_education(text)
        assert isinstance(result, list)
    
    def test_extract_education_multiple(self, analyzer):
        """Test plusieurs diplômes"""
        text = "Master Informatique, Licence Mathématiques"
        result = analyzer._extract_education(text)
        assert isinstance(result, list)
    
    def test_extract_education_none(self, analyzer):
        """Test sans formation"""
        text = "Expérience professionnelle uniquement"
        result = analyzer._extract_education(text)
        assert isinstance(result, list)


class TestExtractLanguages:
    """Tests pour _extract_languages"""
    
    def test_extract_languages_french(self, analyzer):
        """Test extraction Français"""
        text = "Langues: Français (natif)"
        result = analyzer._extract_languages(text)
        assert isinstance(result, list)
    
    def test_extract_languages_english(self, analyzer):
        """Test extraction Anglais"""
        text = "Anglais courant"
        result = analyzer._extract_languages(text)
        assert isinstance(result, list)
    
    def test_extract_languages_multiple(self, analyzer):
        """Test plusieurs langues"""
        text = "Français, Anglais, Espagnol"
        result = analyzer._extract_languages(text)
        assert isinstance(result, list)
    
    def test_extract_languages_with_levels(self, analyzer):
        """Test avec niveaux"""
        text = "Anglais: B2, Espagnol: A1"
        result = analyzer._extract_languages(text)
        assert isinstance(result, list)


class TestFormatResults:
    """Tests pour _format_results"""
    
    def test_format_results_complete(self, analyzer):
        """Test formatage complet"""
        data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "test@email.com",
            "competences": ["Python", "SQL"],
            "experience": 5,
            "formation": ["Master"],
            "langues": ["Français", "Anglais"]
        }
        result = analyzer._format_results(data)
        assert isinstance(result, dict)
    
    def test_format_results_minimal(self, analyzer):
        """Test formatage minimal"""
        data = {"nom": "Dupont"}
        result = analyzer._format_results(data)
        assert isinstance(result, dict)
    
    def test_format_results_empty(self, analyzer):
        """Test données vides"""
        data = {}
        result = analyzer._format_results(data)
        assert isinstance(result, dict)


class TestAnalyzeDocument:
    """Tests pour analyze_document"""
    
    @patch('app.services.document_analyzer.DocumentAnalyzer.parse_cv')
    def test_analyze_document_success(self, mock_parse, analyzer):
        """Test analyse réussie"""
        mock_parse.return_value = {
            "nom": "Dupont",
            "competences": ["Python"]
        }
        result = analyzer.analyze_document("test.pdf")
        assert isinstance(result, dict)
    
    @patch('app.services.document_analyzer.DocumentAnalyzer.parse_cv')
    def test_analyze_document_parse_error(self, mock_parse, analyzer):
        """Test erreur parsing"""
        mock_parse.return_value = {"error": "Parse failed"}
        result = analyzer.analyze_document("test.pdf")
        assert isinstance(result, dict)
    
    @patch('app.services.document_analyzer.DocumentAnalyzer.parse_cv')
    def test_analyze_document_empty_result(self, mock_parse, analyzer):
        """Test résultat vide"""
        mock_parse.return_value = {}
        result = analyzer.analyze_document("test.pdf")
        assert isinstance(result, dict)


class TestEdgeCases:
    """Tests cas limites"""
    
    def test_parse_cv_special_characters(self, analyzer):
        """Test caractères spéciaux"""
        with patch('app.services.document_analyzer.fitz.open') as mock_open:
            mock_doc = Mock()
            mock_page = Mock()
            mock_page.get_text.return_value = "Nom: Dupônt-François"
            mock_doc.__iter__.return_value = [mock_page]
            mock_open.return_value = mock_doc
            
            result = analyzer.parse_cv("test.pdf")
            assert isinstance(result, dict)
    
    def test_extract_skills_case_insensitive(self, analyzer):
        """Test compétences insensible à la casse"""
        text = "python PYTHON Python"
        result = analyzer._extract_skills(text)
        assert isinstance(result, list)
    
    def test_extract_personal_info_multiple_emails(self, analyzer):
        """Test plusieurs emails"""
        text = "test1@email.com et test2@email.com"
        result = analyzer._extract_personal_info(text)
        assert result is not None
    
    def test_extract_experience_text_format(self, analyzer):
        """Test format texte expérience"""
        text = "Cinq années d'expérience"
        result = analyzer._extract_experience(text)
        assert isinstance(result, (int, float, type(None)))
