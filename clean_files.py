#!/usr/bin/env python3
"""
Script de nettoyage automatique des fichiers Python
Supprime les espaces en fin de ligne et les lignes vides avec espaces
"""
import os
import re

def clean_file(filepath):
    """Nettoie un fichier Python des problèmes de formatage courants"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Supprimer les espaces en fin de ligne
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

        # Supprimer les lignes vides avec seulement des espaces
        content = re.sub(r'^[ \t]+$', '', content, flags=re.MULTILINE)

        # Supprimer les lignes vides multiples (plus de 2 consécutives)
        content = re.sub(r'\n\n\n+', '\n\n', content)

        # Écrire seulement si le contenu a changé
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f'❌ Erreur avec {filepath}: {e}')
        return False

def main():
    """Fonction principale"""
    print("🧹 Nettoyage automatique des fichiers Python...")

    count = 0
    modified = 0

    # Traiter tous les fichiers Python dans app/
    for root, dirs, files in os.walk('app'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                count += 1
                if clean_file(filepath):
                    modified += 1
                    print(f'✅ {filepath}')

    print(f"\n📊 Résultats:")
    print(f"   • Fichiers analysés: {count}")
    print(f"   • Fichiers modifiés: {modified}")
    print("🎉 Nettoyage terminé!")

if __name__ == "__main__":
    main()
