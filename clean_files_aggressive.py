#!/usr/bin/env python3
"""
Script de nettoyage agressif des fichiers Python
"""
import os
import re

def clean_file_aggressively(filepath):
    """Nettoie agressivement un fichier Python"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            # Supprimer complètement les espaces en fin de ligne
            line = line.rstrip()
            # Supprimer les lignes qui ne contiennent que des espaces
            if line.strip() or line == '':
                cleaned_lines.append(line)

        # Rejoindre les lignes
        content = '\n'.join(cleaned_lines)

        # Supprimer les lignes vides multiples
        content = re.sub(r'\n\n\n+', '\n\n', content)

        # Supprimer les espaces en fin de ligne (double vérification)
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f'❌ Erreur avec {filepath}: {e}')
        return False

def main():
    """Fonction principale"""
    print("🧹 Nettoyage agressif des fichiers Python...")

    count = 0
    modified = 0

    # Traiter tous les fichiers Python dans app/
    for root, dirs, files in os.walk('app'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                count += 1
                if clean_file_aggressively(filepath):
                    modified += 1

    print(f"\n📊 Résultats:")
    print(f"   • Fichiers traités: {count}")
    print(f"   • Fichiers modifiés: {modified}")
    print("🎉 Nettoyage agressif terminé!")

if __name__ == "__main__":
    main()
