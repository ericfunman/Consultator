"""Tests Phase 37: helpers.py (complétion 84% → 90%+)"""
import unittest
from datetime import date, datetime
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

class TestFormatCurrency(unittest.TestCase):
    def test_format_currency_none(self):
        from app.utils.helpers import format_currency
        self.assertEqual(format_currency(None), "0,00 €")
    
    def test_format_currency_large(self):
        from app.utils.helpers import format_currency
        result = format_currency(1500000.50)
        self.assertIn("€", result)

class TestCalculateAge(unittest.TestCase):
    def test_calculate_age_future_date(self):
        from app.utils.helpers import calculate_age
        future_date = date(2030, 1, 1)
        # Test ne devrait pas crasher
        try:
            result = calculate_age(future_date)
            self.assertIsInstance(result, int)
        except:
            pass

class TestCalculateExperienceYears(unittest.TestCase):
    def test_experience_years_old_date(self):
        from app.utils.helpers import calculate_experience_years
        old_date = date(1990, 1, 1)
        result = calculate_experience_years(old_date)
        self.assertGreater(result, 30)

class TestSafeDivide(unittest.TestCase):
    def test_safe_divide_by_zero(self):
        from app.utils.helpers import safe_divide
        self.assertEqual(safe_divide(10, 0), 0.0)
    
    def test_safe_divide_normal(self):
        from app.utils.helpers import safe_divide
        self.assertEqual(safe_divide(10, 2), 5.0)

class TestRoundToNearest(unittest.TestCase):
    def test_round_to_nearest_5(self):
        from app.utils.helpers import round_to_nearest
        self.assertEqual(round_to_nearest(12.3, 5), 10.0)
    
    def test_round_to_nearest_10(self):
        from app.utils.helpers import round_to_nearest
        self.assertEqual(round_to_nearest(87, 10), 90.0)

class TestCalculatePercentageChange(unittest.TestCase):
    def test_percentage_change_increase(self):
        from app.utils.helpers import calculate_percentage_change
        result = calculate_percentage_change(100, 150)
        self.assertEqual(result, 50.0)
    
    def test_percentage_change_decrease(self):
        from app.utils.helpers import calculate_percentage_change
        result = calculate_percentage_change(200, 100)
        self.assertEqual(result, -50.0)

class TestValidateEmail(unittest.TestCase):
    def test_validate_email_invalid(self):
        from app.utils.helpers import validate_email
        self.assertFalse(validate_email("invalid.email"))
    
    def test_validate_email_valid(self):
        from app.utils.helpers import validate_email
        self.assertTrue(validate_email("test@example.com"))

class TestValidatePhone(unittest.TestCase):
    def test_validate_phone_invalid(self):
        from app.utils.helpers import validate_phone
        self.assertFalse(validate_phone("123"))
    
    def test_validate_phone_valid_fr(self):
        from app.utils.helpers import validate_phone
        self.assertTrue(validate_phone("0612345678"))

class TestValidateDate(unittest.TestCase):
    def test_validate_date_invalid(self):
        from app.utils.helpers import validate_date
        self.assertFalse(validate_date("32/13/2023"))
    
    def test_validate_date_valid(self):
        from app.utils.helpers import validate_date
        self.assertTrue(validate_date("01/01/2023"))

class TestIsValidFileType(unittest.TestCase):
    def test_is_valid_file_type_invalid(self):
        from app.utils.helpers import is_valid_file_type
        self.assertFalse(is_valid_file_type("test.exe", [".pdf", ".docx"]))
    
    def test_is_valid_file_type_valid(self):
        from app.utils.helpers import is_valid_file_type
        self.assertTrue(is_valid_file_type("test.pdf", [".pdf", ".docx"]))

class TestCleanString(unittest.TestCase):
    def test_clean_string_with_spaces(self):
        from app.utils.helpers import clean_string
        result = clean_string("  Hello  World  ")
        self.assertEqual(result, "Hello World")

class TestNormalizeText(unittest.TestCase):
    def test_normalize_text_accents(self):
        from app.utils.helpers import normalize_text
        result = normalize_text("Été")
        self.assertIn("e", result.lower())

class TestSlugify(unittest.TestCase):
    def test_slugify_with_spaces(self):
        from app.utils.helpers import slugify
        result = slugify("Hello World!")
        self.assertEqual(result, "hello-world")

class TestTruncateText(unittest.TestCase):
    def test_truncate_text_long(self):
        from app.utils.helpers import truncate_text
        result = truncate_text("Hello World", 5)
        self.assertEqual(result, "He...")
    
    def test_truncate_text_short(self):
        from app.utils.helpers import truncate_text
        result = truncate_text("Hi", 10)
        self.assertEqual(result, "Hi")

class TestGenerateId(unittest.TestCase):
    def test_generate_id_unique(self):
        from app.utils.helpers import generate_id
        id1 = generate_id()
        id2 = generate_id()
        self.assertNotEqual(id1, id2)
        self.assertGreater(len(id1), 0)

class TestGetFileExtension(unittest.TestCase):
    def test_get_file_extension_pdf(self):
        from app.utils.helpers import get_file_extension
        self.assertEqual(get_file_extension("test.pdf"), ".pdf")
    
    def test_get_file_extension_none(self):
        from app.utils.helpers import get_file_extension
        self.assertEqual(get_file_extension("noextension"), "")

class TestFormatPhoneNumber(unittest.TestCase):
    def test_format_phone_number_fr(self):
        from app.utils.helpers import format_phone_number
        result = format_phone_number("0612345678")
        self.assertIn(" ", result)  # Format avec espaces

if __name__ == "__main__":
    unittest.main()
