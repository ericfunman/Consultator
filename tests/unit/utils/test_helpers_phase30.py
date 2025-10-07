"""
Tests unitaires pour helpers.py - Phase 30
Coverage target: 84% → 92%+ (gain estimé +8%)

Stratégie:
- Fonctions de validation (email, phone, date, file_type)
- Fonctions de manipulation texte (clean_string, normalize_text, slugify)
- Fonctions utilitaires (split_list_into_chunks, generate_id, get_file_extension)
- Cas limites et gestion d'erreurs

Fonctions clés à tester (~46 lignes manquantes):
- validate_email, validate_phone, validate_date, is_valid_file_type
- clean_string, normalize_text, slugify, truncate_text
- split_list_into_chunks, generate_id, get_file_extension
- format_phone_number, round_to_nearest, calculate_percentage_change
"""

import unittest
from datetime import date, datetime
import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


class TestValidateEmail(unittest.TestCase):
    """Tests pour validate_email"""

    def test_validate_email_valid(self):
        """Test email valide"""
        from app.utils.helpers import validate_email

        self.assertTrue(validate_email("user@example.com"))
        self.assertTrue(validate_email("test.user+tag@domain.co.uk"))
        self.assertTrue(validate_email("user123@test-domain.fr"))

    def test_validate_email_invalid(self):
        """Test email invalide"""
        from app.utils.helpers import validate_email

        self.assertFalse(validate_email("invalid"))
        self.assertFalse(validate_email("@example.com"))
        self.assertFalse(validate_email("user@"))
        self.assertFalse(validate_email("user @example.com"))
        self.assertFalse(validate_email(""))

    def test_validate_email_none(self):
        """Test email None"""
        from app.utils.helpers import validate_email

        self.assertFalse(validate_email(None))

    def test_validate_email_with_spaces(self):
        """Test email avec espaces (trimmed)"""
        from app.utils.helpers import validate_email

        self.assertTrue(validate_email("  user@example.com  "))


class TestValidatePhone(unittest.TestCase):
    """Tests pour validate_phone"""

    def test_validate_phone_french_format(self):
        """Test numéro français 10 chiffres"""
        from app.utils.helpers import validate_phone

        self.assertTrue(validate_phone("0123456789"))
        self.assertTrue(validate_phone("06 12 34 56 78"))
        self.assertTrue(validate_phone("01-23-45-67-89"))

    def test_validate_phone_international_format(self):
        """Test numéro international +33"""
        from app.utils.helpers import validate_phone

        self.assertTrue(validate_phone("+33123456789"))
        self.assertTrue(validate_phone("+33 1 23 45 67 89"))

    def test_validate_phone_invalid(self):
        """Test numéro invalide"""
        from app.utils.helpers import validate_phone

        self.assertFalse(validate_phone("123"))
        self.assertFalse(validate_phone("abcdefghij"))
        self.assertFalse(validate_phone(""))
        self.assertFalse(validate_phone(None))

    def test_validate_phone_wrong_length(self):
        """Test numéro mauvaise longueur"""
        from app.utils.helpers import validate_phone

        self.assertFalse(validate_phone("012345678"))  # 9 chiffres
        self.assertFalse(validate_phone("+3312345678"))  # 11 chiffres après +33


class TestValidateDate(unittest.TestCase):
    """Tests pour validate_date"""

    def test_validate_date_valid_formats(self):
        """Test dates valides différents formats"""
        from app.utils.helpers import validate_date

        self.assertTrue(validate_date("01/01/2024"))
        self.assertTrue(validate_date("2024-01-01"))
        self.assertTrue(validate_date("01-01-2024"))

    def test_validate_date_invalid(self):
        """Test dates invalides"""
        from app.utils.helpers import validate_date

        self.assertFalse(validate_date("invalid"))
        self.assertFalse(validate_date("32/13/2024"))  # Date impossible
        self.assertFalse(validate_date(""))
        self.assertFalse(validate_date(None))


class TestIsValidFileType(unittest.TestCase):
    """Tests pour is_valid_file_type"""

    def test_is_valid_file_type_valid(self):
        """Test type de fichier valide"""
        from app.utils.helpers import is_valid_file_type

        allowed = [".pdf", ".docx", ".txt"]
        self.assertTrue(is_valid_file_type("document.pdf", allowed))
        self.assertTrue(is_valid_file_type("report.docx", allowed))
        self.assertTrue(is_valid_file_type("file.txt", allowed))

    def test_is_valid_file_type_invalid(self):
        """Test type de fichier invalide"""
        from app.utils.helpers import is_valid_file_type

        allowed = [".pdf", ".docx"]
        self.assertFalse(is_valid_file_type("image.jpg", allowed))
        self.assertFalse(is_valid_file_type("script.py", allowed))

    def test_is_valid_file_type_no_extension(self):
        """Test fichier sans extension"""
        from app.utils.helpers import is_valid_file_type

        allowed = [".pdf"]
        self.assertFalse(is_valid_file_type("file", allowed))

    def test_is_valid_file_type_case_insensitive(self):
        """Test casse ignorée"""
        from app.utils.helpers import is_valid_file_type

        allowed = [".pdf"]
        self.assertTrue(is_valid_file_type("document.PDF", allowed))


class TestCleanString(unittest.TestCase):
    """Tests pour clean_string"""

    def test_clean_string_basic(self):
        """Test nettoyage basique"""
        from app.utils.helpers import clean_string

        result = clean_string("  Hello World  ")
        self.assertEqual(result, "Hello World")

    def test_clean_string_multiple_spaces(self):
        """Test nettoyage espaces multiples"""
        from app.utils.helpers import clean_string

        result = clean_string("Hello    World")
        self.assertEqual(result, "Hello World")

    def test_clean_string_newlines(self):
        """Test nettoyage sauts de ligne"""
        from app.utils.helpers import clean_string

        result = clean_string("Hello\nWorld\n")
        self.assertNotIn("\n", result)

    def test_clean_string_empty(self):
        """Test chaîne vide"""
        from app.utils.helpers import clean_string

        result = clean_string("")
        self.assertEqual(result, "")


class TestNormalizeText(unittest.TestCase):
    """Tests pour normalize_text"""

    def test_normalize_text_accents(self):
        """Test normalisation accents"""
        from app.utils.helpers import normalize_text

        result = normalize_text("Café")
        self.assertEqual(result, "cafe")

    def test_normalize_text_special_chars(self):
        """Test normalisation retire les accents (pas les symboles)"""
        from app.utils.helpers import normalize_text

        result = normalize_text("Hôtel & Restaurant")
        self.assertNotIn("ô", result)  # Accent retiré
        self.assertIn("&", result)  # Symbole conservé (normalize_text ne les retire pas)

    def test_normalize_text_lowercase(self):
        """Test conversion minuscules"""
        from app.utils.helpers import normalize_text

        result = normalize_text("HELLO WORLD")
        self.assertEqual(result, "hello world")


class TestSlugify(unittest.TestCase):
    """Tests pour slugify"""

    def test_slugify_basic(self):
        """Test slugification basique"""
        from app.utils.helpers import slugify

        result = slugify("Hello World")
        self.assertEqual(result, "hello-world")

    def test_slugify_accents(self):
        """Test slugification avec accents"""
        from app.utils.helpers import slugify

        result = slugify("Café crème")
        self.assertEqual(result, "cafe-creme")

    def test_slugify_special_chars(self):
        """Test slugification caractères spéciaux"""
        from app.utils.helpers import slugify

        result = slugify("Hello & World!")
        self.assertNotIn("&", result)
        self.assertNotIn("!", result)

    def test_slugify_multiple_spaces(self):
        """Test slugification espaces multiples"""
        from app.utils.helpers import slugify

        result = slugify("Hello    World")
        self.assertEqual(result, "hello-world")


class TestTruncateText(unittest.TestCase):
    """Tests pour truncate_text"""

    def test_truncate_text_short(self):
        """Test texte plus court que limite"""
        from app.utils.helpers import truncate_text

        result = truncate_text("Hello", 10)
        self.assertEqual(result, "Hello")

    def test_truncate_text_long(self):
        """Test texte plus long que limite"""
        from app.utils.helpers import truncate_text

        result = truncate_text("Hello World", 5)
        self.assertLessEqual(len(result), 8)  # 5 + "..."
        self.assertTrue(result.endswith("..."))

    def test_truncate_text_exact(self):
        """Test texte exactement à la limite"""
        from app.utils.helpers import truncate_text

        result = truncate_text("Hello", 5)
        self.assertEqual(result, "Hello")


class TestSplitListIntoChunks(unittest.TestCase):
    """Tests pour split_list_into_chunks"""

    def test_split_list_into_chunks_even(self):
        """Test découpage liste taille exacte"""
        from app.utils.helpers import split_list_into_chunks

        data = [1, 2, 3, 4, 5, 6]
        result = split_list_into_chunks(data, 2)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], [1, 2])
        self.assertEqual(result[1], [3, 4])
        self.assertEqual(result[2], [5, 6])

    def test_split_list_into_chunks_uneven(self):
        """Test découpage liste taille inexacte"""
        from app.utils.helpers import split_list_into_chunks

        data = [1, 2, 3, 4, 5]
        result = split_list_into_chunks(data, 2)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[-1], [5])  # Dernier chunk incomplet

    def test_split_list_into_chunks_empty(self):
        """Test découpage liste vide"""
        from app.utils.helpers import split_list_into_chunks

        result = split_list_into_chunks([], 2)
        self.assertEqual(result, [])

    def test_split_list_into_chunks_single(self):
        """Test découpage chunk_size = 1"""
        from app.utils.helpers import split_list_into_chunks

        data = [1, 2, 3]
        result = split_list_into_chunks(data, 1)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], [1])


class TestGenerateId(unittest.TestCase):
    """Tests pour generate_id"""

    def test_generate_id_format(self):
        """Test format UUID généré"""
        from app.utils.helpers import generate_id

        result = generate_id()

        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 36)  # Format UUID standard
        self.assertIn("-", result)

    def test_generate_id_unique(self):
        """Test unicité des IDs"""
        from app.utils.helpers import generate_id

        id1 = generate_id()
        id2 = generate_id()

        self.assertNotEqual(id1, id2)


class TestGetFileExtension(unittest.TestCase):
    """Tests pour get_file_extension"""

    def test_get_file_extension_simple(self):
        """Test extension simple"""
        from app.utils.helpers import get_file_extension

        result = get_file_extension("document.pdf")
        self.assertEqual(result, ".pdf")

    def test_get_file_extension_multiple_dots(self):
        """Test fichier avec plusieurs points"""
        from app.utils.helpers import get_file_extension

        result = get_file_extension("my.file.name.docx")
        self.assertEqual(result, ".docx")

    def test_get_file_extension_no_extension(self):
        """Test fichier sans extension"""
        from app.utils.helpers import get_file_extension

        result = get_file_extension("filename")
        self.assertEqual(result, "")

    def test_get_file_extension_uppercase(self):
        """Test extension majuscules"""
        from app.utils.helpers import get_file_extension

        result = get_file_extension("DOCUMENT.PDF")
        self.assertEqual(result.lower(), ".pdf")


class TestFormatPhoneNumber(unittest.TestCase):
    """Tests pour format_phone_number"""

    def test_format_phone_number_french(self):
        """Test formatage numéro français"""
        from app.utils.helpers import format_phone_number

        result = format_phone_number("0123456789")
        self.assertIn(" ", result)  # Devrait contenir des espaces

    def test_format_phone_number_already_formatted(self):
        """Test numéro déjà formaté"""
        from app.utils.helpers import format_phone_number

        result = format_phone_number("01 23 45 67 89")
        self.assertIsInstance(result, str)


class TestRoundToNearest(unittest.TestCase):
    """Tests pour round_to_nearest"""

    def test_round_to_nearest_basic(self):
        """Test arrondi basique"""
        from app.utils.helpers import round_to_nearest

        result = round_to_nearest(12.3, 5)
        self.assertEqual(result, 10.0)

    def test_round_to_nearest_exact(self):
        """Test arrondi exact"""
        from app.utils.helpers import round_to_nearest

        result = round_to_nearest(15.0, 5)
        self.assertEqual(result, 15.0)

    def test_round_to_nearest_up(self):
        """Test arrondi vers le haut"""
        from app.utils.helpers import round_to_nearest

        result = round_to_nearest(13.0, 5)
        self.assertEqual(result, 15.0)

    def test_round_to_nearest_none(self):
        """Test valeur None"""
        from app.utils.helpers import round_to_nearest

        result = round_to_nearest(None, 5)
        self.assertEqual(result, 0.0)


class TestCalculatePercentageChange(unittest.TestCase):
    """Tests pour calculate_percentage_change"""

    def test_calculate_percentage_change_increase(self):
        """Test augmentation"""
        from app.utils.helpers import calculate_percentage_change

        result = calculate_percentage_change(100, 150)
        self.assertEqual(result, 50.0)

    def test_calculate_percentage_change_decrease(self):
        """Test diminution"""
        from app.utils.helpers import calculate_percentage_change

        result = calculate_percentage_change(100, 75)
        self.assertEqual(result, -25.0)

    def test_calculate_percentage_change_zero_old(self):
        """Test ancienne valeur = 0"""
        from app.utils.helpers import calculate_percentage_change

        result = calculate_percentage_change(0, 100)
        self.assertEqual(result, 0.0)

    def test_calculate_percentage_change_same(self):
        """Test valeurs identiques"""
        from app.utils.helpers import calculate_percentage_change

        result = calculate_percentage_change(100, 100)
        self.assertEqual(result, 0.0)


if __name__ == "__main__":
    unittest.main()
