#!/usr/bin/env python3
"""
Tests rapides pour app/utils/helpers.py
Amélioration couverture 72% → 90%+
"""

import unittest
from datetime import date, datetime
import pandas as pd

from app.utils.helpers import (
    format_currency, format_date, format_percentage, format_number,
    calculate_age, calculate_experience_years, safe_divide,
    round_to_nearest, calculate_percentage_change, validate_email,
    validate_phone, validate_date, is_valid_file_type, clean_string,
    normalize_text, slugify, truncate_text, split_list_into_chunks,
    get_file_extension, format_phone_number, format_date_french,
    sanitize_input, calculate_mission_duration, calculate_tjm,
    convert_to_dataframe
)


class TestHelpers(unittest.TestCase):
    """Tests rapides pour fonctions helpers"""

    def test_format_currency(self):
        self.assertEqual(format_currency(1000), "1 000 €")
        self.assertEqual(format_currency(1234.56), "1 235 €")
        self.assertEqual(format_currency(0), "0 €")

    def test_format_date(self):
        test_date = datetime(2024, 10, 6)
        self.assertEqual(format_date(test_date), "06/10/2024")

    def test_format_percentage(self):
        self.assertEqual(format_percentage(0.5), "50.0%")
        self.assertEqual(format_percentage(1), "100.0%")

    def test_format_number(self):
        self.assertEqual(format_number(1000), "1 000")
        self.assertEqual(format_number(1234567), "1 234 567")

    def test_calculate_age(self):
        birth = date(1990, 1, 1)
        age = calculate_age(birth)
        self.assertGreater(age, 30)

    def test_calculate_experience_years(self):
        start = date(2020, 1, 1)
        exp = calculate_experience_years(start)
        self.assertGreater(exp, 3)

    def test_safe_divide(self):
        self.assertEqual(safe_divide(10, 2), 5.0)
        self.assertEqual(safe_divide(10, 0), 0.0)

    def test_round_to_nearest(self):
        self.assertEqual(round_to_nearest(123, 10), 120)
        self.assertEqual(round_to_nearest(127, 10), 130)

    def test_calculate_percentage_change(self):
        self.assertEqual(calculate_percentage_change(100, 150), 50.0)
        self.assertEqual(calculate_percentage_change(100, 100), 0.0)

    def test_validate_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid"))

    def test_validate_phone(self):
        self.assertTrue(validate_phone("0601020304"))
        self.assertFalse(validate_phone("123"))

    def test_validate_date(self):
        self.assertTrue(validate_date("2024-10-06"))
        self.assertFalse(validate_date("invalid"))

    def test_is_valid_file_type(self):
        self.assertTrue(is_valid_file_type("doc.pdf", [".pdf", ".docx"]))
        self.assertFalse(is_valid_file_type("doc.exe", [".pdf", ".docx"]))

    def test_clean_string(self):
        result = clean_string("  Hello  World  ")
        self.assertEqual(result, "Hello World")

    def test_normalize_text(self):
        result = normalize_text("Café")
        self.assertIn("cafe", result.lower())

    def test_slugify(self):
        result = slugify("Hello World!")
        self.assertEqual(result, "hello-world")

    def test_truncate_text(self):
        result = truncate_text("Hello World", 5)
        self.assertEqual(result, "Hello...")

    def test_split_list_into_chunks(self):
        data = [1, 2, 3, 4, 5]
        chunks = split_list_into_chunks(data, 2)
        self.assertEqual(len(chunks), 3)

    def test_get_file_extension(self):
        self.assertEqual(get_file_extension("test.pdf"), ".pdf")
        self.assertEqual(get_file_extension("noext"), "")

    def test_format_phone_number(self):
        result = format_phone_number("0601020304")
        self.assertIn("06", result)

    def test_format_date_french(self):
        test_date = datetime(2024, 10, 6)
        result = format_date_french(test_date)
        self.assertIn("2024", result)

    def test_sanitize_input(self):
        result = sanitize_input("<script>alert('XSS')</script>")
        self.assertNotIn("<script>", result)

    def test_calculate_mission_duration(self):
        start = date(2024, 1, 1)
        end = date(2024, 1, 31)
        duration = calculate_mission_duration(start, end)
        self.assertEqual(duration, 30)

    def test_calculate_tjm(self):
        tjm = calculate_tjm(50000)
        self.assertGreater(tjm, 200)

    def test_convert_to_dataframe(self):
        data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
        df = convert_to_dataframe(data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)


if __name__ == "__main__":
    unittest.main()
