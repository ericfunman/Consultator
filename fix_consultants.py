#!/usr/bin/env python3
"""
Script pour corriger les problèmes dans consultants.py
"""


def fix_encoding_issues():
    """Corrige les problèmes d'encodage des emojis"""

    replacements = {
        "👥": "👥",
        "👤": "👤",
        "📋": "📋",
        "➕": "➕",
        "📄": "📄",
        "🧪": "🧪",
        "💡": "💡",
        "🚀": "🚀",
        "←": "←",
        "✅": "✅",
        "❌": "❌",
        "💰": "💰",
        "📊": "📊",
        "📅": "📅",
        "💼": "💼",
        "🚀": "🚀",
        "🛠️": "🛠️",
        "📝": "📝",
        "📞": "📞",
        "📧": "📧",
        "🗑️": "🗑️",
        "✏️": "✏️",
        "🏢": "🏢",
        "💾": "💾",
        "📥": "📥",
        "ℹ️": "ℹ️",
        "🔍": "🔍",
        "⏸️": "⏸️",
        "⚙️": "⚙️",
        "Gérez": "Gérez",
        "Vérifier": "Vérifier",
        "spécifique": "spécifique",
        "fonctionnalités": "fonctionnalités",
        "organisé": "organisé",
        "terminée": "terminée",
        "Dernières": "Dernières",
        "ajoutées": "ajoutées",
        "détectées": "détectées",
        "modifié": "modifié",
        "supprimée": "supprimée",
        "supprimé": "supprimé",
        "ajoutée": "ajoutée",
        "évités": "évités",
        "création": "création",
        "définitivement": "définitivement",
        "associées": "associées",
        "Rôle": "Rôle",
        "spécifié": "spécifié",
        "spécifiées": "spécifiées",
        "Début": "Début",
        "€": "€",
    }

    file_path = "app/pages_modules/consultants.py"

    try:
        # Lire le fichier
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Appliquer les remplacements
        for old, new in replacements.items():
            content = content.replace(old, new)

        # Réécrire le fichier
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("✅ Correction d'encodage appliquée avec succès")

    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")


if __name__ == "__main__":
    fix_encoding_issues()
