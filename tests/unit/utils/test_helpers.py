"""
Tests unitaires pour app/utils/helpers.py
Tests des fonctions utilitaires : formatage, validation, calcul, manipulation
"""

from datetime import date
from datetime import datetime
from datetime import timedelta
from io import BytesIO

import pandas as pd
import pytest

from app.utils.helpers import calculate_age
from app.utils.helpers import calculate_experience_years
from app.utils.helpers import calculate_mission_duration
from app.utils.helpers import calculate_percentage_change
from app.utils.helpers import calculate_tjm
from app.utils.helpers import clean_string
from app.utils.helpers import convert_to_dataframe
from app.utils.helpers import export_to_csv
from app.utils.helpers import export_to_excel
from app.utils.helpers import format_currency
from app.utils.helpers import format_date
from app.utils.helpers import format_date_french
from app.utils.helpers import format_number
from app.utils.helpers import format_percentage
from app.utils.helpers import format_phone_number
from app.utils.helpers import generate_id
from app.utils.helpers import get_file_extension
from app.utils.helpers import group_by_category
from app.utils.helpers import is_valid_file_type
from app.utils.helpers import normalize_text
from app.utils.helpers import round_to_nearest
from app.utils.helpers import safe_divide
from app.utils.helpers import sanitize_input
from app.utils.helpers import slugify
from app.utils.helpers import split_list_into_chunks
from app.utils.helpers import truncate_text
from app.utils.helpers import validate_date
from app.utils.helpers import validate_email
from app.utils.helpers import validate_phone


# ============================================================================
# Tests de formatage
# ============================================================================


class TestFormatCurrency:
    """Tests pour format_currency"""

    def test_format_currency_basic(self):
        """Test formatage basique"""
        assert format_currency(1234.56) == "1 234,56 €"
        assert format_currency(100) == "100,00 €"
        assert format_currency(0) == "0,00 €"

    def test_format_currency_large_numbers(self):
        """Test avec grands nombres"""
        assert format_currency(1000000) == "1 000 000,00 €"
        assert format_currency(123456789.99) == "123 456 789,99 €"

    def test_format_currency_negative(self):
        """Test avec nombres négatifs"""
        result = format_currency(-500)
        assert "500" in result
        assert "€" in result

    def test_format_currency_none(self):
        """Test avec None"""
        assert format_currency(None) == "0,00 €"

    def test_format_currency_invalid(self):
        """Test avec valeurs invalides"""
        assert format_currency("invalid") == "0,00 €"


class TestFormatDate:
    """Tests pour format_date"""

    def test_format_date_datetime(self):
        """Test avec datetime"""
        dt = datetime(2024, 3, 15, 10, 30)
        assert format_date(dt) == "15/03/2024"

    def test_format_date_date(self):
        """Test avec date"""
        d = date(2024, 12, 31)
        assert format_date(d) == "31/12/2024"

    def test_format_date_none(self):
        """Test avec None"""
        assert format_date(None) == ""

    def test_format_date_invalid(self):
        """Test avec valeur invalide"""
        result = format_date("invalid")
        assert isinstance(result, str)


class TestFormatPercentage:
    """Tests pour format_percentage"""

    def test_format_percentage_basic(self):
        """Test formatage basique"""
        assert format_percentage(0.85) == "85,0%"
        assert format_percentage(0.5) == "50,0%"
        assert format_percentage(1.0) == "100,0%"

    def test_format_percentage_zero(self):
        """Test avec zéro"""
        assert format_percentage(0) == "0,0%"

    def test_format_percentage_none(self):
        """Test avec None"""
        assert format_percentage(None) == "0,0%"

    def test_format_percentage_invalid(self):
        """Test avec valeur invalide"""
        assert format_percentage("invalid") == "0,0%"


class TestFormatNumber:
    """Tests pour format_number"""

    def test_format_number_integer(self):
        """Test avec entiers"""
        assert format_number(1234) == "1 234"
        assert format_number(1000000) == "1 000 000"

    def test_format_number_float(self):
        """Test avec flottants"""
        result = format_number(1234.56)
        assert "1 234" in result

    def test_format_number_zero(self):
        """Test avec zéro"""
        assert format_number(0) == "0"

    def test_format_number_none(self):
        """Test avec None"""
        assert format_number(None) == "0"


class TestFormatPhoneNumber:
    """Tests pour format_phone_number"""

    def test_format_phone_number_basic(self):
        """Test formatage basique"""
        assert format_phone_number("0612345678") == "06 12 34 56 78"
        assert format_phone_number("0123456789") == "01 23 45 67 89"

    def test_format_phone_number_with_spaces(self):
        """Test avec espaces existants"""
        assert format_phone_number("06 12 34 56 78") == "06 12 34 56 78"

    def test_format_phone_number_with_special_chars(self):
        """Test avec caractères spéciaux"""
        assert format_phone_number("06-12-34-56-78") == "06 12 34 56 78"
        assert format_phone_number("06.12.34.56.78") == "06 12 34 56 78"

    def test_format_phone_number_empty(self):
        """Test avec chaîne vide"""
        assert format_phone_number("") == ""
        assert format_phone_number(None) == ""

    def test_format_phone_number_invalid_length(self):
        """Test avec longueur invalide"""
        result = format_phone_number("123")
        assert result == "123"


class TestFormatDateFrench:
    """Tests pour format_date_french"""

    def test_format_date_french_basic(self):
        """Test formatage basique"""
        d = date(2024, 1, 15)
        assert format_date_french(d) == "15 janvier 2024"

    def test_format_date_french_months(self):
        """Test différents mois"""
        assert format_date_french(date(2024, 3, 10)) == "10 mars 2024"
        assert format_date_french(date(2024, 8, 25)) == "25 août 2024"
        assert format_date_french(date(2024, 12, 31)) == "31 décembre 2024"

    def test_format_date_french_datetime(self):
        """Test avec datetime"""
        dt = datetime(2024, 7, 14, 10, 30)
        assert format_date_french(dt) == "14 juillet 2024"

    def test_format_date_french_none(self):
        """Test avec None"""
        assert format_date_french(None) == ""


# ============================================================================
# Tests de validation
# ============================================================================


class TestValidateEmail:
    """Tests pour validate_email"""

    def test_validate_email_valid(self):
        """Test emails valides"""
        assert validate_email("test@example.com") is True
        assert validate_email("jean.dupont@societe.fr") is True
        assert validate_email("user+tag@domain.co.uk") is True

    def test_validate_email_invalid(self):
        """Test emails invalides"""
        assert validate_email("invalid") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
        assert validate_email("user @example.com") is False

    def test_validate_email_empty(self):
        """Test avec valeurs vides"""
        assert validate_email("") is False
        assert validate_email(None) is False

    def test_validate_email_with_spaces(self):
        """Test avec espaces"""
        assert validate_email("  test@example.com  ") is True


class TestValidatePhone:
    """Tests pour validate_phone"""

    def test_validate_phone_valid_french(self):
        """Test numéros français valides"""
        assert validate_phone("0612345678") is True
        assert validate_phone("06 12 34 56 78") is True
        assert validate_phone("06-12-34-56-78") is True
        assert validate_phone("06.12.34.56.78") is True

    def test_validate_phone_valid_international(self):
        """Test format international"""
        assert validate_phone("+33612345678") is True

    def test_validate_phone_invalid(self):
        """Test numéros invalides"""
        assert validate_phone("123") is False
        assert validate_phone("abcdefghij") is False
        assert validate_phone("06123") is False

    def test_validate_phone_empty(self):
        """Test avec valeurs vides"""
        assert validate_phone("") is False
        assert validate_phone(None) is False


class TestValidateDate:
    """Tests pour validate_date"""

    def test_validate_date_valid_formats(self):
        """Test formats de date valides"""
        assert validate_date("2024-03-15") is True
        assert validate_date("15/03/2024") is True
        assert validate_date("15-03-2024") is True

    def test_validate_date_invalid(self):
        """Test dates invalides"""
        assert validate_date("invalid") is False
        assert validate_date("32/13/2024") is False
        assert validate_date("2024-13-01") is False

    def test_validate_date_empty(self):
        """Test avec valeurs vides"""
        assert validate_date("") is False
        assert validate_date(None) is False


class TestIsValidFileType:
    """Tests pour is_valid_file_type"""

    def test_is_valid_file_type_valid(self):
        """Test extensions valides"""
        assert is_valid_file_type("document.pdf", [".pdf", ".doc"]) is True
        assert is_valid_file_type("image.jpg", [".jpg", ".png"]) is True

    def test_is_valid_file_type_case_insensitive(self):
        """Test insensibilité à la casse"""
        assert is_valid_file_type("Document.PDF", [".pdf"]) is True
        assert is_valid_file_type("image.JPG", [".jpg"]) is True

    def test_is_valid_file_type_invalid(self):
        """Test extensions invalides"""
        assert is_valid_file_type("script.exe", [".pdf", ".doc"]) is False

    def test_is_valid_file_type_empty(self):
        """Test avec valeurs vides"""
        assert is_valid_file_type("", [".pdf"]) is False
        assert is_valid_file_type("file.pdf", []) is False
        assert is_valid_file_type(None, [".pdf"]) is False


# ============================================================================
# Tests de calcul
# ============================================================================


class TestCalculateAge:
    """Tests pour calculate_age"""

    def test_calculate_age_basic(self):
        """Test calcul âge basique"""
        # Personne née il y a 30 ans
        birth_date = date.today() - timedelta(days=30 * 365)
        age = calculate_age(birth_date)
        assert 29 <= age <= 30  # Tolérance pour anniversaire

    def test_calculate_age_birthday_not_passed(self):
        """Test anniversaire non passé cette année"""
        today = date.today()
        # Anniversaire dans le futur cette année
        birth_date = date(today.year - 25, today.month + 1 if today.month < 12 else 1, 1)
        age = calculate_age(birth_date)
        assert age == 24  # Pas encore 25 ans

    def test_calculate_age_birthday_passed(self):
        """Test anniversaire déjà passé"""
        today = date.today()
        # Anniversaire dans le passé cette année
        birth_date = date(today.year - 25, 1, 1)
        age = calculate_age(birth_date)
        assert age == 25

    def test_calculate_age_none(self):
        """Test avec None"""
        assert calculate_age(None) == 0

    def test_calculate_age_negative(self):
        """Test date future (âge négatif)"""
        future_date = date.today() + timedelta(days=365)
        assert calculate_age(future_date) == 0


class TestCalculateExperienceYears:
    """Tests pour calculate_experience_years"""

    def test_calculate_experience_years_basic(self):
        """Test calcul expérience basique"""
        start_date = date.today() - timedelta(days=5 * 365)
        experience = calculate_experience_years(start_date)
        assert 4 <= experience <= 5

    def test_calculate_experience_years_none(self):
        """Test avec None"""
        assert calculate_experience_years(None) == 0

    def test_calculate_experience_years_negative(self):
        """Test date future"""
        future_date = date.today() + timedelta(days=365)
        assert calculate_experience_years(future_date) == 0


class TestSafeDivide:
    """Tests pour safe_divide"""

    def test_safe_divide_basic(self):
        """Test division basique"""
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(7, 2) == 3.5

    def test_safe_divide_by_zero(self):
        """Test division par zéro"""
        assert safe_divide(10, 0) == 0.0

    def test_safe_divide_none(self):
        """Test avec None"""
        assert safe_divide(10, None) == 0.0

    def test_safe_divide_negative(self):
        """Test avec nombres négatifs"""
        assert safe_divide(-10, 2) == -5.0


class TestRoundToNearest:
    """Tests pour round_to_nearest"""

    def test_round_to_nearest_basic(self):
        """Test arrondi basique"""
        assert round_to_nearest(47, 5) == 45.0
        assert round_to_nearest(48, 5) == 50.0

    def test_round_to_nearest_decimal(self):
        """Test arrondi décimal"""
        assert round_to_nearest(1.23, 0.5) == 1.0
        assert round_to_nearest(1.77, 0.5) == 2.0

    def test_round_to_nearest_none(self):
        """Test avec None"""
        assert round_to_nearest(None, 5) == 0.0
        assert round_to_nearest(10, None) == 10.0

    def test_round_to_nearest_zero(self):
        """Test avec zéro"""
        assert round_to_nearest(10, 0) == 10.0


class TestCalculatePercentageChange:
    """Tests pour calculate_percentage_change"""

    def test_calculate_percentage_change_increase(self):
        """Test augmentation"""
        assert calculate_percentage_change(100, 150) == 50.0

    def test_calculate_percentage_change_decrease(self):
        """Test diminution"""
        assert calculate_percentage_change(100, 50) == -50.0

    def test_calculate_percentage_change_no_change(self):
        """Test sans changement"""
        assert calculate_percentage_change(100, 100) == 0.0

    def test_calculate_percentage_change_from_zero(self):
        """Test depuis zéro"""
        assert calculate_percentage_change(0, 100) == 0.0

    def test_calculate_percentage_change_none(self):
        """Test avec None"""
        assert calculate_percentage_change(None, 100) == 0.0


class TestCalculateMissionDuration:
    """Tests pour calculate_mission_duration"""

    def test_calculate_mission_duration_basic(self):
        """Test durée basique"""
        start = date(2024, 1, 1)
        end = date(2024, 6, 1)
        assert calculate_mission_duration(start, end) == 5

    def test_calculate_mission_duration_same_month(self):
        """Test même mois"""
        start = date(2024, 3, 1)
        end = date(2024, 3, 31)
        assert calculate_mission_duration(start, end) >= 1

    def test_calculate_mission_duration_string_dates(self):
        """Test avec dates en string"""
        duration = calculate_mission_duration("2024-01-01", "2024-12-31")
        assert duration == 11

    def test_calculate_mission_duration_none(self):
        """Test avec None"""
        assert calculate_mission_duration(None, date.today()) == 0
        assert calculate_mission_duration(date.today(), None) == 0


class TestCalculateTJM:
    """Tests pour calculate_tjm"""

    def test_calculate_tjm_basic(self):
        """Test calcul TJM basique"""
        tjm = calculate_tjm(50000)  # 50k€ annuel
        assert tjm > 0
        assert isinstance(tjm, float)

    def test_calculate_tjm_custom_days(self):
        """Test avec jours personnalisés"""
        tjm = calculate_tjm(50000, working_days=200)
        assert tjm > 0

    def test_calculate_tjm_zero_salary(self):
        """Test avec salaire zéro"""
        assert calculate_tjm(0) == 0.0

    def test_calculate_tjm_none(self):
        """Test avec None"""
        assert calculate_tjm(None) == 0.0


# ============================================================================
# Tests de manipulation de texte
# ============================================================================


class TestCleanString:
    """Tests pour clean_string"""

    def test_clean_string_basic(self):
        """Test nettoyage basique"""
        assert clean_string("  hello  ") == "hello"
        assert clean_string("hello   world") == "hello world"

    def test_clean_string_control_chars(self):
        """Test suppression caractères de contrôle"""
        result = clean_string("hello\x00world")
        assert result == "helloworld"

    def test_clean_string_empty(self):
        """Test avec valeurs vides"""
        assert clean_string("") == ""
        assert clean_string(None) == ""

    def test_clean_string_multiple_spaces(self):
        """Test espaces multiples"""
        assert clean_string("hello    world    test") == "hello world test"


class TestNormalizeText:
    """Tests pour normalize_text"""

    def test_normalize_text_basic(self):
        """Test normalisation basique"""
        assert normalize_text("HELLO") == "hello"

    def test_normalize_text_accents(self):
        """Test suppression accents"""
        assert normalize_text("éèêë") == "eeee"
        assert normalize_text("àâä") == "aaa"
        assert normalize_text("Élève") == "eleve"

    def test_normalize_text_empty(self):
        """Test avec valeurs vides"""
        assert normalize_text("") == ""
        assert normalize_text(None) == ""


class TestSlugify:
    """Tests pour slugify"""

    def test_slugify_basic(self):
        """Test création slug basique"""
        assert slugify("Hello World") == "hello-world"

    def test_slugify_special_chars(self):
        """Test avec caractères spéciaux"""
        assert slugify("Café & Thé") == "cafe-the"

    def test_slugify_accents(self):
        """Test avec accents"""
        assert slugify("Élève français") == "eleve-francais"

    def test_slugify_multiple_spaces(self):
        """Test avec espaces multiples"""
        assert slugify("hello   world") == "hello-world"

    def test_slugify_empty(self):
        """Test avec valeurs vides"""
        assert slugify("") == ""
        assert slugify(None) == ""


class TestTruncateText:
    """Tests pour truncate_text"""

    def test_truncate_text_no_truncation(self):
        """Test sans troncature nécessaire"""
        assert truncate_text("Hello", 10) == "Hello"

    def test_truncate_text_basic(self):
        """Test troncature basique"""
        result = truncate_text("Hello World Test", 10)
        assert len(result) <= 10
        assert result.endswith("...")

    def test_truncate_text_exact_length(self):
        """Test longueur exacte"""
        assert truncate_text("Hello", 5) == "Hello"

    def test_truncate_text_very_short(self):
        """Test troncature très courte"""
        result = truncate_text("Hello", 3)
        assert len(result) == 3

    def test_truncate_text_empty(self):
        """Test avec valeurs vides"""
        assert truncate_text("", 10) == ""
        assert truncate_text(None, 10) == ""


class TestSanitizeInput:
    """Tests pour sanitize_input"""

    def test_sanitize_input_html_tags(self):
        """Test suppression balises HTML"""
        assert sanitize_input("<p>Hello</p>") == "Hello"
        assert sanitize_input("<div>Test</div>") == "Test"

    def test_sanitize_input_scripts(self):
        """Test suppression scripts"""
        result = sanitize_input("<script>alert('xss')</script>Hello")
        assert "script" not in result.lower()
        assert "Hello" in result

    def test_sanitize_input_special_chars(self):
        """Test échappement caractères spéciaux"""
        result = sanitize_input("<>")
        assert "&lt;" in result
        assert "&gt;" in result

    def test_sanitize_input_empty(self):
        """Test avec valeurs vides"""
        assert sanitize_input("") == ""
        assert sanitize_input(None) == ""


# ============================================================================
# Tests utilitaires
# ============================================================================


class TestGenerateId:
    """Tests pour generate_id"""

    def test_generate_id_format(self):
        """Test format UUID"""
        id1 = generate_id()
        assert isinstance(id1, str)
        assert len(id1) == 36  # Format UUID standard
        assert id1.count("-") == 4

    def test_generate_id_unique(self):
        """Test unicité"""
        id1 = generate_id()
        id2 = generate_id()
        assert id1 != id2


class TestGetFileExtension:
    """Tests pour get_file_extension"""

    def test_get_file_extension_basic(self):
        """Test extraction basique"""
        assert get_file_extension("document.pdf") == ".pdf"
        assert get_file_extension("image.jpg") == ".jpg"

    def test_get_file_extension_multiple_dots(self):
        """Test avec points multiples"""
        assert get_file_extension("archive.tar.gz") == ".gz"

    def test_get_file_extension_no_extension(self):
        """Test sans extension"""
        assert get_file_extension("README") == ""

    def test_get_file_extension_empty(self):
        """Test avec valeurs vides"""
        assert get_file_extension("") == ""
        assert get_file_extension(None) == ""

    def test_get_file_extension_case(self):
        """Test insensibilité à la casse"""
        assert get_file_extension("FILE.PDF") == ".pdf"


class TestSplitListIntoChunks:
    """Tests pour split_list_into_chunks"""

    def test_split_list_basic(self):
        """Test découpage basique"""
        data = [1, 2, 3, 4, 5, 6]
        chunks = split_list_into_chunks(data, 2)
        assert len(chunks) == 3
        assert chunks[0] == [1, 2]
        assert chunks[1] == [3, 4]
        assert chunks[2] == [5, 6]

    def test_split_list_uneven(self):
        """Test découpage inégal"""
        data = [1, 2, 3, 4, 5]
        chunks = split_list_into_chunks(data, 2)
        assert len(chunks) == 3
        assert chunks[2] == [5]

    def test_split_list_chunk_larger(self):
        """Test chunk plus grand que liste"""
        data = [1, 2, 3]
        chunks = split_list_into_chunks(data, 10)
        assert len(chunks) == 1
        assert chunks[0] == [1, 2, 3]

    def test_split_list_empty(self):
        """Test avec liste vide"""
        assert split_list_into_chunks([], 2) == []

    def test_split_list_invalid_size(self):
        """Test avec taille invalide"""
        assert split_list_into_chunks([1, 2, 3], 0) == []
        assert split_list_into_chunks([1, 2, 3], -1) == []


# ============================================================================
# Tests data processing
# ============================================================================


class TestConvertToDataframe:
    """Tests pour convert_to_dataframe"""

    def test_convert_to_dataframe_basic(self):
        """Test conversion basique"""
        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        df = convert_to_dataframe(data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "name" in df.columns
        assert "age" in df.columns

    def test_convert_to_dataframe_empty(self):
        """Test avec liste vide"""
        df = convert_to_dataframe([])
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_convert_to_dataframe_none(self):
        """Test avec None"""
        df = convert_to_dataframe(None)
        assert isinstance(df, pd.DataFrame)
        assert df.empty


class TestExportToCsv:
    """Tests pour export_to_csv"""

    def test_export_to_csv_basic(self):
        """Test export CSV basique"""
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        csv = export_to_csv(df)
        assert isinstance(csv, str)
        assert "A,B" in csv
        assert "1,3" in csv

    def test_export_to_csv_empty(self):
        """Test avec DataFrame vide"""
        df = pd.DataFrame()
        csv = export_to_csv(df)
        assert csv == ""

    def test_export_to_csv_none(self):
        """Test avec None"""
        csv = export_to_csv(None)
        assert csv == ""


class TestExportToExcel:
    """Tests pour export_to_excel"""

    def test_export_to_excel_basic(self):
        """Test export Excel basique"""
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        excel = export_to_excel(df)
        assert isinstance(excel, bytes)
        assert len(excel) > 0

    def test_export_to_excel_empty(self):
        """Test avec DataFrame vide"""
        df = pd.DataFrame()
        excel = export_to_excel(df)
        assert excel == b""

    def test_export_to_excel_none(self):
        """Test avec None"""
        excel = export_to_excel(None)
        assert excel == b""


class TestGroupByCategory:
    """Tests pour group_by_category"""

    def test_group_by_category_basic(self):
        """Test groupement basique"""
        data = [
            {"name": "Alice", "category": "A"},
            {"name": "Bob", "category": "B"},
            {"name": "Charlie", "category": "A"},
        ]
        grouped = group_by_category(data, "category")
        assert len(grouped) == 2
        assert len(grouped["A"]) == 2
        assert len(grouped["B"]) == 1

    def test_group_by_category_missing_key(self):
        """Test avec clé manquante"""
        data = [{"name": "Alice", "category": "A"}, {"name": "Bob"}]
        grouped = group_by_category(data, "category")
        assert "A" in grouped
        assert "Autre" in grouped

    def test_group_by_category_empty(self):
        """Test avec liste vide"""
        grouped = group_by_category([], "category")
        assert grouped == {}

    def test_group_by_category_none(self):
        """Test avec None"""
        grouped = group_by_category(None, "category")
        assert grouped == {}
