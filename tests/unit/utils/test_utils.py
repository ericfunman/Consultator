"""
Tests complets pour les utilitaires
Couvre les fonctions utilitaires et helpers
"""

import pytest
from datetime import date, datetime
from unittest.mock import Mock, patch, MagicMock
import os
import tempfile
import json

from app.utils.helpers import (
    format_currency, format_date, format_percentage,
    calculate_age, calculate_experience_years,
    validate_email, validate_phone, validate_date,
    safe_divide, round_to_nearest, generate_id,
    clean_string, normalize_text, slugify,
    get_file_extension, is_valid_file_type,
    calculate_percentage_change, format_number,
    truncate_text, split_list_into_chunks
)


class TestFormattingUtils:
    """Tests pour les fonctions de formatage"""

    def test_format_currency(self):
        """Test formatage des montants"""
        assert format_currency(1234.56) == "1 234,56 €"
        assert format_currency(1000000) == "1 000 000,00 €"
        assert format_currency(0) == "0,00 €"
        assert format_currency(-500) == "-500,00 €"

    def test_format_date(self):
        """Test formatage des dates"""
        test_date = date(2023, 12, 25)
        assert format_date(test_date) == "25/12/2023"

        test_datetime = datetime(2023, 12, 25, 14, 30)
        assert format_date(test_datetime) == "25/12/2023"

    def test_format_percentage(self):
        """Test formatage des pourcentages"""
        assert format_percentage(0.85) == "85,0%"
        assert format_percentage(1.0) == "100,0%"
        assert format_percentage(0.123) == "12,3%"
        assert format_percentage(0) == "0,0%"

    def test_format_number(self):
        """Test formatage des nombres"""
        assert format_number(1234) == "1 234"
        assert format_number(1234567) == "1 234 567"
        assert format_number(1234.56) == "1 234,56"
        assert format_number(0) == "0"


class TestCalculationUtils:
    """Tests pour les fonctions de calcul"""

    def test_calculate_age(self):
        """Test calcul de l'âge"""
        birth_date = date(1990, 1, 1)
        current_year = datetime.now().year
        expected_age = current_year - 1990

        assert calculate_age(birth_date) == expected_age

        # Test avec date future (ne devrait pas arriver en prod)
        future_date = date(2030, 1, 1)
        assert calculate_age(future_date) == 0  # Age négatif géré

    def test_calculate_experience_years(self):
        """Test calcul des années d'expérience"""
        start_date = date(2020, 1, 1)
        current_year = datetime.now().year
        expected_years = current_year - 2020

        assert calculate_experience_years(start_date) == expected_years

    def test_safe_divide(self):
        """Test division sécurisée"""
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(10, 0) == 0.0
        assert safe_divide(0, 10) == 0.0
        assert safe_divide(7, 3) == 2.3333333333333335

    def test_round_to_nearest(self):
        """Test arrondi au plus proche"""
        assert round_to_nearest(1.234, 0.1) == 1.2
        assert round_to_nearest(1.234, 0.5) == 1.0
        assert round_to_nearest(1.234, 1) == 1.0
        assert round_to_nearest(1.678, 0.5) == 1.5

    def test_calculate_percentage_change(self):
        """Test calcul du changement en pourcentage"""
        assert calculate_percentage_change(100, 120) == 20.0
        assert calculate_percentage_change(100, 80) == -20.0
        assert calculate_percentage_change(100, 100) == 0.0
        assert calculate_percentage_change(0, 100) == 0.0  # Division par zéro


class TestValidationUtils:
    """Tests pour les fonctions de validation"""

    def test_validate_email(self):
        """Test validation des emails"""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name+tag@example.co.uk") is True
        assert validate_email("invalid-email") is False
        assert validate_email("test@") is False
        assert validate_email("@example.com") is False
        assert validate_email("") is False

    def test_validate_phone(self):
        """Test validation des numéros de téléphone"""
        assert validate_phone("0123456789") is True
        assert validate_phone("+33123456789") is True
        assert validate_phone("01 23 45 67 89") is True
        assert validate_phone("123") is False
        assert validate_phone("abcdefghij") is False
        assert validate_phone("") is False

    def test_validate_date(self):
        """Test validation des dates"""
        assert validate_date("2023-12-25") is True
        assert validate_date("25/12/2023") is True
        assert validate_date("2023-02-30") is False  # Date invalide
        assert validate_date("invalid") is False
        assert validate_date("") is False

    def test_is_valid_file_type(self):
        """Test validation des types de fichiers"""
        assert is_valid_file_type("document.pdf", [".pdf", ".docx"]) is True
        assert is_valid_file_type("image.jpg", [".pdf", ".docx"]) is False
        assert is_valid_file_type("document.PDF", [".pdf", ".docx"]) is True  # Case insensitive
        assert is_valid_file_type("file", [".pdf"]) is False  # Pas d'extension


class TestStringUtils:
    """Tests pour les fonctions de manipulation de chaînes"""

    def test_clean_string(self):
        """Test nettoyage des chaînes"""
        assert clean_string("  Hello World  ") == "Hello World"
        assert clean_string("Hello\n\tWorld") == "Hello World"
        assert clean_string("Hello   World") == "Hello World"
        assert clean_string("") == ""

    def test_normalize_text(self):
        """Test normalisation du texte"""
        assert normalize_text("HÉLLO WÖRLD") == "hello world"
        assert normalize_text("café") == "cafe"
        assert normalize_text("naïve résumé") == "naive resume"

    def test_slugify(self):
        """Test création de slugs"""
        assert slugify("Hello World") == "hello-world"
        assert slugify("Héllo Wörld!") == "hello-world"
        assert slugify("Test   Spaces") == "test-spaces"
        assert slugify("") == ""

    def test_truncate_text(self):
        """Test troncature de texte"""
        text = "This is a long text that should be truncated"
        assert truncate_text(text, 20) == "This is a long te..."
        assert truncate_text(text, 50) == text  # Pas de troncature
        assert truncate_text("Short", 20) == "Short"


class TestFileUtils:
    """Tests pour les fonctions de manipulation de fichiers"""

    def test_get_file_extension(self):
        """Test extraction d'extension de fichier"""
        assert get_file_extension("document.pdf") == ".pdf"
        assert get_file_extension("file.txt") == ".txt"
        assert get_file_extension("FILE.PDF") == ".pdf"
        assert get_file_extension("noextension") == ""
        assert get_file_extension("") == ""


class TestListUtils:
    """Tests pour les fonctions de manipulation de listes"""

    def test_split_list_into_chunks(self):
        """Test division de liste en chunks"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        chunks = split_list_into_chunks(data, 3)
        assert len(chunks) == 4
        assert chunks[0] == [1, 2, 3]
        assert chunks[1] == [4, 5, 6]
        assert chunks[2] == [7, 8, 9]
        assert chunks[3] == [10]

        # Test avec taille de chunk plus grande que la liste
        chunks_large = split_list_into_chunks(data, 20)
        assert len(chunks_large) == 1
        assert chunks_large[0] == data


class TestIdUtils:
    """Tests pour les fonctions de génération d'ID"""

    def test_generate_id(self):
        """Test génération d'ID unique"""
        id1 = generate_id()
        id2 = generate_id()

        assert isinstance(id1, str)
        assert len(id1) > 0
        assert id1 != id2  # IDs doivent être uniques


class TestIntegrationUtils:
    """Tests d'intégration des utilitaires"""

    def test_format_currency_with_calculation(self):
        """Test combinaison formatage et calcul"""
        revenue = 123456.78
        formatted = format_currency(revenue)
        assert formatted == "123 456,78 €"

        # Test avec calcul de pourcentage
        percentage = calculate_percentage_change(100000, revenue)
        formatted_percentage = format_percentage(percentage / 100)
        assert isinstance(formatted_percentage, str)

    def test_validation_chain(self):
        """Test chaîne de validations"""
        # Email valide
        email = "test@example.com"
        assert validate_email(email) is True

        # Numéro de téléphone valide
        phone = "01 23 45 67 89"
        assert validate_phone(phone) is True

        # Date valide
        date_str = "2023-12-25"
        assert validate_date(date_str) is True

    def test_string_processing_chain(self):
        """Test chaîne de traitement de chaînes"""
        text = "  HÉLLO WÖRLD!  "
        cleaned = clean_string(text)
        normalized = normalize_text(cleaned)
        slug = slugify(normalized)

        assert cleaned == "HÉLLO WÖRLD!"
        assert normalized == "hello world!"
        assert slug == "hello-world"

    def test_file_processing_chain(self):
        """Test chaîne de traitement de fichiers"""
        filename = "Document Test.PDF"
        extension = get_file_extension(filename)
        is_valid = is_valid_file_type(filename, [".pdf", ".docx"])

        assert extension == ".pdf"
        assert is_valid is True

    def test_list_processing_chain(self):
        """Test chaîne de traitement de listes"""
        data = list(range(1, 21))  # [1, 2, 3, ..., 20]
        chunks = split_list_into_chunks(data, 5)

        assert len(chunks) == 4
        assert all(len(chunk) <= 5 for chunk in chunks)
        assert sum(len(chunk) for chunk in chunks) == 20

    def test_date_processing_chain(self):
        """Test chaîne de traitement de dates"""
        birth_date = date(1990, 5, 15)
        age = calculate_age(birth_date)
        formatted_date = format_date(birth_date)

        assert isinstance(age, int)
        assert age > 0
        assert formatted_date == "15/05/1990"

    def test_number_processing_chain(self):
        """Test chaîne de traitement de nombres"""
        value = 1234.56789
        formatted = format_number(value)
        rounded = round_to_nearest(value, 0.01)

        assert formatted == "1 234,57"
        assert rounded == 1234.57

    def test_percentage_processing_chain(self):
        """Test chaîne de traitement de pourcentages"""
        old_value = 100
        new_value = 125
        change = calculate_percentage_change(old_value, new_value)
        formatted = format_percentage(change / 100)

        assert change == 25.0
        assert formatted == "25,0%"

    def test_text_processing_chain(self):
        """Test chaîne de traitement de texte"""
        text = "Ceci est un TEXTE de TEST avec des ESPACES!"
        cleaned = clean_string(text)
        normalized = normalize_text(cleaned)
        truncated = truncate_text(normalized, 20)
        slug = slugify(truncated)

        assert len(truncated) <= 23  # 20 + "..." mais peut être moins si rstrip supprime des caractères
        assert "..." in truncated or len(normalized) <= 20
        assert isinstance(slug, str)
        assert " " not in slug

    def test_comprehensive_data_processing(self):
        """Test traitement complet de données"""
        # Simuler des données de consultant
        consultant_data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@test.com",
            "telephone": "01 23 45 67 89",
            "salaire": 50000.50,
            "date_naissance": date(1990, 1, 1),
            "description": "Consultant expérimenté en Python"
        }

        # Traiter chaque champ
        processed_data = {
            "nom_complet": f"{consultant_data['prenom']} {consultant_data['nom']}",
            "email_valide": validate_email(consultant_data['email']),
            "telephone_valide": validate_phone(consultant_data['telephone']),
            "salaire_formatte": format_currency(consultant_data['salaire']),
            "age": calculate_age(consultant_data['date_naissance']),
            "date_naissance_formatee": format_date(consultant_data['date_naissance']),
            "description_normalisee": normalize_text(consultant_data['description'])
        }

        # Vérifications
        assert processed_data["nom_complet"] == "Jean Dupont"
        assert processed_data["email_valide"] is True
        assert processed_data["telephone_valide"] is True
        assert processed_data["salaire_formatte"] == "50 000,50 €"
        assert isinstance(processed_data["age"], int)
        assert processed_data["date_naissance_formatee"] == "01/01/1990"
        assert processed_data["description_normalisee"] == "consultant experimente en python"