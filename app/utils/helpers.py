"""
Fonctions utilitaires générales pour Consultator
Fonctions de formatage, validation, calcul et manipulation de données
"""

import math
import os
import re
import unicodedata
import uuid
from datetime import date
from datetime import datetime


def format_currency(amount: float) -> str:
    """
    Formate un montant en euros avec séparateur de milliers

    Args:
        amount: Montant à formater

    Returns:
        Chaîne formatée en euros
    """
    if amount is None:
        return "0,00 €"

    try:
        # Format français : 1 234,56 €
        formatted = f"{amount:,.2f}".replace(",", " ").replace(".", ",")
        return f"{formatted} €"
    except (ValueError, TypeError):
        return "0,00 €"


def format_date(date_obj) -> str:
    """
    Formate une date en format français JJ/MM/AAAA

    Args:
        date_obj: Objet date ou datetime

    Returns:
        Chaîne formatée JJ/MM/AAAA
    """
    if date_obj is None:
        return ""

    try:
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%d/%m/%Y")
        elif isinstance(date_obj, date):
            return date_obj.strftime("%d/%m/%Y")
        else:
            return str(date_obj)
    except (ValueError, AttributeError):
        return ""


def format_percentage(value: float) -> str:
    """
    Formate un pourcentage

    Args:
        value: Valeur entre 0 et 1 (0.85 pour 85%)

    Returns:
        Chaîne formatée en pourcentage
    """
    if value is None:
        return "0,0%"

    try:
        percentage = value * 100
        return f"{percentage:.1f}%".replace(".", ",")
    except (ValueError, TypeError):
        return "0,0%"


def format_number(value: float) -> str:
    """
    Formate un nombre avec séparateur de milliers

    Args:
        value: Nombre à formater

    Returns:
        Chaîne formatée avec séparateurs
    """
    if value is None:
        return "0"

    try:
        # Vérifier si c'est un entier ou un flottant
        if isinstance(value, float) and value != int(value):
            # Pour les flottants, garder 2 décimales si nécessaire
            if value == int(value):
                return f"{int(value):,}".replace(",", " ")
            else:
                return f"{value:,.2f}".replace(",", " ").replace(".", ",")
        else:
            # Pour les entiers
            return f"{int(value):,}".replace(",", " ")
    except (ValueError, TypeError):
        return "0"


def calculate_age(birth_date: date) -> int:
    """
    Calcule l'âge à partir de la date de naissance

    Args:
        birth_date: Date de naissance

    Returns:
        Âge en années
    """
    if birth_date is None:
        return 0

    try:
        today = date.today()
        age = today.year - birth_date.year

        # Ajustement si l'anniversaire n'est pas encore passé cette année
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return max(0, age)
    except (AttributeError, TypeError):
        return 0


def calculate_experience_years(start_date: date) -> int:
    """
    Calcule les années d'expérience à partir de la date de début

    Args:
        start_date: Date de début d'expérience

    Returns:
        Années d'expérience
    """
    if start_date is None:
        return 0

    try:
        today = date.today()
        experience = today.year - start_date.year

        # Ajustement si la date anniversaire n'est pas encore passée
        if (today.month, today.day) < (start_date.month, start_date.day):
            experience -= 1

        return max(0, experience)
    except (AttributeError, TypeError):
        return 0


def safe_divide(numerator: float, denominator: float) -> float:
    """
    Division sécurisée évitant la division par zéro

    Args:
        numerator: Numérateur
        denominator: Dénominateur

    Returns:
        Résultat de la division ou 0 si division par zéro
    """
    try:
        if denominator == 0 or denominator is None:
            return 0.0
        return numerator / denominator
    except (ZeroDivisionError, TypeError):
        return 0.0


def round_to_nearest(value: float, nearest: float) -> float:
    """
    Arrondi à la valeur la plus proche

    Args:
        value: Valeur à arrondir
        nearest: Valeur de référence pour l'arrondi

    Returns:
        Valeur arrondie
    """
    if value is None or nearest is None or nearest == 0:
        return value or 0.0

    try:
        # Utiliser decimal pour éviter les problèmes de précision flottante
        from decimal import ROUND_HALF_UP
        from decimal import Decimal, InvalidOperation

        result = Decimal(str(value)) / Decimal(str(nearest))
        result = result.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        result = result * Decimal(str(nearest))
        return float(result)
    except (ZeroDivisionError, TypeError, ValueError, InvalidOperation):
        return value or 0.0


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calcule le changement en pourcentage

    Args:
        old_value: Valeur ancienne
        new_value: Valeur nouvelle

    Returns:
        Changement en pourcentage
    """
    try:
        if old_value == 0 or old_value is None:
            return 0.0
        return ((new_value - old_value) / old_value) * 100
    except (ZeroDivisionError, TypeError):
        return 0.0


def validate_email(email: str) -> bool:
    """
    Valide un format d'email

    Args:
        email: Adresse email à valider

    Returns:
        True si l'email est valide
    """
    if not email or not isinstance(email, str):
        return False

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email.strip()) is not None


def validate_phone(phone: str) -> bool:
    """
    Valide un numéro de téléphone français

    Args:
        phone: Numéro de téléphone à valider

    Returns:
        True si le numéro est valide
    """
    if not phone or not isinstance(phone, str):
        return False

    # Nettoyer les espaces et caractères spéciaux
    cleaned = re.sub(r"[\s\-\(\)\.]", "", phone.strip())

    # Formats acceptés : 10 chiffres, ou +33 suivi de 9 chiffres
    if cleaned.startswith("+33"):
        return len(cleaned) == 12 and cleaned[3:].isdigit()
    else:
        return len(cleaned) == 10 and cleaned.isdigit()


def validate_date(date_str: str) -> bool:
    """
    Valide une chaîne de date

    Args:
        date_str: Chaîne de date à valider

    Returns:
        True si la date est valide
    """
    if not date_str or not isinstance(date_str, str):
        return False

    try:
        # Essayer différents formats
        for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        return False
    except (TypeError, AttributeError):
        return False


def is_valid_file_type(filename: str, allowed_extensions: list) -> bool:
    """
    Vérifie si l'extension du fichier est autorisée

    Args:
        filename: Nom du fichier
        allowed_extensions: Liste des extensions autorisées (avec point)

    Returns:
        True si l'extension est autorisée
    """
    if not filename or not allowed_extensions:
        return False

    try:
        _, ext = os.path.splitext(filename.lower())
        return ext in [e.lower() for e in allowed_extensions]
    except (AttributeError, TypeError):
        return False


def clean_string(text: str) -> str:
    """
    Nettoie une chaîne de caractères

    Args:
        text: Texte à nettoyer

    Returns:
        Texte nettoyé
    """
    if not text or not isinstance(text, str):
        return ""

    # Supprimer les espaces en début et fin
    cleaned = text.strip()

    # Remplacer les espaces multiples par un seul
    cleaned = re.sub(r"\s+", " ", cleaned)

    # Supprimer les caractères de contrôle
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned)

    return cleaned


def normalize_text(text: str) -> str:
    """
    Normalise un texte (minuscules, suppression accents)

    Args:
        text: Texte à normaliser

    Returns:
        Texte normalisé
    """
    if not text or not isinstance(text, str):
        return ""

    # Convertir en minuscules
    normalized = text.lower()

    # Supprimer les accents
    normalized = unicodedata.normalize("NFD", normalized)
    normalized = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )

    return normalized


def slugify(text: str) -> str:
    """
    Crée un slug à partir d'un texte

    Args:
        text: Texte à convertir en slug

    Returns:
        Slug généré
    """
    if not text or not isinstance(text, str):
        return ""

    # Normaliser le texte
    normalized = normalize_text(text)

    # Remplacer les espaces et caractères spéciaux par des tirets
    slug = re.sub(r"[^a-z0-9]+", "-", normalized)

    # Supprimer les tirets en début et fin
    slug = slug.strip("-")

    return slug


def truncate_text(text: str, max_length: int) -> str:
    """
    Tronque un texte à une longueur maximale

    Args:
        text: Texte à tronquer
        max_length: Longueur maximale

    Returns:
        Texte tronqué avec "..." si nécessaire
    """
    if not text or not isinstance(text, str):
        return ""

    if len(text) <= max_length:
        return text

    # Tronquer et ajouter "..."
    # Garder assez d'espace pour "..."
    if max_length <= 3:
        return text[:max_length]

    truncated = text[: max_length - 3].rstrip()
    # Si après rstrip on a perdu des caractères, essayer de récupérer
    if len(truncated) < max_length - 3 and len(text) > len(truncated):
        additional_chars = (max_length - 3) - len(truncated)
        truncated = text[: len(truncated) + additional_chars].rstrip()

    return truncated + "..."


def split_list_into_chunks(data: list, chunk_size: int) -> list:
    """
    Divise une liste en chunks de taille donnée

    Args:
        data: Liste à diviser
        chunk_size: Taille de chaque chunk

    Returns:
        Liste de chunks
    """
    if not data or not isinstance(data, list) or chunk_size <= 0:
        return []

    try:
        return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]
    except (TypeError, ValueError):
        return []


def generate_id() -> str:
    """
    Génère un identifiant unique

    Returns:
        Identifiant UUID
    """
    return str(uuid.uuid4())


def get_file_extension(filename: str) -> str:
    """
    Extrait l'extension d'un fichier

    Args:
        filename: Nom du fichier

    Returns:
        Extension avec le point (ex: ".pdf")
    """
    if not filename or not isinstance(filename, str):
        return ""

    try:
        _, ext = os.path.splitext(filename)
        return ext.lower()
    except (AttributeError, TypeError):
        return ""
