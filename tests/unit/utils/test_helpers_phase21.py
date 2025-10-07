"""
Tests Phase 21 FINALE: Helpers.py - 74.9% -> 95%+!
Ciblage: 72 lignes manquantes dans helpers.py
Focus: Fonctions formatting, validation, calcul, data processing
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import date, datetime
import pandas as pd


class TestFormattingFunctions(unittest.TestCase):
    """Tests des fonctions de formatage"""

    def test_format_currency_positive(self):
        """Test formatage montant positif"""
        from app.utils.helpers import format_currency
        
        result = format_currency(1234.56)
        assert "1" in result
        assert "234" in result
        assert "€" in result

    def test_format_currency_none(self):
        """Test formatage montant None"""
        from app.utils.helpers import format_currency
        
        result = format_currency(None)
        assert result == "0,00 €"

    def test_format_currency_invalid(self):
        """Test formatage montant invalide"""
        from app.utils.helpers import format_currency
        
        result = format_currency("invalid")
        assert result == "0,00 €"

    def test_format_date_datetime(self):
        """Test formatage datetime"""
        from app.utils.helpers import format_date
        
        dt = datetime(2024, 3, 15)
        result = format_date(dt)
        assert result == "15/03/2024"

    def test_format_date_date(self):
        """Test formatage date"""
        from app.utils.helpers import format_date
        
        d = date(2024, 12, 25)
        result = format_date(d)
        assert result == "25/12/2024"

    def test_format_date_none(self):
        """Test formatage date None"""
        from app.utils.helpers import format_date
        
        result = format_date(None)
        assert result == ""

    def test_format_date_invalid(self):
        """Test formatage date invalide"""
        from app.utils.helpers import format_date
        
        result = format_date("not a date")
        assert isinstance(result, str)

    def test_format_percentage_valid(self):
        """Test formatage pourcentage"""
        from app.utils.helpers import format_percentage
        
        result = format_percentage(0.85)
        assert "85" in result
        assert "%" in result

    def test_format_percentage_none(self):
        """Test formatage pourcentage None"""
        from app.utils.helpers import format_percentage
        
        result = format_percentage(None)
        assert result == "0,0%"

    def test_format_number_integer(self):
        """Test formatage nombre entier"""
        from app.utils.helpers import format_number
        
        result = format_number(1234)
        assert "1" in result
        assert "234" in result

    def test_format_number_float(self):
        """Test formatage nombre flottant"""
        from app.utils.helpers import format_number
        
        result = format_number(1234.56)
        assert "1" in result

    def test_format_number_none(self):
        """Test formatage nombre None"""
        from app.utils.helpers import format_number
        
        result = format_number(None)
        assert result == "0"


class TestCalculationFunctions(unittest.TestCase):
    """Tests des fonctions de calcul"""

    def test_calculate_age_valid(self):
        """Test calcul âge valide"""
        from app.utils.helpers import calculate_age
        
        birth = date(1990, 6, 15)
        age = calculate_age(birth)
        assert age > 0
        assert age < 150

    def test_calculate_age_none(self):
        """Test calcul âge None"""
        from app.utils.helpers import calculate_age
        
        age = calculate_age(None)
        assert age == 0

    def test_calculate_experience_years_valid(self):
        """Test calcul années expérience"""
        from app.utils.helpers import calculate_experience_years
        
        start = date(2015, 1, 1)
        years = calculate_experience_years(start)
        assert years >= 0

    def test_calculate_experience_years_none(self):
        """Test calcul expérience None"""
        from app.utils.helpers import calculate_experience_years
        
        years = calculate_experience_years(None)
        assert years == 0

    def test_safe_divide_valid(self):
        """Test division sécurisée valide"""
        from app.utils.helpers import safe_divide
        
        result = safe_divide(10, 2)
        assert result == 5.0

    def test_safe_divide_by_zero(self):
        """Test division par zéro"""
        from app.utils.helpers import safe_divide
        
        result = safe_divide(10, 0)
        assert result == 0.0

    def test_safe_divide_none_denominator(self):
        """Test division dénominateur None"""
        from app.utils.helpers import safe_divide
        
        result = safe_divide(10, None)
        assert result == 0.0

    def test_round_to_nearest_valid(self):
        """Test arrondi valide"""
        from app.utils.helpers import round_to_nearest
        
        result = round_to_nearest(12.3, 5)
        assert isinstance(result, float)

    def test_round_to_nearest_none(self):
        """Test arrondi None"""
        from app.utils.helpers import round_to_nearest
        
        result = round_to_nearest(None, 5)
        assert result == 0.0

    def test_calculate_percentage_change_valid(self):
        """Test changement pourcentage valide"""
        from app.utils.helpers import calculate_percentage_change
        
        result = calculate_percentage_change(100, 150)
        assert result == 50.0

    def test_calculate_percentage_change_zero_old(self):
        """Test changement avec ancienne valeur zéro"""
        from app.utils.helpers import calculate_percentage_change
        
        result = calculate_percentage_change(0, 100)
        assert result == 0.0


class TestValidationFunctions(unittest.TestCase):
    """Tests des fonctions de validation"""

    def test_validate_email_valid(self):
        """Test validation email valide"""
        from app.utils.helpers import validate_email
        
        assert validate_email("test@example.com") is True

    def test_validate_email_invalid(self):
        """Test validation email invalide"""
        from app.utils.helpers import validate_email
        
        assert validate_email("not-an-email") is False

    def test_validate_email_none(self):
        """Test validation email None"""
        from app.utils.helpers import validate_email
        
        assert validate_email(None) is False

    def test_validate_phone_valid(self):
        """Test validation téléphone valide"""
        from app.utils.helpers import validate_phone
        
        assert validate_phone("0612345678") is True

    def test_validate_phone_with_spaces(self):
        """Test validation téléphone avec espaces"""
        from app.utils.helpers import validate_phone
        
        assert validate_phone("06 12 34 56 78") is True

    def test_validate_phone_international(self):
        """Test validation téléphone international"""
        from app.utils.helpers import validate_phone
        
        assert validate_phone("+33612345678") is True

    def test_validate_phone_invalid(self):
        """Test validation téléphone invalide"""
        from app.utils.helpers import validate_phone
        
        assert validate_phone("123") is False

    def test_validate_date_valid_iso(self):
        """Test validation date ISO"""
        from app.utils.helpers import validate_date
        
        assert validate_date("2024-03-15") is True

    def test_validate_date_valid_fr(self):
        """Test validation date format français"""
        from app.utils.helpers import validate_date
        
        assert validate_date("15/03/2024") is True

    def test_validate_date_invalid(self):
        """Test validation date invalide"""
        from app.utils.helpers import validate_date
        
        assert validate_date("not-a-date") is False


class TestStringManipulation(unittest.TestCase):
    """Tests des fonctions de manipulation de chaînes"""

    def test_clean_string_valid(self):
        """Test nettoyage chaîne valide"""
        from app.utils.helpers import clean_string
        
        result = clean_string("  Hello   World  ")
        assert result == "Hello World"

    def test_clean_string_control_chars(self):
        """Test nettoyage caractères contrôle"""
        from app.utils.helpers import clean_string
        
        result = clean_string("Hello\x00World")
        assert "\x00" not in result

    def test_normalize_text_with_accents(self):
        """Test normalisation avec accents"""
        from app.utils.helpers import normalize_text
        
        result = normalize_text("Éléphant")
        assert "e" in result
        assert result.islower()

    def test_slugify_text(self):
        """Test création slug"""
        from app.utils.helpers import slugify
        
        result = slugify("Hello World!")
        assert result == "hello-world"

    def test_slugify_with_accents(self):
        """Test slug avec accents"""
        from app.utils.helpers import slugify
        
        result = slugify("Café Français")
        assert "cafe" in result
        assert "francais" in result

    def test_truncate_text_short(self):
        """Test troncature texte court"""
        from app.utils.helpers import truncate_text
        
        result = truncate_text("Hello", 10)
        assert result == "Hello"

    def test_truncate_text_long(self):
        """Test troncature texte long"""
        from app.utils.helpers import truncate_text
        
        result = truncate_text("Hello World This Is Long", 15)
        assert len(result) <= 15
        assert "..." in result

    def test_truncate_text_exact_length(self):
        """Test troncature longueur exacte"""
        from app.utils.helpers import truncate_text
        
        result = truncate_text("Hello", 5)
        assert result == "Hello"


class TestFileOperations(unittest.TestCase):
    """Tests des fonctions de gestion de fichiers"""

    def test_is_valid_file_type_pdf(self):
        """Test validation type fichier PDF"""
        from app.utils.helpers import is_valid_file_type
        
        assert is_valid_file_type("document.pdf", [".pdf", ".docx"]) is True

    def test_is_valid_file_type_invalid(self):
        """Test validation type fichier invalide"""
        from app.utils.helpers import is_valid_file_type
        
        assert is_valid_file_type("document.exe", [".pdf", ".docx"]) is False

    def test_get_file_extension_pdf(self):
        """Test extraction extension PDF"""
        from app.utils.helpers import get_file_extension
        
        result = get_file_extension("document.pdf")
        assert result == ".pdf"

    def test_get_file_extension_none(self):
        """Test extraction extension None"""
        from app.utils.helpers import get_file_extension
        
        result = get_file_extension(None)
        assert result == ""


class TestPhoneFormatting(unittest.TestCase):
    """Tests du formatage de téléphone"""

    def test_format_phone_number_valid(self):
        """Test formatage téléphone valide"""
        from app.utils.helpers import format_phone_number
        
        result = format_phone_number("0612345678")
        assert "06" in result
        assert " " in result

    def test_format_phone_number_none(self):
        """Test formatage téléphone None"""
        from app.utils.helpers import format_phone_number
        
        result = format_phone_number(None)
        assert result == ""

    def test_format_phone_number_with_spaces(self):
        """Test formatage téléphone avec espaces"""
        from app.utils.helpers import format_phone_number
        
        result = format_phone_number("06 12 34 56 78")
        assert "06" in result


class TestDateFormatting(unittest.TestCase):
    """Tests du formatage de dates"""

    def test_format_date_french_valid(self):
        """Test formatage date français"""
        from app.utils.helpers import format_date_french
        
        d = date(2024, 1, 15)
        result = format_date_french(d)
        assert "15" in result
        assert "janvier" in result
        assert "2024" in result

    def test_format_date_french_none(self):
        """Test formatage date français None"""
        from app.utils.helpers import format_date_french
        
        result = format_date_french(None)
        assert result == ""


class TestSecurityFunctions(unittest.TestCase):
    """Tests des fonctions de sécurité"""

    def test_sanitize_input_html(self):
        """Test nettoyage HTML"""
        from app.utils.helpers import sanitize_input
        
        result = sanitize_input("<script>alert('xss')</script>Hello")
        assert "<script>" not in result
        assert "Hello" in result

    def test_sanitize_input_special_chars(self):
        """Test nettoyage caractères spéciaux"""
        from app.utils.helpers import sanitize_input
        
        result = sanitize_input("<div>Test</div>")
        assert "&lt;" in result or "Test" in result


class TestMissionCalculations(unittest.TestCase):
    """Tests des calculs de mission"""

    def test_calculate_mission_duration_valid(self):
        """Test calcul durée mission valide"""
        from app.utils.helpers import calculate_mission_duration
        
        start = date(2024, 1, 1)
        end = date(2024, 6, 30)
        result = calculate_mission_duration(start, end)
        assert result >= 5

    def test_calculate_mission_duration_none(self):
        """Test calcul durée mission None"""
        from app.utils.helpers import calculate_mission_duration
        
        result = calculate_mission_duration(None, None)
        assert result == 0

    def test_calculate_tjm_valid(self):
        """Test calcul TJM valide"""
        from app.utils.helpers import calculate_tjm
        
        result = calculate_tjm(50000)
        assert result > 0

    def test_calculate_tjm_zero(self):
        """Test calcul TJM avec salaire zéro"""
        from app.utils.helpers import calculate_tjm
        
        result = calculate_tjm(0)
        assert result == 0.0


class TestUtilityFunctions(unittest.TestCase):
    """Tests des fonctions utilitaires"""

    def test_split_list_into_chunks_valid(self):
        """Test division liste en chunks"""
        from app.utils.helpers import split_list_into_chunks
        
        data = [1, 2, 3, 4, 5, 6, 7, 8]
        result = split_list_into_chunks(data, 3)
        assert len(result) == 3
        assert result[0] == [1, 2, 3]

    def test_split_list_into_chunks_empty(self):
        """Test division liste vide"""
        from app.utils.helpers import split_list_into_chunks
        
        result = split_list_into_chunks([], 3)
        assert result == []

    def test_generate_id(self):
        """Test génération ID unique"""
        from app.utils.helpers import generate_id
        
        id1 = generate_id()
        id2 = generate_id()
        assert id1 != id2
        assert isinstance(id1, str)


class TestDataProcessing(unittest.TestCase):
    """Tests du traitement de données"""

    def test_convert_to_dataframe_valid(self):
        """Test conversion en DataFrame"""
        from app.utils.helpers import convert_to_dataframe
        
        data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
        df = convert_to_dataframe(data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

    def test_convert_to_dataframe_empty(self):
        """Test conversion liste vide"""
        from app.utils.helpers import convert_to_dataframe
        
        df = convert_to_dataframe([])
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_export_to_csv_valid(self):
        """Test export CSV"""
        from app.utils.helpers import export_to_csv
        
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        result = export_to_csv(df)
        assert "col1" in result
        assert isinstance(result, str)

    def test_export_to_csv_empty(self):
        """Test export CSV vide"""
        from app.utils.helpers import export_to_csv
        
        df = pd.DataFrame()
        result = export_to_csv(df)
        assert result == ""

    def test_export_to_excel_valid(self):
        """Test export Excel"""
        from app.utils.helpers import export_to_excel
        
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        result = export_to_excel(df)
        assert isinstance(result, bytes)

    def test_export_to_excel_empty(self):
        """Test export Excel vide"""
        from app.utils.helpers import export_to_excel
        
        df = pd.DataFrame()
        result = export_to_excel(df)
        assert result == b""

    def test_group_by_category_valid(self):
        """Test groupement par catégorie"""
        from app.utils.helpers import group_by_category
        
        data = [
            {"name": "A", "category": "Cat1"},
            {"name": "B", "category": "Cat1"},
            {"name": "C", "category": "Cat2"}
        ]
        result = group_by_category(data, "category")
        assert "Cat1" in result
        assert len(result["Cat1"]) == 2

    def test_group_by_category_empty(self):
        """Test groupement liste vide"""
        from app.utils.helpers import group_by_category
        
        result = group_by_category([], "category")
        assert result == {}


if __name__ == "__main__":
    unittest.main()
